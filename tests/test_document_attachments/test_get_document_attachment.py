"""
Tests for get_document_attachment method from DocumentAttachments module.
"""
import pytest
from unittest.mock import Mock


class TestGetDocumentAttachment:
    """Tests for get_document_attachment method"""
    
    def test_get_document_attachment_basic(self, mock_document_attachments_api):
        """Test getting a single document attachment with basic parameters"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "document_attachments",
                "id": "MyProject/MySpace/MyDoc/MyAttachment",
                "attributes": {
                    "title": "Test Attachment",
                    "fileName": "test.pdf"
                }
            }
        }
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachment(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="MyAttachment"
        )
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert data['data']['type'] == 'document_attachments'
        assert data['data']['id'] == 'MyProject/MySpace/MyDoc/MyAttachment'
        mock_document_attachments_api._session.get.assert_called_once()
    
    def test_get_document_attachment_with_fields(self, mock_document_attachments_api):
        """Test getting document attachment with custom fields"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute with custom fields
        custom_fields = {
            'document_attachments': 'id,title,fileName'
        }
        response = mock_document_attachments_api.get_document_attachment(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="MyAttachment",
            fields=custom_fields
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_document_attachments_api._session.get.call_args
        params = call_args[1]['params']
        # Custom fields should override defaults
        assert 'fields[document_attachments]' in params
        assert params['fields[document_attachments]'] == 'id,title,fileName'
    
    def test_get_document_attachment_with_include(self, mock_document_attachments_api):
        """Test getting document attachment with include parameter"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachment(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="MyAttachment",
            include="author"
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_document_attachments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'author'
