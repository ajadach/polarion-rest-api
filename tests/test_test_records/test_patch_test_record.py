"""
Tests for TestRecords.patch_test_record method.

This module contains comprehensive unit tests for the patch_test_record method,
covering success scenarios and all error responses defined in the OpenAPI spec.
"""
import pytest
from unittest.mock import Mock


class TestPatchTestRecord:
    """Test class for patch_test_record method"""

    # ========================================================================
    # Success Tests
    # ========================================================================

    def test_patch_test_record_success(self, mock_test_records_api):
        """Test successful test record update (204 No Content)"""
        # Arrange
        project_id = "elibrary"
        test_run_id = "MyTestRunId"
        test_case_project_id = "MyProjectId"
        test_case_id = "MyTestcaseId"
        iteration = "0"
        test_record_data = {
            "data": {
                "type": "testrecords",
                "id": "elibrary/MyTestRunId/MyProjectId/MyTestcaseId/0",
                "attributes": {
                    "comment": {
                        "type": "text/html",
                        "value": "My text value"
                    },
                    "duration": 0,
                    "executed": "1970-01-01T00:00:00Z",
                    "result": "passed",
                    "testCaseRevision": "Test Case Revision"
                },
                "relationships": {
                    "defect": {
                        "data": {
                            "type": "workitems",
                            "id": "MyProjectId/MyWorkItemId"
                        }
                    },
                    "executedBy": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId"
                        }
                    }
                }
            }
        }
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 204
        mock_test_records_api._session.patch.assert_called_once()
        call_args = mock_test_records_api._session.patch.call_args
        assert "elibrary/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0" in call_args[0][0]
        assert call_args[1]["json"] == test_record_data

    def test_patch_test_record_minimal_data(self, mock_test_records_api):
        """Test test record update with minimal data"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {
            "data": {
                "type": "testrecords",
                "id": "test_project/RUN-123/case_project/TC-001/1",
                "attributes": {
                    "result": "failed"
                }
            }
        }
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 204
        call_args = mock_test_records_api._session.patch.call_args
        assert call_args[1]["json"]["data"]["attributes"]["result"] == "failed"

    def test_patch_test_record_with_duration(self, mock_test_records_api):
        """Test test record update with duration"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {
            "data": {
                "type": "testrecords",
                "id": "test_project/RUN-123/case_project/TC-001/1",
                "attributes": {
                    "duration": 3600,
                    "result": "passed"
                }
            }
        }
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 204
        call_args = mock_test_records_api._session.patch.call_args
        assert call_args[1]["json"]["data"]["attributes"]["duration"] == 3600

    def test_patch_test_record_with_relationships(self, mock_test_records_api):
        """Test test record update with relationships"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {
            "data": {
                "type": "testrecords",
                "id": "test_project/RUN-123/case_project/TC-001/1",
                "attributes": {
                    "result": "failed"
                },
                "relationships": {
                    "defect": {
                        "data": {
                            "type": "workitems",
                            "id": "test_project/BUG-456"
                        }
                    }
                }
            }
        }
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 204
        call_args = mock_test_records_api._session.patch.call_args
        assert "defect" in call_args[1]["json"]["data"]["relationships"]

    # ========================================================================
    # Error Response Tests
    # ========================================================================

    def test_patch_test_record_400_bad_request(self, mock_test_records_api):
        """Test test record update with 400 Bad Request error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {
            "data": {
                "type": "invalid_type",
                "id": "test_project/RUN-123/case_project/TC-001/1"
            }
        }
        
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
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 400
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "400"

    def test_patch_test_record_401_unauthorized(self, mock_test_records_api):
        """Test test record update with 401 Unauthorized error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {"data": {"type": "testrecords"}}
        
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
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 401
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["detail"] == "No access token"

    def test_patch_test_record_403_forbidden(self, mock_test_records_api):
        """Test test record update with 403 Forbidden error"""
        # Arrange
        project_id = "restricted_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {"data": {"type": "testrecords"}}
        
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You do not have permission to update this test record"
                }
            ]
        }
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 403
        error_data = response.json()
        assert error_data["errors"][0]["status"] == "403"

    def test_patch_test_record_404_not_found(self, mock_test_records_api):
        """Test test record update with 404 Not Found error"""
        # Arrange
        project_id = "nonexistent_project"
        test_run_id = "NONEXISTENT-RUN"
        test_case_project_id = "nonexistent_case"
        test_case_id = "TC-999"
        iteration = "1"
        test_record_data = {"data": {"type": "testrecords"}}
        
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
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert "not found" in error_data["errors"][0]["detail"].lower()

    def test_patch_test_record_409_conflict(self, mock_test_records_api):
        """Test test record update with 409 Conflict error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {"data": {"type": "testrecords"}}
        
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "409",
                    "title": "Conflict",
                    "detail": "Test record cannot be updated due to a conflict"
                }
            ]
        }
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 409
        error_data = response.json()
        assert error_data["errors"][0]["status"] == "409"

    def test_patch_test_record_413_request_entity_too_large(self, mock_test_records_api):
        """Test test record update with 413 Request Entity Too Large error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {"data": {"type": "testrecords", "attributes": {"comment": {"value": "x" * 100000}}}}
        
        mock_response = Mock()
        mock_response.status_code = 413
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "413",
                    "title": "Request Entity Too Large",
                    "detail": "The request payload is too large"
                }
            ]
        }
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 413
        error_data = response.json()
        assert error_data["errors"][0]["status"] == "413"

    def test_patch_test_record_415_unsupported_media_type(self, mock_test_records_api):
        """Test test record update with 415 Unsupported Media Type error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {"data": {"type": "testrecords"}}
        
        mock_response = Mock()
        mock_response.status_code = 415
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "415",
                    "title": "Unsupported Media Type",
                    "detail": "The media type is not supported"
                }
            ]
        }
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 415
        error_data = response.json()
        assert error_data["errors"][0]["status"] == "415"

    def test_patch_test_record_500_internal_server_error(self, mock_test_records_api):
        """Test test record update with 500 Internal Server Error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {"data": {"type": "testrecords"}}
        
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "500",
                    "title": "Internal Server Error",
                    "detail": "An unexpected error occurred on the server"
                }
            ]
        }
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 500
        error_data = response.json()
        assert error_data["errors"][0]["status"] == "500"

    def test_patch_test_record_503_service_unavailable(self, mock_test_records_api):
        """Test test record update with 503 Service Unavailable error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {"data": {"type": "testrecords"}}
        
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "503",
                    "title": "Service Unavailable",
                    "detail": "The service is temporarily unavailable"
                }
            ]
        }
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 503
        error_data = response.json()
        assert error_data["errors"][0]["status"] == "503"

    # ========================================================================
    # URL Construction Tests
    # ========================================================================

    def test_patch_test_record_url_construction(self, mock_test_records_api):
        """Test that URL is correctly constructed with all parameters"""
        # Arrange
        project_id = "my_project"
        test_run_id = "RUN-2024-Q1"
        test_case_project_id = "case_project_main"
        test_case_id = "TC-SMOKE-001"
        iteration = "5"
        test_record_data = {"data": {"type": "testrecords"}}
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/my_project/testruns/RUN-2024-Q1/testrecords/case_project_main/TC-SMOKE-001/5"
        mock_test_records_api._session.patch.assert_called_once()
        call_args = mock_test_records_api._session.patch.call_args
        assert call_args[0][0] == expected_url

    # ========================================================================
    # Edge Case Tests
    # ========================================================================

    def test_patch_test_record_with_iteration_zero(self, mock_test_records_api):
        """Test update with iteration number zero"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-001"
        test_case_project_id = "case_proj"
        test_case_id = "TC-001"
        iteration = "0"
        test_record_data = {"data": {"type": "testrecords", "attributes": {"result": "passed"}}}
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 204

    def test_patch_test_record_with_special_characters(self, mock_test_records_api):
        """Test test record update with special characters in IDs"""
        # Arrange
        project_id = "test-project_v2"
        test_run_id = "RUN-2024-01"
        test_case_project_id = "case_project_123"
        test_case_id = "TC-SPECIAL-001"
        iteration = "2"
        test_record_data = {"data": {"type": "testrecords"}}
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 204
        mock_test_records_api._session.patch.assert_called_once()

    def test_patch_test_record_empty_response_body(self, mock_test_records_api):
        """Test successful update with empty response body"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {"data": {"type": "testrecords"}}
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_response.content = b""
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 204
        assert response.text == ""
        assert response.content == b""

    def test_patch_test_record_response_object_type(self, mock_test_records_api):
        """Test that the method returns a Response object"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {"data": {"type": "testrecords"}}
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response is not None
        assert hasattr(response, 'status_code')
        assert response.status_code == 204

    def test_patch_test_record_data_parameter_passed(self, mock_test_records_api):
        """Test that test_record_data is correctly passed to the API"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_record_data = {
            "data": {
                "type": "testrecords",
                "id": "test_project/RUN-123/case_project/TC-001/1",
                "attributes": {
                    "result": "passed",
                    "duration": 1234,
                    "executed": "2024-11-27T10:00:00Z"
                }
            }
        }
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.patch.return_value = mock_response

        # Act
        response = mock_test_records_api.patch_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_record_data=test_record_data
        )

        # Assert
        assert response.status_code == 204
        call_args = mock_test_records_api._session.patch.call_args
        assert call_args[1]["json"] == test_record_data
        assert call_args[1]["json"]["data"]["attributes"]["result"] == "passed"
        assert call_args[1]["json"]["data"]["attributes"]["duration"] == 1234
