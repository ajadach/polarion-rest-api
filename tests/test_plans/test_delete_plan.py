"""
Tests for Plans.delete_plan method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestDeletePlan:
    """Test suite for delete_plan method"""
    
    def test_delete_plan_success(self, mock_plans_api):
        """Test successful deletion of a single plan"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = ""
        
        mock_plans_api._session.delete.return_value = mock_response
        
        # Call the method
        response = mock_plans_api.delete_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify the call
        mock_plans_api._session.delete.assert_called_once()
        call_args = mock_plans_api._session.delete.call_args
        
        # Check URL
        assert 'projects/MyProjectId/plans/MyPlanId' in call_args[0][0]
        
        # Verify response
        assert response.status_code == 200
    
    def test_delete_plan_url_structure(self, mock_plans_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        response = mock_plans_api.delete_plan(
            project_id='TEST_PROJ',
            plan_id='TEST_PLAN'
        )
        
        # Verify URL structure
        call_args = mock_plans_api._session.delete.call_args
        url = call_args[0][0]
        
        assert 'projects/TEST_PROJ' in url
        assert 'plans/TEST_PLAN' in url
        assert response.status_code == 200
    
    def test_delete_plan_error_400(self, mock_plans_api):
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
        
        response = mock_plans_api.delete_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
        assert 'Unexpected token' in errors[0]['detail']
    
    def test_delete_plan_error_401(self, mock_plans_api):
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
        
        response = mock_plans_api.delete_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
        assert errors[0]['detail'] == 'No access token'
    
    def test_delete_plan_with_special_characters(self, mock_plans_api):
        """Test deleting plan with special characters in ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        response = mock_plans_api.delete_plan(
            project_id='My-Project',
            plan_id='Plan-2023 (v1)'
        )
        
        mock_plans_api._session.delete.assert_called_once()
        assert response.status_code == 200
    
    def test_delete_plan_no_body(self, mock_plans_api):
        """Test that delete_plan does not send a body"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        response = mock_plans_api.delete_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify no json/data body is sent
        call_args = mock_plans_api._session.delete.call_args
        assert 'json' not in call_args[1] or call_args[1].get('json') is None
        assert 'data' not in call_args[1] or call_args[1].get('data') is None
        assert response.status_code == 200
    
    def test_delete_plan_numeric_plan_id(self, mock_plans_api):
        """Test deleting plan with numeric ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        response = mock_plans_api.delete_plan(
            project_id='MyProjectId',
            plan_id='12345'
        )
        
        call_args = mock_plans_api._session.delete.call_args
        assert 'plans/12345' in call_args[0][0]
        assert response.status_code == 200
    
    def test_delete_plan_alphanumeric_plan_id(self, mock_plans_api):
        """Test deleting plan with alphanumeric ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        response = mock_plans_api.delete_plan(
            project_id='ProjectAlpha',
            plan_id='Plan-ABC-123'
        )
        
        call_args = mock_plans_api._session.delete.call_args
        assert 'ProjectAlpha' in call_args[0][0]
        assert 'Plan-ABC-123' in call_args[0][0]
        assert response.status_code == 200
    
    def test_delete_plan_long_plan_id(self, mock_plans_api):
        """Test deleting plan with very long ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        long_plan_id = 'Plan' + 'X' * 200
        
        response = mock_plans_api.delete_plan(
            project_id='MyProjectId',
            plan_id=long_plan_id
        )
        
        call_args = mock_plans_api._session.delete.call_args
        assert long_plan_id in call_args[0][0]
        assert response.status_code == 200
    
    def test_delete_plan_case_sensitive_ids(self, mock_plans_api):
        """Test that plan IDs are case-sensitive"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        response = mock_plans_api.delete_plan(
            project_id='MyProject',
            plan_id='MyPlan'
        )
        
        # Verify exact case is preserved
        call_args = mock_plans_api._session.delete.call_args
        url = call_args[0][0]
        assert 'MyProject' in url
        assert 'MyPlan' in url
        assert 'myproject' not in url.lower() or 'MyProject' in url
        assert response.status_code == 200
    
    def test_delete_plan_with_underscores(self, mock_plans_api):
        """Test deleting plan with underscores in ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        response = mock_plans_api.delete_plan(
            project_id='my_project',
            plan_id='my_plan_id'
        )
        
        call_args = mock_plans_api._session.delete.call_args
        assert 'my_project' in call_args[0][0]
        assert 'my_plan_id' in call_args[0][0]
        assert response.status_code == 200
    
    def test_delete_plan_with_dots(self, mock_plans_api):
        """Test deleting plan with dots in ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        response = mock_plans_api.delete_plan(
            project_id='project.v1',
            plan_id='plan.2023.q4'
        )
        
        call_args = mock_plans_api._session.delete.call_args
        assert 'project.v1' in call_args[0][0]
        assert 'plan.2023.q4' in call_args[0][0]
        assert response.status_code == 200
    
    def test_delete_plan_method_type(self, mock_plans_api):
        """Test that correct HTTP method is used"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        response = mock_plans_api.delete_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify DELETE method was called (not POST, PATCH, etc.)
        mock_plans_api._session.delete.assert_called_once()
        assert response.status_code == 200
    
    def test_delete_plan_path_parameters_order(self, mock_plans_api):
        """Test that path parameters are in correct order"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_plans_api._session.delete.return_value = mock_response
        
        response = mock_plans_api.delete_plan(
            project_id='ProjectA',
            plan_id='PlanB'
        )
        
        # Verify correct order: projects/{project_id}/plans/{plan_id}
        call_args = mock_plans_api._session.delete.call_args
        url = call_args[0][0]
        
        project_pos = url.find('ProjectA')
        plan_pos = url.find('PlanB')
        assert project_pos < plan_pos, "Project ID should come before Plan ID in URL"
        assert response.status_code == 200
    
    def test_delete_plan_empty_response(self, mock_plans_api):
        """Test that successful deletion may return empty response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = ""
        mock_response.content = b""
        
        mock_plans_api._session.delete.return_value = mock_response
        
        response = mock_plans_api.delete_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Empty response is valid for DELETE operations
        assert response.status_code == 200
        assert response.text == ""
