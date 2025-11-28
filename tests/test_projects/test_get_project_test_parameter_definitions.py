"""
Pytest tests for get_project_test_parameter_definitions method.

Tests the get_project_test_parameter_definitions method from Projects class.
Uses mocked API responses for reliable and fast testing.

Run with:
    pytest test_get_project_test_parameter_definitions.py -v
"""
import pytest
from unittest.mock import Mock


# ============================================================================
# Mocked Tests
# ============================================================================

class TestGetProjectTestParameterDefinitionsMocked:
    """Mocked tests for project test parameter definitions"""
    
    def test_get_project_test_parameter_definitions_success(self, mock_projects_api):
        """Test getting list of test parameter definitions successfully"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 2
            },
            "data": [
                {
                    "type": "testparameter_definitions",
                    "id": "MyProjectId/MyTestParamDefinition",
                    "revision": "1234",
                    "attributes": {
                        "name": "Test Parameter Definition example"
                    },
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/testparameterdefinitions/MyTestParamDefinition"
                    }
                },
                {
                    "type": "testparameter_definitions",
                    "id": "MyProjectId/AnotherTestParam",
                    "revision": "5678",
                    "attributes": {
                        "name": "Another Test Parameter"
                    },
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/testparameterdefinitions/AnotherTestParam"
                    }
                }
            ],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/testparameterdefinitions"
            }
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definitions("MyProjectId")
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert data['meta']['totalCount'] == 2
        assert len(data['data']) == 2
        assert data['data'][0]['attributes']['name'] == "Test Parameter Definition example"
        
        # Verify API call
        mock_projects_api._session.get.assert_called_once()
        call_args = mock_projects_api._session.get.call_args
        assert 'projects/MyProjectId/testparameterdefinitions' in call_args[0][0]
    
    def test_get_project_test_parameter_definitions_with_pagination(self, mock_projects_api):
        """Test getting test parameter definitions with pagination"""
        # Mock response with pagination
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 25
            },
            "data": [
                {
                    "type": "testparameter_definitions",
                    "id": f"MyProjectId/TestParam{i}",
                    "revision": str(1000 + i),
                    "attributes": {
                        "name": f"Test Parameter {i}"
                    }
                } for i in range(10)
            ],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/testparameterdefinitions?page%5Bsize%5D=10&page%5Bnumber%5D=1",
                "first": "server-host-name/application-path/projects/MyProjectId/testparameterdefinitions?page%5Bsize%5D=10&page%5Bnumber%5D=1",
                "next": "server-host-name/application-path/projects/MyProjectId/testparameterdefinitions?page%5Bsize%5D=10&page%5Bnumber%5D=2",
                "last": "server-host-name/application-path/projects/MyProjectId/testparameterdefinitions?page%5Bsize%5D=10&page%5Bnumber%5D=3"
            }
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definitions(
            project_id="MyProjectId",
            page_size=10,
            page_number=1
        )
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert len(data['data']) == 10
        assert data['meta']['totalCount'] == 25
        
        # Verify pagination params were passed
        call_args = mock_projects_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 10
        assert params['page[number]'] == 1
    
    def test_get_project_test_parameter_definitions_empty(self, mock_projects_api):
        """Test getting test parameter definitions when project has none"""
        # Mock response with empty list
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 0
            },
            "data": [],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/testparameterdefinitions"
            }
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definitions("MyProjectId")
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert data['meta']['totalCount'] == 0
        assert len(data['data']) == 0
    
    def test_get_project_test_parameter_definitions_not_found(self, mock_projects_api):
        """Test getting test parameter definitions for non-existent project"""
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
        response = mock_projects_api.get_project_test_parameter_definitions("NONEXISTENT")
        
        # Verify
        assert response.status_code == 404
    
    def test_get_project_test_parameter_definitions_unauthorized(self, mock_projects_api):
        """Test getting test parameter definitions without authorization"""
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
        response = mock_projects_api.get_project_test_parameter_definitions("MyProjectId")
        
        # Verify
        assert response.status_code == 401
    
    def test_get_project_test_parameter_definitions_forbidden(self, mock_projects_api):
        """Test getting test parameter definitions without permissions"""
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
        response = mock_projects_api.get_project_test_parameter_definitions("MyProjectId")
        
        # Verify
        assert response.status_code == 403
    
    def test_get_project_test_parameter_definitions_with_fields(self, mock_projects_api):
        """Test getting test parameter definitions with custom fields"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 1},
            "data": [{
                "type": "testparameter_definitions",
                "id": "MyProjectId/MyTestParam",
                "attributes": {
                    "name": "Test Parameter"
                }
            }]
        }
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_projects_api.get_project_test_parameter_definitions(
            project_id="MyProjectId",
            fields={"testparameterdefinitions": "id,name"}
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_projects_api._session.get.call_args
        params = call_args[1]['params']
        assert params['fields[testparameterdefinitions]'] == "id,name"
    
    def test_get_project_test_parameter_definitions_with_include(self, mock_projects_api):
        """Test getting test parameter definitions with included resources"""
        # Mock response with included data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 1},
            "data": [{
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
            }],
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
        response = mock_projects_api.get_project_test_parameter_definitions(
            project_id="MyProjectId",
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


# ============================================================================
# Unit Tests - Default Fields Logic
# ============================================================================

class TestGetProjectTestParameterDefinitionsDefaultFields:
    """Unit tests to verify default_fields logic"""
    
    def test_get_project_test_parameter_definitions_default_fields(self, mock_projects_api):
        """Test that get_project_test_parameter_definitions sends default fields"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute
        mock_projects_api.get_project_test_parameter_definitions("TEST_PROJECT")
        
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
    
    def test_get_project_test_parameter_definitions_override(self, mock_projects_api):
        """Test that get_project_test_parameter_definitions allows field override"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        mock_projects_api._session.get.return_value = mock_response
        
        # Execute with custom field
        custom_fields = {"testparameterdefinitions": "id,name"}
        mock_projects_api.get_project_test_parameter_definitions(
            "TEST_PROJECT", 
            fields=custom_fields
        )
        
        # Verify API call and params
        call_args = mock_projects_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom field is applied
        assert params["fields[testparameterdefinitions]"] == "id,name"
        
        print("\n✓ Custom field overrides default")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s', '--tb=short'])
