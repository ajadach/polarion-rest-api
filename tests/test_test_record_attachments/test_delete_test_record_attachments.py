"""
Tests for TestRecordAttachments.delete_test_record_attachments method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestDeleteTestRecordAttachments:
    """Test suite for delete_test_record_attachments method"""
    
    def test_delete_test_record_attachments_success(self, mock_test_record_attachments_api):
        """Test successful deletion of multiple test record attachments"""
        # Mock response for successful deletion
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Prepare the body data based on example
        body_data = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "MyProjectId/MyTestRunId/MyProjectId/MyTestcaseId/0/MyAttachmentId"
                }
            ]
        }
        
        # Call the method
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="MyProjectId",
            test_run_id="MyTestRunId",
            test_case_project_id="MyProjectId",
            test_case_id="MyTestcaseId",
            iteration="0",
            test_record_attachments_data=body_data
        )
        
        # Verify the response
        assert response.status_code == 204
        
        # Verify the correct endpoint was called
        mock_test_record_attachments_api._session.delete.assert_called_once()
        call_args = mock_test_record_attachments_api._session.delete.call_args
        assert "projects/MyProjectId/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0/attachments" in call_args[0][0]
    
    def test_delete_test_record_attachments_multiple_ids(self, mock_test_record_attachments_api):
        """Test deletion of multiple attachments in one request"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Prepare body with multiple attachment IDs
        body_data = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "Proj1/Run1/Proj1/TC1/1/Att1"
                },
                {
                    "type": "testrecord_attachments",
                    "id": "Proj1/Run1/Proj1/TC1/1/Att2"
                },
                {
                    "type": "testrecord_attachments",
                    "id": "Proj1/Run1/Proj1/TC1/1/Att3"
                }
            ]
        }
        
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="Proj1",
            test_run_id="Run1",
            test_case_project_id="Proj1",
            test_case_id="TC1",
            iteration="1",
            test_record_attachments_data=body_data
        )
        
        assert response.status_code == 204
        
        # Verify body was sent
        call_args = mock_test_record_attachments_api._session.delete.call_args
        assert call_args[1]["json"] == body_data
    
    def test_delete_test_record_attachments_url_construction(self, mock_test_record_attachments_api):
        """Test that URL is correctly constructed with all path parameters"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        body_data = {"data": [{"type": "testrecord_attachments", "id": "P1/R1/P1/TC1/1/A1"}]}
        
        # Test with different parameter combinations
        test_cases = [
            ("Proj1", "Run1", "TPrj1", "TC1", "1"),
            ("MyProject", "TestRun-123", "TestProj", "TestCase-456", "5"),
            ("project_a", "run_b", "proj_c", "case_d", "10"),
        ]
        
        for proj, run, tc_proj, tc, iter in test_cases:
            mock_test_record_attachments_api._session.delete.reset_mock()
            
            response = mock_test_record_attachments_api.delete_test_record_attachments(
                project_id=proj,
                test_run_id=run,
                test_case_project_id=tc_proj,
                test_case_id=tc,
                iteration=iter,
                test_record_attachments_data=body_data
            )
            
            # Verify correct URL construction
            call_args = mock_test_record_attachments_api._session.delete.call_args
            expected_path = f"projects/{proj}/testruns/{run}/testrecords/{tc_proj}/{tc}/{iter}/attachments"
            assert expected_path in call_args[0][0]
    
    def test_delete_test_record_attachments_unauthorized_401(self, mock_test_record_attachments_api):
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
        
        body_data = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "MyProjectId/MyTestRunId/MyProjectId/MyTestcaseId/0/MyAttachmentId"
                }
            ]
        }
        
        # Call the method
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="1",
            test_record_attachments_data=body_data
        )
        
        # Verify the error response
        assert response.status_code == 401
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "401"
        assert errors[0]["title"] == "Unauthorized"
        assert errors[0]["detail"] == "No access token"
    
    def test_delete_test_record_attachments_bad_request_400(self, mock_test_record_attachments_api):
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
        
        # Invalid body data
        body_data = {
            "data": "invalid_format"
        }
        
        # Call the method
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="1",
            test_record_attachments_data=body_data
        )
        
        # Verify the error response
        assert response.status_code == 400
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "400"
        assert errors[0]["title"] == "Bad Request"
        assert "source" in errors[0]
    
    def test_delete_test_record_attachments_empty_array(self, mock_test_record_attachments_api):
        """Test deletion with empty data array"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Empty data array
        body_data = {
            "data": []
        }
        
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="MyProject",
            test_run_id="TR001",
            test_case_project_id="TestProject",
            test_case_id="TC001",
            iteration="1",
            test_record_attachments_data=body_data
        )
        
        assert response.status_code == 204
    
    def test_delete_test_record_attachments_different_iterations(self, mock_test_record_attachments_api):
        """Test deletion with different iteration numbers"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        body_data = {
            "data": [{"type": "testrecord_attachments", "id": "P1/R1/P1/TC1/5/A1"}]
        }
        
        # Test with various iteration numbers
        iterations = ["1", "5", "10", "100"]
        
        for iteration in iterations:
            mock_test_record_attachments_api._session.delete.reset_mock()
            
            response = mock_test_record_attachments_api.delete_test_record_attachments(
                project_id="MyProject",
                test_run_id="TR001",
                test_case_project_id="TestProject",
                test_case_id="TC001",
                iteration=iteration,
                test_record_attachments_data=body_data
            )
            
            assert response.status_code == 204
            call_args = mock_test_record_attachments_api._session.delete.call_args
            assert f"/{iteration}/attachments" in call_args[0][0]
    
    def test_delete_test_record_attachments_body_structure(self, mock_test_record_attachments_api):
        """Test that body structure follows JSON:API format"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Body following JSON:API format
        body_data = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "Project1/TestRun1/Project1/TestCase1/1/Attachment1"
                },
                {
                    "type": "testrecord_attachments",
                    "id": "Project1/TestRun1/Project1/TestCase1/1/Attachment2"
                }
            ]
        }
        
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="Project1",
            test_run_id="TestRun1",
            test_case_project_id="Project1",
            test_case_id="TestCase1",
            iteration="1",
            test_record_attachments_data=body_data
        )
        
        assert response.status_code == 204
        
        # Verify JSON body was sent
        call_args = mock_test_record_attachments_api._session.delete.call_args
        assert "json" in call_args[1]
        assert call_args[1]["json"]["data"][0]["type"] == "testrecord_attachments"
    
    def test_delete_test_record_attachments_not_found_404(self, mock_test_record_attachments_api):
        """Test delete when attachments don't exist (404)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "One or more test record attachments not found"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        body_data = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "P1/R1/P1/TC1/1/NonExistent"
                }
            ]
        }
        
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="P1",
            test_run_id="R1",
            test_case_project_id="P1",
            test_case_id="TC1",
            iteration="1",
            test_record_attachments_data=body_data
        )
        
        assert response.status_code == 404
        errors = response.json()["errors"]
        assert errors[0]["status"] == "404"
    
    def test_delete_test_record_attachments_forbidden_403(self, mock_test_record_attachments_api):
        """Test delete when user doesn't have permission (403)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You do not have permission to delete these attachments"
                }
            ]
        }
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        body_data = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "RestrictedProj/Run1/RestrictedProj/TC1/1/Att1"
                }
            ]
        }
        
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="RestrictedProj",
            test_run_id="Run1",
            test_case_project_id="RestrictedProj",
            test_case_id="TC1",
            iteration="1",
            test_record_attachments_data=body_data
        )
        
        assert response.status_code == 403
        errors = response.json()["errors"]
        assert errors[0]["status"] == "403"
        assert errors[0]["title"] == "Forbidden"
    
    def test_delete_test_record_attachments_special_characters(self, mock_test_record_attachments_api):
        """Test deletion with IDs containing special characters"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        body_data = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "My-Project_v2/Test-Run_123/TC-Project/Test-Case-456/3/Attachment-789_v1"
                }
            ]
        }
        
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="My-Project_v2",
            test_run_id="Test-Run_123",
            test_case_project_id="TC-Project",
            test_case_id="Test-Case-456",
            iteration="3",
            test_record_attachments_data=body_data
        )
        
        assert response.status_code == 204
        call_args = mock_test_record_attachments_api._session.delete.call_args
        assert "My-Project_v2" in call_args[0][0]
        assert "Test-Run_123" in call_args[0][0]
    
    def test_delete_test_record_attachments_same_project_ids(self, mock_test_record_attachments_api):
        """Test deletion when test case project matches main project"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        body_data = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "SharedProject/TR001/SharedProject/TC001/1/ATT001"
                }
            ]
        }
        
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="SharedProject",
            test_run_id="TR001",
            test_case_project_id="SharedProject",
            test_case_id="TC001",
            iteration="1",
            test_record_attachments_data=body_data
        )
        
        assert response.status_code == 204
        call_args = mock_test_record_attachments_api._session.delete.call_args
        # SharedProject should appear twice in URL
        assert call_args[0][0].count("SharedProject") >= 2
    
    def test_delete_test_record_attachments_server_error_500(self, mock_test_record_attachments_api):
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
        
        body_data = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": "P1/R1/P1/TC1/1/A1"
                }
            ]
        }
        
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="P1",
            test_run_id="R1",
            test_case_project_id="P1",
            test_case_id="TC1",
            iteration="1",
            test_record_attachments_data=body_data
        )
        
        assert response.status_code == 500
        errors = response.json()["errors"]
        assert errors[0]["status"] == "500"
    
    def test_delete_test_record_attachments_large_batch(self, mock_test_record_attachments_api):
        """Test deletion of a large batch of attachments"""
        mock_response = Mock()
        mock_response.status_code = 204
        
        mock_test_record_attachments_api._session.delete.return_value = mock_response
        
        # Create body with many attachments
        body_data = {
            "data": [
                {
                    "type": "testrecord_attachments",
                    "id": f"P1/R1/P1/TC1/1/Att{i}"
                }
                for i in range(50)
            ]
        }
        
        response = mock_test_record_attachments_api.delete_test_record_attachments(
            project_id="P1",
            test_run_id="R1",
            test_case_project_id="P1",
            test_case_id="TC1",
            iteration="1",
            test_record_attachments_data=body_data
        )
        
        assert response.status_code == 204
        call_args = mock_test_record_attachments_api._session.delete.call_args
        assert len(call_args[1]["json"]["data"]) == 50
