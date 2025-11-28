"""
Pytest tests for get_global_icons method in Icons class.

Tests the GET /enumerations/icons endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_get_global_icons.py -v
"""
import pytest
from unittest.mock import Mock
import json


@pytest.mark.get
class TestGetGlobalIcons:
    """Unit tests for get_global_icons method using mocks"""
    
    def test_get_global_icons_success_with_200(self, mock_icons_api):
        """Test successful retrieval of global icons list with 200 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 200 status code
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 0
            },
            "data": [
                {
                    "type": "icons",
                    "id": "default/example.gif",
                    "revision": "1234",
                    "attributes": {
                        "iconUrl": "pathexample",
                        "id": "pathexample",
                        "path": "pathexample"
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
                        "self": "server-host-name/application-path/enumerations/defaulticons/example.gif"
                    }
                }
            ],
            "included": [
                {}
            ],
            "links": {
                "self": "server-host-name/application-path/enumerations/defaulticons?page%5Bsize%5D=10&page%5Bnumber%5D=5",
                "first": "server-host-name/application-path/enumerations/defaulticons?page%5Bsize%5D=10&page%5Bnumber%5D=1",
                "prev": "server-host-name/application-path/enumerations/defaulticons?page%5Bsize%5D=10&page%5Bnumber%5D=4",
                "next": "server-host-name/application-path/enumerations/defaulticons?page%5Bsize%5D=10&page%5Bnumber%5D=6",
                "last": "server-host-name/application-path/enumerations/defaulticons?page%5Bsize%5D=10&page%5Bnumber%5D=9"
            }
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_global_icons()
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert 'meta' in data
        assert data['meta']['totalCount'] == 0
        assert isinstance(data['data'], list)
        if len(data['data']) > 0:
            assert data['data'][0]['type'] == 'icons'
            assert 'id' in data['data'][0]
            assert 'attributes' in data['data'][0]
        
        # Verify correct endpoint was called (global context)
        call_args = mock_icons_api._session.get.call_args
        assert 'enumerations/icons' in call_args[0][0]
        assert 'defaulticons' not in call_args[0][0]  # Should NOT be default context
        print("\n✓ Mock: Global icons list retrieved successfully with 200 status code")
    
    def test_get_global_icons_unauthorized_401(self, mock_icons_api):
        """Test unauthorized access with 401 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 401 status code
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "No access token"
                }
            ]
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_global_icons()
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert 'errors' in data
        assert data['errors'][0]['status'] == '401'
        assert data['errors'][0]['title'] == 'Unauthorized'
        assert data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_get_global_icons_bad_request_400(self, mock_icons_api):
        """Test bad request with 400 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 400 status code
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
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
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_global_icons()
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert 'errors' in data
        assert data['errors'][0]['status'] == '400'
        assert data['errors'][0]['title'] == 'Bad Request'
        assert 'source' in data['errors'][0]
        print("\n✓ Mock: Bad request returns 400 status code")
    
    def test_get_global_icons_with_page_size(self, mock_icons_api):
        """Test retrieval with page_size parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute with page_size
        response = mock_icons_api.get_global_icons(page_size=123)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        params = call_args[1]['params']
        assert 'page[size]' in params
        assert params['page[size]'] == 123
        print("\n✓ Mock: page_size parameter applied correctly")
    
    def test_get_global_icons_with_page_number(self, mock_icons_api):
        """Test retrieval with page_number parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute with page_number
        response = mock_icons_api.get_global_icons(page_number=456)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        params = call_args[1]['params']
        assert 'page[number]' in params
        assert params['page[number]'] == 456
        print("\n✓ Mock: page_number parameter applied correctly")
    
    def test_get_global_icons_with_pagination(self, mock_icons_api):
        """Test retrieval with both page_size and page_number parameters (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": [],
            "links": {
                "self": "server-host-name/application-path/enumerations/icons?page%5Bsize%5D=123&page%5Bnumber%5D=456"
            }
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute with both pagination parameters (matching CURL)
        response = mock_icons_api.get_global_icons(page_size=123, page_number=456)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        params = call_args[1]['params']
        assert 'page[size]' in params
        assert params['page[size]'] == 123
        assert 'page[number]' in params
        assert params['page[number]'] == 456
        print("\n✓ Mock: Both pagination parameters applied correctly")
    
    def test_get_global_icons_with_default_fields(self, mock_icons_api):
        """Test retrieval with default fields applied (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute without custom fields (should apply defaults)
        response = mock_icons_api.get_global_icons()
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify default fields are applied
        expected_fields = [
            'collections', 'categories', 'documents', 'document_attachments',
            'document_comments', 'document_parts', 'enumerations', 'globalroles',
            'icons', 'jobs', 'linkedworkitems', 'externallylinkedworkitems',
            'linkedoslcresources', 'pages', 'page_attachments', 'plans',
            'projectroles', 'projects', 'projecttemplates', 'testparameters',
            'testparameter_definitions', 'testrecords', 'teststep_results',
            'testruns', 'testrun_attachments', 'teststepresult_attachments',
            'testrun_comments', 'usergroups', 'users', 'workitems',
            'workitem_attachments', 'workitem_approvals', 'workitem_comments',
            'featureselections', 'teststeps', 'workrecords', 'revisions',
            'testrecord_attachments'
        ]
        
        for field in expected_fields:
            field_key = f'fields[{field}]'
            assert field_key in params, f"Missing default field: {field_key}"
            assert params[field_key] == '@all', f"Field {field_key} should be '@all'"
        
        print("\n✓ Mock: Default fields applied correctly")
    
    def test_get_global_icons_with_custom_fields(self, mock_icons_api):
        """Test retrieval with custom fields filter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute with custom fields
        custom_fields = {
            'icons': 'id,attributes.iconUrl',
            'projects': 'id,attributes.name'
        }
        response = mock_icons_api.get_global_icons(fields=custom_fields)
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom fields override defaults
        assert 'fields[icons]' in params
        assert params['fields[icons]'] == 'id,attributes.iconUrl'
        assert 'fields[projects]' in params
        assert params['fields[projects]'] == 'id,attributes.name'
        
        # Verify other default fields are still present
        assert 'fields[collections]' in params
        assert params['fields[collections]'] == '@all'
        
        print("\n✓ Mock: Custom fields override defaults correctly")
    
    def test_get_global_icons_with_all_parameters(self, mock_icons_api):
        """Test retrieval with all parameters (page_size, page_number, fields) (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute with all parameters matching the CURL example
        custom_fields = {
            'icons': 'id,attributes'
        }
        response = mock_icons_api.get_global_icons(
            page_size=123,
            page_number=456,
            fields=custom_fields
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify pagination parameters
        assert 'page[size]' in params
        assert params['page[size]'] == 123
        assert 'page[number]' in params
        assert params['page[number]'] == 456
        
        # Verify custom fields
        assert 'fields[icons]' in params
        assert params['fields[icons]'] == 'id,attributes'
        
        # Verify default fields are still present for non-overridden fields
        assert 'fields[collections]' in params
        assert params['fields[collections]'] == '@all'
        
        print("\n✓ Mock: All parameters applied correctly")
    
    def test_get_global_icons_empty_response(self, mock_icons_api):
        """Test retrieval with empty response (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_global_icons()
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['meta']['totalCount'] == 0
        assert len(data['data']) == 0
        print("\n✓ Mock: Empty response handled correctly")
    
    def test_get_global_icons_pagination_links(self, mock_icons_api):
        """Test that pagination links are present in response (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": [],
            "links": {
                "self": "server-host-name/application-path/enumerations/icons?page%5Bsize%5D=10&page%5Bnumber%5D=5",
                "first": "server-host-name/application-path/enumerations/icons?page%5Bsize%5D=10&page%5Bnumber%5D=1",
                "prev": "server-host-name/application-path/enumerations/icons?page%5Bsize%5D=10&page%5Bnumber%5D=4",
                "next": "server-host-name/application-path/enumerations/icons?page%5Bsize%5D=10&page%5Bnumber%5D=6",
                "last": "server-host-name/application-path/enumerations/icons?page%5Bsize%5D=10&page%5Bnumber%5D=9"
            }
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_global_icons(page_size=10, page_number=5)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert 'links' in data
        assert 'self' in data['links']
        assert 'first' in data['links']
        assert 'prev' in data['links']
        assert 'next' in data['links']
        assert 'last' in data['links']
        print("\n✓ Mock: Pagination links present in response")
    
    def test_get_global_icons_no_parameters(self, mock_icons_api):
        """Test retrieval without any optional parameters (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute without any parameters
        response = mock_icons_api.get_global_icons()
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify pagination parameters are not present
        assert 'page[size]' not in params or params.get('page[size]') is None
        assert 'page[number]' not in params or params.get('page[number]') is None
        
        # Verify default fields are still applied
        assert 'fields[icons]' in params
        assert params['fields[icons]'] == '@all'
        
        print("\n✓ Mock: No optional parameters, only defaults applied")
    
    def test_get_global_icons_endpoint_format(self, mock_icons_api):
        """Test that the correct endpoint format is used (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_global_icons()
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        endpoint = call_args[0][0]
        
        # Verify endpoint matches expected format (global, not default)
        assert 'enumerations/icons' in endpoint
        assert endpoint.endswith('enumerations/icons')
        assert 'defaulticons' not in endpoint
        
        print("\n✓ Mock: Correct global icons endpoint format used")
    
    def test_get_global_icons_context_distinction(self, mock_icons_api):
        """Test that global icons endpoint is distinct from default icons (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_global_icons()
        
        # Assert
        assert response.status_code == 200
        call_args = mock_icons_api._session.get.call_args
        endpoint = call_args[0][0]
        
        # Verify this is global context (enumerations/icons), not default (enumerations/defaulticons)
        assert 'enumerations/icons' in endpoint
        assert 'defaulticons' not in endpoint
        assert endpoint.count('icons') == 1  # Should appear only once
        
        print("\n✓ Mock: Global context properly distinguished from default context")
    
    def test_get_global_icons_multiple_items(self, mock_icons_api):
        """Test retrieval with multiple icons in response (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 3},
            "data": [
                {
                    "type": "icons",
                    "id": "global/icon1.gif",
                    "attributes": {"iconUrl": "path1", "path": "path1"}
                },
                {
                    "type": "icons",
                    "id": "global/icon2.png",
                    "attributes": {"iconUrl": "path2", "path": "path2"}
                },
                {
                    "type": "icons",
                    "id": "global/icon3.svg",
                    "attributes": {"iconUrl": "path3", "path": "path3"}
                }
            ]
        }
        mock_icons_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_icons_api.get_global_icons()
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['meta']['totalCount'] == 3
        assert len(data['data']) == 3
        assert all(item['type'] == 'icons' for item in data['data'])
        print("\n✓ Mock: Multiple icons in response handled correctly")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
