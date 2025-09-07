# GitHub Copilot Instructions

## Please Read the `README.md` First
Before using GitHub Copilot to generate or modify code in this project, ensure you have read and understood the `README.md` file. It contains the detailed project goals, architecture, and guidelines.

## Key Points for GitHub Copilot Usage
1. **Adhere to the Project Goals:**
   - Ensure all code suggestions align with the defined project goals.
   - Do not deviate from the structure and logic outlined in the `README.md`.

2. **Language Requirement:**
   - All code and documentation must be written in **English**.

3. **Task Tracking:**
   - Refer to the `TODO.md` file for the next steps and tasks.
   - Ensure that any new tasks or progress updates are reflected in the `TODO.md` file.

4. **Configuration Management:**
   - Do not generate or commit sensitive information (e.g., passwords, secrets) to the repository.
   - You are not allowed to read `config.yaml`, please consult the `config.example.yaml` instead.

5. **API Design:**
   - Ensure all endpoints are properly documented and tested.

6. **Security:**
   - Validate all user inputs, especially Cypher queries, to prevent injection attacks.
   - Ensure only authorized users (defined in the configuration) can access the API.

7. **Testing:**
   - Test all endpoints thoroughly.
   - Verify that the Read-Only-User and Write-User have the correct permissions in the Neo4j database.
   - Always create test cases for your code.

8. **Code Quality:**
   - Follow Python best practices and maintain clean, readable code.
   - Document all functions and classes clearly.

## Additional Notes
- If GitHub Copilot generates code that deviates from the project goals, modify the suggestions to align with the `README.md`.
- Any significant changes to the project goals or architecture must be discussed and approved before implementation.
