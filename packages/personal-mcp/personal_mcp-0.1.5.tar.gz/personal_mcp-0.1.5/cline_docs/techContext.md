# Technical Context

## Technologies Used

### Core Technologies
- Python 3.10+ (required)
- Model Context Protocol (MCP) SDK 1.2.0+
- SQLite (for data storage)

### Key Dependencies
- mcp>=0.1.0 (MCP SDK)
- pandas>=2.0.0 (Data analysis)
- pydantic>=2.0.0 (Data validation)
- click>=8.0.0 (CLI interface)
- rich>=10.0.0 (Terminal UI)

### Development Tools
- pytest (Testing)
- black (Code formatting)
- ruff (Linting)
- mypy (Type checking)
- pre-commit (Git hooks)

## Development Setup

### Installation Methods
1. Via Smithery:
   ```bash
   npx -y @smithery/cli install personal-mcp --client claude
   ```

2. Via pip:
   ```bash
   pip install -e .
   ```

3. Development Mode:
   ```bash
   uv pip install -e ".[dev]"
   ```

### Running Modes
1. Basic Server:
   ```bash
   personal-mcp run
   ```

2. Development Mode:
   ```bash
   personal-mcp dev
   ```

3. Inspector Mode:
   ```bash
   personal-mcp inspect
   ```

## Technical Constraints

### Python Version
- Minimum: Python 3.10
- Supported: 3.10, 3.11

### Code Quality Standards
- Line length: 100 characters
- Type hints: Required (strict mypy checking)
- Test coverage: Required
- Code formatting: black
- Linting: ruff with E, F, B, I rules

### MCP Configuration
- Server name: "personal-mcp"
- Development mode available
- Inspector mode supported
- Resource subscription enabled
- Tool list change notifications enabled
- Logging configuration:
  * Logs directed to stderr
  * MCP messages on stdout
  * Uvicorn access logs disabled
  * Rich console formatting
  * Log level: info (debug in verbose mode)

### Build System
- Backend: hatchling
- Wheel package structure: src/personal_mcp
- Direct references allowed in metadata
