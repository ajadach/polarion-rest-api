"""
Pytest tests for get_work_item_test_parameter_definitions method.

Run with:
    pytest test_get_work_item_test_parameter_definitions.py -v
"""
import pytest
from unittest.mock import Mock


class TestGetWorkItemTestParameterDefinitionsMocked:
    """Unit tests for get_work_item_test_parameter_definitions method"""
    
    def test_get_test_parameter_definitions_success(self, mock_work_items_api, test_params):
        """Test successful retrieval of test parameter definitions"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "testparameterdefinitions", "id": "param1"},
                {"type": "testparameterdefinitions", "id": "param2"}
            ]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item_test_parameter_definitions(
            test_params['project_id'],
            "WI-001"
        )
        
        assert response.status_code == 200
        assert len(response.json()['data']) == 2
        print("\n✓ Mock: Test parameter definitions retrieved successfully")
    
    def test_get_test_parameter_definitions_with_pagination(self, mock_work_items_api, test_params):
        """Test get test parameter definitions with pagination"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item_test_parameter_definitions(
            test_params['project_id'],
            "WI-001",
            page_size=10,
            page_number=1
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['page[size]'] == 10
        print("\n✓ Mock: Pagination handled correctly")
    
    def test_get_test_parameter_definitions_with_fields(self, mock_work_items_api, test_params):
        """Test get test parameter definitions with fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item_test_parameter_definitions(
            test_params['project_id'],
            "WI-001",
            fields={'testparameterdefinitions': 'id,name'}
        )
        
        assert response.status_code == 200
        print("\n✓ Mock: Fields parameter handled correctly")
    
    def test_get_test_parameter_definitions_not_found(self, mock_work_items_api, test_params):
        """Test get test parameter definitions for non-existent work item"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{"status": "404", "title": "Not Found"}]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item_test_parameter_definitions(
            test_params['project_id'],
            "NonExistent"
        )
        
        assert response.status_code == 404
        print("\n✓ Mock: Not found (404) handled correctly")
