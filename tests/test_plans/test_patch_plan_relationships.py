"""
Tests for Plans.patch_plan_relationships method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestPatchPlanRelationships:
    """Test suite for patch_plan_relationships method"""
    
    def test_patch_plan_relationships_success(self, mock_plans_api):
        """Test successful update of plan relationships"""
        # Mock response data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        # Request body based on example
        relationships_data = {
            "data": [
                {
                    "type": "MyResourceType",
                    "id": "MyProjectId/MyResourceId"
                }
            ]
        }
        
        # Call the method
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        # Verify the call
        mock_plans_api._session.patch.assert_called_once()
        call_args = mock_plans_api._session.patch.call_args
        
        # Check URL
        assert 'projects/MyProjectId/plans/MyPlanId/relationships/workItems' in call_args[0][0]
        
        # Check body was sent
        assert call_args[1]['json'] == relationships_data
        
        # Verify response
        assert response.status_code == 200
    
    def test_patch_plan_relationships_work_items(self, mock_plans_api):
        """Test updating work items relationship"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"},
                {"type": "workitems", "id": "MyProjectId/WI-2"},
                {"type": "workitems", "id": "MyProjectId/WI-3"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        # Verify body contains work items
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 3
        assert sent_data['data'][0]['type'] == 'workitems'
        assert response.status_code == 200
    
    def test_patch_plan_relationships_single_item(self, mock_plans_api):
        """Test updating relationship with single item"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-100"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 1
        assert sent_data['data'][0]['id'] == 'MyProjectId/WI-100'
        assert response.status_code == 200
    
    def test_patch_plan_relationships_empty_list(self, mock_plans_api):
        """Test updating relationship with empty list (removing all)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": []
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 0
        assert response.status_code == 200
    
    def test_patch_plan_relationships_project_span(self, mock_plans_api):
        """Test updating project span relationship"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {"type": "projects", "id": "Project1"},
                {"type": "projects", "id": "Project2"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='projectSpan',
            relationships_data=relationships_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data'][0]['type'] == 'projects'
        assert len(sent_data['data']) == 2
        assert response.status_code == 200
    
    def test_patch_plan_relationships_error_400(self, mock_plans_api):
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
        
        relationships_data = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
    
    def test_patch_plan_relationships_error_401(self, mock_plans_api):
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
        
        relationships_data = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
    
    def test_patch_plan_relationships_url_structure(self, mock_plans_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {"type": "workitems", "id": "TEST_PROJ/WI-1"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='TEST_PROJ',
            plan_id='TEST_PLAN',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        # Verify URL structure
        call_args = mock_plans_api._session.patch.call_args
        url = call_args[0][0]
        
        assert 'projects/TEST_PROJ' in url
        assert 'plans/TEST_PLAN' in url
        assert 'relationships/workItems' in url
        assert response.status_code == 200
    
    def test_patch_plan_relationships_multiple_work_items(self, mock_plans_api):
        """Test updating with multiple work items"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"},
                {"type": "workitems", "id": "MyProjectId/WI-2"},
                {"type": "workitems", "id": "MyProjectId/WI-3"},
                {"type": "workitems", "id": "MyProjectId/WI-4"},
                {"type": "workitems", "id": "MyProjectId/WI-5"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 5
        assert all(item['type'] == 'workitems' for item in sent_data['data'])
        assert response.status_code == 200
    
    def test_patch_plan_relationships_different_relationship_types(self, mock_plans_api):
        """Test patch_plan_relationships with different relationship IDs"""
        relationship_ids = ['workItems', 'parent', 'children', 'projectSpan']
        
        for rel_id in relationship_ids:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            
            mock_plans_api._session.patch.return_value = mock_response
            
            relationships_data = {
                "data": [
                    {"type": "MyResourceType", "id": f"MyProjectId/{rel_id}Id"}
                ]
            }
            
            response = mock_plans_api.patch_plan_relationships(
                project_id='MyProjectId',
                plan_id='MyPlanId',
                relationship_id=rel_id,
                relationships_data=relationships_data
            )
            
            # Verify URL contains correct relationship ID
            call_args = mock_plans_api._session.patch.call_args
            url = call_args[0][0]
            assert f'relationships/{rel_id}' in url
            assert response.status_code == 200
    
    def test_patch_plan_relationships_json_payload_format(self, mock_plans_api):
        """Test that JSON payload is sent correctly"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        # Verify json parameter was used
        call_args = mock_plans_api._session.patch.call_args
        assert 'json' in call_args[1]
        assert call_args[1]['json'] == relationships_data
        assert response.status_code == 200
    
    def test_patch_plan_relationships_with_revisions(self, mock_plans_api):
        """Test updating relationships with revision information"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1", "revision": "1234"},
                {"type": "workitems", "id": "MyProjectId/WI-2", "revision": "1235"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data'][0]['revision'] == '1234'
        assert sent_data['data'][1]['revision'] == '1235'
        assert response.status_code == 200
    
    def test_patch_plan_relationships_replace_all(self, mock_plans_api):
        """Test replacing all relationships with new set"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        # New set of work items to replace existing ones
        relationships_data = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/NEW-1"},
                {"type": "workitems", "id": "MyProjectId/NEW-2"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert 'NEW-1' in sent_data['data'][0]['id']
        assert 'NEW-2' in sent_data['data'][1]['id']
        assert response.status_code == 200
    
    def test_patch_plan_relationships_parent_relationship(self, mock_plans_api):
        """Test updating parent relationship"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {"type": "plans", "id": "MyProjectId/ParentPlan"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='parent',
            relationships_data=relationships_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data'][0]['type'] == 'plans'
        assert 'ParentPlan' in sent_data['data'][0]['id']
        assert response.status_code == 200
    
    def test_patch_plan_relationships_children_relationship(self, mock_plans_api):
        """Test updating children relationship"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {"type": "plans", "id": "MyProjectId/ChildPlan1"},
                {"type": "plans", "id": "MyProjectId/ChildPlan2"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='children',
            relationships_data=relationships_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 2
        assert all(item['type'] == 'plans' for item in sent_data['data'])
        assert response.status_code == 200
    
    def test_patch_plan_relationships_large_batch(self, mock_plans_api):
        """Test updating relationships with large batch of items"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        # Create a large batch of work items
        work_items = [
            {"type": "workitems", "id": f"MyProjectId/WI-{i}"}
            for i in range(1, 51)
        ]
        
        relationships_data = {
            "data": work_items
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 50
        assert response.status_code == 200
    
    def test_patch_plan_relationships_data_structure(self, mock_plans_api):
        """Test that data structure follows expected format"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": "MyProjectId/MyWorkItemId"
                }
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        
        # Verify structure
        assert 'data' in sent_data
        assert isinstance(sent_data['data'], list)
        assert 'type' in sent_data['data'][0]
        assert 'id' in sent_data['data'][0]
        assert response.status_code == 200
    
    def test_patch_plan_relationships_mixed_resource_types(self, mock_plans_api):
        """Test that each relationship maintains consistent type"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        
        mock_plans_api._session.patch.return_value = mock_response
        
        # All items should be same type for a relationship
        relationships_data = {
            "data": [
                {"type": "workitems", "id": "MyProjectId/WI-1"},
                {"type": "workitems", "id": "MyProjectId/WI-2"},
                {"type": "workitems", "id": "MyProjectId/WI-3"}
            ]
        }
        
        response = mock_plans_api.patch_plan_relationships(
            project_id='MyProjectId',
            plan_id='MyPlanId',
            relationship_id='workItems',
            relationships_data=relationships_data
        )
        
        call_args = mock_plans_api._session.patch.call_args
        sent_data = call_args[1]['json']
        
        # All should have same type
        types = [item['type'] for item in sent_data['data']]
        assert len(set(types)) == 1  # Only one unique type
        assert types[0] == 'workitems'
        assert response.status_code == 200
