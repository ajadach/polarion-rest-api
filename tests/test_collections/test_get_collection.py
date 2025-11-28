"""
Tests for get_collection method.
"""
import pytest


class TestGetCollection:
    """Tests for get_collection method"""
    
    def test_get_collection_basic(self, mock_collections_api):
        """Test getting a single collection"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "collections",
                "id": "MyProjectId/MyCollectionId",
                "attributes": {
                    "name": "My Collection",
                    "description": {
                        "type": "text/html",
                        "value": "<p>Description</p>"
                    }
                }
            }
        }
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_collections_api.get_collection(
            project_id='MyProjectId',
            collection_id='MyCollectionId'
        )
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert data['data']['type'] == 'collections'
        assert data['data']['id'] == 'MyProjectId/MyCollectionId'
    
    def test_get_collection_with_revision(self, mock_collections_api):
        """Test getting a collection with revision"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_collections_api.get_collection(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            revision='1234'
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_collections_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '1234'
    
    def test_get_collection_with_include(self, mock_collections_api):
        """Test getting a collection with include parameter"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_collections_api.get_collection(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            include='author,documents'
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_collections_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'author,documents'
    
    def test_get_collection_not_found(self, mock_collections_api):
        """Test getting non-existent collection"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Collection not found"
                }
            ]
        }
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_collections_api.get_collection(
            project_id='MyProjectId',
            collection_id='NonExistentCollection'
        )
        
        # Verify
        assert response.status_code == 404
        errors = response.json()
        assert 'errors' in errors
    
    def test_get_collection_url_construction(self, mock_collections_api):
        """Test URL construction for get_collection"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        mock_collections_api.get_collection(
            project_id='MyProjectId',
            collection_id='MyCollectionId'
        )
        
        # Verify URL
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/MyProjectId/collections/MyCollectionId"
        call_args = mock_collections_api._session.get.call_args
        assert call_args[0][0] == expected_url
