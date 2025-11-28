"""
Tests for delete_collections_relationship method.
"""
import pytest


class TestDeleteCollectionsRelationship:
    """Tests for delete_collections_relationship method"""
    
    def test_delete_collections_relationship(self, mock_collections_api):
        """Test deleting collections relationships"""
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
        response = mock_collections_api.delete_collections_relationship(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            relationship_id='workitems',
            collections_data=collections_data
        )
        
        # Verify
        assert response.status_code == 204
        mock_collections_api._session.request.assert_called_once()
