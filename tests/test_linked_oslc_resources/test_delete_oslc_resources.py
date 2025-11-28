"""
Pytest tests for delete_oslc_resources method in LinkedOslcResources class.

Tests the DELETE /projects/{projectId}/workitems/{workItemId}/linkedoslcresources endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_delete_oslc_resources.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.delete
class TestDeleteOslcResources:
    """Unit tests for delete_oslc_resources method using mocks"""
    
    def test_delete_oslc_resources_success_204(self, mock_linked_oslc_resources_api):
        """Test successful deletion with 204 status code (mocked)"""
        # Setup mock response (DELETE typically returns 204 No Content)
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute with data matching BODY from CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://server-host-name/ns/cm#relatedChangeRequest/http://server-host-name/application-path/oslc/services/projects/MyProjectId/workitems/MyWorkItemId"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 204
        
        # Verify correct endpoint was called
        call_args = mock_linked_oslc_resources_api._session.delete.call_args
        assert f'projects/{project_id}/workitems/{work_item_id}/linkedoslcresources' in call_args[0][0]
        print("\n✓ Mock: OSLC resources deleted successfully with 204 status code")
    
    def test_delete_oslc_resources_unauthorized_401(self, mock_linked_oslc_resources_api):
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
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_delete_oslc_resources_bad_request_400(self, mock_linked_oslc_resources_api):
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
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute with invalid data
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {"invalid": "data"}
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '400'
        assert response_data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in response_data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code")
    
    def test_delete_oslc_resources_not_found_404(self, mock_linked_oslc_resources_api):
        """Test resource not found with 404 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Work item 'NonExistentWorkItem' not found in project 'MyProjectId'"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "NonExistentWorkItem"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/NonExistentWorkItem/http://example.com/resource"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '404'
        assert response_data['errors'][0]['title'] == 'Not Found'
        print("\n✓ Mock: Not found returns 404 status code")
    
    def test_delete_oslc_resources_forbidden_403(self, mock_linked_oslc_resources_api):
        """Test forbidden access with 403 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "User does not have permission to delete OSLC resources"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 403
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '403'
        assert response_data['errors'][0]['title'] == 'Forbidden'
        print("\n✓ Mock: Forbidden access returns 403 status code")
    
    def test_delete_oslc_resources_endpoint_format(self, mock_linked_oslc_resources_api):
        """Test that the correct endpoint format is used (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "TestProject"
        work_item_id = "WI-123"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "TestProject/WI-123/http://example.com/resource"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 204
        call_args = mock_linked_oslc_resources_api._session.delete.call_args
        endpoint = call_args[0][0]
        
        # Verify endpoint matches expected format from CURL
        assert f'projects/{project_id}/workitems/{work_item_id}/linkedoslcresources' in endpoint
        print("\n✓ Mock: Correct endpoint format used")
    
    def test_delete_oslc_resources_single_resource(self, mock_linked_oslc_resources_api):
        """Test deletion of single OSLC resource (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute with single resource
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://server-host-name/ns/cm#relatedChangeRequest/http://server-host-name/application-path/oslc/services/projects/MyProjectId/workitems/MyWorkItemId"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 204
        call_args = mock_linked_oslc_resources_api._session.delete.call_args
        
        # Verify JSON data was sent
        assert 'json' in call_args[1]
        assert call_args[1]['json'] == oslc_data
        assert len(call_args[1]['json']['data']) == 1
        print("\n✓ Mock: Single OSLC resource deletion handled correctly")
    
    def test_delete_oslc_resources_multiple_resources(self, mock_linked_oslc_resources_api):
        """Test deletion of multiple OSLC resources (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute with multiple resources
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource1"
                },
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource2"
                },
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource3"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 204
        call_args = mock_linked_oslc_resources_api._session.delete.call_args
        
        # Verify all resources were sent
        assert 'json' in call_args[1]
        assert len(call_args[1]['json']['data']) == 3
        print("\n✓ Mock: Multiple OSLC resources deletion handled correctly")
    
    def test_delete_oslc_resources_with_complex_id(self, mock_linked_oslc_resources_api):
        """Test deletion with complex OSLC resource ID (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute with complex ID format
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        complex_id = "MyProjectId/MyWorkItemId/http://server-host-name/ns/cm#relatedChangeRequest/http://server-host-name/application-path/oslc/services/projects/MyProjectId/workitems/MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": complex_id
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 204
        call_args = mock_linked_oslc_resources_api._session.delete.call_args
        
        # Verify complex ID was sent correctly
        sent_data = call_args[1]['json']
        assert sent_data['data'][0]['id'] == complex_id
        print("\n✓ Mock: Complex OSLC resource ID handled correctly")
    
    def test_delete_oslc_resources_different_project_ids(self, mock_linked_oslc_resources_api):
        """Test with different project IDs (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Test various project IDs
        project_ids = ["Project1", "TEST_PROJECT", "my-project-123"]
        work_item_id = "WI-001"
        
        for project_id in project_ids:
            oslc_data = {
                "data": [
                    {
                        "type": "linkedoslcresources",
                        "id": f"{project_id}/{work_item_id}/http://example.com/resource"
                    }
                ]
            }
            
            response = mock_linked_oslc_resources_api.delete_oslc_resources(
                project_id=project_id,
                work_item_id=work_item_id,
                oslc_data=oslc_data
            )
            
            # Assert
            assert response.status_code == 204
            call_args = mock_linked_oslc_resources_api._session.delete.call_args
            endpoint = call_args[0][0]
            assert f'projects/{project_id}/workitems/{work_item_id}' in endpoint
        
        print("\n✓ Mock: Different project IDs handled correctly")
    
    def test_delete_oslc_resources_different_work_item_ids(self, mock_linked_oslc_resources_api):
        """Test with different work item IDs (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Test various work item IDs
        project_id = "MyProjectId"
        work_item_ids = ["WI-123", "TASK-456", "BUG_789", "FEATURE-001"]
        
        for work_item_id in work_item_ids:
            oslc_data = {
                "data": [
                    {
                        "type": "linkedoslcresources",
                        "id": f"{project_id}/{work_item_id}/http://example.com/resource"
                    }
                ]
            }
            
            response = mock_linked_oslc_resources_api.delete_oslc_resources(
                project_id=project_id,
                work_item_id=work_item_id,
                oslc_data=oslc_data
            )
            
            # Assert
            assert response.status_code == 204
            call_args = mock_linked_oslc_resources_api._session.delete.call_args
            endpoint = call_args[0][0]
            assert f'workitems/{work_item_id}' in endpoint
        
        print("\n✓ Mock: Different work item IDs handled correctly")
    
    def test_delete_oslc_resources_json_content_type(self, mock_linked_oslc_resources_api):
        """Test that Content-Type is application/json (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 204
        call_args = mock_linked_oslc_resources_api._session.delete.call_args
        
        # Verify JSON was sent (not form data or other)
        assert 'json' in call_args[1]
        assert call_args[1]['json'] == oslc_data
        print("\n✓ Mock: JSON content type used correctly")
    
    def test_delete_oslc_resources_server_error_500(self, mock_linked_oslc_resources_api):
        """Test server error with 500 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "500",
                    "title": "Internal Server Error",
                    "detail": "An error occurred while deleting OSLC resources"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 500
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '500'
        assert response_data['errors'][0]['title'] == 'Internal Server Error'
        print("\n✓ Mock: Server error returns 500 status code")
    
    def test_delete_oslc_resources_service_unavailable_503(self, mock_linked_oslc_resources_api):
        """Test service unavailable with 503 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "503",
                    "title": "Service Unavailable",
                    "detail": "Service temporarily unavailable"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 503
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '503'
        assert response_data['errors'][0]['title'] == 'Service Unavailable'
        print("\n✓ Mock: Service unavailable returns 503 status code")
    
    def test_delete_oslc_resources_http_method(self, mock_linked_oslc_resources_api):
        """Test that DELETE HTTP method is used (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 204
        call_args = mock_linked_oslc_resources_api._session.delete.call_args
        
        # Verify DELETE method was used (by checking that delete was called)
        assert mock_linked_oslc_resources_api._session.delete.called
        assert f'projects/{project_id}/workitems/{work_item_id}/linkedoslcresources' in call_args[0][0]
        print("\n✓ Mock: DELETE HTTP method used correctly")
    
    def test_delete_oslc_resources_empty_response_body(self, mock_linked_oslc_resources_api):
        """Test that 204 response has no content (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_response.content = b""
        mock_linked_oslc_resources_api._session.delete.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource"
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.delete_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 204
        assert response.text == ""
        assert response.content == b""
        print("\n✓ Mock: 204 response has no content as expected")
