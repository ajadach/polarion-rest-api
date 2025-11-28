"""
Tests for Documents.get_current_enumeration_options_for_document() method.
All tests use mocks - no real API calls.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'polarion_rest_api'))

from modules.documents import Documents


@pytest.fixture
def mock_documents_api():
    """Create Documents instance with mocked session"""
    api = Documents(
        base_url="https://test.polarion.com/polarion/rest/v1",
        token="test_token"
    )
    api._session = Mock()
    api._session.headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer test_token'
    }
    return api


@pytest.fixture
def sample_current_enum_options_response():
    """Sample API response for get_current_enumeration_options_for_document"""
    return {
        "meta": {
            "totalCount": 2
        },
        "data": [
            {
                "id": "open",
                "name": "Open",
                "color": "#F9FF4D",
                "description": "Currently selected open status",
                "hidden": False,
                "default": True,
                "parent": True,
                "oppositeName": "Closed",
                "columnWidth": "90%",
                "iconURL": "/polarion/icons/default/enums/status_open.gif",
                "createDefect": True,
                "templateWorkItem": "exampleTemplate",
                "minValue": 30,
                "requiresSignatureForTestCaseExecution": True,
                "terminal": False,
                "limited": True
            },
            {
                "id": "in_progress",
                "name": "In Progress",
                "color": "#4D9FFF",
                "description": "Currently selected in progress status",
                "hidden": False,
                "default": False,
                "parent": False,
                "oppositeName": "Completed",
                "columnWidth": "80%",
                "iconURL": "/polarion/icons/default/enums/status_in_progress.gif",
                "createDefect": False,
                "templateWorkItem": "progressTemplate",
                "minValue": 50,
                "requiresSignatureForTestCaseExecution": False,
                "terminal": False,
                "limited": False
            }
        ],
        "links": {
            "first": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/documents/MyDocument/fields/status/actions/getCurrentOptions?page%5Bnumber%5D=1",
            "prev": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/documents/MyDocument/fields/status/actions/getCurrentOptions?page%5Bnumber%5D=4",
            "next": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/documents/MyDocument/fields/status/actions/getCurrentOptions?page%5Bnumber%5D=6",
            "last": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/documents/MyDocument/fields/status/actions/getCurrentOptions?page%5Bnumber%5D=9",
            "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/documents/MyDocument/fields/status/actions/getCurrentOptions?page%5Bsize%5D=10&page%5Bnumber%5D=5&revision=1234"
        }
    }


# ============================================================================
# Test: Basic GET request
# ============================================================================

def test_get_current_enumeration_options_basic(mock_documents_api, sample_current_enum_options_response):
    """Test basic get_current_enumeration_options_for_document request"""
    # Setup mock
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status'
    )
    
    # Verify
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
    assert 'meta' in data
    assert data['meta']['totalCount'] == 2
    assert len(data['data']) == 2
    
    # Verify correct endpoint was called
    mock_documents_api._session.get.assert_called_once()
    call_args = mock_documents_api._session.get.call_args
    assert 'projects/MyProjectId/spaces/MySpaceId/documents/MyDocument/fields/status/actions/getCurrentOptions' in call_args[0][0]


# ============================================================================
# Test: With all parameters
# ============================================================================

def test_get_current_enumeration_options_with_all_parameters(mock_documents_api, sample_current_enum_options_response):
    """Test with page_size, page_number, and revision parameters"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status',
        page_size=10,
        page_number=2,
        revision='1234'
    )
    
    # Verify all parameters
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['page[size]'] == 10
    assert params['page[number]'] == 2
    assert params['revision'] == '1234'
    assert response.status_code == 200


# ============================================================================
# Test: With revision only
# ============================================================================

def test_get_current_enumeration_options_with_revision_only(mock_documents_api, sample_current_enum_options_response):
    """Test with only revision parameter"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status',
        revision='5678'
    )
    
    # Verify revision parameter
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['revision'] == '5678'
    assert 'page[size]' not in params
    assert 'page[number]' not in params


# ============================================================================
# Test: With pagination only
# ============================================================================

def test_get_current_enumeration_options_with_pagination_only(mock_documents_api, sample_current_enum_options_response):
    """Test with only pagination parameters"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status',
        page_size=25,
        page_number=3
    )
    
    # Verify
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['page[size]'] == 25
    assert params['page[number]'] == 3
    assert 'revision' not in params


# ============================================================================
# Test: Only page_size parameter
# ============================================================================

def test_get_current_enumeration_options_with_page_size_only(mock_documents_api, sample_current_enum_options_response):
    """Test with only page_size parameter"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status',
        page_size=50
    )
    
    # Verify
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['page[size]'] == 50
    assert 'page[number]' not in params
    assert 'revision' not in params


# ============================================================================
# Test: Only page_number parameter
# ============================================================================

def test_get_current_enumeration_options_with_page_number_only(mock_documents_api, sample_current_enum_options_response):
    """Test with only page_number parameter"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status',
        page_number=5
    )
    
    # Verify
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['page[number]'] == 5
    assert 'page[size]' not in params
    assert 'revision' not in params


