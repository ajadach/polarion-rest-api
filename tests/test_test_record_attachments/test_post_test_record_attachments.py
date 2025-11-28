"""
Tests for TestRecordAttachments.post_test_record_attachments method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
import json
from unittest.mock import Mock


class TestPostTestRecordAttachments:
    """Test suite for post_test_record_attachments method"""
    
    def test_post_test_record_attachments_success_201(self, mock_test_record_attachments_api):
        """Test successful creation of test record attachments with 201 Created"""
        # Mock response based on example for 201 status code
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "MyProjectId/MyTestRunId/MyProjectId/MyTestcaseId/0/MyAttachmentId",
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments/MyAttachmentId",
                        "content": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments/MyAttachmentId/content"
                    }
                }
            ]
        }
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        # Prepare test data
        metadata = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "lid": "att1",
                    "attributes": {
                        "fileName": "test.pdf",
                        "title": "Test Attachment"
                    }
                }
            ]
        }
        
        mock_file = Mock()
        
        # Call the method
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="MyProjectId",
            test_run_id="MyTestRunId",
            test_case_project_id="MyProjectId",
            test_case_id="MyTestcaseId",
            iteration="0",
            files={'file': mock_file},
            data={'resource': json.dumps(metadata)}
        )
        
        # Verify the response
        assert response.status_code == 201
        data = response.json()
        assert len(data["data"]) == 1
        assert data["data"][0]["type"] == "testrecord_attachments"
        assert data["data"][0]["id"] == "MyProjectId/MyTestRunId/MyProjectId/MyTestcaseId/0/MyAttachmentId"
        assert "self" in data["data"][0]["links"]
        assert "content" in data["data"][0]["links"]
        
        # Verify the correct endpoint was called with POST
        mock_test_record_attachments_api._session.post.assert_called_once()
        call_args = mock_test_record_attachments_api._session.post.call_args
        assert "projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments" in call_args[0][0]
    
    def test_post_test_record_attachments_multiple_files(self, mock_test_record_attachments_api):
        """Test creating multiple attachments at once"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "Proj/Run/Proj/TC/0/Att1",
                    "links": {"self": "...", "content": "..."}
                },
                {
                    "type": "testrecord_attachments",
                    "id": "Proj/Run/Proj/TC/0/Att2",
                    "links": {"self": "...", "content": "..."}
                }
            ]
        }
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        metadata = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "lid": "att1",
                    "attributes": {"fileName": "file1.pdf", "title": "File 1"}
                },
                {
                    "type": "testrecord_attachments",
                    "lid": "att2",
                    "attributes": {"fileName": "file2.png", "title": "File 2"}
                }
            ]
        }
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="Proj",
            test_run_id="Run",
            test_case_project_id="Proj",
            test_case_id="TC",
            iteration="0",
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert len(data["data"]) == 2
    
    def test_post_test_record_attachments_url_construction(self, mock_test_record_attachments_api):
        """Test that URL is correctly constructed with all path parameters"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        # Test with different parameter combinations
        test_cases = [
            ("Proj1", "Run1", "TPrj1", "TC1", "1"),
            ("MyProject", "TestRun-123", "TestProj", "TestCase-456", "5"),
            ("project_a", "run_b", "proj_c", "case_d", "10"),
        ]
        
        for proj, run, tc_proj, tc, iter_num in test_cases:
            mock_test_record_attachments_api._session.post.reset_mock()
            
            response = mock_test_record_attachments_api.post_test_record_attachments(
                project_id=proj,
                test_run_id=run,
                test_case_project_id=tc_proj,
                test_case_id=tc,
                iteration=iter_num,
                data={'resource': '{"data":[]}'}
            )
            
            # Verify correct URL construction
            call_args = mock_test_record_attachments_api._session.post.call_args
            expected_path = f"projects/{proj}/testruns/{run}/testrecords/{tc_proj}/{tc}/{iter_num}/attachments"
            assert expected_path in call_args[0][0]
    
    def test_post_test_record_attachments_with_lid(self, mock_test_record_attachments_api):
        """Test creating attachments with local ID (lid) for identification"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": [{"type": "testrecord_attachments", "id": "..."}]}
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        metadata = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "lid": "unique-lid-123",
                    "attributes": {
                        "fileName": "document.pdf",
                        "title": "Important Document"
                    }
                }
            ]
        }
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 201
    
    def test_post_test_record_attachments_bad_request_400(self, mock_test_record_attachments_api):
        """Test post with 400 Bad Request response"""
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
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        # Call with invalid data
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            data={'resource': 'invalid json'}
        )
        
        # Verify the error response
        assert response.status_code == 400
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "400"
        assert errors[0]["title"] == "Bad Request"
        assert "Unexpected token" in errors[0]["detail"]
    
    def test_post_test_record_attachments_unauthorized_401(self, mock_test_record_attachments_api):
        """Test post with 401 Unauthorized response"""
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
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            data={'resource': '{"data":[]}'}
        )
        
        # Verify the error response
        assert response.status_code == 401
        errors = response.json()["errors"]
        assert errors[0]["status"] == "401"
        assert errors[0]["title"] == "Unauthorized"
        assert errors[0]["detail"] == "No access token"
    
    def test_post_test_record_attachments_forbidden_403(self, mock_test_record_attachments_api):
        """Test post with 403 Forbidden response"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "No permission to create attachments"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="RestrictedProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            data={'resource': '{"data":[]}'}
        )
        
        assert response.status_code == 403
        errors = response.json()["errors"]
        assert errors[0]["status"] == "403"
        assert errors[0]["title"] == "Forbidden"
    
    def test_post_test_record_attachments_not_found_404(self, mock_test_record_attachments_api):
        """Test post with 404 Not Found response (test record doesn't exist)"""
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
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="MyProject",
            test_run_id="NONEXISTENT",
            test_case_project_id="TestProject",
            test_case_id="TC999",
            iteration="0",
            data={'resource': '{"data":[]}'}
        )
        
        assert response.status_code == 404
        errors = response.json()["errors"]
        assert errors[0]["status"] == "404"
        assert errors[0]["title"] == "Not Found"
    
    def test_post_test_record_attachments_server_error_500(self, mock_test_record_attachments_api):
        """Test post with 500 Internal Server Error response"""
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
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            data={'resource': '{"data":[]}'}
        )
        
        assert response.status_code == 500
        errors = response.json()["errors"]
        assert errors[0]["status"] == "500"
        assert errors[0]["title"] == "Internal Server Error"
    
    def test_post_test_record_attachments_with_files_and_metadata(self, mock_test_record_attachments_api):
        """Test creating attachments with both files and metadata"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": [{"type": "testrecord_attachments", "id": "..."}]}
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        metadata = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "attributes": {
                        "fileName": "report.pdf",
                        "title": "Test Report"
                    }
                }
            ]
        }
        
        mock_file = Mock()
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            files={'file': mock_file},
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 201
        
        # Verify files and data were passed
        call_args = mock_test_record_attachments_api._session.post.call_args
        assert 'files' in call_args[1]
        assert 'data' in call_args[1]
    
    def test_post_test_record_attachments_multipart_content_type(self, mock_test_record_attachments_api):
        """Test that multipart/form-data is used for file upload"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        mock_file = Mock()
        metadata = {"data": [{"type": "testrecord_attachments", "attributes": {"title": "Test"}}]}
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            files={'file': mock_file},
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 201
        
        # Verify files parameter was passed (multipart/form-data)
        call_args = mock_test_record_attachments_api._session.post.call_args
        assert 'files' in call_args[1]
        assert call_args[1]['files'] is not None
    
    def test_post_test_record_attachments_with_special_characters(self, mock_test_record_attachments_api):
        """Test creating attachments with special characters in parameters"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="My-Project_123",
            test_run_id="TR-001.v2",
            test_case_project_id="Test_Proj",
            test_case_id="TC-001",
            iteration="0",
            data={'resource': '{"data":[]}'}
        )
        
        assert response.status_code == 201
        
        # Verify URL contains special characters
        call_args = mock_test_record_attachments_api._session.post.call_args
        url = call_args[0][0]
        assert "My-Project_123" in url
        assert "TR-001.v2" in url
        assert "Test_Proj" in url
        assert "TC-001" in url
    
    def test_post_test_record_attachments_different_iterations(self, mock_test_record_attachments_api):
        """Test creating attachments in different test iterations"""
        iterations = ["0", "1", "5", "10"]
        
        for iteration in iterations:
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {"data": []}
            
            mock_test_record_attachments_api._session.post.return_value = mock_response
            mock_test_record_attachments_api._session.post.reset_mock()
            
            response = mock_test_record_attachments_api.post_test_record_attachments(
                project_id="MyProject",
                test_run_id="TR001",
                test_case_project_id="TestProject",
                test_case_id="TC001",
                iteration=iteration,
                data={'resource': '{"data":[]}'}
            )
            
            assert response.status_code == 201
            
            # Verify iteration in URL
            call_args = mock_test_record_attachments_api._session.post.call_args
            url = call_args[0][0]
            assert f"/{iteration}/attachments" in url
    
    def test_post_test_record_attachments_without_optional_params(self, mock_test_record_attachments_api):
        """Test that files and data parameters are optional"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        # Call without files and data
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0"
        )
        
        assert response.status_code == 201
        mock_test_record_attachments_api._session.post.assert_called_once()
    
    def test_post_test_record_attachments_response_structure(self, mock_test_record_attachments_api):
        """Test that the response structure matches expected format"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "Proj/Run/Proj/TC/0/Att1",
                    "links": {
                        "self": "https://test.polarion.com/.../Att1",
                        "content": "https://test.polarion.com/.../Att1/content"
                    }
                },
                {
                    "type": "testrecord_attachments",
                    "id": "Proj/Run/Proj/TC/0/Att2",
                    "links": {
                        "self": "https://test.polarion.com/.../Att2",
                        "content": "https://test.polarion.com/.../Att2/content"
                    }
                }
            ]
        }
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="Proj",
            test_run_id="Run",
            test_case_project_id="Proj",
            test_case_id="TC",
            iteration="0",
            data={'resource': '{"data":[]}'}
        )
        
        # Verify response structure
        assert response.status_code == 201
        data = response.json()
        
        # Check data array
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 2
        
        # Check each attachment in response
        for attachment in data["data"]:
            assert attachment["type"] == "testrecord_attachments"
            assert "id" in attachment
            assert "links" in attachment
            assert "self" in attachment["links"]
            assert "content" in attachment["links"]
    
    def test_post_test_record_attachments_empty_data_array(self, mock_test_record_attachments_api):
        """Test creating attachments with empty data array"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        metadata = {"data": []}
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert len(data["data"]) == 0
    
    def test_post_test_record_attachments_complex_metadata(self, mock_test_record_attachments_api):
        """Test creating attachments with complex metadata structure"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": [{"type": "testrecord_attachments", "id": "..."}]}
        
        mock_test_record_attachments_api._session.post.return_value = mock_response
        
        complex_metadata = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "lid": "att-001",
                    "attributes": {
                        "fileName": "complex-file-name-@#$.pdf",
                        "title": "Complex Title with Special Chars: @#$%^&*()"
                    }
                },
                {
                    "type": "testrecord_attachments",
                    "lid": "att-002",
                    "attributes": {
                        "fileName": "another_file.zip",
                        "title": "Another Attachment"
                    }
                }
            ]
        }
        
        response = mock_test_record_attachments_api.post_test_record_attachments(
            project_id="Proj",
            test_run_id="Run",
            test_case_project_id="Proj",
            test_case_id="TC",
            iteration="0",
            data={'resource': json.dumps(complex_metadata)}
        )
        
        assert response.status_code == 201
        
        # Verify data was passed
        call_args = mock_test_record_attachments_api._session.post.call_args
        assert 'data' in call_args[1]
