"""
Tests for Documents.get_document() method.
All tests use mocks - no real API calls.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

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
def sample_document_response():
    """Sample API response for get_document"""
    return {
        "data": {
            "type": "documents",
            "id": "MyProjectId/MySpaceId/MyDocumentId",
            "revision": "1234",
            "attributes": {
                "autoSuspect": True,
                "branchedWithInitializedFields": ["fieldId"],
                "branchedWithQuery": "Branched with Query",
                "created": "1970-01-01T00:00:00Z",
                "derivedFields": ["fieldId"],
                "derivedFromLinkRole": "relates_to",
                "homePageContent": {
                    "type": "text/html",
                    "value": "My text value"
                },
                "moduleFolder": "MySpaceId",
                "moduleName": "MyDocumentId",
                "outlineNumbering": {
                    "prefix": "ABC"
                },
                "renderingLayouts": [
                    {
                        "type": "task",
                        "label": "My label",
                        "layouter": "paragraph",
                        "properties": [
                            {
                                "key": "fieldsAtStart",
                                "value": "id"
                            }
                        ]
                    }
                ],
                "status": "draft",
                "structureLinkRole": "relates_to",
                "title": "Title",
                "type": "req_specification",
                "updated": "1970-01-01T00:00:00Z",
                "usesOutlineNumbering": True
            },
            "relationships": {
                "attachments": {
                    "data": [
                        {
                            "type": "document_attachments",
                            "id": "MyProjectId/MySpaceId/MyDocumentId/MyAttachmentId",
                            "revision": "1234"
                        }
                    ],
                    "meta": {"totalCount": 1},
                    "links": {
                        "related": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/documents/MyDocumentId/attachments?revision=1234"
                    }
                },
                "author": {
                    "data": {
                        "type": "users",
                        "id": "MyUserId",
                        "revision": "1234"
                    }
                },
                "branchedFrom": {
                    "data": {
                        "type": "documents",
                        "id": "MyProjectId/MySpaceId/MyDocumentId",
                        "revision": "1234"
                    }
                },
                "comments": {
                    "data": [
                        {
                            "type": "document_comments",
                            "id": "MyProjectId/MySpaceId/MyDocumentId/MyCommentId",
                            "revision": "1234"
                        }
                    ],
                    "meta": {"totalCount": 1},
                    "links": {
                        "related": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/documents/MyDocumentId/comments?revision=1234"
                    }
                },
                "derivedFrom": {
                    "data": {
                        "type": "documents",
                        "id": "MyProjectId/MySpaceId/MyDocumentId",
                        "revision": "1234"
                    }
                },
                "project": {
                    "data": {
                        "type": "projects",
                        "id": "MyProjectId",
                        "revision": "1234"
                    }
                },
                "updatedBy": {
                    "data": {
                        "type": "users",
                        "id": "MyUserId",
                        "revision": "1234"
                    }
                },
                "variant": {
                    "data": {
                        "type": "workitems",
                        "id": "MyProjectId/MyWorkItemId",
                        "revision": "1234"
                    }
                }
            },
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/documents/MyDocumentId?revision=1234"
            }
        },
        "included": [{}],
        "links": {
            "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/documents/MyDocumentId?revision=1234"
        }
    }


# ============================================================================
# Test: Basic GET request
# ============================================================================

def test_get_document_basic(mock_documents_api, sample_document_response):
    """Test basic get_document request with default parameters"""
    # Setup mock
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId'
    )
    
    # Verify
    assert response.status_code == 200
    data = response.json()
    assert data['data']['type'] == 'documents'
    assert data['data']['id'] == 'MyProjectId/MySpaceId/MyDocumentId'
    assert data['data']['attributes']['title'] == 'Title'
    
    # Verify correct endpoint was called
    mock_documents_api._session.get.assert_called_once()
    call_args = mock_documents_api._session.get.call_args
    assert 'projects/MyProjectId/spaces/MySpaceId/documents/MyDocumentId' in call_args[0][0]


# ============================================================================
# Test: Default fields application
# ============================================================================

def test_get_document_applies_default_fields(mock_documents_api, sample_document_response):
    """Test that default fields are automatically applied"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId'
    )
    
    # Verify that params were passed (default fields should be applied)
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    # Check that default fields are present
    assert 'fields[documents]' in params
    assert params['fields[documents]'] == '@all'
    assert 'fields[document_attachments]' in params
    assert params['fields[document_attachments]'] == '@all'
    assert 'fields[document_comments]' in params
    assert params['fields[document_comments]'] == '@all'


