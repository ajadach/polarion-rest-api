"""
Unit tests for get_externally_linked_work_item method.
Tests the retrieval of a specific externally linked work item.
"""
import pytest
from unittest.mock import Mock
import requests


class TestGetExternallyLinkedWorkItem:
    """Test suite for get_externally_linked_work_item method."""
    
    @pytest.fixture
    def mock_response(self):
        """Fixture for mock response data."""
        return {
            "data": {
                "type": "externallylinkedworkitems",
                "id": "MyProjectId/MyWorkItemId/parent/hostname/MyProjectId/MyLinkedWorkItemId",
                "revision": "1234",
                "attributes": {
                    "role": "relates_to",
                    "workItemURI": "string"
                },
                "meta": {
                    "errors": [
                        {
                            "status": "400",
                            "title": "Bad Request",
                            "detail": "Unexpected token, BEGIN_ARRAY expected, but was : BEGIN_OBJECT (at $.data)",
                            "source": {
                                "pointer": "$.data",
                                "parameter": "revision",
                                "resource": {
                                    "id": "MyProjectId/id",
                                    "type": "type"
                                }
                            }
                        }
                    ]
                },
                "links": {
                    "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/externallylinkedworkitems/parent/hostname/MyProjectId/MyLinkedWorkItemId?revision=1234"
                }
            },
            "included": [
                {}
            ],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/externallylinkedworkitems/parent/hostname/MyProjectId/MyLinkedWorkItemId?revision=1234"
            }
        }
    
    def test_get_externally_linked_work_item_basic(self, mock_externally_linked_work_items_api, mock_response):
        """Test basic retrieval of externally linked work item without optional parameters."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response
        mock_externally_linked_work_items_api._get = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.get_externally_linked_work_item(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            role_id='parent',
            hostname='hostname',
            target_project_id='MyProjectId',
            linked_work_item_id='MyLinkedWorkItemId'
        )
        
        mock_externally_linked_work_items_api._get.assert_called_once()
        call_args = mock_externally_linked_work_items_api._get.call_args
        
        assert call_args[0][0] == 'projects/MyProjectId/workitems/MyWorkItemId/externallylinkedworkitems/parent/hostname/MyProjectId/MyLinkedWorkItemId'
        assert response.status_code == 200
        assert response.json() == mock_response
    
    def test_get_externally_linked_work_item_with_fields(self, mock_externally_linked_work_items_api, mock_response):
        """Test retrieval with custom fields parameter."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response
        mock_externally_linked_work_items_api._get = Mock(return_value=mock_resp)
        
        custom_fields = {
            'workitems': 'id,title',
            'projects': 'id,name'
        }
        
        response = mock_externally_linked_work_items_api.get_externally_linked_work_item(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            role_id='parent',
            hostname='hostname',
            target_project_id='MyProjectId',
            linked_work_item_id='MyLinkedWorkItemId',
            fields=custom_fields
        )
        
        mock_externally_linked_work_items_api._get.assert_called_once()
        call_args = mock_externally_linked_work_items_api._get.call_args
        
        assert call_args[0][0] == 'projects/MyProjectId/workitems/MyWorkItemId/externallylinkedworkitems/parent/hostname/MyProjectId/MyLinkedWorkItemId'
        assert call_args[1]['params'] is not None
        assert 'fields[workitems]' in call_args[1]['params']
        assert call_args[1]['params']['fields[workitems]'] == 'id,title'
        assert response.status_code == 200
    
    def test_get_externally_linked_work_item_with_include(self, mock_externally_linked_work_items_api, mock_response):
        """Test retrieval with include parameter."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response
        mock_externally_linked_work_items_api._get = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.get_externally_linked_work_item(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            role_id='parent',
            hostname='hostname',
            target_project_id='MyProjectId',
            linked_work_item_id='MyLinkedWorkItemId',
            include='workitem'
        )
        
        mock_externally_linked_work_items_api._get.assert_called_once()
        call_args = mock_externally_linked_work_items_api._get.call_args
        
        assert call_args[1]['params']['include'] == 'workitem'
        assert response.status_code == 200
    
    def test_get_externally_linked_work_item_with_revision(self, mock_externally_linked_work_items_api, mock_response):
        """Test retrieval with revision parameter."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response
        mock_externally_linked_work_items_api._get = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.get_externally_linked_work_item(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            role_id='parent',
            hostname='hostname',
            target_project_id='MyProjectId',
            linked_work_item_id='MyLinkedWorkItemId',
            revision='1234'
        )
        
        mock_externally_linked_work_items_api._get.assert_called_once()
        call_args = mock_externally_linked_work_items_api._get.call_args
        
        assert call_args[1]['params']['revision'] == '1234'
        assert response.status_code == 200
    
    def test_get_externally_linked_work_item_with_all_parameters(self, mock_externally_linked_work_items_api, mock_response):
        """Test retrieval with all optional parameters."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response
        mock_externally_linked_work_items_api._get = Mock(return_value=mock_resp)
        
        custom_fields = {
            'workitems': 'id,title',
            'projects': 'id,name'
        }
        
        response = mock_externally_linked_work_items_api.get_externally_linked_work_item(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            role_id='parent',
            hostname='hostname',
            target_project_id='MyProjectId',
            linked_work_item_id='MyLinkedWorkItemId',
            fields=custom_fields,
            include='workitem',
            revision='1234'
        )
        
        mock_externally_linked_work_items_api._get.assert_called_once()
        call_args = mock_externally_linked_work_items_api._get.call_args
        
        assert call_args[0][0] == 'projects/MyProjectId/workitems/MyWorkItemId/externallylinkedworkitems/parent/hostname/MyProjectId/MyLinkedWorkItemId'
        assert call_args[1]['params']['include'] == 'workitem'
        assert call_args[1]['params']['revision'] == '1234'
        assert 'fields[workitems]' in call_args[1]['params']
        assert response.status_code == 200
        assert response.json() == mock_response
    
    def test_get_externally_linked_work_item_different_role(self, mock_externally_linked_work_items_api, mock_response):
        """Test retrieval with different role type."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response
        mock_externally_linked_work_items_api._get = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.get_externally_linked_work_item(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            role_id='relates_to',
            hostname='hostname',
            target_project_id='TargetProject',
            linked_work_item_id='LinkedItem123'
        )
        
        mock_externally_linked_work_items_api._get.assert_called_once()
        call_args = mock_externally_linked_work_items_api._get.call_args
        
        assert call_args[0][0] == 'projects/MyProjectId/workitems/MyWorkItemId/externallylinkedworkitems/relates_to/hostname/TargetProject/LinkedItem123'
        assert response.status_code == 200
    
    def test_get_externally_linked_work_item_not_found(self, mock_externally_linked_work_items_api):
        """Test retrieval when externally linked work item is not found."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 404
        mock_resp.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Externally linked work item not found"
            }]
        }
        mock_externally_linked_work_items_api._get = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.get_externally_linked_work_item(
            project_id='NonExistent',
            work_item_id='WI999',
            role_id='parent',
            hostname='hostname',
            target_project_id='Target',
            linked_work_item_id='Link999'
        )
        
        assert response.status_code == 404
        assert 'errors' in response.json()
    
    def test_get_externally_linked_work_item_unauthorized(self, mock_externally_linked_work_items_api):
        """Test retrieval with unauthorized access."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 401
        mock_resp.json.return_value = {
            "errors": [{
                "status": "401",
                "title": "Unauthorized",
                "detail": "Authentication required"
            }]
        }
        mock_externally_linked_work_items_api._get = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.get_externally_linked_work_item(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            role_id='parent',
            hostname='hostname',
            target_project_id='MyProjectId',
            linked_work_item_id='MyLinkedWorkItemId'
        )
        
        assert response.status_code == 401
    
    def test_get_externally_linked_work_item_verify_response_structure(self, mock_externally_linked_work_items_api, mock_response):
        """Test that response structure matches expected format."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response
        mock_externally_linked_work_items_api._get = Mock(return_value=mock_resp)
        
        response = mock_externally_linked_work_items_api.get_externally_linked_work_item(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            role_id='parent',
            hostname='hostname',
            target_project_id='MyProjectId',
            linked_work_item_id='MyLinkedWorkItemId'
        )
        
        response_data = response.json()
        assert 'data' in response_data
        assert response_data['data']['type'] == 'externallylinkedworkitems'
        assert 'id' in response_data['data']
        assert 'revision' in response_data['data']
        assert 'attributes' in response_data['data']
        assert 'role' in response_data['data']['attributes']
        assert 'workItemURI' in response_data['data']['attributes']
        assert 'links' in response_data['data']
        assert 'included' in response_data
        assert 'links' in response_data
