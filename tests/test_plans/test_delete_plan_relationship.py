"""
Tests for Plans.delete_plan_relationship method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestDeletePlanRelationship:
    """Test suite for delete_plan_relationship method"""
    
    def test_delete_plan_relationship_success(self, mock_plans_api):
        """Test successful deletion of plan relationship"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = ""
        
        mock_plans_api._session.delete.return_value = mock_response
        
        # Prepare request data based on BODY example
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/MyResourceId"
                }
            ]
        }
        
        # Call the method
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='relationshipId',
            relationship_data=relationship_data
        )
        
        # Verify the call
        mock_plans_api._session.delete.assert_called_once()
        call_args = mock_plans_api._session.delete.call_args
        
        # Check URL
        assert 'projects/MyProjectId/plans/MyPlanId/relationships/relationshipId' in call_args[0][0]
        
        # Verify json parameter was passed
        assert call_args[1]['json'] == relationship_data
        
        # Verify response
        assert response.status_code == 200
    
    def test_delete_plan_relationship_single_item(self, mock_plans_api):
        """Test deleting a single relationship item"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "TestProject/Resource001"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='TestProject',
            plan_id='TestPlan',
            relationship_id='testRelationship',
            relationship_data=relationship_data
        )
        
        # Verify call
        call_args = mock_plans_api._session.delete.call_args
        assert len(call_args[1]['json']['data']) == 1
        assert call_args[1]['json']['data'][0]['type'] == 'collections'
        assert response.status_code == 200
    
    def test_delete_plan_relationship_multiple_items(self, mock_plans_api):
        """Test deleting multiple relationship items at once"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/Resource001"
                },
                {
                    "type": "collections",
                    "id": "MyProjectId/Resource002"
                },
                {
                    "type": "collections",
                    "id": "MyProjectId/Resource003"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='myRelationship',
            relationship_data=relationship_data
        )
        
        # Verify multiple items were sent
        call_args = mock_plans_api._session.delete.call_args
        assert len(call_args[1]['json']['data']) == 3
        assert response.status_code == 200
    
    def test_delete_plan_relationship_error_400(self, mock_plans_api):
        """Test handling of 400 Bad Request error"""
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
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/MyResourceId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='relationshipId',
            relationship_data=relationship_data
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
        assert 'Unexpected token' in errors[0]['detail']
    
    def test_delete_plan_relationship_error_401(self, mock_plans_api):
        """Test handling of 401 Unauthorized error"""
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
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/MyResourceId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='relationshipId',
            relationship_data=relationship_data
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
        assert errors[0]['detail'] == 'No access token'
    
    def test_delete_plan_relationship_url_structure(self, mock_plans_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "TEST_PROJ/TEST_RES"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='TEST_PROJ',
            plan_id='TEST_PLAN',
            relationship_id='TEST_REL',
            relationship_data=relationship_data
        )
        
        # Verify URL structure
        call_args = mock_plans_api._session.delete.call_args
        url = call_args[0][0]
        
        assert 'projects/TEST_PROJ' in url
        assert 'plans/TEST_PLAN' in url
        assert 'relationships/TEST_REL' in url
        assert response.status_code == 200
    
    def test_delete_plan_relationship_data_structure(self, mock_plans_api):
        """Test that request data has proper structure"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/MyResourceId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='relationshipId',
            relationship_data=relationship_data
        )
        
        # Verify data structure
        call_args = mock_plans_api._session.delete.call_args
        sent_data = call_args[1]['json']
        
        assert 'data' in sent_data
        assert isinstance(sent_data['data'], list)
        assert 'type' in sent_data['data'][0]
        assert 'id' in sent_data['data'][0]
        assert response.status_code == 200
    
    def test_delete_plan_relationship_with_special_characters(self, mock_plans_api):
        """Test deleting relationship with special characters in IDs"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "My-Project/Resource-2023 (v1)"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='My-Project',
            plan_id='Plan-2023',
            relationship_id='rel-id-001',
            relationship_data=relationship_data
        )
        
        mock_plans_api._session.delete.assert_called_once()
        assert response.status_code == 200
    
    def test_delete_plan_relationship_type_validation(self, mock_plans_api):
        """Test that type field is properly handled"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/MyResourceId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='relationshipId',
            relationship_data=relationship_data
        )
        
        # Verify type is preserved
        call_args = mock_plans_api._session.delete.call_args
        assert call_args[1]['json']['data'][0]['type'] == 'collections'
        assert response.status_code == 200
    
    def test_delete_plan_relationship_empty_list(self, mock_plans_api):
        """Test deleting with empty relationship list"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": []
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='relationshipId',
            relationship_data=relationship_data
        )
        
        # Verify empty list was sent
        call_args = mock_plans_api._session.delete.call_args
        assert len(call_args[1]['json']['data']) == 0
        assert response.status_code == 200
    
    def test_delete_plan_relationship_json_content_type(self, mock_plans_api):
        """Test that request uses JSON content type"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/MyResourceId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='relationshipId',
            relationship_data=relationship_data
        )
        
        # Verify json parameter is used
        call_args = mock_plans_api._session.delete.call_args
        assert 'json' in call_args[1]
        assert response.status_code == 200
    
    def test_delete_plan_relationship_path_order(self, mock_plans_api):
        """Test that path parameters are in correct order"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "ProjectA/ResourceX"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='ProjectA',
            plan_id='PlanB',
            relationship_id='RelC',
            relationship_data=relationship_data
        )
        
        # Verify correct order: projects/{project_id}/plans/{plan_id}/relationships/{relationship_id}
        call_args = mock_plans_api._session.delete.call_args
        url = call_args[0][0]
        
        project_pos = url.find('ProjectA')
        plan_pos = url.find('PlanB')
        rel_pos = url.find('RelC')
        
        assert project_pos < plan_pos < rel_pos, "URL parameters should be in correct order"
        assert response.status_code == 200
    
    def test_delete_plan_relationship_different_types(self, mock_plans_api):
        """Test deleting relationships with different resource types"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/WorkItem001"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='relationshipId',
            relationship_data=relationship_data
        )
        
        # Verify different type is handled
        call_args = mock_plans_api._session.delete.call_args
        assert call_args[1]['json']['data'][0]['type'] == 'workitems'
        assert response.status_code == 200
    
    def test_delete_plan_relationship_method_uses_delete_with_body(self, mock_plans_api):
        """Test that delete_plan_relationship uses DELETE method with body"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/MyResourceId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='relationshipId',
            relationship_data=relationship_data
        )
        
        # Verify DELETE method was called with json body
        mock_plans_api._session.delete.assert_called_once()
        call_args = mock_plans_api._session.delete.call_args
        assert 'json' in call_args[1]
        assert call_args[1]['json'] is not None
        assert response.status_code == 200
    
    def test_delete_plan_relationship_id_format(self, mock_plans_api):
        """Test that resource IDs follow the correct format"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        relationship_data = {
            "data": [
                {
                    "type": "collections",
                    "id": "MyProjectId/MyResourceId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='relationshipId',
            relationship_data=relationship_data
        )
        
        # Verify ID format (ProjectId/ResourceId)
        call_args = mock_plans_api._session.delete.call_args
        resource_id = call_args[1]['json']['data'][0]['id']
        assert '/' in resource_id
        assert resource_id.startswith('MyProjectId/')
        assert response.status_code == 200
    
    def test_delete_plan_relationship_large_batch(self, mock_plans_api):
        """Test deleting a large batch of relationships"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        # Create 30 relationships for deletion
        relationships_list = [
            {
                "type": "collections",
                "id": f"MyProjectId/Resource{i:03d}"
            }
            for i in range(30)
        ]
        
        relationship_data = {
            "data": relationships_list
        }
        
        response = mock_plans_api.delete_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='relationshipId',
            relationship_data=relationship_data
        )
        
        # Verify all relationships were sent
        call_args = mock_plans_api._session.delete.call_args
        assert len(call_args[1]['json']['data']) == 30
        assert response.status_code == 200
