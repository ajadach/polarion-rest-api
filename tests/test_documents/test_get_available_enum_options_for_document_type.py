"""
Tests for Documents.get_available_enum_options_for_document_type() method.
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
def sample_enum_options_for_type_response():
    """Sample API response for get_available_enum_options_for_document_type"""
    return {
        "meta": {
            "totalCount": 3
        },
        "data": [
            {
                "id": "open",
                "name": "Open",
                "color": "#F9FF4D",
                "description": "Open status for document type",
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
                "id": "in_review",
                "name": "In Review",
                "color": "#FFB84D",
                "description": "In review status",
                "hidden": False,
                "default": False,
                "parent": False,
                "oppositeName": "Approved",
                "columnWidth": "85%",
                "iconURL": "/polarion/icons/default/enums/status_review.gif",
                "createDefect": False,
                "templateWorkItem": "reviewTemplate",
                "minValue": 60,
                "requiresSignatureForTestCaseExecution": True,
                "terminal": False,
                "limited": False
            },
            {
                "id": "approved",
                "name": "Approved",
                "color": "#4DFF4D",
                "description": "Approved status",
                "hidden": False,
                "default": False,
                "parent": False,
                "oppositeName": "In Review",
                "columnWidth": "80%",
                "iconURL": "/polarion/icons/default/enums/status_approved.gif",
                "createDefect": False,
                "templateWorkItem": "approvedTemplate",
                "minValue": 100,
                "requiresSignatureForTestCaseExecution": False,
                "terminal": True,
                "limited": False
            }
        ],
        "links": {
            "first": "server-host-name/application-path/projects/MyProjectId/documents/fields/status/actions/getAvailableOptions?page%5Bnumber%5D=1&type=req_specification",
            "prev": "server-host-name/application-path/projects/MyProjectId/documents/fields/status/actions/getAvailableOptions?page%5Bnumber%5D=4&type=req_specification",
            "next": "server-host-name/application-path/projects/MyProjectId/documents/fields/status/actions/getAvailableOptions?page%5Bnumber%5D=6&type=req_specification",
            "last": "server-host-name/application-path/projects/MyProjectId/documents/fields/status/actions/getAvailableOptions?page%5Bnumber%5D=9&type=req_specification",
            "self": "server-host-name/application-path/projects/MyProjectId/documents/fields/status/actions/getAvailableOptions?page%5Bsize%5D=10&page%5Bnumber%5D=5&type=req_specification"
        }
    }


# ============================================================================
# Test: Basic GET request
# ============================================================================

def test_get_available_enum_options_for_document_type_basic(mock_documents_api, sample_enum_options_for_type_response):
    """Test basic get_available_enum_options_for_document_type request"""
    # Setup mock
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status'
    )
    
    # Verify
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
    assert 'meta' in data
    assert data['meta']['totalCount'] == 3
    assert len(data['data']) == 3
    
    # Verify correct endpoint was called
    mock_documents_api._session.get.assert_called_once()
    call_args = mock_documents_api._session.get.call_args
    assert 'projects/MyProjectId/documents/fields/status/actions/getAvailableOptions' in call_args[0][0]


# ============================================================================
# Test: With all parameters
# ============================================================================

def test_get_available_enum_options_for_document_type_with_all_parameters(mock_documents_api, sample_enum_options_for_type_response):
    """Test with page_size, page_number, and document_type parameters"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status',
        page_size=10,
        page_number=2,
        document_type='req_specification'
    )
    
    # Verify all parameters
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['page[size]'] == 10
    assert params['page[number]'] == 2
    assert params['type'] == 'req_specification'
    assert response.status_code == 200


# ============================================================================
# Test: With document_type only
# ============================================================================

def test_get_available_enum_options_for_document_type_with_type_only(mock_documents_api, sample_enum_options_for_type_response):
    """Test with only document_type parameter"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status',
        document_type='test_specification'
    )
    
    # Verify document_type parameter
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['type'] == 'test_specification'
    assert 'page[size]' not in params
    assert 'page[number]' not in params


# ============================================================================
# Test: With pagination only
# ============================================================================

def test_get_available_enum_options_for_document_type_with_pagination_only(mock_documents_api, sample_enum_options_for_type_response):
    """Test with only pagination parameters"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status',
        page_size=25,
        page_number=3
    )
    
    # Verify
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['page[size]'] == 25
    assert params['page[number]'] == 3
    assert 'type' not in params


