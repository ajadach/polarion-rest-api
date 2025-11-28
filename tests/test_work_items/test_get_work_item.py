"""
Pytest tests for get_work_item method.

Tests the get_work_item method from WorkItems class.
Uses mocks to avoid making real API calls.

Run with:
    pytest test_get_work_item.py -v
"""
import pytest
from unittest.mock import Mock


class TestGetWorkItemMocked:
    """Unit tests for get_work_item method using mocks"""
    
    def test_get_work_item_success(self, mock_work_items_api, test_params):
        """Test successful retrieval of a single work item"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/WI-001",
                "attributes": {
                    "title": "Test Work Item",
                    "status": "open",
                    "description": {"type": "text/plain", "value": "Description"}
                }
            }
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item(
            test_params['project_id'],
            "WI-001"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['data']['type'] == 'workitems'
        print("\n✓ Mock: Single work item retrieved successfully")
    
    def test_get_work_item_with_fields(self, mock_work_items_api, test_params):
        """Test get work item with custom fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item(
            test_params['project_id'],
            "WI-001",
            fields={'workitems': 'id,title,status'}
        )
        
        assert response.status_code == 200
        print("\n✓ Mock: Custom fields handled correctly")
    
    def test_get_work_item_with_include(self, mock_work_items_api, test_params):
        """Test get work item with include parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item(
            test_params['project_id'],
            "WI-001",
            include="author,assignee"
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['include'] == "author,assignee"
        print("\n✓ Mock: Include parameter handled correctly")
    
    def test_get_work_item_with_revision(self, mock_work_items_api, test_params):
        """Test get work item with revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item(
            test_params['project_id'],
            "WI-001",
            revision="12345"
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['revision'] == "12345"
        print("\n✓ Mock: Revision parameter handled correctly")
    
    def test_get_work_item_not_found(self, mock_work_items_api, test_params):
        """Test get work item that doesn't exist"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Work item not found"
                }
            ]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item(
            test_params['project_id'],
            "NonExistentWI"
        )
        
        assert response.status_code == 404
        print("\n✓ Mock: Work item not found (404) handled correctly")
    
    def test_get_work_item_unauthorized(self, mock_work_items_api, test_params):
        """Test get work item with invalid authentication"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [{"status": "401", "title": "Unauthorized"}]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item(
            test_params['project_id'],
            "WI-001"
        )
        
        assert response.status_code == 401
        print("\n✓ Mock: Unauthorized (401) handled correctly")
    
    def test_get_work_item_all_parameters(self, mock_work_items_api, test_params):
        """Test get work item with all parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item(
            test_params['project_id'],
            "WI-001",
            fields={'workitems': 'id,title'},
            include="author,assignee",
            revision="999"
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['include'] == "author,assignee"
        assert params['revision'] == "999"
        print("\n✓ Mock: All parameters handled correctly")
