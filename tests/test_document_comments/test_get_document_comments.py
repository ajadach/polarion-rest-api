"""
Unit tests for DocumentComments.get_document_comments method.
"""
import pytest
from unittest.mock import Mock


class TestGetDocumentComments:
    """Test cases for get_document_comments method."""
    
    def test_get_document_comments_basic(self, mock_document_comments_api):
        """Test basic get_document_comments call without optional parameters."""
        
        mock_document_comments_api.get_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ'
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        assert call_args[0][0] == 'https://test.polarion.com/polarion/rest/v1/projects/devel/spaces/_default/documents/REQ/comments'
        
        # Verify default fields are applied
        params = call_args[1]['params']
        assert 'fields[document_comments]' in params
        assert params['fields[document_comments]'] == '@all'
        assert 'page[size]' not in params
        assert 'page[number]' not in params
        assert 'include' not in params
        assert 'revision' not in params
    
    def test_get_document_comments_with_pagination(self, mock_document_comments_api):
        """Test get_document_comments with pagination parameters."""
        
        mock_document_comments_api.get_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            page_size=50,
            page_number=2
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        params = call_args[1]['params']
        
        assert params['page[size]'] == 50
        assert params['page[number]'] == 2
    
    def test_get_document_comments_with_fields(self, mock_document_comments_api):
        """Test get_document_comments with custom fields parameter."""
        
        custom_fields = {
            'document_comments': 'author,created,id,resolved,text',
            'users': 'id,name'
        }
        
        mock_document_comments_api.get_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            fields=custom_fields
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        params = call_args[1]['params']
        
        # Custom fields should override default
        assert params['fields[document_comments]'] == 'author,created,id,resolved,text'
        assert params['fields[users]'] == 'id,name'
        # Other default fields should remain
        assert params['fields[collections]'] == '@all'
    
    def test_get_document_comments_with_include(self, mock_document_comments_api):
        """Test get_document_comments with include parameter."""
        
        mock_document_comments_api.get_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            include='author'
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        params = call_args[1]['params']
        
        assert params['include'] == 'author'
    
    def test_get_document_comments_with_revision(self, mock_document_comments_api):
        """Test get_document_comments with revision parameter."""
        
        mock_document_comments_api.get_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            revision='rev123'
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        params = call_args[1]['params']
        
        assert params['revision'] == 'rev123'
    
    def test_get_document_comments_with_all_parameters(self, mock_document_comments_api):
        """Test get_document_comments with all optional parameters."""
        
        custom_fields = {
            'document_comments': 'author,id,text',
            'users': 'id,name,email'
        }
        
        mock_document_comments_api.get_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            page_size=25,
            page_number=3,
            fields=custom_fields,
            include='author',
            revision='rev456'
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        
        # Verify URL
        assert call_args[0][0] == 'https://test.polarion.com/polarion/rest/v1/projects/devel/spaces/_default/documents/REQ/comments'
        
        # Verify parameters
        params = call_args[1]['params']
        assert params['page[size]'] == 25
        assert params['page[number]'] == 3
        assert params['fields[document_comments]'] == 'author,id,text'
        assert params['fields[users]'] == 'id,name,email'
        assert params['fields[collections]'] == '@all'  # Default field remains
        assert params['include'] == 'author'
        assert params['revision'] == 'rev456'
    
    def test_get_document_comments_response_handling(self, mock_document_comments_api):
        """Test that get_document_comments returns the response object."""
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [
                {
                    'type': 'document_comments',
                    'id': 'comment1',
                    'attributes': {'text': 'First comment'}
                },
                {
                    'type': 'document_comments',
                    'id': 'comment2',
                    'attributes': {'text': 'Second comment'}
                }
            ]
        }
        mock_document_comments_api._session.get.return_value = mock_response
        
        response = mock_document_comments_api.get_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ'
        )
        
        assert response == mock_response
        assert response.status_code == 200
        assert len(response.json()['data']) == 2
    
    def test_get_document_comments_pagination_edge_cases(self, mock_document_comments_api):
        """Test pagination with edge case values."""
        
        # Test with page_number=1 (first page)
        mock_document_comments_api.get_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            page_size=100,
            page_number=1
        )
        
        call_args = mock_document_comments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 100
        assert params['page[number]'] == 1
    
    def test_get_document_comments_only_page_size(self, mock_document_comments_api):
        """Test get_document_comments with only page_size parameter."""
        
        mock_document_comments_api.get_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            page_size=20
        )
        
        call_args = mock_document_comments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 20
        assert 'page[number]' not in params
    
    def test_get_document_comments_only_page_number(self, mock_document_comments_api):
        """Test get_document_comments with only page_number parameter."""
        
        mock_document_comments_api.get_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            page_number=5
        )
        
        call_args = mock_document_comments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[number]'] == 5
        assert 'page[size]' not in params
