"""
Pytest tests for get_current_enum_options_for_work_item method.

Run with:
    pytest test_get_current_enum_options_for_work_item.py -v
"""
import pytest
from unittest.mock import Mock


class TestGetCurrentEnumOptionsForWorkItemMocked:
    """Unit tests for get_current_enum_options_for_work_item method"""
    
    def test_get_current_enum_options_success(self, mock_work_items_api, test_params):
        """Test successful retrieval of current enum options"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "enums", "id": "option1"},
                {"type": "enums", "id": "option2"}
            ]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_current_enum_options_for_work_item(
            test_params['project_id'],
            "WI-001",
            "status"
        )
        
        assert response.status_code == 200
        assert len(response.json()['data']) == 2
        print("\n✓ Mock: Current enum options retrieved successfully")
    
    def test_get_current_enum_options_with_pagination(self, mock_work_items_api, test_params):
        """Test get current enum options with pagination"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_current_enum_options_for_work_item(
            test_params['project_id'],
            "WI-001",
            "status",
            page_size=10,
            page_number=1
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['page[size]'] == 10
        print("\n✓ Mock: Pagination handled correctly")
    
    def test_get_current_enum_options_with_revision(self, mock_work_items_api, test_params):
        """Test get current enum options with revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_current_enum_options_for_work_item(
            test_params['project_id'],
            "WI-001",
            "status",
            revision="12345"
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['revision'] == "12345"
        print("\n✓ Mock: Revision parameter handled correctly")
    
    def test_get_current_enum_options_not_found(self, mock_work_items_api, test_params):
        """Test get current enum options for non-existent work item"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{"status": "404", "title": "Not Found"}]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_current_enum_options_for_work_item(
            test_params['project_id'],
            "NonExistent",
            "status"
        )
        
        assert response.status_code == 404
        print("\n✓ Mock: Not found (404) handled correctly")
