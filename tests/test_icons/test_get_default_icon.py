"""
Pytest tests for get_default_icon method in Icons class.

Tests the GET /enumerations/defaulticons/{iconId} endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_get_default_icon.py -v
"""
import pytest
from unittest.mock import Mock
import json


@pytest.mark.get
class TestGetDefaultIcon:
    """Unit tests for get_default_icon method using mocks"""
    
    def test_get_default_icon_success_with_200(self, mock_icons_api):
        """Test successful retrieval of a default icon with 200 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 200 status code
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "icons",
                "id": "default/example.gif",
                "revision": "1234",
                "attributes": {
                    "iconUrl": "pathexample",
                    "id": "pathexample",
                    "path": "pathexample"
                },
                "meta": {
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
                },
                "links": {
                    "self": "server-host-name/application-path/enumerations/defaulticons/example.gif"
                }
            },
            "included": [
                {}
            ],
            "links": {
                "self": "server-host-name/application-path/enumerations/defaulticons/example.gif"
            }
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_default_icon(icon_id='example.gif')
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert data['data']['type'] == 'icons'
        assert data['data']['id'] == 'default/example.gif'
        assert 'attributes' in data['data']
        assert 'iconUrl' in data['data']['attributes']
        assert 'path' in data['data']['attributes']
        
        # Verify correct endpoint was called
        call_args = mock_icons_api._session.get.call_args
        assert 'enumerations/defaulticons/example.gif' in call_args[0][0]
        print("\n✓ Mock: Default icon retrieved successfully with 200 status code")
    
    def test_get_default_icon_unauthorized_401(self, mock_icons_api):
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
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_default_icon(icon_id='example.gif')
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert 'errors' in data
        assert data['errors'][0]['status'] == '401'
        assert data['errors'][0]['title'] == 'Unauthorized'
        assert data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_get_default_icon_bad_request_400(self, mock_icons_api):
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
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_default_icon(icon_id='invalid_icon')
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert 'errors' in data
        assert data['errors'][0]['status'] == '400'
        assert data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code")
    
    def test_get_default_icon_not_found_404(self, mock_icons_api):
        """Test retrieving non-existent icon (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Icon not found"
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_default_icon(icon_id='nonexistent.gif')
        
        # Assert
        assert response.status_code == 404
        print("\n✓ Mock: Non-existent icon returns 404")
    
    def test_get_default_icon_with_default_fields(self, mock_icons_api):
        """Test retrieval with default fields applied (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "icons",
                "id": "default/test.gif"
            }
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute without custom fields (should apply defaults)
        response = mock_icons_api.get_default_icon(icon_id='test.gif')
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify default fields are applied
        expected_fields = [
            'collections', 'categories', 'documents', 'document_attachments',
            'document_comments', 'document_parts', 'enumerations', 'globalroles',
            'icons', 'jobs', 'linkedworkitems', 'externallylinkedworkitems',
            'linkedoslcresources', 'pages', 'page_attachments', 'plans',
            'projectroles', 'projects', 'projecttemplates', 'testparameters',
            'testparameter_definitions', 'testrecords', 'teststep_results',
            'testruns', 'testrun_attachments', 'teststepresult_attachments',
            'testrun_comments', 'usergroups', 'users', 'workitems',
            'workitem_attachments', 'workitem_approvals', 'workitem_comments',
            'featureselections', 'teststeps', 'workrecords', 'revisions',
            'testrecord_attachments'
        ]
        
        for field in expected_fields:
            field_key = f'fields[{field}]'
            assert field_key in params, f"Missing default field: {field_key}"
            assert params[field_key] == '@all', f"Field {field_key} should be '@all'"
        
        print("\n✓ Mock: Default fields applied correctly")
    
    def test_get_default_icon_with_custom_fields(self, mock_icons_api):
        """Test retrieval with custom fields filter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "icons",
                "id": "default/test.gif"
            }
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute with custom fields
        custom_fields = {
            'icons': 'id,attributes.iconUrl,attributes.path',
            'projects': 'id,attributes.name'
        }
        response = mock_icons_api.get_default_icon(
            icon_id='test.gif',
            fields=custom_fields
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom fields override defaults
        assert 'fields[icons]' in params
        assert params['fields[icons]'] == 'id,attributes.iconUrl,attributes.path'
        assert 'fields[projects]' in params
        assert params['fields[projects]'] == 'id,attributes.name'
        
        # Verify other default fields are still present
        assert 'fields[collections]' in params
        assert params['fields[collections]'] == '@all'
        
        print("\n✓ Mock: Custom fields override defaults correctly")
    
    def test_get_default_icon_with_various_icon_ids(self, mock_icons_api):
        """Test retrieval with various icon ID formats (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "icons",
                "id": "default/test.gif"
            }
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Test various icon ID formats
        icon_ids = [
            'example.gif',
            'test-icon.png',
            'icon_name.svg',
            'folder/icon.gif'
        ]
        
        for icon_id in icon_ids:
            response = mock_icons_api.get_default_icon(icon_id=icon_id)
            
            # Assert
            assert response.status_code == 200
            call_args = mock_icons_api._session.get.call_args
            assert f'enumerations/defaulticons/{icon_id}' in call_args[0][0]
        
        print("\n✓ Mock: Various icon ID formats handled correctly")
    
    def test_get_default_icon_endpoint_format(self, mock_icons_api):
        """Test that the correct endpoint format is used (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "icons",
                "id": "default/iconId"
            }
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_default_icon(icon_id='iconId')
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        endpoint = call_args[0][0]
        
        # Verify endpoint matches expected format from CURL
        assert 'enumerations/defaulticons/iconId' in endpoint
        
        print("\n✓ Mock: Correct endpoint format used")
    
    def test_get_default_icon_response_structure(self, mock_icons_api):
        """Test that response has correct structure (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "icons",
                "id": "default/example.gif",
                "revision": "1234",
                "attributes": {
                    "iconUrl": "pathexample",
                    "id": "pathexample",
                    "path": "pathexample"
                },
                "links": {
                    "self": "server-host-name/application-path/enumerations/defaulticons/example.gif"
                }
            },
            "links": {
                "self": "server-host-name/application-path/enumerations/defaulticons/example.gif"
            }
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_default_icon(icon_id='example.gif')
        
        # Assert response structure
        assert response.status_code == 200
        data = response.json()
        
        # Check top-level structure
        assert 'data' in data
        assert 'links' in data
        
        # Check data structure
        assert 'type' in data['data']
        assert 'id' in data['data']
        assert 'revision' in data['data']
        assert 'attributes' in data['data']
        assert 'links' in data['data']
        
        # Check attributes structure
        assert 'iconUrl' in data['data']['attributes']
        assert 'id' in data['data']['attributes']
        assert 'path' in data['data']['attributes']
        
        print("\n✓ Mock: Response structure is correct")
    
    def test_get_default_icon_with_special_characters(self, mock_icons_api):
        """Test retrieval with icon ID containing special characters (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "icons",
                "id": "default/icon-with_special.chars.gif"
            }
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute with special characters in icon ID
        icon_id = 'icon-with_special.chars.gif'
        response = mock_icons_api.get_default_icon(icon_id=icon_id)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        assert f'enumerations/defaulticons/{icon_id}' in call_args[0][0]
        print("\n✓ Mock: Icon ID with special characters handled correctly")
    
    def test_get_default_icon_included_section(self, mock_icons_api):
        """Test that included section is present in response (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "icons",
                "id": "default/example.gif",
                "attributes": {
                    "iconUrl": "pathexample",
                    "id": "pathexample",
                    "path": "pathexample"
                }
            },
            "included": [
                {}
            ]
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_default_icon(icon_id='example.gif')
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert 'included' in data
        assert isinstance(data['included'], list)
        print("\n✓ Mock: Included section present in response")
    
    def test_get_default_icon_links_section(self, mock_icons_api):
        """Test that links section is present and correct (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "icons",
                "id": "default/example.gif",
                "links": {
                    "self": "server-host-name/application-path/enumerations/defaulticons/example.gif"
                }
            },
            "links": {
                "self": "server-host-name/application-path/enumerations/defaulticons/example.gif"
            }
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_default_icon(icon_id='example.gif')
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert 'links' in data
        assert 'self' in data['links']
        assert 'links' in data['data']
        assert 'self' in data['data']['links']
        print("\n✓ Mock: Links sections present and correct")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
