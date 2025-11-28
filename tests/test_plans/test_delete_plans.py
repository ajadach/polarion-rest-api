"""
Tests for Plans.delete_plans method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestDeletePlans:
    """Test suite for delete_plans method"""
    
    def test_delete_plans_success(self, mock_plans_api):
        """Test successful deletion of plans"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = ""
        
        mock_plans_api._session.delete.return_value = mock_response
        
        # Prepare request data based on BODY example
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId"
                }
            ]
        }
        
        # Call the method
        response = mock_plans_api.delete_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify the call
        mock_plans_api._session.delete.assert_called_once()
        call_args = mock_plans_api._session.delete.call_args
        
        # Check URL
        assert 'projects/MyProjectId/plans' in call_args[0][0]
        
        # Verify json parameter was passed
        assert call_args[1]['json'] == plans_data
        
        # Verify response
        assert response.status_code == 200
    
    def test_delete_plans_single_plan(self, mock_plans_api):
        """Test deleting a single plan"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "TestProject/TestPlan001"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='TestProject',
            plans_data=plans_data
        )
        
        # Verify call
        call_args = mock_plans_api._session.delete.call_args
        assert len(call_args[1]['json']['data']) == 1
        assert call_args[1]['json']['data'][0]['id'] == 'TestProject/TestPlan001'
        assert response.status_code == 200
    
    def test_delete_plans_multiple_plans(self, mock_plans_api):
        """Test deleting multiple plans at once"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/Plan001"
                },
                {
                    "type": "plans",
                    "id": "MyProjectId/Plan002"
                },
                {
                    "type": "plans",
                    "id": "MyProjectId/Plan003"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify multiple plans were sent
        call_args = mock_plans_api._session.delete.call_args
        assert len(call_args[1]['json']['data']) == 3
        assert response.status_code == 200
    
    def test_delete_plans_error_400(self, mock_plans_api):
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
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
        assert 'Unexpected token' in errors[0]['detail']
    
    def test_delete_plans_error_401(self, mock_plans_api):
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
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
        assert errors[0]['detail'] == 'No access token'
    
    def test_delete_plans_data_structure(self, mock_plans_api):
        """Test that request data has proper structure"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify data structure
        call_args = mock_plans_api._session.delete.call_args
        sent_data = call_args[1]['json']
        
        assert 'data' in sent_data
        assert isinstance(sent_data['data'], list)
        assert sent_data['data'][0]['type'] == 'plans'
        assert 'id' in sent_data['data'][0]
        assert response.status_code == 200
    
    def test_delete_plans_url_structure(self, mock_plans_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "TEST_PROJ/TEST_PLAN"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='TEST_PROJ',
            plans_data=plans_data
        )
        
        # Verify URL structure
        call_args = mock_plans_api._session.delete.call_args
        url = call_args[0][0]
        
        assert 'projects/TEST_PROJ' in url
        assert url.endswith('/plans')
        assert response.status_code == 200
    
    def test_delete_plans_with_special_characters(self, mock_plans_api):
        """Test deleting plans with special characters in IDs"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "My-Project/Plan-2023 (v1)"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='My-Project',
            plans_data=plans_data
        )
        
        mock_plans_api._session.delete.assert_called_once()
        assert response.status_code == 200
    
    def test_delete_plans_type_validation(self, mock_plans_api):
        """Test that type field is always 'plans'"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify type is plans
        call_args = mock_plans_api._session.delete.call_args
        for item in call_args[1]['json']['data']:
            assert item['type'] == 'plans'
        assert response.status_code == 200
    
    def test_delete_plans_empty_list(self, mock_plans_api):
        """Test deleting with empty plans list"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        plans_data = {
            "data": []
        }
        
        response = mock_plans_api.delete_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify empty list was sent
        call_args = mock_plans_api._session.delete.call_args
        assert len(call_args[1]['json']['data']) == 0
        assert response.status_code == 200
    
    def test_delete_plans_cross_project_plans(self, mock_plans_api):
        """Test deleting plans from different projects (if allowed)"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "ProjectA/Plan001"
                },
                {
                    "type": "plans",
                    "id": "ProjectA/Plan002"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='ProjectA',
            plans_data=plans_data
        )
        
        assert response.status_code == 200
    
    def test_delete_plans_json_content_type(self, mock_plans_api):
        """Test that request uses JSON content type"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify json parameter is used
        call_args = mock_plans_api._session.delete.call_args
        assert 'json' in call_args[1]
        assert response.status_code == 200
    
    def test_delete_plans_id_format(self, mock_plans_api):
        """Test that plan IDs follow the correct format"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify ID format (ProjectId/PlanId)
        call_args = mock_plans_api._session.delete.call_args
        plan_id = call_args[1]['json']['data'][0]['id']
        assert '/' in plan_id
        assert plan_id.startswith('MyProjectId/')
        assert response.status_code == 200
    
    def test_delete_plans_large_batch(self, mock_plans_api):
        """Test deleting a large batch of plans"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        # Create 50 plans for deletion
        plans_list = [
            {
                "type": "plans",
                "id": f"MyProjectId/Plan{i:03d}"
            }
            for i in range(50)
        ]
        
        plans_data = {
            "data": plans_list
        }
        
        response = mock_plans_api.delete_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify all plans were sent
        call_args = mock_plans_api._session.delete.call_args
        assert len(call_args[1]['json']['data']) == 50
        assert response.status_code == 200
    
    def test_delete_plans_method_uses_delete_with_body(self, mock_plans_api):
        """Test that delete_plans uses DELETE method with body"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId"
                }
            ]
        }
        
        response = mock_plans_api.delete_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify DELETE method was called with json body
        mock_plans_api._session.delete.assert_called_once()
        call_args = mock_plans_api._session.delete.call_args
        assert 'json' in call_args[1]
        assert call_args[1]['json'] is not None
        assert response.status_code == 200
