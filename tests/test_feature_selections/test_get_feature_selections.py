"""
Unit tests for get_feature_selections method.
Tests the retrieval of a list of feature selections.
"""
import pytest
from unittest.mock import Mock
import requests


class TestGetFeatureSelections:
    """Test suite for get_feature_selections method."""
    
    @pytest.fixture
    def mock_response_200(self):
        """Fixture for mock 200 response data."""
        return {
            "meta": {
                "totalCount": 0
            },
            "data": [
                {
                    "type": "featureselections",
                    "id": "MyProjectId/MyWorkItemId/included/MyProjectId/MyWorkItemId",
                    "revision": "1234",
                    "attributes": {
                        "selectionType": "excluded"
                    },
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "MyProjectId/MyWorkItemId",
                                "revision": "1234"
                            }
                        }
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
                        "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/featureselections/included/MyProjectId/MyWorkItemId?revision=1234"
                    }
                }
            ],
            "included": [
                {}
            ],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/featureselections/included/MyProjectId?page%5Bsize%5D=10&page%5Bnumber%5D=5",
                "first": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/featureselections/included/MyProjectId?page%5Bsize%5D=10&page%5Bnumber%5D=1",
                "prev": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/featureselections/included/MyProjectId?page%5Bsize%5D=10&page%5Bnumber%5D=4",
                "next": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/featureselections/included/MyProjectId?page%5Bsize%5D=10&page%5Bnumber%5D=6",
                "last": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/featureselections/included/MyProjectId?page%5Bsize%5D=10&page%5Bnumber%5D=9"
            }
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
    
    def test_get_feature_selections_basic(self, mock_feature_selections_api, mock_response_200):
        """Test basic retrieval of feature selections without optional parameters."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_200
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId'
        )
        
        mock_feature_selections_api._get.assert_called_once()
        call_args = mock_feature_selections_api._get.call_args
        
        assert call_args[0][0] == 'projects/MyProjectId/workitems/MyWorkItemId/featureselections'
        assert response.status_code == 200
        assert response.json() == mock_response_200
    
    def test_get_feature_selections_with_pagination(self, mock_feature_selections_api, mock_response_200):
        """Test retrieval with pagination parameters."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_200
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            page_size=123,
            page_number=456
        )
        
        mock_feature_selections_api._get.assert_called_once()
        call_args = mock_feature_selections_api._get.call_args
        
        assert call_args[0][0] == 'projects/MyProjectId/workitems/MyWorkItemId/featureselections'
        assert call_args[1]['params']['page[size]'] == 123
        assert call_args[1]['params']['page[number]'] == 456
        assert response.status_code == 200
    
    def test_get_feature_selections_with_fields(self, mock_feature_selections_api, mock_response_200):
        """Test retrieval with custom fields parameter."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_200
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        custom_fields = {
            'workitems': 'id,title',
            'featureselections': 'id,selectionType'
        }
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            fields=custom_fields
        )
        
        mock_feature_selections_api._get.assert_called_once()
        call_args = mock_feature_selections_api._get.call_args
        
        assert call_args[0][0] == 'projects/MyProjectId/workitems/MyWorkItemId/featureselections'
        assert call_args[1]['params'] is not None
        assert 'fields[workitems]' in call_args[1]['params']
        assert call_args[1]['params']['fields[workitems]'] == 'id,title'
        assert response.status_code == 200
    
    def test_get_feature_selections_with_include(self, mock_feature_selections_api, mock_response_200):
        """Test retrieval with include parameter."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_200
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            include='workItem'
        )
        
        mock_feature_selections_api._get.assert_called_once()
        call_args = mock_feature_selections_api._get.call_args
        
        assert call_args[1]['params']['include'] == 'workItem'
        assert response.status_code == 200
    
    def test_get_feature_selections_with_revision(self, mock_feature_selections_api, mock_response_200):
        """Test retrieval with revision parameter."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_200
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            revision='1234'
        )
        
        mock_feature_selections_api._get.assert_called_once()
        call_args = mock_feature_selections_api._get.call_args
        
        assert call_args[1]['params']['revision'] == '1234'
        assert response.status_code == 200
    
    def test_get_feature_selections_with_all_parameters(self, mock_feature_selections_api, mock_response_200):
        """Test retrieval with all optional parameters."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_200
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        custom_fields = {
            'workitems': 'id,title',
            'featureselections': 'id,selectionType'
        }
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            page_size=123,
            page_number=456,
            fields=custom_fields,
            include='workItem',
            revision='1234'
        )
        
        mock_feature_selections_api._get.assert_called_once()
        call_args = mock_feature_selections_api._get.call_args
        
        assert call_args[0][0] == 'projects/MyProjectId/workitems/MyWorkItemId/featureselections'
        assert call_args[1]['params']['page[size]'] == 123
        assert call_args[1]['params']['page[number]'] == 456
        assert call_args[1]['params']['include'] == 'workItem'
        assert call_args[1]['params']['revision'] == '1234'
        assert 'fields[workitems]' in call_args[1]['params']
        assert response.status_code == 200
        assert response.json() == mock_response_200
    
    def test_get_feature_selections_empty_list(self, mock_feature_selections_api):
        """Test retrieval when there are no feature selections."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "meta": {
                "totalCount": 0
            },
            "data": [],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/featureselections"
            }
        }
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId'
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['meta']['totalCount'] == 0
        assert len(response_data['data']) == 0
    
    def test_get_feature_selections_unauthorized(self, mock_feature_selections_api, mock_response_401):
        """Test retrieval with unauthorized access."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 401
        mock_resp.json.return_value = mock_response_401
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId'
        )
        
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
    
    def test_get_feature_selections_not_found(self, mock_feature_selections_api):
        """Test retrieval when work item is not found."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 404
        mock_resp.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Work item not found"
            }]
        }
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='NonExistent',
            work_item_id='WI999'
        )
        
        assert response.status_code == 404
        assert 'errors' in response.json()
    
    def test_get_feature_selections_verify_response_structure(self, mock_feature_selections_api, mock_response_200):
        """Test that response structure matches expected format."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_200
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId'
        )
        
        response_data = response.json()
        assert 'meta' in response_data
        assert 'totalCount' in response_data['meta']
        assert 'data' in response_data
        assert isinstance(response_data['data'], list)
        assert 'links' in response_data
        
        # Verify first item structure
        if len(response_data['data']) > 0:
            item = response_data['data'][0]
            assert item['type'] == 'featureselections'
            assert 'id' in item
            assert 'revision' in item
            assert 'attributes' in item
            assert 'selectionType' in item['attributes']
            assert 'relationships' in item
    
    def test_get_feature_selections_pagination_links(self, mock_feature_selections_api, mock_response_200):
        """Test that pagination links are present in response."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_200
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            page_size=10,
            page_number=5
        )
        
        response_data = response.json()
        assert 'links' in response_data
        assert 'self' in response_data['links']
        assert 'first' in response_data['links']
        assert 'prev' in response_data['links']
        assert 'next' in response_data['links']
        assert 'last' in response_data['links']
    
    def test_get_feature_selections_multiple_items(self, mock_feature_selections_api):
        """Test retrieval when multiple feature selections exist."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "meta": {
                "totalCount": 3
            },
            "data": [
                {
                    "type": "featureselections",
                    "id": "MyProjectId/MyWorkItemId/included/ProjectA/ItemA",
                    "revision": "1234",
                    "attributes": {
                        "selectionType": "included"
                    },
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "ProjectA/ItemA",
                                "revision": "1234"
                            }
                        }
                    }
                },
                {
                    "type": "featureselections",
                    "id": "MyProjectId/MyWorkItemId/excluded/ProjectB/ItemB",
                    "revision": "1235",
                    "attributes": {
                        "selectionType": "excluded"
                    },
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "ProjectB/ItemB",
                                "revision": "1235"
                            }
                        }
                    }
                },
                {
                    "type": "featureselections",
                    "id": "MyProjectId/MyWorkItemId/included/ProjectC/ItemC",
                    "revision": "1236",
                    "attributes": {
                        "selectionType": "included"
                    },
                    "relationships": {
                        "workItem": {
                            "data": {
                                "type": "workitems",
                                "id": "ProjectC/ItemC",
                                "revision": "1236"
                            }
                        }
                    }
                }
            ],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/featureselections"
            }
        }
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId'
        )
        
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['meta']['totalCount'] == 3
        assert len(response_data['data']) == 3
        
        # Verify different selection types
        selection_types = [item['attributes']['selectionType'] for item in response_data['data']]
        assert 'included' in selection_types
        assert 'excluded' in selection_types
    
    def test_get_feature_selections_different_work_item(self, mock_feature_selections_api, mock_response_200):
        """Test retrieval for different project and work item IDs."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_200
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='DifferentProject',
            work_item_id='WI-9999'
        )
        
        mock_feature_selections_api._get.assert_called_once()
        call_args = mock_feature_selections_api._get.call_args
        
        assert call_args[0][0] == 'projects/DifferentProject/workitems/WI-9999/featureselections'
        assert response.status_code == 200
    
    def test_get_feature_selections_page_number_only(self, mock_feature_selections_api, mock_response_200):
        """Test retrieval with only page_number parameter."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_200
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            page_number=2
        )
        
        call_args = mock_feature_selections_api._get.call_args
        assert call_args[1]['params']['page[number]'] == 2
        assert response.status_code == 200
    
    def test_get_feature_selections_page_size_only(self, mock_feature_selections_api, mock_response_200):
        """Test retrieval with only page_size parameter."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_200
        mock_feature_selections_api._get = Mock(return_value=mock_resp)
        
        response = mock_feature_selections_api.get_feature_selections(
            project_id='MyProjectId',
            work_item_id='MyWorkItemId',
            page_size=50
        )
        
        call_args = mock_feature_selections_api._get.call_args
        assert call_args[1]['params']['page[size]'] == 50
        assert response.status_code == 200
