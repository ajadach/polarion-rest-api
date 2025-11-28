"""
Pytest tests for delete_all_work_items method.

Tests the delete_all_work_items method from WorkItems class.
Uses mocks to avoid deleting real work items data.

Run with:
    pytest test_delete_all_work_items.py -v
"""
import pytest
from unittest.mock import Mock


# ============================================================================
# Unit Tests - Validation Tests
# ============================================================================

class TestDeleteAllWorkItemsValidation:
    """Unit tests for delete_all_work_items validation
    
    Tests the input validation before API calls are made.
    """
    
    def test_validate_missing_data_key(self, mock_work_items_api):
        """Test validation fails when 'data' key is missing"""
        invalid_data = {
            "items": [{"type": "workitems", "id": "P/W1"}]
        }
        
        with pytest.raises(ValueError, match="must contain a 'data' key"):
            mock_work_items_api.delete_all_work_items(invalid_data)
        print("\n✓ Validation: Missing 'data' key detected")
    
    def test_validate_data_not_list(self, mock_work_items_api):
        """Test validation fails when 'data' is not a list"""
        invalid_data = {
            "data": {
                "type": "workitems",
                "id": "MyProjectId/MyWorkItemId"
            }
        }
        
        with pytest.raises(ValueError, match=r"\['data'\] must be a list \(array\)"):
            mock_work_items_api.delete_all_work_items(invalid_data)
        print("\n✓ Validation: Non-list 'data' detected")
    
    def test_validate_data_string(self, mock_work_items_api):
        """Test validation fails when 'data' is a string"""
        invalid_data = {
            "data": "some string"
        }
        
        with pytest.raises(ValueError, match=r"\['data'\] must be a list \(array\)"):
            mock_work_items_api.delete_all_work_items(invalid_data)
        print("\n✓ Validation: String 'data' detected")
    
    def test_validate_none_body(self, mock_work_items_api):
        """Test validation fails when body is None"""
        with pytest.raises((ValueError, AttributeError)):
            mock_work_items_api.delete_all_work_items(None)
        print("\n✓ Validation: None body detected")
    
    def test_validate_empty_dict(self, mock_work_items_api):
        """Test validation fails when body is empty dict"""
        invalid_data = {}
        
        with pytest.raises(ValueError, match="must contain a 'data' key"):
            mock_work_items_api.delete_all_work_items(invalid_data)
        print("\n✓ Validation: Empty dict detected")
    
    def test_validate_data_empty_list_passes(self, mock_work_items_api):
        """Test validation passes when 'data' is an empty list"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_work_items_api._session.request.return_value = mock_response
        
        valid_data = {
            "data": []
        }
        
        # Should not raise ValueError
        response = mock_work_items_api.delete_all_work_items(valid_data)
        assert response.status_code == 204
        print("\n✓ Validation: Empty list is valid")
    
    def test_validate_correct_structure_passes(self, mock_work_items_api):
        """Test validation passes with correct structure"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_work_items_api._session.request.return_value = mock_response
        
        valid_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/MyWorkItemId"
                }
            ]
        }
        
        # Should not raise ValueError
        response = mock_work_items_api.delete_all_work_items(valid_data)
        assert response.status_code == 204
        print("\n✓ Validation: Correct structure passed")
    
    def test_validate_item_missing_type(self, mock_work_items_api):
        """Test validation fails when item is missing 'type' key"""
        invalid_data = {
            "data": [
                {
                    "id": "MyProjectId/MyWorkItemId"
                }
            ]
        }
        
        with pytest.raises(ValueError, match="must contain a 'type' key"):
            mock_work_items_api.delete_all_work_items(invalid_data)
        print("\n✓ Validation: Missing 'type' in item detected")
    
    def test_validate_item_missing_id(self, mock_work_items_api):
        """Test validation fails when item is missing 'id' key"""
        invalid_data = {
            "data": [
                {
                    "type": "workitems"
                }
            ]
        }
        
        with pytest.raises(ValueError, match="must contain an 'id' key"):
            mock_work_items_api.delete_all_work_items(invalid_data)
        print("\n✓ Validation: Missing 'id' in item detected")
    
    def test_validate_item_not_dict(self, mock_work_items_api):
        """Test validation fails when item in data array is not a dict"""
        invalid_data = {
            "data": [
                "some string"
            ]
        }
        
        with pytest.raises(ValueError, match=r"\['data'\]\[0\] must be a dictionary"):
            mock_work_items_api.delete_all_work_items(invalid_data)
        print("\n✓ Validation: Non-dict item in array detected")


