"""
Pytest test suite for post_project_test_parameter_definitions method.
Tests the creation of test parameter definitions for a project in Polarion.

Test Strategy:
- All tests use mocks to avoid modifying real data
- Tests cover success cases, error cases, and edge cases

Test Coverage:
- Successful creation of single test parameter definition
- Successful creation of multiple test parameter definitions
- Project not found (404)
- Insufficient permissions (403)
- Invalid data format (400)
- Duplicate parameter (409)
- Server errors (500)
- Various parameter types and formats

Run with:
    pytest test_post_project_test_parameter_definitions.py -v
    pytest test_post_project_test_parameter_definitions.py -v --tb=short
"""
import pytest
import json
from unittest.mock import Mock


@pytest.fixture
def sample_single_param_data():
    """Sample data for single test parameter definition"""
    return {
        "data": [
            {
                "type": "testparameterdefinitions",
                "attributes": {
                    "name": "test_param_001",
                    "description": {
                        "type": "text/plain",
                        "content": "Test parameter created by pytest"
                    },
                    "parameterType": "string"
                }
            }
        ]
    }


@pytest.fixture
def sample_multiple_params_data():
    """Sample data for multiple test parameter definitions"""
    return {
        "data": [
            {
                "type": "testparameterdefinitions",
                "attributes": {
                    "name": "param_string",
                    "parameterType": "string",
                    "description": {
                        "type": "text/plain",
                        "content": "String parameter"
                    }
                }
            },
            {
                "type": "testparameterdefinitions",
                "attributes": {
                    "name": "param_number",
                    "parameterType": "number",
                    "description": {
                        "type": "text/plain",
                        "content": "Number parameter"
                    }
                }
            },
            {
                "type": "testparameterdefinitions",
                "attributes": {
                    "name": "param_boolean",
                    "parameterType": "boolean",
                    "description": {
                        "type": "text/plain",
                        "content": "Boolean parameter"
                    }
                }
            }
        ]
    }


# ============================================================================
# Unit Tests - post_project_test_parameter_definitions
# ============================================================================

