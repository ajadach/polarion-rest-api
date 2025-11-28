"""
Tests for get_document_attachment_content method from DocumentAttachments module.
"""
import pytest
from unittest.mock import Mock


class TestGetDocumentAttachmentContent:
    """Tests for get_document_attachment_content method"""
    
    def test_get_document_attachment_content_basic(self, mock_document_attachments_api):
        """Test downloading file content with basic parameters"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'PDF file content here'
        mock_response.headers = {'Content-Type': 'application/pdf'}
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachment_content(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="MyAttachment"
        )
        
        # Verify
        assert response.status_code == 200
        assert response.content == b'PDF file content here'
        assert response.headers['Content-Type'] == 'application/pdf'
        mock_document_attachments_api._session.get.assert_called_once()
    
    def test_get_document_attachment_content_with_revision(self, mock_document_attachments_api):
        """Test downloading file content with revision parameter"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'File content'
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachment_content(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="MyAttachment",
            revision="5678"
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_document_attachments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '5678'
    
    def test_get_document_attachment_content_url_construction(self, mock_document_attachments_api):
        """Test URL construction for get_document_attachment_content"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'content'
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        mock_document_attachments_api.get_document_attachment_content(
            project_id="TestProject",
            space_id="TestSpace",
            document_name="TestDocument",
            attachment_id="TestAttachment"
        )
        
        # Verify URL
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/TestProject/spaces/TestSpace/documents/TestDocument/attachments/TestAttachment/content"
        call_args = mock_document_attachments_api._session.get.call_args
        assert call_args[0][0] == expected_url
    
    def test_get_document_attachment_content_no_fields_param(self, mock_document_attachments_api):
        """Test that no fields parameter is added for content download"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'content'
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachment_content(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="MyAttachment"
        )
        
        # Verify that no fields parameters are present
        call_args = mock_document_attachments_api._session.get.call_args
        params = call_args[1]['params'] if call_args[1].get('params') else {}
        # Fields should not be present for content download
        for key in params.keys():
            assert not key.startswith('fields[')
    
    def test_get_document_attachment_content_different_file_types(self, mock_document_attachments_api):
        """Test downloading different file types"""
        file_types = [
            ('application/pdf', b'%PDF-1.4'),
            ('image/png', b'\x89PNG\r\n'),
            ('text/plain', b'Plain text content'),
            ('application/zip', b'PK\x03\x04')
        ]
        
        for content_type, content in file_types:
            # Setup mock
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = content
            mock_response.headers = {'Content-Type': content_type}
            mock_document_attachments_api._session.get.return_value = mock_response
            
            # Execute
            response = mock_document_attachments_api.get_document_attachment_content(
                project_id="MyProject",
                space_id="MySpace",
                document_name="MyDocument",
                attachment_id="MyAttachment"
            )
            
            # Verify
            assert response.status_code == 200
            assert response.content == content
            assert response.headers['Content-Type'] == content_type
    
    def test_get_document_attachment_content_not_found(self, mock_document_attachments_api):
        """Test downloading content for non-existent attachment"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Attachment not found"
            }]
        }
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachment_content(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="NonExistent"
        )
        
        # Verify
        assert response.status_code == 404
    
    def test_get_document_attachment_content_empty_params_when_no_revision(self, mock_document_attachments_api):
        """Test that params dict is empty when revision is not provided"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'content'
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute without revision
        response = mock_document_attachments_api.get_document_attachment_content(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="MyAttachment"
        )
        
        # Verify that params is either None or empty dict
        call_args = mock_document_attachments_api._session.get.call_args
        params = call_args[1].get('params')
        # params should be None or empty dict {}
        assert params is None or params == {}
