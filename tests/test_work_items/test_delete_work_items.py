"""
Pytest tests for delete_work_items method.

Tests the delete_work_items method from WorkItems class.
Uses mocks to avoid deleting real work items data.

Run with:
    pytest test_delete_work_items.py -v
"""
import pytest
from unittest.mock import Mock


# ============================================================================
# Unit Tests - Validation Tests
# ============================================================================

class TestDeleteWorkItemsValidation:
    """Unit tests for delete_work_items validation
    
    Tests the input validation before API calls are made.
    """
    
    def test_validate_missing_data_key(self, mock_work_items_api, test_params):
        """Test validation fails when 'data' key is missing"""
        invalid_data = {
            "items": [{"type": "workitems", "id": "P/W1"}]
        }
        
        with pytest.raises(ValueError, match="must contain a 'data' key"):
            mock_work_items_api.delete_work_items(
                test_params['project_id'], 
                invalid_data
            )
        print("\n✓ Validation: Missing 'data' key detected")
    
    def test_validate_data_not_list(self, mock_work_items_api, test_params):
        """Test validation fails when 'data' is not a list"""
        invalid_data = {
            "data": {
                "type": "workitems",
                "id": "P/W1"
            }
        }
        
        with pytest.raises(ValueError, match=r"\['data'\] must be a list \(array\)"):
            mock_work_items_api.delete_work_items(
                test_params['project_id'],
                invalid_data
            )
        print("\n✓ Validation: Non-list 'data' detected")
    
    def test_validate_correct_structure_passes(self, mock_work_items_api, test_params):
        """Test validation passes with correct structure"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_work_items_api._session.request.return_value = mock_response
        
        valid_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/MyWorkItemId"
                }
            ]
        }
        
        # Should not raise ValueError
        response = mock_work_items_api.delete_work_items(
            test_params['project_id'],
            valid_data
        )
        assert response.status_code == 204
        print("\n✓ Validation: Correct structure passed")


# ============================================================================
# Unit Tests - DELETE Method (with mocks)
# ============================================================================

class TestDeleteWorkItemsMocked:
    """Unit tests for delete_work_items method using mocks
    
    NOTE: These tests use mocks to avoid deleting real work items data.
    """
    
    def test_delete_work_items_success(self, mock_work_items_api, test_params):
        """Test successful deletion of work items from a project (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204  # Typical DELETE response
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        # Prepare delete data
        project_id = test_params['project_id']
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/MyWorkItemId"
                },
                {
                    "type": "workitems",
                    "id": f"{project_id}/MyWorkItemId2"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items(
            project_id=project_id,
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_work_items_api._session.request.assert_called_once()
        
        # Verify correct endpoint, method and data
        call_args = mock_work_items_api._session.request.call_args
        assert call_args[0][0] == 'DELETE'  # HTTP method
        assert f'projects/{project_id}/workitems' in call_args[0][1]  # URL endpoint
        assert call_args[1]['json'] == delete_data
        print(f"\n✓ Mock: Work items deleted successfully from project {project_id} (204 No Content)")
    
    def test_delete_work_items_unauthorized(self, mock_work_items_api, test_params):
        """Test delete with invalid authentication (401 Unauthorized) (mocked)"""
        # Setup mock response for error
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
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/MyWorkItemId"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items(
            project_id=project_id,
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 401
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '401'
        assert error_data['errors'][0]['title'] == 'Unauthorized'
        print("\n✓ Mock: Unauthorized (401) handled correctly")
    
    def test_delete_work_items_forbidden(self, mock_work_items_api, test_params):
        """Test delete without sufficient permissions (403 Forbidden) (mocked)"""
        # Setup mock response for error
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "Insufficient permissions to delete work items in this project"
                }
            ]
        }
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/MyWorkItemId"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items(
            project_id=project_id,
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 403
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '403'
        assert error_data['errors'][0]['title'] == 'Forbidden'
        print("\n✓ Mock: Forbidden (403) handled correctly")
    
    def test_delete_work_items_not_found(self, mock_work_items_api, test_params):
        """Test delete with non-existent work item (404 Not Found) (mocked)"""
        # Setup mock response for error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Work item 'OT/NonExistentId' not found"
                }
            ]
        }
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/NonExistentId"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items(
            project_id=project_id,
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '404'
        assert error_data['errors'][0]['title'] == 'Not Found'
        print("\n✓ Mock: Not Found (404) handled correctly")
    
    def test_delete_work_items_project_not_found(self, mock_work_items_api):
        """Test delete with non-existent project (404 Not Found) (mocked)"""
        # Setup mock response for error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Project 'NonExistentProject' not found"
                }
            ]
        }
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = "NonExistentProject"
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/MyWorkItemId"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items(
            project_id=project_id,
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '404'
        assert error_data['errors'][0]['title'] == 'Not Found'
        print("\n✓ Mock: Project Not Found (404) handled correctly")
    
    def test_delete_work_items_empty_array(self, mock_work_items_api, test_params):
        """Test delete with empty work items array (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        # Empty data array
        delete_data = {
            "data": []
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items(
            project_id=project_id,
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_work_items_api._session.request.assert_called_once()
        print("\n✓ Mock: Empty array handled successfully")
    
    def test_delete_work_items_single_item(self, mock_work_items_api, test_params):
        """Test delete with single work item (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        # Single item
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/MyWorkItemId"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items(
            project_id=project_id,
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_work_items_api._session.request.assert_called_once()
        
        # Verify the data structure
        call_args = mock_work_items_api._session.request.call_args
        assert len(call_args[1]['json']['data']) == 1
        print("\n✓ Mock: Single work item deleted successfully")
    
    def test_delete_work_items_multiple_items(self, mock_work_items_api, test_params):
        """Test delete with multiple work items (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        # Multiple items
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/MyWorkItemId1"
                },
                {
                    "type": "workitems",
                    "id": f"{project_id}/MyWorkItemId2"
                },
                {
                    "type": "workitems",
                    "id": f"{project_id}/MyWorkItemId3"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items(
            project_id=project_id,
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_work_items_api._session.request.assert_called_once()
        
        # Verify the data structure
        call_args = mock_work_items_api._session.request.call_args
        assert len(call_args[1]['json']['data']) == 3
        print("\n✓ Mock: Multiple work items deleted successfully")


# ============================================================================
# Notes
# ============================================================================
"""
API Endpoint: DELETE /projects/{projectId}/workitems
Description: Deletes a list of Work Items from a project

Expected Response Codes:
- 204: No Content (successful deletion)
- 400: Bad Request (invalid data format)
- 401: Unauthorized (invalid or missing token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (work item or project doesn't exist)
- 500: Internal Server Error

Request Body Example:
{
    "data": [
        {
            "type": "workitems",
            "id": "MyProjectId/MyWorkItemId"
        }
    ]
}

Error Response Example (400):
{
    "errors": [
        {
            "status": "400",
            "title": "Bad Request",
            "detail": "Unexpected token, BEGIN_ARRAY expected, but was : BEGIN_OBJECT (at $.data)",
            "source": {
                "pointer": "$.data",
                "parameter": "revision",
                "resource": {
                    "id": "MyProjectId/id",
                    "type": "type"
                }
            }
        }
    ]
}
"""
