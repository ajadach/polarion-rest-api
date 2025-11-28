"""
Tests for post_collections_relationships method.
"""
import pytest


class TestPostCollectionsRelationships:
    """Tests for post_collections_relationships method"""
    
    def test_post_collections_relationships(self, mock_collections_api):
        """Test creating collections relationships"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/WI-123"
                }
            ]
        }
        mock_collections_api._session.post.return_value = mock_response
        
        # Prepare data
        relationships_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/WI-123",
                    "revision": "1234"
                },
                {
                    "type": "workitems",
                    "id": "MyProjectId/WI-456",
                    "revision": "5678"
                }
            ]
        }
        
        # Execute
        response = mock_collections_api.post_collections_relationships(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            relationship_id='workitems',
            relationships_data=relationships_data
        )
        
        # Verify
        assert response.status_code == 201
        data = response.json()
        assert 'data' in data
        mock_collections_api._session.post.assert_called_once()
    
    def test_post_collections_relationships_single(self, mock_collections_api):
        """Test creating single collections relationship"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_collections_api._session.post.return_value = mock_response
        
        # Prepare data with single relationship
        relationships_data = {
            "data": [
                {
                    "type": "documents",
                    "id": "MyProjectId/MySpace/Doc1",
                    "revision": "1234"
                }
            ]
        }
        
        # Execute
        response = mock_collections_api.post_collections_relationships(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            relationship_id='documents',
            relationships_data=relationships_data
        )
        
        # Verify
        assert response.status_code == 201
