"""
Pytest tests for get_available_enum_options_for_work_item_type method.

Run with:
    pytest test_get_available_enum_options_for_work_item_type.py -v
"""
import pytest
from unittest.mock import Mock


class TestGetAvailableEnumOptionsForWorkItemTypeMocked:
    """Unit tests for get_available_enum_options_for_work_item_type method"""
    
    def test_get_available_enum_options_for_type_success(self, mock_work_items_api, test_params):
        """Test successful retrieval of available enum options for work item type"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "enums", "id": "low"},
                {"type": "enums", "id": "medium"},
                {"type": "enums", "id": "high"}
            ]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_available_enum_options_for_work_item_type(
            test_params['project_id'],
            "priority",
            work_item_type="task"
        )
        
        assert response.status_code == 200
        assert len(response.json()['data']) == 3
        print("\n✓ Mock: Available enum options for type retrieved successfully")
    
    def test_get_available_enum_options_for_type_with_pagination(self, mock_work_items_api, test_params):
        """Test get available enum options with pagination"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_available_enum_options_for_work_item_type(
            test_params['project_id'],
            "status",
            work_item_type="bug",
            page_size=10,
            page_number=1
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['type'] == "bug"
        assert params['page[size]'] == 10
        print("\n✓ Mock: Pagination and type parameter handled correctly")
    
    def test_get_available_enum_options_for_type_without_type_param(self, mock_work_items_api, test_params):
        """Test get available enum options without specifying work item type"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_available_enum_options_for_work_item_type(
            test_params['project_id'],
            "priority"
        )
        
        assert response.status_code == 200
        print("\n✓ Mock: Options retrieved without type parameter")
