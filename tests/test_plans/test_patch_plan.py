"""
Tests for Plans.patch_plan method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestPatchPlan:
    """Test suite for patch_plan method"""
    
    def test_patch_plan_success(self, mock_plans_api):
        """Test successful update of a plan"""
        # Mock response data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        # Request body based on example
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
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
        }
        
        # Call the method
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        # Verify the call
        mock_plans_api._session.patch.assert_called_once()
        call_args = mock_plans_api._session.patch.call_args
        
        # Check URL
        assert 'projects/MyProjectId/plans/MyPlanId' in call_args[0][0]
        
        # Check body was sent
        assert call_args[1]['json'] == plan_data
        
        # Verify response
        assert response.status_code == 200
    
    def test_patch_plan_update_name(self, mock_plans_api):
        """Test updating plan name"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "name": "Updated Plan Name"
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        # Verify body contains updated name
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data']['attributes']['name'] == 'Updated Plan Name'
        assert response.status_code == 200
    
    def test_patch_plan_update_status(self, mock_plans_api):
        """Test updating plan status"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "status": "active"
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data']['attributes']['status'] == 'active'
        assert response.status_code == 200
    
    def test_patch_plan_update_dates(self, mock_plans_api):
        """Test updating plan dates"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "startDate": "2024-01-01",
                    "dueDate": "2024-12-31"
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data']['attributes']['startDate'] == '2024-01-01'
        assert sent_data['data']['attributes']['dueDate'] == '2024-12-31'
        assert response.status_code == 200
    
    def test_patch_plan_update_description(self, mock_plans_api):
        """Test updating plan description"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "description": {
                        "type": "text/plain",
                        "value": "Updated plan description"
                    }
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        desc = sent_data['data']['attributes']['description']
        assert desc['type'] == 'text/plain'
        assert desc['value'] == 'Updated plan description'
        assert response.status_code == 200
    
    def test_patch_plan_update_capacity(self, mock_plans_api):
        """Test updating plan capacity"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "capacity": 100,
                    "calculationType": "timeBased"
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data']['attributes']['capacity'] == 100
        assert sent_data['data']['attributes']['calculationType'] == 'timeBased'
        assert response.status_code == 200
    
    def test_patch_plan_update_relationships(self, mock_plans_api):
        """Test updating plan relationships"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
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
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        parent = sent_data['data']['relationships']['parent']['data']
        assert parent['type'] == 'plans'
        assert parent['id'] == 'MyProjectId/ParentPlan'
        assert response.status_code == 200
    
    def test_patch_plan_update_work_items(self, mock_plans_api):
        """Test updating plan work items relationship"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "relationships": {
                    "workItems": {
                        "data": [
                            {"type": "workitems", "id": "MyProjectId/WI-1"},
                            {"type": "workitems", "id": "MyProjectId/WI-2"}
                        ]
                    }
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        work_items = sent_data['data']['relationships']['workItems']['data']
        assert len(work_items) == 2
        assert work_items[0]['id'] == 'MyProjectId/WI-1'
        assert response.status_code == 200
    
    def test_patch_plan_error_400(self, mock_plans_api):
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
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "name": "Test"
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
    
    def test_patch_plan_error_401(self, mock_plans_api):
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
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "name": "Test"
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
    
    def test_patch_plan_url_structure(self, mock_plans_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "TEST_PROJ/TEST_PLAN",
                "attributes": {"name": "Test"}
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='TEST_PROJ',
            plan_id='TEST_PLAN',
            plan_data=plan_data
        )
        
        # Verify URL structure
        call_args = mock_plans_api._session.patch.call_args
        url = call_args[0][0]
        
        assert 'projects/TEST_PROJ' in url
        assert 'plans/TEST_PLAN' in url
        assert response.status_code == 200
    
    def test_patch_plan_update_home_page_content(self, mock_plans_api):
        """Test updating plan home page content"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "homePageContent": {
                        "type": "text/html",
                        "value": "<h1>Updated Home Page</h1>"
                    }
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        content = sent_data['data']['attributes']['homePageContent']
        assert content['type'] == 'text/html'
        assert '<h1>Updated Home Page</h1>' in content['value']
        assert response.status_code == 200
    
    def test_patch_plan_update_color(self, mock_plans_api):
        """Test updating plan color"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "color": "#FF5733"
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data']['attributes']['color'] == '#FF5733'
        assert response.status_code == 200
    
    def test_patch_plan_update_template_flag(self, mock_plans_api):
        """Test updating plan template flag"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "isTemplate": False
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data']['attributes']['isTemplate'] is False
        assert response.status_code == 200
    
    def test_patch_plan_update_sort_order(self, mock_plans_api):
        """Test updating plan sort order"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "sortOrder": 5
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data']['attributes']['sortOrder'] == 5
        assert response.status_code == 200
    
    def test_patch_plan_update_allowed_types(self, mock_plans_api):
        """Test updating plan allowed types"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "allowedTypes": ["task", "defect", "requirement"]
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        allowed_types = sent_data['data']['attributes']['allowedTypes']
        assert len(allowed_types) == 3
        assert 'task' in allowed_types
        assert 'defect' in allowed_types
        assert response.status_code == 200
    
    def test_patch_plan_update_estimation_fields(self, mock_plans_api):
        """Test updating plan estimation fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "estimationField": "timePoint",
                    "defaultEstimate": 5,
                    "previousTimeSpent": "10d"
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        attrs = sent_data['data']['attributes']
        assert attrs['estimationField'] == 'timePoint'
        assert attrs['defaultEstimate'] == 5
        assert attrs['previousTimeSpent'] == '10d'
        assert response.status_code == 200
    
    def test_patch_plan_update_project_span(self, mock_plans_api):
        """Test updating plan project span"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "relationships": {
                    "projectSpan": {
                        "data": [
                            {"type": "projects", "id": "Project1"},
                            {"type": "projects", "id": "Project2"}
                        ]
                    }
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        project_span = sent_data['data']['relationships']['projectSpan']['data']
        assert len(project_span) == 2
        assert project_span[0]['id'] == 'Project1'
        assert response.status_code == 200
    
    def test_patch_plan_multiple_attributes(self, mock_plans_api):
        """Test updating multiple plan attributes at once"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "name": "Q2 Release Plan",
                    "status": "in_progress",
                    "startDate": "2024-04-01",
                    "dueDate": "2024-06-30",
                    "capacity": 200
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        attrs = sent_data['data']['attributes']
        
        assert attrs['name'] == 'Q2 Release Plan'
        assert attrs['status'] == 'in_progress'
        assert attrs['startDate'] == '2024-04-01'
        assert attrs['dueDate'] == '2024-06-30'
        assert attrs['capacity'] == 200
        assert response.status_code == 200
    
    def test_patch_plan_json_payload_format(self, mock_plans_api):
        """Test that JSON payload is sent correctly"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        plan_data = {
            "data": {
                "type": "plans",
                "id": "MyProjectId/MyPlanId",
                "attributes": {
                    "name": "Test Plan"
                }
            }
        }
        
        response = mock_plans_api.patch_plan(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            plan_data=plan_data
        )
        
        # Verify json parameter was used
        call_args = mock_plans_api._session.patch.call_args
        assert 'json' in call_args[1]
        assert call_args[1]['json'] == plan_data
        assert response.status_code == 200
