"""
Shared pytest fixtures for Projects module tests.

This file contains all common fixtures used across the split test files.
"""
import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'polarion_rest_api'))

from modules.projects import Projects
from modules.roles import Roles
from modules.work_items import WorkItems
from modules.document_attachments import DocumentAttachments
from modules.document_comments import DocumentComments
from modules.collections import Collections
from modules.documents import Documents
from modules.document_parts import DocumentParts
from modules.enumerations import Enumerations
from modules.externally_linked_work_items import ExternallyLinkedWorkItems
from modules.feature_selections import FeatureSelections
from modules.icons import Icons
from modules.jobs import Jobs
from modules.linked_oslc_resources import LinkedOslcResources
from modules.linked_work_items import LinkedWorkItems
from modules.page_attachments import PageAttachments
from modules.pages import Pages
from modules.plans import Plans
from modules.project_templates import ProjectTemplates
from modules.revisions import Revisions
from modules.test_record_attachments import TestRecordAttachments
from modules.test_records import TestRecords


# ============================================================================
# Mock API Instance Fixtures
# ============================================================================

def _create_mock_api(api_class):
    """
    Internal helper to create a mocked API instance.
    
    Args:
        api_class: The API class to instantiate (e.g., Projects, Roles)
        
    Returns:
        API instance with mocked session
    """
    api = api_class(
        base_url="https://test.polarion.com/polarion/rest/v1",
        token="test_token"
    )
    api._session = Mock()
    # Mock headers attribute to support header manipulation in _post and _patch
    api._session.headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer test_token'
    }
    return api


@pytest.fixture
def mock_projects_api():
    """Create Projects instance with mocked session for unit tests"""
    return _create_mock_api(Projects)


@pytest.fixture
def mock_roles_api():
    """Create Roles instance with mocked session for unit tests"""
    return _create_mock_api(Roles)


@pytest.fixture
def mock_work_items_api():
    """Create WorkItems instance with mocked session for unit tests"""
    return _create_mock_api(WorkItems)


@pytest.fixture
def mock_document_attachments_api():
    """Create DocumentAttachments instance with mocked session for unit tests"""
    return _create_mock_api(DocumentAttachments)


@pytest.fixture
def mock_document_comments_api():
    """Create DocumentComments instance with mocked session for unit tests"""
    return _create_mock_api(DocumentComments)


@pytest.fixture
def mock_collections_api():
    """Create Collections instance with mocked session for unit tests"""
    return _create_mock_api(Collections)


@pytest.fixture
def mock_documents_api():
    """Create Documents instance with mocked session for unit tests"""
    return _create_mock_api(Documents)


@pytest.fixture
def mock_document_parts_api():
    """Create DocumentParts instance with mocked session for unit tests"""
    return _create_mock_api(DocumentParts)


@pytest.fixture
def mock_enumerations_api():
    """Create Enumerations instance with mocked session for unit tests"""
    return _create_mock_api(Enumerations)


@pytest.fixture
def mock_externally_linked_work_items_api():
    """Create ExternallyLinkedWorkItems instance with mocked session for unit tests"""
    return _create_mock_api(ExternallyLinkedWorkItems)


@pytest.fixture
def mock_feature_selections_api():
    """Create FeatureSelections instance with mocked session for unit tests"""
    return _create_mock_api(FeatureSelections)


@pytest.fixture
def mock_icons_api():
    """Create Icons instance with mocked session for unit tests"""
    return _create_mock_api(Icons)


@pytest.fixture
def mock_jobs_api():
    """Create Jobs instance with mocked session for unit tests"""
    return _create_mock_api(Jobs)


@pytest.fixture
def mock_linked_oslc_resources_api():
    """Create LinkedOslcResources instance with mocked session for unit tests"""
    return _create_mock_api(LinkedOslcResources)


@pytest.fixture
def mock_linked_work_items_api():
    """Create LinkedWorkItems instance with mocked session for unit tests"""
    return _create_mock_api(LinkedWorkItems)


