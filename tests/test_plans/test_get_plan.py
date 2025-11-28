"""
Tests for Plans.get_plan method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetPlan:
    """Test suite for get_plan method"""
    
    def test_get_plan_success(self, mock_plans_api):
        """Test successful retrieval of a single plan"""
        # Mock response data based on example
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "revision": "1234",
                "attributes": {
                    "allowedTypes": ["optionId"],
                    "calculationType": "timeBased",
                    "capacity": 0,
                    "color": "Color",
                    "created": "1970-01-01T00:00:00Z",
                    "defaultEstimate": 0,
                    "description": {
                        "type": "text/plain",
                        "value": "My text value"
                    },
                    "dueDate": "1970-01-01",
                    "estimationField": "Estimation Field",
                    "finishedOn": "1970-01-01T00:00:00Z",
                    "homePageContent": {
                        "type": "text/html",
                        "value": "My text value"
                    },
                    "id": "ID",
                    "isTemplate": True,
                    "name": "Name",
                    "previousTimeSpent": "5 1/2d",
                    "prioritizationField": "Prioritization Field",
                    "sortOrder": 0,
                    "startDate": "1970-01-01",
                    "startedOn": "1970-01-01T00:00:00Z",
                    "status": "string",
                    "updated": "1970-01-01T00:00:00Z",
                    "useReportFromTemplate": True
                },
                "relationships": {
                    "author": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId",
                            "revision": "1234"
                        }
                    },
                    "parent": {
                        "data": {
                            "type": "plans",
                            "id": "MyProjectId/MyPlanId",
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
                    "projectSpan": {
                        "data": [
                            {
                                "type": "projects",
                                "id": "MyProjectId",
                                "revision": "1234"
                            }
                        ],
                        "meta": {
                            "totalCount": 0
                        }
                    },
                    "template": {
                        "data": {
                            "type": "plans",
                            "id": "MyProjectId/MyPlanId",
                            "revision": "1234"
                        }
                    },
                    "workItems": {
                        "data": [
                            {
                                "type": "workitems",
                                "id": "MyProjectId/MyWorkItemId",
                                "revision": "1234"
                            }
                        ],
                        "meta": {
                            "totalCount": 0
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/projects/MyProjectId/plans/MyPlanId?revision=1234",
                    "portal": "server-host-name/application-path/polarion/redirect/project/MyProjectId/plan?id=MyPlanId&revision=1234"
                }
            },
            "included": [{}],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/plans/MyPlanId?revision=1234"
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify the call
        mock_plans_api._session.get.assert_called_once()
        call_args = mock_plans_api._session.get.call_args
        
        # Check URL
        assert 'projects/MyProjectId/plans/MyPlanId' in call_args[0][0]
        
        # Verify response
        assert response.status_code == 200
        assert response.json()['data']['type'] == 'plans'
        assert response.json()['data']['id'] == 'MyProjectId/MyPlanId'
        assert response.json()['data']['attributes']['name'] == 'Name'
    
    def test_get_plan_with_all_parameters(self, mock_plans_api):
        """Test get_plan with all optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId"
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        # Call with all parameters
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            fields={'plans': 'name,status'},
            include='author,project,workItems',
            revision='1234'
        )
        
        # Verify the call
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom fields override default
        assert 'fields[plans]' in params
        assert params['fields[plans]'] == 'name,status'
        
        # Verify other parameters
        assert params['include'] == 'author,project,workItems'
        assert params['revision'] == '1234'
        
        assert response.status_code == 200
    
    def test_get_plan_default_fields_applied(self, mock_plans_api):
        """Test that default fields are properly applied when no custom fields provided"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_plans_api._session.get.return_value = mock_response
        
        # Call without fields parameter
        response = mock_plans_api.get_plan(
            project_id='TEST_PROJECT',
            plan_id='TEST_PLAN'
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
    
    def test_get_plan_error_400(self, mock_plans_api):
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
        
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
    
    def test_get_plan_error_401(self, mock_plans_api):
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
        
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
    
    def test_get_plan_attributes(self, mock_plans_api):
        """Test that response contains expected plan attributes"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "name": "Q1 Release Plan",
                    "status": "active",
                    "calculationType": "timeBased",
                    "capacity": 100,
                    "isTemplate": False,
                    "startDate": "2024-01-01",
                    "dueDate": "2024-03-31"
                }
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify attributes
        attrs = response.json()['data']['attributes']
        assert attrs['name'] == 'Q1 Release Plan'
        assert attrs['status'] == 'active'
        assert attrs['calculationType'] == 'timeBased'
        assert attrs['capacity'] == 100
        assert attrs['isTemplate'] is False
    
    def test_get_plan_relationships(self, mock_plans_api):
        """Test that response contains proper relationships"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "relationships": {
                    "author": {
                        "data": {"type": "users", "id": "user1"}
                    },
                    "project": {
                        "data": {"type": "projects", "id": "MyProjectId"}
                    },
                    "workItems": {
                        "data": [
                            {"type": "workitems", "id": "MyProjectId/WI-1"},
                            {"type": "workitems", "id": "MyProjectId/WI-2"}
                        ],
                        "meta": {"totalCount": 2}
                    }
                }
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify relationships
        rels = response.json()['data']['relationships']
        assert 'author' in rels
        assert 'project' in rels
        assert 'workItems' in rels
        assert len(rels['workItems']['data']) == 2
        assert rels['workItems']['meta']['totalCount'] == 2
    
    def test_get_plan_with_revision(self, mock_plans_api):
        """Test get_plan with specific revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "revision": "5678"
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            revision='5678'
        )
        
        # Verify revision parameter
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '5678'
        assert response.json()['data']['revision'] == '5678'
    
    def test_get_plan_with_include(self, mock_plans_api):
        """Test get_plan with include parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"type": "plans", "id": "MyProjectId/MyPlanId"},
            "included": [
                {"type": "users", "id": "user1"},
                {"type": "projects", "id": "MyProjectId"}
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            include='author,project'
        )
        
        # Verify include parameter
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'author,project'
        assert len(response.json()['included']) == 2
    
    def test_get_plan_links(self, mock_plans_api):
        """Test that response contains proper links"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "links": {
                    "self": "server-host-name/application-path/projects/MyProjectId/plans/MyPlanId",
                    "portal": "server-host-name/application-path/polarion/redirect/project/MyProjectId/plan?id=MyPlanId"
                }
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify links
        links = response.json()['data']['links']
        assert 'self' in links
        assert 'portal' in links
        assert 'MyPlanId' in links['self']
    
    def test_get_plan_template(self, mock_plans_api):
        """Test retrieving a plan template"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/TemplateId",
                "attributes": {
                    "name": "Sprint Template",
                    "isTemplate": True
                }
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='TemplateId'
        )
        
        # Verify template flag
        assert response.json()['data']['attributes']['isTemplate'] is True
    
    def test_get_plan_url_structure(self, mock_plans_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan(
            project_id='TEST_PROJ',
            plan_id='TEST_PLAN'
        )
        
        # Verify URL structure
        call_args = mock_plans_api._session.get.call_args
        url = call_args[0][0]
        
        assert 'projects/TEST_PROJ' in url
        assert 'plans/TEST_PLAN' in url
        assert response.status_code == 200
    
    def test_get_plan_custom_fields_override(self, mock_plans_api):
        """Test that custom fields override default fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_plans_api._session.get.return_value = mock_response
        
        custom_fields = {
            'plans': 'name,status,dueDate'
        }
        
        response = mock_plans_api.get_plan(
            project_id='TEST_PROJECT',
            plan_id='TEST_PLAN',
            fields=custom_fields
        )
        
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        
        # Custom field should override
        assert params['fields[plans]'] == 'name,status,dueDate'
        
        # Other collections should still be @all
        assert params['fields[workitems]'] == '@all'
        assert params['fields[projects]'] == '@all'
    
    def test_get_plan_with_description(self, mock_plans_api):
        """Test plan with text description"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "name": "Release Plan",
                    "description": {
                        "type": "text/plain",
                        "value": "This is the Q1 release plan"
                    }
                }
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId'
        )
        
        # Verify description structure
        desc = response.json()['data']['attributes']['description']
        assert desc['type'] == 'text/plain'
        assert desc['value'] == 'This is the Q1 release plan'
    
    def test_get_plan_parent_relationship(self, mock_plans_api):
        """Test plan with parent relationship"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/SubPlan",
                "relationships": {
                    "parent": {
                        "data": {
                            "type": "plans",
                            "id": "MyProjectId/ParentPlan"
                        }
                    }
                }
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan(
            project_id='MyProjectId',
            plan_id='SubPlan'
        )
        
        # Verify parent relationship
        parent = response.json()['data']['relationships']['parent']['data']
        assert parent['type'] == 'plans'
        assert parent['id'] == 'MyProjectId/ParentPlan'