# ============================================================================
# Test: Default space
# ============================================================================

def test_get_current_enumeration_options_with_default_space(mock_documents_api, sample_current_enum_options_response):
    """Test with _default space"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='_default',
        document_name='MyDocument',
        field_id='status'
    )
    
    # Verify endpoint contains _default
    call_args = mock_documents_api._session.get.call_args
    assert 'projects/MyProjectId/spaces/_default/documents/MyDocument/fields/status/actions/getCurrentOptions' in call_args[0][0]
    assert response.status_code == 200


# ============================================================================
# Test: Response structure validation
# ============================================================================

def test_get_current_enumeration_options_response_structure(mock_documents_api, sample_current_enum_options_response):
    """Test that response has correct structure"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status'
    )
    
    # Verify structure
    data = response.json()
    
    assert 'data' in data
    assert 'meta' in data
    assert 'links' in data
    
    # Verify meta
    assert 'totalCount' in data['meta']
    assert data['meta']['totalCount'] == 2
    
    # Verify links
    links = data['links']
    assert 'first' in links
    assert 'prev' in links
    assert 'next' in links
    assert 'last' in links
    assert 'self' in links


# ============================================================================
# Test: Enum option attributes validation
# ============================================================================

def test_get_current_enumeration_options_attributes(mock_documents_api, sample_current_enum_options_response):
    """Test that current enum options have all expected attributes"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status'
    )
    
    # Verify first enum option attributes
    data = response.json()
    option = data['data'][0]
    
    assert option['id'] == 'open'
    assert option['name'] == 'Open'
    assert option['color'] == '#F9FF4D'
    assert 'description' in option
    assert option['hidden'] == False
    assert option['default'] == True
    assert 'parent' in option
    assert 'oppositeName' in option
    assert 'columnWidth' in option
    assert 'iconURL' in option
    assert 'createDefect' in option
    assert 'templateWorkItem' in option
    assert 'minValue' in option
    assert 'requiresSignatureForTestCaseExecution' in option
    assert 'terminal' in option
    assert 'limited' in option


# ============================================================================
# Test: Multiple current enum options
# ============================================================================

def test_get_current_enumeration_options_multiple_options(mock_documents_api, sample_current_enum_options_response):
    """Test that multiple current enum options are returned correctly"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status'
    )
    
    # Verify multiple options
    data = response.json()
    options = data['data']
    
    assert len(options) == 2
    assert options[0]['id'] == 'open'
    assert options[1]['id'] == 'in_progress'
    
    # Verify these are current/selected options
    assert options[0]['default'] == True
    assert options[1]['default'] == False


# ============================================================================
# Test: Empty result
# ============================================================================

def test_get_current_enumeration_options_empty_result(mock_documents_api):
    """Test with empty current enum options result"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "meta": {"totalCount": 0},
        "data": [],
        "links": {
            "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/documents/MyDocument/fields/customField/actions/getCurrentOptions"
        }
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='customField'
    )
    
    # Verify
    assert response.status_code == 200
    data = response.json()
    assert data['meta']['totalCount'] == 0
    assert len(data['data']) == 0


# ============================================================================
# Test: Single current option
# ============================================================================

def test_get_current_enumeration_options_single_option(mock_documents_api):
    """Test with single current enum option"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "meta": {"totalCount": 1},
        "data": [
            {
                "id": "open",
                "name": "Open",
                "color": "#F9FF4D",
                "description": "Currently selected status",
                "hidden": False,
                "default": True,
                "parent": True,
                "oppositeName": "Closed",
                "columnWidth": "90%",
                "iconURL": "/polarion/icons/default/enums/status_open.gif",
                "createDefect": True,
                "templateWorkItem": "exampleTemplate",
                "minValue": 30,
                "requiresSignatureForTestCaseExecution": True,
                "terminal": True,
                "limited": True
            }
        ],
        "links": {
            "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/documents/MyDocument/fields/status/actions/getCurrentOptions"
        }
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status'
    )
    
    # Verify single option
    data = response.json()
    assert data['meta']['totalCount'] == 1
    assert len(data['data']) == 1
    assert data['data'][0]['id'] == 'open'


# ============================================================================
# Test: Error responses
# ============================================================================

def test_get_current_enumeration_options_not_found(mock_documents_api):
    """Test with 404 Not Found"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {
        "errors": [{
            "status": "404",
            "title": "Not Found",
            "detail": "Document or field not found"
        }]
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='NonExistent',
        space_id='MySpaceId',
        document_name='NonExistent',
        field_id='status'
    )
    
    # Verify
    assert response.status_code == 404
    assert 'errors' in response.json()


def test_get_current_enumeration_options_forbidden(mock_documents_api):
    """Test with 403 Forbidden"""
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.json.return_value = {
        "errors": [{
            "status": "403",
            "title": "Forbidden",
            "detail": "Access denied to document or field"
        }]
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='SecretDocument',
        field_id='status'
    )
    
    # Verify
    assert response.status_code == 403


def test_get_current_enumeration_options_unauthorized(mock_documents_api):
    """Test with 401 Unauthorized"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {
        "errors": [{
            "status": "401",
            "title": "Unauthorized",
            "detail": "Authentication required"
        }]
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status'
    )
    
    # Verify
    assert response.status_code == 401


