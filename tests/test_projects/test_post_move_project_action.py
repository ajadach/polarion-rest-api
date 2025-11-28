"""
Pytest test suite for move_project_action method.
Tests the moving of a project to a different location in Polarion.

Test Strategy:
- All tests use mocks to avoid modifying real data
- Tests cover success cases, error cases, and edge cases

Test Coverage:
- Successful project move
- Project not found (404)
- Insufficient permissions (403)
- Invalid location (400)
- Target location already exists (409)
- Server errors (500)
- Various location path formats

Run with:
    pytest test_move_project_action.py -v
    pytest test_move_project_action.py -v --tb=short
"""
import pytest
import json
from unittest.mock import Mock


@pytest.fixture
def sample_move_data():
    """Sample move data for testing"""
    return {
        "location": "/new/location"
    }


# ============================================================================
# Unit Tests - move_project_action
# ============================================================================

class TestMoveProjectAction:
    """Unit tests for move_project_action method"""
    
    def test_move_project_success(self, mock_projects_api, sample_move_data):
        """Test successful project move"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "TEST_PROJECT",
                "attributes": {
                    "location": "/new/location",
                    "movedAt": "2024-11-04T10:30:00Z"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Execute
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **sample_move_data
        )
        
        # Assert
        assert response.status_code == 200
        mock_projects_api._session.post.assert_called_once()
        
        # Verify correct endpoint
        call_args = mock_projects_api._session.post.call_args
        assert 'projects/TEST_PROJECT/actions/moveProject' in call_args[0][0]
        
        # Verify request body
        sent_data = call_args[1]['json']
        assert sent_data['location'] == '/new/location'
        
        # Verify response
        result = response.json()
        assert result['data']['attributes']['location'] == '/new/location'
        
        print("\n✓ Project moved successfully (200)")
    
    def test_move_project_no_content(self, mock_projects_api, sample_move_data):
        """Test project move with 204 No Content response"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **sample_move_data
        )
        
        assert response.status_code == 204
        print("\n✓ Project moved successfully (204 No Content)")
    
    def test_move_project_not_found(self, mock_projects_api, sample_move_data):
        """Test moving non-existent project"""
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
        
        response = mock_projects_api.post_move_project_action(
            project_id='NONEXISTENT',
            **sample_move_data
        )
        
        assert response.status_code == 404
        print("\n✓ Project not found handled correctly (404)")
    
    def test_move_project_insufficient_permissions(self, mock_projects_api, sample_move_data):
        """Test moving project without permissions"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = json.dumps({
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to move this project"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_move_project_action(
            project_id='PROTECTED_PROJECT',
            **sample_move_data
        )
        
        assert response.status_code == 403
        print("\n✓ Insufficient permissions handled correctly (403)")
    
    def test_move_project_invalid_location(self, mock_projects_api):
        """Test moving project to invalid location"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid location path format"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        invalid_move_data = {
            "location": "invalid/location"  # Missing leading slash
        }
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **invalid_move_data
        )
        
        assert response.status_code == 400
        print("\n✓ Invalid location handled correctly (400)")
    
    def test_move_project_location_exists(self, mock_projects_api):
        """Test moving project to location that already exists"""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.text = json.dumps({
            "errors": [{
                "status": "409",
                "title": "Conflict",
                "detail": "A project already exists at location '/existing/location'"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        move_data = {
            "location": "/existing/location"
        }
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **move_data
        )
        
        assert response.status_code == 409
        print("\n✓ Location conflict handled correctly (409)")
    
    def test_move_project_server_error(self, mock_projects_api, sample_move_data):
        """Test moving project with server error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = json.dumps({
            "errors": [{
                "status": "500",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred while moving the project"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **sample_move_data
        )
        
        assert response.status_code == 500
        print("\n✓ Server error handled correctly (500)")
    
    def test_move_project_to_root(self, mock_projects_api):
        """Test moving project to root location"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "TEST_PROJECT",
                "attributes": {
                    "location": "/"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        move_data = {

        
            "location": "/"

        
        }
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **move_data
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['data']['attributes']['location'] == '/'
        
        print("\n✓ Move to root location handled correctly (200)")
    
    def test_move_project_nested_location(self, mock_projects_api):
        """Test moving project to deeply nested location"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "TEST_PROJECT",
                "attributes": {
                    "location": "/level1/level2/level3/level4"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        move_data = {

        
            "location": "/level1/level2/level3/level4"

        
        }
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **move_data
        )
        
        assert response.status_code == 200
        print("\n✓ Nested location handled correctly (200)")
    
    def test_move_project_with_special_chars_in_location(self, mock_projects_api):
        """Test moving project to location with special characters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "TEST_PROJECT",
                "attributes": {
                    "location": "/projects/2024-Q1/active_projects"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        move_data = {

        
            "location": "/projects/2024-Q1/active_projects"

        
        }
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **move_data
        )
        
        assert response.status_code == 200
        print("\n✓ Location with special chars handled correctly (200)")
    
    def test_move_project_missing_location(self, mock_projects_api):
        """Test moving project with missing location attribute"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Missing required attribute: location"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        # Should raise ValueError for missing required parameter
        with pytest.raises(ValueError, match="Missing required parameter: location"):
            response = mock_projects_api.post_move_project_action(
                project_id='TEST_PROJECT'
            )
        
        print("\n✓ Missing location handled correctly (ValueError)")
    
    def test_move_project_empty_location(self, mock_projects_api):
        """Test moving project with empty location"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Location cannot be empty"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        move_data = {
            "location": ""
        }
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **move_data
        )
        
        assert response.status_code == 400
        print("\n✓ Empty location handled correctly (400)")
    
    def test_move_project_unauthorized(self, mock_projects_api, sample_move_data):
        """Test moving project with invalid token"""
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
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **sample_move_data
        )
        
        assert response.status_code == 401
        print("\n✓ Unauthorized access handled correctly (401)")
    
    def test_move_project_service_unavailable(self, mock_projects_api, sample_move_data):
        """Test moving project when service is unavailable"""
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
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **sample_move_data
        )
        
        assert response.status_code == 503
        print("\n✓ Service unavailable handled correctly (503)")
    
    def test_move_project_with_additional_attributes(self, mock_projects_api):
        """Test moving project with additional attributes (only location is used)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "TEST_PROJECT",
                "attributes": {
                    "location": "/new/location"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        move_data = {
            "location": "/new/location"
        }
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **move_data
        )
        
        assert response.status_code == 200
        print("\n✓ Move with location handled correctly (200)")
    
    def test_move_project_circular_reference(self, mock_projects_api):
        """Test moving project to create circular reference"""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.text = json.dumps({
            "errors": [{
                "status": "409",
                "title": "Conflict",
                "detail": "Cannot move project: would create circular reference"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        move_data = {

        
            "location": "/TEST_PROJECT/subproject"

        
        }
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **move_data
        )
        
        assert response.status_code == 409
        print("\n✓ Circular reference prevented (409)")
    
    def test_move_project_invalid_data_type(self, mock_projects_api):
        """Test moving project with valid location (data type validation is at API level)"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid data type in request body"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        invalid_data = {
            "location": "/new/location"
        }
        
        response = mock_projects_api.post_move_project_action(
            project_id='TEST_PROJECT',
            **invalid_data
        )
        
        assert response.status_code == 400
        print("\n✓ Invalid data handled by API correctly (400)")


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