@pytest.fixture
def mock_page_attachments_api():
    """Create PageAttachments instance with mocked session for unit tests"""
    return _create_mock_api(PageAttachments)


@pytest.fixture
def mock_pages_api():
    """Create Pages instance with mocked session for unit tests"""
    return _create_mock_api(Pages)


@pytest.fixture
def mock_plans_api():
    """Create Plans instance with mocked session for unit tests"""
    return _create_mock_api(Plans)


@pytest.fixture
def mock_project_templates_api():
    """Create ProjectTemplates instance with mocked session for unit tests"""
    return _create_mock_api(ProjectTemplates)


@pytest.fixture
def mock_revisions_api():
    """Create Revisions instance with mocked session for unit tests"""
    return _create_mock_api(Revisions)


@pytest.fixture
def mock_test_record_attachments_api():
    """Create TestRecordAttachments instance with mocked session for unit tests"""
    return _create_mock_api(TestRecordAttachments)


@pytest.fixture
def mock_test_records_api():
    """Create TestRecords instance with mocked session for unit tests"""
    return _create_mock_api(TestRecords)


@pytest.fixture
def mock_response():
    """Create a mock response object for unit tests"""
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {}
    mock_resp.text = ""
    mock_resp.headers = {}
    return mock_resp


# ============================================================================
# Test Parameters Fixtures (for mocked tests)
# ============================================================================

@pytest.fixture
def test_params():
    """Test parameters for mocked tests (no real API required)"""
    return {
        'project_id': 'TEST_PROJECT',
        'test_param_id': 'test_param_001'
    }


@pytest.fixture
def mock_api_with_spy():
    """
    Create Projects API instance with spy capability to capture parameters.
    This fixture is used to test that default fields are properly applied.
    """
    class ProjectsWithSpy(Projects):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._captured_params = []
        
        def _get(self, endpoint, params=None):
            # Capture the params for testing
            if params:
                self._captured_params.append(params.copy())
            # Return a mock response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": {}}
            return mock_response
    
    api = ProjectsWithSpy(
        base_url="https://test.polarion.com/polarion/rest/v1",
        token="test_token"
    )
    return api


# ============================================================================
# Sample Response Fixtures
# ============================================================================

@pytest.fixture
def sample_project_response():
    """Sample API response for a single project"""
    return {
        "data": {
            "type": "projects",
            "id": "OT",
            "attributes": {
                "name": "OT Project",
                "description": {
                    "type": "text/plain",
                    "content": "Test project description"
                },
                "active": True,
                "finished": False
            }
        }
    }


@pytest.fixture
def sample_projects_list_response():
    """Sample API response for list of projects"""
    return {
        "data": [
            {
                "type": "projects",
                "id": "OT",
                "attributes": {
                    "name": "OT Project",
                    "active": True
                }
            },
            {
                "type": "projects",
                "id": "TEST",
                "attributes": {
                    "name": "Test Project",
                    "active": True
                }
            }
        ],
        "meta": {
            "totalCount": 2
        }
    }


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires real API)"
    )
    config.addinivalue_line(
        "markers", "delete: mark test as delete operation (uses mocks)"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )


# ============================================================================
# Helper Functions
# ============================================================================

def print_project_details(project_data):
    """Helper function to print project details"""
    attrs = project_data.get('attributes', {})
    print(f"\nProject Details:")
    print(f"  ID: {project_data.get('id')}")
    print(f"  Name: {attrs.get('name', 'N/A')}")
    print(f"  Active: {attrs.get('active', 'N/A')}")
    print(f"  Finished: {attrs.get('finished', 'N/A')}")
    
    if 'description' in attrs:
        desc = attrs['description']
        if isinstance(desc, dict):
            content = desc.get('content', '')
            print(f"  Description: {content[:100]}...")
        else:
            print(f"  Description: {str(desc)[:100]}...")
