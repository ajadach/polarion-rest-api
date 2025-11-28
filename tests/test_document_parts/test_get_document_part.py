"""
Pytest tests for get_document_part method.

Tests the get_document_part method from DocumentParts class.
All tests use mocks.

Run with:
    pytest test_get_document_part.py -v
"""
import pytest
from unittest.mock import Mock, patch


# ============================================================================
# Mock Tests
# ============================================================================

class TestGetDocumentPartMock:
    """Mock tests for get_document_part method"""
    
    def test_get_document_part_basic(self, mock_document_parts_api):
        """Test getting a single document part with basic parameters"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "document_parts",
                "id": "MyProjectId/MySpaceId/MyDocumentId/workitem_MyWorkItemId",
                "revision": "1234",
                "attributes": {
                    "content": "<div id=\"polarion_wiki macro name=module-workitem;params=id=workitem_MyWorkItemId\"></div>",
                    "external": True,
                    "id": "workitem_MyWorkItemId",
                    "level": 0,
                    "type": "workitem"
                },
                "relationships": {
                    "nextPart": {
                        "data": {
                            "type": "document_parts",
                            "id": "MyProjectId/MySpaceId/MyDocumentId/workitem_NextPart"
                        }
                    },
                    "workItem": {
                        "data": {
                            "type": "workitems",
                            "id": "MyProjectId/MyWorkItemId",
                            "revision": "1234"
                        }
                    }
                },
                "links": {
                    "self": "server/projects/MyProjectId/spaces/MySpaceId/documents/MyDocumentId/parts/workitem_MyWorkItemId"
                }
            }
        }
        
        # Mock the _get method
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_part(
                project_id="MyProjectId",
                space_id="MySpaceId",
                document_name="MyDocumentId",
                part_id="workitem_MyWorkItemId"
            )
        
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert data['data']['type'] == 'document_parts'
        assert data['data']['id'] == 'MyProjectId/MySpaceId/MyDocumentId/workitem_MyWorkItemId'
        assert data['data']['attributes']['level'] == 0
        
        print(f"\n✓ Basic document part retrieval works correctly")
    
    def test_get_document_part_with_fields(self, mock_document_parts_api):
        """Test getting document part with custom fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "document_parts",
                "id": "P1/S1/D1/part1",
                "attributes": {
                    "id": "part1",
                    "type": "workitem"
                }
            }
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_part(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                part_id="part1",
                fields={'document_parts': 'id,type'}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data['data']['attributes']['id'] == 'part1'
        
        print(f"\n✓ Field filtering works correctly")
    
    def test_get_document_part_with_include(self, mock_document_parts_api):
        """Test getting document part with included entities"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
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
            },
            "included": [{
                "type": "workitems",
                "id": "P1/WI-001",
                "attributes": {
                    "title": "Test Work Item",
                    "status": "open"
                }
            }]
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_part(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                part_id="part1",
                include="workItem"
            )
        
        assert response.status_code == 200
        data = response.json()
        assert 'included' in data
        assert len(data['included']) == 1
        assert data['included'][0]['type'] == 'workitems'
        
        print(f"\n✓ Include parameter works correctly")
    
    def test_get_document_part_with_revision(self, mock_document_parts_api):
        """Test getting document part with specific revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "document_parts",
                "id": "P1/S1/D1/part1",
                "revision": "5678",
                "attributes": {
                    "id": "part1",
                    "level": 1
                }
            }
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_part(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                part_id="part1",
                revision="5678"
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data['data']['revision'] == "5678"
        
        print(f"\n✓ Revision parameter works correctly")
    
    def test_get_document_part_with_all_params(self, mock_document_parts_api):
        """Test getting document part with all parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "document_parts",
                "id": "P1/S1/D1/part1",
                "revision": "1234"
            }
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_part(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                part_id="part1",
                fields={'document_parts': 'id,type'},
                include="workItem,nextPart,previousPart",
                revision="1234"
            )
        
        assert response.status_code == 200
        
        print(f"\n✓ All parameters work correctly together")
    
    def test_get_document_part_not_found(self, mock_document_parts_api):
        """Test getting non-existent document part"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Document part 'NONEXISTENT' not found"
            }]
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_part(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                part_id="NONEXISTENT"
            )
        
        assert response.status_code == 404
        
        print(f"\n✓ 404 error handling works correctly")
    
    def test_get_document_part_unauthorized(self, mock_document_parts_api):
        """Test getting document part without proper authorization"""
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
            response = mock_document_parts_api.get_document_part(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                part_id="part1"
            )
        
        assert response.status_code == 401
        
        print(f"\n✓ 401 error handling works correctly")
    
    def test_get_document_part_forbidden(self, mock_document_parts_api):
        """Test getting document part without sufficient permissions"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to view this document part"
            }]
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_part(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                part_id="part1"
            )
        
        assert response.status_code == 403
        
        print(f"\n✓ 403 error handling works correctly")
    
    def test_get_document_part_server_error(self, mock_document_parts_api):
        """Test server error handling"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [{
                "status": "500",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred"
            }]
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_part(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                part_id="part1"
            )
        
        assert response.status_code == 500
        
        print(f"\n✓ 500 error handling works correctly")
    
    def test_get_document_part_with_special_chars(self, mock_document_parts_api):
        """Test getting document part with special characters in ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "document_parts",
                "id": "P1/S1/D1/part-with_special.chars",
                "attributes": {
                    "id": "part-with_special.chars"
                }
            }
        }
        
        with patch.object(mock_document_parts_api, '_get', return_value=mock_response):
            response = mock_document_parts_api.get_document_part(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                part_id="part-with_special.chars"
            )
        
        assert response.status_code == 200
        
        print(f"\n✓ Special characters in part ID handled correctly")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s', '--tb=short'])
