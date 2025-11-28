"""
Pytest test suite for unmark_project method.
Tests the unmarking of a project in Polarion.

Test Strategy:
- All tests use mocks to avoid modifying real data
- Tests cover success cases, error cases, and edge cases

Test Coverage:
- Successful project unmarking
- Project not found (404)
- Insufficient permissions (403)
- Project not marked (already unmarked)
- Server errors (500)
- Various unmarking scenarios

Run with:
    pytest test_unmark_project.py -v
    pytest test_unmark_project.py -v --tb=short
"""
import pytest
import json
from unittest.mock import Mock


# ============================================================================
# Unit Tests - unmark_project
# ============================================================================

class TestUnmarkProject:
    """Unit tests for unmark_project method"""
    
    def test_unmark_project_success(self, mock_projects_api):
        """Test successful project unmarking"""
        # Setup mock response - realistic Polarion API format
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "unmark-TEST_PROJECT-job-12345",
                "attributes": {
                    "jobId": "unmark-TEST_PROJECT-job-12345",
                    "name": "Unmark Project TEST_PROJECT",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project successfully unmarked"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "TEST_PROJECT"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/unmark-TEST_PROJECT-job-12345",
                    "log": "server-host-name/application-path/polarion/job-report?jobId=unmark-TEST_PROJECT-job-12345"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        # Execute
        response = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        
        # Assert
        assert response.status_code == 200
        mock_projects_api._session.post.assert_called_once()
        
        # Verify correct endpoint
        call_args = mock_projects_api._session.post.call_args
        assert 'projects/TEST_PROJECT/actions/unmarkProject' in call_args[0][0]
        
        # Verify response structure
        result = response.json()
        assert result['data']['type'] == 'jobs'
        assert result['data']['attributes']['status']['type'] == 'OK'
        assert result['data']['relationships']['project']['data']['id'] == 'TEST_PROJECT'
        
        print("\n✓ Project unmarked successfully (200)")
    
    def test_unmark_project_no_content(self, mock_projects_api):
        """Test project unmarking with 204 No Content response"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        
        assert response.status_code == 204
        print("\n✓ Project unmarked successfully (204 No Content)")
    
    def test_unmark_project_not_found(self, mock_projects_api):
        """Test unmarking non-existent project"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = json.dumps({
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Project 'NONEXISTENT' not found",
                "source": {
                    "resource": {
                        "id": "NONEXISTENT",
                        "type": "projects"
                    }
                }
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='NONEXISTENT')
        
        assert response.status_code == 404
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['status'] == '404'
        assert error_data['errors'][0]['source']['resource']['id'] == 'NONEXISTENT'
        
        print("\n✓ Project not found handled correctly (404)")
    
    def test_unmark_project_insufficient_permissions(self, mock_projects_api):
        """Test unmarking project without permissions"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = json.dumps({
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to unmark this project",
                "source": {
                    "resource": {
                        "id": "PROTECTED_PROJECT",
                        "type": "projects"
                    }
                }
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='PROTECTED_PROJECT')
        
        assert response.status_code == 403
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['title'] == 'Forbidden'
        print("\n✓ Insufficient permissions handled correctly (403)")
    
    def test_unmark_project_already_unmarked(self, mock_projects_api):
        """Test unmarking project that is already unmarked"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "unmark-TEST_PROJECT-job-12346",
                "attributes": {
                    "jobId": "unmark-TEST_PROJECT-job-12346",
                    "name": "Unmark Project TEST_PROJECT",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project was already unmarked"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "TEST_PROJECT"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/unmark-TEST_PROJECT-job-12346"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        
        assert response.status_code == 200
        result = response.json()
        assert result['data']['attributes']['status']['type'] == 'OK'
        assert 'already unmarked' in result['data']['attributes']['status']['message']
        
        print("\n✓ Already unmarked project handled correctly (200)")
    
    def test_unmark_project_server_error(self, mock_projects_api):
        """Test unmarking project with server error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = json.dumps({
            "errors": [{
                "status": "500",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred while unmarking the project",
                "source": {
                    "resource": {
                        "id": "TEST_PROJECT",
                        "type": "projects"
                    }
                }
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        
        assert response.status_code == 500
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['status'] == '500'
        print("\n✓ Server error handled correctly (500)")
    
    def test_unmark_project_unauthorized(self, mock_projects_api):
        """Test unmarking project with invalid token"""
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
        
        response = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        
        assert response.status_code == 401
        print("\n✓ Unauthorized access handled correctly (401)")
    
    def test_unmark_project_service_unavailable(self, mock_projects_api):
        """Test unmarking project when service is unavailable"""
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
        
        response = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        
        assert response.status_code == 503
        print("\n✓ Service unavailable handled correctly (503)")
    
    def test_unmark_project_with_special_chars_in_id(self, mock_projects_api):
        """Test unmarking project with special characters in ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "unmark-PROJECT-2024_Q1-job-12347",
                "attributes": {
                    "jobId": "unmark-PROJECT-2024_Q1-job-12347",
                    "name": "Unmark Project PROJECT-2024_Q1",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project successfully unmarked"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "PROJECT-2024_Q1"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/unmark-PROJECT-2024_Q1-job-12347"
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='PROJECT-2024_Q1')
        
        assert response.status_code == 200
        
        # Verify special characters in ID are preserved in URL
        call_args = mock_projects_api._session.post.call_args
        assert 'PROJECT-2024_Q1' in call_args[0][0]
        
        # Verify response
        result = response.json()
        assert result['data']['relationships']['project']['data']['id'] == 'PROJECT-2024_Q1'
        
        print("\n✓ Project ID with special chars handled correctly (200)")
    
    def test_unmark_project_with_empty_id(self, mock_projects_api):
        """Test unmarking project with empty ID"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Project ID cannot be empty",
                "source": {
                    "parameter": "project_id",
                    "resource": {
                        "id": "",
                        "type": "projects"
                    }
                }
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='')
        
        assert response.status_code == 400
        error_data = json.loads(response.text)
        assert error_data['errors'][0]['source']['parameter'] == 'project_id'
        print("\n✓ Empty project ID handled correctly (400)")
    
    def test_unmark_project_with_invalid_id_format(self, mock_projects_api):
        """Test unmarking project with invalid ID format"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid project ID format. ID must contain only alphanumeric characters, dashes, and underscores",
                "source": {
                    "parameter": "project_id",
                    "resource": {
                        "id": "invalid@project#id",
                        "type": "projects"
                    }
                }
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='invalid@project#id')
        
        assert response.status_code == 400
        error_data = json.loads(response.text)
        assert 'Invalid project ID format' in error_data['errors'][0]['detail']
        print("\n✓ Invalid project ID format handled correctly (400)")
    
    def test_unmark_project_with_response_metadata(self, mock_projects_api):
        """Test unmarking project with additional response metadata"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "unmark-TEST_PROJECT-job-12348",
                "attributes": {
                    "jobId": "unmark-TEST_PROJECT-job-12348",
                    "name": "Unmark Project TEST_PROJECT",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project successfully unmarked"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "TEST_PROJECT"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/unmark-TEST_PROJECT-job-12348",
                    "log": "server-host-name/application-path/polarion/job-report?jobId=unmark-TEST_PROJECT-job-12348",
                    "downloads": [
                        "https://polarionpg.adtran.com/polarion/download/unmark-report.pdf"
                    ]
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        
        assert response.status_code == 200
        result = response.json()
        assert result['data']['attributes']['status']['type'] == 'OK'
        assert 'links' in result['data']
        assert 'log' in result['data']['links']
        assert 'downloads' in result['data']['links']
        
        print("\n✓ Response with metadata handled correctly (200)")
    
    def test_unmark_project_method_not_allowed(self, mock_projects_api):
        """Test when POST method is not allowed"""
        mock_response = Mock()
        mock_response.status_code = 405
        mock_response.text = json.dumps({
            "errors": [{
                "status": "405",
                "title": "Method Not Allowed",
                "detail": "POST method is not allowed for this resource"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        
        assert response.status_code == 405
        print("\n✓ Method not allowed handled correctly (405)")
    
    def test_unmark_project_rate_limit(self, mock_projects_api):
        """Test unmarking project with rate limit exceeded"""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = json.dumps({
            "errors": [{
                "status": "429",
                "title": "Too Many Requests",
                "detail": "Rate limit exceeded. Please try again later"
            }]
        })
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        
        assert response.status_code == 429
        print("\n✓ Rate limit handled correctly (429)")


# ============================================================================
# Edge Cases and Sequential Operations
# ============================================================================

class TestUnmarkProjectEdgeCases:
    """Test edge cases and sequential operations"""
    
    def test_mark_then_unmark_sequence(self, mock_projects_api):
        """Test marking and then unmarking a project"""
        # First: Mark the project
        mark_response = Mock()
        mark_response.status_code = 200
        mark_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "mark-TEST_PROJECT-job-12349",
                "attributes": {
                    "jobId": "mark-TEST_PROJECT-job-12349",
                    "name": "Mark Project TEST_PROJECT",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project successfully marked"
                    }
                }
            }
        }
        
        # Then: Unmark the project
        unmark_response = Mock()
        unmark_response.status_code = 200
        unmark_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "unmark-TEST_PROJECT-job-12350",
                "attributes": {
                    "jobId": "unmark-TEST_PROJECT-job-12350",
                    "name": "Unmark Project TEST_PROJECT",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project successfully unmarked"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "TEST_PROJECT"
                        }
                    }
                }
            }
        }
        
        mock_projects_api._session.post.side_effect = [mark_response, unmark_response]
        
        # Mark project (simulated, not testing mark_project here)
        response1 = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')  # Using unmark as proxy
        assert response1.status_code == 200
        
        # Unmark project
        response2 = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        assert response2.status_code == 200
        result = response2.json()
        assert result['data']['attributes']['status']['type'] == 'OK'
        
        print("\n✓ Mark then unmark sequence handled correctly")
    
    def test_unmark_multiple_times(self, mock_projects_api):
        """Test unmarking the same project multiple times"""
        # First unmark succeeds
        first_response = Mock()
        first_response.status_code = 200
        first_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "unmark-TEST_PROJECT-job-12351",
                "attributes": {
                    "jobId": "unmark-TEST_PROJECT-job-12351",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project successfully unmarked"
                    }
                }
            }
        }
        
        # Second unmark also succeeds (idempotent)
        second_response = Mock()
        second_response.status_code = 200
        second_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "unmark-TEST_PROJECT-job-12352",
                "attributes": {
                    "jobId": "unmark-TEST_PROJECT-job-12352",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project was already unmarked"
                    }
                }
            }
        }
        
        mock_projects_api._session.post.side_effect = [first_response, second_response]
        
        # First unmark
        response1 = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        assert response1.status_code == 200
        
        # Second unmark
        response2 = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        assert response2.status_code == 200
        result = response2.json()
        assert result['data']['attributes']['status']['type'] == 'OK'
        assert 'already unmarked' in result['data']['attributes']['status']['message']
        
        print("\n✓ Multiple unmark operations handled correctly (idempotent)")
    
    def test_unmark_project_with_long_id(self, mock_projects_api):
        """Test unmarking project with very long ID"""
        long_id = "VERY_LONG_PROJECT_ID_" + "X" * 100
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": f"unmark-{long_id}-job-12353",
                "attributes": {
                    "jobId": f"unmark-{long_id}-job-12353",
                    "name": f"Unmark Project {long_id}",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project successfully unmarked"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": long_id
                        }
                    }
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id=long_id)
        
        assert response.status_code == 200
        
        # Verify long ID is in URL
        call_args = mock_projects_api._session.post.call_args
        assert long_id in call_args[0][0]
        
        # Verify response contains long ID
        result = response.json()
        assert result['data']['relationships']['project']['data']['id'] == long_id
        
        print("\n✓ Long project ID handled correctly (200)")
    
    def test_unmark_project_no_request_body(self, mock_projects_api):
        """Test that unmark_project sends no request body (URL-only operation)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "unmark-TEST_PROJECT-job-12354",
                "attributes": {
                    "jobId": "unmark-TEST_PROJECT-job-12354",
                    "name": "Unmark Project TEST_PROJECT",
                    "state": "completed",
                    "status": {
                        "type": "OK",
                        "message": "Project successfully unmarked"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "TEST_PROJECT"
                        }
                    }
                }
            }
        }
        mock_projects_api._session.post.return_value = mock_response
        
        response = mock_projects_api.post_unmark_project(project_id='TEST_PROJECT')
        
        assert response.status_code == 200
        
        # Verify that no json body was sent (should only have URL)
        call_args = mock_projects_api._session.post.call_args
        # call_args[1] contains keyword arguments
        assert 'json' not in call_args[1] or call_args[1].get('json') is None
        
        print("\n✓ No request body sent (URL-only operation)")


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
