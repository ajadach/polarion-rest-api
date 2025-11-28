"""
Pytest tests for delete_linked_work_items method in LinkedWorkItems class.

Tests the DELETE /projects/{projectId}/workitems/{workItemId}/linkedworkitems endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_delete_linked_work_items.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.delete
class TestDeleteLinkedWorkItems:
    """Unit tests for delete_linked_work_items method using mocks"""
    
    def test_delete_linked_work_items_success_204(self, mock_linked_work_items_api):
        """Test successful deletion with 204 status code (mocked)"""
        # Setup mock response (DELETE typically returns 204 No Content)
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with data matching BODY from CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 204
        
        # Verify correct endpoint was called
        call_args = mock_linked_work_items_api._session.delete.call_args
        expected_url = f'https://test.polarion.com/polarion/rest/v1/projects/{project_id}/workitems/{work_item_id}/linkedworkitems'
        assert call_args[0][0] == expected_url
        print("\n✓ Mock: Linked work items deleted successfully with 204 status code")
    
    def test_delete_linked_work_items_unauthorized_401(self, mock_linked_work_items_api):
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
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_delete_linked_work_items_bad_request_400(self, mock_linked_work_items_api):
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
        
        # Execute with potentially invalid data structure
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        linked_items_data = {
            "data": "invalid_structure"  # Invalid: should be array
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '400'
        assert response_data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in response_data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code with error details")
    
    def test_delete_linked_work_items_multiple_items(self, mock_linked_work_items_api):
        """Test deletion of multiple linked work items (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with multiple items
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/LinkedItem1"
                },
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/relates_to/MyProjectId/LinkedItem2"
                },
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/depends_on/OtherProject/LinkedItem3"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 204
        
        # Verify JSON body was sent
        call_args = mock_linked_work_items_api._session.delete.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        assert 'json' in call_kwargs
        assert call_kwargs['json'] == linked_items_data
        print("\n✓ Mock: Multiple linked work items deleted successfully")
    
    def test_delete_linked_work_items_single_item(self, mock_linked_work_items_api):
        """Test deletion of a single linked work item using plural method (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with single item in array
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 204
        print("\n✓ Mock: Single linked work item deleted using plural method")
    
    def test_delete_linked_work_items_not_found_404(self, mock_linked_work_items_api):
        """Test resource not found with 404 status code (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "One or more linked work items were not found"
                }
            ]
        }
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/NonExistentItem"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '404'
        print("\n✓ Mock: Not found returns 404 status code")
    
    def test_delete_linked_work_items_forbidden_403(self, mock_linked_work_items_api):
        """Test forbidden access with 403 status code (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You don't have permission to delete these linked work items"
                }
            ]
        }
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "RestrictedProject"
        work_item_id = "RestrictedWorkItem"
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "RestrictedProject/RestrictedWorkItem/parent/RestrictedProject/RestrictedLinkedItem"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 403
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '403'
        print("\n✓ Mock: Forbidden access returns 403 status code")
    
    def test_delete_linked_work_items_internal_error_500(self, mock_linked_work_items_api):
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
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 500
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '500'
        print("\n✓ Mock: Internal server error returns 500 status code")
    
    def test_delete_linked_work_items_endpoint_structure(self, mock_linked_work_items_api):
        """Test that the correct endpoint structure is used (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "TEST_PROJ"
        work_item_id = "WI-123"
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "TEST_PROJ/WI-123/parent/TEST_PROJ/WI-456"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Verify the endpoint structure
        call_args = mock_linked_work_items_api._session.delete.call_args
        called_url = call_args[0][0]
        
        # Check endpoint components
        assert f'projects/{project_id}' in called_url
        assert f'workitems/{work_item_id}' in called_url
        assert 'linkedworkitems' in called_url
        
        # Verify complete URL structure (no extra path parameters)
        expected_path = f'projects/{project_id}/workitems/{work_item_id}/linkedworkitems'
        assert expected_path in called_url
        print("\n✓ Mock: Endpoint structure is correct")
    
    def test_delete_linked_work_items_body_with_different_roles(self, mock_linked_work_items_api):
        """Test deletion with different role types in the ID (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Test different roles in the linkedworkitems ID
        test_roles = ["parent", "child", "relates_to", "duplicates", "depends_on"]
        
        for role in test_roles:
            linked_items_data = {
                "data": [
                    {
                        "type": "linkedworkitems",
                        "id": f"MyProjectId/MyWorkItemId/{role}/MyProjectId/LinkedItem"
                    }
                ]
            }
            
            response = mock_linked_work_items_api.delete_linked_work_items(
                project_id="MyProjectId",
                work_item_id="MyWorkItemId",
                linked_items_data=linked_items_data
            )
            
            assert response.status_code == 204
            
            # Verify the role is in the body
            call_args = mock_linked_work_items_api._session.delete.call_args
            call_kwargs = call_args[1] if len(call_args) > 1 else {}
            assert role in call_kwargs['json']['data'][0]['id']
        
        print(f"\n✓ Mock: Tested {len(test_roles)} different role types in body")
    
    def test_delete_linked_work_items_cross_project(self, mock_linked_work_items_api):
        """Test deletion of cross-project linked work items (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with cross-project links
        source_project = "ProjectA"
        target_project = "ProjectB"
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": f"{source_project}/WI-A-001/relates_to/{target_project}/WI-B-001"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=source_project,
            work_item_id="WI-A-001",
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 204
        
        # Verify both projects are in the body
        call_args = mock_linked_work_items_api._session.delete.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        item_id = call_kwargs['json']['data'][0]['id']
        assert source_project in item_id
        assert target_project in item_id
        print("\n✓ Mock: Cross-project linked work items deletion works correctly")
    
    def test_delete_linked_work_items_body_structure(self, mock_linked_work_items_api):
        """Test that the correct body structure is sent (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Verify the body structure
        call_args = mock_linked_work_items_api._session.delete.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        
        assert 'json' in call_kwargs
        body = call_kwargs['json']
        assert 'data' in body
        assert isinstance(body['data'], list)
        assert len(body['data']) >= 1
        assert body['data'][0]['type'] == 'linkedworkitems'
        assert 'id' in body['data'][0]
        print("\n✓ Mock: Request body structure is correct")
    
    def test_delete_linked_work_items_empty_data_array(self, mock_linked_work_items_api):
        """Test deletion with empty data array (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Data array cannot be empty"
                }
            ]
        }
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with empty data array
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        linked_items_data = {
            "data": []
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 400
        print("\n✓ Mock: Empty data array returns 400 status code")
    
    def test_delete_linked_work_items_uses_delete_with_body(self, mock_linked_work_items_api):
        """Test that the method uses _delete_with_body (DELETE with JSON body) (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Verify DELETE method was used with JSON body
        call_args = mock_linked_work_items_api._session.delete.call_args
        # Verify the method was called (we're already using .delete())
        assert mock_linked_work_items_api._session.delete.called
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        assert 'json' in call_kwargs
        assert call_kwargs['json'] == linked_items_data
        print("\n✓ Mock: Method correctly uses DELETE with JSON body")
    
    def test_delete_linked_work_items_id_format(self, mock_linked_work_items_api):
        """Test that the ID format in body follows the correct pattern (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with correctly formatted ID
        # Format: {projectId}/{workItemId}/{roleId}/{targetProjectId}/{linkedWorkItemId}
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId"
                }
            ]
        }
        
        response = mock_linked_work_items_api.delete_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            linked_items_data=linked_items_data
        )
        
        # Verify the ID format has 5 segments separated by slashes
        call_args = mock_linked_work_items_api._session.delete.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        item_id = call_kwargs['json']['data'][0]['id']
        id_segments = item_id.split('/')
        assert len(id_segments) == 5, f"Expected 5 segments in ID, got {len(id_segments)}"
        print("\n✓ Mock: Linked work item ID follows correct format (5 segments)")
