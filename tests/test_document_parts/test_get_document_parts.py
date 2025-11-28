"""
Pytest tests for get_document_parts method.

Tests the get_document_parts method from DocumentParts class.
All tests use mocks.

Run with:
    pytest test_get_document_parts.py -v
"""
import pytest
from unittest.mock import Mock, patch


# ============================================================================
# Mock Tests
# ============================================================================

class TestGetDocumentPartsMock:
    """Mock tests for get_document_parts method"""
    
    def test_get_document_parts_basic(self, mock_document_parts_api):
        """Test getting document parts with basic parameters"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 2},
            "data": [
                {
                    "type": "document_parts",
                    "id": "MyProjectId/MySpaceId/MyDocumentId/workitem_MyWorkItemId",
                    "revision": "1234",
                    "attributes": {
                        "content": "<div id=\"polarion_wiki macro name=module-workitem;params=id=workitem_MyWorkItemId\"></div>",
                        "external": True,
                        "id": "workitem_MyWorkItemId",
                        "level": 0,
                        "type": "workitem"
                    }
                }
            ]
        }
        
        # Mock the _get method
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_parts(
                project_id="MyProjectId",
                space_id="MySpaceId",
                document_name="MyDocumentId"
            )
        
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert data['meta']['totalCount'] == 2
        assert data['data'][0]['type'] == 'document_parts'
        
        print(f"\n✓ Basic document parts retrieval works correctly")
    
    def test_get_document_parts_with_pagination(self, mock_document_parts_api):
        """Test getting document parts with pagination"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 100},
            "data": [],
            "links": {
                "self": "server/projects/P1/spaces/S1/documents/D1/parts?page[size]=10&page[number]=5",
                "first": "server/projects/P1/spaces/S1/documents/D1/parts?page[size]=10&page[number]=1",
                "prev": "server/projects/P1/spaces/S1/documents/D1/parts?page[size]=10&page[number]=4",
                "next": "server/projects/P1/spaces/S1/documents/D1/parts?page[size]=10&page[number]=6",
                "last": "server/projects/P1/spaces/S1/documents/D1/parts?page[size]=10&page[number]=10"
            }
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                page_size=10,
                page_number=5
            )
        
        assert response.status_code == 200
        data = response.json()
        assert 'links' in data
        
        print(f"\n✓ Pagination works correctly")
    
    def test_get_document_parts_with_fields(self, mock_document_parts_api):
        """Test getting document parts with custom fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{
                "type": "document_parts",
                "id": "P1/S1/D1/part1",
                "attributes": {
                    "id": "part1",
                    "type": "workitem"
                }
            }]
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                fields={'document_parts': 'id,type'}
            )
        
        assert response.status_code == 200
        
        print(f"\n✓ Field filtering works correctly")
    
    def test_get_document_parts_with_include(self, mock_document_parts_api):
        """Test getting document parts with included entities"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{
                "type": "document_parts",
                "id": "P1/S1/D1/part1",
                "relationships": {
                    "workItem": {
                        "data": {
                            "type": "workitems",
                            "id": "P1/WI-001"
                        }
                    }
                }
            }],
            "included": [{
                "type": "workitems",
                "id": "P1/WI-001",
                "attributes": {
                    "title": "Test Work Item"
                }
            }]
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                include="workItem"
            )
        
        assert response.status_code == 200
        data = response.json()
        assert 'included' in data
        assert len(data['included']) == 1
        
        print(f"\n✓ Include parameter works correctly")
    
    def test_get_document_parts_with_revision(self, mock_document_parts_api):
        """Test getting document parts with specific revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{
                "type": "document_parts",
                "id": "P1/S1/D1/part1",
                "revision": "5678"
            }]
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                revision="5678"
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data['data'][0]['revision'] == "5678"
        
        print(f"\n✓ Revision parameter works correctly")
    
    def test_get_document_parts_with_all_params(self, mock_document_parts_api):
        """Test getting document parts with all parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": []
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                page_size=25,
                page_number=2,
                fields={'document_parts': 'id,type'},
                include="workItem,nextPart",
                revision="1234"
            )
        
        assert response.status_code == 200
        
        print(f"\n✓ All parameters work correctly together")
    
    def test_get_document_parts_not_found(self, mock_document_parts_api):
        """Test getting document parts for non-existent document"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Document not found"
            }]
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="NONEXISTENT"
            )
        
        assert response.status_code == 404
        
        print(f"\n✓ 404 error handling works correctly")
    
    def test_get_document_parts_unauthorized(self, mock_document_parts_api):
        """Test getting document parts without proper authorization"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [{
                "status": "401",
                "title": "Unauthorized",
                "detail": "Authentication token is invalid or expired"
            }]
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1"
            )
        
        assert response.status_code == 401
        
        print(f"\n✓ 401 error handling works correctly")
    
    def test_get_document_parts_forbidden(self, mock_document_parts_api):
        """Test getting document parts without sufficient permissions"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to view this document"
            }]
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1"
            )
        
        assert response.status_code == 403
        
        print(f"\n✓ 403 error handling works correctly")
    
    def test_get_document_parts_empty_list(self, mock_document_parts_api):
        """Test getting document parts for document with no parts"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 0},
            "data": []
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="EmptyDoc"
            )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data['data']) == 0
        assert data['meta']['totalCount'] == 0
        
        print(f"\n✓ Empty list handling works correctly")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s', '--tb=short'])
