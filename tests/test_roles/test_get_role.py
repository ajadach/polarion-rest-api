"""
Pytest test suite for get_role method.
Tests the retrieval of a Global Role in Polarion.

Test Strategy:
- Unit tests with mocks for default fields logic
- Tests cover success cases, error cases, and edge cases

Test Coverage:
- Successful role retrieval
- Role with field filtering
- Role with include parameter
- Role not found (404)
- Invalid role ID
- Permission issues (403)
- Default fields behavior

Run with:
    pytest test_get_role.py -v
"""
import pytest
import json
from unittest.mock import Mock


# ============================================================================
# Unit Tests - Default Fields Behavior
# ============================================================================

class TestGetRoleDefaultFields:
    """Unit tests for default fields behavior"""
    
    def test_get_role_sends_all_default_fields(self, mock_roles_api):
        """Test that get_role sends all default fields when none specified"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "globalroles",
                "id": "test_role",
                "attributes": {
                    "name": "Test Role"
                }
            }
        }
        mock_roles_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_roles_api.get_role(role_id='test_role')
        
        # Assert
        assert response.status_code == 200
        mock_roles_api._session.get.assert_called_once()
        
        # Verify that params contain default fields
        call_args = mock_roles_api._session.get.call_args
        params = call_args[1]['params']
        
        # Should have default fields set to @all
        assert 'fields[globalroles]' in params
        assert params['fields[globalroles]'] == '@all'
        assert 'fields[projects]' in params
        assert params['fields[projects]'] == '@all'
        
        print("\n✓ All default fields sent with @all value")
    
    def test_get_role_overrides_only_specified_fields(self, mock_roles_api):
        """Test that custom fields override only specified keys"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "globalroles",
                "id": "test_role",
                "attributes": {
                    "name": "Test Role"
                }
            }
        }
        mock_roles_api._session.get.return_value = mock_response
        
        # Execute with custom fields
        response = mock_roles_api.get_role(
            role_id='test_role',
            fields={'globalroles': 'name,id'}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify params
        call_args = mock_roles_api._session.get.call_args
        params = call_args[1]['params']
        
        # Custom field should be overridden
        assert params['fields[globalroles]'] == 'name,id'
        
        # Other fields should still be @all
        assert 'fields[projects]' in params
        assert params['fields[projects]'] == '@all'
        assert 'fields[users]' in params
        assert params['fields[users]'] == '@all'
        
        print("\n✓ Custom fields override only specified keys")
        print(f"✓ globalroles overridden to: {params['fields[globalroles]']}")
        print(f"✓ Other fields remain @all")


# ============================================================================
# Unit Tests - Mocked Scenarios
# ============================================================================

class TestGetRoleMocked:
    """Unit tests for get_role with mocked responses"""
    
    def test_get_role_success(self, mock_roles_api):
        """Test successful role retrieval"""
        # Setup mock response - realistic Polarion API format
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "globalroles",
                "id": "project_user",
                "attributes": {
                    "name": "Project User",
                    "description": {
                        "type": "text/plain",
                        "value": "Standard project user role"
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/roles/project_user"
                }
            }
        }
        mock_roles_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_roles_api.get_role(role_id='project_user')
        
        # Assert
        assert response.status_code == 200
        mock_roles_api._session.get.assert_called_once()
        
        # Verify correct endpoint
        call_args = mock_roles_api._session.get.call_args
        assert '/roles/project_user' in call_args[0][0]
        
        # Verify response
        result = response.json()
        assert result['data']['type'] == 'globalroles'
        assert result['data']['id'] == 'project_user'
        assert result['data']['attributes']['name'] == 'Project User'
        
        print("\n✓ Role retrieved successfully (200)")
    
    def test_get_role_not_found_mocked(self, mock_roles_api):
        """Test role not found error"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = json.dumps({
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Role 'NONEXISTENT' not found",
                "source": {
                    "resource": {
                        "id": "NONEXISTENT",
                        "type": "globalroles"
                    }
                }
            }]
        })
        mock_roles_api._session.get.return_value = mock_response
        
        response = mock_roles_api.get_role(role_id='NONEXISTENT')
        
        assert response.status_code == 404
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['status'] == '404'
        assert error_data['errors'][0]['source']['resource']['id'] == 'NONEXISTENT'
        
        print("\n✓ Role not found handled correctly (404)")
    
    def test_get_role_forbidden(self, mock_roles_api):
        """Test permission denied for role access"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = json.dumps({
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to view this role",
                "source": {
                    "resource": {
                        "id": "admin",
                        "type": "globalroles"
                    }
                }
            }]
        })
        mock_roles_api._session.get.return_value = mock_response
        
        response = mock_roles_api.get_role(role_id='admin')
        
        assert response.status_code == 403
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['title'] == 'Forbidden'
        
        print("\n✓ Permission denied handled correctly (403)")
    
    def test_get_role_with_include_parameter(self, mock_roles_api):
        """Test getting role with include parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "globalroles",
                "id": "project_user",
                "attributes": {
                    "name": "Project User"
                },
                "relationships": {
                    "permissions": {
                        "data": [
                            {"type": "permissions", "id": "read"},
                            {"type": "permissions", "id": "write"}
                        ]
                    }
                }
            },
            "included": [
                {
                    "type": "permissions",
                    "id": "read",
                    "attributes": {
                        "name": "Read Permission"
                    }
                },
                {
                    "type": "permissions",
                    "id": "write",
                    "attributes": {
                        "name": "Write Permission"
                    }
                }
            ]
        }
        mock_roles_api._session.get.return_value = mock_response
        
        response = mock_roles_api.get_role(
            role_id='project_user',
            include='permissions'
        )
        
        assert response.status_code == 200
        
        # Verify include parameter was sent
        call_args = mock_roles_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'permissions'
        
        # Verify included data
        result = response.json()
        assert 'included' in result
        assert len(result['included']) == 2
        
        print("\n✓ Include parameter handled correctly")
    
    def test_get_role_server_error(self, mock_roles_api):
        """Test server error handling"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = json.dumps({
            "errors": [{
                "status": "500",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred while retrieving the role",
                "source": {
                    "resource": {
                        "id": "project_user",
                        "type": "globalroles"
                    }
                }
            }]
        })
        mock_roles_api._session.get.return_value = mock_response
        
        response = mock_roles_api.get_role(role_id='project_user')
        
        assert response.status_code == 500
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['status'] == '500'
        
        print("\n✓ Server error handled correctly (500)")
    
    def test_get_role_unauthorized(self, mock_roles_api):
        """Test unauthorized access"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = json.dumps({
            "errors": [{
                "status": "401",
                "title": "Unauthorized",
                "detail": "Authentication token is invalid or expired"
            }]
        })
        mock_roles_api._session.get.return_value = mock_response
        
        response = mock_roles_api.get_role(role_id='project_user')
        
        assert response.status_code == 401
        
        print("\n✓ Unauthorized access handled correctly (401)")
    
    def test_get_role_with_special_chars_in_id(self, mock_roles_api):
        """Test getting role with special characters in ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "globalroles",
                "id": "role-2024_Q1",
                "attributes": {
                    "name": "Role 2024 Q1"
                }
            }
        }
        mock_roles_api._session.get.return_value = mock_response
        
        response = mock_roles_api.get_role(role_id='role-2024_Q1')
        
        assert response.status_code == 200
        
        # Verify special characters in ID are preserved in URL
        call_args = mock_roles_api._session.get.call_args
        assert 'role-2024_Q1' in call_args[0][0]
        
        print("\n✓ Role ID with special chars handled correctly (200)")


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
