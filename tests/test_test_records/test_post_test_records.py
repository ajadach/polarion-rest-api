"""
Tests for TestRecords.post_test_records method.

This module contains comprehensive unit tests for the post_test_records method,
covering success scenarios and all error responses defined in the OpenAPI spec.
"""
import pytest
from unittest.mock import Mock


class TestPostTestRecords:
    """Test class for post_test_records method"""

    # ========================================================================
    # Success Tests
    # ========================================================================

    def test_post_test_records_success(self, mock_test_records_api):
        """Test successful test records creation (201 Created)"""
        # Arrange
        project_id = "elibrary"
        test_run_id = "MyTestRunId"
        test_records_data = {
            "data": [
                {
                    "type": "testrecords",
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
                        },
                        "testCase": {
                            "data": {
                                "type": "workitems",
                                "id": "MyProjectId/MyWorkItemId"
                            }
                        }
                    }
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testrecords",
                    "id": "elibrary/MyTestRunId/MyProjectId/MyTestcaseId/0",
                    "links": {
                        "self": "server-host-name/application-path/projects/elibrary/testruns/MyTestRunId/testrecords/MyProjectId/MyTestcaseId/0"
                    }
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 1
        assert data["data"][0]["type"] == "testrecords"
        assert data["data"][0]["id"] == "elibrary/MyTestRunId/MyProjectId/MyTestcaseId/0"
        
        mock_test_records_api._session.post.assert_called_once()
        call_args = mock_test_records_api._session.post.call_args
        assert "elibrary/testruns/MyTestRunId/testrecords" in call_args[0][0]
        assert call_args[1]["json"] == test_records_data

    def test_post_test_records_single_record(self, mock_test_records_api):
        """Test creation with a single test record"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {
            "data": [
                {
                    "type": "testrecords",
                    "attributes": {
                        "result": "passed",
                        "duration": 120
                    },
                    "relationships": {
                        "testCase": {
                            "data": {
                                "type": "workitems",
                                "id": "test_project/TC-001"
                            }
                        }
                    }
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testrecords",
                    "id": "test_project/RUN-123/test_project/TC-001/1"
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert len(data["data"]) == 1

    def test_post_test_records_multiple_records(self, mock_test_records_api):
        """Test creation with multiple test records"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {
            "data": [
                {
                    "type": "testrecords",
                    "attributes": {"result": "passed"},
                    "relationships": {
                        "testCase": {"data": {"type": "workitems", "id": "test_project/TC-001"}}
                    }
                },
                {
                    "type": "testrecords",
                    "attributes": {"result": "failed"},
                    "relationships": {
                        "testCase": {"data": {"type": "workitems", "id": "test_project/TC-002"}}
                    }
                },
                {
                    "type": "testrecords",
                    "attributes": {"result": "passed"},
                    "relationships": {
                        "testCase": {"data": {"type": "workitems", "id": "test_project/TC-003"}}
                    }
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "testrecords", "id": "test_project/RUN-123/test_project/TC-001/1"},
                {"type": "testrecords", "id": "test_project/RUN-123/test_project/TC-002/1"},
                {"type": "testrecords", "id": "test_project/RUN-123/test_project/TC-003/1"}
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert len(data["data"]) == 3

    def test_post_test_records_with_all_attributes(self, mock_test_records_api):
        """Test creation with all available attributes"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {
            "data": [
                {
                    "type": "testrecords",
                    "attributes": {
                        "comment": {
                            "type": "text/html",
                            "value": "Detailed test comment"
                        },
                        "duration": 300,
                        "executed": "2024-01-15T10:30:00Z",
                        "result": "passed",
                        "testCaseRevision": "Rev 2.0"
                    },
                    "relationships": {
                        "testCase": {
                            "data": {
                                "type": "workitems",
                                "id": "test_project/TC-001"
                            }
                        },
                        "executedBy": {
                            "data": {
                                "type": "users",
                                "id": "user123"
                            }
                        },
                        "defect": {
                            "data": {
                                "type": "workitems",
                                "id": "test_project/BUG-001"
                            }
                        }
                    }
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "testrecords", "id": "test_project/RUN-123/test_project/TC-001/1"}
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 201
        call_args = mock_test_records_api._session.post.call_args
        assert call_args[1]["json"]["data"][0]["attributes"]["duration"] == 300

    # ========================================================================
    # Error Response Tests
    # ========================================================================

    def test_post_test_records_400_bad_request(self, mock_test_records_api):
        """Test test records creation with 400 Bad Request error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {
            "data": [
                {
                    "type": "testrecords",
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
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 400
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "400"

    def test_post_test_records_401_unauthorized(self, mock_test_records_api):
        """Test test records creation with 401 Unauthorized error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {"data": [{"type": "testrecords"}]}
        
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
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 401
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "401"
        assert error_data["errors"][0]["detail"] == "No access token"

    def test_post_test_records_403_forbidden(self, mock_test_records_api):
        """Test test records creation with 403 Forbidden error"""
        # Arrange
        project_id = "restricted_project"
        test_run_id = "RUN-123"
        test_records_data = {"data": [{"type": "testrecords"}]}
        
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You do not have permission to create test records"
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 403
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "403"

    def test_post_test_records_404_not_found(self, mock_test_records_api):
        """Test test records creation with 404 Not Found error"""
        # Arrange
        project_id = "nonexistent_project"
        test_run_id = "NONEXISTENT-RUN"
        test_records_data = {"data": [{"type": "testrecords"}]}
        
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Test run not found"
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "404"
        assert "not found" in error_data["errors"][0]["detail"].lower()

    def test_post_test_records_413_payload_too_large(self, mock_test_records_api):
        """Test test records creation with 413 Payload Too Large error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {"data": [{"type": "testrecords"}] * 1000}  # Large payload
        
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
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 413
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "413"

    def test_post_test_records_415_unsupported_media_type(self, mock_test_records_api):
        """Test test records creation with 415 Unsupported Media Type error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {"data": [{"type": "testrecords"}]}
        
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
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 415
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "415"

    def test_post_test_records_500_internal_server_error(self, mock_test_records_api):
        """Test test records creation with 500 Internal Server Error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {"data": [{"type": "testrecords"}]}
        
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
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 500
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "500"

    def test_post_test_records_503_service_unavailable(self, mock_test_records_api):
        """Test test records creation with 503 Service Unavailable error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {"data": [{"type": "testrecords"}]}
        
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
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 503
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "503"

    # ========================================================================
    # URL Construction Tests
    # ========================================================================

    def test_post_test_records_url_construction(self, mock_test_records_api):
        """Test that URL is correctly constructed"""
        # Arrange
        project_id = "my_project"
        test_run_id = "RUN-2024-Q1"
        test_records_data = {"data": [{"type": "testrecords"}]}
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/my_project/testruns/RUN-2024-Q1/testrecords"
        mock_test_records_api._session.post.assert_called_once()
        call_args = mock_test_records_api._session.post.call_args
        assert call_args[0][0] == expected_url

    def test_post_test_records_json_body_passed(self, mock_test_records_api):
        """Test that JSON body is correctly passed to the request"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {
            "data": [
                {
                    "type": "testrecords",
                    "attributes": {"result": "passed"},
                    "relationships": {
                        "testCase": {"data": {"type": "workitems", "id": "proj/TC-1"}}
                    }
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        call_args = mock_test_records_api._session.post.call_args
        assert call_args[1]["json"] == test_records_data

    # ========================================================================
    # Edge Case Tests
    # ========================================================================

    def test_post_test_records_with_special_characters(self, mock_test_records_api):
        """Test creation with special characters in IDs"""
        # Arrange
        project_id = "test-project_v2"
        test_run_id = "RUN-2024-01"
        test_records_data = {"data": [{"type": "testrecords"}]}
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 201
        mock_test_records_api._session.post.assert_called_once()

    def test_post_test_records_response_includes_links(self, mock_test_records_api):
        """Test that response includes links to created resources"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {"data": [{"type": "testrecords"}]}
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testrecords",
                    "id": "test_project/RUN-123/proj/TC-001/1",
                    "links": {
                        "self": "server-host-name/application-path/projects/test_project/testruns/RUN-123/testrecords/proj/TC-001/1"
                    }
                }
            ]
        }
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "links" in data["data"][0]
        assert "self" in data["data"][0]["links"]

    def test_post_test_records_response_object_type(self, mock_test_records_api):
        """Test that the method returns a Response object"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_records_data = {"data": [{"type": "testrecords"}]}
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.post.return_value = mock_response

        # Act
        response = mock_test_records_api.post_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_records_data=test_records_data
        )

        # Assert
        assert response is not None
        assert hasattr(response, 'status_code')
        assert hasattr(response, 'json')
        assert response.status_code == 201
