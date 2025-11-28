"""
Unit tests for post_externally_linked_work_items method.
Tests the creation of externally linked work items.
"""
import pytest
from unittest.mock import Mock
import requests


class TestPostExternallyLinkedWorkItems:
    """Test suite for post_externally_linked_work_items method."""
    
    @pytest.fixture
    def request_body_single(self):
        """Fixture for single externally linked work item request body."""
        return {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "attributes": {
                        "role": "relates_to",
                        "workItemURI": "string"
                    }
                }
            ]
        }
    
    @pytest.fixture
    def request_body_multiple(self):
        """Fixture for multiple externally linked work items request body."""
        return {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "attributes": {
                        "role": "parent",
                        "workItemURI": "https://external-system.com/items/123"
                    }
                },
                {
                    "type": "externallylinkedworkitems",
                    "attributes": {
                        "role": "child",
                        "workItemURI": "https://external-system.com/items/456"
                    }
                },
                {
                    "type": "externallylinkedworkitems",
                    "attributes": {
                        "role": "relates_to",
                        "workItemURI": "https://external-system.com/items/789"
                    }
                }
            ]
        }
    
    @pytest.fixture
    def mock_response_201(self):
        """Fixture for mock 201 response data."""
        return {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/hostname/MyProjectId/MyLinkedWorkItemId",
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/externallylinkedworkitems/parent/hostname/MyProjectId/MyLinkedWorkItemId?revision=1234"
                    }
                }
            ]
        }
    
    @pytest.fixture
    def mock_response_401(self):
        """Fixture for mock 401 response data."""
        return {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "No access token"
                }
            ]
        }
    
    def test_post_externally_linked_work_items_single(self, mock_externally_linked_work_items_api, request_body_single, mock_response_201):
        """Test creating a single externally linked work item."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = mock_response_201
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            external_links_data=request_body_single
        )
        
        mock_externally_linked_work_items_api._post.assert_called_once()
        call_args = mock_externally_linked_work_items_api._post.call_args
        
        assert call_args[0][0] == 'projects/MyProjectId/workitems/MyWorkItemId/externallylinkedworkitems'
        assert call_args[1]['json'] == request_body_single
        assert response.status_code == 201
        assert response.json() == mock_response_201
    
    def test_post_externally_linked_work_items_multiple(self, mock_externally_linked_work_items_api, request_body_multiple):
        """Test creating multiple externally linked work items."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/hostname/ProjectA/Item123",
                    "links": {"self": "..."}
                },
                {
                    "type": "externallylinkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/child/hostname/ProjectB/Item456",
                    "links": {"self": "..."}
                },
                {
                    "type": "externallylinkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/relates_to/hostname/ProjectC/Item789",
                    "links": {"self": "..."}
                }
            ]
        }
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            external_links_data=request_body_multiple
        )
        
        mock_externally_linked_work_items_api._post.assert_called_once()
        call_args = mock_externally_linked_work_items_api._post.call_args
        
        assert call_args[1]['json'] == request_body_multiple
        assert response.status_code == 201
        assert len(response.json()['data']) == 3
    
    def test_post_externally_linked_work_items_with_parent_role(self, mock_externally_linked_work_items_api, mock_response_201):
        """Test creating externally linked work item with parent role."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = mock_response_201
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        request_body = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "attributes": {
                        "role": "parent",
                        "workItemURI": "https://external.com/parent/123"
                    }
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='TestProject',
            work_item_id='WI-001',
            external_links_data=request_body
        )
        
        call_args = mock_externally_linked_work_items_api._post.call_args
        assert call_args[1]['json']['data'][0]['attributes']['role'] == 'parent'
        assert response.status_code == 201
    
    def test_post_externally_linked_work_items_with_child_role(self, mock_externally_linked_work_items_api, mock_response_201):
        """Test creating externally linked work item with child role."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = mock_response_201
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        request_body = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "attributes": {
                        "role": "child",
                        "workItemURI": "https://external.com/child/456"
                    }
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='TestProject',
            work_item_id='WI-001',
            external_links_data=request_body
        )
        
        call_args = mock_externally_linked_work_items_api._post.call_args
        assert call_args[1]['json']['data'][0]['attributes']['role'] == 'child'
        assert response.status_code == 201
    
    def test_post_externally_linked_work_items_with_duplicates_role(self, mock_externally_linked_work_items_api, mock_response_201):
        """Test creating externally linked work item with duplicates role."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = mock_response_201
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        request_body = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "attributes": {
                        "role": "duplicates",
                        "workItemURI": "https://external.com/dup/789"
                    }
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='TestProject',
            work_item_id='WI-001',
            external_links_data=request_body
        )
        
        call_args = mock_externally_linked_work_items_api._post.call_args
        assert call_args[1]['json']['data'][0]['attributes']['role'] == 'duplicates'
        assert response.status_code == 201
    
    def test_post_externally_linked_work_items_with_blocks_role(self, mock_externally_linked_work_items_api, mock_response_201):
        """Test creating externally linked work item with blocks role."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = mock_response_201
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        request_body = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "attributes": {
                        "role": "blocks",
                        "workItemURI": "https://external.com/blocked/321"
                    }
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='TestProject',
            work_item_id='WI-001',
            external_links_data=request_body
        )
        
        call_args = mock_externally_linked_work_items_api._post.call_args
        assert call_args[1]['json']['data'][0]['attributes']['role'] == 'blocks'
        assert response.status_code == 201
    
    def test_post_externally_linked_work_items_with_depends_on_role(self, mock_externally_linked_work_items_api, mock_response_201):
        """Test creating externally linked work item with depends_on role."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = mock_response_201
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        request_body = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "attributes": {
                        "role": "depends_on",
                        "workItemURI": "https://external.com/dependency/654"
                    }
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='TestProject',
            work_item_id='WI-001',
            external_links_data=request_body
        )
        
        call_args = mock_externally_linked_work_items_api._post.call_args
        assert call_args[1]['json']['data'][0]['attributes']['role'] == 'depends_on'
        assert response.status_code == 201
    
    def test_post_externally_linked_work_items_unauthorized(self, mock_externally_linked_work_items_api, request_body_single, mock_response_401):
        """Test creation with unauthorized access."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 401
        mock_resp.json.return_value = mock_response_401
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            external_links_data=request_body_single
        )
        
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
    
    def test_post_externally_linked_work_items_bad_request(self, mock_externally_linked_work_items_api):
        """Test creation with invalid request body."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 400
        mock_resp.json.return_value = {
            "errors": [
                {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Invalid request body structure"
                }
            ]
        }
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        invalid_body = {
            "data": [
                {
                    "type": "wrong_type",
                    "attributes": {}
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            external_links_data=invalid_body
        )
        
        assert response.status_code == 400
        assert 'errors' in response.json()
    
    def test_post_externally_linked_work_items_not_found(self, mock_externally_linked_work_items_api, request_body_single):
        """Test creation when work item is not found."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 404
        mock_resp.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Work item not found"
                }
            ]
        }
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='NonExistent',
            work_item_id='WI-999',
            external_links_data=request_body_single
        )
        
        assert response.status_code == 404
        assert 'errors' in response.json()
    
    def test_post_externally_linked_work_items_verify_response_structure(self, mock_externally_linked_work_items_api, request_body_single, mock_response_201):
        """Test that response structure matches expected format."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = mock_response_201
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            external_links_data=request_body_single
        )
        
        response_data = response.json()
        assert 'data' in response_data
        assert isinstance(response_data['data'], list)
        
        if len(response_data['data']) > 0:
            item = response_data['data'][0]
            assert item['type'] == 'externallylinkedworkitems'
            assert 'id' in item
            assert 'links' in item
            assert 'self' in item['links']
    
    def test_post_externally_linked_work_items_different_project(self, mock_externally_linked_work_items_api, request_body_single, mock_response_201):
        """Test creation for different project and work item IDs."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = mock_response_201
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='DifferentProject',
            work_item_id='WI-9999',
            external_links_data=request_body_single
        )
        
        mock_externally_linked_work_items_api._post.assert_called_once()
        call_args = mock_externally_linked_work_items_api._post.call_args
        
        assert call_args[0][0] == 'projects/DifferentProject/workitems/WI-9999/externallylinkedworkitems'
        assert response.status_code == 201
    
    def test_post_externally_linked_work_items_with_complex_uri(self, mock_externally_linked_work_items_api, mock_response_201):
        """Test creation with complex work item URI."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = mock_response_201
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        request_body = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "attributes": {
                        "role": "relates_to",
                        "workItemURI": "https://external-system.example.com:8443/project/workitems/123?version=2&revision=5"
                    }
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            external_links_data=request_body
        )
        
        call_args = mock_externally_linked_work_items_api._post.call_args
        uri = call_args[1]['json']['data'][0]['attributes']['workItemURI']
        assert 'https://external-system.example.com:8443' in uri
        assert '?version=2&revision=5' in uri
        assert response.status_code == 201
    
    def test_post_externally_linked_work_items_verify_endpoint(self, mock_externally_linked_work_items_api, request_body_single):
        """Test that correct endpoint is called."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"data": []}
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='TestProj',
            work_item_id='WI-123',
            external_links_data=request_body_single
        )
        
        mock_externally_linked_work_items_api._post.assert_called_once_with(
            'projects/TestProj/workitems/WI-123/externallylinkedworkitems',
            json=request_body_single
        )
    
    def test_post_externally_linked_work_items_verify_json_parameter(self, mock_externally_linked_work_items_api, request_body_multiple):
        """Test that json parameter is correctly passed."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"data": []}
        mock_externally_linked_work_items_api._post = Mock(return_value=mock_resp)
        
        mock_externally_linked_work_items_api.post_externally_linked_work_items(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            external_links_data=request_body_multiple
        )
        
        call_args = mock_externally_linked_work_items_api._post.call_args
        assert 'json' in call_args[1]
        assert call_args[1]['json'] == request_body_multiple
        assert len(call_args[1]['json']['data']) == 3