# ============================================================================
# Test: Custom fields override
# ============================================================================

def test_get_document_with_custom_fields(mock_documents_api, sample_document_response):
    """Test get_document with custom fields parameter"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    custom_fields = {
        'documents': 'title,status,type',
        'document_parts': 'id,title'
    }
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId',
        fields=custom_fields
    )
    
    # Verify custom fields override defaults
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['fields[documents]'] == 'title,status,type'
    assert params['fields[document_parts]'] == 'id,title'
    # Other fields should still have default @all
    assert params['fields[projects]'] == '@all'


# ============================================================================
# Test: Include parameter
# ============================================================================

def test_get_document_with_include(mock_documents_api, sample_document_response):
    """Test get_document with include parameter"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId',
        include='author,project,attachments'
    )
    
    # Verify include parameter
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    assert params['include'] == 'author,project,attachments'


# ============================================================================
# Test: Revision parameter
# ============================================================================

def test_get_document_with_revision(mock_documents_api, sample_document_response):
    """Test get_document with revision parameter"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId',
        revision='1234'
    )
    
    # Verify revision parameter
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    assert params['revision'] == '1234'


# ============================================================================
# Test: All parameters combined
# ============================================================================

def test_get_document_with_all_parameters(mock_documents_api, sample_document_response):
    """Test get_document with all optional parameters"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    custom_fields = {'documents': 'title,status'}
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId',
        fields=custom_fields,
        include='author,project',
        revision='5678'
    )
    
    # Verify all parameters
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    assert params['fields[documents]'] == 'title,status'
    assert params['include'] == 'author,project'
    assert params['revision'] == '5678'
    assert response.status_code == 200


# ============================================================================
# Test: Default space
# ============================================================================

def test_get_document_with_default_space(mock_documents_api, sample_document_response):
    """Test get_document with _default space"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='_default',
        document_name='MyDocumentId'
    )
    
    # Verify endpoint contains _default
    call_args = mock_documents_api._session.get.call_args
    assert 'projects/MyProjectId/spaces/_default/documents/MyDocumentId' in call_args[0][0]
    assert response.status_code == 200


# ============================================================================
# Test: Response structure validation
# ============================================================================

def test_get_document_response_structure(mock_documents_api, sample_document_response):
    """Test that response has correct structure"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId'
    )
    
    # Verify structure
    data = response.json()
    assert 'data' in data
    assert 'attributes' in data['data']
    assert 'relationships' in data['data']
    assert 'links' in data['data']
    
    # Verify attributes
    attrs = data['data']['attributes']
    assert 'title' in attrs
    assert 'status' in attrs
    assert 'type' in attrs
    assert 'created' in attrs
    assert 'updated' in attrs
    
    # Verify relationships
    rels = data['data']['relationships']
    assert 'author' in rels
    assert 'project' in rels
    assert 'attachments' in rels
    assert 'comments' in rels


# ============================================================================
# Test: Error responses
# ============================================================================

