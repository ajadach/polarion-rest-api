"""
Pytest test suite for delete_project_test_parameter_definition method.
Tests the deletion of a single test parameter definition for a project.

Test Strategy:
- All tests use mocks to avoid modifying real data
- Tests cover success cases, error cases, and edge cases

Test Coverage:
- Successful deletion of test parameter definition
- Project not found (404)
- Test parameter not found (404)
- Insufficient permissions (403)
- Parameter in use / conflict (409)
- Invalid parameter ID format (400)
- Special characters in IDs
- Server errors (500)

Run with:
    pytest test_delete_project_test_parameter_definition.py -v
    pytest test_delete_project_test_parameter_definition.py -v --tb=short
"""
import pytest
import json
from unittest.mock import Mock


# ============================================================================
# Unit Tests - delete_project_test_parameter_definition
# ============================================================================

class TestDeleteProjectTestParameterDefinition:
    """Unit tests for delete_project_test_parameter_definition method"""
    
    def test_delete_success(self, mock_projects_api):
        """Test successful deletion of test parameter definition"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_projects_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param_001'
        )
        
        # Assert
        assert response.status_code == 204
        mock_projects_api._session.delete.assert_called_once()
        
        # Verify correct endpoint
        call_args = mock_projects_api._session.delete.call_args
        expected_url = 'projects/TEST_PROJECT/testparameterdefinitions/param_001'
        assert expected_url in call_args[0][0]
        
        print("\n✓ Successfully deleted test parameter definition (204)")
    
    def test_delete_project_not_found(self, mock_projects_api):
        """Test deletion when project doesn't exist"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = json.dumps({
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Project 'NONEXISTENT' not found"
            }]
        })
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='NONEXISTENT',
            test_param_id='param_001'
        )
        
        assert response.status_code == 404
        
        # Verify error message can be parsed
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['status'] == '404'
        
        print("\n✓ Project not found handled correctly (404)")
    
    def test_delete_param_not_found(self, mock_projects_api):
        """Test deletion when test parameter doesn't exist"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = json.dumps({
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Test parameter definition 'nonexistent_param' not found in project 'TEST_PROJECT'"
            }]
        })
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='nonexistent_param'
        )
        
        assert response.status_code == 404
        print("\n✓ Test parameter not found handled correctly (404)")
    
    def test_delete_insufficient_permissions(self, mock_projects_api):
        """Test deletion without sufficient permissions"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = json.dumps({
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to delete test parameter definitions in this project"
            }]
        })
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='PROTECTED_PROJECT',
            test_param_id='param_001'
        )
        
        assert response.status_code == 403
        print("\n✓ Insufficient permissions handled correctly (403)")
    
    def test_delete_param_in_use(self, mock_projects_api):
        """Test deletion when parameter is in use (conflict)"""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.text = json.dumps({
            "errors": [{
                "status": "409",
                "title": "Conflict",
                "detail": "Cannot delete test parameter 'param_001' because it is referenced by 5 test runs"
            }]
        })
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param_001'
        )
        
        assert response.status_code == 409
        
        # Verify conflict details
        error_data = json.loads(response.text)
        assert 'referenced' in error_data['errors'][0]['detail']
        
        print("\n✓ Parameter in use conflict handled correctly (409)")
    
    def test_delete_invalid_param_id_format(self, mock_projects_api):
        """Test deletion with invalid parameter ID format"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid test parameter ID format"
            }]
        })
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='invalid@param#id'
        )
        
        assert response.status_code == 400
        print("\n✓ Invalid parameter ID format handled correctly (400)")
    
    def test_delete_with_dashes_in_id(self, mock_projects_api):
        """Test deletion with dashes in parameter ID"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param-with-dashes'
        )
        
        assert response.status_code == 204
        
        # Verify correct URL construction
        call_args = mock_projects_api._session.delete.call_args
        assert 'param-with-dashes' in call_args[0][0]
        
        print("\n✓ Parameter ID with dashes handled correctly (204)")
    
    def test_delete_with_underscores_in_id(self, mock_projects_api):
        """Test deletion with underscores in parameter ID"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param_with_underscores'
        )
        
        assert response.status_code == 204
        
        # Verify correct URL construction
        call_args = mock_projects_api._session.delete.call_args
        assert 'param_with_underscores' in call_args[0][0]
        
        print("\n✓ Parameter ID with underscores handled correctly (204)")
    
    def test_delete_with_dots_in_id(self, mock_projects_api):
        """Test deletion with dots in parameter ID"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param.with.dots'
        )
        
        assert response.status_code == 204
        
        # Verify correct URL construction
        call_args = mock_projects_api._session.delete.call_args
        assert 'param.with.dots' in call_args[0][0]
        
        print("\n✓ Parameter ID with dots handled correctly (204)")
    
    def test_delete_with_numbers_in_id(self, mock_projects_api):
        """Test deletion with numbers in parameter ID"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param_123_test'
        )
        
        assert response.status_code == 204
        
        # Verify correct URL construction
        call_args = mock_projects_api._session.delete.call_args
        assert 'param_123_test' in call_args[0][0]
        
        print("\n✓ Parameter ID with numbers handled correctly (204)")
    
    def test_delete_server_error(self, mock_projects_api):
        """Test deletion with server error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = json.dumps({
            "errors": [{
                "status": "500",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred while deleting the test parameter"
            }]
        })
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param_001'
        )
        
        assert response.status_code == 500
        print("\n✓ Server error handled correctly (500)")
    
    def test_delete_service_unavailable(self, mock_projects_api):
        """Test deletion when service is unavailable"""
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.text = json.dumps({
            "errors": [{
                "status": "503",
                "title": "Service Unavailable",
                "detail": "The service is temporarily unavailable"
            }]
        })
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param_001'
        )
        
        assert response.status_code == 503
        print("\n✓ Service unavailable handled correctly (503)")
    
    def test_delete_with_long_param_id(self, mock_projects_api):
        """Test deletion with very long parameter ID"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._session.delete.return_value = mock_response
        
        long_param_id = 'very_long_parameter_id_' + 'x' * 100
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id=long_param_id
        )
        
        assert response.status_code == 204
        
        # Verify long ID is in URL
        call_args = mock_projects_api._session.delete.call_args
        assert long_param_id in call_args[0][0]
        
        print("\n✓ Long parameter ID handled correctly (204)")
    
    def test_delete_with_project_containing_special_chars(self, mock_projects_api):
        """Test deletion with project ID containing special characters"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='PROJECT-2024_Q1',
            test_param_id='param_001'
        )
        
        assert response.status_code == 204
        
        # Verify project ID is in URL
        call_args = mock_projects_api._session.delete.call_args
        assert 'PROJECT-2024_Q1' in call_args[0][0]
        
        print("\n✓ Project ID with special chars handled correctly (204)")
    
    def test_delete_unauthorized(self, mock_projects_api):
        """Test deletion with invalid/expired token"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = json.dumps({
            "errors": [{
                "status": "401",
                "title": "Unauthorized",
                "detail": "Authentication token is invalid or expired"
            }]
        })
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param_001'
        )
        
        assert response.status_code == 401
        print("\n✓ Unauthorized access handled correctly (401)")
    
    def test_delete_method_not_allowed(self, mock_projects_api):
        """Test when DELETE method is not allowed"""
        mock_response = Mock()
        mock_response.status_code = 405
        mock_response.text = json.dumps({
            "errors": [{
                "status": "405",
                "title": "Method Not Allowed",
                "detail": "DELETE method is not allowed for this resource"
            }]
        })
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param_001'
        )
        
        assert response.status_code == 405
        print("\n✓ Method not allowed handled correctly (405)")
    
    def test_delete_with_empty_project_id(self, mock_projects_api):
        """Test deletion with empty project ID"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Project ID cannot be empty"
            }]
        })
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='',
            test_param_id='param_001'
        )
        
        assert response.status_code == 400
        print("\n✓ Empty project ID handled correctly (400)")
    
    def test_delete_with_empty_param_id(self, mock_projects_api):
        """Test deletion with empty parameter ID"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Test parameter ID cannot be empty"
            }]
        })
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id=''
        )
        
        assert response.status_code == 400
        print("\n✓ Empty parameter ID handled correctly (400)")
    
    def test_delete_returns_200_with_details(self, mock_projects_api):
        """Test deletion that returns 200 with deletion details"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameterdefinitions",
                "id": "TEST_PROJECT/param_001",
                "attributes": {
                    "deletedAt": "2024-11-04T10:30:00Z",
                    "deletedBy": "test_user"
                }
            }
        }
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param_001'
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['data']['id'] == 'TEST_PROJECT/param_001'
        assert 'deletedAt' in result['data']['attributes']
        
        print("\n✓ Deletion with details handled correctly (200)")


# ============================================================================
# Edge Cases and Error Combinations
# ============================================================================

class TestDeleteParameterDefinitionEdgeCases:
    """Test edge cases and error combinations"""
    
    def test_delete_multiple_times(self, mock_projects_api):
        """Test deleting the same parameter multiple times"""
        # First deletion succeeds
        mock_response_success = Mock()
        mock_response_success.status_code = 204
        
        # Second deletion fails (not found)
        mock_response_not_found = Mock()
        mock_response_not_found.status_code = 404
        mock_response_not_found.text = json.dumps({
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Test parameter already deleted"
            }]
        })
        
        mock_projects_api._session.delete.side_effect = [
            mock_response_success,
            mock_response_not_found
        ]
        
        # First deletion
        response1 = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param_001'
        )
        assert response1.status_code == 204
        
        # Second deletion (should fail)
        response2 = mock_projects_api.delete_project_test_parameter_definition(
            project_id='TEST_PROJECT',
            test_param_id='param_001'
        )
        assert response2.status_code == 404
        
        print("\n✓ Multiple deletion attempts handled correctly")


# ============================================================================
# Test Configuration and Markers
# ============================================================================

def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line(
        "markers", "delete: mark test as delete operation (uses mocks)"
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
