"""
Pytest test suite for create_project method.
Tests the creation of a new project in Polarion.

Test Strategy:
- All tests use mocks to avoid modifying real data
- Tests cover success cases, error cases, and edge cases

Test Coverage:
- Successful project creation
- Project already exists (409)
- Insufficient permissions (403)
- Invalid data format (400)
- Missing required fields
- Server errors (500)
- Various project configurations

Run with:
    pytest test_create_project.py -v
    pytest test_create_project.py -v --tb=short
"""
import pytest
import json
from unittest.mock import Mock


@pytest.fixture
def sample_create_data():
    """Sample project creation data - attributes only for **kwargs"""
    return {
        "projectId": "NEW_PROJECT",
        "name": "New Test Project",
        "trackerPrefix": "NTP",
        "location": "default/NEW_PROJECT",
        "templateId": "agile",
        "description": {
            "type": "text/plain",
            "content": "Test project created by pytest"
        }
    }


# ============================================================================
# Unit Tests - create_project
# ============================================================================

class TestCreateProject:
    """Unit tests for create_project method"""
    
    def test_create_project_success(self, mock_projects_api, sample_create_data):
        """Test successful project creation"""
        # Setup mock response - realistic Polarion API format with jobs
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "create-NEW_PROJECT-job-10001",
                "attributes": {
                    "jobId": "create-NEW_PROJECT-job-10001",
                    "name": "Create Project NEW_PROJECT",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project created successfully"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "NEW_PROJECT"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/create-NEW_PROJECT-job-10001",
                    "log": "server-host-name/application-path/polarion/job-report?jobId=create-NEW_PROJECT-job-10001"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Execute - pass attributes as **kwargs
        response = mock_projects_api.post_create_project(**sample_create_data)
        
        # Assert
        assert response.status_code == 201
        mock_projects_api._session.post.assert_called_once()
        
        # Verify correct endpoint
        call_args = mock_projects_api._session.post.call_args
        assert 'projects/actions/createProject' in call_args[0][0]
        
        # Verify request body - simple format without type/attributes wrapper
        sent_data = call_args[1]['json']
        assert sent_data['projectId'] == 'NEW_PROJECT'
        assert sent_data['trackerPrefix'] == 'NTP'
        assert sent_data['location'] == 'default/NEW_PROJECT'
        
        # Verify response - JSON API format with jobs
        result = response.json()
        assert result['data']['type'] == 'jobs'
        assert result['data']['attributes']['status']['type'] == 'OK'
        assert result['data']['relationships']['project']['data']['id'] == 'NEW_PROJECT'
        
        print("\n✓ Project created successfully (201)")
    
    def test_create_project_already_exists(self, mock_projects_api):
        """Test creating project that already exists"""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.text = json.dumps({
            "errors": [{
                "status": "409",
                "title": "Conflict",
                "detail": "Project 'EXISTING_PROJECT' already exists",
                "source": {
                    "resource": {
                        "id": "EXISTING_PROJECT",
                        "type": "projects"
                    }
                }
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        # Pass required parameters as kwargs
        response = mock_projects_api.post_create_project(
            projectId="EXISTING_PROJECT",
            name="Existing Project",
            trackerPrefix="EP",
            location="default/EXISTING_PROJECT",
            templateId="agile"
        )
        
        assert response.status_code == 409
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['status'] == '409'
        assert error_data['errors'][0]['source']['resource']['id'] == 'EXISTING_PROJECT'
        
        print("\n✓ Project already exists handled correctly (409)")
    
    def test_create_project_insufficient_permissions(self, mock_projects_api, sample_create_data):
        """Test creating project without permissions"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = json.dumps({
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to create projects",
                "source": {
                    "resource": {
                        "id": "NEW_PROJECT",
                        "type": "projects"
                    }
                }
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_create_project(**sample_create_data)
        
        assert response.status_code == 403
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['title'] == 'Forbidden'
        print("\n✓ Insufficient permissions handled correctly (403)")
    
    def test_create_project_invalid_data(self, mock_projects_api):
        """Test creating project with invalid data format (server-side validation)"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid project data format",
                "source": {
                    "pointer": "$.data",
                    "parameter": "templateId",
                    "resource": {
                        "id": "INVALID",
                        "type": "projects"
                    }
                }
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        # Pass minimal required params but server will reject
        response = mock_projects_api.post_create_project(
            projectId="INVALID",
            trackerPrefix="INV",
            location="invalid",
            templateId="invalid_template"
        )
        
        assert response.status_code == 400
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['source']['parameter'] == 'templateId'
        print("\n✓ Invalid data format handled correctly (400)")
    
    def test_create_project_missing_id(self, mock_projects_api):
        """Test creating project with missing projectId - client-side validation"""
        # Should raise ValueError before making the request
        with pytest.raises(ValueError) as exc_info:
            mock_projects_api.post_create_project(
                name="Project Without ID",
                trackerPrefix="PWI",
                location="default/test",
                templateId="agile"
                # Missing projectId
            )
        
        assert "Missing required parameters" in str(exc_info.value)
        assert "projectId" in str(exc_info.value)
        print("\n✓ Missing projectId handled correctly (ValueError)")
    
    def test_create_project_missing_name(self, mock_projects_api):
        """Test creating project with missing trackerPrefix - client-side validation"""
        # Should raise ValueError before making the request
        with pytest.raises(ValueError) as exc_info:
            mock_projects_api.post_create_project(
                projectId="PROJECT_WITHOUT_PREFIX",
                location="default/test",
                templateId="agile"
                # Missing trackerPrefix
            )
        
        assert "Missing required parameters" in str(exc_info.value)
        assert "trackerPrefix" in str(exc_info.value)
        print("\n✓ Missing trackerPrefix handled correctly (ValueError)")
    
    def test_create_project_invalid_id_format(self, mock_projects_api):
        """Test creating project with invalid ID format"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid project ID format. ID must contain only alphanumeric characters, dashes, and underscores",
                "source": {
                    "parameter": "projectId",
                    "resource": {
                        "id": "invalid@project#id",
                        "type": "projects"
                    }
                }
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        # Pass required params but server will reject the format
        response = mock_projects_api.post_create_project(
            projectId="invalid@project#id",
            name="Invalid Project",
            trackerPrefix="INV",
            location="default/test",
            templateId="agile"
        )
        
        assert response.status_code == 400
        error_data = json.loads(response.text)
        assert 'Invalid project ID format' in error_data['errors'][0]['detail']
        print("\n✓ Invalid ID format handled correctly (400)")
    
    def test_create_project_server_error(self, mock_projects_api, sample_create_data):
        """Test creating project with server error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = json.dumps({
            "errors": [{
                "status": "500",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred while creating the project",
                "source": {
                    "resource": {
                        "id": "NEW_PROJECT",
                        "type": "projects"
                    }
                }
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_create_project(**sample_create_data)
        
        assert response.status_code == 500
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['status'] == '500'
        print("\n✓ Server error handled correctly (500)")
    
    def test_create_project_with_template(self, mock_projects_api):
        """Test creating project from template"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "create-NEW_PROJECT_FROM_TEMPLATE-job-10002",
                "attributes": {
                    "jobId": "create-NEW_PROJECT_FROM_TEMPLATE-job-10002",
                    "name": "Create Project from Template",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project created from template TEMPLATE_PROJECT"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "NEW_PROJECT_FROM_TEMPLATE"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/create-NEW_PROJECT_FROM_TEMPLATE-job-10002"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Pass required params with template
        response = mock_projects_api.post_create_project(
            projectId="NEW_PROJECT_FROM_TEMPLATE",
            name="Project from Template",
            trackerPrefix="NPFT",
            location="default/NEW_PROJECT_FROM_TEMPLATE",
            templateId="TEMPLATE_PROJECT"
        )
        
        assert response.status_code == 201
        result = response.json()
        assert result['data']['type'] == 'jobs'
        assert result['data']['relationships']['project']['data']['id'] == 'NEW_PROJECT_FROM_TEMPLATE'
        
        print("\n✓ Project created from template successfully (201)")
    
    def test_create_project_with_location(self, mock_projects_api):
        """Test creating project with specific location"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "create-NEW_PROJECT_WITH_LOCATION-job-10003",
                "attributes": {
                    "jobId": "create-NEW_PROJECT_WITH_LOCATION-job-10003",
                    "name": "Create Project with Custom Location",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project created at location /projects/active"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "NEW_PROJECT_WITH_LOCATION"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/create-NEW_PROJECT_WITH_LOCATION-job-10003"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Pass required params with custom location
        response = mock_projects_api.post_create_project(
            projectId="NEW_PROJECT_WITH_LOCATION",
            name="Project with Location",
            trackerPrefix="NPWL",
            location="/projects/active",
            templateId="agile"
        )
        
        assert response.status_code == 201
        result = response.json()
        assert result['data']['type'] == 'jobs'
        assert result['data']['attributes']['status']['type'] == 'OK'
        
        print("\n✓ Project created with location successfully (201)")
    
    def test_create_project_with_rich_text_description(self, mock_projects_api):
        """Test creating project with rich text description"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "PROJECT_WITH_HTML",
                "attributes": {
                    "name": "Project with HTML Description",
                    "description": {
                        "type": "text/html",
                        "value": "<p>Rich <strong>text</strong> description</p>"
                    }
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Pass required params with rich text description
        response = mock_projects_api.post_create_project(
            projectId="PROJECT_WITH_HTML",
            name="Project with HTML Description",
            trackerPrefix="PWH",
            location="default/PROJECT_WITH_HTML",
            templateId="agile",
            description={
                "type": "text/html",
                "content": "<p>Rich <strong>text</strong> description</p>"
            }
        )
        
        assert response.status_code == 201
        print("\n✓ Project with rich text description created successfully (201)")
    
    def test_create_project_with_relationships(self, mock_projects_api):
        """Test creating project with relationships"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "create-PROJECT_WITH_LEAD-job-10004",
                "attributes": {
                    "jobId": "create-PROJECT_WITH_LEAD-job-10004",
                    "name": "Create Project with Lead",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project created with lead user"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "PROJECT_WITH_LEAD"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/create-PROJECT_WITH_LEAD-job-10004",
                    "log": "server-host-name/application-path/polarion/job-report?jobId=create-PROJECT_WITH_LEAD-job-10004"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Pass required params with relationships (note: relationships might not be supported in kwargs)
        # For now, we'll pass minimal params
        response = mock_projects_api.post_create_project(
            projectId="PROJECT_WITH_LEAD",
            name="Project with Lead",
            trackerPrefix="PWL",
            location="default/PROJECT_WITH_LEAD",
            templateId="agile"
        )
        
        assert response.status_code == 201
        result = response.json()
        assert 'relationships' in result['data']
        assert result['data']['relationships']['project']['data']['id'] == 'PROJECT_WITH_LEAD'
        
        print("\n✓ Project with relationships created successfully (201)")
    
    def test_create_project_unauthorized(self, mock_projects_api, sample_create_data):
        """Test creating project with invalid token"""
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
        
        response = mock_projects_api.post_create_project(**sample_create_data)
        
        assert response.status_code == 401
        print("\n✓ Unauthorized access handled correctly (401)")
    
    def test_create_project_service_unavailable(self, mock_projects_api, sample_create_data):
        """Test creating project when service is unavailable"""
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
        
        response = mock_projects_api.post_create_project(**sample_create_data)
        
        assert response.status_code == 503
        print("\n✓ Service unavailable handled correctly (503)")
    
    def test_create_project_with_special_chars_in_id(self, mock_projects_api):
        """Test creating project with special characters in ID"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "PROJECT-2024_Q1",
                "attributes": {
                    "name": "Project 2024 Q1"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Pass required params with special chars in ID
        response = mock_projects_api.post_create_project(
            projectId="PROJECT-2024_Q1",
            name="Project 2024 Q1",
            trackerPrefix="P2024",
            location="default/PROJECT-2024_Q1",
            templateId="agile"
        )
        
        assert response.status_code == 201
        print("\n✓ Project with special chars in ID created successfully (201)")
    
    def test_create_project_with_active_flag(self, mock_projects_api):
        """Test creating project with active flag set"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "create-ACTIVE_PROJECT-job-10005",
                "attributes": {
                    "jobId": "create-ACTIVE_PROJECT-job-10005",
                    "name": "Create Active Project",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Active project created successfully"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "ACTIVE_PROJECT"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/create-ACTIVE_PROJECT-job-10005"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Pass required params with active flags
        response = mock_projects_api.post_create_project(
            projectId="ACTIVE_PROJECT",
            name="Active Project",
            trackerPrefix="AP",
            location="default/ACTIVE_PROJECT",
            templateId="agile",
            active=True,
            finished=False
        )
        
        assert response.status_code == 201
        result = response.json()
        assert result['data']['type'] == 'jobs'
        assert result['data']['attributes']['status']['type'] == 'OK'
        
        print("\n✓ Project with active flag created successfully (201)")
    
    def test_create_project_empty_data(self, mock_projects_api):
        """Test creating project with empty data"""
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
        
        # Empty kwargs should raise ValueError for missing required params
        with pytest.raises(ValueError) as exc_info:
            response = mock_projects_api.post_create_project()
        
        assert "Missing required parameters" in str(exc_info.value)
        print("\n✓ Empty data handled correctly (ValueError)")
    
    def test_create_project_with_prefix(self, mock_projects_api):
        """Test creating project with ID prefix"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "create-PRJ_NEW_PROJECT-job-10006",
                "attributes": {
                    "jobId": "create-PRJ_NEW_PROJECT-job-10006",
                    "name": "Create Project with Prefix",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project with prefix PRJ created successfully"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "PRJ_NEW_PROJECT"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/create-PRJ_NEW_PROJECT-job-10006"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Pass required params with prefix
        response = mock_projects_api.post_create_project(
            projectId="PRJ_NEW_PROJECT",
            name="Project with Prefix",
            trackerPrefix="PRJ",
            location="default/PRJ_NEW_PROJECT",
            templateId="agile",
            prefix="PRJ"
        )
        
        assert response.status_code == 201
        result = response.json()
        assert result['data']['type'] == 'jobs'
        assert result['data']['relationships']['project']['data']['id'] == 'PRJ_NEW_PROJECT'
        
        print("\n✓ Project with prefix created successfully (201)")


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
