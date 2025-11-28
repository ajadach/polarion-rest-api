"""
Tests for Pages.patch_rich_page method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestPatchRichPage:
    """Test suite for patch_rich_page method"""
    
    def test_patch_rich_page_success(self, mock_pages_api):
        """Test successful update of a page"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = ""
        
        mock_pages_api._session.patch.return_value = mock_response
        
        # Prepare request data based on BODY example
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": "Updated Title"
                }
            }
        }
        
        # Call the method
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        # Verify the call
        mock_pages_api._session.patch.assert_called_once()
        call_args = mock_pages_api._session.patch.call_args
        
        # Check URL
        assert 'projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId' in call_args[0][0]
        
        # Verify json parameter was passed
        assert call_args[1]['json'] == page_data
        
        # Verify response
        assert response.status_code == 200
    
    def test_patch_rich_page_update_title(self, mock_pages_api):
        """Test updating page title"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": "New Page Title"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        # Verify call
        call_args = mock_pages_api._session.patch.call_args
        assert call_args[1]['json']['data']['attributes']['title'] == 'New Page Title'
        assert response.status_code == 200
    
    def test_patch_rich_page_with_default_space(self, mock_pages_api):
        """Test updating page in _default space"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/_default/MyRichPageId",
                "attributes": {
                    "title": "Title"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='_default',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        # Verify URL contains _default
        call_args = mock_pages_api._session.patch.call_args
        assert 'spaces/_default/' in call_args[0][0]
        assert response.status_code == 200
    
    def test_patch_rich_page_error_400(self, mock_pages_api):
        """Test handling of 400 Bad Request error"""
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
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": "Title"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
        assert 'Unexpected token' in errors[0]['detail']
    
    def test_patch_rich_page_error_401(self, mock_pages_api):
        """Test handling of 401 Unauthorized error"""
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
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": "Title"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
        assert errors[0]['detail'] == 'No access token'
    
    def test_patch_rich_page_data_structure(self, mock_pages_api):
        """Test that request data has proper structure"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": "Title"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        # Verify data structure
        call_args = mock_pages_api._session.patch.call_args
        sent_data = call_args[1]['json']
        
        assert 'data' in sent_data
        assert sent_data['data']['type'] == 'pages'
        assert 'id' in sent_data['data']
        assert 'attributes' in sent_data['data']
        assert response.status_code == 200
    
    def test_patch_rich_page_url_structure(self, mock_pages_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "TEST_PROJ/TEST_SPACE/TEST_PAGE",
                "attributes": {
                    "title": "Test Title"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='TEST_PROJ',
            space_id='TEST_SPACE',
            page_name='TEST_PAGE',
            page_data=page_data
        )
        
        # Verify URL structure
        call_args = mock_pages_api._session.patch.call_args
        url = call_args[0][0]
        
        assert 'projects/TEST_PROJ' in url
        assert 'spaces/TEST_SPACE' in url
        assert 'pages/TEST_PAGE' in url
        assert response.status_code == 200
    
    def test_patch_rich_page_with_special_characters(self, mock_pages_api):
        """Test updating page with special characters in name"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "My-Project/My Space/My Page (2023)",
                "attributes": {
                    "title": "Special Title"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='My-Project',
            space_id='My Space',
            page_name='My Page (2023)',
            page_data=page_data
        )
        
        mock_pages_api._session.patch.assert_called_once()
        assert response.status_code == 200
    
    def test_patch_rich_page_minimal_update(self, mock_pages_api):
        """Test minimal page update with only required fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": "T"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        assert response.status_code == 200
    
    def test_patch_rich_page_long_title(self, mock_pages_api):
        """Test updating page with long title"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        long_title = "A" * 500  # Very long title
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": long_title
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        # Verify long title was sent
        call_args = mock_pages_api._session.patch.call_args
        assert len(call_args[1]['json']['data']['attributes']['title']) == 500
        assert response.status_code == 200
    
    def test_patch_rich_page_id_matches_path(self, mock_pages_api):
        """Test that page ID in data matches the path parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "ProjectA/SpaceB/PageC",
                "attributes": {
                    "title": "Title"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='ProjectA',
            space_id='SpaceB',
            page_name='PageC',
            page_data=page_data
        )
        
        # Verify URL and data ID consistency
        call_args = mock_pages_api._session.patch.call_args
        url = call_args[0][0]
        sent_data = call_args[1]['json']
        
        assert 'ProjectA' in url
        assert 'SpaceB' in url
        assert 'PageC' in url
        assert sent_data['data']['id'] == 'ProjectA/SpaceB/PageC'
        assert response.status_code == 200
    
    def test_patch_rich_page_type_validation(self, mock_pages_api):
        """Test that type field is always 'pages'"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": "Title"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        # Verify type is pages
        call_args = mock_pages_api._session.patch.call_args
        assert call_args[1]['json']['data']['type'] == 'pages'
        assert response.status_code == 200
    
    def test_patch_rich_page_empty_title(self, mock_pages_api):
        """Test updating page with empty title"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": ""
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        assert response.status_code == 200
    
    def test_patch_rich_page_unicode_title(self, mock_pages_api):
        """Test updating page with unicode characters in title"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": "Title with émojis 🚀 and ünïcödé"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        # Verify unicode title was sent
        call_args = mock_pages_api._session.patch.call_args
        assert '🚀' in call_args[1]['json']['data']['attributes']['title']
        assert 'ünïcödé' in call_args[1]['json']['data']['attributes']['title']
        assert response.status_code == 200
    
    def test_patch_rich_page_multiple_attributes(self, mock_pages_api):
        """Test updating page with multiple attributes"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": "Updated Title",
                    "customField1": "value1",
                    "customField2": "value2"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        # Verify all attributes were sent
        call_args = mock_pages_api._session.patch.call_args
        attrs = call_args[1]['json']['data']['attributes']
        assert 'title' in attrs
        assert 'customField1' in attrs
        assert 'customField2' in attrs
        assert response.status_code == 200
    
    def test_patch_rich_page_json_content_type(self, mock_pages_api):
        """Test that request uses JSON content type"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_pages_api._session.patch.return_value = mock_response
        
        page_data = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "title": "Title"
                }
            }
        }
        
        response = mock_pages_api.patch_rich_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            page_data=page_data
        )
        
        # Verify json parameter is used (not data)
        call_args = mock_pages_api._session.patch.call_args
        assert 'json' in call_args[1]
        assert 'data' not in call_args[1] or call_args[1].get('data') is None
        assert response.status_code == 200
