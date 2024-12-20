from typing import Any, Optional
import asyncio
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import os

TOGETHER_AI_BASE = "https://api.together.xyz/v1/images/generations"
API_KEY = os.getenv("TOGETHER_AI_API_KEY")

server = Server("image-gen")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="generate_image",
            description="Generate an image based on the text prompt",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "The text prompt for image generation"},
                    "width": {"type": "number", "description": "Optional width for the image"},
                    "height": {"type": "number", "description": "Optional height for the image"}
                },
                "required": ["prompt"]
            },
        )
    ]

async def make_together_request(client: httpx.AsyncClient, prompt: str, width: Optional[int] = None, height: Optional[int] = None) -> dict[str, Any]:
    """ Make a request to the Together API with proper error handling. """
    request_body = {
        "model": "black-forest-labs/FLUX.1-schnell",
        "prompt": prompt,
        "response_format": "b64_json"
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    if width is not None:
        request_body["width"] = width
    if height is not None:
        request_body["height"] = height
        
    try:
        response = await client.post(TOGETHER_AI_BASE, headers=headers, json=request_body)
        response.raise_for_status()
        
        if response.status_code == 429:
            return {"error": f"Rate limit exceeded. Error details: {response.text}"}
        elif response.status_code == 401:
            return {"error": f"API key invalid or expired. Error details: {response.text}"}
            
        data = response.json()
        if "error" in data:
            return {"error": f"Together API error: {data['error']}"}
        return data
        
    except httpx.TimeoutException:
        return {"error": "Request timed out. API may be experiencing delays."}
    except httpx.ConnectError:
        return {"error": "Failed to connect to API. Please check your internet connection."}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error occurred: {str(e)} - Response: {e.response.text}"}
    except Exception as e:
        return {"error": f"Unexpected error occurred: {str(e)}"}

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can generate images and notify clients of changes.
    """
    if not arguments:
        return [types.TextContent(type="text", text="Missing arguments for the request")]
        
    if name == "generate_image":
        prompt = arguments.get("prompt")
        width = arguments.get("width")
        height = arguments.get("height")
        
        if not prompt:
            return [types.TextContent(type="text", text="Missing prompt parameter")]
            
        async with httpx.AsyncClient() as client:
            response_data = await make_together_request(client=client, prompt=prompt, width=width, height=height)
            
            if "error" in response_data:
                return [types.TextContent(type="text", text=response_data["error"])]
                
            try:
                b64_image = response_data["data"][0]["b64_json"]
                return [types.ImageContent(type="image", data=b64_image, mimeType="image/jpeg")]
            except (KeyError, IndexError) as e:
                return [types.TextContent(type="text", text=f"Failed to parse API response: {e}")]


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="image-gen",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
