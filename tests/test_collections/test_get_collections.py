"""
Tests for get_collections method.
"""
import pytest


class TestGetCollections:
    """Tests for get_collections method"""
    
    def test_get_collections_basic(self, mock_collections_api):
        """Test getting collections list with basic parameters"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/MyCollectionId",
                    "attributes": {
                        "name": "My Collection"
                    }
                }
            ]
        }
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_collections_api.get_collections(
            project_id='MyProjectId'
        )
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert len(data['data']) > 0
        mock_collections_api._session.get.assert_called_once()
    
    def test_get_collections_with_pagination(self, mock_collections_api):
        """Test getting collections with pagination"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_collections_api.get_collections(
            project_id='MyProjectId',
            page_size=50,
            page_number=1
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_collections_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 50
        assert params['page[number]'] == 1
    
    def test_get_collections_with_revision(self, mock_collections_api):
        """Test getting collections with revision parameter"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_collections_api.get_collections(
            project_id='MyProjectId',
            revision='1234'
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_collections_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '1234'
    
    def test_get_collections_with_query_and_sort(self, mock_collections_api):
        """Test get_collections with query and sort parameters"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_collections_api.get_collections(
            project_id='MyProjectId',
            query='status:open',
            sort='created'
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_collections_api._session.get.call_args
        params = call_args[1]['params']
        assert params['query'] == 'status:open'
        assert params['sort'] == 'created'
    
    def test_get_collections_url_construction(self, mock_collections_api):
        """Test URL construction for get_collections"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_collections_api._session.get.return_value = mock_response
        
        # Execute
        mock_collections_api.get_collections(
            project_id='MyProjectId'
        )
        
        # Verify URL
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/MyProjectId/collections"
        call_args = mock_collections_api._session.get.call_args
        assert call_args[0][0] == expected_url
