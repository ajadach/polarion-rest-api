"""
Pytest tests for patch_work_item_relationships method.

Tests the patch_work_item_relationships method from WorkItems class.
Uses mocks to avoid making real API calls.

Run with:
    pytest test_patch_work_item_relationships.py -v
"""
import pytest
from unittest.mock import Mock


class TestPatchWorkItemRelationshipsMocked:
    """Unit tests for patch_work_item_relationships method using mocks"""
    
    def test_patch_work_item_relationships_success(self, mock_work_items_api, test_params):
        """Test successful update of work item relationships"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/WI-002"
                }
            ]
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/WI-002"
                }
            ]
        }
        
        response = mock_work_items_api.patch_work_item_relationships(
            test_params['project_id'],
            "WI-001",
            "parent",
            relationships_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        mock_work_items_api._session.patch.assert_called_once()
        print("\n✓ Mock: Work item relationships updated successfully")
    
    def test_patch_work_item_relationships_parent(self, mock_work_items_api, test_params):
        """Test update parent relationship"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/PARENT-001"
                }
            ]
        }
        
        response = mock_work_items_api.patch_work_item_relationships(
            test_params['project_id'],
            "WI-001",
            "parent",
            relationships_data
        )
        
        assert response.status_code == 200
        call_args = mock_work_items_api._session.patch.call_args
        assert 'parent' in call_args[0][0]
        print("\n✓ Mock: Parent relationship updated successfully")
    
    def test_patch_work_item_relationships_child(self, mock_work_items_api, test_params):
        """Test update child relationship"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/CHILD-001"
                }
            ]
        }
        
        response = mock_work_items_api.patch_work_item_relationships(
            test_params['project_id'],
            "WI-001",
            "child",
            relationships_data
        )
        
        assert response.status_code == 200
        call_args = mock_work_items_api._session.patch.call_args
        assert 'child' in call_args[0][0]
        print("\n✓ Mock: Child relationship updated successfully")
    
    def test_patch_work_item_relationships_relates_to(self, mock_work_items_api, test_params):
        """Test update relates_to relationship"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/RELATED-001"
                }
            ]
        }
        
        response = mock_work_items_api.patch_work_item_relationships(
            test_params['project_id'],
            "WI-001",
            "relates_to",
            relationships_data
        )
        
        assert response.status_code == 200
        call_args = mock_work_items_api._session.patch.call_args
        assert 'relates_to' in call_args[0][0]
        print("\n✓ Mock: Relates_to relationship updated successfully")
    
    def test_patch_work_item_relationships_multiple(self, mock_work_items_api, test_params):
        """Test update multiple relationships at once"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "workitems", "id": f"{test_params['project_id']}/WI-002"},
                {"type": "workitems", "id": f"{test_params['project_id']}/WI-003"}
            ]
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/WI-002"
                },
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/WI-003"
                }
            ]
        }
        
        response = mock_work_items_api.patch_work_item_relationships(
            test_params['project_id'],
            "WI-001",
            "child",
            relationships_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data['data']) == 2
        print("\n✓ Mock: Multiple relationships updated successfully")
    
    def test_patch_work_item_relationships_not_found(self, mock_work_items_api, test_params):
        """Test patch with non-existent work item (404 Not Found)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Work item not found"
                }
            ]
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/WI-002"
                }
            ]
        }
        
        response = mock_work_items_api.patch_work_item_relationships(
            test_params['project_id'],
            "NONEXISTENT",
            "parent",
            relationships_data
        )
        
        assert response.status_code == 404
        errors = response.json()['errors']
        assert errors[0]['title'] == 'Not Found'
        print("\n✓ Mock: Not found error handled correctly")
    
    def test_patch_work_item_relationships_unauthorized(self, mock_work_items_api, test_params):
        """Test patch with invalid authentication (401 Unauthorized)"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "Invalid or missing authentication token"
                }
            ]
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/WI-002"
                }
            ]
        }
        
        response = mock_work_items_api.patch_work_item_relationships(
            test_params['project_id'],
            "WI-001",
            "parent",
            relationships_data
        )
        
        assert response.status_code == 401
        errors = response.json()['errors']
        assert errors[0]['title'] == 'Unauthorized'
        print("\n✓ Mock: Unauthorized error handled correctly")
    
    def test_patch_work_item_relationships_validation_error(self, mock_work_items_api, test_params):
        """Test patch with invalid data (400 Bad Request)"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Invalid relationship data"
                }
            ]
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        relationships_data = {
            "data": [
                {
                    "type": "workitems"
                    # Missing 'id' field
                }
            ]
        }
        
        response = mock_work_items_api.patch_work_item_relationships(
            test_params['project_id'],
            "WI-001",
            "parent",
            relationships_data
        )
        
        assert response.status_code == 400
        errors = response.json()['errors']
        assert errors[0]['title'] == 'Bad Request'
        print("\n✓ Mock: Validation error handled correctly")
    
    def test_patch_work_item_relationships_circular_dependency(self, mock_work_items_api, test_params):
        """Test patch with circular dependency (400 Bad Request)"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Circular dependency detected"
                }
            ]
        }
        mock_work_items_api._session.patch.return_value = mock_response
        
        # Try to make a work item its own parent
        relationships_data = {
            "data": [
                {
                    "type": "workitems",
                    "id": f"{test_params['project_id']}/WI-001"
                }
            ]
        }
        
        response = mock_work_items_api.patch_work_item_relationships(
            test_params['project_id'],
            "WI-001",
            "parent",
            relationships_data
        )
        
        assert response.status_code == 400
        errors = response.json()['errors']
        assert 'Circular dependency' in errors[0]['detail']
        print("\n✓ Mock: Circular dependency error handled correctly")
