"""
Pytest tests for patch_all_work_items method.

Tests the patch_all_work_items method from WorkItems class.
Uses mocks to avoid making real API calls.

Run with:
    pytest test_patch_all_work_items.py -v
"""
import pytest
from unittest.mock import Mock


class TestPatchAllWorkItemsMocked:
    """Unit tests for patch_all_work_items method using mocks"""
    
    def test_patch_all_work_items_success(self, mock_work_items_api):
        """Test successful update of all work items"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "workitems",
                    "id": "Project1/WI-001",
                    "attributes": {
                        "title": "Updated Work Item",
                        "status": "in_progress"
                    }
                }
            ]
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_items_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "Project1/WI-001",
                    "attributes": {
                        "title": "Updated Work Item"
                    }
                }
            ]
        }
        
        response = mock_work_items_api.patch_all_work_items(work_items_data)
        
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert data['data'][0]['attributes']['title'] == 'Updated Work Item'
        mock_work_items_api._session.patch.assert_called_once()
        print("\n✓ Mock: All work items updated successfully")
    
    def test_patch_all_work_items_with_workflow_action(self, mock_work_items_api):
        """Test patch all work items with workflow action"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_items_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "Project1/WI-001",
                    "attributes": {}
                }
            ]
        }
        
        response = mock_work_items_api.patch_all_work_items(
            work_items_data,
            workflow_action="approve"
        )
        
        assert response.status_code == 200
        call_args = mock_work_items_api._session.patch.call_args
        assert 'params' in call_args[1]
        assert call_args[1]['params']['workflowAction'] == 'approve'
        print("\n✓ Mock: Workflow action parameter handled correctly")
    
    def test_patch_all_work_items_with_change_type_to(self, mock_work_items_api):
        """Test patch all work items with change type to"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_items_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "Project1/WI-001",
                    "attributes": {}
                }
            ]
        }
        
        response = mock_work_items_api.patch_all_work_items(
            work_items_data,
            change_type_to="task"
        )
        
        assert response.status_code == 200
        call_args = mock_work_items_api._session.patch.call_args
        assert call_args[1]['params']['changeTypeTo'] == 'task'
        print("\n✓ Mock: Change type parameter handled correctly")
    
    def test_patch_all_work_items_with_all_parameters(self, mock_work_items_api):
        """Test patch all work items with all optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_items_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "Project1/WI-001",
                    "attributes": {
                        "title": "Updated Title"
                    }
                }
            ]
        }
        
        response = mock_work_items_api.patch_all_work_items(
            work_items_data,
            workflow_action="approve",
            change_type_to="task"
        )
        
        assert response.status_code == 200
        call_args = mock_work_items_api._session.patch.call_args
        assert call_args[1]['params']['workflowAction'] == 'approve'
        assert call_args[1]['params']['changeTypeTo'] == 'task'
        print("\n✓ Mock: All parameters handled correctly")
    
    def test_patch_all_work_items_multiple_items(self, mock_work_items_api):
        """Test patch multiple work items at once"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "workitems", "id": "Project1/WI-001"},
                {"type": "workitems", "id": "Project1/WI-002"}
            ]
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        work_items_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "Project1/WI-001",
                    "attributes": {"status": "closed"}
                },
                {
                    "type": "workitems",
                    "id": "Project1/WI-002",
                    "attributes": {"status": "closed"}
                }
            ]
        }
        
        response = mock_work_items_api.patch_all_work_items(work_items_data)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data['data']) == 2
        print("\n✓ Mock: Multiple work items updated successfully")
    
    def test_patch_all_work_items_unauthorized(self, mock_work_items_api):
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
        
        work_items_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "Project1/WI-001",
                    "attributes": {}
                }
            ]
        }
        
        response = mock_work_items_api.patch_all_work_items(work_items_data)
        
        assert response.status_code == 401
        errors = response.json()['errors']
        assert errors[0]['title'] == 'Unauthorized'
        print("\n✓ Mock: Unauthorized error handled correctly")
    
    def test_patch_all_work_items_not_found(self, mock_work_items_api):
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
        
        work_items_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "Project1/NONEXISTENT",
                    "attributes": {}
                }
            ]
        }
        
        response = mock_work_items_api.patch_all_work_items(work_items_data)
        
        assert response.status_code == 404
        errors = response.json()['errors']
        assert errors[0]['title'] == 'Not Found'
        print("\n✓ Mock: Not found error handled correctly")
    
    def test_patch_all_work_items_validation_error(self, mock_work_items_api):
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
        
        work_items_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "Project1/WI-001"
                    # Missing required fields
                }
            ]
        }
        
        response = mock_work_items_api.patch_all_work_items(work_items_data)
        
        assert response.status_code == 400
        errors = response.json()['errors']
        assert errors[0]['title'] == 'Bad Request'
        print("\n✓ Mock: Validation error handled correctly")
