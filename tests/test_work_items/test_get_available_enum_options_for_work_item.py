"""
Pytest tests for get_available_enum_options_for_work_item method.

Run with:
    pytest test_get_available_enum_options_for_work_item.py -v
"""
import pytest
from unittest.mock import Mock


class TestGetAvailableEnumOptionsForWorkItemMocked:
    """Unit tests for get_available_enum_options_for_work_item method"""
    
    def test_get_available_enum_options_success(self, mock_work_items_api, test_params):
        """Test successful retrieval of available enum options"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "enums", "id": "open"},
                {"type": "enums", "id": "closed"},
                {"type": "enums", "id": "in_progress"}
            ]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_available_enum_options_for_work_item(
            test_params['project_id'],
            "WI-001",
            "status"
        )
        
        assert response.status_code == 200
        assert len(response.json()['data']) == 3
        print("\n✓ Mock: Available enum options retrieved successfully")
    
    def test_get_available_enum_options_with_pagination(self, mock_work_items_api, test_params):
        """Test get available enum options with pagination"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_available_enum_options_for_work_item(
            test_params['project_id'],
            "WI-001",
            "priority",
            page_size=5,
            page_number=1
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['page[size]'] == 5
        assert params['page[number]'] == 1
        print("\n✓ Mock: Pagination handled correctly")
    
    def test_get_available_enum_options_invalid_field(self, mock_work_items_api, test_params):
        """Test get available enum options for invalid field"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{"status": "404", "title": "Field not found"}]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_available_enum_options_for_work_item(
            test_params['project_id'],
            "WI-001",
            "invalid_field"
        )
        
        assert response.status_code == 404
        print("\n✓ Mock: Invalid field (404) handled correctly")
