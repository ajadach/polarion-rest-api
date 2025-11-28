"""
Pytest tests for patch_linked_work_item method in LinkedWorkItems class.

Tests the PATCH /projects/{projectId}/workitems/{workItemId}/linkedworkitems/{roleId}/{targetProjectId}/{linkedWorkItemId} endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_patch_linked_work_item.py -v
"""
import pytest
from unittest.mock import Mock


class TestPatchLinkedWorkItem:
    """Unit tests for patch_linked_work_item method using mocks"""
    
    def test_patch_linked_work_item_success_200(self, mock_linked_work_items_api):
        """Test successful update with 200 status code (mocked)"""
        # Setup mock response (PATCH typically returns 200 or 204)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute with data matching BODY from CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        role_id = "parent"
        target_project_id = "MyProjectId"
        linked_work_item_id = "MyLinkedWorkItemId"
        
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": f"{project_id}/{work_item_id}/{role_id}/{target_project_id}/{linked_work_item_id}",
                "attributes": {
                    "revision": "1234",
                    "suspect": True
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id=project_id,
            work_item_id=work_item_id,
            role_id=role_id,
            target_project_id=target_project_id,
            linked_work_item_id=linked_work_item_id,
            linked_item_data=linked_item_data
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify correct endpoint was called
        call_args = mock_linked_work_items_api._session.patch.call_args
        expected_url = f'https://test.polarion.com/polarion/rest/v1/projects/{project_id}/workitems/{work_item_id}/linkedworkitems/{role_id}/{target_project_id}/{linked_work_item_id}'
        assert call_args[0][0] == expected_url
        print("\n✓ Mock: Linked work item updated successfully with 200 status code")
    
    def test_patch_linked_work_item_success_204(self, mock_linked_work_items_api):
        """Test successful update with 204 status code (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": "Proj/WI1/parent/Proj/WI2",
                "attributes": {
                    "suspect": False
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id="Proj",
            work_item_id="WI1",
            role_id="parent",
            target_project_id="Proj",
            linked_work_item_id="WI2",
            linked_item_data=linked_item_data
        )
        
        # Assert
        assert response.status_code == 204
        print("\n✓ Mock: Linked work item updated successfully with 204 status code")
    
    def test_patch_linked_work_item_unauthorized_401(self, mock_linked_work_items_api):
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
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId",
                "attributes": {
                    "suspect": True
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="MyLinkedWorkItemId",
            linked_item_data=linked_item_data
        )
        
        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_patch_linked_work_item_bad_request_400(self, mock_linked_work_items_api):
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
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute with invalid data structure
        linked_item_data = {
            "data": "invalid_structure"  # Invalid structure
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="MyLinkedWorkItemId",
            linked_item_data=linked_item_data
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '400'
        assert response_data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in response_data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code with error details")
    
    def test_patch_linked_work_item_not_found_404(self, mock_linked_work_items_api):
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
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/NonExistent",
                "attributes": {
                    "suspect": True
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="NonExistent",
            linked_item_data=linked_item_data
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '404'
        print("\n✓ Mock: Not found returns 404 status code")
    
    def test_patch_linked_work_item_forbidden_403(self, mock_linked_work_items_api):
        """Test forbidden access with 403 status code (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You don't have permission to update this linked work item"
                }
            ]
        }
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": "RestrictedProject/RestrictedWI/parent/RestrictedProject/LinkedWI",
                "attributes": {
                    "suspect": True
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id="RestrictedProject",
            work_item_id="RestrictedWI",
            role_id="parent",
            target_project_id="RestrictedProject",
            linked_work_item_id="LinkedWI",
            linked_item_data=linked_item_data
        )
        
        # Assert
        assert response.status_code == 403
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '403'
        print("\n✓ Mock: Forbidden access returns 403 status code")
    
    def test_patch_linked_work_item_endpoint_structure(self, mock_linked_work_items_api):
        """Test that the correct endpoint structure is used (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute
        project_id = "TEST_PROJ"
        work_item_id = "WI-123"
        role_id = "relates_to"
        target_project_id = "TARGET_PROJ"
        linked_work_item_id = "WI-456"
        
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": f"{project_id}/{work_item_id}/{role_id}/{target_project_id}/{linked_work_item_id}",
                "attributes": {
                    "suspect": False
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id=project_id,
            work_item_id=work_item_id,
            role_id=role_id,
            target_project_id=target_project_id,
            linked_work_item_id=linked_work_item_id,
            linked_item_data=linked_item_data
        )
        
        # Verify the endpoint structure
        call_args = mock_linked_work_items_api._session.patch.call_args
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
    
    def test_patch_linked_work_item_update_suspect_flag(self, mock_linked_work_items_api):
        """Test updating suspect flag (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute - update suspect flag to True
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": "Proj/WI1/parent/Proj/WI2",
                "attributes": {
                    "suspect": True
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id="Proj",
            work_item_id="WI1",
            role_id="parent",
            target_project_id="Proj",
            linked_work_item_id="WI2",
            linked_item_data=linked_item_data
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify suspect flag was sent in body
        call_args = mock_linked_work_items_api._session.patch.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        assert 'json' in call_kwargs
        assert call_kwargs['json']['data']['attributes']['suspect'] == True
        print("\n✓ Mock: Suspect flag updated correctly")
    
    def test_patch_linked_work_item_with_revision(self, mock_linked_work_items_api):
        """Test updating with revision in attributes (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute with revision
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": "Proj/WI1/parent/Proj/WI2",
                "attributes": {
                    "revision": "1234",
                    "suspect": True
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id="Proj",
            work_item_id="WI1",
            role_id="parent",
            target_project_id="Proj",
            linked_work_item_id="WI2",
            linked_item_data=linked_item_data
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify revision was sent in body
        call_args = mock_linked_work_items_api._session.patch.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        assert call_kwargs['json']['data']['attributes']['revision'] == '1234'
        print("\n✓ Mock: Revision attribute handled correctly")
    
    def test_patch_linked_work_item_body_structure(self, mock_linked_work_items_api):
        """Test that the correct body structure is sent (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId",
                "attributes": {
                    "revision": "1234",
                    "suspect": True
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="MyLinkedWorkItemId",
            linked_item_data=linked_item_data
        )
        
        # Verify the body structure
        call_args = mock_linked_work_items_api._session.patch.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        
        assert 'json' in call_kwargs
        body = call_kwargs['json']
        assert 'data' in body
        assert body['data']['type'] == 'linkedworkitems'
        assert 'id' in body['data']
        assert 'attributes' in body['data']
        print("\n✓ Mock: Request body structure is correct")
    
    def test_patch_linked_work_item_cross_project(self, mock_linked_work_items_api):
        """Test updating cross-project linked work item (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute with cross-project link
        source_project = "ProjectA"
        target_project = "ProjectB"
        
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": f"{source_project}/WI-A-001/relates_to/{target_project}/WI-B-001",
                "attributes": {
                    "suspect": False
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id=source_project,
            work_item_id="WI-A-001",
            role_id="relates_to",
            target_project_id=target_project,
            linked_work_item_id="WI-B-001",
            linked_item_data=linked_item_data
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify both projects are in the URL
        call_args = mock_linked_work_items_api._session.patch.call_args
        called_url = call_args[0][0]
        assert f'projects/{source_project}' in called_url
        assert f'/{target_project}/' in called_url
        print("\n✓ Mock: Cross-project linked work item update works correctly")
    
    def test_patch_linked_work_item_different_roles(self, mock_linked_work_items_api):
        """Test updating with different role types (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Test different role types
        test_roles = ["parent", "child", "relates_to", "duplicates", "depends_on"]
        
        for role_id in test_roles:
            linked_item_data = {
                "data": {
                    "type": "linkedworkitems",
                    "id": f"Proj/WI1/{role_id}/Proj/WI2",
                    "attributes": {
                        "suspect": False
                    }
                }
            }
            
            response = mock_linked_work_items_api.patch_linked_work_item(
                project_id="Proj",
                work_item_id="WI1",
                role_id=role_id,
                target_project_id="Proj",
                linked_work_item_id="WI2",
                linked_item_data=linked_item_data
            )
            
            assert response.status_code == 200
            
            # Verify role is in the URL
            call_args = mock_linked_work_items_api._session.patch.call_args
            called_url = call_args[0][0]
            assert f'linkedworkitems/{role_id}/' in called_url
        
        print(f"\n✓ Mock: Tested {len(test_roles)} different role types successfully")
    
    def test_patch_linked_work_item_id_format_in_body(self, mock_linked_work_items_api):
        """Test that the ID format in body follows the correct pattern (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute with correctly formatted ID
        # Format: {projectId}/{workItemId}/{roleId}/{targetProjectId}/{linkedWorkItemId}
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId",
                "attributes": {
                    "suspect": True
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            role_id="parent",
            target_project_id="MyProjectId",
            linked_work_item_id="MyLinkedWorkItemId",
            linked_item_data=linked_item_data
        )
        
        # Verify the ID format has 5 segments separated by slashes
        call_args = mock_linked_work_items_api._session.patch.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        item_id = call_kwargs['json']['data']['id']
        id_segments = item_id.split('/')
        assert len(id_segments) == 5, f"Expected 5 segments in ID, got {len(id_segments)}"
        print("\n✓ Mock: Linked work item ID follows correct format (5 segments)")
    
    def test_patch_linked_work_item_minimal_attributes(self, mock_linked_work_items_api):
        """Test updating with minimal attributes (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_linked_work_items_api._session.patch.return_value = mock_response
        
        # Execute with only suspect attribute
        linked_item_data = {
            "data": {
                "type": "linkedworkitems",
                "id": "Proj/WI1/parent/Proj/WI2",
                "attributes": {
                    "suspect": False
                }
            }
        }
        
        response = mock_linked_work_items_api.patch_linked_work_item(
            project_id="Proj",
            work_item_id="WI1",
            role_id="parent",
            target_project_id="Proj",
            linked_work_item_id="WI2",
            linked_item_data=linked_item_data
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify minimal attributes were sent
        call_args = mock_linked_work_items_api._session.patch.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        attributes = call_kwargs['json']['data']['attributes']
        assert 'suspect' in attributes
        assert len(attributes) == 1  # Only suspect attribute
        print("\n✓ Mock: Minimal attributes handled correctly")
