# Image Generation MCP Server

A Model Context Protocol (MCP) server that enables seamless generation of high-quality images via Together AI. This server provides a standardized interface to specify image generation parameters.

<a href="https://glama.ai/mcp/servers/o0137xiz62">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/o0137xiz62/badge" alt="Image Generation Server MCP server" />
</a>

## Features

- High-quality image generation powered by the Flux.1 Schnell model
- Support for customizable dimensions (width and height)
- Clear error handling for prompt validation and API issues
- Easy integration with MCP-compatible clients

## Installation

#### Claude Desktop

- On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<summary>Development/Unpublished Servers Configuration</summary>

```json
{
  "mcpServers": {
    "image-gen": {
      "command": "uv",
      "args": ["--directory", "/ABSOLUTE/PATH/TO/image-gen/", "run", "image-gen"],
      "env": {
        "TOGETHER_AI_API_KEY": "<API KEY>"
      }
    }
  }
}
```

## Available Tools

The server implements one tool:

### generate_image

Generates an image based on the given textual prompt and optional dimensions.

**Input Schema:**

```json
{
  "prompt": {
    "type": "string",
    "description": "A descriptive prompt for generating the image (e.g., 'a futuristic cityscape at sunset')"
  },
  "width": {
    "type": "integer",
    "description": "Width of the generated image in pixels (optional)"
  },
  "height": {
    "type": "integer",
    "description": "Height of the generated image in pixels (optional)"
  },
  "model": {
    "type": "string",
    "description": "The exact model name as it appears in Together AI. If incorrect, it will fallback to the default model (black-forest-labs/FLUX.1-schnell)."
  }
}
```

## Prerequisites

- Python 3.12 or higher
- httpx
- mcp

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch (`feature/my-new-feature`)
3. Commit your changes
4. Push the branch to your fork
5. Open a Pull Request

For significant changes, please open an issue first to discuss your proposed changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.