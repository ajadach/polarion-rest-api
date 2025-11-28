# Installation and Usage Guide

## Installation Options

### 1. Install from PyPI (when published)
```bash
pip install polarion-rest-api
```

### 2. Install from local directory
```bash
# Navigate to the project root directory
cd /path/to/polarion-rest-api

# Install in development mode (recommended for development)
pip install -e .

# Or install normally
pip install .
```

### 3. Install with development dependencies
```bash
pip install -e .[dev]
```

### 4. Build and install from wheel
```bash
# Build the package
python -m pip install --upgrade build
python -m build

# This creates dist/ directory with .whl and .tar.gz files
# Install from wheel
pip install dist/polarion_rest_api-0.1.0-py3-none-any.whl
```

## Usage Examples

### Basic Usage

```python
from polarion_rest_api import PolarionRestApi

# Initialize API client
api = PolarionRestApi(
    base_url="https://your-polarion-instance.com/polarion/rest/v1",
    token="your_bearer_token"
)

# Or set token later
api = PolarionRestApi(base_url="https://your-polarion-instance.com/polarion/rest/v1")
api.set_token("your_bearer_token")
```

### Working with Projects

```python
# Get a project
response = api.projects.get_project(project_id="myproject")
project_data = response.json()
print(project_data)

# Get all projects
response = api.projects.get_projects()
projects = response.json()
```

### Working with Test Records

```python
# Get test records
response = api.test_records.get_test_records(
    project_id="myproject",
    test_run_id="test-run-1"
)
test_records = response.json()

# Create test records
test_records_data = {
    "data": [
        {
            "type": "testrecords",
            "attributes": {
                "result": "passed",
                "duration": 120
            },
            "relationships": {
                "testCase": {
                    "data": {
                        "type": "workitems",
                        "id": "myproject/TC-001"
                    }
                }
            }
        }
    ]
}

response = api.test_records.post_test_records(
    project_id="myproject",
    test_run_id="test-run-1",
    test_records_data=test_records_data
)
```

### Working with Test Parameters

```python
# Get test parameters for a test record
response = api.test_records.get_test_record_test_parameters(
    project_id="myproject",
    test_run_id="run-1",
    test_case_project_id="myproject",
    test_case_id="TC-001",
    iteration="0"
)

# Create test parameters
test_params_data = {
    "data": [
        {
            "type": "testparameters",
            "attributes": {
                "name": "browser",
                "value": "Chrome"
            }
        },
        {
            "type": "testparameters",
            "attributes": {
                "name": "os",
                "value": "Windows 10"
            }
        }
    ]
}

response = api.test_records.post_test_record_test_parameters(
    project_id="myproject",
    test_run_id="run-1",
    test_case_project_id="myproject",
    test_case_id="TC-001",
    iteration="0",
    test_parameters_data=test_params_data
)
```

### Working with Work Items

```python
# Get work items
response = api.work_items.get_work_items(project_id="myproject")
work_items = response.json()

# Get specific work item
response = api.work_items.get_work_item(
    project_id="myproject",
    work_item_id="WI-123"
)
work_item = response.json()
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=polarion_rest_api --cov-report=html

# Run specific test file
pytest tests/test_test_records/test_post_test_records.py -v

# Run specific test
pytest tests/test_test_records/test_post_test_records.py::TestPostTestRecords::test_post_test_records_success -v
```

### Verifying Installation

```bash
# After installation, verify it works
python -c "from polarion_rest_api import PolarionRestApi; print('Installation successful!')"
```

## Uninstallation

```bash
pip uninstall polarion-rest-api
```

## Troubleshooting

### Import Error
If you get import errors, make sure you're importing from the correct package name:
```python
# Correct
from polarion_rest_api import PolarionRestApi

# Incorrect
from polarion-rest-api import PolarionRestApi  # Python doesn't allow hyphens in imports
```

### Module Not Found
If you get "Module not found" errors:
1. Check that the package is installed: `pip list | grep polarion`
2. Reinstall in development mode: `pip install -e .`
3. Check your Python path: `python -c "import sys; print(sys.path)"`

## Requirements

- Python >= 3.7
- requests >= 2.25.0

## Additional Resources

- [Polarion REST API Documentation](https://docs.sw.siemens.com/en-US/product/820367186/doc/PL20231214133625842.polarion_help_sc.polarion_sdk/xid1806046?uistate=wsm___doc-PL20231214133625842_polarion_help_sc_polarion_sdk__polarion_sdk)
- [GitHub Repository](https://github.com/yourusername/polarion-rest-api)
