# Prompt Template for Generating Polarion API Module Classes

## How to use this template:
Replace `[MODULE_NAME]` with the desired module name (e.g., "Projects", "Test Runs", "Documents", etc.)

---

## PROMPT:

```
I need to create a Python class for the **[MODULE_NAME]** module in Polarion REST API, following the same structure and pattern that was used for the "Work Items" module.

### Context:
- I have an openapi.json file located at: `${PATH_TO_REPO}/polarion-rest-api /polarion-rest-api/data/openapi.json`
- There is a base class PolarionBase at: `${PATH_TO_REPO}/polarion-rest-api /polarion-rest-api/modules/base.py`
- Main class PolarionRestApi at: `${PATH_TO_REPO}/polarion-rest-api /polarion-rest-api/polarion_api.py`
- Reference class WorkItems at: `${PATH_TO_REPO}/polarion-rest-api /polarion-rest-api/modules/work_items.py`

### Tasks to complete:

1. **Analyze openapi.json**:
   - Find all endpoints related to the **[MODULE_NAME]** category in the openapi.json file
   - Identify their tagging ("tags" field in each endpoint)
   - Count the number of endpoints for this category (broken down by DELETE, GET, PATCH, POST)

2. **Create new class**:
   - Create a new file: `${PATH_TO_REPO}/polarion-rest-api /polarion-rest-api/modules/[module_name_snake_case].py`
   - Class name: `[ModuleNamePascalCase]`
   - Class must inherit from `PolarionBase`

3. **Class structure**:
   - Add docstring describing the module and its functionality
   - Organize methods by HTTP type in order: DELETE, GET, PATCH, POST (according to Swagger)
   - Each section should be separated by a comment: `# ========== [METHOD] methods ==========`

4. **Method requirements**:
   - Each method must correspond to a specific endpoint from openapi.json
   - Method name should be in snake_case format and describe the operation (e.g., `get_project`, `create_project`, `delete_project`)
   - Method parameters must match parameters from openapi.json (path parameters, query parameters, request body)
   - All optional parameters should have `Optional[]` type hint and default value `None`
   - Request body should be of type `Dict[str, Any]`
   - Each method should return `requests.Response`
   - Add docstring with description, arguments (Args:) and return value (Returns:)

5. **Method implementation**:
   - Use methods from the base class: `self._get()`, `self._post()`, `self._patch()`, `self._delete()`
   - For DELETE with body use helper `self._delete_with_body()` (or create it if it doesn't exist)
   - Pass query parameters as dict in `params=`
   - Pass request body as dict in `json=`
   - Build correct endpoint path using f-strings for path parameters

6. **Verification**:
   - Check if the number of methods in the class matches the number of endpoints in openapi.json for this category
   - Check if the method order matches the order in Swagger documentation
   - Ensure all parameters from openapi.json are included

7. **Integration with PolarionRestApi**:
   - Ensure the new class will be automatically loaded by `PolarionRestApi.load_modules()`
   - No need to modify polarion_api.py - it should work automatically

### Response format:
1. First analyze openapi.json and list found endpoints for **[MODULE_NAME]**
2. Show summary: how many endpoints of each type (DELETE, GET, PATCH, POST)
3. Create the class file
4. Verify correctness (number of methods vs number of endpoints)

### Important rules:
- All endpoint paths from openapi.json are relative to base_url (remove leading `/api` if present)
- Maintain naming consistency with other modules
- Code must be readable, with appropriate type hints and docstrings
- Methods should be in exactly the same order as in Swagger documentation
```

---

## Example usage:

### For "Projects" module:
Replace `[MODULE_NAME]` with **"Projects"**

### For "Test Runs" module:
Replace `[MODULE_NAME]` with **"Test Runs"**

### For "Documents" module:
Replace `[MODULE_NAME]` with **"Documents"**

---

## Quick Reference - Available Modules in openapi.json:
To check available modules/categories, look for unique values in the "tags" field across all endpoints in openapi.json.

Common categories might include:
- Projects
- Test Runs
- Documents
- Plans
- Users
- Baselines
- Revisions
- etc.

Use semantic search or grep to find: `"tags"` in openapi.json to see all available categories.
