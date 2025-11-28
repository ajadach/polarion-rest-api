"""
Pytest tests for get_linked_work_items method in LinkedWorkItems class.

Tests the GET /projects/{projectId}/workitems/{workItemId}/linkedworkitems endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_get_linked_work_items.py -v
"""
import pytest
from unittest.mock import Mock


class TestGetLinkedWorkItems:
    """Unit tests for get_linked_work_items method using mocks"""
    
    def test_get_linked_work_items_success_200(self, mock_linked_work_items_api):
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
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId",
                    "revision": "1234",
                    "attributes": {
                        "revision": "1234",
                        "role": "relates_to",
                        "suspect": True
                    },
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "MyProjectId/MyWorkItemId",
                                "revision": "1234"
                            }
                        }
                    },
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/linkedworkitems/parent/MyProjectId/MyLinkedWorkItemId?revision=1234"
                    }
                }
            ],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/linkedworkitems/parent/MyProjectId?page%5Bsize%5D=10&page%5Bnumber%5D=5"
            }
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert 'data' in response_data
        assert 'meta' in response_data
        assert response_data['meta']['totalCount'] == 1
        assert len(response_data['data']) == 1
        assert response_data['data'][0]['type'] == 'linkedworkitems'
        print("\n✓ Mock: Linked work items retrieved successfully with 200 status code")
    
    def test_get_linked_work_items_with_pagination(self, mock_linked_work_items_api):
        """Test retrieval with pagination parameters (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 100},
            "data": [],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/linkedworkitems?page%5Bsize%5D=10&page%5Bnumber%5D=5"
            }
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with pagination
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            page_size=10,
            page_number=5
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify pagination parameters were passed
        call_args = mock_linked_work_items_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 10
        assert params['page[number]'] == 5
        print("\n✓ Mock: Pagination parameters handled correctly")
    
    def test_get_linked_work_items_with_fields(self, mock_linked_work_items_api):
        """Test retrieval with custom fields (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with custom fields
        custom_fields = {
            "workitems": "@basic",
            "linkedworkitems": "role,suspect"
        }
        
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            fields=custom_fields
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify custom fields were passed
        call_args = mock_linked_work_items_api._session.get.call_args
        params = call_args[1]['params']
        assert params['fields[workitems]'] == '@basic'
        assert params['fields[linkedworkitems]'] == 'role,suspect'
        # Default fields should still be present for other collections
        assert params['fields[documents]'] == '@all'
        print("\n✓ Mock: Custom fields handled correctly")
    
    def test_get_linked_work_items_with_include(self, mock_linked_work_items_api):
        """Test retrieval with include parameter (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": [],
            "included": [{}]
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with include
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            include="workItem"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify include parameter was passed
        call_args = mock_linked_work_items_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'workItem'
        print("\n✓ Mock: Include parameter handled correctly")
    
    def test_get_linked_work_items_with_revision(self, mock_linked_work_items_api):
        """Test retrieval with revision parameter (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with revision
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            revision="5678"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify revision parameter was passed
        call_args = mock_linked_work_items_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '5678'
        print("\n✓ Mock: Revision parameter handled correctly")
    
    def test_get_linked_work_items_unauthorized_401(self, mock_linked_work_items_api):
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
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId"
        )
        
        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_get_linked_work_items_bad_request_400(self, mock_linked_work_items_api):
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
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId"
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '400'
        assert response_data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in response_data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code with error details")
    
    def test_get_linked_work_items_not_found_404(self, mock_linked_work_items_api):
        """Test resource not found with 404 status code (mocked)"""
        # Setup mock response
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
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="MyProjectId",
            work_item_id="NonExistentWorkItem"
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '404'
        print("\n✓ Mock: Not found returns 404 status code")
    
    def test_get_linked_work_items_endpoint_structure(self, mock_linked_work_items_api):
        """Test that the correct endpoint structure is used (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "TEST_PROJ"
        work_item_id = "WI-123"
        
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        # Verify the endpoint structure
        call_args = mock_linked_work_items_api._session.get.call_args
        called_url = call_args[0][0]
        
        # Check endpoint components
        assert f'projects/{project_id}' in called_url
        assert f'workitems/{work_item_id}' in called_url
        assert 'linkedworkitems' in called_url
        
        # Verify complete URL structure
        expected_path = f'projects/{project_id}/workitems/{work_item_id}/linkedworkitems'
        assert expected_path in called_url
        print("\n✓ Mock: Endpoint structure is correct")
    
    def test_get_linked_work_items_default_fields(self, mock_linked_work_items_api):
        """Test that default fields are applied (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute without specifying fields
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify default fields were applied
        call_args = mock_linked_work_items_api._session.get.call_args
        params = call_args[1]['params']
        
        # Check that default fields are present
        assert 'fields[linkedworkitems]' in params
        assert params['fields[linkedworkitems]'] == '@all'
        assert 'fields[workitems]' in params
        assert params['fields[workitems]'] == '@all'
        print("\n✓ Mock: Default fields are applied correctly")
    
    def test_get_linked_work_items_all_parameters(self, mock_linked_work_items_api):
        """Test retrieval with all parameters (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with all parameters
        custom_fields = {"linkedworkitems": "role,suspect"}
        
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            page_size=123,
            page_number=456,
            fields=custom_fields,
            include="workItem",
            revision="1234"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify all parameters were passed
        call_args = mock_linked_work_items_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 123
        assert params['page[number]'] == 456
        assert params['fields[linkedworkitems]'] == 'role,suspect'
        assert params['include'] == 'workItem'
        assert params['revision'] == '1234'
        print("\n✓ Mock: All parameters handled correctly together")
    
    def test_get_linked_work_items_empty_response(self, mock_linked_work_items_api):
        """Test retrieval with empty data array (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": [],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/linkedworkitems"
            }
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId"
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['meta']['totalCount'] == 0
        assert len(response_data['data']) == 0
        print("\n✓ Mock: Empty response handled correctly")
    
    def test_get_linked_work_items_multiple_items(self, mock_linked_work_items_api):
        """Test retrieval with multiple linked work items (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 3},
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "Proj/WI1/parent/Proj/WI2",
                    "attributes": {"role": "parent"}
                },
                {
                    "type": "linkedworkitems",
                    "id": "Proj/WI1/relates_to/Proj/WI3",
                    "attributes": {"role": "relates_to"}
                },
                {
                    "type": "linkedworkitems",
                    "id": "Proj/WI1/depends_on/OtherProj/WI4",
                    "attributes": {"role": "depends_on"}
                }
            ]
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="Proj",
            work_item_id="WI1"
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['meta']['totalCount'] == 3
        assert len(response_data['data']) == 3
        print("\n✓ Mock: Multiple linked work items retrieved successfully")
    
    def test_get_linked_work_items_pagination_not_overwritten(self, mock_linked_work_items_api):
        """Test that pagination parameters are not overwritten by default fields (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with both pagination and fields
        response = mock_linked_work_items_api.get_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            page_size=25,
            page_number=3,
            fields={"workitems": "@basic"}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify pagination was NOT overwritten
        call_args = mock_linked_work_items_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 25, "Pagination page_size should not be overwritten"
        assert params['page[number]'] == 3, "Pagination page_number should not be overwritten"
        assert params['fields[workitems]'] == '@basic'
        print("\n✓ Mock: Pagination parameters are preserved correctly")
