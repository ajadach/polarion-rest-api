"""
Pytest tests for post_oslc_resources method in LinkedOslcResources class.

Tests the POST /projects/{projectId}/workitems/{workItemId}/linkedoslcresources endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_post_oslc_resources.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.post
class TestPostOslcResources:
    """Unit tests for post_oslc_resources method using mocks"""
    
    def test_post_oslc_resources_success_201(self, mock_linked_oslc_resources_api):
        """Test successful creation with 201 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 201 status code
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://server-host-name/ns/cm#relatedChangeRequest/http://server-host-name/application-path/oslc/services/projects/MyProjectId/workitems/MyWorkItemId",
                    "links": {}
                }
            ]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute with data matching BODY from CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "http://open-services.net/ns/cm#relatedChangeRequest",
                        "uri": "Uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 201
        response_data = response.json()
        assert 'data' in response_data
        assert isinstance(response_data['data'], list)
        assert len(response_data['data']) > 0
        assert response_data['data'][0]['type'] == 'linkedoslcresources'
        assert 'id' in response_data['data'][0]
        
        # Verify correct endpoint was called
        call_args = mock_linked_oslc_resources_api._session.post.call_args
        assert f'projects/{project_id}/workitems/{work_item_id}/linkedoslcresources' in call_args[0][0]
        print("\n✓ Mock: OSLC resources created successfully with 201 status code")
    
    def test_post_oslc_resources_unauthorized_401(self, mock_linked_oslc_resources_api):
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
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "http://open-services.net/ns/cm#relatedChangeRequest",
                        "uri": "Uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
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
    
    def test_post_oslc_resources_bad_request_400(self, mock_linked_oslc_resources_api):
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
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute with invalid data
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {"invalid": "data"}
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
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
    
    def test_post_oslc_resources_not_found_404(self, mock_linked_oslc_resources_api):
        """Test resource not found with 404 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Work item 'NonExistentWorkItem' not found"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "NonExistentWorkItem"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "role",
                        "uri": "uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
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
    
    def test_post_oslc_resources_forbidden_403(self, mock_linked_oslc_resources_api):
        """Test forbidden access with 403 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "User does not have permission to create OSLC resources"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "role",
                        "uri": "uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
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
    
    def test_post_oslc_resources_endpoint_format(self, mock_linked_oslc_resources_api):
        """Test that the correct endpoint format is used (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "TestProject/WI-123/http://example.com/resource"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "TestProject"
        work_item_id = "WI-123"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "role",
                        "uri": "uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_linked_oslc_resources_api._session.post.call_args
        endpoint = call_args[0][0]
        
        # Verify endpoint matches expected format from CURL
        assert f'projects/{project_id}/workitems/{work_item_id}/linkedoslcresources' in endpoint
        print("\n✓ Mock: Correct endpoint format used")
    
    def test_post_oslc_resources_single_resource(self, mock_linked_oslc_resources_api):
        """Test creation of single OSLC resource (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://server-host-name/ns/cm#relatedChangeRequest/http://server-host-name/application-path/oslc/services/projects/MyProjectId/workitems/MyWorkItemId",
                    "links": {}
                }
            ]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute with single resource
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "http://open-services.net/ns/cm#relatedChangeRequest",
                        "uri": "Uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_linked_oslc_resources_api._session.post.call_args
        
        # Verify JSON data was sent
        assert 'json' in call_args[1]
        assert call_args[1]['json'] == oslc_data
        assert len(call_args[1]['json']['data']) == 1
        print("\n✓ Mock: Single OSLC resource creation handled correctly")
    
    def test_post_oslc_resources_multiple_resources(self, mock_linked_oslc_resources_api):
        """Test creation of multiple OSLC resources (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
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
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute with multiple resources
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Resource 1",
                        "role": "role1",
                        "uri": "uri1"
                    }
                },
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Resource 2",
                        "role": "role2",
                        "uri": "uri2"
                    }
                },
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Resource 3",
                        "role": "role3",
                        "uri": "uri3"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_linked_oslc_resources_api._session.post.call_args
        
        # Verify all resources were sent
        assert 'json' in call_args[1]
        assert len(call_args[1]['json']['data']) == 3
        print("\n✓ Mock: Multiple OSLC resources creation handled correctly")
    
    def test_post_oslc_resources_with_complete_attributes(self, mock_linked_oslc_resources_api):
        """Test creation with complete attributes from BODY (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://server-host-name/ns/cm#relatedChangeRequest/http://server-host-name/application-path/oslc/services/projects/MyProjectId/workitems/MyWorkItemId"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute with complete attributes from BODY
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "http://open-services.net/ns/cm#relatedChangeRequest",
                        "uri": "Uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_linked_oslc_resources_api._session.post.call_args
        sent_data = call_args[1]['json']
        
        # Verify all required attributes
        assert sent_data['data'][0]['attributes']['label'] == 'Label'
        assert sent_data['data'][0]['attributes']['role'] == 'http://open-services.net/ns/cm#relatedChangeRequest'
        assert sent_data['data'][0]['attributes']['uri'] == 'Uri'
        print("\n✓ Mock: Complete attributes handled correctly")
    
    def test_post_oslc_resources_different_project_ids(self, mock_linked_oslc_resources_api):
        """Test with different project IDs (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{"type": "linkedoslcresources", "id": "test/test/test"}]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Test various project IDs
        project_ids = ["Project1", "TEST_PROJECT", "my-project-123"]
        work_item_id = "WI-001"
        
        for project_id in project_ids:
            oslc_data = {
                "data": [
                    {
                        "type": "linkedoslcresources",
                        "attributes": {
                            "label": "Label",
                            "role": "role",
                            "uri": "uri"
                        }
                    }
                ]
            }
            
            response = mock_linked_oslc_resources_api.post_oslc_resources(
                project_id=project_id,
                work_item_id=work_item_id,
                oslc_data=oslc_data
            )
            
            # Assert
            assert response.status_code == 201
            call_args = mock_linked_oslc_resources_api._session.post.call_args
            endpoint = call_args[0][0]
            assert f'projects/{project_id}/workitems/{work_item_id}' in endpoint
        
        print("\n✓ Mock: Different project IDs handled correctly")
    
    def test_post_oslc_resources_different_work_item_ids(self, mock_linked_oslc_resources_api):
        """Test with different work item IDs (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{"type": "linkedoslcresources", "id": "test/test/test"}]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Test various work item IDs
        project_id = "MyProjectId"
        work_item_ids = ["WI-123", "TASK-456", "BUG_789", "FEATURE-001"]
        
        for work_item_id in work_item_ids:
            oslc_data = {
                "data": [
                    {
                        "type": "linkedoslcresources",
                        "attributes": {
                            "label": "Label",
                            "role": "role",
                            "uri": "uri"
                        }
                    }
                ]
            }
            
            response = mock_linked_oslc_resources_api.post_oslc_resources(
                project_id=project_id,
                work_item_id=work_item_id,
                oslc_data=oslc_data
            )
            
            # Assert
            assert response.status_code == 201
            call_args = mock_linked_oslc_resources_api._session.post.call_args
            endpoint = call_args[0][0]
            assert f'workitems/{work_item_id}' in endpoint
        
        print("\n✓ Mock: Different work item IDs handled correctly")
    
    def test_post_oslc_resources_json_content_type(self, mock_linked_oslc_resources_api):
        """Test that Content-Type is application/json (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{"type": "linkedoslcresources", "id": "test/test/test"}]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "role",
                        "uri": "uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_linked_oslc_resources_api._session.post.call_args
        
        # Verify JSON was sent (not form data or other)
        assert 'json' in call_args[1]
        assert call_args[1]['json'] == oslc_data
        print("\n✓ Mock: JSON content type used correctly")
    
    def test_post_oslc_resources_response_structure(self, mock_linked_oslc_resources_api):
        """Test that response has correct structure (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://server-host-name/ns/cm#relatedChangeRequest/http://server-host-name/application-path/oslc/services/projects/MyProjectId/workitems/MyWorkItemId",
                    "links": {}
                }
            ]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "http://open-services.net/ns/cm#relatedChangeRequest",
                        "uri": "Uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert response structure
        assert response.status_code == 201
        response_data = response.json()
        
        # Check structure
        assert 'data' in response_data
        assert isinstance(response_data['data'], list)
        assert 'type' in response_data['data'][0]
        assert 'id' in response_data['data'][0]
        assert 'links' in response_data['data'][0]
        
        print("\n✓ Mock: Response structure is correct")
    
    def test_post_oslc_resources_conflict_409(self, mock_linked_oslc_resources_api):
        """Test conflict error with 409 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "409",
                    "title": "Conflict",
                    "detail": "OSLC resource already exists"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "role",
                        "uri": "uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 409
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '409'
        assert response_data['errors'][0]['title'] == 'Conflict'
        print("\n✓ Mock: Conflict returns 409 status code")
    
    def test_post_oslc_resources_entity_too_large_413(self, mock_linked_oslc_resources_api):
        """Test request entity too large with 413 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 413
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "413",
                    "title": "Request Entity Too Large",
                    "detail": "Request body size exceeds maximum allowed size"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [{"type": "linkedoslcresources", "attributes": {"label": "x" * 10000}}]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 413
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '413'
        assert response_data['errors'][0]['title'] == 'Request Entity Too Large'
        print("\n✓ Mock: Request entity too large returns 413 status code")
    
    def test_post_oslc_resources_unsupported_media_type_415(self, mock_linked_oslc_resources_api):
        """Test unsupported media type with 415 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 415
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "415",
                    "title": "Unsupported Media Type",
                    "detail": "Content-Type must be application/json"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "role",
                        "uri": "uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 415
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '415'
        assert response_data['errors'][0]['title'] == 'Unsupported Media Type'
        print("\n✓ Mock: Unsupported media type returns 415 status code")
    
    def test_post_oslc_resources_server_error_500(self, mock_linked_oslc_resources_api):
        """Test server error with 500 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "500",
                    "title": "Internal Server Error",
                    "detail": "An error occurred while creating OSLC resources"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "role",
                        "uri": "uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
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
    
    def test_post_oslc_resources_service_unavailable_503(self, mock_linked_oslc_resources_api):
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
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "role",
                        "uri": "uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
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
    
    def test_post_oslc_resources_data_type_validation(self, mock_linked_oslc_resources_api):
        """Test that data type is validated (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{"type": "linkedoslcresources", "id": "test/test/test"}]
        }
        mock_linked_oslc_resources_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        oslc_data = {
            "data": [
                {
                    "type": "linkedoslcresources",
                    "attributes": {
                        "label": "Label",
                        "role": "role",
                        "uri": "uri"
                    }
                }
            ]
        }
        
        response = mock_linked_oslc_resources_api.post_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            oslc_data=oslc_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_linked_oslc_resources_api._session.post.call_args
        sent_data = call_args[1]['json']
        
        # Verify type field is correct
        assert sent_data['data'][0]['type'] == 'linkedoslcresources'
        print("\n✓ Mock: Data type validation handled correctly")
