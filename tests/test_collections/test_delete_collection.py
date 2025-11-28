"""
Tests for delete_collection method.
"""
import pytest


class TestDeleteCollection:
    """Tests for delete_collection method"""
    
    def test_delete_collection(self, mock_collections_api):
        """Test deleting a single collection"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_collections_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_collections_api.delete_collection(
            project_id='MyProjectId',
            collection_id='MyCollectionId'
        )
        
        # Verify
        assert response.status_code == 204
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/MyProjectId/collections/MyCollectionId"
        mock_collections_api._session.delete.assert_called_once()
        call_args = mock_collections_api._session.delete.call_args
        assert call_args[0][0] == expected_url
    
    def test_delete_collection_not_found(self, mock_collections_api):
        """Test deleting non-existent collection returns 404"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found"
            }]
        }
        mock_collections_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_collections_api.delete_collection(
            project_id='MyProjectId',
            collection_id='NonExistent'
        )
        
        # Verify
        assert response.status_code == 404
