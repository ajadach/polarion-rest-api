"""
Tests for Pages.get_page method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetPage:
    """Test suite for get_page method"""
    
    def test_get_page_success(self, mock_pages_api):
        """Test successful retrieval of a page"""
        # Mock response data based on example
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "revision": "1234",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z",
                    "pageName": "MyRichPageId",
                    "spaceId": "MySpaceId",
                    "title": "Title",
                    "updated": "1970-01-01T00:00:00Z"
                },
                "relationships": {
                    "attachments": {
                        "data": [
                            {
                                "type": "page_attachments",
                                "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId",
                                "revision": "1234"
                            }
                        ],
                        "meta": {
                            "totalCount": 0
                        }
                    },
                    "author": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId",
                            "revision": "1234"
                        }
                    },
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "MyProjectId",
                            "revision": "1234"
                        }
                    },
                    "updatedBy": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId",
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
                    "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId?revision=1234"
                }
            },
            "included": [
                {}
            ],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId?revision=1234"
            }
        }
        
        mock_pages_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId'
        )
        
        # Verify the call
        mock_pages_api._session.get.assert_called_once()
        call_args = mock_pages_api._session.get.call_args
        
        # Check URL
        assert 'projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId' in call_args[0][0]
        
        # Verify response
        assert response.status_code == 200
        assert response.json()['data']['type'] == 'pages'
        assert response.json()['data']['attributes']['pageName'] == 'MyRichPageId'
        assert response.json()['data']['attributes']['spaceId'] == 'MySpaceId'
    
    def test_get_page_with_all_parameters(self, mock_pages_api):
        """Test get_page with all optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId"
            }
        }
        
        mock_pages_api._session.get.return_value = mock_response
        
        # Call with all parameters
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            fields={'pages': 'title,pageName'},
            include='author,project,attachments',
            revision='1234'
        )
        
        # Verify the call
        call_args = mock_pages_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom fields override default
        assert 'fields[pages]' in params
        assert params['fields[pages]'] == 'title,pageName'
        
        # Verify other parameters
        assert params['include'] == 'author,project,attachments'
        assert params['revision'] == '1234'
        
        assert response.status_code == 200
    
    def test_get_page_with_default_space(self, mock_pages_api):
        """Test get_page with _default space"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "pages"}}
        
        mock_pages_api._session.get.return_value = mock_response
        
        # Call with _default space
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='_default',
            page_name='MyRichPageId'
        )
        
        # Verify URL contains _default
        call_args = mock_pages_api._session.get.call_args
        assert 'spaces/_default/' in call_args[0][0]
        assert response.status_code == 200
    
    def test_get_page_default_fields_applied(self, mock_pages_api):
        """Test that default fields are properly applied when no custom fields provided"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_pages_api._session.get.return_value = mock_response
        
        # Call without fields parameter
        response = mock_pages_api.get_page(
            project_id='TEST_PROJECT',
            space_id='TEST_SPACE',
            page_name='TEST_PAGE'
        )
        
        # Verify default fields are applied
        call_args = mock_pages_api._session.get.call_args
        params = call_args[1]['params']
        
        # Check that all default collection fields are set to @all
        expected_collections = [
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
        
        for collection in expected_collections:
            field_key = f'fields[{collection}]'
            assert field_key in params
            assert params[field_key] == '@all'
    
    def test_get_page_custom_fields_override(self, mock_pages_api):
        """Test that custom fields override default fields for specified keys only"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_pages_api._session.get.return_value = mock_response
        
        # Call with custom fields for pages only
        custom_fields = {
            'pages': 'title,pageName,spaceId'
        }
        
        response = mock_pages_api.get_page(
            project_id='TEST_PROJECT',
            space_id='TEST_SPACE',
            page_name='TEST_PAGE',
            fields=custom_fields
        )
        
        call_args = mock_pages_api._session.get.call_args
        params = call_args[1]['params']
        
        # Custom field should override
        assert params['fields[pages]'] == 'title,pageName,spaceId'
        
        # Other collections should still be @all
        assert params['fields[workitems]'] == '@all'
        assert params['fields[projects]'] == '@all'
    
    def test_get_page_error_400(self, mock_pages_api):
        """Test handling of 400 Bad Request error"""
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
        
        mock_pages_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId'
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
        assert 'Unexpected token' in errors[0]['detail']
    
    def test_get_page_error_401(self, mock_pages_api):
        """Test handling of 401 Unauthorized error"""
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
        
        mock_pages_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId'
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
        assert errors[0]['detail'] == 'No access token'
    
    def test_get_page_with_revision(self, mock_pages_api):
        """Test get_page with specific revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "revision": "1234"
            }
        }
        
        mock_pages_api._session.get.return_value = mock_response
        
        # Call with revision
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            revision='1234'
        )
        
        # Verify revision parameter
        call_args = mock_pages_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '1234'
        
        # Verify response
        assert response.status_code == 200
        assert response.json()['data']['revision'] == '1234'
    
    def test_get_page_with_include(self, mock_pages_api):
        """Test get_page with include parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId"
            },
            "included": [
                {
                    "type": "users",
                    "id": "MyUserId"
                },
                {
                    "type": "projects",
                    "id": "MyProjectId"
                }
            ]
        }
        
        mock_pages_api._session.get.return_value = mock_response
        
        # Call with include
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            include='author,project,updatedBy'
        )
        
        # Verify include parameter
        call_args = mock_pages_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'author,project,updatedBy'
        
        # Verify response contains included entities
        assert response.status_code == 200
        assert 'included' in response.json()
        assert len(response.json()['included']) == 2
    
    def test_get_page_attributes(self, mock_pages_api):
        """Test that response contains all expected attributes"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "revision": "1234",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z",
                    "pageName": "MyRichPageId",
                    "spaceId": "MySpaceId",
                    "title": "My Page Title",
                    "updated": "2023-01-15T10:30:00Z"
                }
            }
        }
        
        mock_pages_api._session.get.return_value = mock_response
        
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId'
        )
        
        # Verify attributes
        attrs = response.json()['data']['attributes']
        assert attrs['pageName'] == 'MyRichPageId'
        assert attrs['spaceId'] == 'MySpaceId'
        assert attrs['title'] == 'My Page Title'
        assert 'created' in attrs
        assert 'updated' in attrs
    
    def test_get_page_relationships(self, mock_pages_api):
        """Test that response contains proper relationships"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "relationships": {
                    "attachments": {
                        "data": [
                            {
                                "type": "page_attachments",
                                "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId",
                                "revision": "1234"
                            }
                        ],
                        "meta": {
                            "totalCount": 1
                        }
                    },
                    "author": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId",
                            "revision": "1234"
                        }
                    },
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "MyProjectId",
                            "revision": "1234"
                        }
                    },
                    "updatedBy": {
                        "data": {
                            "type": "users",
                            "id": "UpdaterUserId",
                            "revision": "1234"
                        }
                    }
                }
            }
        }
        
        mock_pages_api._session.get.return_value = mock_response
        
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId'
        )
        
        # Verify relationships structure
        data = response.json()['data']
        assert 'relationships' in data
        assert 'attachments' in data['relationships']
        assert 'author' in data['relationships']
        assert 'project' in data['relationships']
        assert 'updatedBy' in data['relationships']
        
        # Verify attachments relationship
        assert len(data['relationships']['attachments']['data']) == 1
        assert data['relationships']['attachments']['data'][0]['type'] == 'page_attachments'
        assert data['relationships']['attachments']['meta']['totalCount'] == 1
        
        # Verify other relationships
        assert data['relationships']['author']['data']['type'] == 'users'
        assert data['relationships']['project']['data']['type'] == 'projects'
        assert data['relationships']['updatedBy']['data']['type'] == 'users'
    
    def test_get_page_links(self, mock_pages_api):
        """Test that response contains proper links"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "links": {
                    "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId?revision=1234"
                }
            },
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId?revision=1234"
            }
        }
        
        mock_pages_api._session.get.return_value = mock_response
        
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId'
        )
        
        # Verify links structure
        data = response.json()['data']
        assert 'links' in data
        assert 'self' in data['links']
        assert 'pages/MyRichPageId' in data['links']['self']
        
        # Verify top-level links
        assert 'links' in response.json()
        assert 'self' in response.json()['links']
    
    def test_get_page_with_special_characters(self, mock_pages_api):
        """Test get_page with special characters in page name"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "pages"}}
        
        mock_pages_api._session.get.return_value = mock_response
        
        # Call with special characters
        response = mock_pages_api.get_page(
            project_id='My-Project',
            space_id='My Space',
            page_name='My Page (2023)'
        )
        
        # Verify the call was made
        mock_pages_api._session.get.assert_called_once()
        assert response.status_code == 200
    
    def test_get_page_url_structure(self, mock_pages_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_pages_api._session.get.return_value = mock_response
        
        response = mock_pages_api.get_page(
            project_id='TEST_PROJ',
            space_id='TEST_SPACE',
            page_name='TEST_PAGE'
        )
        
        # Verify URL structure
        call_args = mock_pages_api._session.get.call_args
        url = call_args[0][0]
        
        # Should contain all path segments in correct order
        assert 'projects/TEST_PROJ' in url
        assert 'spaces/TEST_SPACE' in url
        assert 'pages/TEST_PAGE' in url
        
        assert response.status_code == 200
    
    def test_get_page_with_attachments(self, mock_pages_api):
        """Test get_page response with multiple attachments"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "relationships": {
                    "attachments": {
                        "data": [
                            {
                                "type": "page_attachments",
                                "id": "MyProjectId/MySpaceId/MyRichPageId/attachment1"
                            },
                            {
                                "type": "page_attachments",
                                "id": "MyProjectId/MySpaceId/MyRichPageId/attachment2"
                            },
                            {
                                "type": "page_attachments",
                                "id": "MyProjectId/MySpaceId/MyRichPageId/attachment3"
                            }
                        ],
                        "meta": {
                            "totalCount": 3
                        }
                    }
                }
            }
        }
        
        mock_pages_api._session.get.return_value = mock_response
        
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId'
        )
        
        # Verify attachments
        attachments = response.json()['data']['relationships']['attachments']
        assert len(attachments['data']) == 3
        assert attachments['meta']['totalCount'] == 3
        for attachment in attachments['data']:
            assert attachment['type'] == 'page_attachments'
    
    def test_get_page_minimal_response(self, mock_pages_api):
        """Test get_page with minimal response (no relationships)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "pages",
                "id": "MyProjectId/MySpaceId/MyRichPageId",
                "attributes": {
                    "pageName": "MyRichPageId",
                    "spaceId": "MySpaceId",
                    "title": "Simple Page"
                }
            }
        }
        
        mock_pages_api._session.get.return_value = mock_response
        
        response = mock_pages_api.get_page(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            fields={'pages': 'pageName,spaceId,title'}
        )
        
        # Verify minimal response
        assert response.status_code == 200
        data = response.json()['data']
        assert data['type'] == 'pages'
        assert 'attributes' in data
        assert len(data['attributes']) == 3
