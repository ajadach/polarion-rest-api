"""
Tests for TestRecordAttachments.get_test_record_attachment method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetTestRecordAttachment:
    """Test suite for get_test_record_attachment method"""
    
    def test_get_test_record_attachment_success_200(self, mock_test_record_attachments_api):
        """Test successful retrieval of a test record attachment with 200 status code"""
        # Mock response based on example for 200 status code
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testrecord_attachments",
                "id": "MyProjectId/MyTestRunId/MyProjectId/MyTestcaseId/0/MyAttachmentId",
                "revision": "1234",
                "attributes": {
                    "fileName": "File Name",
                    "id": "MyAttachmentId",
                    "length": 0,
                    "title": "Title",
                    "updated": "1970-01-01T00:00:00Z"
                },
                "relationships": {
                    "author": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId",
                            "revision": "1234"
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
                    "self": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments/MyAttachmentId",
                    "content": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments/MyAttachmentId/content"
                }
            },
            "included": [
                {}
            ],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments/MyAttachmentId"
            }
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="MyProjectId",
            test_run_id="MyTestRunId",
            test_case_project_id="MyProjectId",
            test_case_id="MyTestcaseId",
            iteration="0",
            attachment_id="MyAttachmentId"
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["type"] == "testrecord_attachments"
        assert data["data"]["id"] == "MyProjectId/MyTestRunId/MyProjectId/MyTestcaseId/0/MyAttachmentId"
        assert data["data"]["revision"] == "1234"
        assert data["data"]["attributes"]["fileName"] == "File Name"
        assert data["data"]["attributes"]["id"] == "MyAttachmentId"
        assert data["data"]["attributes"]["title"] == "Title"
        
        # Verify relationships
        assert data["data"]["relationships"]["author"]["data"]["type"] == "users"
        assert data["data"]["relationships"]["author"]["data"]["id"] == "MyUserId"
        assert data["data"]["relationships"]["project"]["data"]["type"] == "projects"
        assert data["data"]["relationships"]["project"]["data"]["id"] == "MyProjectId"
        
        # Verify links
        assert "self" in data["data"]["links"]
        assert "content" in data["data"]["links"]
        
        # Verify the correct endpoint was called
        mock_test_record_attachments_api._session.get.assert_called_once()
        call_args = mock_test_record_attachments_api._session.get.call_args
        assert "projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments/MyAttachmentId" in call_args[0][0]
    
    def test_get_test_record_attachment_url_construction(self, mock_test_record_attachments_api):
        """Test that URL is correctly constructed with all path parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Test with different parameter combinations
        test_cases = [
            ("Proj1", "Run1", "TPrj1", "TC1", "1", "Att1"),
            ("MyProject", "TestRun-123", "TestProj", "TestCase-456", "5", "Attachment-789"),
            ("project_a", "run_b", "proj_c", "case_d", "10", "att_e"),
        ]
        
        for proj, run, tc_proj, tc, iter_num, att in test_cases:
            mock_test_record_attachments_api._session.get.reset_mock()
            
            response = mock_test_record_attachments_api.get_test_record_attachment(
                project_id=proj,
                test_run_id=run,
                test_case_project_id=tc_proj,
                test_case_id=tc,
                iteration=iter_num,
                attachment_id=att
            )
            
            # Verify correct URL construction
            call_args = mock_test_record_attachments_api._session.get.call_args
            expected_path = f"projects/{proj}/testruns/{run}/testrecords/{tc_proj}/{tc}/{iter_num}/attachments/{att}"
            assert expected_path in call_args[0][0]
    
    def test_get_test_record_attachment_with_default_fields(self, mock_test_record_attachments_api):
        """Test that default fields are applied correctly"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call without custom fields - should use defaults
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001"
        )
        
        # Verify default fields are included in params
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        
        # Verify some key default fields
        assert params.get('fields[collections]') == '@all'
        assert params.get('fields[categories]') == '@all'
        assert params.get('fields[documents]') == '@all'
        assert params.get('fields[testrecord_attachments]') == '@all'
        assert params.get('fields[workitems]') == '@all'
        assert params.get('fields[users]') == '@all'
    
    def test_get_test_record_attachment_with_custom_fields(self, mock_test_record_attachments_api):
        """Test that custom fields override defaults correctly"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call with custom fields
        custom_fields = {
            'workitems': 'id,title',
            'users': 'id,name'
        }
        
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            fields=custom_fields
        )
        
        # Verify custom fields override defaults
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        
        # Custom fields should override
        assert params.get('fields[workitems]') == 'id,title'
        assert params.get('fields[users]') == 'id,name'
        
        # Other fields should still be @all
        assert params.get('fields[collections]') == '@all'
        assert params.get('fields[documents]') == '@all'
    
    def test_get_test_record_attachment_with_include_parameter(self, mock_test_record_attachments_api):
        """Test that include parameter is correctly added to request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call with include parameter
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            include="author,project"
        )
        
        # Verify include is in params
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        assert params.get('include') == 'author,project'
    
    def test_get_test_record_attachment_with_revision_parameter(self, mock_test_record_attachments_api):
        """Test that revision parameter is correctly added to request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call with revision parameter
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            revision="1234"
        )
        
        # Verify revision is in params
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        assert params.get('revision') == '1234'
    
    def test_get_test_record_attachment_with_all_optional_parameters(self, mock_test_record_attachments_api):
        """Test with all optional parameters provided"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        custom_fields = {
            'workitems': 'id,title',
            'users': 'id,name,email'
        }
        
        # Call with all parameters
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            fields=custom_fields,
            include="author,project",
            revision="5678"
        )
        
        # Verify all parameters are in the call
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        
        assert params.get('fields[workitems]') == 'id,title'
        assert params.get('fields[users]') == 'id,name,email'
        assert params.get('include') == 'author,project'
        assert params.get('revision') == '5678'
    
    def test_get_test_record_attachment_bad_request_400(self, mock_test_record_attachments_api):
        """Test get with 400 Bad Request response"""
        # Mock 400 response based on example
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
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001"
        )
        
        # Verify the error response
        assert response.status_code == 400
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "400"
        assert errors[0]["title"] == "Bad Request"
        assert "Unexpected token" in errors[0]["detail"]
        assert errors[0]["source"]["pointer"] == "$.data"
        assert errors[0]["source"]["parameter"] == "revision"
    
    def test_get_test_record_attachment_unauthorized_401(self, mock_test_record_attachments_api):
        """Test get with 401 Unauthorized response"""
        # Mock 401 response based on example
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
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001"
        )
        
        # Verify the error response
        assert response.status_code == 401
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "401"
        assert errors[0]["title"] == "Unauthorized"
        assert errors[0]["detail"] == "No access token"
    
    def test_get_test_record_attachment_not_found_404(self, mock_test_record_attachments_api):
        """Test get with 404 Not Found response"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Test record attachment not found"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="NonExistent",
            test_run_id="TR999",
            test_case_project_id="TestProject",
            test_case_id="TC999",
            iteration="0",
            attachment_id="ATT999"
        )
        
        # Verify the error response
        assert response.status_code == 404
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "404"
        assert errors[0]["title"] == "Not Found"
    
    def test_get_test_record_attachment_forbidden_403(self, mock_test_record_attachments_api):
        """Test get with 403 Forbidden response"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "Access denied to the test record attachment"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="RestrictedProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001"
        )
        
        # Verify the error response
        assert response.status_code == 403
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "403"
        assert errors[0]["title"] == "Forbidden"
    
    def test_get_test_record_attachment_server_error_500(self, mock_test_record_attachments_api):
        """Test get with 500 Internal Server Error response"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "500",
                    "title": "Internal Server Error",
                    "detail": "An unexpected error occurred"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001"
        )
        
        # Verify the error response
        assert response.status_code == 500
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "500"
        assert errors[0]["title"] == "Internal Server Error"
    
    def test_get_test_record_attachment_without_optional_params(self, mock_test_record_attachments_api):
        """Test that optional parameters can be omitted"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call without optional parameters
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001"
            # No fields, include, or revision parameters
        )
        
        # Verify the call was made
        assert response.status_code == 200
        mock_test_record_attachments_api._session.get.assert_called_once()
        
        # Verify params contain default fields but not include/revision
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        
        # Should have default fields
        assert 'fields[collections]' in params
        # Should not have include or revision
        assert 'include' not in params
        assert 'revision' not in params
    
    def test_get_test_record_attachment_response_structure(self, mock_test_record_attachments_api):
        """Test that the response structure matches expected format"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testrecord_attachments",
                "id": "MyProjectId/MyTestRunId/MyProjectId/MyTestcaseId/0/MyAttachmentId",
                "revision": "1234",
                "attributes": {
                    "fileName": "test_file.pdf",
                    "id": "MyAttachmentId",
                    "length": 12345,
                    "title": "Test Attachment",
                    "updated": "2025-01-15T10:30:00Z"
                },
                "relationships": {
                    "author": {
                        "data": {
                            "type": "users",
                            "id": "testuser",
                            "revision": "5678"
                        }
                    },
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "MyProjectId",
                            "revision": "9012"
                        }
                    }
                },
                "links": {
                    "self": "https://test.polarion.com/polarion/rest/v1/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments/MyAttachmentId",
                    "content": "https://test.polarion.com/polarion/rest/v1/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments/MyAttachmentId/content"
                }
            },
            "links": {
                "self": "https://test.polarion.com/polarion/rest/v1/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments/MyAttachmentId"
            }
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="MyProjectId",
            test_run_id="MyTestRunId",
            test_case_project_id="MyProjectId",
            test_case_id="MyTestcaseId",
            iteration="0",
            attachment_id="MyAttachmentId"
        )
        
        # Verify response structure
        assert response.status_code == 200
        data = response.json()
        
        # Check top-level structure
        assert "data" in data
        assert "links" in data
        
        # Check data structure
        assert data["data"]["type"] == "testrecord_attachments"
        assert "id" in data["data"]
        assert "revision" in data["data"]
        assert "attributes" in data["data"]
        assert "relationships" in data["data"]
        assert "links" in data["data"]
        
        # Check attributes
        assert "fileName" in data["data"]["attributes"]
        assert "id" in data["data"]["attributes"]
        assert "length" in data["data"]["attributes"]
        assert "title" in data["data"]["attributes"]
        assert "updated" in data["data"]["attributes"]
        
        # Check relationships
        assert "author" in data["data"]["relationships"]
        assert "project" in data["data"]["relationships"]
        
        # Check links
        assert "self" in data["data"]["links"]
        assert "content" in data["data"]["links"]
    
    def test_get_test_record_attachment_with_special_characters(self, mock_test_record_attachments_api):
        """Test handling of special characters in parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call with special characters
        response = mock_test_record_attachments_api.get_test_record_attachment(
            project_id="My-Project_123",
            test_run_id="TR-001_Test",
            test_case_project_id="Test_Project-ABC",
            test_case_id="TC_001-XYZ",
            iteration="0",
            attachment_id="ATT-001_File"
        )
        
        # Verify the call was made successfully
        assert response.status_code == 200
        mock_test_record_attachments_api._session.get.assert_called_once()
        
        # Verify URL contains special characters
        call_args = mock_test_record_attachments_api._session.get.call_args
        url = call_args[0][0]
        assert "My-Project_123" in url
        assert "TR-001_Test" in url
        assert "Test_Project-ABC" in url
        assert "TC_001-XYZ" in url
        assert "ATT-001_File" in url
    
    def test_get_test_record_attachment_iteration_as_string(self, mock_test_record_attachments_api):
        """Test that iteration parameter works correctly as a string"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Test with different iteration values
        iterations = ["0", "1", "5", "10", "100"]
        
        for iteration in iterations:
            mock_test_record_attachments_api._session.get.reset_mock()
            
            response = mock_test_record_attachments_api.get_test_record_attachment(
                project_id="MyProject",
                test_run_id="TR001",
                test_case_project_id="TestProject",
                test_case_id="TC001",
                iteration=iteration,
                attachment_id="ATT001"
            )
            
            # Verify iteration is in URL
            call_args = mock_test_record_attachments_api._session.get.call_args
            url = call_args[0][0]
            assert f"/{iteration}/attachments/" in url
