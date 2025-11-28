"""
Pytest tests for get_project_test_parameter_definition method.

Tests the get_project_test_parameter_definition method from Projects class.
Uses mocked API responses for reliable and fast testing.

Run with:
    pytest test_get_project_test_parameter_definition.py -v
"""
import pytest
from unittest.mock import Mock


# ============================================================================
# Mocked Tests
# ============================================================================

class TestGetProjectTestParameterDefinitionMocked:
    """Mocked tests for single project test parameter definition"""
    
    def test_get_project_test_parameter_definition_success(self, mock_projects_api):
        """Test getting a single test parameter definition successfully"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameter_definitions",
                "id": "MyProjectId/MyTestParamDefinition",
                "revision": "1234",
                "attributes": {
                    "name": "Test Parameter Definition example",
                    "type": "string",
                    "description": "Example test parameter"
                },
                "links": {
                    "self": "server-host-name/application-path/projects/MyProjectId/testparameterdefinitions/MyTestParamDefinition"
                }
            },
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/testparameterdefinitions/MyTestParamDefinition"
            }
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definition(
            "MyProjectId", 
            "MyTestParamDefinition"
        )
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert data['data']['type'] == "testparameter_definitions"
        assert data['data']['id'] == "MyProjectId/MyTestParamDefinition"
        assert data['data']['attributes']['name'] == "Test Parameter Definition example"
        
        # Verify API call
        mock_projects_api._session.get.assert_called_once()
        call_args = mock_projects_api._session.get.call_args
        assert 'projects/MyProjectId/testparameterdefinitions/MyTestParamDefinition' in call_args[0][0]
    
    def test_get_project_test_parameter_definition_with_fields(self, mock_projects_api):
        """Test getting test parameter definition with custom fields"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameter_definitions",
                "id": "MyProjectId/MyTestParam",
                "attributes": {
                    "name": "Test Parameter"
                }
            }
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definition(
            project_id="MyProjectId",
            test_param_id="MyTestParam",
            fields={"testparameterdefinitions": "id,name"}
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_projects_api._session.get.call_args
        params = call_args[1]['params']
        assert params['fields[testparameterdefinitions]'] == "id,name"
    
    def test_get_project_test_parameter_definition_with_include(self, mock_projects_api):
        """Test getting test parameter definition with included resources"""
        # Mock response with included data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameter_definitions",
                "id": "MyProjectId/MyTestParam",
                "attributes": {
                    "name": "Test Parameter"
                },
                "relationships": {
                    "project": {
                        "data": {"type": "projects", "id": "MyProjectId"}
                    }
                }
            },
            "included": [{
                "type": "projects",
                "id": "MyProjectId",
                "attributes": {
                    "name": "My Project"
                }
            }]
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definition(
            project_id="MyProjectId",
            test_param_id="MyTestParam",
            include="project"
        )
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert 'included' in data
        assert len(data['included']) == 1
        
        # Verify include param was passed
        call_args = mock_projects_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == "project"
    
    def test_get_project_test_parameter_definition_not_found(self, mock_projects_api):
        """Test getting non-existent test parameter definition"""
        # Mock 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Test parameter definition not found"
            }]
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definition(
            "MyProjectId", 
            "NonExistentParam"
        )
        
        # Verify
        assert response.status_code == 404
    
    def test_get_project_test_parameter_definition_project_not_found(self, mock_projects_api):
        """Test getting test parameter definition from non-existent project"""
        # Mock 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Project not found"
            }]
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definition(
            "NONEXISTENT", 
            "MyTestParam"
        )
        
        # Verify
        assert response.status_code == 404
    
    def test_get_project_test_parameter_definition_unauthorized(self, mock_projects_api):
        """Test getting test parameter definition without authorization"""
        # Mock 401 response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [{
                "status": "401",
                "title": "Unauthorized",
                "detail": "Authentication required"
            }]
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definition(
            "MyProjectId", 
            "MyTestParam"
        )
        
        # Verify
        assert response.status_code == 401
    
    def test_get_project_test_parameter_definition_forbidden(self, mock_projects_api):
        """Test getting test parameter definition without permissions"""
        # Mock 403 response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "Insufficient permissions"
            }]
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definition(
            "MyProjectId", 
            "MyTestParam"
        )
        
        # Verify
        assert response.status_code == 403
    
    def test_get_project_test_parameter_definition_with_all_params(self, mock_projects_api):
        """Test getting test parameter definition with all parameters"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameter_definitions",
                "id": "MyProjectId/MyTestParam",
                "revision": "5678",
                "attributes": {
                    "name": "Test Parameter"
                }
            },
            "included": []
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definition(
            project_id="MyProjectId",
            test_param_id="MyTestParam",
            fields={"testparameterdefinitions": "id,name,type"},
            include="project"
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_projects_api._session.get.call_args
        params = call_args[1]['params']
        assert params['fields[testparameterdefinitions]'] == "id,name,type"
        assert params['include'] == "project"
    
    def test_get_project_test_parameter_definition_server_error(self, mock_projects_api):
        """Test getting test parameter definition with server error"""
        # Mock 500 response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [{
                "status": "500",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred"
            }]
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definition(
            "MyProjectId", 
            "MyTestParam"
        )
        
        # Verify
        assert response.status_code == 500
    
    def test_get_project_test_parameter_definition_url_encoding(self, mock_projects_api):
        """Test URL is properly constructed with special characters"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute with IDs containing special characters
        response = mock_projects_api.get_project_test_parameter_definition(
            "My-Project", 
            "test_param_01"
        )
        
        # Verify URL construction
        call_args = mock_projects_api._session.get.call_args
        assert 'projects/My-Project/testparameterdefinitions/test_param_01' in call_args[0][0]


# ============================================================================
# Unit Tests - Default Fields Logic
# ============================================================================

class TestGetProjectTestParameterDefinitionDefaultFields:
    """Unit tests to verify default_fields logic"""
    
    def test_get_project_test_parameter_definition_default_fields(self, mock_projects_api):
        """Test that get_project_test_parameter_definition sends default fields"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        mock_projects_api.get_project_test_parameter_definition("TEST_PROJECT", "param1")
        
        # Verify API call and params
        call_args = mock_projects_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify all default fields are present
        assert "fields[testparameter_definitions]" in params or "fields[testparameterdefinitions]" in params
        # Check which format is used and verify @all
        if "fields[testparameter_definitions]" in params:
            assert params["fields[testparameter_definitions]"] == "@all"
        else:
            assert params["fields[testparameterdefinitions]"] == "@all"
        
        print("\n✓ Default fields sent with @all")
    
    def test_get_project_test_parameter_definition_override(self, mock_projects_api):
        """Test that get_project_test_parameter_definition allows field override"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute with custom field
        custom_fields = {"testparameterdefinitions": "id,name,type"}
        mock_projects_api.get_project_test_parameter_definition(
            "TEST_PROJECT", 
            "param1",
            fields=custom_fields
        )
        
        # Verify API call and params
        call_args = mock_projects_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom field is applied
        assert params["fields[testparameterdefinitions]"] == "id,name,type"
        
        print("\n✓ Custom field overrides default")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s', '--tb=short'])
