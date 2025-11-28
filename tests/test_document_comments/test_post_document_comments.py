"""
Unit tests for DocumentComments.post_document_comments method.
"""
import pytest
from unittest.mock import Mock


class TestPostDocumentComments:
    """Test cases for post_document_comments method."""
    
    def test_post_document_comments_single(self, mock_document_comments_api):
        """Test creating a single document comment."""
        
        comments_data = {
            'data': [
                {
                    'type': 'document_comments',
                    'attributes': {
                        'text': 'This is a new comment'
                    }
                }
            ]
        }
        
        mock_document_comments_api.post_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comments_data=comments_data
        )
        
        mock_document_comments_api._session.post.assert_called_once()
        call_args = mock_document_comments_api._session.post.call_args
        
        # Verify URL
        assert call_args[0][0] == 'https://test.polarion.com/polarion/rest/v1/projects/devel/spaces/_default/documents/REQ/comments'
        
        # Verify JSON data
        assert call_args[1]['json'] == comments_data
    
    def test_post_document_comments_multiple(self, mock_document_comments_api):
        """Test creating multiple document comments."""
        
        comments_data = {
            'data': [
                {
                    'type': 'document_comments',
                    'attributes': {
                        'text': 'First comment'
                    }
                },
                {
                    'type': 'document_comments',
                    'attributes': {
                        'text': 'Second comment'
                    }
                },
                {
                    'type': 'document_comments',
                    'attributes': {
                        'text': 'Third comment'
                    }
                }
            ]
        }
        
        mock_document_comments_api.post_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comments_data=comments_data
        )
        
        mock_document_comments_api._session.post.assert_called_once()
        call_args = mock_document_comments_api._session.post.call_args
        json_data = call_args[1]['json']
        
        # Verify multiple comments in data array
        assert len(json_data['data']) == 3
        assert json_data['data'][0]['attributes']['text'] == 'First comment'
        assert json_data['data'][1]['attributes']['text'] == 'Second comment'
        assert json_data['data'][2]['attributes']['text'] == 'Third comment'
    
    def test_post_document_comments_with_parent(self, mock_document_comments_api):
        """Test creating a comment with parent reference."""
        
        comments_data = {
            'data': [
                {
                    'type': 'document_comments',
                    'attributes': {
                        'text': 'Reply to parent comment'
                    },
                    'relationships': {
                        'parent': {
                            'data': {
                                'type': 'document_comments',
                                'id': 'parent_comment_123'
                            }
                        }
                    }
                }
            ]
        }
        
        mock_document_comments_api.post_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comments_data=comments_data
        )
        
        mock_document_comments_api._session.post.assert_called_once()
        call_args = mock_document_comments_api._session.post.call_args
        json_data = call_args[1]['json']
        
        assert 'relationships' in json_data['data'][0]
        assert json_data['data'][0]['relationships']['parent']['data']['id'] == 'parent_comment_123'
    
    def test_post_document_comments_with_author(self, mock_document_comments_api):
        """Test creating a comment with author relationship."""
        
        comments_data = {
            'data': [
                {
                    'type': 'document_comments',
                    'attributes': {
                        'text': 'Comment by specific author'
                    },
                    'relationships': {
                        'author': {
                            'data': {
                                'type': 'users',
                                'id': 'user456'
                            }
                        }
                    }
                }
            ]
        }
        
        mock_document_comments_api.post_document_comments(
            project_id='my-project',
            space_id='space_1',
            document_name='DOC-2024',
            comments_data=comments_data
        )
        
        mock_document_comments_api._session.post.assert_called_once()
        call_args = mock_document_comments_api._session.post.call_args
        
        # Verify URL with special characters
        assert 'my-project' in call_args[0][0]
        assert 'space_1' in call_args[0][0]
        assert 'DOC-2024' in call_args[0][0]
        
        json_data = call_args[1]['json']
        assert json_data['data'][0]['relationships']['author']['data']['id'] == 'user456'
    
    def test_post_document_comments_response_handling(self, mock_document_comments_api):
        """Test that post_document_comments returns the response object."""
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'data': [
                {
                    'type': 'document_comments',
                    'id': 'new_comment_123',
                    'attributes': {
                        'text': 'Created comment'
                    }
                }
            ]
        }
        mock_document_comments_api._session.post.return_value = mock_response
        
        comments_data = {
            'data': [
                {
                    'type': 'document_comments',
                    'attributes': {
                        'text': 'Created comment'
                    }
                }
            ]
        }
        
        response = mock_document_comments_api.post_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comments_data=comments_data
        )
        
        assert response == mock_response
        assert response.status_code == 201
        assert response.json()['data'][0]['id'] == 'new_comment_123'
    
    def test_post_document_comments_resolved_status(self, mock_document_comments_api):
        """Test creating a comment with resolved status."""
        
        comments_data = {
            'data': [
                {
                    'type': 'document_comments',
                    'attributes': {
                        'text': 'Pre-resolved comment',
                        'resolved': True
                    }
                }
            ]
        }
        
        mock_document_comments_api.post_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comments_data=comments_data
        )
        
        mock_document_comments_api._session.post.assert_called_once()
        call_args = mock_document_comments_api._session.post.call_args
        json_data = call_args[1]['json']
        
        assert json_data['data'][0]['attributes']['resolved'] is True
    
    def test_post_document_comments_complex_structure(self, mock_document_comments_api):
        """Test creating comments with complex structure including multiple relationships."""
        
        comments_data = {
            'data': [
                {
                    'type': 'document_comments',
                    'attributes': {
                        'text': 'Complex comment with all features',
                        'resolved': False
                    },
                    'relationships': {
                        'author': {
                            'data': {
                                'type': 'users',
                                'id': 'user789'
                            }
                        },
                        'parent': {
                            'data': {
                                'type': 'document_comments',
                                'id': 'parent_abc'
                            }
                        }
                    }
                }
            ]
        }
        
        mock_document_comments_api.post_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comments_data=comments_data
        )
        
        mock_document_comments_api._session.post.assert_called_once()
        call_args = mock_document_comments_api._session.post.call_args
        json_data = call_args[1]['json']
        
        comment = json_data['data'][0]
        assert comment['attributes']['text'] == 'Complex comment with all features'
        assert comment['attributes']['resolved'] is False
        assert comment['relationships']['author']['data']['id'] == 'user789'
        assert comment['relationships']['parent']['data']['id'] == 'parent_abc'
    
    def test_post_document_comments_minimal_data(self, mock_document_comments_api):
        """Test creating a comment with minimal required data."""
        
        comments_data = {
            'data': [
                {
                    'type': 'document_comments',
                    'attributes': {
                        'text': 'Minimal comment'
                    }
                }
            ]
        }
        
        mock_document_comments_api.post_document_comments(
            project_id='proj1',
            space_id='_default',
            document_name='DOC1',
            comments_data=comments_data
        )
        
        mock_document_comments_api._session.post.assert_called_once()
        call_args = mock_document_comments_api._session.post.call_args
        json_data = call_args[1]['json']
        
        assert len(json_data['data']) == 1
        assert json_data['data'][0]['type'] == 'document_comments'
        assert json_data['data'][0]['attributes']['text'] == 'Minimal comment'
    
    def test_post_document_comments_content_type_header(self, mock_document_comments_api):
        """Test that Content-Type header is set for POST request."""
        
        comments_data = {
            'data': [
                {
                    'type': 'document_comments',
                    'attributes': {
                        'text': 'Test header'
                    }
                }
            ]
        }
        
        mock_document_comments_api.post_document_comments(
            project_id='devel',
            space_id='_default',
            document_name='REQ',
            comments_data=comments_data
        )
        
        # Verify that post was called with json parameter
        # which should set Content-Type automatically
        call_args = mock_document_comments_api._session.post.call_args
        assert 'json' in call_args[1]
