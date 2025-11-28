"""
Pytest tests for delete_work_items_relationship method.

Tests the delete_work_items_relationship method from WorkItems class.
Uses mocks to avoid deleting real work item relationships data.

Run with:
    pytest test_delete_work_items_relationship.py -v
"""
import pytest
from unittest.mock import Mock


# ============================================================================
# Unit Tests - Validation Tests
# ============================================================================

class TestDeleteWorkItemsRelationshipValidation:
    """Unit tests for delete_work_items_relationship validation
    
    Tests the input validation before API calls are made.
    """
    
    def test_validate_missing_data_key(self, mock_work_items_api, test_params):
        """Test validation fails when 'data' key is missing"""
        invalid_data = {
            "items": [{"type": "workitems", "id": "P/W1"}]
        }
        
        with pytest.raises(ValueError, match="must contain a 'data' key"):
            mock_work_items_api.delete_work_items_relationship(
                test_params['project_id'],
                "WorkItemId",
                "parent",
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
            mock_work_items_api.delete_work_items_relationship(
                test_params['project_id'],
                "WorkItemId",
                "parent",
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
                    "id": f"{test_params['project_id']}/RelatedWorkItem"
                }
            ]
        }
        
        # Should not raise ValueError
        response = mock_work_items_api.delete_work_items_relationship(
            test_params['project_id'],
            "WorkItemId",
            "parent",
            valid_data
        )
        assert response.status_code == 204
        print("\n✓ Validation: Correct structure passed")


# ============================================================================
# Unit Tests - DELETE Method (with mocks)
# ============================================================================

