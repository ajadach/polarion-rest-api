"""
Tests for TestRecords.delete_test_record method.

This module contains comprehensive unit tests for the delete_test_record method,
covering success scenarios and all error responses defined in the OpenAPI spec.
"""
import pytest
from unittest.mock import Mock


class TestDeleteTestRecord:
    """Test class for delete_test_record method"""

    # ========================================================================
    # Success Tests
    # ========================================================================

    def test_delete_test_record_success(self, mock_test_records_api):
        """Test successful test record deletion (204 No Content)"""
        # Arrange
        project_id = "test_project"
        test_run_id = "TEST-RUN-123"
        test_case_project_id = "test_case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 204
        mock_test_records_api._session.delete.assert_called_once_with(
            "https://test.polarion.com/polarion/rest/v1/projects/test_project/testruns/TEST-RUN-123/testrecords/test_case_project/TC-001/1",
            json=None
        )

    def test_delete_test_record_with_special_characters(self, mock_test_records_api):
        """Test test record deletion with special characters in IDs"""
        # Arrange
        project_id = "test-project_v2"
        test_run_id = "RUN-2024-01"
        test_case_project_id = "case_project_123"
        test_case_id = "TC-SPECIAL-001"
        iteration = "2"
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 204
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/test-project_v2/testruns/RUN-2024-01/testrecords/case_project_123/TC-SPECIAL-001/2"
        mock_test_records_api._session.delete.assert_called_once_with(expected_url, json=None)

    def test_delete_test_record_with_high_iteration(self, mock_test_records_api):
        """Test test record deletion with high iteration number"""
        # Arrange
        project_id = "proj1"
        test_run_id = "run1"
        test_case_project_id = "caseproj1"
        test_case_id = "TC1"
        iteration = "999"
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 204
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/proj1/testruns/run1/testrecords/caseproj1/TC1/999"
        mock_test_records_api._session.delete.assert_called_once_with(expected_url, json=None)

    # ========================================================================
    # Error Response Tests
    # ========================================================================

    def test_delete_test_record_400_bad_request(self, mock_test_records_api):
        """Test test record deletion with 400 Bad Request error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "TEST-RUN-123"
        test_case_project_id = "test_case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Invalid test record identifier"
                }
            ]
        }
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 400
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "400"

    def test_delete_test_record_401_unauthorized(self, mock_test_records_api):
        """Test test record deletion with 401 Unauthorized error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "TEST-RUN-123"
        test_case_project_id = "test_case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "Authentication credentials are missing or invalid"
                }
            ]
        }
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 401
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "401"

    def test_delete_test_record_403_forbidden(self, mock_test_records_api):
        """Test test record deletion with 403 Forbidden error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "TEST-RUN-123"
        test_case_project_id = "test_case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You do not have permission to delete this test record"
                }
            ]
        }
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 403
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "403"

    def test_delete_test_record_404_not_found(self, mock_test_records_api):
        """Test test record deletion with 404 Not Found error"""
        # Arrange
        project_id = "nonexistent_project"
        test_run_id = "NONEXISTENT-RUN"
        test_case_project_id = "nonexistent_case_project"
        test_case_id = "TC-999"
        iteration = "1"
        
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
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "404"
        assert "not found" in error_data["errors"][0]["detail"].lower()

    def test_delete_test_record_409_conflict(self, mock_test_records_api):
        """Test test record deletion with 409 Conflict error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "TEST-RUN-123"
        test_case_project_id = "test_case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "409",
                    "title": "Conflict",
                    "detail": "Test record cannot be deleted due to a conflict"
                }
            ]
        }
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 409
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "409"

    def test_delete_test_record_500_internal_server_error(self, mock_test_records_api):
        """Test test record deletion with 500 Internal Server Error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "TEST-RUN-123"
        test_case_project_id = "test_case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
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
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 500
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "500"

    def test_delete_test_record_503_service_unavailable(self, mock_test_records_api):
        """Test test record deletion with 503 Service Unavailable error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "TEST-RUN-123"
        test_case_project_id = "test_case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
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
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 503
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "503"

    # ========================================================================
    # URL Construction Tests
    # ========================================================================

    def test_delete_test_record_url_construction(self, mock_test_records_api):
        """Test that URL is correctly constructed with all parameters"""
        # Arrange
        project_id = "my_project"
        test_run_id = "RUN-2024-Q1"
        test_case_project_id = "case_project_main"
        test_case_id = "TC-SMOKE-001"
        iteration = "5"
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/my_project/testruns/RUN-2024-Q1/testrecords/case_project_main/TC-SMOKE-001/5"
        mock_test_records_api._session.delete.assert_called_once_with(expected_url, json=None)

    def test_delete_test_record_url_with_numeric_ids(self, mock_test_records_api):
        """Test URL construction with numeric string identifiers"""
        # Arrange
        project_id = "123"
        test_run_id = "456"
        test_case_project_id = "789"
        test_case_id = "101112"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/123/testruns/456/testrecords/789/101112/1"
        mock_test_records_api._session.delete.assert_called_once_with(expected_url, json=None)

    # ========================================================================
    # Edge Case Tests
    # ========================================================================

    def test_delete_test_record_with_iteration_zero(self, mock_test_records_api):
        """Test deletion with iteration number zero"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-001"
        test_case_project_id = "case_proj"
        test_case_id = "TC-001"
        iteration = "0"
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 204
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/test_project/testruns/RUN-001/testrecords/case_proj/TC-001/0"
        mock_test_records_api._session.delete.assert_called_once_with(expected_url, json=None)

    def test_delete_test_record_empty_response_body(self, mock_test_records_api):
        """Test successful deletion with empty response body"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_response.content = b""
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 204
        assert response.text == ""
        assert response.content == b""

    def test_delete_test_record_with_long_ids(self, mock_test_records_api):
        """Test deletion with very long identifier strings"""
        # Arrange
        project_id = "test_project_with_very_long_name_for_testing_purposes"
        test_run_id = "RUN-2024-REGRESSION-FULL-SUITE-ITERATION-01"
        test_case_project_id = "test_case_project_name_very_long"
        test_case_id = "TC-DETAILED-SCENARIO-001-WITH-LONG-DESCRIPTION"
        iteration = "42"
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 204
        call_args = mock_test_records_api._session.delete.call_args[0][0]
        assert project_id in call_args
        assert test_run_id in call_args
        assert test_case_project_id in call_args
        assert test_case_id in call_args
        assert iteration in call_args

    # ========================================================================
    # Multiple Error Scenarios Tests
    # ========================================================================

    def test_delete_test_record_multiple_errors_in_response(self, mock_test_records_api):
        """Test handling of multiple errors in response"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Invalid project identifier"
                },
                {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Invalid test run identifier"
                }
            ]
        }
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 400
        error_data = response.json()
        assert "errors" in error_data
        assert len(error_data["errors"]) == 2

    def test_delete_test_record_response_object_type(self, mock_test_records_api):
        """Test that the method returns a Response object"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_test_records_api._session.delete.return_value = mock_response

        # Act
        response = mock_test_records_api.delete_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response is not None
        assert hasattr(response, 'status_code')
        assert response.status_code == 204
