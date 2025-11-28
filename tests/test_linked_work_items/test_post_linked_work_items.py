"""
Pytest tests for post_linked_work_items method in LinkedWorkItems class.

Tests the POST /projects/{projectId}/workitems/{workItemId}/linkedworkitems endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_post_linked_work_items.py -v
"""
import pytest
from unittest.mock import Mock


class TestPostLinkedWorkItems:
    """Unit tests for post_linked_work_items method using mocks"""
    
    def test_post_linked_work_items_success_200(self, mock_linked_work_items_api):
        """Test successful creation with 200 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 200 status code
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId",
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/linkedworkitems/parent/MyProjectId/MyLinkedWorkItemId?revision=1234"
                    }
                }
            ]
        }
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute with data matching BODY from CURL
        project_id = "MyProjectId"
        work_item_id = "MyWorkItemId"
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {
                        "revision": "1234",
                        "role": "relates_to",
                        "suspect": True
                    },
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "MyProjectId/MyWorkItemId"
                            }
                        }
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert 'data' in response_data
        assert len(response_data['data']) == 1
        assert response_data['data'][0]['type'] == 'linkedworkitems'
        assert 'id' in response_data['data'][0]
        
        # Verify correct endpoint was called
        call_args = mock_linked_work_items_api._session.post.call_args
        expected_url = f'https://test.polarion.com/polarion/rest/v1/projects/{project_id}/workitems/{work_item_id}/linkedworkitems'
        assert call_args[0][0] == expected_url
        print("\n✓ Mock: Linked work items created successfully with 200 status code")
    
    def test_post_linked_work_items_success_201(self, mock_linked_work_items_api):
        """Test successful creation with 201 status code (mocked)"""
        # Setup mock response (POST typically returns 201 Created)
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "Proj/WI1/parent/Proj/WI2"
                }
            ]
        }
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {
                        "role": "parent"
                    },
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "Proj/WI2"
                            }
                        }
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id="Proj",
            work_item_id="WI1",
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 201
        print("\n✓ Mock: Linked work items created successfully with 201 status code")
    
    def test_post_linked_work_items_unauthorized_401(self, mock_linked_work_items_api):
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
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {
                        "role": "relates_to"
                    },
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "MyProjectId/MyWorkItemId"
                            }
                        }
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
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
    
    def test_post_linked_work_items_bad_request_400(self, mock_linked_work_items_api):
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
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute with invalid data structure
        linked_items_data = {
            "data": "invalid_structure"  # Invalid: should be array
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
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
    
    def test_post_linked_work_items_multiple_items(self, mock_linked_work_items_api):
        """Test creation of multiple linked work items (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "Proj/WI1/parent/Proj/WI2"
                },
                {
                    "type": "linkedworkitems",
                    "id": "Proj/WI1/relates_to/Proj/WI3"
                },
                {
                    "type": "linkedworkitems",
                    "id": "Proj/WI1/depends_on/OtherProj/WI4"
                }
            ]
        }
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute with multiple items
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {"role": "parent"},
                    "relationships": {
                        "workItem": {"data": {"type": "workitems", "id": "Proj/WI2"}}
                    }
                },
                {
                    "type": "linkedworkitems",
                    "attributes": {"role": "relates_to"},
                    "relationships": {
                        "workItem": {"data": {"type": "workitems", "id": "Proj/WI3"}}
                    }
                },
                {
                    "type": "linkedworkitems",
                    "attributes": {"role": "depends_on"},
                    "relationships": {
                        "workItem": {"data": {"type": "workitems", "id": "OtherProj/WI4"}}
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id="Proj",
            work_item_id="WI1",
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data['data']) == 3
        
        # Verify JSON body was sent
        call_args = mock_linked_work_items_api._session.post.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        assert 'json' in call_kwargs
        assert len(call_kwargs['json']['data']) == 3
        print("\n✓ Mock: Multiple linked work items created successfully")
    
    def test_post_linked_work_items_single_item(self, mock_linked_work_items_api):
        """Test creation of a single linked work item (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/MyProjectId/MyLinkedWorkItemId"
                }
            ]
        }
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute with single item in array
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {
                        "role": "parent",
                        "suspect": False
                    },
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "MyProjectId/MyLinkedWorkItemId"
                            }
                        }
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data['data']) == 1
        print("\n✓ Mock: Single linked work item created successfully")
    
    def test_post_linked_work_items_endpoint_structure(self, mock_linked_work_items_api):
        """Test that the correct endpoint structure is used (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "TEST_PROJ"
        work_item_id = "WI-123"
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {"role": "parent"},
                    "relationships": {
                        "workItem": {"data": {"type": "workitems", "id": "TEST_PROJ/WI-456"}}
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id=project_id,
            work_item_id=work_item_id,
            linked_items_data=linked_items_data
        )
        
        # Verify the endpoint structure
        call_args = mock_linked_work_items_api._session.post.call_args
        called_url = call_args[0][0]
        
        # Check endpoint components
        assert f'projects/{project_id}' in called_url
        assert f'workitems/{work_item_id}' in called_url
        assert 'linkedworkitems' in called_url
        
        # Verify complete URL structure (no extra path parameters)
        expected_path = f'projects/{project_id}/workitems/{work_item_id}/linkedworkitems'
        assert expected_path in called_url
        print("\n✓ Mock: Endpoint structure is correct")
    
    def test_post_linked_work_items_with_all_attributes(self, mock_linked_work_items_api):
        """Test creation with all attributes (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"type": "linkedworkitems", "id": "test"}]}
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute with all attributes from CURL example
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {
                        "revision": "1234",
                        "role": "relates_to",
                        "suspect": True
                    },
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "MyProjectId/MyWorkItemId"
                            }
                        }
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify all attributes were sent
        call_args = mock_linked_work_items_api._session.post.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        attributes = call_kwargs['json']['data'][0]['attributes']
        assert 'revision' in attributes
        assert 'role' in attributes
        assert 'suspect' in attributes
        print("\n✓ Mock: All attributes handled correctly")
    
    def test_post_linked_work_items_body_structure(self, mock_linked_work_items_api):
        """Test that the correct body structure is sent (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {
                        "role": "parent",
                        "suspect": True
                    },
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "MyProjectId/MyLinkedWorkItemId"
                            }
                        }
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            linked_items_data=linked_items_data
        )
        
        # Verify the body structure
        call_args = mock_linked_work_items_api._session.post.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        
        assert 'json' in call_kwargs
        body = call_kwargs['json']
        assert 'data' in body
        assert isinstance(body['data'], list)
        assert len(body['data']) >= 1
        assert body['data'][0]['type'] == 'linkedworkitems'
        assert 'attributes' in body['data'][0]
        assert 'relationships' in body['data'][0]
        print("\n✓ Mock: Request body structure is correct")
    
    def test_post_linked_work_items_different_roles(self, mock_linked_work_items_api):
        """Test creation with different role types (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"type": "linkedworkitems", "id": "test"}]}
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Test different role types
        test_roles = ["parent", "child", "relates_to", "duplicates", "depends_on"]
        
        for role in test_roles:
            linked_items_data = {
                "data": [
                    {
                        "type": "linkedworkitems",
                        "attributes": {"role": role},
                        "relationships": {
                            "workItem": {"data": {"type": "workitems", "id": "Proj/WI2"}}
                        }
                    }
                ]
            }
            
            response = mock_linked_work_items_api.post_linked_work_items(
                project_id="Proj",
                work_item_id="WI1",
                linked_items_data=linked_items_data
            )
            
            assert response.status_code == 200
            
            # Verify role is in the body
            call_args = mock_linked_work_items_api._session.post.call_args
            call_kwargs = call_args[1] if len(call_args) > 1 else {}
            assert call_kwargs['json']['data'][0]['attributes']['role'] == role
        
        print(f"\n✓ Mock: Tested {len(test_roles)} different role types")
    
    def test_post_linked_work_items_cross_project(self, mock_linked_work_items_api):
        """Test creation of cross-project linked work items (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "id": "ProjectA/WI-A-001/relates_to/ProjectB/WI-B-001"
                }
            ]
        }
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute with cross-project link
        source_project = "ProjectA"
        target_project = "ProjectB"
        
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {"role": "relates_to"},
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": f"{target_project}/WI-B-001"
                            }
                        }
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id=source_project,
            work_item_id="WI-A-001",
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify target project is in the body
        call_args = mock_linked_work_items_api._session.post.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        work_item_id = call_kwargs['json']['data'][0]['relationships']['workItem']['data']['id']
        assert target_project in work_item_id
        print("\n✓ Mock: Cross-project linked work items creation works correctly")
    
    def test_post_linked_work_items_with_suspect_flag(self, mock_linked_work_items_api):
        """Test creation with suspect flag (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"type": "linkedworkitems", "id": "test"}]}
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute with suspect flag
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {
                        "role": "parent",
                        "suspect": True
                    },
                    "relationships": {
                        "workItem": {"data": {"type": "workitems", "id": "Proj/WI2"}}
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id="Proj",
            work_item_id="WI1",
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify suspect flag was sent
        call_args = mock_linked_work_items_api._session.post.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        assert call_kwargs['json']['data'][0]['attributes']['suspect'] == True
        print("\n✓ Mock: Suspect flag handled correctly")
    
    def test_post_linked_work_items_relationships_structure(self, mock_linked_work_items_api):
        """Test that relationships structure is correct (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {"role": "parent"},
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "MyProjectId/MyLinkedWorkItemId"
                            }
                        }
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            linked_items_data=linked_items_data
        )
        
        # Verify relationships structure
        call_args = mock_linked_work_items_api._session.post.call_args
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        
        relationships = call_kwargs['json']['data'][0]['relationships']
        assert 'workItem' in relationships
        assert 'data' in relationships['workItem']
        assert relationships['workItem']['data']['type'] == 'workitems'
        assert 'id' in relationships['workItem']['data']
        print("\n✓ Mock: Relationships structure is correct")
    
    def test_post_linked_work_items_forbidden_403(self, mock_linked_work_items_api):
        """Test forbidden access with 403 status code (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You don't have permission to create linked work items"
                }
            ]
        }
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute
        linked_items_data = {
            "data": [
                {
                    "type": "linkedworkitems",
                    "attributes": {"role": "parent"},
                    "relationships": {
                        "workItem": {"data": {"type": "workitems", "id": "RestrictedProject/WI"}}
                    }
                }
            ]
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id="RestrictedProject",
            work_item_id="RestrictedWI",
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 403
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '403'
        print("\n✓ Mock: Forbidden access returns 403 status code")
    
    def test_post_linked_work_items_empty_data_array(self, mock_linked_work_items_api):
        """Test creation with empty data array (mocked)"""
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
        mock_linked_work_items_api._session.post.return_value = mock_response
        
        # Execute with empty data array
        linked_items_data = {
            "data": []
        }
        
        response = mock_linked_work_items_api.post_linked_work_items(
            project_id="MyProjectId",
            work_item_id="MyWorkItemId",
            linked_items_data=linked_items_data
        )
        
        # Assert
        assert response.status_code == 400
        print("\n✓ Mock: Empty data array returns 400 status code")
