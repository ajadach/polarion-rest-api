"""
Pytest tests for delete_linked_work_item method in LinkedWorkItems class.

Tests the DELETE /projects/{projectId}/workitems/{workItemId}/linkedworkitems/{roleId}/{targetProjectId}/{linkedWorkItemId} endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_delete_linked_work_item.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.delete
class TestDeleteLinkedWorkItem:
    """Unit tests for delete_linked_work_item method using mocks"""
    
    def test_delete_linked_work_item_success_204(self, mock_linked_work_items_api):
        """Test successful deletion with 204 status code (mocked)"""
        # Setup mock response (DELETE typically returns 204 No Content)
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with path parameters matching CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        role_id = "parent"
        target_project_id = "MyProjectId"
        linked_work_item_id = "MyLinkedWorkItemId"
        
        response = mock_linked_work_items_api.delete_linked_work_item(
            project_id=project_id,
            work_item_id=work_item_id,
            role_id=role_id,
            target_project_id=target_project_id,
            linked_work_item_id=linked_work_item_id
        )
        
        # Assert
        assert response.status_code == 204
        
        # Verify correct endpoint was called
        call_args = mock_linked_work_items_api._session.delete.call_args
        expected_url = f'https://test.polarion.com/polarion/rest/v1/projects/{project_id}/workitems/{work_item_id}/linkedworkitems/{role_id}/{target_project_id}/{linked_work_item_id}'
        assert call_args[0][0] == expected_url
        print("\n✓ Mock: Linked work item deleted successfully with 204 status code")
    
    def test_delete_linked_work_item_unauthorized_401(self, mock_linked_work_items_api):
        """Test unauthorized access with 401 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 401 status code
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "No access token"
                }
            ]
        }
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        role_id = "parent"
        target_project_id = "MyProjectId"
        linked_work_item_id = "MyLinkedWorkItemId"
        
        response = mock_linked_work_items_api.delete_linked_work_item(
            project_id=project_id,
            work_item_id=work_item_id,
            role_id=role_id,
            target_project_id=target_project_id,
            linked_work_item_id=linked_work_item_id
        )
        
        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_delete_linked_work_item_bad_request_400(self, mock_linked_work_items_api):
        """Test bad request with 400 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 400 status code
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
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
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with potentially invalid parameters
        project_id = "InvalidProject"
        work_item_id = "InvalidWorkItem"
        role_id = "invalid_role"
        target_project_id = "InvalidTargetProject"
        linked_work_item_id = "InvalidLinkedWorkItem"
        
        response = mock_linked_work_items_api.delete_linked_work_item(
            project_id=project_id,
            work_item_id=work_item_id,
            role_id=role_id,
            target_project_id=target_project_id,
            linked_work_item_id=linked_work_item_id
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '400'
        assert response_data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in response_data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code with error details")
    
    def test_delete_linked_work_item_not_found_404(self, mock_linked_work_items_api):
        """Test resource not found with 404 status code (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "The linked work item was not found"
                }
            ]
        }
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        role_id = "parent"
        target_project_id = "MyProjectId"
        linked_work_item_id = "NonExistentWorkItem"
        
        response = mock_linked_work_items_api.delete_linked_work_item(
            project_id=project_id,
            work_item_id=work_item_id,
            role_id=role_id,
            target_project_id=target_project_id,
            linked_work_item_id=linked_work_item_id
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '404'
        print("\n✓ Mock: Not found returns 404 status code")
    
    def test_delete_linked_work_item_forbidden_403(self, mock_linked_work_items_api):
        """Test forbidden access with 403 status code (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You don't have permission to delete this linked work item"
                }
            ]
        }
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "RestrictedProject"
        work_item_id = "RestrictedWorkItem"
        role_id = "parent"
        target_project_id = "RestrictedProject"
        linked_work_item_id = "RestrictedLinkedWorkItem"
        
        response = mock_linked_work_items_api.delete_linked_work_item(
            project_id=project_id,
            work_item_id=work_item_id,
            role_id=role_id,
            target_project_id=target_project_id,
            linked_work_item_id=linked_work_item_id
        )
        
        # Assert
        assert response.status_code == 403
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '403'
        print("\n✓ Mock: Forbidden access returns 403 status code")
    
    def test_delete_linked_work_item_internal_error_500(self, mock_linked_work_items_api):
        """Test internal server error with 500 status code (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "500",
                    "title": "Internal Server Error",
                    "detail": "An unexpected error occurred while processing the request"
                }
            ]
        }
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        role_id = "parent"
        target_project_id = "MyProjectId"
        linked_work_item_id = "MyLinkedWorkItemId"
        
        response = mock_linked_work_items_api.delete_linked_work_item(
            project_id=project_id,
            work_item_id=work_item_id,
            role_id=role_id,
            target_project_id=target_project_id,
            linked_work_item_id=linked_work_item_id
        )
        
        # Assert
        assert response.status_code == 500
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '500'
        print("\n✓ Mock: Internal server error returns 500 status code")
    
    def test_delete_linked_work_item_endpoint_structure(self, mock_linked_work_items_api):
        """Test that the correct endpoint structure is used (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with specific parameters
        project_id = "TEST_PROJ"
        work_item_id = "WI-123"
        role_id = "relates_to"
        target_project_id = "TARGET_PROJ"
        linked_work_item_id = "WI-456"
        
        response = mock_linked_work_items_api.delete_linked_work_item(
            project_id=project_id,
            work_item_id=work_item_id,
            role_id=role_id,
            target_project_id=target_project_id,
            linked_work_item_id=linked_work_item_id
        )
        
        # Verify the endpoint structure
        call_args = mock_linked_work_items_api._session.delete.call_args
        called_url = call_args[0][0]
        
        # Check that all parameters are in the correct order
        assert f'projects/{project_id}' in called_url
        assert f'workitems/{work_item_id}' in called_url
        assert f'linkedworkitems/{role_id}' in called_url
        assert f'{role_id}/{target_project_id}' in called_url
        assert f'{target_project_id}/{linked_work_item_id}' in called_url
        
        # Verify complete URL structure
        expected_path = f'projects/{project_id}/workitems/{work_item_id}/linkedworkitems/{role_id}/{target_project_id}/{linked_work_item_id}'
        assert expected_path in called_url
        print("\n✓ Mock: Endpoint structure is correct with all path parameters")
    
    def test_delete_linked_work_item_parameter_types(self, mock_linked_work_items_api):
        """Test that method accepts correct parameter types (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Test with string parameters (correct type)
        response = mock_linked_work_items_api.delete_linked_work_item(
            project_id="PROJ1",
            work_item_id="WI1",
            role_id="parent",
            target_project_id="PROJ2",
            linked_work_item_id="WI2"
        )
        
        assert response.status_code == 204
        assert mock_linked_work_items_api._session.delete.called
        print("\n✓ Mock: Method accepts string parameters correctly")
    
    def test_delete_linked_work_item_different_role_types(self, mock_linked_work_items_api):
        """Test deletion with different role types (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Test different role types
        test_roles = [
            "parent",
            "child",
            "relates_to",
            "duplicates",
            "depends_on"
        ]
        
        for role_id in test_roles:
            response = mock_linked_work_items_api.delete_linked_work_item(
                project_id="MyProjectId",
                work_item_id="MyWorkItemId",
                role_id=role_id,
                target_project_id="MyProjectId",
                linked_work_item_id="MyLinkedWorkItemId"
            )
            
            assert response.status_code == 204
            
            # Verify role is in the URL
            call_args = mock_linked_work_items_api._session.delete.call_args
            called_url = call_args[0][0]
            assert f'linkedworkitems/{role_id}/' in called_url
        
        print(f"\n✓ Mock: Tested {len(test_roles)} different role types successfully")
    
    def test_delete_linked_work_item_cross_project(self, mock_linked_work_items_api):
        """Test deletion of cross-project linked work items (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with different project IDs (cross-project link)
        source_project = "ProjectA"
        target_project = "ProjectB"
        
        response = mock_linked_work_items_api.delete_linked_work_item(
            project_id=source_project,
            work_item_id="WI-A-001",
            role_id="relates_to",
            target_project_id=target_project,
            linked_work_item_id="WI-B-001"
        )
        
        # Assert
        assert response.status_code == 204
        
        # Verify both project IDs are in the URL
        call_args = mock_linked_work_items_api._session.delete.call_args
        called_url = call_args[0][0]
        assert f'projects/{source_project}' in called_url
        assert f'/{target_project}/' in called_url
        print("\n✓ Mock: Cross-project linked work item deletion works correctly")
    
    def test_delete_linked_work_item_same_project(self, mock_linked_work_items_api):
        """Test deletion of same-project linked work items (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with same project ID (internal link)
        project_id = "MyProject"
        
        response = mock_linked_work_items_api.delete_linked_work_item(
            project_id=project_id,
            work_item_id="WI-001",
            role_id="parent",
            target_project_id=project_id,
            linked_work_item_id="WI-002"
        )
        
        # Assert
        assert response.status_code == 204
        
        # Verify project ID appears in correct positions
        call_args = mock_linked_work_items_api._session.delete.call_args
        called_url = call_args[0][0]
        assert called_url.count(project_id) == 2  # Should appear twice
        print("\n✓ Mock: Same-project linked work item deletion works correctly")
    
    def test_delete_linked_work_item_no_body_sent(self, mock_linked_work_items_api):
        """Test that DELETE request does not send a body (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_linked_work_items_api.delete_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="MyLinkedWorkItemId"
        )
        
        # Verify no JSON body was sent
        call_args = mock_linked_work_items_api._session.delete.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        
        # Should not have 'json' parameter or it should be None
        assert call_kwargs.get('json') is None
        print("\n✓ Mock: DELETE request correctly sends no body (path-only parameters)")
