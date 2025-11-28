"""
Pytest tests for post_branch_document method.

Tests the post_branch_document method from Documents class.
All tests use mocks.

Run with:
    pytest test_post_branch_document.py -v
"""
import pytest
from unittest.mock import Mock


# ============================================================================
# Mock Tests
# ============================================================================

class TestPostBranchDocumentMock:
    """Mock tests for post_branch_document method"""
    
    def test_post_branch_document_basic(self, mock_documents_api):
        """Test branching a document with basic parameters"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyBranchedDocument"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "_default"
        document_name = "MyDocument"
        branch_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "BranchedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_branch_document(
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            branch_data=branch_data
        )
        
        # Assert
        assert response.status_code == 201
        mock_documents_api._session.post.assert_called_once()
        call_args = mock_documents_api._session.post.call_args
        
        # Verify endpoint
        expected_url = f"https://test.polarion.com/polarion/rest/v1/projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/branch"
        assert call_args[0][0] == expected_url
        
        # Verify JSON body
        assert call_args[1]['json'] == branch_data
        assert 'params' not in call_args[1] or call_args[1]['params'] is None
    
    def test_post_branch_document_with_revision(self, mock_documents_api):
        """Test branching a document with revision parameter"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyBranchedDocument"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "_default"
        document_name = "MyDocument"
        revision = "1234"
        branch_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "BranchedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_branch_document(
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            branch_data=branch_data,
            revision=revision
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        
        # Verify params
        assert call_args[1]['params'] == {'revision': revision}
    
    def test_post_branch_document_with_all_fields(self, mock_documents_api):
        """Test branching a document with all optional fields"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyBranchedDocument"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "_default"
        document_name = "MyDocument"
        revision = "1234"
        branch_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "BranchedDoc",
            "copyWorkflowStatusAndSignatures": True,
            "query": "status:open"
        }
        
        # Execute
        response = mock_documents_api.post_branch_document(
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            branch_data=branch_data,
            revision=revision
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        
        # Verify all fields in body
        assert call_args[1]['json']['copyWorkflowStatusAndSignatures'] == True
        assert call_args[1]['json']['query'] == "status:open"
    
    def test_post_branch_document_not_found(self, mock_documents_api):
        """Test branching a document that doesn't exist"""
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
        branch_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "BranchedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_branch_document(
            project_id="INVALID",
            space_id="_default",
            document_name="NonExistent",
            branch_data=branch_data
        )
        
        # Assert
        assert response.status_code == 404
    
    def test_post_branch_document_unauthorized(self, mock_documents_api):
        """Test branching a document without proper authorization"""
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
        branch_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "BranchedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_branch_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            branch_data=branch_data
        )
        
        # Assert
        assert response.status_code == 401
    
    def test_post_branch_document_forbidden(self, mock_documents_api):
        """Test branching a document without sufficient permissions"""
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
        branch_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "BranchedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_branch_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            branch_data=branch_data
        )
        
        # Assert
        assert response.status_code == 403
    
    def test_post_branch_document_bad_request(self, mock_documents_api):
        """Test branching a document with invalid data"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid branch data"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data - invalid branch data
        branch_data = {
            "invalidField": "someValue"
        }
        
        # Execute
        response = mock_documents_api.post_branch_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            branch_data=branch_data
        )
        
        # Assert
        assert response.status_code == 400
    
    def test_post_branch_document_conflict(self, mock_documents_api):
        """Test branching a document when target already exists"""
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
        branch_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "ExistingDoc"
        }
        
        # Execute
        response = mock_documents_api.post_branch_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            branch_data=branch_data
        )
        
        # Assert
        assert response.status_code == 409
    
    def test_post_branch_document_server_error(self, mock_documents_api):
        """Test branching a document with server error"""
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
        branch_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "BranchedDoc"
        }
        
        # Execute
        response = mock_documents_api.post_branch_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            branch_data=branch_data
        )
        
        # Assert
        assert response.status_code == 500
    
    def test_post_branch_document_url_construction(self, mock_documents_api):
        """Test URL construction for branch document endpoint"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data with special characters
        project_id = "TEST_PROJECT"
        space_id = "MySpace"
        document_name = "MyDocument"
        branch_data = {"targetDocumentName": "NewDoc"}
        
        # Execute
        mock_documents_api.post_branch_document(
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            branch_data=branch_data
        )
        
        # Assert URL construction
        call_args = mock_documents_api._session.post.call_args
        expected_url = f"https://test.polarion.com/polarion/rest/v1/projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/branch"
        assert call_args[0][0] == expected_url
    
    def test_post_branch_document_minimal_data(self, mock_documents_api):
        """Test branching a document with minimal required data"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyBranchedDocument"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data - minimal fields
        branch_data = {}
        
        # Execute
        response = mock_documents_api.post_branch_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            branch_data=branch_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        assert call_args[1]['json'] == branch_data
    
    def test_post_branch_document_with_query_filter(self, mock_documents_api):
        """Test branching a document with query filter"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyBranchedDocument"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data with query
        branch_data = {
            "targetProjectId": "TARGET_PROJECT",
            "targetSpaceId": "TARGET_SPACE",
            "targetDocumentName": "BranchedDoc",
            "query": "status:open AND type:requirement"
        }
        
        # Execute
        response = mock_documents_api.post_branch_document(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="MyDocument",
            branch_data=branch_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        assert "query" in call_args[1]['json']
        assert call_args[1]['json']['query'] == "status:open AND type:requirement"
