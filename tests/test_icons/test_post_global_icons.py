"""
Pytest tests for post_global_icons method in Icons class.

Tests the POST /enumerations/icons endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_post_global_icons.py -v
"""
import pytest
from unittest.mock import Mock
import json


@pytest.mark.post
class TestPostGlobalIcons:
    """Unit tests for post_global_icons method using mocks"""
    
    def test_post_global_icons_success_with_200(self, mock_icons_api):
        """Test successful creation of global icons with 200 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 200 status code
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "default/example.gif",
                    "links": {
                        "self": "server-host-name/application-path/enumerations/defaulticons/example.gif"
                    }
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with data matching BODY from CURL
        data = {
            "resource": json.dumps({
                "data": [
                    {
                        "type": "icons"
                    }
                ]
            })
        }
        
        response = mock_icons_api.post_global_icons(data=data)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert 'data' in response_data
        assert isinstance(response_data['data'], list)
        assert len(response_data['data']) > 0
        assert response_data['data'][0]['type'] == 'icons'
        assert 'id' in response_data['data'][0]
        
        # Verify correct endpoint was called
        call_args = mock_icons_api._session.post.call_args
        assert 'enumerations/icons' in call_args[0][0]
        print("\n✓ Mock: Global icons created successfully with 200 status code")
    
    def test_post_global_icons_unauthorized_401(self, mock_icons_api):
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
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        response = mock_icons_api.post_global_icons(data=data)
        
        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_post_global_icons_bad_request_400(self, mock_icons_api):
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
        data = {"resource": "invalid_json"}
        response = mock_icons_api.post_global_icons(data=data)
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '400'
        assert response_data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in response_data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code")
    
    def test_post_global_icons_with_files(self, mock_icons_api):
        """Test creation with file uploads (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "global/uploaded_icon.gif"
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with data and files
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        files = {
            "files": ("icon.gif", b"fake_image_data", "image/gif")
        }
        
        response = mock_icons_api.post_global_icons(data=data, files=files)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.post.call_args
        
        # Verify data and files were passed
        assert call_args[1]['data'] == data
        assert call_args[1]['files'] == files
        print("\n✓ Mock: Icon creation with files handled correctly")
    
    def test_post_global_icons_with_only_data(self, mock_icons_api):
        """Test creation with only data, no files (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "global/icon.gif"
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with only data
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        
        response = mock_icons_api.post_global_icons(data=data)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.post.call_args
        assert call_args[1]['data'] == data
        assert call_args[1]['files'] is None
        print("\n✓ Mock: Icon creation with only data handled correctly")
    
    def test_post_global_icons_with_only_files(self, mock_icons_api):
        """Test creation with only files, no data (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "global/icon.gif"
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with only files
        files = {
            "files": ("icon.gif", b"fake_image_data", "image/gif")
        }
        
        response = mock_icons_api.post_global_icons(files=files)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.post.call_args
        assert call_args[1]['data'] is None
        assert call_args[1]['files'] == files
        print("\n✓ Mock: Icon creation with only files handled correctly")
    
    def test_post_global_icons_no_parameters(self, mock_icons_api):
        """Test creation without any parameters (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": []
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute without parameters
        response = mock_icons_api.post_global_icons()
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.post.call_args
        assert call_args[1]['data'] is None
        assert call_args[1]['files'] is None
        print("\n✓ Mock: Icon creation without parameters handled correctly")
    
    def test_post_global_icons_endpoint_format(self, mock_icons_api):
        """Test that the correct endpoint format is used (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"type": "icons", "id": "global/icon.gif"}]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute
        response = mock_icons_api.post_global_icons()
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.post.call_args
        endpoint = call_args[0][0]
        
        # Verify endpoint matches expected format from CURL
        assert 'enumerations/icons' in endpoint
        assert endpoint.endswith('enumerations/icons')
        print("\n✓ Mock: Correct global icons POST endpoint format used")
    
    def test_post_global_icons_multiple_icons(self, mock_icons_api):
        """Test creation of multiple icons at once (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "global/icon1.gif",
                    "links": {"self": "server/enumerations/icons/icon1.gif"}
                },
                {
                    "type": "icons",
                    "id": "global/icon2.png",
                    "links": {"self": "server/enumerations/icons/icon2.png"}
                },
                {
                    "type": "icons",
                    "id": "global/icon3.svg",
                    "links": {"self": "server/enumerations/icons/icon3.svg"}
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with multiple icons
        data = {
            "resource": json.dumps({
                "data": [
                    {"type": "icons"},
                    {"type": "icons"},
                    {"type": "icons"}
                ]
            })
        }
        
        response = mock_icons_api.post_global_icons(data=data)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data['data']) == 3
        assert all(item['type'] == 'icons' for item in response_data['data'])
        print("\n✓ Mock: Multiple icons creation handled correctly")
    
    def test_post_global_icons_response_structure(self, mock_icons_api):
        """Test that response has correct structure (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "icons",
                    "id": "default/example.gif",
                    "links": {
                        "self": "server-host-name/application-path/enumerations/defaulticons/example.gif"
                    }
                }
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        response = mock_icons_api.post_global_icons(data=data)
        
        # Assert response structure
        assert response.status_code == 200
        response_data = response.json()
        
        # Check structure
        assert 'data' in response_data
        assert isinstance(response_data['data'], list)
        assert 'type' in response_data['data'][0]
        assert 'id' in response_data['data'][0]
        assert 'links' in response_data['data'][0]
        assert 'self' in response_data['data'][0]['links']
        
        print("\n✓ Mock: Response structure is correct")
    
    def test_post_global_icons_multipart_form_data(self, mock_icons_api):
        """Test that multipart/form-data is used correctly (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"type": "icons", "id": "global/icon.gif"}]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with form data
        data = {
            "resource": json.dumps({
                "data": [{"type": "icons"}]
            })
        }
        files = {
            "files": ("icon.gif", b"fake_image_data", "image/gif")
        }
        
        response = mock_icons_api.post_global_icons(data=data, files=files)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.post.call_args
        
        # Verify that _post was called with correct parameters
        assert 'data' in call_args[1]
        assert 'files' in call_args[1]
        print("\n✓ Mock: Multipart/form-data handled correctly")
    
    def test_post_global_icons_context_global(self, mock_icons_api):
        """Test that global context endpoint is used (not default or project) (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"type": "icons", "id": "global/icon.gif"}]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute
        response = mock_icons_api.post_global_icons()
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.post.call_args
        endpoint = call_args[0][0]
        
        # Verify this is global context
        assert 'enumerations/icons' in endpoint
        assert 'defaulticons' not in endpoint  # Should NOT be default context
        assert 'projects/' not in endpoint  # Should NOT be project context
        
        print("\n✓ Mock: Global context endpoint used correctly")
    
    def test_post_global_icons_different_file_types(self, mock_icons_api):
        """Test creation with different file types (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "icons", "id": "global/icon1.gif"},
                {"type": "icons", "id": "global/icon2.png"},
                {"type": "icons", "id": "global/icon3.svg"}
            ]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Test different file types
        file_types = [
            ("icon.gif", "image/gif"),
            ("icon.png", "image/png"),
            ("icon.svg", "image/svg+xml")
        ]
        
        for filename, mime_type in file_types:
            files = {
                "files": (filename, b"fake_image_data", mime_type)
            }
            response = mock_icons_api.post_global_icons(files=files)
            assert response.status_code == 200
        
        print("\n✓ Mock: Different file types handled correctly")
    
    def test_post_global_icons_json_resource_format(self, mock_icons_api):
        """Test that resource data is properly formatted as JSON (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"type": "icons", "id": "global/icon.gif"}]
        }
        mock_icons_api._session.post.return_value = mock_response
        
        # Execute with properly formatted JSON resource
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
        
        response = mock_icons_api.post_global_icons(data=data)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.post.call_args
        assert 'resource' in call_args[1]['data']
        
        # Verify resource can be parsed back to JSON
        resource_str = call_args[1]['data']['resource']
        parsed_resource = json.loads(resource_str)
        assert 'data' in parsed_resource
        assert parsed_resource['data'][0]['type'] == 'icons'
        
        print("\n✓ Mock: JSON resource format handled correctly")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
