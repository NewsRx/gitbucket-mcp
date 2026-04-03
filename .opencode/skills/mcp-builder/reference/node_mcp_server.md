# Node.js MCP Server Implementation

This guide covers implementing MCP servers using Node.js/TypeScript.

## Prerequisites

- Node.js 18+ (LTS recommended)
- TypeScript 5.0+
- npm or pnpm package manager

## Project Setup

### Initialize Project

```bash
mkdir my-mcp-server
cd my-mcp-server
npm init -y
npm install typescript @types/node --save-dev
npm install @modelcontextprotocol/sdk zod
npx tsc --init
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Server Structure

### Basic Server (src/index.ts)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Define server capabilities
const server = new Server(
  {
    name: "my-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// Tool implementations
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "example_tool",
        description: "An example tool",
        inputSchema: {
          type: "object" as const,
          properties: {
            query: {
              type: "string",
              description: "Query parameter",
            },
          },
          required: ["query"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "example_tool") {
    const { query } = request.params.arguments as { query: string };
    return {
      content: [
        {
          type: "text",
          text: `Result for: ${query}`,
        },
      ],
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Resource implementations
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "file:///example.txt",
        name: "Example Resource",
        mimeType: "text/plain",
      },
    ],
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  if (request.params.uri === "file:///example.txt") {
    return {
      contents: [
        {
          uri: "file:///example.txt",
          mimeType: "text/plain",
          text: "Example resource content",
        },
      ],
    };
  }
  throw new Error(`Unknown resource: ${request.params.uri}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

## Input Validation with Zod

```typescript
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

// Define input schema
const ExampleToolSchema = z.object({
  query: z.string().describe("Search query"),
  limit: z.number().optional().default(10).describe("Maximum results"),
});

// Convert to JSON Schema for tool definition
const exampleToolInputSchema = zodToJsonSchema(ExampleToolSchema);

// Validate in handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "example_tool") {
    const args = ExampleToolSchema.parse(request.params.arguments);
    // Process validated args
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ query: args.query, limit: args.limit }),
        },
      ],
    };
  }
});
```

## Environment Variables

```typescript
import dotenv from "dotenv";

// Load .env file
dotenv.config();

// Validate required environment variables
const config = {
  apiKey: process.env.API_KEY,
  apiEndpoint: process.env.API_ENDPOINT || "https://api.example.com",
};

if (!config.apiKey) {
  throw new Error("API_KEY environment variable is required");
}
```

## Error Handling

```typescript
import { McpError } from "@modelcontextprotocol/sdk/types.js";

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    // Tool logic
  } catch (error) {
    if (error instanceof z.ZodError) {
      throw new McpError(
        ErrorCode.InvalidParams,
        `Validation error: ${error.message}`
      );
    }
    throw new McpError(
      ErrorCode.InternalError,
      `Tool execution failed: ${error instanceof Error ? error.message : String(error)}`
    );
  }
});
```

## Package.json Scripts

```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsc --watch",
    "test": "jest",
    "lint": "eslint src/**/*.ts",
    "format": "prettier --write \"src/**/*.ts\""
  },
  "bin": {
    "my-mcp-server": "./dist/index.js"
  }
}
```

## Publishing

### package.json Configuration

```json
{
  "name": "@yourorg/my-mcp-server",
  "version": "1.0.0",
  "description": "MCP server for ...",
  "type": "module",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "bin": {
    "my-mcp-server": "./dist/index.js"
  },
  "files": ["dist", "README.md", "LICENSE"],
  "keywords": ["mcp", "model-context-protocol", "ai"],
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourorg/my-mcp-server.git"
  }
}
```

### Publishing Steps

```bash
# Build
npm run build

# Test locally
npm link
my-mcp-server --help

# Publish to npm
npm login
npm publish --access public
```

## Testing

### Jest Configuration (jest.config.js)

```javascript
module.exports = {
  preset: "ts-jest",
  testEnvironment: "node",
  moduleFileExtensions: ["ts", "js"],
  testMatch: ["**/*.test.ts"],
};
```

### Example Test (src/index.test.ts)

```typescript
import { describe, it, expect } from "@jest/globals";

describe("Example Tool", () => {
  it("should return result for valid input", async () => {
    // Test implementation
  });
});
```

## Best Practices

1. **Use TypeScript** for type safety and better IDE support
2. **Validate inputs** with Zod schemas
3. **Document all tools** with clear descriptions
4. **Handle errors gracefully** using McpError
5. **Use environment variables** for configuration
6. **Add shebang** (`#!/usr/bin/env node`) to compiled entry point
7. **Test thoroughly** before publishing
8. **Version your API** for backward compatibility
9. **Use structured logging** for debugging
10. **Follow semantic versioning** for releases