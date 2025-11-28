"""
Unit tests for DocumentComments.get_document_comment method.
"""
import pytest
from unittest.mock import Mock


class TestGetDocumentComment:
    """Test cases for get_document_comment method."""
    
    def test_get_document_comment_basic(self, mock_document_comments_api):
        """Test basic get_document_comment call without optional parameters."""
        
        mock_document_comments_api.get_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='id123'
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        assert call_args[0][0] == 'https://test.polarion.com/polarion/rest/v1/projects/devel/spaces/_default/documents/REQ/comments/id123'
        
        # Verify default fields are applied
        params = call_args[1]['params']
        assert 'fields[document_comments]' in params
        assert params['fields[document_comments]'] == '@all'
        assert 'include' not in params
        assert 'revision' not in params
    
    def test_get_document_comment_with_fields(self, mock_document_comments_api):
        """Test get_document_comment with custom fields parameter."""
        
        custom_fields = {
            'document_comments': 'author,id,resolved,text'
        }
        
        mock_document_comments_api.get_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='id123',
            fields=custom_fields
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        params = call_args[1]['params']
        
        # Custom fields should override default
        assert params['fields[document_comments]'] == 'author,id,resolved,text'
        # Other default fields should remain
        assert params['fields[collections]'] == '@all'
        assert params['fields[documents]'] == '@all'
    
    def test_get_document_comment_with_include(self, mock_document_comments_api):
        """Test get_document_comment with include parameter."""
        
        mock_document_comments_api.get_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='id123',
            include='author'
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        params = call_args[1]['params']
        
        assert params['include'] == 'author'
    
    def test_get_document_comment_with_revision(self, mock_document_comments_api):
        """Test get_document_comment with revision parameter."""
        
        mock_document_comments_api.get_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='id123',
            revision='rev456'
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        params = call_args[1]['params']
        
        assert params['revision'] == 'rev456'
    
    def test_get_document_comment_with_all_parameters(self, mock_document_comments_api):
        """Test get_document_comment with all optional parameters."""
        
        custom_fields = {
            'document_comments': 'author,id,resolved,text',
            'users': 'id,name,email'
        }
        
        mock_document_comments_api.get_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='id123',
            fields=custom_fields,
            include='author',
            revision='rev789'
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        
        # Verify URL
        assert call_args[0][0] == 'https://test.polarion.com/polarion/rest/v1/projects/devel/spaces/_default/documents/REQ/comments/id123'
        
        # Verify parameters
        params = call_args[1]['params']
        assert params['fields[document_comments]'] == 'author,id,resolved,text'
        assert params['fields[users]'] == 'id,name,email'
        assert params['fields[collections]'] == '@all'  # Default field remains
        assert params['include'] == 'author'
        assert params['revision'] == 'rev789'
    
    def test_get_document_comment_response_handling(self, mock_document_comments_api):
        """Test that get_document_comment returns the response object."""
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'type': 'document_comments',
                'id': 'id123',
                'attributes': {
                    'text': 'Test comment',
                    'resolved': False
                }
            }
        }
        mock_document_comments_api._session.get.return_value = mock_response
        
        response = mock_document_comments_api.get_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='id123'
        )
        
        assert response == mock_response
        assert response.status_code == 200
        assert response.json()['data']['id'] == 'id123'
    
    def test_get_document_comment_with_special_characters(self, mock_document_comments_api):
        """Test get_document_comment with special characters in identifiers."""
        
        mock_document_comments_api.get_document_comment(
            project_id='my-project',
            space_id='space_123',
            document_name='DOC-2024',
            comment_id='comment_abc_123'
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        assert call_args[0][0] == 'https://test.polarion.com/polarion/rest/v1/projects/my-project/spaces/space_123/documents/DOC-2024/comments/comment_abc_123'
    
    def test_get_document_comment_fields_format_conversion(self, mock_document_comments_api):
        """Test that fields with or without fields[] wrapper are handled correctly."""
        
        # Test with fields[] wrapper already present
        custom_fields = {
            'fields[document_comments]': 'author,id'
        }
        
        mock_document_comments_api.get_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='id123',
            fields=custom_fields
        )
        
        mock_document_comments_api._session.get.assert_called_once()
        call_args = mock_document_comments_api._session.get.call_args
        params = call_args[1]['params']
        
        # Should handle both formats
        assert params['fields[document_comments]'] == 'author,id'

