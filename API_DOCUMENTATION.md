# Knowledge Graph MCP Server - API Documentation

## Overview

The Knowledge Graph MCP Server provides a RESTful API for storing, querying, and managing structured knowledge using Neo4j as the backend database. The server acts as a long-term memory system for Large Language Models (LLMs) and supports both read and write operations with proper authentication and validation.

## Authentication

All API endpoints require authentication using API keys. Include the API key in the Authorization header:

```
Authorization: Bearer <your_api_key>
```

API keys are configured in the `config.yaml` file and are securely hashed for storage.

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### Health Check Endpoints

#### GET /
Returns basic server status.

**Response:**
```json
{
  "message": "Knowledge Graph MCP Server is running"
}
```

#### GET /health
Returns detailed health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Knowledge Management

#### POST /api/v1/knowledge
Create a new Knowledge node with associated Source nodes.

**Headers:**
```
Authorization: Bearer <api_key>
Content-Type: application/json
```

**Request Body:**
```json
{
  "knowledge": {
    "type": "Algorithm",
    "title": "Binary Search",
    "content": "A search algorithm that finds the position of a target value within a sorted array.",
    "properties": {
      "complexity": "O(log n)",
      "space_complexity": "O(1)"
    }
  },
  "sources": [
    {
      "type": "Website",
      "url": "https://en.wikipedia.org/wiki/Binary_search_algorithm",
      "name": "Wikipedia - Binary Search",
      "trustworthiness": 8,
      "expertise": ["Computer Science", "Algorithms"]
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "knowledge_id": "k123456",
  "source_ids": ["s789012"]
}
```

**Knowledge Types:**
- `Algorithm`
- `Theorem`
- `Definition`
- `API`
- `Concept`
- `Fact`
- `Process`
- `Tool`
- `Other`

**Source Types:**
- `Website`
- `User`
- `Publication`
- `Book`
- `Journal`
- `Conference`
- `Other`

#### GET /api/v1/knowledge/{knowledge_id}
Retrieve a Knowledge node by ID with its associated Sources.

**Headers:**
```
Authorization: Bearer <api_key>
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "k": {
        "title": "Binary Search",
        "type": "Algorithm",
        "content": "A search algorithm...",
        "properties": {"complexity": "O(log n)"}
      },
      "sources": [
        {
          "name": "Wikipedia",
          "type": "Website",
          "trustworthiness": 8
        }
      ]
    }
  ],
  "metadata": {
    "knowledge_id": "k123456",
    "user": "test_user"
  }
}
```

#### GET /api/v1/knowledge/search/{search_term}
Search for Knowledge nodes by title or content.

**Headers:**
```
Authorization: Bearer <api_key>
```

**Query Parameters:**
- `knowledge_type` (optional): Filter by knowledge type

**Example:**
```
GET /api/v1/knowledge/search/algorithm?knowledge_type=Algorithm
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "k": {
        "title": "Binary Search Algorithm",
        "type": "Algorithm"
      },
      "sources": [...]
    }
  ],
  "metadata": {
    "search_term": "algorithm",
    "knowledge_type": "Algorithm",
    "result_count": 1,
    "user": "test_user"
  }
}
```

### Cypher Query Execution

#### POST /api/v1/query
Execute a read-only Cypher query against the knowledge graph.

**Headers:**
```
Authorization: Bearer <api_key>
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "MATCH (k:Knowledge)-[:DERIVED_FROM]->(s:Source) WHERE k.type = 'Algorithm' RETURN k.title, s.name LIMIT 10",
  "parameters": {}
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "k.title": "Binary Search",
      "s.name": "Wikipedia"
    }
  ],
  "metadata": {
    "query": "MATCH (k:Knowledge)...",
    "user": "test_user",
    "result_count": 1
  }
}
```

**Note:** Only read-only operations are allowed. Queries containing `CREATE`, `DELETE`, `SET`, `MERGE`, `REMOVE`, or `DROP` will be rejected.

## Data Models

### Knowledge Node
```json
{
  "type": "string",           // Required: Knowledge type
  "title": "string",          // Required: Knowledge title
  "content": "string",        // Required: Knowledge content
  "properties": {}            // Optional: Additional properties
}
```

### Source Node
```json
{
  "type": "string",           // Required: Source type
  "url": "string",            // Optional: Source URL (validated for existence)
  "name": "string",           // Required: Source name
  "trustworthiness": -10,     // Required: Integer between -10 and +10
  "expertise": ["string"]     // Required: Array of expertise domains
}
```

### Validation Rules

1. **Knowledge Validation:**
   - Title must be at least 3 characters
   - Content must be at least 10 characters
   - Type must be from predefined list

2. **Source Validation:**
   - URL must be accessible (if provided)
   - Trustworthiness must be between -10 and +10
   - Expertise domains must contain only alphanumeric characters, spaces, hyphens, and underscores
   - Type must be from predefined list

3. **Relationship Rules:**
   - Every Knowledge node must be linked to at least one Source node
   - Relationships are created as `DERIVED_FROM` edges

## Error Responses

### Authentication Error (401)
```json
{
  "detail": "Invalid API key"
}
```

### Validation Error (400)
```json
{
  "detail": {
    "message": "Validation failed",
    "errors": [
      "Source 1: URL does not exist or is not accessible"
    ]
  }
}
```

### Not Found Error (404)
```json
{
  "detail": "Knowledge node with ID k123456 not found"
}
```

### Server Error (500)
```json
{
  "success": false,
  "error": "Failed to create knowledge: Database connection error"
}
```

## Configuration

The server is configured via `config.yaml`:

```yaml
neo4j:
  read_only:
    host: "bolt://localhost:7687"
    username: "readonly_user"
    password: "readonly_password"
  write:
    host: "bolt://localhost:7687"
    username: "write_user"
    password: "write_password"

api_keys:
  - key: "your_api_key_here"
    user: "Username"
```

## Security Features

1. **API Key Authentication:** Secure hashing of API keys
2. **Database Access Control:** Separate read-only and write database users
3. **Query Validation:** Prevention of dangerous Cypher operations
4. **URL Validation:** Verification of source URL accessibility
5. **Input Sanitization:** Comprehensive validation of all input data

## Usage Examples

### Store Algorithm Knowledge
```bash
curl -X POST http://localhost:8000/api/v1/knowledge \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "knowledge": {
      "type": "Algorithm",
      "title": "Quick Sort",
      "content": "A divide-and-conquer sorting algorithm",
      "properties": {"complexity": "O(n log n)"}
    },
    "sources": [{
      "type": "Publication",
      "name": "Algorithms Textbook",
      "trustworthiness": 9,
      "expertise": ["Computer Science"]
    }]
  }'
```

### Query Knowledge
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "MATCH (k:Knowledge) WHERE k.type = '\''Algorithm'\'' RETURN k.title LIMIT 5"
  }'
```

### Search Knowledge
```bash
curl "http://localhost:8000/api/v1/knowledge/search/algorithm?knowledge_type=Algorithm" \
  -H "Authorization: Bearer your_api_key"
```