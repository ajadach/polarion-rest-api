"""
Tests for get_collections_relationship method.
"""
import pytest


class TestGetCollectionsRelationship:
    """Tests for get_collections_relationship method"""
    
    def test_get_collections_relationship(self, mock_collections_api):
        """Test getting collections relationships"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/WI-123"
                }
            ]
        }
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_collections_api.get_collections_relationship(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            relationship_id='workitems'
        )
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
    
    def test_get_collections_relationship_with_all_params(self, mock_collections_api):
        """Test getting collections relationships with all parameters"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_collections_api.get_collections_relationship(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            relationship_id='workitems',
            page_size=50,
            page_number=1,
            fields={'fields[workitems]': 'id,title'},
            include='author',
            revision='1234'
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_collections_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 50
        assert params['page[number]'] == 1
        assert params['include'] == 'author'
        assert params['revision'] == '1234'
    
    def test_get_collections_relationship_with_pagination(self, mock_collections_api):
        """Test getting collections relationships with pagination"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_collections_api.get_collections_relationship(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            relationship_id='workitems',
            page_size=25,
            page_number=2
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_collections_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 25
        assert params['page[number]'] == 2
    
    def test_get_collections_relationship_url_construction(self, mock_collections_api):
        """Test URL construction for get_collections_relationship"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        mock_collections_api.get_collections_relationship(
            project_id='MyProjectId',
            collection_id='MyCollectionId',
            relationship_id='workitems'
        )
        
        # Verify URL
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/MyProjectId/collections/MyCollectionId/relationships/workitems"
        call_args = mock_collections_api._session.get.call_args
        assert call_args[0][0] == expected_url
