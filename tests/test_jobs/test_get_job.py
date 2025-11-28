"""
Pytest tests for get_job method in Jobs class.

Tests the GET /jobs/{jobId} endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_get_job.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.get
class TestGetJob:
    """Unit tests for get_job method using mocks"""
    
    def test_get_job_success_200(self, mock_jobs_api):
        """Test successful job retrieval with 200 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 200 status code (user provided 201 but GET returns 200)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "MyJobId",
                "revision": "1234",
                "attributes": {
                    "jobId": "example",
                    "name": "example",
                    "state": "example",
                    "status": {
                        "type": "OK",
                        "message": "message"
                    }
                },
                "relationships": {
                    "document": {
                        "data": {
                            "type": "documents",
                            "id": "MyProjectId/MySpaceId/MyDocumentId",
                            "revision": "1234"
                        }
                    },
                    "documents": {
                        "data": [
                            {
                                "type": "documents",
                                "id": "MyProjectId/MySpaceId/MyDocumentId",
                                "revision": "1234"
                            }
                        ],
                        "meta": {
                            "totalCount": 0
                        }
                    },
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "MyProjectId",
                            "revision": "1234"
                        }
                    }
                },
                "meta": {
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
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/MyJobId",
                    "log": "server-host-name/application-path/polarion/job-report?jobId=MyJobId",
                    "downloads": [
                        "https://testdrive.polarion.com/polarion/download/filename1",
                        "https://testdrive.polarion.com/polarion/download/filename2"
                    ]
                }
            },
            "included": [
                {}
            ],
            "links": {
                "self": "server-host-name/application-path/jobs/MyJobId"
            }
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert 'data' in response_data
        assert response_data['data']['type'] == 'jobs'
        assert response_data['data']['id'] == 'MyJobId'
        assert 'attributes' in response_data['data']
        assert 'relationships' in response_data['data']
        assert 'links' in response_data['data']
        
        # Verify correct endpoint was called
        call_args = mock_jobs_api._session.get.call_args
        assert f'jobs/{job_id}' in call_args[0][0]
        print("\n✓ Mock: Job retrieved successfully with 200 status code")
    
    def test_get_job_unauthorized_401(self, mock_jobs_api):
        """Test unauthorized access with 401 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 401 status code
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
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_get_job_bad_request_400(self, mock_jobs_api):
        """Test bad request with 400 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 400 status code
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
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute with invalid parameters
        job_id = "InvalidJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '400'
        assert response_data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in response_data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code")
    
    def test_get_job_not_found_404(self, mock_jobs_api):
        """Test job not found with 404 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Job 'NonExistentJob' not found"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "NonExistentJob"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '404'
        assert response_data['errors'][0]['title'] == 'Not Found'
        print("\n✓ Mock: Not found returns 404 status code")
    
    def test_get_job_with_default_fields(self, mock_jobs_api):
        """Test that default fields are applied automatically (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "MyJobId"
            }
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute without explicit fields parameter
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_jobs_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify default fields are applied
        assert 'fields[collections]' in params
        assert params['fields[collections]'] == '@all'
        assert 'fields[jobs]' in params
        assert params['fields[jobs]'] == '@all'
        print("\n✓ Mock: Default fields applied automatically")
    
    def test_get_job_with_custom_fields(self, mock_jobs_api):
        """Test with custom fields parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "MyJobId"
            }
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute with custom fields
        job_id = "MyJobId"
        custom_fields = {
            'jobs': 'jobId,name,state',
            'documents': 'title'
        }
        response = mock_jobs_api.get_job(job_id=job_id, fields=custom_fields)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_jobs_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom fields override defaults
        assert 'fields[jobs]' in params
        assert params['fields[jobs]'] == 'jobId,name,state'
        assert 'fields[documents]' in params
        assert params['fields[documents]'] == 'title'
        
        # Verify other defaults still apply
        assert 'fields[collections]' in params
        assert params['fields[collections]'] == '@all'
        print("\n✓ Mock: Custom fields override defaults correctly")
    
    def test_get_job_with_include(self, mock_jobs_api):
        """Test with include parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "MyJobId"
            },
            "included": [
                {
                    "type": "documents",
                    "id": "MyProjectId/MySpaceId/MyDocumentId"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute with include parameter
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id, include="documents,project")
        
        # Assert
        assert response.status_code == 200
        call_args = mock_jobs_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify include parameter is passed
        assert 'include' in params
        assert params['include'] == 'documents,project'
        
        # Verify included section in response
        response_data = response.json()
        assert 'included' in response_data
        print("\n✓ Mock: Include parameter handled correctly")
    
    def test_get_job_with_fields_and_include(self, mock_jobs_api):
        """Test with both fields and include parameters (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "MyJobId"
            },
            "included": []
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute with both fields and include
        job_id = "MyJobId"
        custom_fields = {'jobs': 'jobId,name'}
        response = mock_jobs_api.get_job(
            job_id=job_id,
            fields=custom_fields,
            include="documents"
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_jobs_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify both parameters are passed
        assert 'fields[jobs]' in params
        assert params['fields[jobs]'] == 'jobId,name'
        assert 'include' in params
        assert params['include'] == 'documents'
        print("\n✓ Mock: Both fields and include parameters work together")
    
    def test_get_job_endpoint_format(self, mock_jobs_api):
        """Test that the correct endpoint format is used (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"type": "jobs", "id": "MyJobId"}
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "test-job-123"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_jobs_api._session.get.call_args
        endpoint = call_args[0][0]
        
        # Verify endpoint matches expected format from CURL
        assert f'jobs/{job_id}' in endpoint
        assert endpoint.endswith(f'jobs/{job_id}')
        print("\n✓ Mock: Correct endpoint format used")
    
    def test_get_job_different_job_ids(self, mock_jobs_api):
        """Test with different job ID formats (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"type": "jobs", "id": "test"}
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Test various job ID formats
        job_ids = [
            "simple-job",
            "job_with_underscores",
            "JOB-123-ABC",
            "export-job-2024",
            "import_job_001"
        ]
        
        for job_id in job_ids:
            response = mock_jobs_api.get_job(job_id=job_id)
            
            # Assert
            assert response.status_code == 200
            call_args = mock_jobs_api._session.get.call_args
            endpoint = call_args[0][0]
            assert f'jobs/{job_id}' in endpoint
        
        print("\n✓ Mock: Different job ID formats handled correctly")
    
    def test_get_job_response_structure(self, mock_jobs_api):
        """Test that response has correct structure (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "MyJobId",
                "revision": "1234",
                "attributes": {
                    "jobId": "example",
                    "name": "example",
                    "state": "example",
                    "status": {
                        "type": "OK",
                        "message": "message"
                    }
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "MyProjectId"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/jobs/MyJobId"
                }
            }
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert response structure
        assert response.status_code == 200
        response_data = response.json()
        
        # Check structure
        assert 'data' in response_data
        assert 'type' in response_data['data']
        assert 'id' in response_data['data']
        assert 'attributes' in response_data['data']
        assert 'relationships' in response_data['data']
        assert 'links' in response_data['data']
        
        # Check attributes structure
        assert 'jobId' in response_data['data']['attributes']
        assert 'name' in response_data['data']['attributes']
        assert 'state' in response_data['data']['attributes']
        assert 'status' in response_data['data']['attributes']
        
        print("\n✓ Mock: Response structure is correct")
    
    def test_get_job_with_relationships(self, mock_jobs_api):
        """Test that relationships are properly included (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "MyJobId",
                "relationships": {
                    "document": {
                        "data": {
                            "type": "documents",
                            "id": "MyProjectId/MySpaceId/MyDocumentId"
                        }
                    },
                    "documents": {
                        "data": [
                            {
                                "type": "documents",
                                "id": "MyProjectId/MySpaceId/MyDocumentId"
                            }
                        ]
                    },
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "MyProjectId"
                        }
                    }
                }
            }
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        relationships = response_data['data']['relationships']
        
        # Verify relationships structure
        assert 'document' in relationships
        assert 'documents' in relationships
        assert 'project' in relationships
        
        # Verify relationship data
        assert relationships['document']['data']['type'] == 'documents'
        assert relationships['project']['data']['type'] == 'projects'
        print("\n✓ Mock: Relationships properly included in response")
    
    def test_get_job_with_links(self, mock_jobs_api):
        """Test that links are properly included (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "MyJobId",
                "links": {
                    "self": "server-host-name/application-path/jobs/MyJobId",
                    "log": "server-host-name/application-path/polarion/job-report?jobId=MyJobId",
                    "downloads": [
                        "https://testdrive.polarion.com/polarion/download/filename1",
                        "https://testdrive.polarion.com/polarion/download/filename2"
                    ]
                }
            },
            "links": {
                "self": "server-host-name/application-path/jobs/MyJobId"
            }
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        
        # Verify links in data
        assert 'links' in response_data['data']
        assert 'self' in response_data['data']['links']
        assert 'log' in response_data['data']['links']
        assert 'downloads' in response_data['data']['links']
        
        # Verify top-level links
        assert 'links' in response_data
        assert 'self' in response_data['links']
        print("\n✓ Mock: Links properly included in response")
    
    def test_get_job_with_job_status(self, mock_jobs_api):
        """Test that job status is properly returned (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "jobs",
                "id": "MyJobId",
                "attributes": {
                    "jobId": "export-job-123",
                    "name": "Export Job",
                    "state": "COMPLETED",
                    "status": {
                        "type": "OK",
                        "message": "Job completed successfully"
                    }
                }
            }
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        attributes = response_data['data']['attributes']
        
        # Verify status structure
        assert 'status' in attributes
        assert 'type' in attributes['status']
        assert 'message' in attributes['status']
        assert attributes['status']['type'] == 'OK'
        assert attributes['state'] == 'COMPLETED'
        print("\n✓ Mock: Job status properly returned")
    
    def test_get_job_forbidden_403(self, mock_jobs_api):
        """Test forbidden access with 403 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "User does not have permission to access this job"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "RestrictedJob"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 403
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '403'
        assert response_data['errors'][0]['title'] == 'Forbidden'
        print("\n✓ Mock: Forbidden access returns 403 status code")
    
    def test_get_job_server_error_500(self, mock_jobs_api):
        """Test server error with 500 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "500",
                    "title": "Internal Server Error",
                    "detail": "An error occurred while retrieving the job"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 500
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '500'
        assert response_data['errors'][0]['title'] == 'Internal Server Error'
        print("\n✓ Mock: Server error returns 500 status code")
    
    def test_get_job_service_unavailable_503(self, mock_jobs_api):
        """Test service unavailable with 503 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "503",
                    "title": "Service Unavailable",
                    "detail": "Service temporarily unavailable"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 503
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '503'
        assert response_data['errors'][0]['title'] == 'Service Unavailable'
        print("\n✓ Mock: Service unavailable returns 503 status code")
    
    def test_get_job_not_acceptable_406(self, mock_jobs_api):
        """Test not acceptable with 406 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 406
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "406",
                    "title": "Not Acceptable",
                    "detail": "The requested content type is not acceptable"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 406
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '406'
        assert response_data['errors'][0]['title'] == 'Not Acceptable'
        print("\n✓ Mock: Not acceptable returns 406 status code")
    
    def test_get_job_without_optional_parameters(self, mock_jobs_api):
        """Test with only required parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"type": "jobs", "id": "MyJobId"}
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute with only job_id
        job_id = "MyJobId"
        response = mock_jobs_api.get_job(job_id=job_id)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_jobs_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify default fields are applied but include is not
        assert 'fields[jobs]' in params
        assert 'include' not in params or params.get('include') is None
        print("\n✓ Mock: Works correctly with only required parameter")
