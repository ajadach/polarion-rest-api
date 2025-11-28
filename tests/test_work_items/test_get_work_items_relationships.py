"""
Pytest tests for get_work_items_relationships method.

Run with:
    pytest test_get_work_items_relationships.py -v
"""
import pytest
from unittest.mock import Mock


class TestGetWorkItemsRelationshipsMocked:
    """Unit tests for get_work_items_relationships method"""
    
    def test_get_work_items_relationships_success(self, mock_work_items_api, test_params):
        """Test successful retrieval of work item relationships"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "workitems", "id": f"{test_params['project_id']}/WI-002"},
                {"type": "workitems", "id": f"{test_params['project_id']}/WI-003"}
            ]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_items_relationships(
            test_params['project_id'],
            "WI-001",
            "parent"
        )
        
        assert response.status_code == 200
        assert len(response.json()['data']) == 2
        print("\n✓ Mock: Work item relationships retrieved successfully")
    
    def test_get_work_items_relationships_with_pagination(self, mock_work_items_api, test_params):
        """Test get work item relationships with pagination"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_items_relationships(
            test_params['project_id'],
            "WI-001",
            "child",
            page_size=10,
            page_number=1
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['page[size]'] == 10
        assert params['page[number]'] == 1
        print("\n✓ Mock: Pagination handled correctly")
    
    def test_get_work_items_relationships_with_revision(self, mock_work_items_api, test_params):
        """Test get work item relationships with revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_items_relationships(
            test_params['project_id'],
            "WI-001",
            "relates_to",
            revision="12345"
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['revision'] == "12345"
        print("\n✓ Mock: Revision parameter handled correctly")
    
    def test_get_work_items_relationships_different_types(self, mock_work_items_api, test_params):
        """Test get work item relationships for different relationship types"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        relationship_types = ["parent", "child", "relates_to", "duplicates", "blocks"]
        
        for rel_type in relationship_types:
            response = mock_work_items_api.get_work_items_relationships(
                test_params['project_id'],
                "WI-001",
                rel_type
            )
            assert response.status_code == 200
        
        print("\n✓ Mock: Different relationship types handled correctly")
    
    def test_get_work_items_relationships_not_found(self, mock_work_items_api, test_params):
        """Test get work item relationships for non-existent work item"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{"status": "404", "title": "Not Found"}]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_items_relationships(
            test_params['project_id'],
            "NonExistent",
            "parent"
        )
        
        assert response.status_code == 404
        print("\n✓ Mock: Not found (404) handled correctly")
    
    def test_get_work_items_relationships_all_parameters(self, mock_work_items_api, test_params):
        """Test get work item relationships with all parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        response = mock_work_items_api.get_work_items_relationships(
            test_params['project_id'],
            "WI-001",
            "parent",
            page_size=5,
            page_number=2,
            revision="999"
        )
        
        assert response.status_code == 200
        params = mock_work_items_api._session.get.call_args[1]['params']
        assert params['page[size]'] == 5
        assert params['page[number]'] == 2
        assert params['revision'] == "999"
        print("\n✓ Mock: All parameters handled correctly")
