"""
Tests for patch_document_attachment method from DocumentAttachments module.
"""
import pytest
import json
from unittest.mock import Mock, mock_open, patch


class TestPatchDocumentAttachment:
    """Tests for patch_document_attachment method"""
    
    def test_patch_document_attachment_metadata_only(self, mock_document_attachments_api):
        """Test updating document attachment metadata only"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_document_attachments_api._session.patch.return_value = mock_response
        
        # Prepare data
        attachment_data = {
            "data": {
                "type": "document_attachments",
                "id": "MyProject/MySpace/MyDoc/MyAttachment",
                "attributes": {
                    "title": "Updated Title"
                }
            }
        }
        
        # Execute
        response = mock_document_attachments_api.patch_document_attachment(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="MyAttachment",
            attachment_data=attachment_data
        )
        
        # Verify
        assert response.status_code == 204
        mock_document_attachments_api._session.patch.assert_called_once()
        
        # Verify call arguments
        call_args = mock_document_attachments_api._session.patch.call_args
        # Check that data contains 'resource' with JSON
        data_arg = call_args[1]['data']
        assert 'resource' in data_arg
        # Verify JSON content
        resource_json = json.loads(data_arg['resource'])
        assert resource_json == attachment_data
    
    def test_patch_document_attachment_with_file(self, mock_document_attachments_api):
        """Test updating document attachment with new file"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_document_attachments_api._session.patch.return_value = mock_response
        
        # Prepare data
        attachment_data = {
            "data": {
                "type": "document_attachments",
                "id": "MyProject/MySpace/MyDoc/MyAttachment",
                "attributes": {
                    "title": "Updated Title"
                }
            }
        }
        
        # Mock file
        mock_file = Mock()
        mock_file.read.return_value = b'PDF content'
        file_tuple = ('document.pdf', mock_file, 'application/pdf')
        
        # Execute
        response = mock_document_attachments_api.patch_document_attachment(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="MyAttachment",
            attachment_data=attachment_data,
            file_content=file_tuple
        )
        
        # Verify
        assert response.status_code == 204
        mock_document_attachments_api._session.patch.assert_called_once()
        
        # Verify call arguments
        call_args = mock_document_attachments_api._session.patch.call_args
        # Check that files parameter is present
        files_arg = call_args[1]['files']
        assert files_arg is not None
        assert 'file' in files_arg
        assert files_arg['file'] == file_tuple
    
    def test_patch_document_attachment_url_construction(self, mock_document_attachments_api):
        """Test URL construction for patch_document_attachment"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_document_attachments_api._session.patch.return_value = mock_response
        
        # Prepare minimal data
        attachment_data = {
            "data": {
                "type": "document_attachments",
                "id": "TestProject/TestSpace/TestDoc/TestAttachment",
                "attributes": {"title": "Test"}
            }
        }
        
        # Execute
        mock_document_attachments_api.patch_document_attachment(
            project_id="TestProject",
            space_id="TestSpace",
            document_name="TestDocument",
            attachment_id="TestAttachment",
            attachment_data=attachment_data
        )
        
        # Verify URL
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/TestProject/spaces/TestSpace/documents/TestDocument/attachments/TestAttachment"
        call_args = mock_document_attachments_api._session.patch.call_args
        assert call_args[0][0] == expected_url
    
    def test_patch_document_attachment_multipart_format(self, mock_document_attachments_api):
        """Test that data is sent as multipart/form-data with 'resource' field"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_document_attachments_api._session.patch.return_value = mock_response
        
        # Prepare data
        attachment_data = {
            "data": {
                "type": "document_attachments",
                "id": "MyProject/MySpace/MyDoc/MyAttachment",
                "attributes": {
                    "title": "Test Title",
                    "fileName": "test.pdf"
                }
            }
        }
        
        # Execute
        response = mock_document_attachments_api.patch_document_attachment(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="MyAttachment",
            attachment_data=attachment_data
        )
        
        # Verify
        call_args = mock_document_attachments_api._session.patch.call_args
        data_arg = call_args[1]['data']
        
        # Verify that 'resource' key exists and contains JSON string
        assert 'resource' in data_arg
        assert isinstance(data_arg['resource'], str)
        
        # Verify JSON can be parsed back
        parsed_data = json.loads(data_arg['resource'])
        assert parsed_data == attachment_data
    
    def test_patch_document_attachment_update_title(self, mock_document_attachments_api):
        """Test updating attachment title"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_document_attachments_api._session.patch.return_value = mock_response
        
        # Prepare data
        attachment_data = {
            "data": {
                "type": "document_attachments",
                "id": "MyProject/MySpace/MyDoc/Att1",
                "attributes": {
                    "title": "New Fancy Title"
                }
            }
        }
        
        # Execute
        response = mock_document_attachments_api.patch_document_attachment(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="Att1",
            attachment_data=attachment_data
        )
        
        # Verify
        assert response.status_code == 204
    
    def test_patch_document_attachment_unauthorized(self, mock_document_attachments_api):
        """Test updating attachment without proper authorization"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "User does not have permission to update attachment"
            }]
        }
        mock_document_attachments_api._session.patch.return_value = mock_response
        
        # Prepare data
        attachment_data = {
            "data": {
                "type": "document_attachments",
                "id": "MyProject/MySpace/MyDoc/Att1",
                "attributes": {"title": "Test"}
            }
        }
        
        # Execute
        response = mock_document_attachments_api.patch_document_attachment(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="Att1",
            attachment_data=attachment_data
        )
        
        # Verify
        assert response.status_code == 403
    
    def test_patch_document_attachment_not_found(self, mock_document_attachments_api):
        """Test updating non-existent attachment"""
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
        mock_document_attachments_api._session.patch.return_value = mock_response
        
        # Prepare data
        attachment_data = {
            "data": {
                "type": "document_attachments",
                "id": "MyProject/MySpace/MyDoc/NonExistent",
                "attributes": {"title": "Test"}
            }
        }
        
        # Execute
        response = mock_document_attachments_api.patch_document_attachment(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="NonExistent",
            attachment_data=attachment_data
        )
        
        # Verify
        assert response.status_code == 404
    
    def test_patch_document_attachment_files_none_when_no_file(self, mock_document_attachments_api):
        """Test that files parameter is None when no file is provided"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_document_attachments_api._session.patch.return_value = mock_response
        
        # Prepare data
        attachment_data = {
            "data": {
                "type": "document_attachments",
                "id": "MyProject/MySpace/MyDoc/Att1",
                "attributes": {"title": "Test"}
            }
        }
        
        # Execute without file_content
        response = mock_document_attachments_api.patch_document_attachment(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachment_id="Att1",
            attachment_data=attachment_data
        )
        
        # Verify
        call_args = mock_document_attachments_api._session.patch.call_args
        files_arg = call_args[1]['files']
        assert files_arg is None
