# MCP Server Evaluation Guidelines

This guide covers evaluating MCP server implementations for quality, security, and best practices compliance.

## Evaluation Checklist

### 1. Server Configuration

| Criteria | Check | Pass/Fail |
|----------|-------|-----------|
| Server name | Unique, descriptive name | Must pass |
| Version | Semantic versioning (x.y.z) | Must pass |
| Description | Clear, concise purpose | Must pass |
| Capabilities | Accurately declared capabilities | Must pass |

### 2. Tool Implementation

#### InputSchema Validation

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search query"
    },
    "limit": {
      "type": "number",
      "description": "Maximum results",
      "default": 10
    }
  },
  "required": ["query"]
}
```

**Must:**
- Define all parameters
- Include descriptions for all properties
- Specify required parameters
- Use appropriate types (string, number, boolean, object, array)

#### OutputSchema Validation

```json
{
  "content": [
    {
      "type": "text",
      "text": "..."
    }
  ],
  "isError": false
}
```

**Must:**
- Return content array
- Each item has type field
- Include isError for error conditions
- Use structured errors (not just strings)

### 3. Error Handling

#### Proper Error Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Error: Invalid parameter 'query' - must be a non-empty string"
    }
  ],
  "isError": true
}
```

**Should:**
- Include error type in message
- Provide actionable guidance
- Log errors for debugging
- Not expose internal implementation details

### 4. Resource Implementation

#### Resource Metadata

```json
{
  "uri": "file:///path/to/resource",
  "name": "Descriptive Name",
  "description": "What this resource provides",
  "mimeType": "text/plain"
}
```

**Must:**
- Use valid URI scheme
- Include name and description
- Specify mimeType
- Handle read errors gracefully

### 5. Security Considerations

| Security Check | Description |
|----------------|-------------|
| Input sanitization | All user inputs are validated and sanitized |
| Output filtering | No sensitive data leaked in responses |
| Rate limiting | Prevents abuse through excessive requests |
| Authentication | If required, uses secure authentication |
| Authorization | Enforces proper access controls |

### 6. Performance

| Performance Check | Target |
|-------------------|--------|
| Response time | < 500ms for typical operations |
| Memory usage | Minimal memory footprint |
| Resource cleanup | Properly closes resources |
| Concurrent connections | Handles multiple connections gracefully |

### 7. Documentation

**README.md must include:**
1. Installation instructions
2. Configuration options
3. Available tools and their parameters
4. Available resources
5. Usage examples
6. Error handling guidance
7. Security considerations
8. License information

### 8. Testing

**Test coverage must include:**
1. Happy path for each tool
2. Invalid parameter handling
3. Resource not found cases
4. Edge cases (empty inputs, large inputs)
5. Error conditions
6. Integration tests with real MCP client

### 9. Version Compatibility

| MCP Version | Compatibility |
|-------------|---------------|
| Spec version | Must match spec version in server config |
| SDK version | Must use compatible SDK version |
| Breaking changes | Must be documented in CHANGELOG |

### 10. Packaging

**Package.json requirements:**
```json
{
  "name": "@org/mcp-server-name",
  "version": "1.0.0",
  "description": "Clear description",
  "bin": {
    "mcp-server-name": "./dist/index.js"
  },
  "files": ["dist", "README.md", "LICENSE"],
  "engines": {
    "node": ">=18"
  }
}
```

## Evaluation Process

### Step 1: Automated Checks

```bash
# Type checking
npm run typecheck

# Linting
npm run lint

# Tests
npm test

# Build
npm run build
```

### Step 2: Manual Review

1. Review tool definitions for clarity and completeness
2. Check error messages for usefulness
3. Verify security practices
4. Test with real data
5. Review documentation quality

### Step 3: Integration Testing

```bash
# Install in test environment
npm link

# Test with Claude Desktop or other MCP client
# Verify tool execution and resource access
```

### Step 4: Security Audit

1. Review input validation code
2. Check for hardcoded credentials
3. Verify output sanitization
4. Test with malformed inputs
5. Review network requests for data leaks

## Common Issues

### 1. Missing Error Handling

```typescript
// BAD: No error handling
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const result = someOperation(request.params.arguments);
  return { content: [{ type: "text", text: result }] };
});

// GOOD: Proper error handling
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const result = someOperation(request.params.arguments);
    return { content: [{ type: "text", text: result }] };
  } catch (error) {
    return {
      content: [{ type: "text", text: `Error: ${error.message}` }],
      isError: true
    };
  }
});
```

### 2. Incomplete Input Schema

```json
// BAD: Missing descriptions
{
  "type": "object",
  "properties": {
    "query": { "type": "string" }
  }
}

// GOOD: Complete with descriptions
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search query string"
    }
  },
  "required": ["query"]
}
```

### 3. Resource URI Issues

```json
// BAD: Invalid URI scheme
{
  "uri": "/path/to/file"
}

// GOOD: Proper URI scheme
{
  "uri": "file:///path/to/file"
}
```

## Evaluation Rubric

| Category | Weight | Score (1-5) | Weighted Score |
|----------|--------|-------------|----------------|
| Correctness | 30% | - | - |
| Security | 25% | - | - |
| Performance | 15% | - | - |
| Documentation | 15% | - | - |
| Testing | 15% | - | - |
| **Total** | **100%** | - | - |

**Pass threshold:** 3.5/5 weighted average

## Certification Process

1. **Self-assessment:** Developer completes checklist
2. **Automated testing:** Run all tests
3. **Peer review:** Another developer reviews code
4. **Integration test:** Test with real MCP client
5. **Security review:** Check for common vulnerabilities
6. **Documentation review:** Verify completeness
7. **Certification:** Add to approved servers list

## Post-Evaluation

### For Passing Servers

1. Add to skill documentation
2. Publish to package repository
3. Register in MCP server directory (if applicable)
4. Add usage examples to documentation

### For Failing Servers

1. Document specific issues found
2. Provide remediation guidance
3. Offer follow-up evaluation after fixes
4. Block publication until issues resolved