class TestDeleteWorkItemsRelationshipMocked:
    """Unit tests for delete_work_items_relationship method using mocks
    
    NOTE: These tests use mocks to avoid deleting real work item relationships data.
    """
    
    def test_delete_work_items_relationship_success(self, mock_work_items_api, test_params):
        """Test successful deletion of work item relationships (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204  # Typical DELETE response
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        # Prepare delete data
        project_id = test_params['project_id']
        work_item_id = "MyWorkItemId"
        relationship_id = "parent"
        
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/RelatedWorkItem1"
                },
                {
                    "type": "workitems",
                    "id": f"{project_id}/RelatedWorkItem2"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items_relationship(
            project_id=project_id,
            work_item_id=work_item_id,
            relationship_id=relationship_id,
            relationships_data=delete_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_work_items_api._session.request.assert_called_once()
        
        # Verify correct endpoint, method and data
        call_args = mock_work_items_api._session.request.call_args
        assert call_args[0][0] == 'DELETE'  # HTTP method
        assert f'projects/{project_id}/workitems/{work_item_id}/relationships/{relationship_id}' in call_args[0][1]
        assert call_args[1]['json'] == delete_data
        print(f"\n✓ Mock: Relationships deleted successfully for work item {work_item_id} (204 No Content)")
    
    def test_delete_work_items_relationship_unauthorized(self, mock_work_items_api, test_params):
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
        work_item_id = "MyWorkItemId"
        relationship_id = "parent"
        
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/RelatedWorkItem"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items_relationship(
            project_id=project_id,
            work_item_id=work_item_id,
            relationship_id=relationship_id,
            relationships_data=delete_data
        )
        
        # Assert
        assert response.status_code == 401
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '401'
        assert error_data['errors'][0]['title'] == 'Unauthorized'
        print("\n✓ Mock: Unauthorized (401) handled correctly")
    
    def test_delete_work_items_relationship_forbidden(self, mock_work_items_api, test_params):
        """Test delete without sufficient permissions (403 Forbidden) (mocked)"""
        # Setup mock response for error
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "Insufficient permissions to delete relationships for this work item"
                }
            ]
        }
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        work_item_id = "MyWorkItemId"
        relationship_id = "parent"
        
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/RelatedWorkItem"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items_relationship(
            project_id=project_id,
            work_item_id=work_item_id,
            relationship_id=relationship_id,
            relationships_data=delete_data
        )
        
        # Assert
        assert response.status_code == 403
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '403'
        assert error_data['errors'][0]['title'] == 'Forbidden'
        print("\n✓ Mock: Forbidden (403) handled correctly")
    
    def test_delete_work_items_relationship_not_found_work_item(self, mock_work_items_api, test_params):
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
        work_item_id = "NonExistentId"
        relationship_id = "parent"
        
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/RelatedWorkItem"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items_relationship(
            project_id=project_id,
            work_item_id=work_item_id,
            relationship_id=relationship_id,
            relationships_data=delete_data
        )
        
        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '404'
        assert error_data['errors'][0]['title'] == 'Not Found'
        print("\n✓ Mock: Work Item Not Found (404) handled correctly")
    
    def test_delete_work_items_relationship_not_found_relationship(self, mock_work_items_api, test_params):
        """Test delete with non-existent relationship (404 Not Found) (mocked)"""
        # Setup mock response for error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Relationship 'invalid_relationship' not found"
                }
            ]
        }
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        work_item_id = "MyWorkItemId"
        relationship_id = "invalid_relationship"
        
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/RelatedWorkItem"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items_relationship(
            project_id=project_id,
            work_item_id=work_item_id,
            relationship_id=relationship_id,
            relationships_data=delete_data
        )
        
        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '404'
        assert error_data['errors'][0]['title'] == 'Not Found'
        print("\n✓ Mock: Relationship Not Found (404) handled correctly")
    
    def test_delete_work_items_relationship_project_not_found(self, mock_work_items_api):
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
        work_item_id = "MyWorkItemId"
        relationship_id = "parent"
        
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/RelatedWorkItem"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items_relationship(
            project_id=project_id,
            work_item_id=work_item_id,
            relationship_id=relationship_id,
            relationships_data=delete_data
        )
        
        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '404'
        assert error_data['errors'][0]['title'] == 'Not Found'
        print("\n✓ Mock: Project Not Found (404) handled correctly")
    
    def test_delete_work_items_relationship_empty_array(self, mock_work_items_api, test_params):
        """Test delete with empty relationships array (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        work_item_id = "MyWorkItemId"
        relationship_id = "parent"
        
        # Empty data array
        delete_data = {
            "data": []
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items_relationship(
            project_id=project_id,
            work_item_id=work_item_id,
            relationship_id=relationship_id,
            relationships_data=delete_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_work_items_api._session.request.assert_called_once()
        print("\n✓ Mock: Empty array handled successfully")
    
    def test_delete_work_items_relationship_single_item(self, mock_work_items_api, test_params):
        """Test delete with single relationship (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        work_item_id = "MyWorkItemId"
        relationship_id = "parent"
        
        # Single item
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/RelatedWorkItem"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items_relationship(
            project_id=project_id,
            work_item_id=work_item_id,
            relationship_id=relationship_id,
            relationships_data=delete_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_work_items_api._session.request.assert_called_once()
        
        # Verify the data structure
        call_args = mock_work_items_api._session.request.call_args
        assert len(call_args[1]['json']['data']) == 1
        print("\n✓ Mock: Single relationship deleted successfully")
    
    def test_delete_work_items_relationship_multiple_items(self, mock_work_items_api, test_params):
        """Test delete with multiple relationships (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        work_item_id = "MyWorkItemId"
        relationship_id = "parent"
        
        # Multiple items
        delete_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{project_id}/RelatedWorkItem1"
                },
                {
                    "type": "workitems",
                    "id": f"{project_id}/RelatedWorkItem2"
                },
                {
                    "type": "workitems",
                    "id": f"{project_id}/RelatedWorkItem3"
                }
            ]
        }
        
        # Execute
        response = mock_work_items_api.delete_work_items_relationship(
            project_id=project_id,
            work_item_id=work_item_id,
            relationship_id=relationship_id,
            relationships_data=delete_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_work_items_api._session.request.assert_called_once()
        
        # Verify the data structure
        call_args = mock_work_items_api._session.request.call_args
        assert len(call_args[1]['json']['data']) == 3
        print("\n✓ Mock: Multiple relationships deleted successfully")
    
    def test_delete_work_items_relationship_different_types(self, mock_work_items_api, test_params):
        """Test delete with different relationship types (parent, child, etc.) (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_work_items_api._session.request.return_value = mock_response
        
        project_id = test_params['project_id']
        work_item_id = "MyWorkItemId"
        
        # Test different relationship types
        relationship_types = ["parent", "child", "relates_to", "duplicates", "blocks"]
        
        for rel_type in relationship_types:
            delete_data = {
                "data": [
                    {
                        "type": "workitems",
                        "id": f"{project_id}/RelatedWorkItem"
                    }
                ]
            }
            
            # Execute
            response = mock_work_items_api.delete_work_items_relationship(
                project_id=project_id,
                work_item_id=work_item_id,
                relationship_id=rel_type,
                relationships_data=delete_data
            )
            
            # Assert
            assert response.status_code == 204
            
            # Verify correct endpoint
            call_args = mock_work_items_api._session.request.call_args
            assert f'relationships/{rel_type}' in call_args[0][1]
        
        print(f"\n✓ Mock: Different relationship types handled successfully")


# ============================================================================
# Notes
# ============================================================================
"""
API Endpoint: DELETE /projects/{projectId}/workitems/{workItemId}/relationships/{relationshipId}
Description: Deletes a list of Work Item Relationships

Expected Response Codes:
- 204: No Content (successful deletion)
- 400: Bad Request (invalid data format)
- 401: Unauthorized (invalid or missing token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (work item, project, or relationship doesn't exist)
- 500: Internal Server Error

Request Body Example:
{
    "data": [
        {
            "type": "workitems",
            "id": "MyProjectId/RelatedWorkItemId"
        }
    ]
}

Relationship Types:
- parent: Parent relationship
- child: Child relationship (inverse of parent)
- relates_to: General relationship
- duplicates: Duplicate relationship
- blocks: Blocking relationship
- depends_on: Dependency relationship

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
