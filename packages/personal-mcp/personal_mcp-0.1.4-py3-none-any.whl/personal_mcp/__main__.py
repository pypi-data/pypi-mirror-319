import sys

from .cli import cli


def main():
    """Main entry point for the Personal MCP server."""
    cli.main(standalone_mode=False)


if __name__ == "__main__":
    sys.exit(main())
