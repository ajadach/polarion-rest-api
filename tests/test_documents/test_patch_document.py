"""
Unit tests for Documents.patch_document method.
Tests the endpoint: PATCH /projects/{projectId}/spaces/{spaceId}/documents/{documentName}
"""
import pytest
from unittest.mock import Mock
from requests import Response


@pytest.fixture
def mock_response():
    """Create a mock response object"""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {}
    return response


class TestPatchDocument:
    """Test suite for patch_document method."""

    def test_basic_patch_without_workflow_action(self, mock_documents_api, mock_response):
        """Test basic PATCH request without workflow action."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "MyProject/_default/MyDoc",
                "attributes": {
                    "title": "Updated Title",
                    "status": "draft"
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="MyProject",
            space_id="_default",
            document_name="MyDoc",
            document_data=document_data
        )

        mock_documents_api._patch.assert_called_once_with(
            'projects/MyProject/spaces/_default/documents/MyDoc',
            json=document_data,
            params=None
        )
        assert response.status_code == 204

    def test_patch_with_workflow_action(self, mock_documents_api, mock_response):
        """Test PATCH request with workflow action parameter."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "MyProject/_default/MyDoc",
                "attributes": {
                    "status": "approved"
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="MyProject",
            space_id="_default",
            document_name="MyDoc",
            document_data=document_data,
            workflow_action="approve"
        )

        mock_documents_api._patch.assert_called_once_with(
            'projects/MyProject/spaces/_default/documents/MyDoc',
            json=document_data,
            params={'workflowAction': 'approve'}
        )
        assert response.status_code == 204

    def test_patch_with_full_document_structure(self, mock_documents_api, mock_response):
        """Test PATCH with complete document data structure from cURL example."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyDocumentId",
                "attributes": {
                    "autoSuspect": True,
                    "homePageContent": {
                        "type": "text/html",
                        "value": "My text value"
                    },
                    "outlineNumbering": {
                        "prefix": "ABC"
                    },
                    "renderingLayouts": [
                        {
                            "type": "task",
                            "label": "My label",
                            "layouter": "paragraph",
                            "properties": [
                                {
                                    "key": "fieldsAtStart",
                                    "value": "id"
                                }
                            ]
                        }
                    ],
                    "status": "draft",
                    "title": "Title",
                    "type": "req_specification",
                    "usesOutlineNumbering": True
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="MyProjectId",
            space_id="MySpaceId",
            document_name="MyDocumentId",
            document_data=document_data,
            workflow_action="submit"
        )

        mock_documents_api._patch.assert_called_once_with(
            'projects/MyProjectId/spaces/MySpaceId/documents/MyDocumentId',
            json=document_data,
            params={'workflowAction': 'submit'}
        )
        assert response.status_code == 204

    def test_patch_only_title(self, mock_documents_api, mock_response):
        """Test PATCH updating only the title attribute."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "TestProject/_default/TestDoc",
                "attributes": {
                    "title": "New Document Title"
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="TestProject",
            space_id="_default",
            document_name="TestDoc",
            document_data=document_data
        )

        assert response.status_code == 204
        mock_documents_api._patch.assert_called_once()

    def test_patch_only_status(self, mock_documents_api, mock_response):
        """Test PATCH updating only the status attribute."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "TestProject/_default/TestDoc",
                "attributes": {
                    "status": "in_review"
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="TestProject",
            space_id="_default",
            document_name="TestDoc",
            document_data=document_data
        )

        assert response.status_code == 204

    def test_patch_multiple_attributes(self, mock_documents_api, mock_response):
        """Test PATCH updating multiple attributes at once."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "MyProject/_default/MyDoc",
                "attributes": {
                    "title": "Updated Title",
                    "status": "approved",
                    "type": "requirement",
                    "autoSuspect": False
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="MyProject",
            space_id="_default",
            document_name="MyDoc",
            document_data=document_data
        )

        assert response.status_code == 204

    def test_patch_with_home_page_content(self, mock_documents_api, mock_response):
        """Test PATCH updating homePageContent."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {
                    "homePageContent": {
                        "type": "text/html",
                        "value": "<h1>Welcome</h1><p>This is the home page content.</p>"
                    }
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 204

    def test_patch_with_outline_numbering(self, mock_documents_api, mock_response):
        """Test PATCH updating outline numbering settings."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {
                    "usesOutlineNumbering": True,
                    "outlineNumbering": {
                        "prefix": "REQ-"
                    }
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 204

    def test_patch_with_rendering_layouts(self, mock_documents_api, mock_response):
        """Test PATCH updating rendering layouts."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {
                    "renderingLayouts": [
                        {
                            "type": "task",
                            "label": "Task Layout",
                            "layouter": "section",
                            "properties": [
                                {"key": "showTitle", "value": "true"},
                                {"key": "fieldsAtStart", "value": "id,status"}
                            ]
                        }
                    ]
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 204

    def test_error_400_bad_request(self, mock_documents_api, mock_response):
        """Test handling of 400 Bad Request error."""
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
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": "invalid_structure"  # Invalid data structure
        }

        response = mock_documents_api.patch_document(
            project_id="MyProjectId",
            space_id="_default",
            document_name="MyDoc",
            document_data=document_data
        )

        assert response.status_code == 400
        error_data = response.json()
        assert "errors" in error_data
        assert error_data["errors"][0]["status"] == "400"
        assert error_data["errors"][0]["title"] == "Bad Request"
        assert "Unexpected token" in error_data["errors"][0]["detail"]
        assert error_data["errors"][0]["source"]["pointer"] == "$.data"

    def test_error_401_unauthorized(self, mock_documents_api, mock_response):
        """Test handling of 401 Unauthorized error."""
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "Invalid or expired authentication token"
                }
            ]
        }
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {"title": "Test"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 401

    def test_error_403_forbidden(self, mock_documents_api, mock_response):
        """Test handling of 403 Forbidden error."""
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "Insufficient permissions to update document"
                }
            ]
        }
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {"title": "Test"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 403

    def test_error_404_not_found(self, mock_documents_api, mock_response):
        """Test handling of 404 Not Found error."""
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Document 'NonExistentDoc' not found in space '_default'"
                }
            ]
        }
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/NonExistentDoc",
                "attributes": {"title": "Test"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="NonExistentDoc",
            document_data=document_data
        )

        assert response.status_code == 404

    def test_error_409_conflict(self, mock_documents_api, mock_response):
        """Test handling of 409 Conflict error."""
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "409",
                    "title": "Conflict",
                    "detail": "Document has been modified by another user"
                }
            ]
        }
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {"title": "Test"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 409

    def test_error_413_request_entity_too_large(self, mock_documents_api, mock_response):
        """Test handling of 413 Request Entity Too Large error."""
        mock_response.status_code = 413
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "413",
                    "title": "Request Entity Too Large",
                    "detail": "Request body exceeds maximum allowed size"
                }
            ]
        }
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {
                    "homePageContent": {
                        "type": "text/html",
                        "value": "x" * 10000000  # Very large content
                    }
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 413

    def test_error_415_unsupported_media_type(self, mock_documents_api, mock_response):
        """Test handling of 415 Unsupported Media Type error."""
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
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {"title": "Test"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 415

    def test_error_500_internal_server_error(self, mock_documents_api, mock_response):
        """Test handling of 500 Internal Server Error."""
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
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {"title": "Test"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 500

    def test_error_503_service_unavailable(self, mock_documents_api, mock_response):
        """Test handling of 503 Service Unavailable error."""
        mock_response.status_code = 503
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "503",
                    "title": "Service Unavailable",
                    "detail": "Service is temporarily unavailable"
                }
            ]
        }
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {"title": "Test"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 503

    def test_patch_with_default_space(self, mock_documents_api, mock_response):
        """Test PATCH using _default space identifier."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "MyProject/_default/MyDoc",
                "attributes": {"title": "Updated"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="MyProject",
            space_id="_default",
            document_name="MyDoc",
            document_data=document_data
        )

        mock_documents_api._patch.assert_called_once()
        call_args = mock_documents_api._patch.call_args
        assert '_default' in call_args[0][0]
        assert response.status_code == 204

    def test_patch_with_custom_space(self, mock_documents_api, mock_response):
        """Test PATCH using custom space identifier."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "MyProject/CustomSpace/MyDoc",
                "attributes": {"title": "Updated"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="MyProject",
            space_id="CustomSpace",
            document_name="MyDoc",
            document_data=document_data
        )

        mock_documents_api._patch.assert_called_once()
        call_args = mock_documents_api._patch.call_args
        assert 'CustomSpace' in call_args[0][0]
        assert response.status_code == 204

    def test_patch_with_special_characters_in_names(self, mock_documents_api, mock_response):
        """Test PATCH with special characters in project/space/document names."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project-2024/Space_v1/Doc.1",
                "attributes": {"title": "Updated"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project-2024",
            space_id="Space_v1",
            document_name="Doc.1",
            document_data=document_data
        )

        assert response.status_code == 204
        mock_documents_api._patch.assert_called_once_with(
            'projects/Project-2024/spaces/Space_v1/documents/Doc.1',
            json=document_data,
            params=None
        )

    def test_different_workflow_actions(self, mock_documents_api, mock_response):
        """Test PATCH with different workflow action values."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {"status": "approved"}
            }
        }

        workflow_actions = ["approve", "reject", "submit", "reopen", "close"]
        
        for action in workflow_actions:
            response = mock_documents_api.patch_document(
                project_id="Project1",
                space_id="_default",
                document_name="Doc1",
                document_data=document_data,
                workflow_action=action
            )
            
            assert response.status_code == 204
            # Verify workflow action is in params
            call_args = mock_documents_api._patch.call_args
            assert call_args[1]['params']['workflowAction'] == action

    def test_patch_document_type_change(self, mock_documents_api, mock_response):
        """Test PATCH changing document type."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {
                    "type": "req_specification"
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 204

    def test_patch_auto_suspect_flag(self, mock_documents_api, mock_response):
        """Test PATCH updating autoSuspect flag."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {
                    "autoSuspect": False
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        assert response.status_code == 204

    def test_endpoint_path_construction(self, mock_documents_api, mock_response):
        """Test that the correct endpoint path is constructed."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "TestProj/TestSpace/TestDoc",
                "attributes": {"title": "Test"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="TestProj",
            space_id="TestSpace",
            document_name="TestDoc",
            document_data=document_data
        )

        mock_documents_api._patch.assert_called_once()
        call_args = mock_documents_api._patch.call_args
        endpoint = call_args[0][0]
        
        assert endpoint == 'projects/TestProj/spaces/TestSpace/documents/TestDoc'
        assert response.status_code == 204

    def test_params_none_when_no_workflow_action(self, mock_documents_api, mock_response):
        """Test that params is None when workflow_action is not provided."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {"title": "Test"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        call_args = mock_documents_api._patch.call_args
        assert call_args[1]['params'] is None

    def test_params_dict_when_workflow_action_provided(self, mock_documents_api, mock_response):
        """Test that params is a dict when workflow_action is provided."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {"title": "Test"}
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data,
            workflow_action="approve"
        )

        call_args = mock_documents_api._patch.call_args
        assert call_args[1]['params'] == {'workflowAction': 'approve'}

    def test_json_parameter_contains_document_data(self, mock_documents_api, mock_response):
        """Test that json parameter contains the document_data."""
        mock_response.status_code = 204
        mock_documents_api._patch = Mock(return_value=mock_response)

        document_data = {
            "data": {
                "type": "documents",
                "id": "Project1/_default/Doc1",
                "attributes": {
                    "title": "Specific Title",
                    "status": "specific_status"
                }
            }
        }

        response = mock_documents_api.patch_document(
            project_id="Project1",
            space_id="_default",
            document_name="Doc1",
            document_data=document_data
        )

        call_args = mock_documents_api._patch.call_args
        assert call_args[1]['json'] == document_data
        assert call_args[1]['json']['data']['attributes']['title'] == "Specific Title"
