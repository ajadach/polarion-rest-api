"""
Tests for Plans.get_plans method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetPlans:
    """Test suite for get_plans method"""
    
    def test_get_plans_success(self, mock_plans_api):
        """Test successful retrieval of plans list"""
        # Mock response data based on example
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 1
            },
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId",
                    "revision": "1234",
                    "attributes": {
                        "id": "MyPlanId",
                        "name": "My Plan",
                        "status": "active",
                        "isTemplate": False
                    },
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/plans/MyPlanId?revision=1234"
                    }
                }
            ],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/plans"
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_plans_api.get_plans(
            project_id='MyProjectId'
        )
        
        # Verify the call
        mock_plans_api._session.get.assert_called_once()
        call_args = mock_plans_api._session.get.call_args
        
        # Check URL
        assert 'projects/MyProjectId/plans' in call_args[0][0]
        
        # Verify response
        assert response.status_code == 200
        assert response.json()['meta']['totalCount'] == 1
        assert len(response.json()['data']) == 1
        assert response.json()['data'][0]['type'] == 'plans'
    
    def test_get_plans_with_pagination(self, mock_plans_api):
        """Test get_plans with pagination parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 100},
            "data": [],
            "links": {
                "self": "server/projects/MyProjectId/plans?page%5Bsize%5D=10&page%5Bnumber%5D=5",
                "first": "server/projects/MyProjectId/plans?page%5Bsize%5D=10&page%5Bnumber%5D=1",
                "prev": "server/projects/MyProjectId/plans?page%5Bsize%5D=10&page%5Bnumber%5D=4",
                "next": "server/projects/MyProjectId/plans?page%5Bsize%5D=10&page%5Bnumber%5D=6",
                "last": "server/projects/MyProjectId/plans?page%5Bsize%5D=10&page%5Bnumber%5D=10"
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId',
            page_size=10,
            page_number=5
        )
        
        # Verify pagination parameters
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 10
        assert params['page[number]'] == 5
        assert response.status_code == 200
    
    def test_get_plans_with_all_parameters(self, mock_plans_api):
        """Test get_plans with all optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId',
            page_size=123,
            page_number=456,
            fields={'plans': 'name,status'},
            include='author,project',
            query='status:active',
            sort='name',
            revision='1234',
            templates=True
        )
        
        # Verify all parameters
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        
        assert params['page[size]'] == 123
        assert params['page[number]'] == 456
        assert params['fields[plans]'] == 'name,status'
        assert params['include'] == 'author,project'
        assert params['query'] == 'status:active'
        assert params['sort'] == 'name'
        assert params['revision'] == '1234'
        assert params['templates'] is True
        assert response.status_code == 200
    
    def test_get_plans_default_fields_applied(self, mock_plans_api):
        """Test that default fields are properly applied"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='TEST_PROJECT'
        )
        
        # Verify default fields are applied
        call_args = mock_plans_api._session.get.call_args
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
    
    def test_get_plans_custom_fields_override(self, mock_plans_api):
        """Test that custom fields override default fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        
        mock_plans_api._session.get.return_value = mock_response
        
        custom_fields = {
            'plans': 'id,name,status,isTemplate'
        }
        
        response = mock_plans_api.get_plans(
            project_id='TEST_PROJECT',
            fields=custom_fields
        )
        
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        
        # Custom field should override
        assert params['fields[plans]'] == 'id,name,status,isTemplate'
        
        # Other collections should still be @all
        assert params['fields[workitems]'] == '@all'
        assert params['fields[projects]'] == '@all'
    
    def test_get_plans_with_query(self, mock_plans_api):
        """Test get_plans with query filter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 5}, "data": []}
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId',
            query='status:active AND isTemplate:false'
        )
        
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['query'] == 'status:active AND isTemplate:false'
        assert response.status_code == 200
    
    def test_get_plans_with_sort(self, mock_plans_api):
        """Test get_plans with sort parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId',
            sort='name,-created'
        )
        
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['sort'] == 'name,-created'
        assert response.status_code == 200
    
    def test_get_plans_templates_true(self, mock_plans_api):
        """Test get_plans with templates=true to get only templates"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 2},
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/Template1",
                    "attributes": {"isTemplate": True}
                },
                {
                    "type": "plans",
                    "id": "MyProjectId/Template2",
                    "attributes": {"isTemplate": True}
                }
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId',
            templates=True
        )
        
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['templates'] is True
        assert response.status_code == 200
    
    def test_get_plans_templates_false(self, mock_plans_api):
        """Test get_plans with templates=false to get only instances"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 3},
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/Plan1",
                    "attributes": {"isTemplate": False}
                }
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId',
            templates=False
        )
        
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['templates'] is False
        assert response.status_code == 200
    
    def test_get_plans_error_400(self, mock_plans_api):
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
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId'
        )
        
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
    
    def test_get_plans_error_401(self, mock_plans_api):
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
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId'
        )
        
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
        assert errors[0]['detail'] == 'No access token'
    
    def test_get_plans_with_revision(self, mock_plans_api):
        """Test get_plans with specific revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId',
            revision='1234'
        )
        
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '1234'
        assert response.status_code == 200
    
    def test_get_plans_with_include(self, mock_plans_api):
        """Test get_plans with include parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 1},
            "data": [],
            "included": [
                {"type": "users", "id": "UserId"},
                {"type": "projects", "id": "ProjectId"}
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId',
            include='author,project,workItems'
        )
        
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'author,project,workItems'
        assert 'included' in response.json()
    
    def test_get_plans_empty_list(self, mock_plans_api):
        """Test get_plans returns empty list when no plans exist"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": [],
            "links": {"self": "server/projects/MyProjectId/plans"}
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId'
        )
        
        assert response.status_code == 200
        assert response.json()['meta']['totalCount'] == 0
        assert len(response.json()['data']) == 0
    
    def test_get_plans_multiple_plans(self, mock_plans_api):
        """Test get_plans returns multiple plans"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 3},
            "data": [
                {"type": "plans", "id": "MyProjectId/Plan1"},
                {"type": "plans", "id": "MyProjectId/Plan2"},
                {"type": "plans", "id": "MyProjectId/Plan3"}
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId'
        )
        
        assert response.status_code == 200
        assert len(response.json()['data']) == 3
        assert response.json()['meta']['totalCount'] == 3
    
    def test_get_plans_attributes(self, mock_plans_api):
        """Test that response contains expected plan attributes"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 1},
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId",
                    "revision": "1234",
                    "attributes": {
                        "id": "MyPlanId",
                        "name": "Sprint 1",
                        "status": "active",
                        "isTemplate": False,
                        "startDate": "2023-01-01",
                        "dueDate": "2023-01-31",
                        "calculationType": "timeBased"
                    }
                }
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId'
        )
        
        attrs = response.json()['data'][0]['attributes']
        assert attrs['name'] == 'Sprint 1'
        assert attrs['status'] == 'active'
        assert attrs['isTemplate'] is False
        assert 'startDate' in attrs
        assert 'dueDate' in attrs
    
    def test_get_plans_relationships(self, mock_plans_api):
        """Test that response contains plan relationships"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 1},
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId",
                    "relationships": {
                        "author": {
                            "data": {"type": "users", "id": "UserId"}
                        },
                        "project": {
                            "data": {"type": "projects", "id": "MyProjectId"}
                        },
                        "workItems": {
                            "data": [],
                            "meta": {"totalCount": 0}
                        }
                    }
                }
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId'
        )
        
        rels = response.json()['data'][0]['relationships']
        assert 'author' in rels
        assert 'project' in rels
        assert 'workItems' in rels
        assert rels['author']['data']['type'] == 'users'
        assert rels['project']['data']['type'] == 'projects'
    
    def test_get_plans_links(self, mock_plans_api):
        """Test that response contains proper links"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 1},
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId",
                    "links": {
                        "self": "server/projects/MyProjectId/plans/MyPlanId",
                        "portal": "server/polarion/redirect/project/MyProjectId/plan?id=MyPlanId"
                    }
                }
            ],
            "links": {
                "self": "server/projects/MyProjectId/plans",
                "portal": "server/polarion/redirect/project/MyProjectId/plans"
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='MyProjectId'
        )
        
        # Verify individual plan links
        plan_links = response.json()['data'][0]['links']
        assert 'self' in plan_links
        assert 'portal' in plan_links
        
        # Verify collection links
        collection_links = response.json()['links']
        assert 'self' in collection_links
        assert 'portal' in collection_links
    
    def test_get_plans_url_structure(self, mock_plans_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"totalCount": 0}, "data": []}
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plans(
            project_id='TEST_PROJ'
        )
        
        call_args = mock_plans_api._session.get.call_args
        url = call_args[0][0]
        
        assert 'projects/TEST_PROJ' in url
        assert url.endswith('/plans')
        assert response.status_code == 200
