"""
Pytest tests for get_linked_work_item method in LinkedWorkItems class.

Tests the GET /projects/{projectId}/workitems/{workItemId}/linkedworkitems/{roleId}/{targetProjectId}/{linkedWorkItemId} endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_get_linked_work_item.py -v
"""
import pytest
from unittest.mock import Mock


class TestGetLinkedWorkItem:
    """Unit tests for get_linked_work_item method using mocks"""
    
    def test_get_linked_work_item_success_200(self, mock_linked_work_items_api):
        """Test successful retrieval with 200 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 200 status code
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
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
            },
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/linkedworkitems/parent/MyProjectId/MyLinkedWorkItemId?revision=1234"
            }
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        role_id = "parent"
        target_project_id = "MyProjectId"
        linked_work_item_id = "MyLinkedWorkItemId"
        
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id=project_id,
            work_item_id=work_item_id,
            role_id=role_id,
            target_project_id=target_project_id,
            linked_work_item_id=linked_work_item_id
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert 'data' in response_data
        assert response_data['data']['type'] == 'linkedworkitems'
        assert response_data['data']['id'] == f'{project_id}/{work_item_id}/{role_id}/{target_project_id}/{linked_work_item_id}'
        assert 'attributes' in response_data['data']
        assert 'relationships' in response_data['data']
        print("\n✓ Mock: Linked work item retrieved successfully with 200 status code")
    
    def test_get_linked_work_item_with_fields(self, mock_linked_work_items_api):
        """Test retrieval with custom fields (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "linkedworkitems",
                "id": "Proj/WI1/parent/Proj/WI2",
                "attributes": {"role": "parent"}
            }
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with custom fields
        custom_fields = {
            "linkedworkitems": "role,suspect",
            "workitems": "@basic"
        }
        
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id="Proj",
            work_item_id="WI1",
            role_id="parent",
            target_project_id="Proj",
            linked_work_item_id="WI2",
            fields=custom_fields
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify custom fields were passed
        call_args = mock_linked_work_items_api._session.get.call_args
        params = call_args[1]['params']
        assert params['fields[linkedworkitems]'] == 'role,suspect'
        assert params['fields[workitems]'] == '@basic'
        # Default fields should still be present for other collections
        assert params['fields[documents]'] == '@all'
        print("\n✓ Mock: Custom fields handled correctly")
    
    def test_get_linked_work_item_with_include(self, mock_linked_work_items_api):
        """Test retrieval with include parameter (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "linkedworkitems",
                "id": "Proj/WI1/parent/Proj/WI2"
            },
            "included": [
                {
                    "type": "workitems",
                    "id": "Proj/WI2"
                }
            ]
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with include
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id="Proj",
            work_item_id="WI1",
            role_id="parent",
            target_project_id="Proj",
            linked_work_item_id="WI2",
            include="workItem"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify include parameter was passed
        call_args = mock_linked_work_items_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'workItem'
        print("\n✓ Mock: Include parameter handled correctly")
    
    def test_get_linked_work_item_with_revision(self, mock_linked_work_items_api):
        """Test retrieval with revision parameter (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "linkedworkitems",
                "id": "Proj/WI1/parent/Proj/WI2",
                "revision": "5678"
            }
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with revision
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id="Proj",
            work_item_id="WI1",
            role_id="parent",
            target_project_id="Proj",
            linked_work_item_id="WI2",
            revision="5678"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify revision parameter was passed
        call_args = mock_linked_work_items_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '5678'
        print("\n✓ Mock: Revision parameter handled correctly")
    
    def test_get_linked_work_item_unauthorized_401(self, mock_linked_work_items_api):
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
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="MyLinkedWorkItemId"
        )
        
        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_get_linked_work_item_bad_request_400(self, mock_linked_work_items_api):
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
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="MyLinkedWorkItemId"
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '400'
        assert response_data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in response_data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code with error details")
    
    def test_get_linked_work_item_not_found_404(self, mock_linked_work_items_api):
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
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="NonExistentItem"
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '404'
        print("\n✓ Mock: Not found returns 404 status code")
    
    def test_get_linked_work_item_endpoint_structure(self, mock_linked_work_items_api):
        """Test that the correct endpoint structure is used (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "linkedworkitems", "id": "test"}}
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with specific parameters
        project_id = "TEST_PROJ"
        work_item_id = "WI-123"
        role_id = "relates_to"
        target_project_id = "TARGET_PROJ"
        linked_work_item_id = "WI-456"
        
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id=project_id,
            work_item_id=work_item_id,
            role_id=role_id,
            target_project_id=target_project_id,
            linked_work_item_id=linked_work_item_id
        )
        
        # Verify the endpoint structure
        call_args = mock_linked_work_items_api._session.get.call_args
        called_url = call_args[0][0]
        
        # Check that all path parameters are in the correct order
        assert f'projects/{project_id}' in called_url
        assert f'workitems/{work_item_id}' in called_url
        assert f'linkedworkitems/{role_id}' in called_url
        assert f'{role_id}/{target_project_id}' in called_url
        assert f'{target_project_id}/{linked_work_item_id}' in called_url
        
        # Verify complete URL structure
        expected_path = f'projects/{project_id}/workitems/{work_item_id}/linkedworkitems/{role_id}/{target_project_id}/{linked_work_item_id}'
        assert expected_path in called_url
        print("\n✓ Mock: Endpoint structure is correct with all path parameters")
    
    def test_get_linked_work_item_default_fields(self, mock_linked_work_items_api):
        """Test that default fields are applied (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "linkedworkitems", "id": "test"}}
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute without specifying fields
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="MyLinkedWorkItemId"
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
    
    def test_get_linked_work_item_all_parameters(self, mock_linked_work_items_api):
        """Test retrieval with all parameters (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "linkedworkitems", "id": "test"}}
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with all parameters
        custom_fields = {"linkedworkitems": "role,suspect"}
        
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="MyLinkedWorkItemId",
            fields=custom_fields,
            include="workItem",
            revision="1234"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify all parameters were passed
        call_args = mock_linked_work_items_api._session.get.call_args
        params = call_args[1]['params']
        assert params['fields[linkedworkitems]'] == 'role,suspect'
        assert params['include'] == 'workItem'
        assert params['revision'] == '1234'
        print("\n✓ Mock: All parameters handled correctly together")
    
    def test_get_linked_work_item_different_roles(self, mock_linked_work_items_api):
        """Test retrieval with different role types (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "linkedworkitems", "id": "test"}}
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Test different role types
        test_roles = [
            "parent",
            "child",
            "relates_to",
            "duplicates",
            "depends_on"
        ]
        
        for role_id in test_roles:
            response = mock_linked_work_items_api.get_linked_work_item(
                project_id="MyProjectId",
                work_item_id="MyWorkItemId",
                role_id=role_id,
                target_project_id="MyProjectId",
                linked_work_item_id="MyLinkedWorkItemId"
            )
            
            assert response.status_code == 200
            
            # Verify role is in the URL
            call_args = mock_linked_work_items_api._session.get.call_args
            called_url = call_args[0][0]
            assert f'linkedworkitems/{role_id}/' in called_url
        
        print(f"\n✓ Mock: Tested {len(test_roles)} different role types successfully")
    
    def test_get_linked_work_item_cross_project(self, mock_linked_work_items_api):
        """Test retrieval of cross-project linked work item (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "linkedworkitems",
                "id": "ProjectA/WI-A-001/relates_to/ProjectB/WI-B-001"
            }
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with different project IDs (cross-project link)
        source_project = "ProjectA"
        target_project = "ProjectB"
        
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id=source_project,
            work_item_id="WI-A-001",
            role_id="relates_to",
            target_project_id=target_project,
            linked_work_item_id="WI-B-001"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify both project IDs are in the URL
        call_args = mock_linked_work_items_api._session.get.call_args
        called_url = call_args[0][0]
        assert f'projects/{source_project}' in called_url
        assert f'/{target_project}/' in called_url
        print("\n✓ Mock: Cross-project linked work item retrieval works correctly")
    
    def test_get_linked_work_item_same_project(self, mock_linked_work_items_api):
        """Test retrieval of same-project linked work item (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "linkedworkitems",
                "id": "MyProject/WI-001/parent/MyProject/WI-002"
            }
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute with same project ID (internal link)
        project_id = "MyProject"
        
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id=project_id,
            work_item_id="WI-001",
            role_id="parent",
            target_project_id=project_id,
            linked_work_item_id="WI-002"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify project ID appears in correct positions
        call_args = mock_linked_work_items_api._session.get.call_args
        called_url = call_args[0][0]
        assert called_url.count(project_id) == 2  # Should appear twice
        print("\n✓ Mock: Same-project linked work item retrieval works correctly")
    
    def test_get_linked_work_item_with_attributes(self, mock_linked_work_items_api):
        """Test retrieval with full attributes structure (mocked)"""
        # Setup mock response with complete structure
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "linkedworkitems",
                "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId",
                "revision": "1234",
                "attributes": {
                    "revision": "1234",
                    "role": "parent",
                    "suspect": False
                },
                "relationships": {
                    "workItem": {
                        "data": {
                            "type": "workitems",
                            "id": "MyProjectId/MyLinkedWorkItemId",
                            "revision": "1234"
                        }
                    }
                }
            }
        }
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="MyLinkedWorkItemId"
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        
        # Verify structure
        assert 'data' in response_data
        assert 'attributes' in response_data['data']
        assert 'role' in response_data['data']['attributes']
        assert response_data['data']['attributes']['role'] == 'parent'
        assert 'suspect' in response_data['data']['attributes']
        assert 'relationships' in response_data['data']
        print("\n✓ Mock: Full attributes structure retrieved correctly")
    
    def test_get_linked_work_item_parameter_types(self, mock_linked_work_items_api):
        """Test that method accepts correct parameter types (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "linkedworkitems", "id": "test"}}
        mock_linked_work_items_api._session.get.return_value = mock_response
        
        # Test with string parameters (correct type)
        response = mock_linked_work_items_api.get_linked_work_item(
            project_id="PROJ1",
            work_item_id="WI1",
            role_id="parent",
            target_project_id="PROJ2",
            linked_work_item_id="WI2"
        )
        
        assert response.status_code == 200
        assert mock_linked_work_items_api._session.get.called
        print("\n✓ Mock: Method accepts string parameters correctly")
