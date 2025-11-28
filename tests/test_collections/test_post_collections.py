"""
Tests for post_collections method.
"""
import pytest


class TestPostCollections:
    """Tests for post_collections method"""
    
    def test_post_collections(self, mock_collections_api):
        """Test creating collections"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/NewCollection",
                    "attributes": {
                        "name": "New Collection"
                    }
                }
            ]
        }
        mock_collections_api._session.post.return_value = mock_response
        
        # Prepare data
        collections_data = {
            "data": [
                {
                    "type": "collections",
                    "attributes": {
                        "id": "NewCollection",
                        "name": "New Collection",
                        "description": {
                            "type": "text/html",
                            "value": "<p>New collection description</p>"
                        }
                    }
                }
            ]
        }
        
        # Execute
        response = mock_collections_api.post_collections(
            project_id='MyProjectId',
            collections_data=collections_data
        )
        
        # Verify
        assert response.status_code == 201
        data = response.json()
        assert 'data' in data
        mock_collections_api._session.post.assert_called_once()
    
    def test_post_collections_with_relationships(self, mock_collections_api):
        """Test creating collections with relationships"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_collections_api._session.post.return_value = mock_response
        
        # Prepare data with relationships
        collections_data = {
            "data": [
                {
                    "type": "collections",
                    "attributes": {
                        "id": "NewCollection",
                        "name": "New Collection"
                    },
                    "relationships": {
                        "documents": {
                            "data": [
                                {
                                    "type": "documents",
                                    "id": "MyProjectId/MySpace/Doc1",
                                    "revision": "1234"
                                }
                            ]
                        }
                    }
                }
            ]
        }
        
        # Execute
        response = mock_collections_api.post_collections(
            project_id='MyProjectId',
            collections_data=collections_data
        )
        
        # Verify
        assert response.status_code == 201
    
    def test_post_collections_empty_data(self, mock_collections_api):
        """Test creating collections with empty data"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [{
                "status": "400",
                "title": "Bad Request"
            }]
        }
        mock_collections_api._session.post.return_value = mock_response
        
        # Prepare empty data
        collections_data = {"data": []}
        
        # Execute
        response = mock_collections_api.post_collections(
            project_id='MyProjectId',
            collections_data=collections_data
        )
        
        # Verify
        assert response.status_code == 400
