"""
Tests for Plans.post_plans method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestPostPlans:
    """Test suite for post_plans method"""
    
    def test_post_plans_success(self, mock_plans_api):
        """Test successful creation of plans"""
        # Mock response data based on example
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId",
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/plans/MyPlanId?revision=1234",
                        "portal": "server-host-name/application-path/polarion/redirect/project/MyProjectId/plan?id=MyPlanId&revision=1234"
                    }
                }
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        # Request body based on example
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "allowedTypes": ["optionId"],
                        "calculationType": "timeBased",
                        "capacity": 0,
                        "color": "Color",
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
                        "useReportFromTemplate": True
                    },
                    "relationships": {
                        "parent": {
                            "data": {
                                "type": "plans",
                                "id": "MyProjectId/MyPlanId"
                            }
                        },
                        "projectSpan": {
                            "data": [
                                {
                                    "type": "projects",
                                    "id": "MyProjectId"
                                }
                            ]
                        },
                        "template": {
                            "data": {
                                "type": "plans",
                                "id": "MyProjectId/MyPlanId"
                            }
                        },
                        "workItems": {
                            "data": [
                                {
                                    "type": "workitems",
                                    "id": "MyProjectId/MyWorkItemId"
                                }
                            ]
                        }
                    }
                }
            ]
        }
        
        # Call the method
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify the call
        mock_plans_api._session.post.assert_called_once()
        call_args = mock_plans_api._session.post.call_args
        
        # Check URL
        assert 'projects/MyProjectId/plans' in call_args[0][0]
        
        # Check body was sent
        assert call_args[1]['json'] == plans_data
        
        # Verify response
        assert response.status_code == 201
        assert len(response.json()['data']) == 1
        assert response.json()['data'][0]['type'] == 'plans'
        assert response.json()['data'][0]['id'] == 'MyProjectId/MyPlanId'
    
    def test_post_plans_single_plan(self, mock_plans_api):
        """Test creating a single plan"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/NewPlan",
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/plans/NewPlan"
                    }
                }
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "name": "Q1 Release Plan",
                        "startDate": "2024-01-01",
                        "dueDate": "2024-03-31"
                    }
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify body
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 1
        assert sent_data['data'][0]['attributes']['name'] == 'Q1 Release Plan'
        assert response.status_code == 201
    
    def test_post_plans_multiple_plans(self, mock_plans_api):
        """Test creating multiple plans at once"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "plans", "id": "MyProjectId/Plan1"},
                {"type": "plans", "id": "MyProjectId/Plan2"},
                {"type": "plans", "id": "MyProjectId/Plan3"}
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {"type": "plans", "attributes": {"name": "Plan 1"}},
                {"type": "plans", "attributes": {"name": "Plan 2"}},
                {"type": "plans", "attributes": {"name": "Plan 3"}}
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify multiple plans were sent
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 3
        
        # Verify response
        assert len(response.json()['data']) == 3
        assert response.status_code == 201
    
    def test_post_plans_with_template(self, mock_plans_api):
        """Test creating a plan template"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "plans", "id": "MyProjectId/TemplateId"}
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "name": "Sprint Template",
                        "isTemplate": True
                    }
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data'][0]['attributes']['isTemplate'] is True
        assert response.status_code == 201
    
    def test_post_plans_with_relationships(self, mock_plans_api):
        """Test creating plan with relationships"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "plans", "id": "MyProjectId/NewPlan"}
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "name": "Child Plan"
                    },
                    "relationships": {
                        "parent": {
                            "data": {
                                "type": "plans",
                                "id": "MyProjectId/ParentPlan"
                            }
                        },
                        "workItems": {
                            "data": [
                                {"type": "workitems", "id": "MyProjectId/WI-1"},
                                {"type": "workitems", "id": "MyProjectId/WI-2"}
                            ]
                        }
                    }
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        assert 'relationships' in sent_data['data'][0]
        assert 'parent' in sent_data['data'][0]['relationships']
        assert 'workItems' in sent_data['data'][0]['relationships']
        assert response.status_code == 201
    
    def test_post_plans_with_description(self, mock_plans_api):
        """Test creating plan with description"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "plans", "id": "MyProjectId/NewPlan"}
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "name": "New Plan",
                        "description": {
                            "type": "text/plain",
                            "value": "This is a new plan"
                        }
                    }
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        desc = sent_data['data'][0]['attributes']['description']
        assert desc['type'] == 'text/plain'
        assert desc['value'] == 'This is a new plan'
        assert response.status_code == 201
    
    def test_post_plans_with_dates(self, mock_plans_api):
        """Test creating plan with dates"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "plans", "id": "MyProjectId/NewPlan"}
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "name": "Q2 Plan",
                        "startDate": "2024-04-01",
                        "dueDate": "2024-06-30"
                    }
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        attrs = sent_data['data'][0]['attributes']
        assert attrs['startDate'] == '2024-04-01'
        assert attrs['dueDate'] == '2024-06-30'
        assert response.status_code == 201
    
    def test_post_plans_with_capacity(self, mock_plans_api):
        """Test creating plan with capacity settings"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "plans", "id": "MyProjectId/NewPlan"}
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "name": "Sprint 1",
                        "capacity": 100,
                        "calculationType": "timeBased",
                        "defaultEstimate": 5
                    }
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        attrs = sent_data['data'][0]['attributes']
        assert attrs['capacity'] == 100
        assert attrs['calculationType'] == 'timeBased'
        assert attrs['defaultEstimate'] == 5
        assert response.status_code == 201
    
    def test_post_plans_error_400(self, mock_plans_api):
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
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {"name": "Test"}
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
    
    def test_post_plans_error_401(self, mock_plans_api):
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
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {"name": "Test"}
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
    
    def test_post_plans_url_structure(self, mock_plans_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {"type": "plans", "attributes": {"name": "Test"}}
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='TEST_PROJ',
            plans_data=plans_data
        )
        
        # Verify URL structure
        call_args = mock_plans_api._session.post.call_args
        url = call_args[0][0]
        
        assert 'projects/TEST_PROJ/plans' in url
        assert response.status_code == 201
    
    def test_post_plans_with_home_page_content(self, mock_plans_api):
        """Test creating plan with home page content"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "plans", "id": "MyProjectId/NewPlan"}
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "name": "New Plan",
                        "homePageContent": {
                            "type": "text/html",
                            "value": "<h1>Welcome to the Plan</h1>"
                        }
                    }
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        content = sent_data['data'][0]['attributes']['homePageContent']
        assert content['type'] == 'text/html'
        assert '<h1>Welcome to the Plan</h1>' in content['value']
        assert response.status_code == 201
    
    def test_post_plans_with_color(self, mock_plans_api):
        """Test creating plan with color"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "plans", "id": "MyProjectId/NewPlan"}
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "name": "New Plan",
                        "color": "#FF5733"
                    }
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data'][0]['attributes']['color'] == '#FF5733'
        assert response.status_code == 201
    
    def test_post_plans_with_allowed_types(self, mock_plans_api):
        """Test creating plan with allowed work item types"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "plans", "id": "MyProjectId/NewPlan"}
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "name": "New Plan",
                        "allowedTypes": ["task", "defect", "requirement"]
                    }
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        allowed_types = sent_data['data'][0]['attributes']['allowedTypes']
        assert len(allowed_types) == 3
        assert 'task' in allowed_types
        assert response.status_code == 201
    
    def test_post_plans_with_project_span(self, mock_plans_api):
        """Test creating plan with project span"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "plans", "id": "MyProjectId/NewPlan"}
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "name": "Cross-Project Plan"
                    },
                    "relationships": {
                        "projectSpan": {
                            "data": [
                                {"type": "projects", "id": "Project1"},
                                {"type": "projects", "id": "Project2"}
                            ]
                        }
                    }
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        project_span = sent_data['data'][0]['relationships']['projectSpan']['data']
        assert len(project_span) == 2
        assert response.status_code == 201
    
    def test_post_plans_response_links(self, mock_plans_api):
        """Test that response contains proper links"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "plans",
                    "id": "MyProjectId/MyPlanId",
                    "links": {
                        "self": "server-host-name/application-path/projects/MyProjectId/plans/MyPlanId?revision=1234",
                        "portal": "server-host-name/application-path/polarion/redirect/project/MyProjectId/plan?id=MyPlanId&revision=1234"
                    }
                }
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {"type": "plans", "attributes": {"name": "Test"}}
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify response links
        links = response.json()['data'][0]['links']
        assert 'self' in links
        assert 'portal' in links
        assert 'MyPlanId' in links['self']
    
    def test_post_plans_json_payload_format(self, mock_plans_api):
        """Test that JSON payload is sent correctly"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {"type": "plans", "attributes": {"name": "Test"}}
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        # Verify json parameter was used
        call_args = mock_plans_api._session.post.call_args
        assert 'json' in call_args[1]
        assert call_args[1]['json'] == plans_data
        assert response.status_code == 201
    
    def test_post_plans_data_array_structure(self, mock_plans_api):
        """Test that data is sent as array"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": []}
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {"type": "plans", "attributes": {"name": "Plan 1"}},
                {"type": "plans", "attributes": {"name": "Plan 2"}}
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        
        # Verify structure
        assert 'data' in sent_data
        assert isinstance(sent_data['data'], list)
        assert len(sent_data['data']) == 2
        assert response.status_code == 201
    
    def test_post_plans_with_estimation_fields(self, mock_plans_api):
        """Test creating plan with estimation fields"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "plans", "id": "MyProjectId/NewPlan"}
            ]
        }
        
        mock_plans_api._session.post.return_value = mock_response
        
        plans_data = {
            "data": [
                {
                    "type": "plans",
                    "attributes": {
                        "name": "Sprint Plan",
                        "estimationField": "timePoint",
                        "prioritizationField": "priority"
                    }
                }
            ]
        }
        
        response = mock_plans_api.post_plans(
            project_id='MyProjectId',
            plans_data=plans_data
        )
        
        call_args = mock_plans_api._session.post.call_args
        sent_data = call_args[1]['json']
        attrs = sent_data['data'][0]['attributes']
        assert attrs['estimationField'] == 'timePoint'
        assert attrs['prioritizationField'] == 'priority'
        assert response.status_code == 201
