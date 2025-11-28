"""
Pytest tests for patch_work_item method.

Tests the patch_work_item method from WorkItems class.
Uses mocks to avoid making real API calls.

Run with:
    pytest test_patch_work_item.py -v
"""
import pytest
from unittest.mock import Mock


class TestPatchWorkItemMocked:
    """Unit tests for patch_work_item method using mocks"""
    
    def test_patch_work_item_success(self, mock_work_items_api, test_params):
        """Test successful update of a single work item"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/WI-001",
                "attributes": {
                    "title": "Updated Work Item",
                    "status": "in_progress",
                    "description": {"type": "text/plain", "value": "Updated description"}
                }
            }
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_item_data = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/WI-001",
                "attributes": {
                    "title": "Updated Work Item",
                    "description": {"type": "text/plain", "value": "Updated description"}
                }
            }
        }
        
        response = mock_work_items_api.patch_work_item(
            test_params['project_id'],
            "WI-001",
            work_item_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['data']['type'] == 'workitems'
        assert data['data']['attributes']['title'] == 'Updated Work Item'
        mock_work_items_api._session.patch.assert_called_once()
        print("\n✓ Mock: Single work item updated successfully")
    
    def test_patch_work_item_with_workflow_action(self, mock_work_items_api, test_params):
        """Test patch work item with workflow action"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_item_data = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/WI-001",
                "attributes": {}
            }
        }
        
        response = mock_work_items_api.patch_work_item(
            test_params['project_id'],
            "WI-001",
            work_item_data,
            workflow_action="approve"
        )
        
        assert response.status_code == 200
        call_args = mock_work_items_api._session.patch.call_args
        assert 'params' in call_args[1]
        assert call_args[1]['params']['workflowAction'] == 'approve'
        print("\n✓ Mock: Workflow action parameter handled correctly")
    
    def test_patch_work_item_with_change_type_to(self, mock_work_items_api, test_params):
        """Test patch work item with change type to"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_item_data = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/WI-001",
                "attributes": {}
            }
        }
        
        response = mock_work_items_api.patch_work_item(
            test_params['project_id'],
            "WI-001",
            work_item_data,
            change_type_to="task"
        )
        
        assert response.status_code == 200
        call_args = mock_work_items_api._session.patch.call_args
        assert call_args[1]['params']['changeTypeTo'] == 'task'
        print("\n✓ Mock: Change type parameter handled correctly")
    
    def test_patch_work_item_with_all_parameters(self, mock_work_items_api, test_params):
        """Test patch work item with all optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_item_data = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/WI-001",
                "attributes": {
                    "title": "Updated Title"
                }
            }
        }
        
        response = mock_work_items_api.patch_work_item(
            test_params['project_id'],
            "WI-001",
            work_item_data,
            workflow_action="approve",
            change_type_to="task"
        )
        
        assert response.status_code == 200
        call_args = mock_work_items_api._session.patch.call_args
        assert call_args[1]['params']['workflowAction'] == 'approve'
        assert call_args[1]['params']['changeTypeTo'] == 'task'
        print("\n✓ Mock: All parameters handled correctly")
    
    def test_patch_work_item_status_change(self, mock_work_items_api, test_params):
        """Test patch work item to change status"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/WI-001",
                "attributes": {
                    "status": "closed"
                }
            }
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_item_data = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/WI-001",
                "attributes": {
                    "status": "closed"
                }
            }
        }
        
        response = mock_work_items_api.patch_work_item(
            test_params['project_id'],
            "WI-001",
            work_item_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['data']['attributes']['status'] == 'closed'
        print("\n✓ Mock: Work item status changed successfully")
    
    def test_patch_work_item_not_found(self, mock_work_items_api, test_params):
        """Test patch with non-existent work item (404 Not Found)"""
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
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_item_data = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/NONEXISTENT",
                "attributes": {}
            }
        }
        
        response = mock_work_items_api.patch_work_item(
            test_params['project_id'],
            "NONEXISTENT",
            work_item_data
        )
        
        assert response.status_code == 404
        errors = response.json()['errors']
        assert errors[0]['title'] == 'Not Found'
        print("\n✓ Mock: Not found error handled correctly")
    
    def test_patch_work_item_unauthorized(self, mock_work_items_api, test_params):
        """Test patch with invalid authentication (401 Unauthorized)"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "Invalid or missing authentication token"
                }
            ]
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_item_data = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/WI-001",
                "attributes": {}
            }
        }
        
        response = mock_work_items_api.patch_work_item(
            test_params['project_id'],
            "WI-001",
            work_item_data
        )
        
        assert response.status_code == 401
        errors = response.json()['errors']
        assert errors[0]['title'] == 'Unauthorized'
        print("\n✓ Mock: Unauthorized error handled correctly")
    
    def test_patch_work_item_validation_error(self, mock_work_items_api, test_params):
        """Test patch with invalid data (400 Bad Request)"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Invalid request body"
                }
            ]
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_item_data = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/WI-001"
                # Missing required fields
            }
        }
        
        response = mock_work_items_api.patch_work_item(
            test_params['project_id'],
            "WI-001",
            work_item_data
        )
        
        assert response.status_code == 400
        errors = response.json()['errors']
        assert errors[0]['title'] == 'Bad Request'
        print("\n✓ Mock: Validation error handled correctly")
    
    def test_patch_work_item_forbidden(self, mock_work_items_api, test_params):
        """Test patch with insufficient permissions (403 Forbidden)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "Insufficient permissions to update work item"
                }
            ]
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_item_data = {
            "data": {
                "type": "workitems",
                "id": f"{test_params['project_id']}/WI-001",
                "attributes": {}
            }
        }
        
        response = mock_work_items_api.patch_work_item(
            test_params['project_id'],
            "WI-001",
            work_item_data
        )
        
        assert response.status_code == 403
        errors = response.json()['errors']
        assert errors[0]['title'] == 'Forbidden'
        print("\n✓ Mock: Forbidden error handled correctly")
