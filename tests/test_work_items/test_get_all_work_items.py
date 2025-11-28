"""
Pytest tests for get_all_work_items method.

Tests the get_all_work_items method from WorkItems class.
Uses mocks to avoid making real API calls.

Run with:
    pytest test_get_all_work_items.py -v
"""
import pytest
from unittest.mock import Mock


# ============================================================================
# Unit Tests - GET Method (with mocks)
# ============================================================================

class TestGetAllWorkItemsMocked:
    """Unit tests for get_all_work_items method using mocks
    
    NOTE: These tests use mocks to avoid making real API calls.
    """
    
    def test_get_all_work_items_success(self, mock_work_items_api):
        """Test successful retrieval of all work items (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "workitems",
                    "id": "Project1/WI-001",
                    "attributes": {
                        "title": "Test Work Item 1",
                        "status": "open"
                    }
                },
                {
                    "type": "workitems",
                    "id": "Project1/WI-002",
                    "attributes": {
                        "title": "Test Work Item 2",
                        "status": "closed"
                    }
                }
            ]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_work_items_api.get_all_work_items()
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert len(data['data']) == 2
        mock_work_items_api._session.get.assert_called_once()
        print("\n✓ Mock: All work items retrieved successfully")
    
    def test_get_all_work_items_with_pagination(self, mock_work_items_api):
        """Test get all work items with pagination parameters (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [],
            "meta": {
                "totalCount": 100
            }
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        # Execute with pagination
        response = mock_work_items_api.get_all_work_items(
            page_size=10,
            page_number=2
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_work_items_api._session.get.call_args
        assert 'params' in call_args[1]
        assert call_args[1]['params']['page[size]'] == 10
        assert call_args[1]['params']['page[number]'] == 2
        print("\n✓ Mock: Pagination parameters handled correctly")
    
    def test_get_all_work_items_with_query(self, mock_work_items_api):
        """Test get all work items with query parameter (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        # Execute with query
        response = mock_work_items_api.get_all_work_items(
            query="status:open"
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_work_items_api._session.get.call_args
        assert call_args[1]['params']['query'] == "status:open"
        print("\n✓ Mock: Query parameter handled correctly")
    
    def test_get_all_work_items_with_fields(self, mock_work_items_api):
        """Test get all work items with custom fields (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        # Execute with custom fields
        response = mock_work_items_api.get_all_work_items(
            fields={'workitems': 'id,title'}
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_work_items_api._session.get.call_args
        assert 'params' in call_args[1]
        assert 'fields[workitems]' in call_args[1]['params']
        print("\n✓ Mock: Custom fields parameter handled correctly")
    
    def test_get_all_work_items_with_sort(self, mock_work_items_api):
        """Test get all work items with sort parameter (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        # Execute with sort
        response = mock_work_items_api.get_all_work_items(
            sort="title"
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_work_items_api._session.get.call_args
        assert call_args[1]['params']['sort'] == "title"
        print("\n✓ Mock: Sort parameter handled correctly")
    
    def test_get_all_work_items_with_include(self, mock_work_items_api):
        """Test get all work items with include parameter (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        # Execute with include
        response = mock_work_items_api.get_all_work_items(
            include="author,assignee"
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_work_items_api._session.get.call_args
        assert call_args[1]['params']['include'] == "author,assignee"
        print("\n✓ Mock: Include parameter handled correctly")
    
    def test_get_all_work_items_with_revision(self, mock_work_items_api):
        """Test get all work items with revision parameter (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        # Execute with revision
        response = mock_work_items_api.get_all_work_items(
            revision="12345"
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_work_items_api._session.get.call_args
        assert call_args[1]['params']['revision'] == "12345"
        print("\n✓ Mock: Revision parameter handled correctly")
    
    def test_get_all_work_items_unauthorized(self, mock_work_items_api):
        """Test get with invalid authentication (401 Unauthorized) (mocked)"""
        # Setup mock response for error
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
        mock_work_items_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_work_items_api.get_all_work_items()
        
        # Assert
        assert response.status_code == 401
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '401'
        print("\n✓ Mock: Unauthorized (401) handled correctly")
    
    def test_get_all_work_items_forbidden(self, mock_work_items_api):
        """Test get without sufficient permissions (403 Forbidden) (mocked)"""
        # Setup mock response for error
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "Insufficient permissions to read work items"
                }
            ]
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_work_items_api.get_all_work_items()
        
        # Assert
        assert response.status_code == 403
        error_data = response.json()
        assert error_data['errors'][0]['status'] == '403'
        print("\n✓ Mock: Forbidden (403) handled correctly")
    
    def test_get_all_work_items_empty_result(self, mock_work_items_api):
        """Test get all work items with empty result (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [],
            "meta": {
                "totalCount": 0
            }
        }
        mock_work_items_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_work_items_api.get_all_work_items()
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data['data']) == 0
        print("\n✓ Mock: Empty result handled correctly")
    
    def test_get_all_work_items_all_parameters(self, mock_work_items_api):
        """Test get all work items with all parameters (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_work_items_api._session.get.return_value = mock_response
        
        # Execute with all parameters
        response = mock_work_items_api.get_all_work_items(
            page_size=20,
            page_number=1,
            fields={'workitems': 'id,title,status'},
            include="author",
            query="status:open",
            sort="created",
            revision="67890"
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_work_items_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 20
        assert params['page[number]'] == 1
        assert params['query'] == "status:open"
        assert params['sort'] == "created"
        assert params['include'] == "author"
        assert params['revision'] == "67890"
        print("\n✓ Mock: All parameters handled correctly")


# ============================================================================
# Notes
# ============================================================================
"""
API Endpoint: GET /all/workitems
Description: Returns a list of Work Items from the Global context

Expected Response Codes:
- 200: OK (successful retrieval)
- 401: Unauthorized (invalid or missing token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (resource doesn't exist)

Response Body Example:
{
    "data": [
        {
            "type": "workitems",
            "id": "ProjectId/WorkItemId",
            "attributes": {
                "title": "Work Item Title",
                "status": "open",
                "created": "2025-01-01T10:00:00Z"
            }
        }
    ],
    "meta": {
        "totalCount": 100
    }
}

Query Parameters:
- page[size]: Limit the number of entities returned
- page[number]: Specify the page number (starts from 1)
- fields[type]: Sparse fieldsets for specific types
- include: Include related entities
- query: Query string for filtering
- sort: Sort results by field
- revision: Get data from specific revision
"""
