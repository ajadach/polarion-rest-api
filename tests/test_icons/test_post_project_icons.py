"""
Pytest tests for post_project_icons method in Icons class.

Tests the POST /projects/{projectId}/enumerations/icons endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_post_project_icons.py -v
"""
import pytest
from unittest.mock import Mock
import json


@pytest.mark.post
class TestPostProjectIcons:
    """Unit tests for post_project_icons method using mocks"""
    
    def test_post_project_icons_success_with_201(self, mock_icons_api):
        """Test successful creation of project icons with 201 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 201 status code
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "MyProjectId/example.gif",
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/enumerations/icons/example.gif"
                    }
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with data matching BODY from CURL
        project_id = "MyProjectId"
        data = {
            "resource": json.dumps({
                "data": [
                    {
                        "type": "icons"
                    }
                ]
            })
        }
        
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data)
        
        # Assert
        assert response.status_code == 201
        response_data = response.json()
        assert 'data' in response_data
        assert isinstance(response_data['data'], list)
        assert len(response_data['data']) > 0
        assert response_data['data'][0]['type'] == 'icons'
        assert 'id' in response_data['data'][0]
        assert 'MyProjectId' in response_data['data'][0]['id']
        
        # Verify correct endpoint was called
        call_args = mock_icons_api._session.post.call_args
        assert f'projects/{project_id}/enumerations/icons' in call_args[0][0]
        print("\n✓ Mock: Project icons created successfully with 201 status code")
    
    def test_post_project_icons_unauthorized_401(self, mock_icons_api):
        """Test unauthorized access with 401 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 401 status code
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
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data)
        
        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_post_project_icons_bad_request_400(self, mock_icons_api):
        """Test bad request with 400 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 400 status code
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
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with invalid data
        project_id = "MyProjectId"
        data = {"resource": "invalid_json"}
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data)
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '400'
        assert response_data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in response_data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code")
    
    def test_post_project_icons_not_found_404(self, mock_icons_api):
        """Test project not found with 404 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Project 'NonExistentProject' not found"
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "NonExistentProject"
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data)
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '404'
        assert response_data['errors'][0]['title'] == 'Not Found'
        print("\n✓ Mock: Not found returns 404 status code")
    
    def test_post_project_icons_with_files(self, mock_icons_api):
        """Test creation with file uploads (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "MyProjectId/uploaded_icon.gif"
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with data and files
        project_id = "MyProjectId"
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        files = {
            "files": ("icon.gif", b"fake_image_data", "image/gif")
        }
        
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data, files=files)
        
        # Assert
        assert response.status_code == 201
        call_args = mock_icons_api._session.post.call_args
        
        # Verify data and files were passed
        assert call_args[1]['data'] == data
        assert call_args[1]['files'] == files
        print("\n✓ Mock: Project icon creation with files handled correctly")
    
    def test_post_project_icons_with_only_data(self, mock_icons_api):
        """Test creation with only data, no files (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "MyProjectId/icon.gif"
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with only data
        project_id = "MyProjectId"
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data)
        
        # Assert
        assert response.status_code == 201
        call_args = mock_icons_api._session.post.call_args
        assert call_args[1]['data'] == data
        assert call_args[1]['files'] is None
        print("\n✓ Mock: Project icon creation with only data handled correctly")
    
    def test_post_project_icons_with_only_files(self, mock_icons_api):
        """Test creation with only files, no data (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "MyProjectId/icon.gif"
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with only files
        project_id = "MyProjectId"
        files = {
            "files": ("icon.gif", b"fake_image_data", "image/gif")
        }
        
        response = mock_icons_api.post_project_icons(project_id=project_id, files=files)
        
        # Assert
        assert response.status_code == 201
        call_args = mock_icons_api._session.post.call_args
        assert call_args[1]['data'] is None
        assert call_args[1]['files'] == files
        print("\n✓ Mock: Project icon creation with only files handled correctly")
    
    def test_post_project_icons_no_optional_parameters(self, mock_icons_api):
        """Test creation without optional parameters (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": []
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with only required project_id
        project_id = "MyProjectId"
        response = mock_icons_api.post_project_icons(project_id=project_id)
        
        # Assert
        assert response.status_code == 201
        call_args = mock_icons_api._session.post.call_args
        assert call_args[1]['data'] is None
        assert call_args[1]['files'] is None
        print("\n✓ Mock: Project icon creation without optional parameters handled correctly")
    
    def test_post_project_icons_endpoint_format(self, mock_icons_api):
        """Test that the correct endpoint format is used (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{"type": "icons", "id": "MyProjectId/icon.gif"}]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        response = mock_icons_api.post_project_icons(project_id=project_id)
        
        # Assert
        assert response.status_code == 201
        call_args = mock_icons_api._session.post.call_args
        endpoint = call_args[0][0]
        
        # Verify endpoint matches expected format from CURL
        assert f'projects/{project_id}/enumerations/icons' in endpoint
        assert endpoint.endswith(f'projects/{project_id}/enumerations/icons')
        print("\n✓ Mock: Correct project icons POST endpoint format used")
    
    def test_post_project_icons_multiple_icons(self, mock_icons_api):
        """Test creation of multiple icons at once (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "MyProjectId/icon1.gif",
                    "links": {"self": "server/projects/MyProjectId/enumerations/icons/icon1.gif"}
                },
                {
                    "type": "icons",
                    "id": "MyProjectId/icon2.png",
                    "links": {"self": "server/projects/MyProjectId/enumerations/icons/icon2.png"}
                },
                {
                    "type": "icons",
                    "id": "MyProjectId/icon3.svg",
                    "links": {"self": "server/projects/MyProjectId/enumerations/icons/icon3.svg"}
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with multiple icons
        project_id = "MyProjectId"
        data = {
            "resource": json.dumps({
                "data": [
                    {"type": "icons"},
                    {"type": "icons"},
                    {"type": "icons"}
                ]
            })
        }
        
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data)
        
        # Assert
        assert response.status_code == 201
        response_data = response.json()
        assert len(response_data['data']) == 3
        assert all(item['type'] == 'icons' for item in response_data['data'])
        assert all('MyProjectId' in item['id'] for item in response_data['data'])
        print("\n✓ Mock: Multiple project icons creation handled correctly")
    
    def test_post_project_icons_response_structure(self, mock_icons_api):
        """Test that response has correct structure (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "MyProjectId/example.gif",
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/enumerations/icons/example.gif"
                    }
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data)
        
        # Assert response structure
        assert response.status_code == 201
        response_data = response.json()
        
        # Check structure
        assert 'data' in response_data
        assert isinstance(response_data['data'], list)
        assert 'type' in response_data['data'][0]
        assert 'id' in response_data['data'][0]
        assert 'links' in response_data['data'][0]
        assert 'self' in response_data['data'][0]['links']
        
        print("\n✓ Mock: Response structure is correct")
    
    def test_post_project_icons_multipart_form_data(self, mock_icons_api):
        """Test that multipart/form-data is used correctly (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{"type": "icons", "id": "MyProjectId/icon.gif"}]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with form data
        project_id = "MyProjectId"
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        files = {
            "files": ("icon.gif", b"fake_image_data", "image/gif")
        }
        
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data, files=files)
        
        # Assert
        assert response.status_code == 201
        call_args = mock_icons_api._session.post.call_args
        
        # Verify that _post was called with correct parameters
        assert 'data' in call_args[1]
        assert 'files' in call_args[1]
        print("\n✓ Mock: Multipart/form-data handled correctly")
    
    def test_post_project_icons_context_project(self, mock_icons_api):
        """Test that project context endpoint is used (not default or global) (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{"type": "icons", "id": "MyProjectId/icon.gif"}]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        response = mock_icons_api.post_project_icons(project_id=project_id)
        
        # Assert
        assert response.status_code == 201
        call_args = mock_icons_api._session.post.call_args
        endpoint = call_args[0][0]
        
        # Verify this is project context
        assert f'projects/{project_id}/enumerations/icons' in endpoint
        assert 'defaulticons' not in endpoint
        assert 'projects/' in endpoint
        print("\n✓ Mock: Correct project context endpoint used (not global or default)")
    
    def test_post_project_icons_different_project_ids(self, mock_icons_api):
        """Test with different project IDs (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{"type": "icons", "id": "TestProject/icon.gif"}]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with different project IDs
        project_ids = ["TestProject", "AnotherProject", "MyProject123"]
        
        for pid in project_ids:
            response = mock_icons_api.post_project_icons(project_id=pid)
            
            # Assert
            assert response.status_code == 201
            call_args = mock_icons_api._session.post.call_args
            endpoint = call_args[0][0]
            assert f'projects/{pid}/enumerations/icons' in endpoint
        
        print("\n✓ Mock: Different project IDs handled correctly")
    
    def test_post_project_icons_conflict_409(self, mock_icons_api):
        """Test conflict error with 409 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "409",
                    "title": "Conflict",
                    "detail": "Icon already exists in the project"
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute
        project_id = "MyProjectId"
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data)
        
        # Assert
        assert response.status_code == 409
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '409'
        assert response_data['errors'][0]['title'] == 'Conflict'
        print("\n✓ Mock: Conflict returns 409 status code")
    
    def test_post_project_icons_entity_too_large_413(self, mock_icons_api):
        """Test request entity too large with 413 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 413
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "413",
                    "title": "Request Entity Too Large",
                    "detail": "Icon file size exceeds maximum allowed size"
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with large file
        project_id = "MyProjectId"
        files = {
            "files": ("large_icon.gif", b"x" * 10000000, "image/gif")  # Very large file
        }
        response = mock_icons_api.post_project_icons(project_id=project_id, files=files)
        
        # Assert
        assert response.status_code == 413
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '413'
        assert response_data['errors'][0]['title'] == 'Request Entity Too Large'
        print("\n✓ Mock: Request entity too large returns 413 status code")
    
    def test_post_project_icons_unsupported_media_type_415(self, mock_icons_api):
        """Test unsupported media type with 415 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 415
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "415",
                    "title": "Unsupported Media Type",
                    "detail": "The uploaded file type is not supported"
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with unsupported file type
        project_id = "MyProjectId"
        files = {
            "files": ("icon.exe", b"fake_executable_data", "application/x-msdownload")
        }
        response = mock_icons_api.post_project_icons(project_id=project_id, files=files)
        
        # Assert
        assert response.status_code == 415
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '415'
        assert response_data['errors'][0]['title'] == 'Unsupported Media Type'
        print("\n✓ Mock: Unsupported media type returns 415 status code")
    
    def test_post_project_icons_multiple_files(self, mock_icons_api):
        """Test creation with multiple file uploads (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "icons", "id": "MyProjectId/icon1.gif"},
                {"type": "icons", "id": "MyProjectId/icon2.png"}
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with multiple files
        project_id = "MyProjectId"
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}, {"type": "icons"}]
            })
        }
        files = [
            ("files", ("icon1.gif", b"fake_gif_data", "image/gif")),
            ("files", ("icon2.png", b"fake_png_data", "image/png"))
        ]
        
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data, files=files)
        
        # Assert
        assert response.status_code == 201
        response_data = response.json()
        assert len(response_data['data']) == 2
        print("\n✓ Mock: Multiple file uploads handled correctly")
    
    def test_post_project_icons_resource_json_format(self, mock_icons_api):
        """Test that resource field is properly formatted JSON (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{"type": "icons", "id": "MyProjectId/icon.gif"}]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with properly formatted resource JSON
        project_id = "MyProjectId"
        resource_data = {
            "data": [
                {
                    "type": "icons"
                }
            ]
        }
        data = {
            "resource": json.dumps(resource_data)
        }
        
        response = mock_icons_api.post_project_icons(project_id=project_id, data=data)
        
        # Assert
        assert response.status_code == 201
        call_args = mock_icons_api._session.post.call_args
        
        # Verify resource is a JSON string
        assert 'resource' in call_args[1]['data']
        assert isinstance(call_args[1]['data']['resource'], str)
        
        # Verify it can be parsed back to dict
        parsed = json.loads(call_args[1]['data']['resource'])
        assert parsed == resource_data
        print("\n✓ Mock: Resource JSON format is correct")