def test_get_document_not_found(mock_documents_api):
    """Test get_document with 404 Not Found"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {
        "errors": [{
            "status": "404",
            "title": "Not Found",
            "detail": "Document not found"
        }]
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='NonExistent',
        space_id='MySpaceId',
        document_name='NonExistent'
    )
    
    # Verify
    assert response.status_code == 404
    assert 'errors' in response.json()


def test_get_document_forbidden(mock_documents_api):
    """Test get_document with 403 Forbidden"""
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.json.return_value = {
        "errors": [{
            "status": "403",
            "title": "Forbidden",
            "detail": "Access denied to document"
        }]
    }
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='SecretDocument'
    )
    
    # Verify
    assert response.status_code == 403


def test_get_document_unauthorized(mock_documents_api):
    """Test get_document with 401 Unauthorized"""
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
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId'
    )
    
    # Verify
    assert response.status_code == 401


def test_get_document_bad_request(mock_documents_api):
    """Test get_document with 400 Bad Request"""
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
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId',
        revision='invalid'
    )
    
    # Verify
    assert response.status_code == 400


def test_get_document_server_error(mock_documents_api):
    """Test get_document with 500 Internal Server Error"""
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
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId'
    )
    
    # Verify
    assert response.status_code == 500


# ============================================================================
# Test: Special characters in parameters
# ============================================================================

def test_get_document_with_special_characters(mock_documents_api, sample_document_response):
    """Test get_document with special characters in document name"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute with special characters
    response = mock_documents_api.get_document(
        project_id='Project-123',
        space_id='Space_456',
        document_name='Doc-Name_With.Special'
    )
    
    # Verify endpoint contains special characters
    call_args = mock_documents_api._session.get.call_args
    assert 'projects/Project-123/spaces/Space_456/documents/Doc-Name_With.Special' in call_args[0][0]
    assert response.status_code == 200


# ============================================================================
# Test: Document with relationships
# ============================================================================

def test_get_document_with_relationships(mock_documents_api, sample_document_response):
    """Test that document relationships are properly included"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId',
        include='author,project,attachments,comments'
    )
    
    # Verify relationships
    data = response.json()
    rels = data['data']['relationships']
    
    assert 'author' in rels
    assert rels['author']['data']['type'] == 'users'
    
    assert 'project' in rels
    assert rels['project']['data']['type'] == 'projects'
    
    assert 'attachments' in rels
    assert len(rels['attachments']['data']) > 0
    assert rels['attachments']['data'][0]['type'] == 'document_attachments'
    
    assert 'comments' in rels
    assert len(rels['comments']['data']) > 0
    assert rels['comments']['data'][0]['type'] == 'document_comments'


# ============================================================================
# Test: Document attributes validation
# ============================================================================

def test_get_document_attributes_validation(mock_documents_api, sample_document_response):
    """Test that all expected document attributes are present"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId'
    )
    
    # Verify all expected attributes
    attrs = response.json()['data']['attributes']
    
    assert attrs['autoSuspect'] == True
    assert attrs['title'] == 'Title'
    assert attrs['status'] == 'draft'
    assert attrs['type'] == 'req_specification'
    assert attrs['moduleFolder'] == 'MySpaceId'
    assert attrs['moduleName'] == 'MyDocumentId'
    assert attrs['usesOutlineNumbering'] == True
    assert 'created' in attrs
    assert 'updated' in attrs
    assert 'homePageContent' in attrs
    assert 'renderingLayouts' in attrs


# ============================================================================
# Test: Empty optional parameters
# ============================================================================

def test_get_document_with_none_optional_parameters(mock_documents_api, sample_document_response):
    """Test get_document with explicitly None optional parameters"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_document_response
    mock_documents_api._session.get.return_value = mock_response
    
    # Execute with None values
    response = mock_documents_api.get_document(
        project_id='MyProjectId',
        space_id='MySpaceId',
        document_name='MyDocumentId',
        fields=None,
        include=None,
        revision=None
    )
    
    # Verify
    assert response.status_code == 200
    call_args = mock_documents_api._session.get.call_args
    params = call_args[1]['params']
    
    # Should not have include or revision
    assert 'include' not in params
    assert 'revision' not in params
    # But should have default fields
    assert 'fields[documents]' in params
