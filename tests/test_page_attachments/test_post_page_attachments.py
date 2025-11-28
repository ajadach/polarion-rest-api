"""
Tests for PageAttachments.post_page_attachments method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestPostPageAttachments:
    """Test suite for post_page_attachments method"""
    
    def test_post_page_attachments_success(self, mock_page_attachments_api):
        """Test successful creation of page attachments"""
        # Mock response data based on example
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "page_attachments",
                    "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId",
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments/MyAttachmentId?revision=1234",
                        "content": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments/MyAttachmentId/content?revision=1234"
                    }
                }
            ]
        }
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        # Prepare request data
        data = {
            "resource": '''{
                "data": [
                    {
                        "type": "page_attachments",
                        "lid": "attachment1",
                        "attributes": {
                            "fileName": "File Name",
                            "title": "Title"
                        }
                    }
                ]
            }'''
        }
        
        files = {
            "files": ("test.pdf", b"PDF content", "application/pdf")
        }
        
        # Call the method
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=files
        )
        
        # Verify the call
        mock_page_attachments_api._session.post.assert_called_once()
        call_args = mock_page_attachments_api._session.post.call_args
        
        # Check URL
        assert 'projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments' in call_args[0][0]
        
        # Verify response
        assert response.status_code == 201
        assert len(response.json()['data']) == 1
        assert response.json()['data'][0]['type'] == 'page_attachments'
        assert 'links' in response.json()['data'][0]
    
    def test_post_page_attachments_multiple_files(self, mock_page_attachments_api):
        """Test creating multiple page attachments at once"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "page_attachments",
                    "id": "MyProjectId/MySpaceId/MyRichPageId/attachment1"
                },
                {
                    "type": "page_attachments",
                    "id": "MyProjectId/MySpaceId/MyRichPageId/attachment2"
                }
            ]
        }
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        # Prepare multiple attachments
        data = {
            "resource": '''{
                "data": [
                    {
                        "type": "page_attachments",
                        "lid": "attachment1",
                        "attributes": {
                            "fileName": "file1.pdf",
                            "title": "First File"
                        }
                    },
                    {
                        "type": "page_attachments",
                        "lid": "attachment2",
                        "attributes": {
                            "fileName": "file2.png",
                            "title": "Second File"
                        }
                    }
                ]
            }'''
        }
        
        files = [
            ("files", ("file1.pdf", b"PDF content", "application/pdf")),
            ("files", ("file2.png", b"PNG content", "image/png"))
        ]
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=files
        )
        
        # Verify response
        assert response.status_code == 201
        assert len(response.json()['data']) == 2
    
    def test_post_page_attachments_with_lid(self, mock_page_attachments_api):
        """Test creating attachments with local ID (lid) attribute"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "page_attachments",
                    "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId"
                }
            ]
        }
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        # Data with lid attribute
        data = {
            "resource": '''{
                "data": [
                    {
                        "type": "page_attachments",
                        "lid": "custom-lid-123",
                        "attributes": {
                            "fileName": "document.pdf",
                            "title": "Important Document"
                        }
                    }
                ]
            }'''
        }
        
        files = {
            "files": ("document.pdf", b"content", "application/pdf")
        }
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=files
        )
        
        # Verify call was made with data and files
        call_args = mock_page_attachments_api._session.post.call_args
        assert call_args[1]['data'] == data
        assert call_args[1]['files'] == files
        assert response.status_code == 201
    
    def test_post_page_attachments_without_lid(self, mock_page_attachments_api):
        """Test creating attachments without lid (identified by order)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "page_attachments",
                    "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId"
                }
            ]
        }
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        # Data without lid attribute - files identified by order
        data = {
            "resource": '''{
                "data": [
                    {
                        "type": "page_attachments",
                        "attributes": {
                            "fileName": "ordered-file.pdf",
                            "title": "File By Order"
                        }
                    }
                ]
            }'''
        }
        
        files = {
            "files": ("ordered-file.pdf", b"content", "application/pdf")
        }
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=files
        )
        
        assert response.status_code == 201
    
    def test_post_page_attachments_with_default_space(self, mock_page_attachments_api):
        """Test creating attachments in _default space"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": [{"type": "page_attachments"}]}
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        data = {
            "resource": '''{
                "data": [{
                    "type": "page_attachments",
                    "attributes": {"fileName": "file.pdf", "title": "Title"}
                }]
            }'''
        }
        
        files = {"files": ("file.pdf", b"content", "application/pdf")}
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='_default',
            page_name='MyRichPageId',
            data=data,
            files=files
        )
        
        # Verify URL contains _default
        call_args = mock_page_attachments_api._session.post.call_args
        assert 'spaces/_default/' in call_args[0][0]
        assert response.status_code == 201
    
    def test_post_page_attachments_error_400(self, mock_page_attachments_api):
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
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        data = {
            "resource": '''{"data": [{"type": "page_attachments"}]}'''
        }
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=None
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
    
    def test_post_page_attachments_error_401(self, mock_page_attachments_api):
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
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        data = {
            "resource": '''{"data": [{"type": "page_attachments"}]}'''
        }
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=None
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
        assert errors[0]['detail'] == 'No access token'
    
    def test_post_page_attachments_pdf_file(self, mock_page_attachments_api):
        """Test uploading PDF file"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "page_attachments",
                    "id": "MyProjectId/MySpaceId/MyRichPageId/document.pdf"
                }
            ]
        }
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        data = {
            "resource": '''{
                "data": [{
                    "type": "page_attachments",
                    "attributes": {"fileName": "document.pdf", "title": "PDF Document"}
                }]
            }'''
        }
        
        files = {
            "files": ("document.pdf", b"%PDF-1.4...", "application/pdf")
        }
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=files
        )
        
        assert response.status_code == 201
        assert 'document.pdf' in response.json()['data'][0]['id']
    
    def test_post_page_attachments_image_file(self, mock_page_attachments_api):
        """Test uploading image file"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "page_attachments",
                    "id": "MyProjectId/MySpaceId/MyRichPageId/screenshot.png"
                }
            ]
        }
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        data = {
            "resource": '''{
                "data": [{
                    "type": "page_attachments",
                    "attributes": {"fileName": "screenshot.png", "title": "Screenshot"}
                }]
            }'''
        }
        
        files = {
            "files": ("screenshot.png", b"\x89PNG\r\n\x1a\n", "image/png")
        }
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=files
        )
        
        assert response.status_code == 201
    
    def test_post_page_attachments_text_file(self, mock_page_attachments_api):
        """Test uploading text file"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "page_attachments",
                    "id": "MyProjectId/MySpaceId/MyRichPageId/notes.txt"
                }
            ]
        }
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        data = {
            "resource": '''{
                "data": [{
                    "type": "page_attachments",
                    "attributes": {"fileName": "notes.txt", "title": "Notes"}
                }]
            }'''
        }
        
        files = {
            "files": ("notes.txt", b"Some notes here", "text/plain")
        }
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=files
        )
        
        assert response.status_code == 201
    
    def test_post_page_attachments_response_links(self, mock_page_attachments_api):
        """Test that response contains proper links"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "page_attachments",
                    "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId",
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments/MyAttachmentId?revision=1234",
                        "content": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments/MyAttachmentId/content?revision=1234"
                    }
                }
            ]
        }
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        data = {
            "resource": '''{"data": [{"type": "page_attachments", "attributes": {"fileName": "file.pdf"}}]}'''
        }
        files = {"files": ("file.pdf", b"content", "application/pdf")}
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=files
        )
        
        # Verify links structure
        assert response.status_code == 201
        data_item = response.json()['data'][0]
        assert 'links' in data_item
        assert 'self' in data_item['links']
        assert 'content' in data_item['links']
        assert 'attachments' in data_item['links']['self']
        assert 'content' in data_item['links']['content']
    
    def test_post_page_attachments_url_structure(self, mock_page_attachments_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        data = {"resource": '''{"data": []}'''}
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='TEST_PROJ',
            space_id='TEST_SPACE',
            page_name='TEST_PAGE',
            data=data,
            files=None
        )
        
        # Verify URL structure
        call_args = mock_page_attachments_api._session.post.call_args
        url = call_args[0][0]
        
        assert 'projects/TEST_PROJ' in url
        assert 'spaces/TEST_SPACE' in url
        assert 'pages/TEST_PAGE' in url
        assert url.endswith('/attachments')
        assert response.status_code == 201
    
    def test_post_page_attachments_with_only_data(self, mock_page_attachments_api):
        """Test posting with only metadata (no files)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        data = {
            "resource": '''{
                "data": [{
                    "type": "page_attachments",
                    "attributes": {"fileName": "file.pdf", "title": "Title"}
                }]
            }'''
        }
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=None
        )
        
        # Verify call
        call_args = mock_page_attachments_api._session.post.call_args
        assert call_args[1]['data'] == data
        assert call_args[1]['files'] is None
        assert response.status_code == 201
    
    def test_post_page_attachments_with_only_files(self, mock_page_attachments_api):
        """Test posting with only files (no metadata)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        files = {
            "files": ("file.pdf", b"content", "application/pdf")
        }
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=None,
            files=files
        )
        
        # Verify call
        call_args = mock_page_attachments_api._session.post.call_args
        assert call_args[1]['data'] is None
        assert call_args[1]['files'] == files
        assert response.status_code == 201
    
    def test_post_page_attachments_with_special_characters(self, mock_page_attachments_api):
        """Test uploading files with special characters in names"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": [{"type": "page_attachments"}]}
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        data = {
            "resource": '''{
                "data": [{
                    "type": "page_attachments",
                    "attributes": {"fileName": "file-2023 (v2).pdf", "title": "Special File"}
                }]
            }'''
        }
        
        files = {
            "files": ("file-2023 (v2).pdf", b"content", "application/pdf")
        }
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='My-Project',
            space_id='My Space',
            page_name='My Page',
            data=data,
            files=files
        )
        
        mock_page_attachments_api._session.post.assert_called_once()
        assert response.status_code == 201
    
    def test_post_page_attachments_large_file(self, mock_page_attachments_api):
        """Test uploading large file"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": [{"type": "page_attachments"}]}
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        # Simulate large file (5MB)
        large_content = b'x' * (5 * 1024 * 1024)
        
        data = {
            "resource": '''{
                "data": [{
                    "type": "page_attachments",
                    "attributes": {"fileName": "large.zip", "title": "Large File"}
                }]
            }'''
        }
        
        files = {
            "files": ("large.zip", large_content, "application/zip")
        }
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=files
        )
        
        assert response.status_code == 201
    
    def test_post_page_attachments_multipart_form_data(self, mock_page_attachments_api):
        """Test that method uses multipart/form-data for upload"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_page_attachments_api._session.post.return_value = mock_response
        
        data = {"resource": '''{"data": []}'''}
        files = {"files": ("file.pdf", b"content", "application/pdf")}
        
        response = mock_page_attachments_api.post_page_attachments(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            data=data,
            files=files
        )
        
        # Verify both data and files are passed (multipart/form-data)
        call_args = mock_page_attachments_api._session.post.call_args
        assert 'data' in call_args[1]
        assert 'files' in call_args[1]
        assert response.status_code == 201
