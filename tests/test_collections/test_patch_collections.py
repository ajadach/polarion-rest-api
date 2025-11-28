"""
Tests for patch_collections method.
"""
import pytest


class TestPatchCollections:
    """Tests for patch_collections method"""
    
    def test_patch_collections(self, mock_collections_api):
        """Test updating a collection"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_collections_api._session.patch.return_value = mock_response
        
        # Prepare data
        collection_data = {
            "data": {
                "type": "collections",
                "id": "MyProjectId/MyCollectionId",
                "attributes": {
                    "name": "Updated Collection",
                    "description": {
                        "type": "text/html",
                        "value": "<p>Updated description</p>"
                    }
                }
            }
        }
        
        # Execute
        response = mock_collections_api.patch_collections(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            collection_data=collection_data
        )
        
        # Verify
        assert response.status_code == 204
        mock_collections_api._session.patch.assert_called_once()
    
    def test_patch_collections_with_relationships(self, mock_collections_api):
        """Test updating a collection with relationships"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_collections_api._session.patch.return_value = mock_response
        
        # Prepare data with relationships
        collection_data = {
            "data": {
                "type": "collections",
                "id": "MyProjectId/MyCollectionId",
                "attributes": {
                    "name": "Updated Collection"
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
        }
        
        # Execute
        response = mock_collections_api.patch_collections(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            collection_data=collection_data
        )
        
        # Verify
        assert response.status_code == 204
