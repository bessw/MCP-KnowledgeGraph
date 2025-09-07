# Knowledge Graph MCP Server

## Project Goals

### 1. **General Description**
- The Knowledge Graph MCP Server serves as a local interface for storing, querying, and managing knowledge.
- Supports both **read** and **write** operations.
- Acts as a long-term memory for Large Language Models (LLMs), enabling them to store and retrieve structured knowledge efficiently.

### 2. **Data Model**
- **Node Type: `Knowledge`**
  - All data types (e.g., Algorithm, Theorem, Definition, API, etc.) are stored as nodes of type `Knowledge`.
  - The specific type is defined by the `type` attribute.
  - **Requirement:** Every `Knowledge` node must be linked to at least one `Source` node.
- **Node Type: `Source`**
  - Sources (e.g., Websites, Users, Publications) are stored as nodes of type `Source`.
  - Attributes of a `Source` node:
    - `type`: Type of the source (e.g., "Website", "User", "Publication").
    - `url`: URL of the source (if applicable).
    - `name`: Name of the source (e.g., user name or publication title).
    - `trustworthiness`: A metric indicating how trustworthy the source is, ranging from -10 (absolutely untrustworthy) to +10 (absolutely trustworthy), with 0 being neutral.
    - `expertise`: An array of domains or fields of expertise of the source (e.g., ["Mathematics", "Computer Science", "Physics"]).
- **Relationships between `Knowledge` and `Source`:**
  - Standardized relationship: `DERIVED_FROM`.
  - A `Knowledge` node must be linked to one or more `Source` nodes.

### 3. **API Design**
- **REST API**:
  - Endpoints for read and write operations.
  - Read operations accept Cypher queries and use a read-only user in the database.
  - Write operations use a write user in the database.
- **Validation:**
  - Only authorized users (defined in the configuration file) can use the API.

### 4. **Security Measures**
- **Authentication:**
  - Users are authenticated via API keys.
  - A list of valid API keys is defined in the configuration file.
  - API keys are stored as secure hashes to enhance security.
- **Access Control for the Database:**
  - A Read-Only user is used for read queries.
  - A Write user is used for write queries.
- **Cypher Queries:**
  - Read operations accept Cypher queries and use a read-only user in the database to minimize security risks.

### 5. **Configuration File**
- The configuration file includes:
  - A list of valid API keys (`api_keys`).
  - Credentials for the Neo4j database (Read-Only and Write users).
- Example: `config.example.yaml`.

### 6. **Validation Logic**
- URLs in `Source` nodes are validated synchronously to ensure they exist.
- Invalid URLs result in an error message, and the input is rejected.
- When creating a `Knowledge` node via the API, it is validated that the node is linked to at least one `Source` node. Nodes without a `Source` are not allowed and result in an error.
- The `trustworthiness` attribute is mandatory for `Source` nodes and must be within the range of -10 to +10.
- The `expertise` attribute of `Source` nodes must only contain alphanumeric values.

### 7. **Technology Stack**
- **Neo4j** as the database.
- **FastAPI** as the framework for the REST API.
- **Python** as the programming language.

### 8. **Extensibility**
- The structure of the Knowledge Graph is flexible and can be easily extended with new types and relationships.

### 9. **Test Cases**
- Test cases should be created to ensure the functionality of the Knowledge Graph MCP Server.
- GitHub Copilot should regularly generate realistic test scenarios for software projects. These scenarios should include both software-related and non-software-related tasks.
- In these test scenarios, the Knowledge Graph MCP Server should be used to solve problems by either retrieving information from it or simulating online research and user input. The obtained information should be inserted into the graph for later retrieval.
- If internet access is available, GitHub Copilot should actually perform online research for these tests.

## TODOs

For detailed tracking of tasks and progress, refer to the `TODO.md` file.