# ============================================================================
# Test: Only page_size parameter
# ============================================================================

def test_get_available_enum_options_for_document_type_with_page_size_only(mock_documents_api, sample_enum_options_for_type_response):
    """Test with only page_size parameter"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status',
        page_size=50
    )
    
    # Verify
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['page[size]'] == 50
    assert 'page[number]' not in params
    assert 'type' not in params


# ============================================================================
# Test: Only page_number parameter
# ============================================================================

def test_get_available_enum_options_for_document_type_with_page_number_only(mock_documents_api, sample_enum_options_for_type_response):
    """Test with only page_number parameter"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status',
        page_number=5
    )
    
    # Verify
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['page[number]'] == 5
    assert 'page[size]' not in params
    assert 'type' not in params


# ============================================================================
# Test: Response structure validation
# ============================================================================

def test_get_available_enum_options_for_document_type_response_structure(mock_documents_api, sample_enum_options_for_type_response):
    """Test that response has correct structure"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status'
    )
    
    # Verify structure
    data = response.json()
    
    assert 'data' in data
    assert 'meta' in data
    assert 'links' in data
    
    # Verify meta
    assert 'totalCount' in data['meta']
    assert data['meta']['totalCount'] == 3
    
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

def test_get_available_enum_options_for_document_type_attributes(mock_documents_api, sample_enum_options_for_type_response):
    """Test that enum options have all expected attributes"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
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
# Test: Multiple enum options
# ============================================================================

def test_get_available_enum_options_for_document_type_multiple_options(mock_documents_api, sample_enum_options_for_type_response):
    """Test that multiple enum options are returned correctly"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status'
    )
    
    # Verify multiple options
    data = response.json()
    options = data['data']
    
    assert len(options) == 3
    assert options[0]['id'] == 'open'
    assert options[1]['id'] == 'in_review'
    assert options[2]['id'] == 'approved'
    
    # Verify different properties
    assert options[0]['terminal'] == False
    assert options[2]['terminal'] == True


# ============================================================================
# Test: Empty result
# ============================================================================

def test_get_available_enum_options_for_document_type_empty_result(mock_documents_api):
    """Test with empty enum options result"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "meta": {"totalCount": 0},
        "data": [],
        "links": {
            "self": "server-host-name/application-path/projects/MyProjectId/documents/fields/customField/actions/getAvailableOptions"
        }
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='customField'
    )
    
    # Verify
    assert response.status_code == 200
    data = response.json()
    assert data['meta']['totalCount'] == 0
    assert len(data['data']) == 0


# ============================================================================
# Test: Error responses
# ============================================================================

def test_get_available_enum_options_for_document_type_not_found(mock_documents_api):
    """Test with 404 Not Found"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {
        "errors": [{
            "status": "404",
            "title": "Not Found",
            "detail": "Project or field not found"
        }]
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='NonExistent',
        field_id='status'
    )
    
    # Verify
    assert response.status_code == 404
    assert 'errors' in response.json()


def test_get_available_enum_options_for_document_type_forbidden(mock_documents_api):
    """Test with 403 Forbidden"""
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.json.return_value = {
        "errors": [{
            "status": "403",
            "title": "Forbidden",
            "detail": "Access denied to project or field"
        }]
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status'
    )
    
    # Verify
    assert response.status_code == 403


def test_get_available_enum_options_for_document_type_unauthorized(mock_documents_api):
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
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status'
    )
    
    # Verify
    assert response.status_code == 401


def test_get_available_enum_options_for_document_type_bad_request(mock_documents_api):
    """Test with 400 Bad Request"""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "errors": [{
            "status": "400",
            "title": "Bad Request",
            "detail": "Invalid document_type parameter"
        }]
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status',
        document_type='invalid_type'
    )
    
    # Verify
    assert response.status_code == 400


def test_get_available_enum_options_for_document_type_server_error(mock_documents_api):
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
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status'
    )
    
    # Verify
    assert response.status_code == 500


# ============================================================================
# Test: Special characters in parameters
# ============================================================================

def test_get_available_enum_options_for_document_type_with_special_characters(mock_documents_api, sample_enum_options_for_type_response):
    """Test with special characters in parameters"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute with special characters
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='Project-123',
        field_id='custom_field_01'
    )
    
    # Verify endpoint contains special characters
    call_args = mock_documents_api._session.get.call_args
    assert 'projects/Project-123/documents/fields/custom_field_01/actions/getAvailableOptions' in call_args[0][0]
    assert response.status_code == 200


