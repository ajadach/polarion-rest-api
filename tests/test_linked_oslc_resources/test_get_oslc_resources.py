"""
Pytest tests for get_oslc_resources method in LinkedOslcResources class.

Tests the GET /projects/{projectId}/workitems/{workItemId}/linkedoslcresources endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_get_oslc_resources.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.get
class TestGetOslcResources:
    """Unit tests for get_oslc_resources method using mocks"""
    
    def test_get_oslc_resources_success_200(self, mock_linked_oslc_resources_api):
        """Test successful retrieval with 200 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 200 status code
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 1
            },
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://server-host-name/ns/cm#relatedChangeRequest/http://server-host-name/application-path/oslc/services/projects/MyProjectId/workitems/MyWorkItemId",
                    "revision": "1234",
                    "attributes": {
                        "label": "Label",
                        "role": "http://open-services.net/ns/cm#relatedChangeRequest",
                        "uri": "Uri"
                    },
                    "links": {}
                }
            ],
            "included": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert 'data' in response_data
        assert 'meta' in response_data
        assert isinstance(response_data['data'], list)
        assert len(response_data['data']) > 0
        assert response_data['data'][0]['type'] == 'linkedoslcresources'
        
        # Verify correct endpoint was called
        call_args = mock_linked_oslc_resources_api._session.get.call_args
        assert f'projects/{project_id}/workitems/{work_item_id}/linkedoslcresources' in call_args[0][0]
        print("\n✓ Mock: OSLC resources retrieved successfully with 200 status code")
    
    def test_get_oslc_resources_unauthorized_401(self, mock_linked_oslc_resources_api):
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
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_get_oslc_resources_bad_request_400(self, mock_linked_oslc_resources_api):
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
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '400'
        assert response_data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in response_data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code")
    
    def test_get_oslc_resources_not_found_404(self, mock_linked_oslc_resources_api):
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
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "NonExistentWorkItem"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '404'
        assert response_data['errors'][0]['title'] == 'Not Found'
        print("\n✓ Mock: Not found returns 404 status code")
    
    def test_get_oslc_resources_with_pagination(self, mock_linked_oslc_resources_api):
        """Test with pagination parameters (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 100},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute with pagination from CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            page_size=123,
            page_number=456
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_linked_oslc_resources_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify pagination parameters
        assert 'page[size]' in params
        assert params['page[size]'] == 123
        assert 'page[number]' in params
        assert params['page[number]'] == 456
        print("\n✓ Mock: Pagination parameters handled correctly")
    
    def test_get_oslc_resources_with_default_fields(self, mock_linked_oslc_resources_api):
        """Test that default fields are applied automatically (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute without explicit fields parameter
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_linked_oslc_resources_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify default fields are applied
        assert 'fields[linkedoslcresources]' in params
        assert params['fields[linkedoslcresources]'] == '@all'
        assert 'fields[collections]' in params
        assert params['fields[collections]'] == '@all'
        print("\n✓ Mock: Default fields applied automatically")
    
    def test_get_oslc_resources_with_custom_fields(self, mock_linked_oslc_resources_api):
        """Test with custom fields parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute with custom fields
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        custom_fields = {
            'linkedoslcresources': 'label,role,uri',
            'workitems': 'title'
        }
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            fields=custom_fields
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_linked_oslc_resources_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom fields override defaults
        assert 'fields[linkedoslcresources]' in params
        assert params['fields[linkedoslcresources]'] == 'label,role,uri'
        assert 'fields[workitems]' in params
        assert params['fields[workitems]'] == 'title'
        print("\n✓ Mock: Custom fields override defaults correctly")
    
    def test_get_oslc_resources_with_include(self, mock_linked_oslc_resources_api):
        """Test with include parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": [],
            "included": [{"type": "workitems", "id": "MyProjectId/MyWorkItemId"}]
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute with include parameter from CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            include="include"
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_linked_oslc_resources_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify include parameter
        assert 'include' in params
        assert params['include'] == 'include'
        print("\n✓ Mock: Include parameter handled correctly")
    
    def test_get_oslc_resources_with_query(self, mock_linked_oslc_resources_api):
        """Test with query parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute with query parameter from CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            query="query"
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_linked_oslc_resources_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify query parameter
        assert 'query' in params
        assert params['query'] == 'query'
        print("\n✓ Mock: Query parameter handled correctly")
    
    def test_get_oslc_resources_with_sort(self, mock_linked_oslc_resources_api):
        """Test with sort parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute with sort parameter from CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            sort="sort"
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_linked_oslc_resources_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify sort parameter
        assert 'sort' in params
        assert params['sort'] == 'sort'
        print("\n✓ Mock: Sort parameter handled correctly")
    
    def test_get_oslc_resources_with_revision(self, mock_linked_oslc_resources_api):
        """Test with revision parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute with revision parameter from CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            revision="revision"
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_linked_oslc_resources_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify revision parameter
        assert 'revision' in params
        assert params['revision'] == 'revision'
        print("\n✓ Mock: Revision parameter handled correctly")
    
    def test_get_oslc_resources_with_all_parameters(self, mock_linked_oslc_resources_api):
        """Test with all parameters from CURL (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute with all parameters from CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        custom_fields = {'linkedoslcresources': 'label,role'}
        
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            page_size=123,
            page_number=456,
            fields=custom_fields,
            include="include",
            query="query",
            sort="sort",
            revision="revision"
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_linked_oslc_resources_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify all parameters
        assert params['page[size]'] == 123
        assert params['page[number]'] == 456
        assert params['fields[linkedoslcresources]'] == 'label,role'
        assert params['include'] == 'include'
        assert params['query'] == 'query'
        assert params['sort'] == 'sort'
        assert params['revision'] == 'revision'
        print("\n✓ Mock: All parameters handled correctly together")
    
    def test_get_oslc_resources_endpoint_format(self, mock_linked_oslc_resources_api):
        """Test that the correct endpoint format is used (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "TestProject"
        work_item_id = "WI-123"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_linked_oslc_resources_api._session.get.call_args
        endpoint = call_args[0][0]
        
        # Verify endpoint matches expected format from CURL
        assert f'projects/{project_id}/workitems/{work_item_id}/linkedoslcresources' in endpoint
        print("\n✓ Mock: Correct endpoint format used")
    
    def test_get_oslc_resources_response_structure(self, mock_linked_oslc_resources_api):
        """Test that response has correct structure (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 1
            },
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://server-host-name/ns/cm#relatedChangeRequest/http://server-host-name/application-path/oslc/services/projects/MyProjectId/workitems/MyWorkItemId",
                    "revision": "1234",
                    "attributes": {
                        "label": "Label",
                        "role": "http://open-services.net/ns/cm#relatedChangeRequest",
                        "uri": "Uri"
                    },
                    "links": {}
                }
            ],
            "included": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert response structure
        assert response.status_code == 200
        response_data = response.json()
        
        # Check structure
        assert 'meta' in response_data
        assert 'totalCount' in response_data['meta']
        assert 'data' in response_data
        assert isinstance(response_data['data'], list)
        
        # Check data item structure
        if len(response_data['data']) > 0:
            item = response_data['data'][0]
            assert 'type' in item
            assert 'id' in item
            assert 'attributes' in item
            assert 'label' in item['attributes']
            assert 'role' in item['attributes']
            assert 'uri' in item['attributes']
        
        print("\n✓ Mock: Response structure is correct")
    
    def test_get_oslc_resources_empty_list(self, mock_linked_oslc_resources_api):
        """Test with empty result list (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['meta']['totalCount'] == 0
        assert len(response_data['data']) == 0
        print("\n✓ Mock: Empty result list handled correctly")
    
    def test_get_oslc_resources_multiple_items(self, mock_linked_oslc_resources_api):
        """Test with multiple OSLC resources (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 3},
            "data": [
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource1",
                    "attributes": {"label": "Resource 1", "role": "role1", "uri": "uri1"}
                },
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource2",
                    "attributes": {"label": "Resource 2", "role": "role2", "uri": "uri2"}
                },
                {
                    "type": "linkedoslcresources",
                    "id": "MyProjectId/MyWorkItemId/http://example.com/resource3",
                    "attributes": {"label": "Resource 3", "role": "role3", "uri": "uri3"}
                }
            ]
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['meta']['totalCount'] == 3
        assert len(response_data['data']) == 3
        assert all(item['type'] == 'linkedoslcresources' for item in response_data['data'])
        print("\n✓ Mock: Multiple OSLC resources retrieved correctly")
    
    def test_get_oslc_resources_different_project_ids(self, mock_linked_oslc_resources_api):
        """Test with different project IDs (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Test various project IDs
        project_ids = ["Project1", "TEST_PROJECT", "my-project-123"]
        work_item_id = "WI-001"
        
        for project_id in project_ids:
            response = mock_linked_oslc_resources_api.get_oslc_resources(
                project_id=project_id,
                work_item_id=work_item_id
            )
            
            # Assert
            assert response.status_code == 200
            call_args = mock_linked_oslc_resources_api._session.get.call_args
            endpoint = call_args[0][0]
            assert f'projects/{project_id}/workitems/{work_item_id}' in endpoint
        
        print("\n✓ Mock: Different project IDs handled correctly")
    
    def test_get_oslc_resources_different_work_item_ids(self, mock_linked_oslc_resources_api):
        """Test with different work item IDs (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Test various work item IDs
        project_id = "MyProjectId"
        work_item_ids = ["WI-123", "TASK-456", "BUG_789", "FEATURE-001"]
        
        for work_item_id in work_item_ids:
            response = mock_linked_oslc_resources_api.get_oslc_resources(
                project_id=project_id,
                work_item_id=work_item_id
            )
            
            # Assert
            assert response.status_code == 200
            call_args = mock_linked_oslc_resources_api._session.get.call_args
            endpoint = call_args[0][0]
            assert f'workitems/{work_item_id}' in endpoint
        
        print("\n✓ Mock: Different work item IDs handled correctly")
    
    def test_get_oslc_resources_forbidden_403(self, mock_linked_oslc_resources_api):
        """Test forbidden access with 403 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "User does not have permission to access OSLC resources"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 403
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '403'
        assert response_data['errors'][0]['title'] == 'Forbidden'
        print("\n✓ Mock: Forbidden access returns 403 status code")
    
    def test_get_oslc_resources_server_error_500(self, mock_linked_oslc_resources_api):
        """Test server error with 500 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "500",
                    "title": "Internal Server Error",
                    "detail": "An error occurred while retrieving OSLC resources"
                }
            ]
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 500
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '500'
        assert response_data['errors'][0]['title'] == 'Internal Server Error'
        print("\n✓ Mock: Server error returns 500 status code")
    
    def test_get_oslc_resources_service_unavailable_503(self, mock_linked_oslc_resources_api):
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
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 503
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '503'
        assert response_data['errors'][0]['title'] == 'Service Unavailable'
        print("\n✓ Mock: Service unavailable returns 503 status code")
    
    def test_get_oslc_resources_pagination_and_fields_merge(self, mock_linked_oslc_resources_api):
        """Test that pagination and fields parameters are properly merged (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_linked_oslc_resources_api._session.get.return_value = mock_response
        
        # Execute with both pagination and fields
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        custom_fields = {'linkedoslcresources': 'label'}
        
        response = mock_linked_oslc_resources_api.get_oslc_resources(
            project_id=project_id,
            work_item_id=work_item_id,
            page_size=10,
            page_number=2,
            fields=custom_fields
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_linked_oslc_resources_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify both pagination and fields are present
        assert 'page[size]' in params
        assert params['page[size]'] == 10
        assert 'page[number]' in params
        assert params['page[number]'] == 2
        assert 'fields[linkedoslcresources]' in params
        assert params['fields[linkedoslcresources]'] == 'label'
        
        # Verify default fields still apply
        assert 'fields[collections]' in params
        print("\n✓ Mock: Pagination and fields parameters merged correctly")
