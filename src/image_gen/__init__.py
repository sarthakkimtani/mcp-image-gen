from . import server
import asyncio

def main():
    """Main entry point for the server."""
    asyncio.run(server.main())

__all__ = ['main', 'server']
