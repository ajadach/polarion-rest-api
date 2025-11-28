"""
Tests for TestRecordAttachments.get_test_record_attachment_content method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetTestRecordAttachmentContent:
    """Test suite for get_test_record_attachment_content method"""
    
    def test_get_test_record_attachment_content_success(self, mock_test_record_attachments_api):
        """Test successful retrieval of test record attachment content (binary file)"""
        # Mock response for successful binary content retrieval (200 OK)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"PDF file binary content example"
        mock_response.headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': 'attachment; filename="test.pdf"'
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.get_test_record_attachment_content(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001"
        )
        
        # Verify the response
        assert response.status_code == 200
        assert response.content == b"PDF file binary content example"
        assert response.headers['Content-Type'] == 'application/octet-stream'
        
        # Verify the correct endpoint was called
        mock_test_record_attachments_api._session.get.assert_called_once()
        call_args = mock_test_record_attachments_api._session.get.call_args
        assert "projects/MyProject/testruns/TR001/testrecords/TestProject/TC001/0/attachments/ATT001/content" in call_args[0][0]
    
    def test_get_test_record_attachment_content_with_revision(self, mock_test_record_attachments_api):
        """Test retrieval with specific revision parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"Binary content"
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method with revision
        response = mock_test_record_attachments_api.get_test_record_attachment_content(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="1",
            attachment_id="ATT001",
            revision="1234"
        )
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify revision parameter was passed
        call_args = mock_test_record_attachments_api._session.get.call_args
        assert call_args[1]['params']['revision'] == "1234"
    
    def test_get_test_record_attachment_content_without_revision(self, mock_test_record_attachments_api):
        """Test retrieval without revision parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"Binary content"
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method without revision
        response = mock_test_record_attachments_api.get_test_record_attachment_content(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001"
        )
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify params is either None or empty dict (no revision)
        call_args = mock_test_record_attachments_api._session.get.call_args
        params = call_args[1].get('params')
        if params is not None:
            assert 'revision' not in params or params == {}
    
    def test_get_test_record_attachment_content_url_construction(self, mock_test_record_attachments_api):
        """Test that URL is correctly constructed with all path parameters and /content suffix"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"Test content"
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Test with different parameter combinations
        test_cases = [
            ("Proj1", "Run1", "TPrj1", "TC1", "1", "Att1"),
            ("MyProject", "TestRun-123", "TestProj", "TestCase-456", "5", "Attachment-789"),
            ("project_a", "run_b", "proj_c", "case_d", "10", "att_e"),
        ]
        
        for proj, run, tc_proj, tc, iter, att in test_cases:
            mock_test_record_attachments_api._session.get.reset_mock()
            
            response = mock_test_record_attachments_api.get_test_record_attachment_content(
                project_id=proj,
                test_run_id=run,
                test_case_project_id=tc_proj,
                test_case_id=tc,
                iteration=iter,
                attachment_id=att
            )
            
            # Verify correct URL construction with /content suffix
            call_args = mock_test_record_attachments_api._session.get.call_args
            expected_path = f"projects/{proj}/testruns/{run}/testrecords/{tc_proj}/{tc}/{iter}/attachments/{att}/content"
            assert expected_path in call_args[0][0]
    
    def test_get_test_record_attachment_content_unauthorized_401(self, mock_test_record_attachments_api):
        """Test retrieval with 401 Unauthorized response"""
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
        response = mock_test_record_attachments_api.get_test_record_attachment_content(
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
    
    def test_get_test_record_attachment_content_bad_request_400(self, mock_test_record_attachments_api):
        """Test retrieval with 400 Bad Request response"""
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
        response = mock_test_record_attachments_api.get_test_record_attachment_content(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            revision="invalid"
        )
        
        # Verify the error response
        assert response.status_code == 400
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "400"
        assert errors[0]["title"] == "Bad Request"
        assert "source" in errors[0]
    
    def test_get_test_record_attachment_content_not_found_404(self, mock_test_record_attachments_api):
        """Test retrieval with 404 Not Found response (attachment doesn't exist)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "The requested attachment was not found"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.get_test_record_attachment_content(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="NONEXISTENT"
        )
        
        # Verify the error response
        assert response.status_code == 404
        errors = response.json()["errors"]
        assert errors[0]["status"] == "404"
        assert errors[0]["title"] == "Not Found"
    
    def test_get_test_record_attachment_content_different_file_types(self, mock_test_record_attachments_api):
        """Test retrieval of different binary file types"""
        file_types = [
            (b"PDF content", "application/pdf", "test.pdf"),
            (b"Image content", "image/png", "screenshot.png"),
            (b"ZIP content", "application/zip", "archive.zip"),
            (b"Text content", "text/plain", "document.txt"),
        ]
        
        for content, content_type, filename in file_types:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = content
            mock_response.headers = {
                'Content-Type': content_type,
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
            
            mock_test_record_attachments_api._session.get.return_value = mock_response
            
            response = mock_test_record_attachments_api.get_test_record_attachment_content(
                project_id="MyProject",
                test_run_id="TR001",
                test_case_project_id="TestProject",
                test_case_id="TC001",
                iteration="0",
                attachment_id="ATT001"
            )
            
            assert response.status_code == 200
            assert response.content == content
            assert response.headers['Content-Type'] == content_type
    
    def test_get_test_record_attachment_content_large_file(self, mock_test_record_attachments_api):
        """Test retrieval of large binary file"""
        # Simulate a large file (10MB)
        large_content = b"x" * (10 * 1024 * 1024)
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = large_content
        mock_response.headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(len(large_content))
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        response = mock_test_record_attachments_api.get_test_record_attachment_content(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="LARGE_FILE"
        )
        
        assert response.status_code == 200
        assert len(response.content) == 10 * 1024 * 1024
        assert response.headers['Content-Length'] == str(len(large_content))
    
    def test_get_test_record_attachment_content_empty_file(self, mock_test_record_attachments_api):
        """Test retrieval of empty file"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b""
        mock_response.headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Length': '0'
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        response = mock_test_record_attachments_api.get_test_record_attachment_content(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="EMPTY_FILE"
        )
        
        assert response.status_code == 200
        assert response.content == b""
        assert response.headers['Content-Length'] == '0'
    
    def test_get_test_record_attachment_content_with_special_characters_in_params(self, mock_test_record_attachments_api):
        """Test retrieval with special characters in path parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"Content"
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        # Call with special characters
        response = mock_test_record_attachments_api.get_test_record_attachment_content(
            project_id="My-Project_123",
            test_run_id="TR-001.v2",
            test_case_project_id="Test_Proj",
            test_case_id="TC-001",
            iteration="0",
            attachment_id="ATT_001-v2"
        )
        
        assert response.status_code == 200
        
        # Verify URL construction
        call_args = mock_test_record_attachments_api._session.get.call_args
        assert "My-Project_123" in call_args[0][0]
        assert "TR-001.v2" in call_args[0][0]
        assert "Test_Proj" in call_args[0][0]
        assert "TC-001" in call_args[0][0]
        assert "ATT_001-v2" in call_args[0][0]
        assert "/content" in call_args[0][0]
    
    def test_get_test_record_attachment_content_forbidden_403(self, mock_test_record_attachments_api):
        """Test retrieval with 403 Forbidden response (no permission)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "User does not have permission to access this attachment"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        response = mock_test_record_attachments_api.get_test_record_attachment_content(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001"
        )
        
        assert response.status_code == 403
        errors = response.json()["errors"]
        assert errors[0]["status"] == "403"
        assert errors[0]["title"] == "Forbidden"
    
    def test_get_test_record_attachment_content_server_error_500(self, mock_test_record_attachments_api):
        """Test retrieval with 500 Internal Server Error response"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "500",
                    "title": "Internal Server Error",
                    "detail": "An unexpected error occurred while retrieving the attachment"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.get.return_value = mock_response
        
        response = mock_test_record_attachments_api.get_test_record_attachment_content(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001"
        )
        
        assert response.status_code == 500
        errors = response.json()["errors"]
        assert errors[0]["status"] == "500"
        assert errors[0]["title"] == "Internal Server Error"
    
    def test_get_test_record_attachment_content_multiple_iterations(self, mock_test_record_attachments_api):
        """Test retrieval for different test iterations"""
        iterations = ["0", "1", "5", "10"]
        
        for iteration in iterations:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = f"Content for iteration {iteration}".encode()
            
            mock_test_record_attachments_api._session.get.return_value = mock_response
            mock_test_record_attachments_api._session.get.reset_mock()
            
            response = mock_test_record_attachments_api.get_test_record_attachment_content(
                project_id="MyProject",
                test_run_id="TR001",
                test_case_project_id="TestProject",
                test_case_id="TC001",
                iteration=iteration,
                attachment_id="ATT001"
            )
            
            assert response.status_code == 200
            
            # Verify correct iteration in URL
            call_args = mock_test_record_attachments_api._session.get.call_args
            assert f"/{iteration}/attachments/ATT001/content" in call_args[0][0]
