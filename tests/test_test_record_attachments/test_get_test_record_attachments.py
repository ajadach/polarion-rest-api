"""
Tests for TestRecordAttachments.get_test_record_attachments method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetTestRecordAttachments:
    """Test suite for get_test_record_attachments method"""
    
    def test_get_test_record_attachments_success_200(self, mock_test_record_attachments_api):
        """Test successful retrieval of test record attachments list with 200 status code"""
        # Mock response based on example for 200 status code
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 1
            },
            "data": [
                {
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
                }
            ],
            "included": [
                {}
            ],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments?page%5Bsize%5D=10&page%5Bnumber%5D=5",
                "first": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments?page%5Bsize%5D=10&page%5Bnumber%5D=1",
                "prev": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments?page%5Bsize%5D=10&page%5Bnumber%5D=4",
                "next": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments?page%5Bsize%5D=10&page%5Bnumber%5D=6",
                "last": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments?page%5Bsize%5D=10&page%5Bnumber%5D=9"
            }
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProjectId",
            test_run_id="MyTestRunId",
            test_case_project_id="MyProjectId",
            test_case_id="MyTestcaseId",
            iteration="0"
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["totalCount"] == 1
        assert len(data["data"]) == 1
        assert data["data"][0]["type"] == "testrecord_attachments"
        assert data["data"][0]["id"] == "MyProjectId/MyTestRunId/MyProjectId/MyTestcaseId/0/MyAttachmentId"
        
        # Verify pagination links
        assert "self" in data["links"]
        assert "first" in data["links"]
        assert "prev" in data["links"]
        assert "next" in data["links"]
        assert "last" in data["links"]
        
        # Verify the correct endpoint was called
        mock_test_record_attachments_api._session.get.assert_called_once()
        call_args = mock_test_record_attachments_api._session.get.call_args
        assert "projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments" in call_args[0][0]
    
    def test_get_test_record_attachments_url_construction(self, mock_test_record_attachments_api):
        """Test that URL is correctly constructed with all path parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [], "meta": {"totalCount": 0}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Test with different parameter combinations
        test_cases = [
            ("Proj1", "Run1", "TPrj1", "TC1", "1"),
            ("MyProject", "TestRun-123", "TestProj", "TestCase-456", "5"),
            ("project_a", "run_b", "proj_c", "case_d", "10"),
        ]
        
        for proj, run, tc_proj, tc, iter_num in test_cases:
            mock_test_record_attachments_api._session.get.reset_mock()
            
            response = mock_test_record_attachments_api.get_test_record_attachments(
                project_id=proj,
                test_run_id=run,
                test_case_project_id=tc_proj,
                test_case_id=tc,
                iteration=iter_num
            )
            
            # Verify correct URL construction
            call_args = mock_test_record_attachments_api._session.get.call_args
            expected_path = f"projects/{proj}/testruns/{run}/testrecords/{tc_proj}/{tc}/{iter_num}/attachments"
            assert expected_path in call_args[0][0]
    
    def test_get_test_record_attachments_with_pagination(self, mock_test_record_attachments_api):
        """Test that pagination parameters are correctly applied"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [], "meta": {"totalCount": 0}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call with pagination parameters
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            page_size=123,
            page_number=456
        )
        
        # Verify pagination parameters are in params
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        assert params.get('page[size]') == 123
        assert params.get('page[number]') == 456
    
    def test_get_test_record_attachments_with_default_fields(self, mock_test_record_attachments_api):
        """Test that default fields are applied correctly"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [], "meta": {"totalCount": 0}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call without custom fields - should use defaults
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0"
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
    
    def test_get_test_record_attachments_with_custom_fields(self, mock_test_record_attachments_api):
        """Test that custom fields override defaults correctly"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [], "meta": {"totalCount": 0}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call with custom fields
        custom_fields = {
            'testrecord_attachments': 'id,fileName,title',
            'users': 'id,name'
        }
        
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            fields=custom_fields
        )
        
        # Verify custom fields override defaults
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        
        # Custom fields should override
        assert params.get('fields[testrecord_attachments]') == 'id,fileName,title'
        assert params.get('fields[users]') == 'id,name'
        
        # Other fields should still be @all
        assert params.get('fields[collections]') == '@all'
        assert params.get('fields[documents]') == '@all'
    
    def test_get_test_record_attachments_with_include_parameter(self, mock_test_record_attachments_api):
        """Test that include parameter is correctly added to request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [], "meta": {"totalCount": 0}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call with include parameter
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            include="author,project"
        )
        
        # Verify include is in params
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        assert params.get('include') == 'author,project'
    
    def test_get_test_record_attachments_with_revision_parameter(self, mock_test_record_attachments_api):
        """Test that revision parameter is correctly added to request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [], "meta": {"totalCount": 0}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call with revision parameter
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            revision="1234"
        )
        
        # Verify revision is in params
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        assert params.get('revision') == '1234'
    
    def test_get_test_record_attachments_with_all_optional_parameters(self, mock_test_record_attachments_api):
        """Test with all optional parameters provided"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [], "meta": {"totalCount": 0}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        custom_fields = {
            'testrecord_attachments': 'id,fileName',
            'users': 'id,name,email'
        }
        
        # Call with all parameters
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            page_size=50,
            page_number=2,
            fields=custom_fields,
            include="author,project",
            revision="5678"
        )
        
        # Verify all parameters are in the call
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        
        assert params.get('page[size]') == 50
        assert params.get('page[number]') == 2
        assert params.get('fields[testrecord_attachments]') == 'id,fileName'
        assert params.get('fields[users]') == 'id,name,email'
        assert params.get('include') == 'author,project'
        assert params.get('revision') == '5678'
    
    def test_get_test_record_attachments_bad_request_400(self, mock_test_record_attachments_api):
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
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0"
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
    
    def test_get_test_record_attachments_unauthorized_401(self, mock_test_record_attachments_api):
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
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0"
        )
        
        # Verify the error response
        assert response.status_code == 401
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "401"
        assert errors[0]["title"] == "Unauthorized"
        assert errors[0]["detail"] == "No access token"
    
    def test_get_test_record_attachments_not_found_404(self, mock_test_record_attachments_api):
        """Test get with 404 Not Found response"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Test record not found"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="NonExistent",
            test_run_id="TR999",
            test_case_project_id="TestProject",
            test_case_id="TC999",
            iteration="0"
        )
        
        # Verify the error response
        assert response.status_code == 404
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "404"
        assert errors[0]["title"] == "Not Found"
    
    def test_get_test_record_attachments_empty_list(self, mock_test_record_attachments_api):
        """Test retrieval when no attachments exist"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 0
            },
            "data": [],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments"
            }
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["totalCount"] == 0
        assert len(data["data"]) == 0
    
    def test_get_test_record_attachments_multiple_items(self, mock_test_record_attachments_api):
        """Test retrieval of multiple attachments"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 3
            },
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "Proj/Run/Proj/TC/0/Att1",
                    "attributes": {"fileName": "file1.pdf", "title": "Attachment 1"}
                },
                {
                    "type": "testrecord_attachments",
                    "id": "Proj/Run/Proj/TC/0/Att2",
                    "attributes": {"fileName": "file2.png", "title": "Attachment 2"}
                },
                {
                    "type": "testrecord_attachments",
                    "id": "Proj/Run/Proj/TC/0/Att3",
                    "attributes": {"fileName": "file3.zip", "title": "Attachment 3"}
                }
            ],
            "links": {"self": "..."}
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="Proj",
            test_run_id="Run",
            test_case_project_id="Proj",
            test_case_id="TC",
            iteration="0"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["totalCount"] == 3
        assert len(data["data"]) == 3
        assert data["data"][0]["attributes"]["fileName"] == "file1.pdf"
        assert data["data"][1]["attributes"]["fileName"] == "file2.png"
        assert data["data"][2]["attributes"]["fileName"] == "file3.zip"
    
    def test_get_test_record_attachments_pagination_different_sizes(self, mock_test_record_attachments_api):
        """Test pagination with different page sizes"""
        page_sizes = [10, 25, 50, 100]
        
        for page_size in page_sizes:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": [], "meta": {"totalCount": 0}}
            
            mock_test_record_attachments_api._session.get.return_value = mock_response
            mock_test_record_attachments_api._session.get.reset_mock()
            
            response = mock_test_record_attachments_api.get_test_record_attachments(
                project_id="MyProject",
                test_run_id="TR001",
                test_case_project_id="TestProject",
                test_case_id="TC001",
                iteration="0",
                page_size=page_size,
                page_number=1
            )
            
            # Verify page size parameter
            call_args = mock_test_record_attachments_api._session.get.call_args
            params = call_args[1].get('params', {})
            assert params.get('page[size]') == page_size
    
    def test_get_test_record_attachments_without_optional_params(self, mock_test_record_attachments_api):
        """Test that optional parameters can be omitted"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [], "meta": {"totalCount": 0}}
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call without optional parameters
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0"
            # No page_size, page_number, fields, include, or revision
        )
        
        # Verify the call was made
        assert response.status_code == 200
        mock_test_record_attachments_api._session.get.assert_called_once()
        
        # Verify params contain default fields but not pagination/include/revision
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params', {})
        
        # Should have default fields
        assert 'fields[collections]' in params
        # Should not have pagination, include or revision
        assert 'page[size]' not in params
        assert 'page[number]' not in params
        assert 'include' not in params
        assert 'revision' not in params
    
    def test_get_test_record_attachments_forbidden_403(self, mock_test_record_attachments_api):
        """Test get with 403 Forbidden response"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "Access denied to test record attachments"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="RestrictedProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0"
        )
        
        assert response.status_code == 403
        errors = response.json()["errors"]
        assert errors[0]["status"] == "403"
        assert errors[0]["title"] == "Forbidden"
    
    def test_get_test_record_attachments_server_error_500(self, mock_test_record_attachments_api):
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
        
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0"
        )
        
        assert response.status_code == 500
        errors = response.json()["errors"]
        assert errors[0]["status"] == "500"
        assert errors[0]["title"] == "Internal Server Error"
    
    def test_get_test_record_attachments_response_structure(self, mock_test_record_attachments_api):
        """Test that the response structure matches expected format"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 2
            },
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "Proj/Run/Proj/TC/0/Att1",
                    "revision": "100",
                    "attributes": {
                        "fileName": "test1.pdf",
                        "id": "Att1",
                        "length": 1024,
                        "title": "Test File 1",
                        "updated": "2025-01-15T10:00:00Z"
                    },
                    "relationships": {
                        "author": {
                            "data": {"type": "users", "id": "user1"}
                        },
                        "project": {
                            "data": {"type": "projects", "id": "Proj"}
                        }
                    },
                    "links": {
                        "self": "https://test.polarion.com/.../Att1",
                        "content": "https://test.polarion.com/.../Att1/content"
                    }
                },
                {
                    "type": "testrecord_attachments",
                    "id": "Proj/Run/Proj/TC/0/Att2",
                    "revision": "101",
                    "attributes": {
                        "fileName": "test2.png",
                        "id": "Att2",
                        "length": 2048,
                        "title": "Test File 2",
                        "updated": "2025-01-15T11:00:00Z"
                    },
                    "relationships": {
                        "author": {
                            "data": {"type": "users", "id": "user2"}
                        },
                        "project": {
                            "data": {"type": "projects", "id": "Proj"}
                        }
                    },
                    "links": {
                        "self": "https://test.polarion.com/.../Att2",
                        "content": "https://test.polarion.com/.../Att2/content"
                    }
                }
            ],
            "links": {
                "self": "https://test.polarion.com/.../attachments",
                "first": "https://test.polarion.com/.../attachments?page[number]=1",
                "last": "https://test.polarion.com/.../attachments?page[number]=3"
            }
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        response = mock_test_record_attachments_api.get_test_record_attachments(
            project_id="Proj",
            test_run_id="Run",
            test_case_project_id="Proj",
            test_case_id="TC",
            iteration="0"
        )
        
        # Verify response structure
        assert response.status_code == 200
        data = response.json()
        
        # Check top-level structure
        assert "meta" in data
        assert "data" in data
        assert "links" in data
        
        # Check meta
        assert data["meta"]["totalCount"] == 2
        
        # Check data items
        for item in data["data"]:
            assert item["type"] == "testrecord_attachments"
            assert "id" in item
            assert "revision" in item
            assert "attributes" in item
            assert "relationships" in item
            assert "links" in item
            
            # Check attributes
            assert "fileName" in item["attributes"]
            assert "id" in item["attributes"]
            assert "length" in item["attributes"]
            assert "title" in item["attributes"]
            assert "updated" in item["attributes"]
            
            # Check relationships
            assert "author" in item["relationships"]
            assert "project" in item["relationships"]
            
            # Check links
            assert "self" in item["links"]
            assert "content" in item["links"]
        
        # Check pagination links
        assert "self" in data["links"]
        assert "first" in data["links"]
        assert "last" in data["links"]
