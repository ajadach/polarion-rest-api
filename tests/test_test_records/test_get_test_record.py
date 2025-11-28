"""
Tests for TestRecords.get_test_record method.

This module contains comprehensive unit tests for the get_test_record method,
covering success scenarios and all error responses defined in the OpenAPI spec.
"""
import pytest
from unittest.mock import Mock


class TestGetTestRecord:
    """Test class for get_test_record method"""

    # ========================================================================
    # Success Tests
    # ========================================================================

    def test_get_test_record_success(self, mock_test_records_api):
        """Test successful test record retrieval (200 OK)"""
        # Arrange
        project_id = "elibrary"
        test_run_id = "MyTestRunId"
        test_case_project_id = "MyProjectId"
        test_case_id = "MyTestcaseId"
        iteration = "0"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testrecords",
                "id": "elibrary/MyTestRunId/MyProjectId/MyTestcaseId/0",
                "revision": "1234",
                "attributes": {
                    "comment": {
                        "type": "text/html",
                        "value": "My text value"
                    },
                    "duration": 0,
                    "executed": "1970-01-01T00:00:00Z",
                    "iteration": 0,
                    "result": "passed",
                    "testCaseRevision": "Test Case Revision"
                },
                "relationships": {
                    "defect": {
                        "data": {
                            "type": "workitems",
                            "id": "MyProjectId/MyWorkItemId",
                            "revision": "1234"
                        }
                    },
                    "executedBy": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId",
                            "revision": "1234"
                        }
                    },
                    "testCase": {
                        "data": {
                            "type": "workitems",
                            "id": "MyProjectId/MyWorkItemId",
                            "revision": "1234"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/projects/elibrary/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0"
                }
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["type"] == "testrecords"
        assert data["data"]["id"] == "elibrary/MyTestRunId/MyProjectId/MyTestcaseId/0"
        assert data["data"]["attributes"]["result"] == "passed"
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert "elibrary/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0" in call_args[0][0]

    def test_get_test_record_with_fields(self, mock_test_records_api):
        """Test test record retrieval with custom fields parameter"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        fields = {"testrecords": "result,duration,executed"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testrecords",
                "id": "test_project/RUN-123/case_project/TC-001/1",
                "attributes": {
                    "result": "passed",
                    "duration": 120,
                    "executed": "2024-01-15T10:30:00Z"
                }
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            fields=fields
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["attributes"]["result"] == "passed"
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["fields"] == fields

    def test_get_test_record_with_include(self, mock_test_records_api):
        """Test test record retrieval with include parameter"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        include = "defect,executedBy,testCase"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testrecords",
                "id": "test_project/RUN-123/case_project/TC-001/1"
            },
            "included": [
                {"type": "workitems", "id": "test_project/WI-001"},
                {"type": "users", "id": "user1"}
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            include=include
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "included" in data
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["include"] == include

    def test_get_test_record_with_revision(self, mock_test_records_api):
        """Test test record retrieval with revision parameter"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        revision = "5678"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testrecords",
                "id": "test_project/RUN-123/case_project/TC-001/1",
                "revision": "5678"
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            revision=revision
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["revision"] == "5678"
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["revision"] == revision

    def test_get_test_record_with_all_parameters(self, mock_test_records_api):
        """Test test record retrieval with all optional parameters"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        fields = {"testrecords": "result,duration"}
        include = "defect,executedBy"
        revision = "9999"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testrecords",
                "id": "test_project/RUN-123/case_project/TC-001/1",
                "revision": "9999"
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            fields=fields,
            include=include,
            revision=revision
        )

        # Assert
        assert response.status_code == 200
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["fields"] == fields
        assert call_args[1]["params"]["include"] == include
        assert call_args[1]["params"]["revision"] == revision

    # ========================================================================
    # Error Response Tests
    # ========================================================================

    def test_get_test_record_400_bad_request(self, mock_test_records_api):
        """Test test record retrieval with 400 Bad Request error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "invalid"
        
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
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
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

    def test_get_test_record_401_unauthorized(self, mock_test_records_api):
        """Test test record retrieval with 401 Unauthorized error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
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
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
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
        assert error_data["errors"][0]["detail"] == "No access token"

    def test_get_test_record_403_forbidden(self, mock_test_records_api):
        """Test test record retrieval with 403 Forbidden error"""
        # Arrange
        project_id = "restricted_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You do not have permission to access this test record"
                }
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
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

    def test_get_test_record_404_not_found(self, mock_test_records_api):
        """Test test record retrieval with 404 Not Found error"""
        # Arrange
        project_id = "nonexistent_project"
        test_run_id = "NONEXISTENT-RUN"
        test_case_project_id = "nonexistent_case"
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
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
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

    def test_get_test_record_406_not_acceptable(self, mock_test_records_api):
        """Test test record retrieval with 406 Not Acceptable error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 406
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "406",
                    "title": "Not Acceptable",
                    "detail": "Requested content type is not acceptable"
                }
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 406
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "406"

    def test_get_test_record_500_internal_server_error(self, mock_test_records_api):
        """Test test record retrieval with 500 Internal Server Error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
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
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
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

    def test_get_test_record_503_service_unavailable(self, mock_test_records_api):
        """Test test record retrieval with 503 Service Unavailable error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
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
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
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

    def test_get_test_record_url_construction(self, mock_test_records_api):
        """Test that URL is correctly constructed with all parameters"""
        # Arrange
        project_id = "my_project"
        test_run_id = "RUN-2024-Q1"
        test_case_project_id = "case_project_main"
        test_case_id = "TC-SMOKE-001"
        iteration = "5"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "testrecords"}}
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/my_project/testruns/RUN-2024-Q1/testrecords/case_project_main/TC-SMOKE-001/5"
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[0][0] == expected_url

    def test_get_test_record_no_optional_params(self, mock_test_records_api):
        """Test test record retrieval without optional parameters"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "testrecords"}}
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 200
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        # Should be called with None or no params
        assert call_args[1].get("params") is None

    # ========================================================================
    # Edge Case Tests
    # ========================================================================

    def test_get_test_record_with_iteration_zero(self, mock_test_records_api):
        """Test retrieval with iteration number zero"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-001"
        test_case_project_id = "case_proj"
        test_case_id = "TC-001"
        iteration = "0"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testrecords",
                "id": "test_project/RUN-001/case_proj/TC-001/0",
                "attributes": {"iteration": 0}
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["attributes"]["iteration"] == 0

    def test_get_test_record_with_special_characters(self, mock_test_records_api):
        """Test test record retrieval with special characters in IDs"""
        # Arrange
        project_id = "test-project_v2"
        test_run_id = "RUN-2024-01"
        test_case_project_id = "case_project_123"
        test_case_id = "TC-SPECIAL-001"
        iteration = "2"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testrecords",
                "id": "test-project_v2/RUN-2024-01/case_project_123/TC-SPECIAL-001/2"
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 200
        mock_test_records_api._session.get.assert_called_once()

    def test_get_test_record_response_includes_relationships(self, mock_test_records_api):
        """Test that response includes relationships data"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testrecords",
                "id": "test_project/RUN-123/case_project/TC-001/1",
                "relationships": {
                    "defect": {
                        "data": {
                            "type": "workitems",
                            "id": "test_project/WI-001"
                        }
                    },
                    "executedBy": {
                        "data": {
                            "type": "users",
                            "id": "user123"
                        }
                    }
                }
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "relationships" in data["data"]
        assert "defect" in data["data"]["relationships"]
        assert "executedBy" in data["data"]["relationships"]

    def test_get_test_record_response_object_type(self, mock_test_records_api):
        """Test that the method returns a Response object"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "testrecords"}}
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration
        )

        # Assert
        assert response is not None
        assert hasattr(response, 'status_code')
        assert hasattr(response, 'json')
        assert response.status_code == 200