class TestPostProjectTestParameterDefinitions:
    """Unit tests for post_project_test_parameter_definitions method"""
    
    def test_create_single_param_success(self, mock_projects_api, sample_single_param_data):
        """Test successful creation of single test parameter definition"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "id": "TEST_PROJECT/test_param_001",
                    "attributes": {
                        "name": "test_param_001",
                        "description": {
                            "type": "text/plain",
                            "value": "Test parameter created by pytest"
                        },
                        "parameterType": "string"
                    }
                }
            ]
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Execute
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=sample_single_param_data
        )
        
        # Assert
        assert response.status_code == 201
        mock_projects_api._session.post.assert_called_once()
        
        # Verify correct endpoint
        call_args = mock_projects_api._session.post.call_args
        assert 'projects/TEST_PROJECT/testparameterdefinitions' in call_args[0][0]
        
        # Verify request body
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 1
        assert sent_data['data'][0]['attributes']['name'] == 'test_param_001'
        
        # Verify response
        result = response.json()
        assert len(result['data']) == 1
        assert result['data'][0]['id'] == 'TEST_PROJECT/test_param_001'
        
        print("\n✓ Single test parameter definition created successfully (201)")
    
    def test_create_multiple_params_success(self, mock_projects_api, sample_multiple_params_data):
        """Test successful creation of multiple test parameter definitions"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "id": "TEST_PROJECT/param_string",
                    "attributes": {"name": "param_string", "parameterType": "string"}
                },
                {
                    "type": "testparameterdefinitions",
                    "id": "TEST_PROJECT/param_number",
                    "attributes": {"name": "param_number", "parameterType": "number"}
                },
                {
                    "type": "testparameterdefinitions",
                    "id": "TEST_PROJECT/param_boolean",
                    "attributes": {"name": "param_boolean", "parameterType": "boolean"}
                }
            ]
        }
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=sample_multiple_params_data
        )
        
        assert response.status_code == 201
        result = response.json()
        assert len(result['data']) == 3
        assert result['data'][0]['attributes']['parameterType'] == 'string'
        assert result['data'][1]['attributes']['parameterType'] == 'number'
        assert result['data'][2]['attributes']['parameterType'] == 'boolean'
        
        print("\n✓ Multiple test parameter definitions created successfully (201)")
    
    def test_create_param_project_not_found(self, mock_projects_api, sample_single_param_data):
        """Test creation when project doesn't exist"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = json.dumps({
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Project 'NONEXISTENT' not found"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='NONEXISTENT',
            test_params_data=sample_single_param_data
        )
        
        assert response.status_code == 404
        print("\n✓ Project not found handled correctly (404)")
    
    def test_create_param_insufficient_permissions(self, mock_projects_api, sample_single_param_data):
        """Test creation without sufficient permissions"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = json.dumps({
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to create test parameter definitions in this project"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='PROTECTED_PROJECT',
            test_params_data=sample_single_param_data
        )
        
        assert response.status_code == 403
        print("\n✓ Insufficient permissions handled correctly (403)")
    
    def test_create_param_invalid_data(self, mock_projects_api):
        """Test creation with invalid data format"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid test parameter definition format"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        invalid_data = {
            "data": [
                {
                    "type": "wrong_type",
                    "attributes": {}
                }
            ]
        }
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=invalid_data
        )
        
        assert response.status_code == 400
        print("\n✓ Invalid data format handled correctly (400)")
    
    def test_create_param_duplicate(self, mock_projects_api, sample_single_param_data):
        """Test creation of duplicate test parameter definition"""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.text = json.dumps({
            "errors": [{
                "status": "409",
                "title": "Conflict",
                "detail": "Test parameter definition 'test_param_001' already exists in project 'TEST_PROJECT'"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=sample_single_param_data
        )
        
        assert response.status_code == 409
        print("\n✓ Duplicate parameter handled correctly (409)")
    
    def test_create_param_server_error(self, mock_projects_api, sample_single_param_data):
        """Test creation with server error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = json.dumps({
            "errors": [{
                "status": "500",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred while creating test parameter definitions"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=sample_single_param_data
        )
        
        assert response.status_code == 500
        print("\n✓ Server error handled correctly (500)")
    
    def test_create_param_missing_required_fields(self, mock_projects_api):
        """Test creation with missing required fields"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Missing required field: name"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        invalid_data = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "attributes": {
                        "parameterType": "string"
                        # Missing 'name' field
                    }
                }
            ]
        }
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=invalid_data
        )
        
        assert response.status_code == 400
        print("\n✓ Missing required fields handled correctly (400)")
    
    def test_create_param_empty_data_array(self, mock_projects_api):
        """Test creation with empty data array"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Data array cannot be empty"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        empty_data = {
            "data": []
        }
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=empty_data
        )
        
        assert response.status_code == 400
        print("\n✓ Empty data array handled correctly (400)")
    
    def test_create_param_with_default_value(self, mock_projects_api):
        """Test creation with default value"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "id": "TEST_PROJECT/param_with_default",
                    "attributes": {
                        "name": "param_with_default",
                        "parameterType": "string",
                        "defaultValue": "default_value"
                    }
                }
            ]
        }
        mock_projects_api._session.post.return_value = mock_response
        
        param_data = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "attributes": {
                        "name": "param_with_default",
                        "parameterType": "string",
                        "defaultValue": "default_value"
                    }
                }
            ]
        }
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=param_data
        )
        
        assert response.status_code == 201
        result = response.json()
        assert result['data'][0]['attributes']['defaultValue'] == 'default_value'
        
        print("\n✓ Parameter with default value created successfully (201)")
    
    def test_create_param_with_enum_values(self, mock_projects_api):
        """Test creation with enumerated values"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "id": "TEST_PROJECT/param_enum",
                    "attributes": {
                        "name": "param_enum",
                        "parameterType": "enum",
                        "allowedValues": ["value1", "value2", "value3"]
                    }
                }
            ]
        }
        mock_projects_api._session.post.return_value = mock_response
        
        param_data = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "attributes": {
                        "name": "param_enum",
                        "parameterType": "enum",
                        "allowedValues": ["value1", "value2", "value3"]
                    }
                }
            ]
        }
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=param_data
        )
        
        assert response.status_code == 201
        result = response.json()
        assert len(result['data'][0]['attributes']['allowedValues']) == 3
        
        print("\n✓ Parameter with enum values created successfully (201)")
    
    def test_create_param_unauthorized(self, mock_projects_api, sample_single_param_data):
        """Test creation with invalid token"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = json.dumps({
            "errors": [{
                "status": "401",
                "title": "Unauthorized",
                "detail": "Authentication token is invalid or expired"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=sample_single_param_data
        )
        
        assert response.status_code == 401
        print("\n✓ Unauthorized access handled correctly (401)")
    
    def test_create_param_service_unavailable(self, mock_projects_api, sample_single_param_data):
        """Test creation when service is unavailable"""
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.text = json.dumps({
            "errors": [{
                "status": "503",
                "title": "Service Unavailable",
                "detail": "The service is temporarily unavailable"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=sample_single_param_data
        )
        
        assert response.status_code == 503
        print("\n✓ Service unavailable handled correctly (503)")
    
    def test_create_param_with_special_chars_in_name(self, mock_projects_api):
        """Test creation with special characters in parameter name"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "id": "TEST_PROJECT/param-with-dashes_and_underscores",
                    "attributes": {
                        "name": "param-with-dashes_and_underscores"
                    }
                }
            ]
        }
        mock_projects_api._session.post.return_value = mock_response
        
        param_data = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "attributes": {
                        "name": "param-with-dashes_and_underscores",
                        "parameterType": "string"
                    }
                }
            ]
        }
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=param_data
        )
        
        assert response.status_code == 201
        print("\n✓ Parameter with special chars in name created successfully (201)")
    
    def test_create_param_large_batch(self, mock_projects_api):
        """Test creation of large batch of parameters"""
        mock_response = Mock()
        mock_response.status_code = 201
        
        # Create response with 20 parameters
        response_data = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "id": f"TEST_PROJECT/param_{i:03d}",
                    "attributes": {"name": f"param_{i:03d}"}
                }
                for i in range(20)
            ]
        }
        mock_response.json.return_value = response_data
        mock_projects_api._session.post.return_value = mock_response
        
        # Create request with 20 parameters
        large_batch_data = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "attributes": {
                        "name": f"param_{i:03d}",
                        "parameterType": "string"
                    }
                }
                for i in range(20)
            ]
        }
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=large_batch_data
        )
        
        assert response.status_code == 201
        result = response.json()
        assert len(result['data']) == 20
        
        print("\n✓ Large batch (20 parameters) created successfully (201)")
    
    def test_create_param_partial_success(self, mock_projects_api, sample_multiple_params_data):
        """Test creation with partial success (some params fail)"""
        mock_response = Mock()
        mock_response.status_code = 207  # Multi-Status
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "id": "TEST_PROJECT/param_string",
                    "attributes": {"name": "param_string"},
                    "meta": {"status": "created"}
                },
                {
                    "type": "testparameterdefinitions",
                    "id": "TEST_PROJECT/param_number",
                    "attributes": {"name": "param_number"},
                    "meta": {"status": "created"}
                }
            ],
            "errors": [
                {
                    "status": "409",
                    "title": "Conflict",
                    "detail": "Parameter 'param_boolean' already exists",
                    "source": {"pointer": "/data/2"}
                }
            ]
        }
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=sample_multiple_params_data
        )
        
        assert response.status_code == 207
        result = response.json()
        assert len(result['data']) == 2
        assert len(result['errors']) == 1
        
        print("\n✓ Partial success handled correctly (207)")
    
    def test_create_param_with_rich_text_description(self, mock_projects_api):
        """Test creation with rich text description"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "id": "TEST_PROJECT/param_with_html",
                    "attributes": {
                        "name": "param_with_html",
                        "description": {
                            "type": "text/html",
                            "value": "<p>Rich <strong>text</strong> description</p>"
                        }
                    }
                }
            ]
        }
        mock_projects_api._session.post.return_value = mock_response
        
        param_data = {
            "data": [
                {
                    "type": "testparameterdefinitions",
                    "attributes": {
                        "name": "param_with_html",
                        "parameterType": "string",
                        "description": {
                            "type": "text/html",
                            "content": "<p>Rich <strong>text</strong> description</p>"
                        }
                    }
                }
            ]
        }
        
        response = mock_projects_api.post_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_params_data=param_data
        )
        
        assert response.status_code == 201
        print("\n✓ Parameter with rich text description created successfully (201)")


# ============================================================================
# Test Configuration and Markers
# ============================================================================

def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line(
        "markers", "post: mark test as POST operation (uses mocks)"
    )


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([
        __file__,
        '-v',
        '-s',
        '--tb=short'
    ])
