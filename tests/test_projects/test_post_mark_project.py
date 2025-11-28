"""
Pytest test suite for mark_project method.
Tests the marking of a project in Polarion.

Test Strategy:
- All tests use mocks to avoid modifying real data
- Tests cover success cases, error cases, and edge cases

Test Coverage:
- Successful project marking
- Project not found (404)
- Insufficient permissions (403)
- Invalid data format (400)
- Project already marked
- Server errors (500)
- Multiple projects marking

Run with:
    pytest test_mark_project.py -v
    pytest test_mark_project.py -v --tb=short
"""
import pytest
import json
from unittest.mock import Mock


@pytest.fixture
def sample_mark_data():
    """Sample mark data for testing"""
    return {
        "projectId": "TEST_PROJECT",
        "trackerPrefix": "TEST",
        "location": "test/location",
        "templateId": "default_template",
        "params": {}
    }


# ============================================================================
# Unit Tests - mark_project
# ============================================================================

class TestMarkProject:
    """Unit tests for mark_project method"""
    
    def test_mark_project_success(self, mock_projects_api, sample_mark_data):
        """Test successful project marking"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "TEST_PROJECT",
                "attributes": {
                    "marked": True,
                    "markedAt": "2024-11-04T10:30:00Z"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Execute
        response = mock_projects_api.post_mark_project(**sample_mark_data)
        
        # Assert
        assert response.status_code == 200
        mock_projects_api._session.post.assert_called_once()
        
        # Verify correct endpoint
        call_args = mock_projects_api._session.post.call_args
        assert 'projects/actions/markProject' in call_args[0][0]
        
        # Verify request body
        sent_data = call_args[1]['json']
        assert sent_data['projectId'] == 'TEST_PROJECT'
        assert sent_data['trackerPrefix'] == 'TEST'
        assert sent_data['location'] == 'test/location'
        assert sent_data['templateId'] == 'default_template'
        
        # Verify response
        result = response.json()
        assert result['data']['attributes']['marked'] is True
        
        print("\n✓ Project marked successfully (200)")
    
    def test_mark_project_no_content(self, mock_projects_api, sample_mark_data):
        """Test project marking with 204 No Content response"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_mark_project(**sample_mark_data)
        
        assert response.status_code == 204
        print("\n✓ Project marked successfully (204 No Content)")
    
    def test_mark_project_not_found(self, mock_projects_api):
        """Test marking non-existent project"""
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
        
        mark_data = {
            "projectId": "NONEXISTENT",
            "trackerPrefix": "TEST",
            "location": "test/location",
            "templateId": "default_template"
        }
        
        response = mock_projects_api.post_mark_project(**mark_data)
        
        assert response.status_code == 404
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['status'] == '404'
        
        print("\n✓ Project not found handled correctly (404)")
    
    def test_mark_project_insufficient_permissions(self, mock_projects_api, sample_mark_data):
        """Test marking project without permissions"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = json.dumps({
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to mark this project"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_mark_project(**sample_mark_data)
        
        assert response.status_code == 403
        print("\n✓ Insufficient permissions handled correctly (403)")
    
    def test_mark_project_invalid_data(self, mock_projects_api):
        """Test marking project with invalid data format"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid request body format"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        invalid_data = {
            "projectId": "TEST_PROJECT",
            "trackerPrefix": "TEST",
            "location": "test/location",
            "templateId": "default_template"
        }
        
        response = mock_projects_api.post_mark_project(**invalid_data)
        
        assert response.status_code == 400
        print("\n✓ Invalid data format handled correctly (400)")
    
    def test_mark_project_already_marked(self, mock_projects_api, sample_mark_data):
        """Test marking project that is already marked"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "TEST_PROJECT",
                "attributes": {
                    "marked": True,
                    "message": "Project was already marked"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_mark_project(**sample_mark_data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['data']['attributes']['marked'] is True
        
        print("\n✓ Already marked project handled correctly (200)")
    
    def test_mark_project_server_error(self, mock_projects_api, sample_mark_data):
        """Test marking project with server error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = json.dumps({
            "errors": [{
                "status": "500",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred while marking the project"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_mark_project(**sample_mark_data)
        
        assert response.status_code == 500
        print("\n✓ Server error handled correctly (500)")
    
    def test_mark_project_unauthorized(self, mock_projects_api, sample_mark_data):
        """Test marking project with invalid token"""
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
        
        response = mock_projects_api.post_mark_project(**sample_mark_data)
        
        assert response.status_code == 401
        print("\n✓ Unauthorized access handled correctly (401)")
    
    def test_mark_project_with_additional_attributes(self, mock_projects_api):
        """Test marking project with additional attributes"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "TEST_PROJECT",
                "attributes": {
                    "marked": True
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        mark_data = {
            "projectId": "TEST_PROJECT",
            "trackerPrefix": "TEST",
            "location": "test/location",
            "templateId": "default_template",
            "params": {
                "reason": "Important project",
                "priority": "high"
            }
        }
        
        response = mock_projects_api.post_mark_project(**mark_data)
        
        assert response.status_code == 200
        
        # Verify additional params were sent
        call_args = mock_projects_api._session.post.call_args
        sent_data = call_args[1]['json']
        assert 'params' in sent_data
        assert sent_data['params']['reason'] == 'Important project'
        
        print("\n✓ Marking with additional attributes handled correctly (200)")
    
    def test_mark_project_with_special_chars_in_id(self, mock_projects_api):
        """Test marking project with special characters in ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "PROJECT-2024_Q1",
                "attributes": {
                    "marked": True
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        mark_data = {
            "projectId": "PROJECT-2024_Q1",
            "trackerPrefix": "PRJ",
            "location": "test/location",
            "templateId": "default_template"
        }
        
        response = mock_projects_api.post_mark_project(**mark_data)
        
        assert response.status_code == 200
        print("\n✓ Project ID with special chars handled correctly (200)")
    
    def test_mark_project_service_unavailable(self, mock_projects_api, sample_mark_data):
        """Test marking project when service is unavailable"""
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
        
        response = mock_projects_api.post_mark_project(**sample_mark_data)
        
        assert response.status_code == 503
        print("\n✓ Service unavailable handled correctly (503)")
    
    def test_mark_project_missing_required_fields(self, mock_projects_api):
        """Test marking project with missing required fields"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Missing required field: id"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        # Missing required field 'projectId'
        invalid_data = {
            "trackerPrefix": "TEST",
            "location": "test/location",
            "templateId": "default_template"
        }
        
        # Should raise ValueError for missing required parameter
        with pytest.raises(ValueError, match="Missing required parameters"):
            response = mock_projects_api.post_mark_project(**invalid_data)
        
        print("\n✓ Missing required fields handled correctly (ValueError)")
    
    def test_mark_project_empty_data(self, mock_projects_api):
        """Test marking project with empty data"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Request body cannot be empty"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        # Empty data should raise ValueError for missing required parameters
        with pytest.raises(ValueError, match="Missing required parameters"):
            response = mock_projects_api.post_mark_project()
        
        print("\n✓ Empty data handled correctly (ValueError)")
    
    def test_mark_project_with_relationships(self, mock_projects_api):
        """Test marking project with relationships"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "TEST_PROJECT",
                "attributes": {
                    "marked": True
                },
                "relationships": {
                    "lead": {
                        "data": {
                            "type": "users",
                            "id": "user123"
                        }
                    }
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        mark_data = {
            "projectId": "TEST_PROJECT",
            "trackerPrefix": "TEST",
            "location": "test/location",
            "templateId": "default_template",
            "params": {
                "lead": {
                    "type": "users",
                    "id": "user123"
                }
            }
        }
        
        response = mock_projects_api.post_mark_project(**mark_data)
        
        assert response.status_code == 200
        result = response.json()
        assert 'relationships' in result['data']
        
        # Verify params with lead were sent
        call_args = mock_projects_api._session.post.call_args
        sent_data = call_args[1]['json']
        assert 'params' in sent_data
        assert 'lead' in sent_data['params']
        
        print("\n✓ Marking with relationships handled correctly (200)")


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
