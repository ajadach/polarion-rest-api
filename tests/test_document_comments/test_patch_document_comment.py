"""
Unit tests for DocumentComments.patch_document_comment method.
"""
import pytest
from unittest.mock import Mock


class TestPatchDocumentComment:
    """Test cases for patch_document_comment method."""
    
    def test_patch_document_comment_basic(self, mock_document_comments_api):
        """Test basic patch_document_comment call."""
        
        comment_data = {
            'data': {
                'type': 'document_comments',
                'id': 'comment123',
                'attributes': {
                    'text': 'Updated comment text'
                }
            }
        }
        
        mock_document_comments_api.patch_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='comment123',
            comment_data=comment_data
        )
        
        mock_document_comments_api._session.patch.assert_called_once()
        call_args = mock_document_comments_api._session.patch.call_args
        
        # Verify URL
        assert call_args[0][0] == 'https://test.polarion.com/polarion/rest/v1/projects/devel/spaces/_default/documents/REQ/comments/comment123'
        
        # Verify JSON data
        assert call_args[1]['json'] == comment_data
    
    def test_patch_document_comment_resolve_status(self, mock_document_comments_api):
        """Test patching comment to change resolved status."""
        
        comment_data = {
            'data': {
                'type': 'document_comments',
                'id': 'comment456',
                'attributes': {
                    'resolved': True
                }
            }
        }
        
        mock_document_comments_api.patch_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='DOC',
            comment_id='comment456',
            comment_data=comment_data
        )
        
        mock_document_comments_api._session.patch.assert_called_once()
        call_args = mock_document_comments_api._session.patch.call_args
        
        # Verify the data
        json_data = call_args[1]['json']
        assert json_data['data']['attributes']['resolved'] is True
    
    def test_patch_document_comment_text_and_resolved(self, mock_document_comments_api):
        """Test patching both text and resolved status."""
        
        comment_data = {
            'data': {
                'type': 'document_comments',
                'id': 'comment789',
                'attributes': {
                    'text': 'Updated and resolved',
                    'resolved': True
                }
            }
        }
        
        mock_document_comments_api.patch_document_comment(
            project_id='my-project',
            space_id='space_1',
            document_name='SPEC-2024',
            comment_id='comment789',
            comment_data=comment_data
        )
        
        mock_document_comments_api._session.patch.assert_called_once()
        call_args = mock_document_comments_api._session.patch.call_args
        
        # Verify URL with special characters
        assert 'my-project' in call_args[0][0]
        assert 'space_1' in call_args[0][0]
        assert 'SPEC-2024' in call_args[0][0]
        
        # Verify both attributes are included
        json_data = call_args[1]['json']
        assert json_data['data']['attributes']['text'] == 'Updated and resolved'
        assert json_data['data']['attributes']['resolved'] is True
    
    def test_patch_document_comment_response_handling(self, mock_document_comments_api):
        """Test that patch_document_comment returns the response object."""
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_document_comments_api._session.patch.return_value = mock_response
        
        comment_data = {
            'data': {
                'type': 'document_comments',
                'id': 'comment_abc',
                'attributes': {
                    'text': 'Test'
                }
            }
        }
        
        response = mock_document_comments_api.patch_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='comment_abc',
            comment_data=comment_data
        )
        
        assert response == mock_response
        assert response.status_code == 204
    
    def test_patch_document_comment_minimal_data(self, mock_document_comments_api):
        """Test patching with minimal required data structure."""
        
        comment_data = {
            'data': {
                'type': 'document_comments',
                'id': 'minimal'
            }
        }
        
        mock_document_comments_api.patch_document_comment(
            project_id='proj1',
            space_id='_default',
            document_name='DOC1',
            comment_id='minimal',
            comment_data=comment_data
        )
        
        mock_document_comments_api._session.patch.assert_called_once()
        call_args = mock_document_comments_api._session.patch.call_args
        json_data = call_args[1]['json']
        
        assert json_data['data']['type'] == 'document_comments'
        assert json_data['data']['id'] == 'minimal'
    
    def test_patch_document_comment_with_relationships(self, mock_document_comments_api):
        """Test patching comment with relationships data."""
        
        comment_data = {
            'data': {
                'type': 'document_comments',
                'id': 'comment_rel',
                'attributes': {
                    'text': 'Comment with relationships'
                },
                'relationships': {
                    'author': {
                        'data': {
                            'type': 'users',
                            'id': 'user123'
                        }
                    }
                }
            }
        }
        
        mock_document_comments_api.patch_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='comment_rel',
            comment_data=comment_data
        )
        
        mock_document_comments_api._session.patch.assert_called_once()
        call_args = mock_document_comments_api._session.patch.call_args
        json_data = call_args[1]['json']
        
        assert 'relationships' in json_data['data']
        assert json_data['data']['relationships']['author']['data']['id'] == 'user123'
    
    def test_patch_document_comment_empty_attributes(self, mock_document_comments_api):
        """Test patching with empty attributes dictionary."""
        
        comment_data = {
            'data': {
                'type': 'document_comments',
                'id': 'empty_attrs',
                'attributes': {}
            }
        }
        
        mock_document_comments_api.patch_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='empty_attrs',
            comment_data=comment_data
        )
        
        mock_document_comments_api._session.patch.assert_called_once()
        call_args = mock_document_comments_api._session.patch.call_args
        json_data = call_args[1]['json']
        
        assert json_data['data']['attributes'] == {}
    
    def test_patch_document_comment_content_type_header(self, mock_document_comments_api):
        """Test that Content-Type header is set for PATCH request."""
        
        comment_data = {
            'data': {
                'type': 'document_comments',
                'id': 'test_header'
            }
        }
        
        mock_document_comments_api.patch_document_comment(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comment_id='test_header',
            comment_data=comment_data
        )
        
        # Verify that patch was called with json parameter
        # which should set Content-Type automatically
        call_args = mock_document_comments_api._session.patch.call_args
        assert 'json' in call_args[1]
