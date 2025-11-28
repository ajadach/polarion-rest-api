"""
Pytest tests for get_work_item_test_parameter_definition method.

Run with:
    pytest test_get_work_item_test_parameter_definition.py -v
"""
import pytest
from unittest.mock import Mock


class TestGetWorkItemTestParameterDefinitionMocked:
    """Unit tests for get_work_item_test_parameter_definition method"""
    
    def test_get_test_parameter_definition_success(self, mock_work_items_api, test_params):
        """Test successful retrieval of a single test parameter definition"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameterdefinitions",
                "id": "param1",
                "attributes": {
                    "name": "TestParam1",
                    "dataType": "string"
                }
            }
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item_test_parameter_definition(
            test_params['project_id'],
            "WI-001",
            "param1"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['data']['type'] == 'testparameterdefinitions'
        print("\n✓ Mock: Test parameter definition retrieved successfully")
    
    def test_get_test_parameter_definition_with_fields(self, mock_work_items_api, test_params):
        """Test get test parameter definition with fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item_test_parameter_definition(
            test_params['project_id'],
            "WI-001",
            "param1",
            fields={'testparameterdefinitions': 'id,name'}
        )
        
        assert response.status_code == 200
        print("\n✓ Mock: Fields parameter handled correctly")
    
    def test_get_test_parameter_definition_with_include(self, mock_work_items_api, test_params):
        """Test get test parameter definition with include"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item_test_parameter_definition(
            test_params['project_id'],
            "WI-001",
            "param1",
            include="workitem"
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['include'] == "workitem"
        print("\n✓ Mock: Include parameter handled correctly")
    
    def test_get_test_parameter_definition_not_found(self, mock_work_items_api, test_params):
        """Test get test parameter definition that doesn't exist"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{"status": "404", "title": "Not Found"}]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_item_test_parameter_definition(
            test_params['project_id'],
            "WI-001",
            "NonExistentParam"
        )
        
        assert response.status_code == 404
        print("\n✓ Mock: Not found (404) handled correctly")
