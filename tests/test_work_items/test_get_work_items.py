"""
Pytest tests for get_work_items method.

Tests the get_work_items method from WorkItems class.
Uses mocks to avoid making real API calls.

Run with:
    pytest test_get_work_items.py -v
"""
import pytest
from unittest.mock import Mock


class TestGetWorkItemsMocked:
    """Unit tests for get_work_items method using mocks"""
    
    def test_get_work_items_success(self, mock_work_items_api, test_params):
        """Test successful retrieval of work items from a project"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/WI-001",
                    "attributes": {"title": "Test Item"}
                }
            ]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_items(test_params['project_id'])
        
        assert response.status_code == 200
        assert 'projects/' + test_params['project_id'] + '/workitems' in mock_work_items_api._session.get.call_args[0][0]
        print("\n✓ Mock: Work items retrieved from project successfully")
    
    def test_get_work_items_with_pagination(self, mock_work_items_api, test_params):
        """Test get work items with pagination"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_items(
            test_params['project_id'],
            page_size=10,
            page_number=2
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['page[size]'] == 10
        assert params['page[number]'] == 2
        print("\n✓ Mock: Pagination handled correctly")
    
    def test_get_work_items_with_query(self, mock_work_items_api, test_params):
        """Test get work items with query filter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_items(
            test_params['project_id'],
            query="status:open AND type:task"
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['query'] == "status:open AND type:task"
        print("\n✓ Mock: Query filter handled correctly")
    
    def test_get_work_items_project_not_found(self, mock_work_items_api):
        """Test get work items with non-existent project"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{"status": "404", "title": "Not Found"}]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_items("NonExistentProject")
        
        assert response.status_code == 404
        print("\n✓ Mock: Project not found (404) handled correctly")
    
    def test_get_work_items_unauthorized(self, mock_work_items_api, test_params):
        """Test get work items with invalid authentication"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [{"status": "401", "title": "Unauthorized"}]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_items(test_params['project_id'])
        
        assert response.status_code == 401
        print("\n✓ Mock: Unauthorized (401) handled correctly")
    
    def test_get_work_items_all_parameters(self, mock_work_items_api, test_params):
        """Test get work items with all parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_items(
            test_params['project_id'],
            page_size=50,
            page_number=1,
            fields={'workitems': 'id,title'},
            include="author",
            query="status:open",
            sort="created",
            revision="123"
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['page[size]'] == 50
        assert params['query'] == "status:open"
        assert params['sort'] == "created"
        print("\n✓ Mock: All parameters handled correctly")
