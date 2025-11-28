"""
Tests for TestRecords.get_test_records method.

This module contains comprehensive unit tests for the get_test_records method,
covering success scenarios and all error responses defined in the OpenAPI spec.
"""
import pytest
from unittest.mock import Mock


class TestGetTestRecords:
    """Test class for get_test_records method"""

    # ========================================================================
    # Success Tests
    # ========================================================================

    def test_get_test_records_success(self, mock_test_records_api):
        """Test successful test records list retrieval (200 OK)"""
        # Arrange
        project_id = "elibrary"
        test_run_id = "MyTestRunId"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 1
            },
            "data": [
                {
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
            ],
            "links": {
                "self": "server-host-name/application-path/projects/elibrary/testruns/MyTestRunId/testrecords"
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 1
        assert data["data"][0]["type"] == "testrecords"
        assert data["meta"]["totalCount"] == 1
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert "elibrary/testruns/MyTestRunId/testrecords" in call_args[0][0]

    def test_get_test_records_with_pagination(self, mock_test_records_api):
        """Test test records retrieval with pagination parameters"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        page_size = 10
        page_number = 5
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 100},
            "data": [{"type": "testrecords", "id": f"test_project/RUN-123/case/TC-{i}/1"} for i in range(10)],
            "links": {
                "self": "server-host-name/application-path/projects/test_project/testruns/RUN-123/testrecords?page%5Bsize%5D=10&page%5Bnumber%5D=5",
                "first": "server-host-name/application-path/projects/test_project/testruns/RUN-123/testrecords?page%5Bsize%5D=10&page%5Bnumber%5D=1",
                "prev": "server-host-name/application-path/projects/test_project/testruns/RUN-123/testrecords?page%5Bsize%5D=10&page%5Bnumber%5D=4",
                "next": "server-host-name/application-path/projects/test_project/testruns/RUN-123/testrecords?page%5Bsize%5D=10&page%5Bnumber%5D=6",
                "last": "server-host-name/application-path/projects/test_project/testruns/RUN-123/testrecords?page%5Bsize%5D=10&page%5Bnumber%5D=10"
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            page_size=page_size,
            page_number=page_number
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 10
        assert data["meta"]["totalCount"] == 100
        assert "links" in data
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["page[size]"] == page_size
        assert call_args[1]["params"]["page[number]"] == page_number

    def test_get_test_records_with_fields(self, mock_test_records_api):
        """Test test records retrieval with custom fields parameter"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        fields = {"testrecords": "result,duration,executed"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testrecords",
                    "id": "test_project/RUN-123/case/TC-001/1",
                    "attributes": {
                        "result": "passed",
                        "duration": 120,
                        "executed": "2024-01-15T10:30:00Z"
                    }
                }
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            fields=fields
        )

        # Assert
        assert response.status_code == 200
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["fields"] == fields

    def test_get_test_records_with_include(self, mock_test_records_api):
        """Test test records retrieval with include parameter"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        include = "defect,executedBy,testCase"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"type": "testrecords", "id": "test_project/RUN-123/case/TC-001/1"}],
            "included": [
                {"type": "workitems", "id": "test_project/WI-001"},
                {"type": "users", "id": "user1"}
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            include=include
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "included" in data
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["include"] == include

    def test_get_test_records_with_revision(self, mock_test_records_api):
        """Test test records retrieval with revision parameter"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        revision = "5678"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testrecords",
                    "id": "test_project/RUN-123/case/TC-001/1",
                    "revision": "5678"
                }
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            revision=revision
        )

        # Assert
        assert response.status_code == 200
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["revision"] == revision

    def test_get_test_records_with_filters(self, mock_test_records_api):
        """Test test records retrieval with filter parameters"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        test_result_id = "passed"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testrecords",
                    "id": "test_project/RUN-123/case_project/TC-001/1",
                    "attributes": {"result": "passed"}
                }
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            test_result_id=test_result_id
        )

        # Assert
        assert response.status_code == 200
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["testCaseProjectId"] == test_case_project_id
        assert call_args[1]["params"]["testCaseId"] == test_case_id
        assert call_args[1]["params"]["testResultId"] == test_result_id

    def test_get_test_records_with_all_parameters(self, mock_test_records_api):
        """Test test records retrieval with all optional parameters"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        page_size = 25
        page_number = 3
        fields = {"testrecords": "result,duration"}
        include = "defect,executedBy"
        revision = "9999"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        test_result_id = "failed"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"type": "testrecords", "id": "test_project/RUN-123/case_project/TC-001/1"}]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            page_size=page_size,
            page_number=page_number,
            fields=fields,
            include=include,
            revision=revision,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            test_result_id=test_result_id
        )

        # Assert
        assert response.status_code == 200
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["page[size]"] == page_size
        assert call_args[1]["params"]["page[number]"] == page_number
        assert call_args[1]["params"]["fields"] == fields
        assert call_args[1]["params"]["include"] == include
        assert call_args[1]["params"]["revision"] == revision
        assert call_args[1]["params"]["testCaseProjectId"] == test_case_project_id
        assert call_args[1]["params"]["testCaseId"] == test_case_id
        assert call_args[1]["params"]["testResultId"] == test_result_id

    # ========================================================================
    # Error Response Tests
    # ========================================================================

    def test_get_test_records_400_bad_request(self, mock_test_records_api):
        """Test test records retrieval with 400 Bad Request error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        
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
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        assert response.status_code == 400
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "400"

    def test_get_test_records_401_unauthorized(self, mock_test_records_api):
        """Test test records retrieval with 401 Unauthorized error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        
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
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        assert response.status_code == 401
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "401"
        assert error_data["errors"][0]["detail"] == "No access token"

    def test_get_test_records_403_forbidden(self, mock_test_records_api):
        """Test test records retrieval with 403 Forbidden error"""
        # Arrange
        project_id = "restricted_project"
        test_run_id = "RUN-123"
        
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You do not have permission to access these test records"
                }
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        assert response.status_code == 403
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "403"

    def test_get_test_records_404_not_found(self, mock_test_records_api):
        """Test test records retrieval with 404 Not Found error"""
        # Arrange
        project_id = "nonexistent_project"
        test_run_id = "NONEXISTENT-RUN"
        
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
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "404"
        assert "not found" in error_data["errors"][0]["detail"].lower()

    def test_get_test_records_406_not_acceptable(self, mock_test_records_api):
        """Test test records retrieval with 406 Not Acceptable error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        
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
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        assert response.status_code == 406
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "406"

    def test_get_test_records_500_internal_server_error(self, mock_test_records_api):
        """Test test records retrieval with 500 Internal Server Error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        
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
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        assert response.status_code == 500
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "500"

    def test_get_test_records_503_service_unavailable(self, mock_test_records_api):
        """Test test records retrieval with 503 Service Unavailable error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        
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
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        assert response.status_code == 503
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "503"

    # ========================================================================
    # URL Construction Tests
    # ========================================================================

    def test_get_test_records_url_construction(self, mock_test_records_api):
        """Test that URL is correctly constructed"""
        # Arrange
        project_id = "my_project"
        test_run_id = "RUN-2024-Q1"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/my_project/testruns/RUN-2024-Q1/testrecords"
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[0][0] == expected_url

    def test_get_test_records_no_optional_params(self, mock_test_records_api):
        """Test test records retrieval without optional parameters"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
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

    def test_get_test_records_empty_list(self, mock_test_records_api):
        """Test retrieval with no test records in response"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-001"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": [],
            "links": {"self": "server-host-name/application-path/projects/test_project/testruns/RUN-001/testrecords"}
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["totalCount"] == 0
        assert len(data["data"]) == 0

    def test_get_test_records_with_special_characters(self, mock_test_records_api):
        """Test test records retrieval with special characters in IDs"""
        # Arrange
        project_id = "test-project_v2"
        test_run_id = "RUN-2024-01"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "testrecords",
                    "id": "test-project_v2/RUN-2024-01/case_project_123/TC-SPECIAL-001/2"
                }
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        assert response.status_code == 200
        mock_test_records_api._session.get.assert_called_once()

    def test_get_test_records_pagination_links(self, mock_test_records_api):
        """Test that response includes pagination links"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        page_size = 10
        page_number = 5
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [],
            "links": {
                "self": "server-host-name/application-path/testrecords?page%5Bsize%5D=10&page%5Bnumber%5D=5",
                "first": "server-host-name/application-path/testrecords?page%5Bsize%5D=10&page%5Bnumber%5D=1",
                "prev": "server-host-name/application-path/testrecords?page%5Bsize%5D=10&page%5Bnumber%5D=4",
                "next": "server-host-name/application-path/testrecords?page%5Bsize%5D=10&page%5Bnumber%5D=6",
                "last": "server-host-name/application-path/testrecords?page%5Bsize%5D=10&page%5Bnumber%5D=9"
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            page_size=page_size,
            page_number=page_number
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "links" in data
        assert "first" in data["links"]
        assert "prev" in data["links"]
        assert "next" in data["links"]
        assert "last" in data["links"]

    def test_get_test_records_response_object_type(self, mock_test_records_api):
        """Test that the method returns a Response object"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id
        )

        # Assert
        assert response is not None
        assert hasattr(response, 'status_code')
        assert hasattr(response, 'json')
        assert response.status_code == 200

    def test_get_test_records_with_page_size_zero(self, mock_test_records_api):
        """Test retrieval with page_size of 0"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        page_size = 0
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_records(
            project_id=project_id,
            test_run_id=test_run_id,
            page_size=page_size
        )

        # Assert
        assert response.status_code == 200
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["page[size]"] == 0
