"""
Tests for TestRecordAttachments.delete_test_record_attachment method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestDeleteTestRecordAttachment:
    """Test suite for delete_test_record_attachment method"""
    
    def test_delete_test_record_attachment_success(self, mock_test_record_attachments_api):
        """Test successful deletion of a test record attachment"""
        # Mock response for successful deletion
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="1",
            attachment_id="ATT001"
        )
        
        # Verify the response
        assert response.status_code == 204
        
        # Verify the correct endpoint was called
        mock_test_record_attachments_api._session.delete.assert_called_once()
        call_args = mock_test_record_attachments_api._session.delete.call_args
        assert "projects/MyProject/testruns/TR001/testrecords/TestProject/TC001/1/attachments/ATT001" in call_args[0][0]
    
    def test_delete_test_record_attachment_url_construction(self, mock_test_record_attachments_api):
        """Test that URL is correctly constructed with all path parameters"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Test with different parameter combinations
        test_cases = [
            ("Proj1", "Run1", "TPrj1", "TC1", "1", "Att1"),
            ("MyProject", "TestRun-123", "TestProj", "TestCase-456", "5", "Attachment-789"),
            ("project_a", "run_b", "proj_c", "case_d", "10", "att_e"),
        ]
        
        for proj, run, tc_proj, tc, iter, att in test_cases:
            mock_test_record_attachments_api._session.delete.reset_mock()
            
            response = mock_test_record_attachments_api.delete_test_record_attachment(
                project_id=proj,
                test_run_id=run,
                test_case_project_id=tc_proj,
                test_case_id=tc,
                iteration=iter,
                attachment_id=att
            )
            
            # Verify correct URL construction
            call_args = mock_test_record_attachments_api._session.delete.call_args
            expected_path = f"projects/{proj}/testruns/{run}/testrecords/{tc_proj}/{tc}/{iter}/attachments/{att}"
            assert expected_path in call_args[0][0]
    
    def test_delete_test_record_attachment_unauthorized_401(self, mock_test_record_attachments_api):
        """Test delete with 401 Unauthorized response"""
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
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="1",
            attachment_id="ATT001"
        )
        
        # Verify the error response
        assert response.status_code == 401
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "401"
        assert errors[0]["title"] == "Unauthorized"
        assert errors[0]["detail"] == "No access token"
    
    def test_delete_test_record_attachment_bad_request_400(self, mock_test_record_attachments_api):
        """Test delete with 400 Bad Request response"""
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
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="1",
            attachment_id="InvalidAtt"
        )
        
        # Verify the error response
        assert response.status_code == 400
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "400"
        assert errors[0]["title"] == "Bad Request"
        assert "source" in errors[0]
    
    def test_delete_test_record_attachment_not_found_404(self, mock_test_record_attachments_api):
        """Test delete when attachment doesn't exist (404)"""
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
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Call the method with non-existent attachment
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="1",
            attachment_id="NonExistent"
        )
        
        # Verify the error response
        assert response.status_code == 404
        errors = response.json()["errors"]
        assert errors[0]["status"] == "404"
        assert errors[0]["title"] == "Not Found"
    
    def test_delete_test_record_attachment_different_iterations(self, mock_test_record_attachments_api):
        """Test deletion with different iteration numbers"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Test with various iteration numbers
        iterations = ["1", "5", "10", "100"]
        
        for iteration in iterations:
            mock_test_record_attachments_api._session.delete.reset_mock()
            
            response = mock_test_record_attachments_api.delete_test_record_attachment(
                project_id="MyProject",
                test_run_id="TR001",
                test_case_project_id="TestProject",
                test_case_id="TC001",
                iteration=iteration,
                attachment_id="ATT001"
            )
            
            assert response.status_code == 204
            call_args = mock_test_record_attachments_api._session.delete.call_args
            assert f"/{iteration}/attachments/" in call_args[0][0]
    
    def test_delete_test_record_attachment_special_characters(self, mock_test_record_attachments_api):
        """Test deletion with IDs containing special characters"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Call with IDs containing hyphens and underscores
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id="My-Project_v2",
            test_run_id="Test-Run_123",
            test_case_project_id="TC-Project",
            test_case_id="Test-Case-456",
            iteration="3",
            attachment_id="Attachment-789_v1"
        )
        
        assert response.status_code == 204
        call_args = mock_test_record_attachments_api._session.delete.call_args
        assert "My-Project_v2" in call_args[0][0]
        assert "Test-Run_123" in call_args[0][0]
        assert "TC-Project" in call_args[0][0]
        assert "Test-Case-456" in call_args[0][0]
        assert "Attachment-789_v1" in call_args[0][0]
    
    def test_delete_test_record_attachment_forbidden_403(self, mock_test_record_attachments_api):
        """Test delete when user doesn't have permission (403)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You do not have permission to delete this attachment"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id="RestrictedProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="1",
            attachment_id="ATT001"
        )
        
        # Verify the error response
        assert response.status_code == 403
        errors = response.json()["errors"]
        assert errors[0]["status"] == "403"
        assert errors[0]["title"] == "Forbidden"
    
    def test_delete_test_record_attachment_multiple_calls(self, mock_test_record_attachments_api):
        """Test multiple delete calls in sequence"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Delete multiple attachments
        attachment_ids = ["ATT001", "ATT002", "ATT003"]
        
        for att_id in attachment_ids:
            mock_test_record_attachments_api._session.delete.reset_mock()
            
            response = mock_test_record_attachments_api.delete_test_record_attachment(
                project_id="MyProject",
                test_run_id="TR001",
                test_case_project_id="TestProject",
                test_case_id="TC001",
                iteration="1",
                attachment_id=att_id
            )
            
            assert response.status_code == 204
            mock_test_record_attachments_api._session.delete.assert_called_once()
    
    def test_delete_test_record_attachment_numeric_ids(self, mock_test_record_attachments_api):
        """Test deletion with numeric string IDs"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Call with numeric IDs
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id="12345",
            test_run_id="67890",
            test_case_project_id="11111",
            test_case_id="22222",
            iteration="5",
            attachment_id="99999"
        )
        
        assert response.status_code == 204
        call_args = mock_test_record_attachments_api._session.delete.call_args
        assert "12345/testruns/67890" in call_args[0][0]
        assert "99999" in call_args[0][0]
    
    def test_delete_test_record_attachment_no_body_sent(self, mock_test_record_attachments_api):
        """Test that DELETE request doesn't send a body"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="1",
            attachment_id="ATT001"
        )
        
        # Verify no body/json was sent
        call_args = mock_test_record_attachments_api._session.delete.call_args
        # DELETE requests typically don't have json or data parameters
        assert response.status_code == 204
    
    def test_delete_test_record_attachment_same_project_ids(self, mock_test_record_attachments_api):
        """Test deletion when test case project matches main project"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Use same project_id and test_case_project_id
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id="SharedProject",
            test_run_id="TR001",
            test_case_project_id="SharedProject",
            test_case_id="TC001",
            iteration="1",
            attachment_id="ATT001"
        )
        
        assert response.status_code == 204
        call_args = mock_test_record_attachments_api._session.delete.call_args
        # Both SharedProject instances should appear in URL
        assert call_args[0][0].count("SharedProject") >= 2
    
    def test_delete_test_record_attachment_different_projects(self, mock_test_record_attachments_api):
        """Test deletion when test case is from different project"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Test case from different project
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id="ProjectA",
            test_run_id="TR001",
            test_case_project_id="ProjectB",
            test_case_id="TC001",
            iteration="1",
            attachment_id="ATT001"
        )
        
        assert response.status_code == 204
        call_args = mock_test_record_attachments_api._session.delete.call_args
        assert "projects/ProjectA/testruns" in call_args[0][0]
        assert "testrecords/ProjectB" in call_args[0][0]
    
    def test_delete_test_record_attachment_server_error_500(self, mock_test_record_attachments_api):
        """Test delete with 500 Internal Server Error response"""
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
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Call the method
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="1",
            attachment_id="ATT001"
        )
        
        # Verify the error response
        assert response.status_code == 500
        errors = response.json()["errors"]
        assert errors[0]["status"] == "500"
        assert errors[0]["title"] == "Internal Server Error"
    
    def test_delete_test_record_attachment_long_ids(self, mock_test_record_attachments_api):
        """Test deletion with long identifier strings"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Use long IDs
        long_id = "VeryLongIdentifierString_123456789_ABCDEFGHIJKLMNOP"
        
        response = mock_test_record_attachments_api.delete_test_record_attachment(
            project_id=long_id,
            test_run_id=long_id,
            test_case_project_id=long_id,
            test_case_id=long_id,
            iteration="1",
            attachment_id=long_id
        )
        
        assert response.status_code == 204
        call_args = mock_test_record_attachments_api._session.delete.call_args
        # Long ID should appear multiple times in the URL
        assert long_id in call_args[0][0]