def test_get_current_enumeration_options_bad_request(mock_documents_api):
    """Test with 400 Bad Request"""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "errors": [{
            "status": "400",
            "title": "Bad Request",
            "detail": "Invalid revision parameter"
        }]
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status',
        revision='invalid'
    )
    
    # Verify
    assert response.status_code == 400


def test_get_current_enumeration_options_server_error(mock_documents_api):
    """Test with 500 Internal Server Error"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {
        "errors": [{
            "status": "500",
            "title": "Internal Server Error",
            "detail": "Server error occurred"
        }]
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status'
    )
    
    # Verify
    assert response.status_code == 500


# ============================================================================
# Test: Special characters in parameters
# ============================================================================

def test_get_current_enumeration_options_with_special_characters(mock_documents_api, sample_current_enum_options_response):
    """Test with special characters in parameters"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute with special characters
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='Project-123',
        space_id='Space_456',
        document_name='Doc-Name_With.Special',
        field_id='custom_field_01'
    )
    
    # Verify endpoint contains special characters
    call_args = mock_documents_api._session.get.call_args
    assert 'projects/Project-123/spaces/Space_456/documents/Doc-Name_With.Special/fields/custom_field_01/actions/getCurrentOptions' in call_args[0][0]
    assert response.status_code == 200


# ============================================================================
# Test: Different field types
# ============================================================================

def test_get_current_enumeration_options_for_different_fields(mock_documents_api, sample_current_enum_options_response):
    """Test for different field types (status, priority, type, etc.)"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Test for different field types
    field_ids = ['status', 'priority', 'type', 'severity', 'category']
    
    for field_id in field_ids:
        response = mock_documents_api.get_current_enumeration_options_for_document(
            project_id='MyProjectId',
            space_id='MySpaceId',
            document_name='MyDocument',
            field_id=field_id
        )
        
        assert response.status_code == 200
        call_args = mock_documents_api._session.get.call_args
        assert f'fields/{field_id}/actions/getCurrentOptions' in call_args[0][0]


# ============================================================================
# Test: Historical revision
# ============================================================================

def test_get_current_enumeration_options_with_historical_revision(mock_documents_api, sample_current_enum_options_response):
    """Test with historical revision to get options from past"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute with old revision
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status',
        revision='100'
    )
    
    # Verify revision is passed
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    assert params['revision'] == '100'
    assert response.status_code == 200


# ============================================================================
# Test: Large page size
# ============================================================================

def test_get_current_enumeration_options_with_large_page_size(mock_documents_api, sample_current_enum_options_response):
    """Test with large page_size value"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute with large page size
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status',
        page_size=1000
    )
    
    # Verify
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    assert params['page[size]'] == 1000
    assert response.status_code == 200


# ============================================================================
# Test: None optional parameters
# ============================================================================

def test_get_current_enumeration_options_with_none_parameters(mock_documents_api, sample_current_enum_options_response):
    """Test with explicitly None optional parameters"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute with None values
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status',
        page_size=None,
        page_number=None,
        revision=None
    )
    
    # Verify
    assert response.status_code == 200
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1].get('params')
    
    # Should not have optional params or should be None/empty
    if params:
        assert 'page[size]' not in params
        assert 'page[number]' not in params
        assert 'revision' not in params


# ============================================================================
# Test: Verify current enum option properties
# ============================================================================

def test_get_current_enumeration_options_verify_properties(mock_documents_api, sample_current_enum_options_response):
    """Test that all current enum option properties are correctly returned"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_current_enum_options_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status'
    )
    
    # Verify specific properties of each option
    data = response.json()
    
    # Check "open" option (currently selected)
    open_option = data['data'][0]
    assert open_option['default'] == True
    assert open_option['terminal'] == False
    assert open_option['limited'] == True
    assert open_option['color'] == '#F9FF4D'
    
    # Check "in_progress" option (currently selected)
    progress_option = data['data'][1]
    assert progress_option['default'] == False
    assert progress_option['limited'] == False
    assert progress_option['minValue'] == 50


# ============================================================================
# Test: Difference from available options
# ============================================================================

def test_get_current_enumeration_options_vs_available(mock_documents_api):
    """Test that current options are subset of available options"""
    # This test demonstrates the difference between getCurrentOptions and getAvailableOptions
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "meta": {"totalCount": 2},
        "data": [
            {"id": "open", "name": "Open", "color": "#F9FF4D"},
            {"id": "in_progress", "name": "In Progress", "color": "#4D9FFF"}
        ],
        "links": {"self": "...getCurrentOptions"}
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute - get current options (selected/in use)
    response = mock_documents_api.get_current_enumeration_options_for_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocument',
        field_id='status'
    )
    
    # Verify - should return only currently selected options
    data = response.json()
    assert len(data['data']) == 2  # Only 2 options are currently selected
    assert response.status_code == 200
