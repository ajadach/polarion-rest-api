"""
Tests for Plans.get_plan_relationship method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetPlanRelationship:
    """Test suite for get_plan_relationship method"""
    
    def test_get_plan_relationship_success(self, mock_plans_api):
        """Test successful retrieval of plan relationships"""
        # Mock response data based on example
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "MyResourceType",
                    "id": "MyProjectId/MyResourceId"
                }
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='parent'
        )
        
        # Verify the call
        mock_plans_api._session.get.assert_called_once()
        call_args = mock_plans_api._session.get.call_args
        
        # Check URL
        assert 'projects/MyProjectId/plans/MyPlanId/relationships/parent' in call_args[0][0]
        
        # Verify response
        assert response.status_code == 200
        assert len(response.json()['data']) == 1
        assert response.json()['data'][0]['type'] == 'MyResourceType'
        assert response.json()['data'][0]['id'] == 'MyProjectId/MyResourceId'
    
    def test_get_plan_relationship_with_pagination(self, mock_plans_api):
        """Test get_plan_relationship with pagination parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"},
                {"type": "workitems", "id": "MyProjectId/WI-2"}
            ],
            "meta": {
                "totalCount": 50
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        # Call with pagination
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            page_size=123,
            page_number=465
        )
        
        # Verify pagination parameters
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        
        assert params['page[size]'] == 123
        assert params['page[number]'] == 465
        assert response.status_code == 200
    
    def test_get_plan_relationship_with_all_parameters(self, mock_plans_api):
        """Test get_plan_relationship with all optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"}
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        # Call with all parameters
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            page_size=50,
            page_number=2,
            fields={'workitems': 'title,status'},
            include='assignee,author',
            revision='1234'
        )
        
        # Verify the call
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom fields override default
        assert 'fields[workitems]' in params
        assert params['fields[workitems]'] == 'title,status'
        
        # Verify other parameters
        assert params['page[size]'] == 50
        assert params['page[number]'] == 2
        assert params['include'] == 'assignee,author'
        assert params['revision'] == '1234'
        
        assert response.status_code == 200
    
    def test_get_plan_relationship_default_fields_applied(self, mock_plans_api):
        """Test that default fields are properly applied when no custom fields provided"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        mock_plans_api._session.get.return_value = mock_response
        
        # Call without fields parameter
        response = mock_plans_api.get_plan_relationship(
            project_id='TEST_PROJECT',
            plan_id='TEST_PLAN',
            relationship_id='workItems'
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
    
    def test_get_plan_relationship_error_400(self, mock_plans_api):
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
        
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems'
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
    
    def test_get_plan_relationship_error_401(self, mock_plans_api):
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
        
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems'
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
    
    def test_get_plan_relationship_work_items(self, mock_plans_api):
        """Test retrieving work items relationship"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/WI-1",
                    "revision": "1234"
                },
                {
                    "type": "workitems",
                    "id": "MyProjectId/WI-2",
                    "revision": "1235"
                }
            ],
            "meta": {
                "totalCount": 2
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems'
        )
        
        # Verify response
        data = response.json()['data']
        assert len(data) == 2
        assert data[0]['type'] == 'workitems'
        assert data[1]['type'] == 'workitems'
        assert response.json()['meta']['totalCount'] == 2
    
    def test_get_plan_relationship_url_structure(self, mock_plans_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan_relationship(
            project_id='TEST_PROJ',
            plan_id='TEST_PLAN',
            relationship_id='parent'
        )
        
        # Verify URL structure
        call_args = mock_plans_api._session.get.call_args
        url = call_args[0][0]
        
        assert 'projects/TEST_PROJ' in url
        assert 'plans/TEST_PLAN' in url
        assert 'relationships/parent' in url
        assert response.status_code == 200
    
    def test_get_plan_relationship_with_revision(self, mock_plans_api):
        """Test get_plan_relationship with specific revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/WI-1",
                    "revision": "5678"
                }
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            revision='5678'
        )
        
        # Verify revision parameter
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '5678'
        assert response.json()['data'][0]['revision'] == '5678'
    
    def test_get_plan_relationship_with_include(self, mock_plans_api):
        """Test get_plan_relationship with include parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"}
            ],
            "included": [
                {"type": "users", "id": "user1"},
                {"type": "projects", "id": "MyProjectId"}
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            include='assignee,author'
        )
        
        # Verify include parameter
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'assignee,author'
        assert len(response.json()['included']) == 2
    
    def test_get_plan_relationship_custom_fields_override(self, mock_plans_api):
        """Test that custom fields override default fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        mock_plans_api._session.get.return_value = mock_response
        
        custom_fields = {
            'workitems': 'title,status,priority'
        }
        
        response = mock_plans_api.get_plan_relationship(
            project_id='TEST_PROJECT',
            plan_id='TEST_PLAN',
            relationship_id='workItems',
            fields=custom_fields
        )
        
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        
        # Custom field should override
        assert params['fields[workitems]'] == 'title,status,priority'
        
        # Other collections should still be @all
        assert params['fields[plans]'] == '@all'
        assert params['fields[projects]'] == '@all'
    
    def test_get_plan_relationship_empty_result(self, mock_plans_api):
        """Test get_plan_relationship with empty result"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [],
            "meta": {
                "totalCount": 0
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems'
        )
        
        # Verify empty result
        assert response.status_code == 200
        assert len(response.json()['data']) == 0
        assert response.json()['meta']['totalCount'] == 0
    
    def test_get_plan_relationship_pagination_first_page(self, mock_plans_api):
        """Test get_plan_relationship with first page"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"},
                {"type": "workitems", "id": "MyProjectId/WI-2"}
            ],
            "meta": {
                "totalCount": 10
            },
            "links": {
                "next": "server-host-name/application-path/projects/MyProjectId/plans/MyPlanId/relationships/workItems?page[number]=2"
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            page_size=2,
            page_number=1
        )
        
        # Verify pagination
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 2
        assert params['page[number]'] == 1
        
        # Verify response has next link
        assert 'next' in response.json()['links']
    
    def test_get_plan_relationship_multiple_resources(self, mock_plans_api):
        """Test get_plan_relationship returning multiple resource types"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"},
                {"type": "workitems", "id": "MyProjectId/WI-2"},
                {"type": "workitems", "id": "MyProjectId/WI-3"}
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems'
        )
        
        # Verify multiple items
        data = response.json()['data']
        assert len(data) == 3
        assert all(item['type'] == 'workitems' for item in data)
    
    def test_get_plan_relationship_different_relationship_types(self, mock_plans_api):
        """Test get_plan_relationship with different relationship IDs"""
        relationship_ids = ['workItems', 'parent', 'children', 'projectSpan']
        
        for rel_id in relationship_ids:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "data": [
                    {"type": "MyResourceType", "id": f"MyProjectId/{rel_id}Id"}
                ]
            }
            
            mock_plans_api._session.get.return_value = mock_response
            
            response = mock_plans_api.get_plan_relationship(
                project_id='MyProjectId',
                plan_id='MyPlanId',
                relationship_id=rel_id
            )
            
            # Verify URL contains correct relationship ID
            call_args = mock_plans_api._session.get.call_args
            url = call_args[0][0]
            assert f'relationships/{rel_id}' in url
            assert response.status_code == 200
    
    def test_get_plan_relationship_minimal_parameters(self, mock_plans_api):
        """Test get_plan_relationship with only required parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"}
            ]
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        # Call with only required parameters
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems'
        )
        
        # Verify call was made
        mock_plans_api._session.get.assert_called_once()
        
        # Verify only default fields are in params
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        
        # Should have default fields but no pagination, include, or revision
        assert 'page[size]' not in params
        assert 'page[number]' not in params
        assert 'include' not in params
        assert 'revision' not in params
        
        assert response.status_code == 200
    
    def test_get_plan_relationship_large_page_size(self, mock_plans_api):
        """Test get_plan_relationship with large page size"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"type": "workitems", "id": f"MyProjectId/WI-{i}"} for i in range(1, 101)],
            "meta": {
                "totalCount": 100
            }
        }
        
        mock_plans_api._session.get.return_value = mock_response
        
        response = mock_plans_api.get_plan_relationship(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            page_size=100
        )
        
        # Verify large page size
        call_args = mock_plans_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 100
        
        # Verify response contains all items
        assert len(response.json()['data']) == 100
