"""
Tests for get_document_attachments method from DocumentAttachments module.
"""
import pytest
from unittest.mock import Mock


class TestGetDocumentAttachments:
    """Tests for get_document_attachments method"""
    
    def test_get_document_attachments_basic(self, mock_document_attachments_api):
        """Test getting list of document attachments with basic parameters"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "document_attachments",
                    "id": "MyProject/MySpace/MyDoc/Attachment1",
                    "attributes": {
                        "title": "First Attachment",
                        "fileName": "file1.pdf"
                    }
                },
                {
                    "type": "document_attachments",
                    "id": "MyProject/MySpace/MyDoc/Attachment2",
                    "attributes": {
                        "title": "Second Attachment",
                        "fileName": "file2.png"
                    }
                }
            ]
        }
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument"
        )
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert len(data['data']) == 2
        mock_document_attachments_api._session.get.assert_called_once()
    
    def test_get_document_attachments_with_pagination(self, mock_document_attachments_api):
        """Test getting document attachments with pagination"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            page_size=50,
            page_number=2
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_document_attachments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 50
        assert params['page[number]'] == 2
    
    def test_get_document_attachments_with_fields(self, mock_document_attachments_api):
        """Test getting document attachments with custom fields"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        custom_fields = {
            'document_attachments': 'id,title,fileName'
        }
        response = mock_document_attachments_api.get_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            fields=custom_fields
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_document_attachments_api._session.get.call_args
        params = call_args[1]['params']
        assert 'fields[document_attachments]' in params
        assert params['fields[document_attachments]'] == 'id,title,fileName'
    
    def test_get_document_attachments_with_include(self, mock_document_attachments_api):
        """Test getting document attachments with include parameter"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            include="author,document"
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_document_attachments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'author,document'
    
    def test_get_document_attachments_with_revision(self, mock_document_attachments_api):
        """Test getting document attachments with revision parameter"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            revision="9999"
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_document_attachments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '9999'
    
    def test_get_document_attachments_with_all_params(self, mock_document_attachments_api):
        """Test getting document attachments with all parameters"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument",
            page_size=25,
            page_number=3,
            fields={'document_attachments': 'id,title'},
            include="author",
            revision="1234"
        )
        
        # Verify
        assert response.status_code == 200
        call_args = mock_document_attachments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 25
        assert params['page[number]'] == 3
        assert params['include'] == 'author'
        assert params['revision'] == '1234'
    
    def test_get_document_attachments_url_construction(self, mock_document_attachments_api):
        """Test URL construction for get_document_attachments"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        mock_document_attachments_api.get_document_attachments(
            project_id="TestProject",
            space_id="TestSpace",
            document_name="TestDocument"
        )
        
        # Verify URL
        expected_url = "https://test.polarion.com/polarion/rest/v1/projects/TestProject/spaces/TestSpace/documents/TestDocument/attachments"
        call_args = mock_document_attachments_api._session.get.call_args
        assert call_args[0][0] == expected_url
    
    def test_get_document_attachments_default_fields_applied(self, mock_document_attachments_api):
        """Test that default fields are applied"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="MyDocument"
        )
        
        # Verify that default fields are present
        call_args = mock_document_attachments_api._session.get.call_args
        params = call_args[1]['params']
        # Check for some default fields
        assert 'fields[collections]' in params
        assert params['fields[collections]'] == '@all'
        assert 'fields[document_attachments]' in params
        assert params['fields[document_attachments]'] == '@all'
    
    def test_get_document_attachments_empty_list(self, mock_document_attachments_api):
        """Test getting attachments when document has no attachments"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="EmptyDocument"
        )
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert len(data['data']) == 0
    
    def test_get_document_attachments_document_not_found(self, mock_document_attachments_api):
        """Test getting attachments for non-existent document"""
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
        mock_document_attachments_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_document_attachments_api.get_document_attachments(
            project_id="MyProject",
            space_id="MySpace",
            document_name="NonExistent"
        )
        
        # Verify
        assert response.status_code == 404
        errors = response.json()
        assert 'errors' in errors
