"""
Pytest tests for get_workflow_actions_for_work_item method.

Run with:
    pytest test_get_workflow_actions_for_work_item.py -v
"""
import pytest
from unittest.mock import Mock


class TestGetWorkflowActionsForWorkItemMocked:
    """Unit tests for get_workflow_actions_for_work_item method"""
    
    def test_get_workflow_actions_success(self, mock_work_items_api, test_params):
        """Test successful retrieval of workflow actions"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "workflow_actions", "id": "resolve"},
                {"type": "workflow_actions", "id": "close"},
                {"type": "workflow_actions", "id": "reopen"}
            ]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_workflow_actions_for_work_item(
            test_params['project_id'],
            "WI-001"
        )
        
        assert response.status_code == 200
        assert len(response.json()['data']) == 3
        print("\n✓ Mock: Workflow actions retrieved successfully")
    
    def test_get_workflow_actions_with_pagination(self, mock_work_items_api, test_params):
        """Test get workflow actions with pagination"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_workflow_actions_for_work_item(
            test_params['project_id'],
            "WI-001",
            page_size=5,
            page_number=1
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['page[size]'] == 5
        print("\n✓ Mock: Pagination handled correctly")
    
    def test_get_workflow_actions_not_found(self, mock_work_items_api, test_params):
        """Test get workflow actions for non-existent work item"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{"status": "404", "title": "Not Found"}]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_workflow_actions_for_work_item(
            test_params['project_id'],
            "NonExistent"
        )
        
        assert response.status_code == 404
        print("\n✓ Mock: Not found (404) handled correctly")
