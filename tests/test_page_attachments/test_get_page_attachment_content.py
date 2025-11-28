"""
Tests for PageAttachments.get_page_attachment_content method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetPageAttachmentContent:
    """Test suite for get_page_attachment_content method"""
    
    def test_get_page_attachment_content_success(self, mock_page_attachments_api):
        """Test successful download of page attachment content"""
        # Mock response with binary content
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'PDF file content here...'
        mock_response.headers = {'Content-Type': 'application/octet-stream'}
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify the call
        mock_page_attachments_api._session.get.assert_called_once()
        call_args = mock_page_attachments_api._session.get.call_args
        
        # Check URL contains /content endpoint
        assert 'projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments/MyAttachmentId/content' in call_args[0][0]
        
        # Verify response
        assert response.status_code == 200
        assert response.content == b'PDF file content here...'
        assert response.headers['Content-Type'] == 'application/octet-stream'
    
    def test_get_page_attachment_content_with_revision(self, mock_page_attachments_api):
        """Test downloading attachment content with specific revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'File content at revision 1234'
        mock_response.headers = {'Content-Type': 'application/octet-stream'}
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call with revision
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId',
            revision='1234'
        )
        
        # Verify revision parameter
        call_args = mock_page_attachments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '1234'
        
        # Verify response
        assert response.status_code == 200
        assert response.content == b'File content at revision 1234'
    
    def test_get_page_attachment_content_without_revision(self, mock_page_attachments_api):
        """Test downloading attachment content without revision (latest version)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'Latest file content'
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call without revision
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify no revision parameter or empty params
        call_args = mock_page_attachments_api._session.get.call_args
        params = call_args[1]['params']
        assert params is None or params == {} or 'revision' not in params
        
        assert response.status_code == 200
    
    def test_get_page_attachment_content_with_default_space(self, mock_page_attachments_api):
        """Test downloading content from _default space"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'Content from default space'
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call with _default space
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='_default',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify URL contains _default
        call_args = mock_page_attachments_api._session.get.call_args
        assert 'spaces/_default/' in call_args[0][0]
        assert response.status_code == 200
    
    def test_get_page_attachment_content_error_400(self, mock_page_attachments_api):
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
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
        assert 'Unexpected token' in errors[0]['detail']
    
    def test_get_page_attachment_content_error_401(self, mock_page_attachments_api):
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
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
        assert errors[0]['detail'] == 'No access token'
    
    def test_get_page_attachment_content_pdf_file(self, mock_page_attachments_api):
        """Test downloading PDF file content"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'%PDF-1.4\n%...'  # PDF file signature
        mock_response.headers = {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename="document.pdf"'
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='document.pdf'
        )
        
        # Verify response
        assert response.status_code == 200
        assert response.content.startswith(b'%PDF')
        assert 'pdf' in response.headers['Content-Type']
    
    def test_get_page_attachment_content_image_file(self, mock_page_attachments_api):
        """Test downloading image file content"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'\x89PNG\r\n\x1a\n'  # PNG file signature
        mock_response.headers = {
            'Content-Type': 'image/png',
            'Content-Disposition': 'attachment; filename="screenshot.png"'
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='screenshot.png'
        )
        
        # Verify response
        assert response.status_code == 200
        assert response.content.startswith(b'\x89PNG')
        assert 'image/png' in response.headers['Content-Type']
    
    def test_get_page_attachment_content_text_file(self, mock_page_attachments_api):
        """Test downloading text file content"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'This is a text file content\nLine 2\nLine 3'
        mock_response.headers = {
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename="notes.txt"'
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='notes.txt'
        )
        
        # Verify response
        assert response.status_code == 200
        assert b'text file content' in response.content
        assert 'text/plain' in response.headers['Content-Type']
    
    def test_get_page_attachment_content_large_file(self, mock_page_attachments_api):
        """Test downloading large file content"""
        # Simulate a large file (10MB)
        large_content = b'x' * (10 * 1024 * 1024)
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = large_content
        mock_response.headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(len(large_content))
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='large_file.bin'
        )
        
        # Verify response
        assert response.status_code == 200
        assert len(response.content) == 10 * 1024 * 1024
        assert response.headers['Content-Length'] == str(len(large_content))
    
    def test_get_page_attachment_content_empty_file(self, mock_page_attachments_api):
        """Test downloading empty file content"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b''
        mock_response.headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Length': '0'
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='empty.txt'
        )
        
        # Verify response
        assert response.status_code == 200
        assert len(response.content) == 0
        assert response.headers['Content-Length'] == '0'
    
    def test_get_page_attachment_content_with_special_characters(self, mock_page_attachments_api):
        """Test downloading content with special characters in filename"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'File content'
        mock_response.headers = {'Content-Type': 'application/octet-stream'}
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call with special characters in attachment_id
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProject-123',
            space_id='My Space',
            page_name='My Page',
            attachment_id='file-2023 (v2).pdf'
        )
        
        # Verify the call was made
        mock_page_attachments_api._session.get.assert_called_once()
        assert response.status_code == 200
    
    def test_get_page_attachment_content_url_structure(self, mock_page_attachments_api):
        """Test that URL is properly constructed for content endpoint"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'content'
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='TEST_PROJ',
            space_id='TEST_SPACE',
            page_name='TEST_PAGE',
            attachment_id='TEST_ATTACH'
        )
        
        # Verify URL structure
        call_args = mock_page_attachments_api._session.get.call_args
        url = call_args[0][0]
        
        # Should contain all path segments in correct order
        assert 'projects/TEST_PROJ' in url
        assert 'spaces/TEST_SPACE' in url
        assert 'pages/TEST_PAGE' in url
        assert 'attachments/TEST_ATTACH' in url
        assert url.endswith('/content')
        
        assert response.status_code == 200
    
    def test_get_page_attachment_content_no_fields_parameter(self, mock_page_attachments_api):
        """Test that content endpoint doesn't use fields parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'content'
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='TEST_PROJ',
            space_id='TEST_SPACE',
            page_name='TEST_PAGE',
            attachment_id='TEST_ATTACH'
        )
        
        # Verify no fields parameter in call
        call_args = mock_page_attachments_api._session.get.call_args
        params = call_args[1]['params']
        
        # Should not contain any fields[...] parameters
        if params:
            for key in params.keys():
                assert not key.startswith('fields[')
        
        assert response.status_code == 200
    
    def test_get_page_attachment_content_binary_types(self, mock_page_attachments_api):
        """Test downloading various binary file types"""
        # Test with ZIP file
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'PK\x03\x04'  # ZIP file signature
        mock_response.headers = {'Content-Type': 'application/zip'}
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        response = mock_page_attachments_api.get_page_attachment_content(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='archive.zip'
        )
        
        assert response.status_code == 200
        assert response.content.startswith(b'PK\x03\x04')
        assert 'zip' in response.headers['Content-Type']