# ============================================================================
# Unit Tests - DELETE Method (with mocks)
# ============================================================================

class TestDeleteAllWorkItemsMocked:
    """Unit tests for delete_all_work_items method using mocks
    
    NOTE: These tests use mocks to avoid deleting real work items data.
    """
    
    def test_delete_all_work_items_success(self, mock_work_items_api):
        """Test successful deletion of work items from global context (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204  # Typical DELETE response
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        # Prepare delete data
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/MyWorkItemId"
                },
                {
                    "type": "workitems",
                    "id": "MyProjectId/MyWorkItemId2"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_all_work_items(
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_work_items_api._session.request.assert_called_once()
        
        # Verify correct endpoint, method and data
        call_args = mock_work_items_api._session.request.call_args
        assert call_args[0][0] == 'DELETE'  # HTTP method
        assert 'all/workitems' in call_args[0][1]  # URL endpoint
        assert call_args[1]['json'] == delete_data
        print("\n✓ Mock: Work items deleted successfully from global context (204 No Content)")
    
    def test_delete_all_work_items_unauthorized(self, mock_work_items_api):
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
        
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/MyWorkItemId"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_all_work_items(
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 401
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '401'
        assert error_data['errors'][0]['title'] == 'Unauthorized'
        print("\n✓ Mock: Unauthorized (401) handled correctly")
    
    def test_delete_all_work_items_not_found(self, mock_work_items_api):
        """Test delete with non-existent work item (404 Not Found) (mocked)"""
        # Setup mock response for error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Work item 'MyProjectId/NonExistentId' not found"
                }
            ]
        }
        mock_work_items_api._session.request.return_value = mock_response
        
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/NonExistentId"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_all_work_items(
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '404'
        assert error_data['errors'][0]['title'] == 'Not Found'
        print("\n✓ Mock: Not Found (404) handled correctly")
    
    def test_delete_all_work_items_forbidden(self, mock_work_items_api):
        """Test delete without sufficient permissions (403 Forbidden) (mocked)"""
        # Setup mock response for error
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "Insufficient permissions to delete work items"
                }
            ]
        }
        mock_work_items_api._session.request.return_value = mock_response
        
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/MyWorkItemId"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_all_work_items(
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 403
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '403'
        assert error_data['errors'][0]['title'] == 'Forbidden'
        print("\n✓ Mock: Forbidden (403) handled correctly")
    
    def test_delete_all_work_items_empty_array(self, mock_work_items_api):
        """Test delete with empty work items array (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        # Empty data array
        delete_data = {
            "data": []
        }
        
        # Execute
        response = mock_work_items_api.delete_all_work_items(
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_work_items_api._session.request.assert_called_once()
        print("\n✓ Mock: Empty array handled successfully")
    
    def test_delete_all_work_items_single_item(self, mock_work_items_api):
        """Test delete with single work item (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        # Single item
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/MyWorkItemId"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_all_work_items(
            work_items_data=delete_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_work_items_api._session.request.assert_called_once()
        
        # Verify the data structure
        call_args = mock_work_items_api._session.request.call_args
        assert len(call_args[1]['json']['data']) == 1
        print("\n✓ Mock: Single work item deleted successfully")
    
    def test_delete_all_work_items_multiple_items(self, mock_work_items_api):
        """Test delete with multiple work items (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        # Multiple items
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/MyWorkItemId1"
                },
                {
                    "type": "workitems",
                    "id": "MyProjectId/MyWorkItemId2"
                },
                {
                    "type": "workitems",
                    "id": "MyProjectId/MyWorkItemId3"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_all_work_items(
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
API Endpoint: DELETE /all/workitems
Description: Deletes a list of Work Items from the Global context

Expected Response Codes:
- 204: No Content (successful deletion)
- 400: Bad Request (invalid data format)
- 401: Unauthorized (invalid or missing token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (work item doesn't exist)
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
