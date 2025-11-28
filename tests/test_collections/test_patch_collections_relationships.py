"""
Tests for patch_collections_relationships method.
"""
import pytest


class TestPatchCollectionsRelationships:
    """Tests for patch_collections_relationships method"""
    
    def test_patch_collections_relationships(self, mock_collections_api):
        """Test updating collections relationships"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_collections_api._session.patch.return_value = mock_response
        
        # Prepare data
        relationships_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/WI-123",
                    "revision": "1234"
                }
            ]
        }
        
        # Execute
        response = mock_collections_api.patch_collections_relationships(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            relationship_id='workitems',
            relationships_data=relationships_data
        )
        
        # Verify
        assert response.status_code == 204
        mock_collections_api._session.patch.assert_called_once()
    
    def test_patch_collections_relationships_multiple(self, mock_collections_api):
        """Test updating multiple collections relationships"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_collections_api._session.patch.return_value = mock_response
        
        # Prepare data with multiple relationships
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
        response = mock_collections_api.patch_collections_relationships(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            relationship_id='workitems',
            relationships_data=relationships_data
        )
        
        # Verify
        assert response.status_code == 204
