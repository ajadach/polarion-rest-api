"""
Tests for TestRecords.post_test_record_test_parameters method.

This module contains comprehensive unit tests for the post_test_record_test_parameters method,
covering success scenarios and all error responses defined in the OpenAPI spec.
"""
import pytest
from unittest.mock import Mock


class TestPostTestRecordTestParameters:
    """Test class for post_test_record_test_parameters method"""

    # ========================================================================
    # Success Tests
    # ========================================================================

    def test_post_test_record_test_parameters_success(self, mock_test_records_api):
        """Test successful test parameters creation (201 Created)"""
        # Arrange
        project_id = "MyProjectId"
        test_run_id = "MyTestRunId"
        test_case_project_id = "testCaseProjectId"
        test_case_id = "testCaseId"
        iteration = "0"
        test_parameters_data = {
            "data": [
                {
                    "type": "testparameters",
                    "attributes": {
                        "name": "Example Test Parameter value",
                        "value": "Example Test Parameter value"
                    }
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testparameters",
                    "id": "MyProjectId/MyTestRunId/MyTestParameter",
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testparameters/MyTestParameter"
                    }
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 1
        assert data["data"][0]["type"] == "testparameters"
        assert data["data"][0]["id"] == "MyProjectId/MyTestRunId/MyTestParameter"
        
        mock_test_records_api._session.post.assert_called_once()
        call_args = mock_test_records_api._session.post.call_args
        assert f"{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/testparameters" in call_args[0][0]
        assert call_args[1]["json"] == test_parameters_data

    def test_post_test_record_test_parameters_single_parameter(self, mock_test_records_api):
        """Test creation with a single test parameter"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {
            "data": [
                {
                    "type": "testparameters",
                    "attributes": {
                        "name": "param1",
                        "value": "value1"
                    }
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testparameters",
                    "id": "test_project/RUN-123/param1"
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert len(data["data"]) == 1

    def test_post_test_record_test_parameters_multiple_parameters(self, mock_test_records_api):
        """Test creation with multiple test parameters"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {
            "data": [
                {
                    "type": "testparameters",
                    "attributes": {"name": "param1", "value": "value1"}
                },
                {
                    "type": "testparameters",
                    "attributes": {"name": "param2", "value": "value2"}
                },
                {
                    "type": "testparameters",
                    "attributes": {"name": "param3", "value": "value3"}
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "testparameters", "id": "test_project/RUN-123/param1"},
                {"type": "testparameters", "id": "test_project/RUN-123/param2"},
                {"type": "testparameters", "id": "test_project/RUN-123/param3"}
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert len(data["data"]) == 3

    def test_post_test_record_test_parameters_with_special_values(self, mock_test_records_api):
        """Test creation with special characters in parameter values"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {
            "data": [
                {
                    "type": "testparameters",
                    "attributes": {
                        "name": "config_param",
                        "value": "https://example.com/api?key=value&test=true"
                    }
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "testparameters", "id": "test_project/RUN-123/config_param"}
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 201
        call_args = mock_test_records_api._session.post.call_args
        assert call_args[1]["json"]["data"][0]["attributes"]["value"] == "https://example.com/api?key=value&test=true"

    def test_post_test_record_test_parameters_different_iterations(self, mock_test_records_api):
        """Test creation for different iteration numbers"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "5"
        test_parameters_data = {
            "data": [
                {
                    "type": "testparameters",
                    "attributes": {"name": "param1", "value": "value1"}
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 201
        call_args = mock_test_records_api._session.post.call_args
        assert f"/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/testparameters" in call_args[0][0]

    # ========================================================================
    # Error Response Tests
    # ========================================================================

    def test_post_test_record_test_parameters_400_bad_request(self, mock_test_records_api):
        """Test test parameters creation with 400 Bad Request error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {
            "data": [
                {
                    "type": "testparameters",
                    "attributes": {"invalid_field": "value"}
                }
            ]
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
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 400
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "400"

    def test_post_test_record_test_parameters_401_unauthorized(self, mock_test_records_api):
        """Test test parameters creation with 401 Unauthorized error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
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
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 401
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "401"
        assert error_data["errors"][0]["detail"] == "No access token"

    def test_post_test_record_test_parameters_403_forbidden(self, mock_test_records_api):
        """Test test parameters creation with 403 Forbidden error"""
        # Arrange
        project_id = "restricted_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You do not have permission to create test parameters"
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 403
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "403"

    def test_post_test_record_test_parameters_404_not_found(self, mock_test_records_api):
        """Test test parameters creation with 404 Not Found error"""
        # Arrange
        project_id = "nonexistent_project"
        test_run_id = "NONEXISTENT-RUN"
        test_case_project_id = "proj"
        test_case_id = "TC-999"
        iteration = "1"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
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
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "404"
        assert "not found" in error_data["errors"][0]["detail"].lower()

    def test_post_test_record_test_parameters_406_not_acceptable(self, mock_test_records_api):
        """Test test parameters creation with 406 Not Acceptable error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
        mock_response = Mock()
        mock_response.status_code = 406
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "406",
                    "title": "Not Acceptable",
                    "detail": "Requested format not available"
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 406
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "406"

    def test_post_test_record_test_parameters_409_conflict(self, mock_test_records_api):
        """Test test parameters creation with 409 Conflict error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "409",
                    "title": "Conflict",
                    "detail": "Test parameter already exists"
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 409
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "409"

    def test_post_test_record_test_parameters_413_payload_too_large(self, mock_test_records_api):
        """Test test parameters creation with 413 Payload Too Large error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {"data": [{"type": "testparameters"}] * 1000}  # Large payload
        
        mock_response = Mock()
        mock_response.status_code = 413
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "413",
                    "title": "Payload Too Large",
                    "detail": "Request payload is too large"
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 413
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "413"

    def test_post_test_record_test_parameters_415_unsupported_media_type(self, mock_test_records_api):
        """Test test parameters creation with 415 Unsupported Media Type error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
        mock_response = Mock()
        mock_response.status_code = 415
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "415",
                    "title": "Unsupported Media Type",
                    "detail": "Content-Type must be application/json"
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 415
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "415"

    def test_post_test_record_test_parameters_500_internal_server_error(self, mock_test_records_api):
        """Test test parameters creation with 500 Internal Server Error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
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
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 500
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "500"

    def test_post_test_record_test_parameters_503_service_unavailable(self, mock_test_records_api):
        """Test test parameters creation with 503 Service Unavailable error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
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
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 503
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "503"

    # ========================================================================
    # URL Construction Tests
    # ========================================================================

    def test_post_test_record_test_parameters_url_construction(self, mock_test_records_api):
        """Test that URL is correctly constructed with all path parameters"""
        # Arrange
        project_id = "my_project"
        test_run_id = "RUN-2024-Q1"
        test_case_project_id = "test_proj"
        test_case_id = "TC-100"
        iteration = "3"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        expected_url = f"https://test.polarion.com/polarion/rest/v1/projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/testparameters"
        mock_test_records_api._session.post.assert_called_once()
        call_args = mock_test_records_api._session.post.call_args
        assert call_args[0][0] == expected_url

    def test_post_test_record_test_parameters_json_body_passed(self, mock_test_records_api):
        """Test that JSON body is correctly passed to the request"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {
            "data": [
                {
                    "type": "testparameters",
                    "attributes": {
                        "name": "test_param",
                        "value": "test_value"
                    }
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        call_args = mock_test_records_api._session.post.call_args
        assert call_args[1]["json"] == test_parameters_data

    # ========================================================================
    # Edge Case Tests
    # ========================================================================

    def test_post_test_record_test_parameters_with_special_characters_in_ids(self, mock_test_records_api):
        """Test creation with special characters in IDs"""
        # Arrange
        project_id = "test-project_v2"
        test_run_id = "RUN-2024-01"
        test_case_project_id = "test_proj-v1"
        test_case_id = "TC-001_2"
        iteration = "0"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 201
        mock_test_records_api._session.post.assert_called_once()

    def test_post_test_record_test_parameters_response_includes_links(self, mock_test_records_api):
        """Test that response includes links to created resources"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testparameters",
                    "id": "test_project/RUN-123/param1",
                    "links": {
                        "self": "server-host-name/application-path/projects/test_project/testruns/RUN-123/testparameters/param1"
                    }
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "links" in data["data"][0]
        assert "self" in data["data"][0]["links"]

    def test_post_test_record_test_parameters_response_object_type(self, mock_test_records_api):
        """Test that the method returns a Response object"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {"data": [{"type": "testparameters"}]}
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response is not None
        assert hasattr(response, 'status_code')
        assert hasattr(response, 'json')
        assert response.status_code == 201

    def test_post_test_record_test_parameters_empty_name_value(self, mock_test_records_api):
        """Test creation with empty name and value"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "proj"
        test_case_id = "TC-001"
        iteration = "1"
        test_parameters_data = {
            "data": [
                {
                    "type": "testparameters",
                    "attributes": {
                        "name": "",
                        "value": ""
                    }
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_record_test_parameters(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_parameters_data=test_parameters_data
        )

        # Assert
        assert response.status_code == 201
        call_args = mock_test_records_api._session.post.call_args
        assert call_args[1]["json"]["data"][0]["attributes"]["name"] == ""
        assert call_args[1]["json"]["data"][0]["attributes"]["value"] == ""
