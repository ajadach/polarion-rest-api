# Polarion REST API Python Client

Python client library for Polarion REST API, providing easy access to all Polarion endpoints.

## Features

- Full coverage of Polarion REST API endpoints
- Type hints for better IDE support
- Comprehensive error handling
- Easy authentication management
- Well-documented API

## Installation

```bash
pip install polarion-rest-api
```

For development:
```bash
pip install polarion-rest-api[dev]
```

## Quick Start

```python
from polarion_rest_api import PolarionRestApi

# Initialize the API client
api = PolarionRestApi(
    base_url="https://your-polarion-instance.com/polarion/rest/v1",
    username="your_username",
    password="your_password"
)

# Get a project
response = api.projects.get_project(project_id="myproject")
print(response.json())

# Get test records
response = api.test_records.get_test_records(
    project_id="myproject",
    test_run_id="test-run-1"
)
print(response.json())
```

## Available Modules

The library provides access to the following Polarion API modules:

- **collections**: Collections operations
- **document_attachments**: Document Attachments operations
- **document_comments**: Document Comments operations
- **document_parts**: Document Parts operations
- **documents**: Documents operations
- **enumerations**: Enumerations operations
- **externally_linked_work_items**: Externally Linked Work Items operations
- **feature_selections**: Feature Selections operations
- **icons**: Icons operations
- **jobs**: Jobs operations
- **linked_oslc_resources**: Linked OSLC Resources operations
- **linked_work_items**: Linked Work Items operations
- **page_attachments**: Page Attachments operations
- **pages**: Pages operations
- **plans**: Plans operations
- **project_templates**: Project Templates operations
- **projects**: Projects operations
- **revisions**: Revisions operations
- **roles**: Roles operations
- **test_record_attachments**: Test Record Attachments operations
- **test_records**: Test Records operations
- **test_run_attachments**: Test Run Attachments operations
- **test_run_comments**: Test Run Comments operations
- **test_runs**: Test Runs operations
- **test_step_result_attachments**: Test Step Result Attachments operations
- **test_step_results**: Test Step Results operations
- **test_steps**: Test Steps operations
- **user_groups**: User Groups operations
- **users**: Users operations
- **work_item_approvals**: Work Item Approvals operations
- **work_item_attachments**: Work Item Attachments operations
- **work_item_comments**: Work Item Comments operations
- **work_item_work_records**: Work Item Work Records operations
- **work_items**: Work Items operations

## Requirements

- Python >= 3.7
- requests >= 2.25.0

## Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/polarion-rest-api.git
cd polarion-rest-api
pip install -e .[dev]
```

### Run Tests

```bash
pytest tests/
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please use the GitHub issue tracker.
