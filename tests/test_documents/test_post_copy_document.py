"""
Pytest tests for post_copy_document method.

Tests the post_copy_document method from Documents class.
All tests use mocks.

Run with:
    pytest test_post_copy_document.py -v
"""
import pytest
from unittest.mock import Mock


# ============================================================================
# Mock Tests
# ============================================================================

class TestPostCopyDocumentMock:
    """Mock tests for post_copy_document method"""
    
    def test_post_copy_document_basic(self, mock_documents_api):
        """Test copying a document with basic parameters"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyCopiedDocument"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "_default"
        document_name = "MyDocument"
        copy_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "CopiedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            copy_data=copy_data
        )
        
        # Assert
        assert response.status_code == 201
        mock_documents_api._session.post.assert_called_once()
        call_args = mock_documents_api._session.post.call_args
        
        # Verify endpoint
        expected_url = f"https://test.polarion.com/polarion/rest/v1/projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/copy"
        assert call_args[0][0] == expected_url
        
        # Verify JSON body
        assert call_args[1]['json'] == copy_data
        assert 'params' not in call_args[1] or call_args[1]['params'] is None
    
    def test_post_copy_document_with_revision(self, mock_documents_api):
        """Test copying a document with revision parameter"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyCopiedDocument"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "_default"
        document_name = "MyDocument"
        revision = "5678"
        copy_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "CopiedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            copy_data=copy_data,
            revision=revision
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        
        # Verify params
        assert call_args[1]['params'] == {'revision': revision}
    
    def test_post_copy_document_with_all_fields(self, mock_documents_api):
        """Test copying a document with all optional fields"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyCopiedDocument"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "_default"
        document_name = "MyDocument"
        revision = "5678"
        copy_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "CopiedDoc",
            "removeOutgoingLinks": True,
            "linkOriginalItemsWithRole": "duplicates"
        }
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            copy_data=copy_data,
            revision=revision
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        
        # Verify all fields in body
        assert call_args[1]['json']['removeOutgoingLinks'] == True
        assert call_args[1]['json']['linkOriginalItemsWithRole'] == "duplicates"
    
    def test_post_copy_document_remove_links(self, mock_documents_api):
        """Test copying a document with removeOutgoingLinks option"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyCopiedDocument"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        copy_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "CopiedDoc",
            "removeOutgoingLinks": True
        }
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            copy_data=copy_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        assert call_args[1]['json']['removeOutgoingLinks'] == True
    
    def test_post_copy_document_link_original(self, mock_documents_api):
        """Test copying a document with linking to original items"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyCopiedDocument"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        copy_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "CopiedDoc",
            "linkOriginalItemsWithRole": "relates_to"
        }
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            copy_data=copy_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        assert call_args[1]['json']['linkOriginalItemsWithRole'] == "relates_to"
    
    def test_post_copy_document_not_found(self, mock_documents_api):
        """Test copying a document that doesn't exist"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Document not found"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        copy_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "CopiedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id="INVALID",
            space_id="_default",
            document_name="NonExistent",
            copy_data=copy_data
        )
        
        # Assert
        assert response.status_code == 404
    
    def test_post_copy_document_unauthorized(self, mock_documents_api):
        """Test copying a document without proper authorization"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [{
                "status": "401",
                "title": "Unauthorized"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        copy_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "CopiedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            copy_data=copy_data
        )
        
        # Assert
        assert response.status_code == 401
    
    def test_post_copy_document_forbidden(self, mock_documents_api):
        """Test copying a document without sufficient permissions"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "Insufficient permissions"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        copy_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "CopiedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            copy_data=copy_data
        )
        
        # Assert
        assert response.status_code == 403
    
    def test_post_copy_document_bad_request(self, mock_documents_api):
        """Test copying a document with invalid data"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid copy data"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data - invalid copy data
        copy_data = {
            "invalidField": "someValue"
        }
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            copy_data=copy_data
        )
        
        # Assert
        assert response.status_code == 400
    
    def test_post_copy_document_conflict(self, mock_documents_api):
        """Test copying a document when target already exists"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "errors": [{
                "status": "409",
                "title": "Conflict",
                "detail": "Target document already exists"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        copy_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "ExistingDoc"
        }
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            copy_data=copy_data
        )
        
        # Assert
        assert response.status_code == 409
    
    def test_post_copy_document_server_error(self, mock_documents_api):
        """Test copying a document with server error"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [{
                "status": "500",
                "title": "Internal Server Error"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        copy_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "CopiedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            copy_data=copy_data
        )
        
        # Assert
        assert response.status_code == 500
    
    def test_post_copy_document_url_construction(self, mock_documents_api):
        """Test URL construction for copy document endpoint"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data with special characters
        project_id = "TEST_PROJECT"
        space_id = "MySpace"
        document_name = "MyDocument"
        copy_data = {"targetDocumentName": "NewDoc"}
        
        # Execute
        mock_documents_api.post_copy_document(
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            copy_data=copy_data
        )
        
        # Assert URL construction
        call_args = mock_documents_api._session.post.call_args
        expected_url = f"https://test.polarion.com/polarion/rest/v1/projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/copy"
        assert call_args[0][0] == expected_url
    
    def test_post_copy_document_minimal_data(self, mock_documents_api):
        """Test copying a document with minimal required data"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyCopiedDocument"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data - minimal fields
        copy_data = {}
        
        # Execute
        response = mock_documents_api.post_copy_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            copy_data=copy_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        assert call_args[1]['json'] == copy_data
