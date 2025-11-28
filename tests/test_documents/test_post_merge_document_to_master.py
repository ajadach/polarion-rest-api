"""
Pytest tests for post_merge_document_to_master method.

Tests the post_merge_document_to_master method from Documents class.
All tests use mocks.

Run with:
    pytest test_post_merge_document_to_master.py -v
"""
import pytest
from unittest.mock import Mock


# ============================================================================
# Mock Tests
# ============================================================================

class TestPostMergeDocumentToMasterMock:
    """Mock tests for post_merge_document_to_master method"""
    
    def test_post_merge_to_master_basic(self, mock_documents_api):
        """Test merging to master with no parameters"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 202
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "job-123"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "_default"
        document_name = "BranchedDocument"
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id=project_id,
            space_id=space_id,
            document_name=document_name
        )
        
        # Assert
        assert response.status_code == 202
        mock_documents_api._session.post.assert_called_once()
        call_args = mock_documents_api._session.post.call_args
        
        # Verify endpoint
        expected_url = f"https://test.polarion.com/polarion/rest/v1/projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/mergeToMaster"
        assert call_args[0][0] == expected_url
        
        # Verify JSON body (should be empty dict when no merge_data provided)
        assert call_args[1]['json'] == {}
    
    def test_post_merge_to_master_with_merge_data(self, mock_documents_api):
        """Test merging to master with merge data"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 202
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "job-456"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "_default"
        document_name = "BranchedDocument"
        merge_data = {
            "createBaseline": True,
            "userFilter": "status:open"
        }
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            merge_data=merge_data
        )
        
        # Assert
        assert response.status_code == 202
        call_args = mock_documents_api._session.post.call_args
        
        # Verify JSON body
        assert call_args[1]['json'] == merge_data
    
    def test_post_merge_to_master_with_baseline(self, mock_documents_api):
        """Test merging to master with baseline creation"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 202
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "job-789"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        merge_data = {
            "createBaseline": True
        }
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="BranchedDocument",
            merge_data=merge_data
        )
        
        # Assert
        assert response.status_code == 202
        call_args = mock_documents_api._session.post.call_args
        assert call_args[1]['json']['createBaseline'] == True
    
    def test_post_merge_to_master_with_user_filter(self, mock_documents_api):
        """Test merging to master with user filter"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 202
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "job-321"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        merge_data = {
            "userFilter": "status:resolved AND type:requirement"
        }
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="BranchedDocument",
            merge_data=merge_data
        )
        
        # Assert
        assert response.status_code == 202
        call_args = mock_documents_api._session.post.call_args
        assert call_args[1]['json']['userFilter'] == "status:resolved AND type:requirement"
    
    def test_post_merge_to_master_with_all_options(self, mock_documents_api):
        """Test merging to master with all options"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 202
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "job-999"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        merge_data = {
            "createBaseline": True,
            "userFilter": "status:approved"
        }
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="BranchedDocument",
            merge_data=merge_data
        )
        
        # Assert
        assert response.status_code == 202
        call_args = mock_documents_api._session.post.call_args
        assert call_args[1]['json']['createBaseline'] == True
        assert call_args[1]['json']['userFilter'] == "status:approved"
    
    def test_post_merge_to_master_not_found(self, mock_documents_api):
        """Test merging to master when document doesn't exist"""
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
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id="INVALID",
            space_id="_default",
            document_name="NonExistent"
        )
        
        # Assert
        assert response.status_code == 404
    
    def test_post_merge_to_master_unauthorized(self, mock_documents_api):
        """Test merging to master without proper authorization"""
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
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="BranchedDocument"
        )
        
        # Assert
        assert response.status_code == 401
    
    def test_post_merge_to_master_forbidden(self, mock_documents_api):
        """Test merging to master without sufficient permissions"""
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
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="BranchedDocument"
        )
        
        # Assert
        assert response.status_code == 403
    
    def test_post_merge_to_master_bad_request(self, mock_documents_api):
        """Test merging to master with invalid data"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Document is not a branch"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        merge_data = {
            "invalidField": "someValue"
        }
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="NotABranch",
            merge_data=merge_data
        )
        
        # Assert
        assert response.status_code == 400
    
    def test_post_merge_to_master_conflict(self, mock_documents_api):
        """Test merging to master with conflicts"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "errors": [{
                "status": "409",
                "title": "Conflict",
                "detail": "Merge conflicts detected"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="BranchedDocument"
        )
        
        # Assert
        assert response.status_code == 409
    
    def test_post_merge_to_master_server_error(self, mock_documents_api):
        """Test merging to master with server error"""
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
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="BranchedDocument"
        )
        
        # Assert
        assert response.status_code == 500
    
    def test_post_merge_to_master_url_construction(self, mock_documents_api):
        """Test URL construction for merge to master endpoint"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 202
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "MySpace"
        document_name = "BranchedDoc"
        
        # Execute
        mock_documents_api.post_merge_document_to_master(
            project_id=project_id,
            space_id=space_id,
            document_name=document_name
        )
        
        # Assert URL construction
        call_args = mock_documents_api._session.post.call_args
        expected_url = f"https://test.polarion.com/polarion/rest/v1/projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/mergeToMaster"
        assert call_args[0][0] == expected_url
    
    def test_post_merge_to_master_returns_job_id(self, mock_documents_api):
        """Test that merge to master returns a job ID"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 202
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "merge-job-67890",
                "attributes": {
                    "status": "running"
                }
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="BranchedDocument"
        )
        
        # Assert
        assert response.status_code == 202
        data = response.json()
        assert 'data' in data
        assert data['data']['type'] == 'jobs'
        assert 'id' in data['data']
    
    def test_post_merge_to_master_none_merge_data(self, mock_documents_api):
        """Test merging to master with None merge_data explicitly"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 202
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "job-none"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Execute with explicit None
        response = mock_documents_api.post_merge_document_to_master(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="BranchedDocument",
            merge_data=None
        )
        
        # Assert
        assert response.status_code == 202
        call_args = mock_documents_api._session.post.call_args
        # When merge_data is None, should send empty dict
        assert call_args[1]['json'] == {}
    
    def test_post_merge_to_master_baseline_false(self, mock_documents_api):
        """Test merging to master without creating baseline"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 202
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "job-no-baseline"
            }
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        merge_data = {
            "createBaseline": False
        }
        
        # Execute
        response = mock_documents_api.post_merge_document_to_master(
            project_id="TEST_PROJECT",
            space_id="_default",
            document_name="BranchedDocument",
            merge_data=merge_data
        )
        
        # Assert
        assert response.status_code == 202
        call_args = mock_documents_api._session.post.call_args
        assert call_args[1]['json']['createBaseline'] == False
