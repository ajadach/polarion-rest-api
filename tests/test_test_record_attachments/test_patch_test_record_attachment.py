"""
Tests for TestRecordAttachments.patch_test_record_attachment method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
import json
from unittest.mock import Mock


class TestPatchTestRecordAttachment:
    """Test suite for patch_test_record_attachment method"""
    
    def test_patch_test_record_attachment_success_204(self, mock_test_record_attachments_api):
        """Test successful update of test record attachment with 204 No Content"""
        # Mock response for successful update
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        # Prepare metadata
        metadata = {
            "data": {
                "type": "testrecord_attachments",
                "id": "MyProjectId/MyTestRunId/MyProjectId/MyTestcaseId/0/MyAttachmentId",
                "attributes": {
                    "title": "Updated Title"
                }
            }
        }
        
        # Call the method with metadata
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="MyProjectId",
            test_run_id="MyTestRunId",
            test_case_project_id="MyProjectId",
            test_case_id="MyTestcaseId",
            iteration="0",
            attachment_id="MyAttachmentId",
            data={'resource': json.dumps(metadata)}
        )
        
        # Verify the response
        assert response.status_code == 204
        
        # Verify the correct endpoint was called
        mock_test_record_attachments_api._session.patch.assert_called_once()
        call_args = mock_test_record_attachments_api._session.patch.call_args
        assert "projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments/MyAttachmentId" in call_args[0][0]
    
    def test_patch_test_record_attachment_with_file_only(self, mock_test_record_attachments_api):
        """Test updating attachment with file upload only"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        # Mock file object
        mock_file = Mock()
        mock_file.read.return_value = b"PDF content"
        
        # Call with file only
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            files={'file': mock_file}
        )
        
        assert response.status_code == 204
        
        # Verify files parameter was passed
        call_args = mock_test_record_attachments_api._session.patch.call_args
        assert call_args[1]['files'] is not None
    
    def test_patch_test_record_attachment_with_metadata_only(self, mock_test_record_attachments_api):
        """Test updating attachment metadata without file upload"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        # Update only metadata (title)
        metadata = {
            "data": {
                "type": "testrecord_attachments",
                "id": "MyProject/TR001/TestProject/TC001/0/ATT001",
                "attributes": {
                    "title": "New Title"
                }
            }
        }
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 204
        
        # Verify data parameter was passed
        call_args = mock_test_record_attachments_api._session.patch.call_args
        assert call_args[1]['data'] is not None
        assert 'resource' in call_args[1]['data']
    
    def test_patch_test_record_attachment_with_file_and_metadata(self, mock_test_record_attachments_api):
        """Test updating both file and metadata"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        # Mock file
        mock_file = Mock()
        mock_file.read.return_value = b"Updated file content"
        
        # Metadata
        metadata = {
            "data": {
                "type": "testrecord_attachments",
                "id": "Proj/Run/Proj/TC/0/Att",
                "attributes": {
                    "title": "Updated Document"
                }
            }
        }
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="Proj",
            test_run_id="Run",
            test_case_project_id="Proj",
            test_case_id="TC",
            iteration="0",
            attachment_id="Att",
            files={'file': mock_file},
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 204
        
        # Verify both files and data were passed
        call_args = mock_test_record_attachments_api._session.patch.call_args
        assert call_args[1]['files'] is not None
        assert call_args[1]['data'] is not None
    
    def test_patch_test_record_attachment_url_construction(self, mock_test_record_attachments_api):
        """Test that URL is correctly constructed with all path parameters"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        # Test with different parameter combinations
        test_cases = [
            ("Proj1", "Run1", "TPrj1", "TC1", "1", "Att1"),
            ("MyProject", "TestRun-123", "TestProj", "TestCase-456", "5", "Attachment-789"),
            ("project_a", "run_b", "proj_c", "case_d", "10", "att_e"),
        ]
        
        for proj, run, tc_proj, tc, iter_num, att in test_cases:
            mock_test_record_attachments_api._session.patch.reset_mock()
            
            metadata = {"data": {"type": "testrecord_attachments", "id": f"{proj}/{run}/{tc_proj}/{tc}/{iter_num}/{att}"}}
            
            response = mock_test_record_attachments_api.patch_test_record_attachment(
                project_id=proj,
                test_run_id=run,
                test_case_project_id=tc_proj,
                test_case_id=tc,
                iteration=iter_num,
                attachment_id=att,
                data={'resource': json.dumps(metadata)}
            )
            
            # Verify correct URL construction
            call_args = mock_test_record_attachments_api._session.patch.call_args
            expected_path = f"projects/{proj}/testruns/{run}/testrecords/{tc_proj}/{tc}/{iter_num}/attachments/{att}"
            assert expected_path in call_args[0][0]
    
    def test_patch_test_record_attachment_bad_request_400(self, mock_test_record_attachments_api):
        """Test patch with 400 Bad Request response"""
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
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        # Invalid metadata
        invalid_metadata = {"invalid": "structure"}
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            data={'resource': json.dumps(invalid_metadata)}
        )
        
        # Verify the error response
        assert response.status_code == 400
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "400"
        assert errors[0]["title"] == "Bad Request"
        assert "Unexpected token" in errors[0]["detail"]
    
    def test_patch_test_record_attachment_unauthorized_401(self, mock_test_record_attachments_api):
        """Test patch with 401 Unauthorized response"""
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
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        metadata = {"data": {"type": "testrecord_attachments"}}
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            data={'resource': json.dumps(metadata)}
        )
        
        # Verify the error response
        assert response.status_code == 401
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "401"
        assert errors[0]["title"] == "Unauthorized"
        assert errors[0]["detail"] == "No access token"
    
    def test_patch_test_record_attachment_not_found_404(self, mock_test_record_attachments_api):
        """Test patch with 404 Not Found response (attachment doesn't exist)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "The attachment was not found"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        metadata = {"data": {"type": "testrecord_attachments"}}
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="NONEXISTENT",
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 404
        errors = response.json()["errors"]
        assert errors[0]["status"] == "404"
        assert errors[0]["title"] == "Not Found"
    
    def test_patch_test_record_attachment_forbidden_403(self, mock_test_record_attachments_api):
        """Test patch with 403 Forbidden response"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "User does not have permission to update this attachment"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        metadata = {"data": {"type": "testrecord_attachments"}}
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="RestrictedProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 403
        errors = response.json()["errors"]
        assert errors[0]["status"] == "403"
        assert errors[0]["title"] == "Forbidden"
    
    def test_patch_test_record_attachment_server_error_500(self, mock_test_record_attachments_api):
        """Test patch with 500 Internal Server Error response"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "500",
                    "title": "Internal Server Error",
                    "detail": "An unexpected error occurred while updating the attachment"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        metadata = {"data": {"type": "testrecord_attachments"}}
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 500
        errors = response.json()["errors"]
        assert errors[0]["status"] == "500"
        assert errors[0]["title"] == "Internal Server Error"
    
    def test_patch_test_record_attachment_without_parameters(self, mock_test_record_attachments_api):
        """Test that method can be called without optional files and data parameters"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        # Call without files and data (both optional)
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001"
        )
        
        assert response.status_code == 204
        mock_test_record_attachments_api._session.patch.assert_called_once()
    
    def test_patch_test_record_attachment_multipart_form_data(self, mock_test_record_attachments_api):
        """Test that multipart/form-data is properly formatted"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        # Mock file
        mock_file = Mock()
        
        # Metadata as JSON string (as per CURL -F parameter)
        metadata = {
            "data": {
                "type": "testrecord_attachments",
                "id": "Proj/Run/Proj/TC/0/Att",
                "attributes": {
                    "title": "Title"
                }
            }
        }
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="Proj",
            test_run_id="Run",
            test_case_project_id="Proj",
            test_case_id="TC",
            iteration="0",
            attachment_id="Att",
            files={'file': mock_file},
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 204
        
        # Verify the call structure
        call_args = mock_test_record_attachments_api._session.patch.call_args
        assert 'files' in call_args[1]
        assert 'data' in call_args[1]
    
    def test_patch_test_record_attachment_with_different_file_types(self, mock_test_record_attachments_api):
        """Test updating attachments with different file types"""
        file_types = [
            ("document.pdf", b"PDF content"),
            ("image.png", b"PNG content"),
            ("archive.zip", b"ZIP content"),
            ("data.json", b'{"key": "value"}'),
        ]
        
        for filename, content in file_types:
            mock_response = Mock()
            mock_response.status_code = 204
            
            mock_test_record_attachments_api._session.patch.return_value = mock_response
            mock_test_record_attachments_api._session.patch.reset_mock()
            
            mock_file = Mock()
            mock_file.read.return_value = content
            mock_file.name = filename
            
            response = mock_test_record_attachments_api.patch_test_record_attachment(
                project_id="MyProject",
                test_run_id="TR001",
                test_case_project_id="TestProject",
                test_case_id="TC001",
                iteration="0",
                attachment_id="ATT001",
                files={'file': mock_file}
            )
            
            assert response.status_code == 204
    
    def test_patch_test_record_attachment_different_iterations(self, mock_test_record_attachments_api):
        """Test patching attachments for different test iterations"""
        iterations = ["0", "1", "5", "10"]
        
        for iteration in iterations:
            mock_response = Mock()
            mock_response.status_code = 204
            
            mock_test_record_attachments_api._session.patch.return_value = mock_response
            mock_test_record_attachments_api._session.patch.reset_mock()
            
            metadata = {"data": {"type": "testrecord_attachments"}}
            
            response = mock_test_record_attachments_api.patch_test_record_attachment(
                project_id="MyProject",
                test_run_id="TR001",
                test_case_project_id="TestProject",
                test_case_id="TC001",
                iteration=iteration,
                attachment_id="ATT001",
                data={'resource': json.dumps(metadata)}
            )
            
            assert response.status_code == 204
            
            # Verify correct iteration in URL
            call_args = mock_test_record_attachments_api._session.patch.call_args
            assert f"/{iteration}/attachments/" in call_args[0][0]
    
    def test_patch_test_record_attachment_complex_metadata(self, mock_test_record_attachments_api):
        """Test patching with complex metadata structure"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        # Complex metadata with multiple attributes
        metadata = {
            "data": {
                "type": "testrecord_attachments",
                "id": "MyProjectId/MyTestRunId/MyProjectId/MyTestcaseId/0/MyAttachmentId",
                "attributes": {
                    "title": "Updated Test Attachment",
                    "fileName": "updated_test.pdf"
                },
                "relationships": {
                    "author": {
                        "data": {
                            "type": "users",
                            "id": "testuser"
                        }
                    }
                }
            }
        }
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="MyProjectId",
            test_run_id="MyTestRunId",
            test_case_project_id="MyProjectId",
            test_case_id="MyTestcaseId",
            iteration="0",
            attachment_id="MyAttachmentId",
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 204
        
        # Verify metadata was passed correctly
        call_args = mock_test_record_attachments_api._session.patch.call_args
        assert 'resource' in call_args[1]['data']
        
        # Verify the JSON can be parsed back
        passed_metadata = json.loads(call_args[1]['data']['resource'])
        assert passed_metadata["data"]["attributes"]["title"] == "Updated Test Attachment"
    
    def test_patch_test_record_attachment_with_special_characters(self, mock_test_record_attachments_api):
        """Test patching with special characters in parameters"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        metadata = {"data": {"type": "testrecord_attachments"}}
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="My-Project_123",
            test_run_id="TR-001.v2",
            test_case_project_id="Test_Proj",
            test_case_id="TC-001",
            iteration="0",
            attachment_id="ATT_001-v2",
            data={'resource': json.dumps(metadata)}
        )
        
        assert response.status_code == 204
        
        # Verify URL contains special characters
        call_args = mock_test_record_attachments_api._session.patch.call_args
        url = call_args[0][0]
        assert "My-Project_123" in url
        assert "TR-001.v2" in url
        assert "Test_Proj" in url
        assert "TC-001" in url
        assert "ATT_001-v2" in url
    
    def test_patch_test_record_attachment_empty_data(self, mock_test_record_attachments_api):
        """Test patching with empty data dict"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            data={}
        )
        
        assert response.status_code == 204
    
    def test_patch_test_record_attachment_uses_patch_method(self, mock_test_record_attachments_api):
        """Verify that the method uses _patch (PATCH HTTP method)"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.patch.return_value = mock_response
        
        metadata = {"data": {"type": "testrecord_attachments"}}
        
        response = mock_test_record_attachments_api.patch_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="0",
            attachment_id="ATT001",
            data={'resource': json.dumps(metadata)}
        )
        
        # Verify _session.patch was called (not post, get, etc.)
        mock_test_record_attachments_api._session.patch.assert_called_once()
        assert response.status_code == 204
