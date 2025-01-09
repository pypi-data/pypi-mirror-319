# System Patterns

## Architecture Overview

### Core Components
1. **MCP Server Layer** (server.py)
   - Handles MCP protocol communication
   - Manages tool and resource registration
   - Implements capability handling
   - Processes client requests

2. **Database Layer** (database.py)
   - SQLite-based storage
   - Handles data persistence
   - Manages relationships between entities
   - Implements query patterns

3. **Models Layer** (models.py)
   - Pydantic models for data validation
   - Type-safe data structures
   - Schema definitions
   - Data transformation logic

4. **Tools Layer** (tools/)
   - Modular tool implementation
   - Domain-specific logic
   - Separate concerns by health aspect
   - Standardized tool interfaces

### Tool Architecture
Each tool module follows a consistent pattern:
```
tools/
├── workout.py
├── nutrition.py
└── journal.py
```

Each implements:
- Tool registration
- Input validation
- Business logic
- Data persistence
- Response formatting

## Key Technical Decisions

### 1. Data Storage
- **Choice**: SQLite
- **Rationale**: 
  - Local storage for privacy
  - No server dependencies
  - ACID compliance
  - Simple deployment

### 2. Code Organization
- **Pattern**: src-layout
- **Benefits**:
  - Clear separation of source and tests
  - Proper package installation
  - Development mode support
  - Clean import paths

### 3. Type System
- **Approach**: Strict typing
- **Implementation**:
  - Pydantic for data validation
  - MyPy for static analysis
  - Runtime type checking
  - Complete type coverage

### 4. Tool Implementation
- **Pattern**: Modular tools
- **Structure**:
  - Independent modules
  - Standardized interfaces
  - Self-contained logic
  - Clear responsibility boundaries

### 5. Testing Strategy
- **Framework**: pytest
- **Coverage**: Required
- **Patterns**:
  - Async test support
  - Fixture-based setup
  - Integration tests
  - Unit test isolation

## Communication Patterns

### 1. MCP Protocol
- Standardized tool interfaces
- Resource subscription support
- Capability negotiation
- Event notifications

### 2. Data Flow
```
Client Request -> MCP Server -> Tool Handler -> Database -> Response
```

### 3. Error Handling
- Structured error responses
- Error code standardization
- Detailed error messages
- Error recovery patterns

## Development Patterns

### 1. Code Quality
- Pre-commit hooks
- Automated formatting
- Linting enforcement
- Type checking

### 2. Documentation
- Inline documentation
- API documentation
- Usage examples
- Type hints

### 3. Testing
- Test-driven development
- Comprehensive coverage
- Integration testing
- Performance testing