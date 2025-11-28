"""
Tests for post_document_attachments method from DocumentAttachments module.
"""
import pytest
import json
from unittest.mock import Mock


class TestPostDocumentAttachments:
    """Tests for post_document_attachments method"""
    
    def test_post_document_attachments_single_with_file(self, mock_document_attachments_api):
        """Test creating single document attachment with file"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "document_attachments",
                    "id": "MyProject/MySpace/MyDoc/NewAttachment",
                    "attributes": {
                        "title": "Report",
                        "fileName": "report.pdf"
                    }
                }
            ]
        }
        mock_document_attachments_api._session.post.return_value = mock_response
        
        # Prepare data
        attachments_data = {
            "data": [
                {
                    "type": "document_attachments",
                    "lid": "attachment1",
                    "attributes": {
                        "fileName": "report.pdf",
                        "title": "Monthly Report"
                    }
                }
            ]
        }
        
        # Mock file
        mock_file = Mock()
        mock_file.read.return_value = b'PDF content'
        file_tuple = ('report.pdf', mock_file, 'application/pdf')
        
        # Execute
        response = mock_document_attachments_api.post_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachments_data=attachments_data,
            files=[file_tuple]
        )
        
        # Verify
        assert response.status_code == 201
        data = response.json()
        assert 'data' in data
        assert len(data['data']) == 1
        mock_document_attachments_api._session.post.assert_called_once()
    
    def test_post_document_attachments_multiple_with_files(self, mock_document_attachments_api):
        """Test creating multiple document attachments with files"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "document_attachments",
                    "id": "MyProject/MySpace/MyDoc/Att1"
                },
                {
                    "type": "document_attachments",
                    "id": "MyProject/MySpace/MyDoc/Att2"
                }
            ]
        }
        mock_document_attachments_api._session.post.return_value = mock_response
        
        # Prepare data
        attachments_data = {
            "data": [
                {
                    "type": "document_attachments",
                    "lid": "attachment1",
                    "attributes": {
                        "fileName": "report.pdf",
                        "title": "Report"
                    }
                },
                {
                    "type": "document_attachments",
                    "lid": "attachment2",
                    "attributes": {
                        "fileName": "chart.png",
                        "title": "Chart"
                    }
                }
            ]
        }
        
        # Mock files
        files = [
            ('report.pdf', Mock(), 'application/pdf'),
            ('chart.png', Mock(), 'image/png')
        ]
        
        # Execute
        response = mock_document_attachments_api.post_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachments_data=attachments_data,
            files=files
        )
        
        # Verify
        assert response.status_code == 201
        data = response.json()
        assert len(data['data']) == 2
    
    def test_post_document_attachments_metadata_only(self, mock_document_attachments_api):
        """Test creating attachments with metadata only (no files)"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "document_attachments",
                    "id": "MyProject/MySpace/MyDoc/NewAtt"
                }
            ]
        }
        mock_document_attachments_api._session.post.return_value = mock_response
        
        # Prepare data
        attachments_data = {
            "data": [
                {
                    "type": "document_attachments",
                    "attributes": {
                        "fileName": "reference.txt",
                        "title": "External Reference"
                    }
                }
            ]
        }
        
        # Execute without files
        response = mock_document_attachments_api.post_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachments_data=attachments_data
        )
        
        # Verify
        assert response.status_code == 201
        
        # Verify that files parameter is None
        call_args = mock_document_attachments_api._session.post.call_args
        files_arg = call_args[1]['files']
        assert files_arg is None
    
    def test_post_document_attachments_url_construction(self, mock_document_attachments_api):
        """Test URL construction for post_document_attachments"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.post.return_value = mock_response
        
        # Prepare minimal data
        attachments_data = {
            "data": [
                {
                    "type": "document_attachments",
                    "attributes": {"title": "Test"}
                }
            ]
        }
        
        # Execute
        mock_document_attachments_api.post_document_attachments(
            project_id="TestProject",
            space_id="TestSpace",
            document_name="TestDocument",
            attachments_data=attachments_data
        )
        
        # Verify URL
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/TestProject/spaces/TestSpace/documents/TestDocument/attachments"
        call_args = mock_document_attachments_api._session.post.call_args
        assert call_args[0][0] == expected_url
    
    def test_post_document_attachments_multipart_format(self, mock_document_attachments_api):
        """Test that data is sent as multipart/form-data with 'resource' field"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.post.return_value = mock_response
        
        # Prepare data
        attachments_data = {
            "data": [
                {
                    "type": "document_attachments",
                    "attributes": {
                        "fileName": "test.pdf",
                        "title": "Test"
                    }
                }
            ]
        }
        
        # Execute
        response = mock_document_attachments_api.post_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachments_data=attachments_data
        )
        
        # Verify
        call_args = mock_document_attachments_api._session.post.call_args
        data_arg = call_args[1]['data']
        
        # Verify that 'resource' key exists and contains JSON string
        assert 'resource' in data_arg
        assert isinstance(data_arg['resource'], str)
        
        # Verify JSON can be parsed back
        parsed_data = json.loads(data_arg['resource'])
        assert parsed_data == attachments_data
    
    def test_post_document_attachments_files_format(self, mock_document_attachments_api):
        """Test that files are formatted correctly for multipart request"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.post.return_value = mock_response
        
        # Prepare data
        attachments_data = {
            "data": [
                {
                    "type": "document_attachments",
                    "attributes": {"title": "Test"}
                }
            ]
        }
        
        # Mock files
        file1 = ('file1.pdf', Mock(), 'application/pdf')
        file2 = ('file2.png', Mock(), 'image/png')
        files = [file1, file2]
        
        # Execute
        response = mock_document_attachments_api.post_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachments_data=attachments_data,
            files=files
        )
        
        # Verify
        call_args = mock_document_attachments_api._session.post.call_args
        files_arg = call_args[1]['files']
        
        # Verify files are formatted as list of tuples with 'files' key
        assert files_arg is not None
        assert isinstance(files_arg, list)
        assert len(files_arg) == 2
        assert files_arg[0][0] == 'files'
        assert files_arg[1][0] == 'files'
    
    def test_post_document_attachments_with_lid(self, mock_document_attachments_api):
        """Test creating attachments with local IDs (lid) for file matching"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.post.return_value = mock_response
        
        # Prepare data with lid
        attachments_data = {
            "data": [
                {
                    "type": "document_attachments",
                    "lid": "myLocalId123",
                    "attributes": {
                        "fileName": "important.pdf",
                        "title": "Important Document"
                    }
                }
            ]
        }
        
        # Execute
        response = mock_document_attachments_api.post_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachments_data=attachments_data,
            files=[('important.pdf', Mock(), 'application/pdf')]
        )
        
        # Verify lid is preserved in request data
        call_args = mock_document_attachments_api._session.post.call_args
        data_arg = call_args[1]['data']
        parsed_data = json.loads(data_arg['resource'])
        assert parsed_data['data'][0]['lid'] == 'myLocalId123'
    
    def test_post_document_attachments_empty_files_list(self, mock_document_attachments_api):
        """Test that empty files list results in None files parameter"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.post.return_value = mock_response
        
        # Prepare data
        attachments_data = {
            "data": [
                {
                    "type": "document_attachments",
                    "attributes": {"title": "Test"}
                }
            ]
        }
        
        # Execute with empty files list
        response = mock_document_attachments_api.post_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachments_data=attachments_data,
            files=[]
        )
        
        # Verify
        call_args = mock_document_attachments_api._session.post.call_args
        files_arg = call_args[1]['files']
        assert files_arg is None
    
    def test_post_document_attachments_unauthorized(self, mock_document_attachments_api):
        """Test creating attachment without proper authorization"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [{
                "status": "403",
                "title": "Forbidden"
            }]
        }
        mock_document_attachments_api._session.post.return_value = mock_response
        
        # Prepare data
        attachments_data = {
            "data": [
                {
                    "type": "document_attachments",
                    "attributes": {"title": "Test"}
                }
            ]
        }
        
        # Execute
        response = mock_document_attachments_api.post_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            attachments_data=attachments_data
        )
        
        # Verify
        assert response.status_code == 403
    
    def test_post_document_attachments_document_not_found(self, mock_document_attachments_api):
        """Test creating attachment for non-existent document"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Document not found"
            }]
        }
        mock_document_attachments_api._session.post.return_value = mock_response
        
        # Prepare data
        attachments_data = {
            "data": [
                {
                    "type": "document_attachments",
                    "attributes": {"title": "Test"}
                }
            ]
        }
        
        # Execute
        response = mock_document_attachments_api.post_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="NonExistent",
            attachments_data=attachments_data
        )
        
        # Verify
        assert response.status_code == 404
