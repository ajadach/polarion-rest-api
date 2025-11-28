"""
Tests for Revisions.get_revisions method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetRevisions:
    """Test suite for get_revisions method"""
    
    def test_get_revisions_success(self, mock_revisions_api):
        """Test successful retrieval of revisions"""
        # Mock response data based on example
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 1
            },
            "data": [
                {
                    "type": "revisions",
                    "id": "default/1234",
                    "revision": "1234",
                    "attributes": {
                        "created": "1970-01-01T00:00:00Z",
                        "id": "string",
                        "internalCommit": True,
                        "message": "Message",
                        "repositoryName": "Repository name"
                    },
                    "relationships": {
                        "author": {
                            "data": {
                                "type": "users",
                                "id": "MyUserId",
                                "revision": "1234"
                            }
                        }
                    },
                    "links": {
                        "self": "server-host-name/application-path/revisions/default/1234"
                    }
                }
            ],
            "links": {
                "self": "server-host-name/application-path/revisions/default"
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_revisions_api.get_revisions()
        
        # Verify the call
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        
        # Check URL
        assert 'revisions' in call_args[0][0]
        
        # Verify response
        assert response.status_code == 200
        assert response.json()['meta']['totalCount'] == 1
        assert len(response.json()['data']) == 1
        assert response.json()['data'][0]['type'] == 'revisions'
    
    def test_get_revisions_with_pagination(self, mock_revisions_api):
        """Test get_revisions with pagination parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 50},
            "data": [
                {"type": "revisions", "id": "default/1"},
                {"type": "revisions", "id": "default/2"}
            ],
            "links": {
                "self": "server-host-name/application-path/revisions?page%5Bsize%5D=123&page%5Bnumber%5D=456",
                "next": "server-host-name/application-path/revisions?page%5Bsize%5D=123&page%5Bnumber%5D=457"
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with pagination
        response = mock_revisions_api.get_revisions(
            page_size=123,
            page_number=456
        )
        
        # Verify pagination parameters
        call_args = mock_revisions_api._session.get.call_args
        params = call_args[1]['params']
        
        assert params['page[size]'] == 123
        assert params['page[number]'] == 456
        assert response.status_code == 200
    
    def test_get_revisions_with_all_parameters(self, mock_revisions_api):
        """Test get_revisions with all optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "revisions", "id": "default/1"}
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with all parameters
        response = mock_revisions_api.get_revisions(
            page_size=50,
            page_number=2,
            fields={'revisions': 'message,created'},
            include='author',
            query='message:\"bug fix\"',
            sort='-created'
        )
        
        # Verify the call
        call_args = mock_revisions_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom fields override default
        assert 'fields[revisions]' in params
        assert params['fields[revisions]'] == 'message,created'
        
        # Verify other parameters
        assert params['page[size]'] == 50
        assert params['page[number]'] == 2
        assert params['include'] == 'author'
        assert params['query'] == 'message:"bug fix"'
        assert params['sort'] == '-created'
        
        assert response.status_code == 200
    
    def test_get_revisions_default_fields_applied(self, mock_revisions_api):
        """Test that default fields are properly applied when no custom fields provided"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call without fields parameter
        response = mock_revisions_api.get_revisions()
        
        # Verify default fields are applied
        call_args = mock_revisions_api._session.get.call_args
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
    
    def test_get_revisions_error_400(self, mock_revisions_api):
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
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions()
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
    
    def test_get_revisions_error_401(self, mock_revisions_api):
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
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions()
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
    
    def test_get_revisions_attributes(self, mock_revisions_api):
        """Test that response contains expected revision attributes"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "revisions",
                    "id": "default/12345",
                    "revision": "12345",
                    "attributes": {
                        "id": "12345",
                        "repositoryName": "default",
                        "message": "Fixed critical bug in authentication",
                        "created": "2024-01-15T10:30:00Z",
                        "internalCommit": False
                    }
                }
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions()
        
        # Verify attributes
        attrs = response.json()['data'][0]['attributes']
        assert attrs['id'] == '12345'
        assert attrs['repositoryName'] == 'default'
        assert attrs['message'] == 'Fixed critical bug in authentication'
        assert attrs['internalCommit'] is False
    
    def test_get_revisions_with_author_relationship(self, mock_revisions_api):
        """Test that response includes author relationship"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "revisions",
                    "id": "default/1234",
                    "relationships": {
                        "author": {
                            "data": {
                                "type": "users",
                                "id": "john.doe",
                                "revision": "5678"
                            }
                        }
                    }
                }
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions()
        
        # Verify author relationship
        rels = response.json()['data'][0]['relationships']
        assert 'author' in rels
        assert rels['author']['data']['type'] == 'users'
        assert rels['author']['data']['id'] == 'john.doe'
    
    def test_get_revisions_url_structure(self, mock_revisions_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions()
        
        # Verify URL structure
        call_args = mock_revisions_api._session.get.call_args
        url = call_args[0][0]
        
        assert 'revisions' in url
        assert response.status_code == 200
    
    def test_get_revisions_with_query(self, mock_revisions_api):
        """Test get_revisions with query parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "revisions", "id": "default/1", "attributes": {"message": "bug fix"}}
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions(
            query='message:\"bug fix\"'
        )
        
        # Verify query parameter
        call_args = mock_revisions_api._session.get.call_args
        params = call_args[1]['params']
        assert params['query'] == 'message:"bug fix"'
        assert response.json()['data'][0]['attributes']['message'] == 'bug fix'
    
    def test_get_revisions_with_sort(self, mock_revisions_api):
        """Test get_revisions with sort parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "revisions", "id": "default/3"},
                {"type": "revisions", "id": "default/2"},
                {"type": "revisions", "id": "default/1"}
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions(
            sort='-created'
        )
        
        # Verify sort parameter
        call_args = mock_revisions_api._session.get.call_args
        params = call_args[1]['params']
        assert params['sort'] == '-created'
        assert len(response.json()['data']) == 3
    
    def test_get_revisions_with_include(self, mock_revisions_api):
        """Test get_revisions with include parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "revisions", "id": "default/1"}
            ],
            "included": [
                {"type": "users", "id": "author1"}
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions(
            include='author'
        )
        
        # Verify include parameter
        call_args = mock_revisions_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'author'
        assert len(response.json()['included']) == 1
    
    def test_get_revisions_links(self, mock_revisions_api):
        """Test that response contains proper pagination links"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "revisions", "id": "default/1"}
            ],
            "links": {
                "self": "server-host-name/application-path/revisions/default?page%5Bsize%5D=10&page%5Bnumber%5D=5",
                "first": "server-host-name/application-path/revisions/default?page%5Bsize%5D=10&page%5Bnumber%5D=1",
                "prev": "server-host-name/application-path/revisions/default?page%5Bsize%5D=10&page%5Bnumber%5D=4",
                "next": "server-host-name/application-path/revisions/default?page%5Bsize%5D=10&page%5Bnumber%5D=6",
                "last": "server-host-name/application-path/revisions/default?page%5Bsize%5D=10&page%5Bnumber%5D=9"
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions(
            page_size=10,
            page_number=5
        )
        
        # Verify links
        links = response.json()['links']
        assert 'self' in links
        assert 'first' in links
        assert 'prev' in links
        assert 'next' in links
        assert 'last' in links
    
    def test_get_revisions_empty_list(self, mock_revisions_api):
        """Test get_revisions with empty result"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 0
            },
            "data": []
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions()
        
        # Verify empty result
        assert response.status_code == 200
        assert len(response.json()['data']) == 0
        assert response.json()['meta']['totalCount'] == 0
    
    def test_get_revisions_multiple_revisions(self, mock_revisions_api):
        """Test retrieving multiple revisions"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 3},
            "data": [
                {"type": "revisions", "id": "default/1", "attributes": {"message": "Commit 1"}},
                {"type": "revisions", "id": "default/2", "attributes": {"message": "Commit 2"}},
                {"type": "revisions", "id": "default/3", "attributes": {"message": "Commit 3"}}
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions()
        
        # Verify multiple revisions
        data = response.json()['data']
        assert len(data) == 3
        assert all(item['type'] == 'revisions' for item in data)
        assert data[0]['attributes']['message'] == 'Commit 1'
    
    def test_get_revisions_custom_fields_override(self, mock_revisions_api):
        """Test that custom fields override default fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        mock_revisions_api._session.get.return_value = mock_response
        
        custom_fields = {
            'revisions': 'message,created,author'
        }
        
        response = mock_revisions_api.get_revisions(
            fields=custom_fields
        )
        
        call_args = mock_revisions_api._session.get.call_args
        params = call_args[1]['params']
        
        # Custom field should override
        assert params['fields[revisions]'] == 'message,created,author'
        
        # Other collections should still be @all
        assert params['fields[users]'] == '@all'
        assert params['fields[projects]'] == '@all'
    
    def test_get_revisions_internal_commit(self, mock_revisions_api):
        """Test revision with internal commit flag"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "revisions",
                    "id": "default/5000",
                    "attributes": {
                        "message": "Internal system commit",
                        "internalCommit": True
                    }
                }
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions()
        
        # Verify internal commit flag
        assert response.json()['data'][0]['attributes']['internalCommit'] is True
    
    def test_get_revisions_pagination_first_page(self, mock_revisions_api):
        """Test get_revisions with first page"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 100},
            "data": [
                {"type": "revisions", "id": "default/1"},
                {"type": "revisions", "id": "default/2"}
            ],
            "links": {
                "self": "server-host-name/application-path/revisions?page[number]=1",
                "next": "server-host-name/application-path/revisions?page[number]=2"
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions(
            page_size=10,
            page_number=1
        )
        
        # Verify pagination
        call_args = mock_revisions_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 10
        assert params['page[number]'] == 1
        
        # Verify response has next link but no prev
        assert 'next' in response.json()['links']
    
    def test_get_revisions_repository_name_in_attributes(self, mock_revisions_api):
        """Test revision with repository name"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "revisions",
                    "id": "custom-repo/1234",
                    "attributes": {
                        "repositoryName": "custom-repo",
                        "message": "Update from custom repository"
                    }
                }
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions()
        
        # Verify repository name
        attrs = response.json()['data'][0]['attributes']
        assert attrs['repositoryName'] == 'custom-repo'
    
    def test_get_revisions_minimal_parameters(self, mock_revisions_api):
        """Test get_revisions with no optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "revisions", "id": "default/1"}
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with no parameters
        response = mock_revisions_api.get_revisions()
        
        # Verify call was made
        mock_revisions_api._session.get.assert_called_once()
        
        # Verify only default fields are in params
        call_args = mock_revisions_api._session.get.call_args
        params = call_args[1]['params']
        
        # Should have default fields but no pagination, include, query, or sort
        assert 'page[size]' not in params
        assert 'page[number]' not in params
        assert 'include' not in params
        assert 'query' not in params
        assert 'sort' not in params
        
        assert response.status_code == 200
    
    def test_get_revisions_complex_query(self, mock_revisions_api):
        """Test get_revisions with complex query"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "revisions", "id": "default/100"}
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revisions(
            query='message:\"fix\" AND NOT internalCommit:true'
        )
        
        # Verify complex query
        call_args = mock_revisions_api._session.get.call_args
        params = call_args[1]['params']
        assert 'query' in params
        assert 'fix' in params['query']
        assert response.status_code == 200
