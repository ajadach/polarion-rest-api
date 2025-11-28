"""
Tests for TestRecords.get_test_record_test_parameter method.

This module contains comprehensive unit tests for the get_test_record_test_parameter method,
covering success scenarios and all error responses defined in the OpenAPI spec.
"""
import pytest
from unittest.mock import Mock


class TestGetTestRecordTestParameter:
    """Test class for get_test_record_test_parameter method"""

    # ========================================================================
    # Success Tests
    # ========================================================================

    def test_get_test_record_test_parameter_success(self, mock_test_records_api):
        """Test successful test parameter retrieval (200 OK)"""
        # Arrange
        project_id = "MyProjectId"
        test_run_id = "MyTestRunId"
        test_case_project_id = "MyTestCaseProjectId"
        test_case_id = "MyTestcaseId"
        iteration = "0"
        test_param_id = "MyTestParameter"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameters",
                "id": "MyProjectId/MyTestRunId/MyTestParameter",
                "revision": "1234",
                "attributes": {
                    "name": "Example Test Parameter value",
                    "value": "Example Test Parameter value"
                },
                "relationships": {
                    "definition": {
                        "data": {
                            "type": "testparameter_definitions",
                            "id": "MyProjectId/MyTestParamDefinition",
                            "revision": "1234"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testparameters/MyTestParameter"
                }
            },
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/testruns/MyTestRunId/testparameters/MyTestParameter"
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["type"] == "testparameters"
        assert data["data"]["id"] == "MyProjectId/MyTestRunId/MyTestParameter"
        assert data["data"]["attributes"]["name"] == "Example Test Parameter value"
        assert data["data"]["attributes"]["value"] == "Example Test Parameter value"
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert "testparameters/MyTestParameter" in call_args[0][0]

    def test_get_test_record_test_parameter_with_fields(self, mock_test_records_api):
        """Test test parameter retrieval with custom fields parameter"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        fields = {"testparameters": "name,value"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameters",
                "id": "test_project/RUN-123/param1",
                "attributes": {
                    "name": "test_param",
                    "value": "test_value"
                }
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id,
            fields=fields
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["attributes"]["name"] == "test_param"
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["fields"] == fields

    def test_get_test_record_test_parameter_with_include(self, mock_test_records_api):
        """Test test parameter retrieval with include parameter"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        include = "definition"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameters",
                "id": "test_project/RUN-123/param1"
            },
            "included": [
                {"type": "testparameter_definitions", "id": "test_project/def1"}
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id,
            include=include
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "included" in data
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["include"] == include

    def test_get_test_record_test_parameter_with_revision(self, mock_test_records_api):
        """Test test parameter retrieval with revision parameter"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        revision = "5678"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameters",
                "id": "test_project/RUN-123/param1",
                "revision": "5678"
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id,
            revision=revision
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["revision"] == "5678"
        
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[1]["params"]["revision"] == revision

    def test_get_test_record_test_parameter_with_all_parameters(self, mock_test_records_api):
        """Test test parameter retrieval with all optional parameters"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        fields = {"testparameters": "name,value"}
        include = "definition"
        revision = "9999"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameters",
                "id": "test_project/RUN-123/param1",
                "revision": "9999"
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id,
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

    def test_get_test_record_test_parameter_400_bad_request(self, mock_test_records_api):
        """Test test parameter retrieval with 400 Bad Request error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        
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
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response.status_code == 400
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "400"

    def test_get_test_record_test_parameter_401_unauthorized(self, mock_test_records_api):
        """Test test parameter retrieval with 401 Unauthorized error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        
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
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response.status_code == 401
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "401"
        assert error_data["errors"][0]["detail"] == "No access token"

    def test_get_test_record_test_parameter_403_forbidden(self, mock_test_records_api):
        """Test test parameter retrieval with 403 Forbidden error"""
        # Arrange
        project_id = "restricted_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You do not have permission to access this test parameter"
                }
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response.status_code == 403
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "403"

    def test_get_test_record_test_parameter_404_not_found(self, mock_test_records_api):
        """Test test parameter retrieval with 404 Not Found error"""
        # Arrange
        project_id = "nonexistent_project"
        test_run_id = "NONEXISTENT-RUN"
        test_case_project_id = "nonexistent_case"
        test_case_id = "TC-999"
        iteration = "1"
        test_param_id = "nonexistent_param"
        
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Test parameter not found"
                }
            ]
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "404"
        assert "not found" in error_data["errors"][0]["detail"].lower()

    def test_get_test_record_test_parameter_406_not_acceptable(self, mock_test_records_api):
        """Test test parameter retrieval with 406 Not Acceptable error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        
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
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response.status_code == 406
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "406"

    def test_get_test_record_test_parameter_500_internal_server_error(self, mock_test_records_api):
        """Test test parameter retrieval with 500 Internal Server Error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        
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
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response.status_code == 500
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "500"

    def test_get_test_record_test_parameter_503_service_unavailable(self, mock_test_records_api):
        """Test test parameter retrieval with 503 Service Unavailable error"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        
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
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response.status_code == 503
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "503"

    # ========================================================================
    # URL Construction Tests
    # ========================================================================

    def test_get_test_record_test_parameter_url_construction(self, mock_test_records_api):
        """Test that URL is correctly constructed with all parameters"""
        # Arrange
        project_id = "my_project"
        test_run_id = "RUN-2024-Q1"
        test_case_project_id = "case_project_main"
        test_case_id = "TC-SMOKE-001"
        iteration = "5"
        test_param_id = "param_xyz"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "testparameters"}}
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/my_project/testruns/RUN-2024-Q1/testrecords/case_project_main/TC-SMOKE-001/5/testparameters/param_xyz"
        mock_test_records_api._session.get.assert_called_once()
        call_args = mock_test_records_api._session.get.call_args
        assert call_args[0][0] == expected_url

    def test_get_test_record_test_parameter_no_optional_params(self, mock_test_records_api):
        """Test test parameter retrieval without optional parameters"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "testparameters"}}
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
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

    def test_get_test_record_test_parameter_with_iteration_zero(self, mock_test_records_api):
        """Test retrieval with iteration number zero"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-001"
        test_case_project_id = "case_proj"
        test_case_id = "TC-001"
        iteration = "0"
        test_param_id = "param1"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameters",
                "id": "test_project/RUN-001/param1"
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response.status_code == 200

    def test_get_test_record_test_parameter_with_special_characters(self, mock_test_records_api):
        """Test test parameter retrieval with special characters in IDs"""
        # Arrange
        project_id = "test-project_v2"
        test_run_id = "RUN-2024-01"
        test_case_project_id = "case_project_123"
        test_case_id = "TC-SPECIAL-001"
        iteration = "2"
        test_param_id = "param_special-123"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameters",
                "id": "test-project_v2/RUN-2024-01/param_special-123"
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response.status_code == 200
        mock_test_records_api._session.get.assert_called_once()

    def test_get_test_record_test_parameter_response_includes_relationships(self, mock_test_records_api):
        """Test that response includes relationships data"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "testparameters",
                "id": "test_project/RUN-123/param1",
                "relationships": {
                    "definition": {
                        "data": {
                            "type": "testparameter_definitions",
                            "id": "test_project/def1"
                        }
                    }
                }
            }
        }
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "relationships" in data["data"]
        assert "definition" in data["data"]["relationships"]

    def test_get_test_record_test_parameter_response_object_type(self, mock_test_records_api):
        """Test that the method returns a Response object"""
        # Arrange
        project_id = "test_project"
        test_run_id = "RUN-123"
        test_case_project_id = "case_project"
        test_case_id = "TC-001"
        iteration = "1"
        test_param_id = "param1"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "testparameters"}}
        mock_test_records_api._session.get.return_value = mock_response

        # Act
        response = mock_test_records_api.get_test_record_test_parameter(
            project_id=project_id,
            test_run_id=test_run_id,
            test_case_project_id=test_case_project_id,
            test_case_id=test_case_id,
            iteration=iteration,
            test_param_id=test_param_id
        )

        # Assert
        assert response is not None
        assert hasattr(response, 'status_code')
        assert hasattr(response, 'json')
        assert response.status_code == 200
