"""
Tests for delete_collections method.
"""
import pytest


class TestDeleteCollections:
    """Tests for delete_collections method"""
    
    def test_delete_collections(self, mock_collections_api):
        """Test deleting collections"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_collections_api._session.request.return_value = mock_response
        
        # Prepare data
        collections_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/MyCollectionId"
                }
            ]
        }
        
        # Execute
        response = mock_collections_api.delete_collections(
            project_id='MyProjectId',
            collections_data=collections_data
        )
        
        # Verify
        assert response.status_code == 204
        mock_collections_api._session.request.assert_called_once()
        call_args = mock_collections_api._session.request.call_args
        assert call_args[0][0] == 'DELETE'
        assert 'MyProjectId/collections' in call_args[0][1]
    
    def test_delete_collections_multiple(self, mock_collections_api):
        """Test deleting multiple collections"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_collections_api._session.request.return_value = mock_response
        
        # Prepare data with multiple collections
        collections_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/Collection1"
                },
                {
                    "type": "collections",
                    "id": "MyProjectId/Collection2"
                }
            ]
        }
        
        # Execute
        response = mock_collections_api.delete_collections(
            project_id='MyProjectId',
            collections_data=collections_data
        )
        
        # Verify
        assert response.status_code == 204
