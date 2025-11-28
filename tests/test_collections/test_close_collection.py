"""
Tests for post_close_collection method.
"""
import pytest


class TestCloseCollection:
    """Tests for post_close_collection method"""
    
    def test_post_close_collection(self, mock_collections_api):
        """Test closing a collection"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_collections_api._session.post.return_value = mock_response
        
        # Execute
        response = mock_collections_api.post_close_collection(
            project_id='MyProjectId',
            collection_id='MyCollectionId'
        )
        
        # Verify
        assert response.status_code == 200
        mock_collections_api._session.post.assert_called_once()
        call_args = mock_collections_api._session.post.call_args
        assert 'actions/close' in call_args[0][0]
    
    def test_post_close_collection_url_construction(self, mock_collections_api):
        """Test URL construction for post_close_collection"""
        from unittest.mock import Mock
        
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_collections_api._session.post.return_value = mock_response
        
        # Execute
        mock_collections_api.post_close_collection(
            project_id='MyProjectId',
            collection_id='MyCollectionId'
        )
        
        # Verify URL contains action
        call_args = mock_collections_api._session.post.call_args
        url = call_args[0][0]
        assert 'MyProjectId' in url
        assert 'MyCollectionId' in url
        assert 'actions/close' in url