# ============================================================================
# Test: Different document types
# ============================================================================

def test_get_available_enum_options_for_different_document_types(mock_documents_api, sample_enum_options_for_type_response):
    """Test for different document types"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Test for different document types
    document_types = ['req_specification', 'test_specification', 'design_specification', 'project_plan']
    
    for doc_type in document_types:
        response = mock_documents_api.get_available_enum_options_for_document_type(
            project_id='MyProjectId',
            field_id='status',
            document_type=doc_type
        )
        
        assert response.status_code == 200
        call_args = mock_documents_api._session.get.call_args
        params = call_args[1]['params']
        assert params['type'] == doc_type


# ============================================================================
# Test: Different field types
# ============================================================================

def test_get_available_enum_options_for_different_fields(mock_documents_api, sample_enum_options_for_type_response):
    """Test for different field types (status, priority, category, etc.)"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Test for different field types
    field_ids = ['status', 'priority', 'category', 'severity', 'type']
    
    for field_id in field_ids:
        response = mock_documents_api.get_available_enum_options_for_document_type(
            project_id='MyProjectId',
            field_id=field_id
        )
        
        assert response.status_code == 200
        call_args = mock_documents_api._session.get.call_args
        assert f'fields/{field_id}/actions/getAvailableOptions' in call_args[0][0]


# ============================================================================
# Test: Large page size
# ============================================================================

def test_get_available_enum_options_for_document_type_with_large_page_size(mock_documents_api, sample_enum_options_for_type_response):
    """Test with large page_size value"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute with large page size
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
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

def test_get_available_enum_options_for_document_type_with_none_parameters(mock_documents_api, sample_enum_options_for_type_response):
    """Test with explicitly None optional parameters"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute with None values
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status',
        page_size=None,
        page_number=None,
        document_type=None
    )
    
    # Verify
    assert response.status_code == 200
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1].get('params')
    
    # Should not have optional params or should be None/empty
    if params:
        assert 'page[size]' not in params
        assert 'page[number]' not in params
        assert 'type' not in params


# ============================================================================
# Test: Verify enum option properties
# ============================================================================

def test_get_available_enum_options_for_document_type_verify_properties(mock_documents_api, sample_enum_options_for_type_response):
    """Test that all enum option properties are correctly returned"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status'
    )
    
    # Verify specific properties of each option
    data = response.json()
    
    # Check "open" option
    open_option = data['data'][0]
    assert open_option['default'] == True
    assert open_option['terminal'] == False
    assert open_option['limited'] == True
    assert open_option['color'] == '#F9FF4D'
    
    # Check "in_review" option
    review_option = data['data'][1]
    assert review_option['default'] == False
    assert review_option['limited'] == False
    assert review_option['minValue'] == 60
    
    # Check "approved" option
    approved_option = data['data'][2]
    assert approved_option['terminal'] == True
    assert approved_option['minValue'] == 100


# ============================================================================
# Test: Document type specific options
# ============================================================================

def test_get_available_enum_options_type_specific(mock_documents_api):
    """Test that options are specific to document type"""
    # Different options for different document types
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "meta": {"totalCount": 2},
        "data": [
            {"id": "draft", "name": "Draft", "color": "#CCCCCC"},
            {"id": "final", "name": "Final", "color": "#00FF00"}
        ],
        "links": {"self": "...type=req_specification"}
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute with specific document type
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status',
        document_type='req_specification'
    )
    
    # Verify
    data = response.json()
    assert len(data['data']) == 2
    assert data['data'][0]['id'] == 'draft'
    assert data['data'][1]['id'] == 'final'


# ============================================================================
# Test: Endpoint path validation
# ============================================================================

def test_get_available_enum_options_for_document_type_endpoint(mock_documents_api, sample_enum_options_for_type_response):
    """Test that correct endpoint is called (without space_id and document_name)"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_enum_options_for_type_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_available_enum_options_for_document_type(
        project_id='MyProjectId',
        field_id='status'
    )
    
    # Verify endpoint does NOT contain spaces/ or documents/{name}/
    call_args = mock_documents_api._session.get.call_args
    endpoint = call_args[0][0]
    
    assert 'projects/MyProjectId/documents/fields/status/actions/getAvailableOptions' in endpoint
    assert '/spaces/' not in endpoint
    assert '/documents/' in endpoint  # But only as part of the path, not with a specific document name
    assert response.status_code == 200
