"""
Pytest tests for post_document_parts method.

Tests the post_document_parts method from DocumentParts class.
All tests use mocks.

Run with:
    pytest test_post_document_parts.py -v
"""
import pytest
from unittest.mock import Mock, patch


# ============================================================================
# Mock Tests
# ============================================================================

class TestPostDocumentPartsMock:
    """Mock tests for post_document_parts method"""
    
    def test_post_document_parts_single(self, mock_document_parts_api):
        """Test creating a single document part"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{
                "type": "document_parts",
                "id": "MyProjectId/MySpaceId/MyDocumentId/workitem_MyWorkItemId",
                "attributes": {
                    "id": "workitem_MyWorkItemId",
                    "level": 0,
                    "type": "workitem"
                }
            }]
        }
        
        parts_data = {
            "data": [{
                "type": "document_parts",
                "attributes": {
                    "level": 0,
                    "type": "workitem"
                },
                "relationships": {
                    "workItem": {
                        "data": {
                            "type": "workitems",
                            "id": "MyProjectId/MyWorkItemId"
                        }
                    }
                }
            }]
        }
        
        # Mock the _post method
        with patch.object(mock_document_parts_api, '_post', return_value=mock_response):
            response = mock_document_parts_api.post_document_parts(
                project_id="MyProjectId",
                space_id="MySpaceId",
                document_name="MyDocumentId",
                parts_data=parts_data
            )
        
        assert response.status_code == 201
        data = response.json()
        assert 'data' in data
        assert len(data['data']) == 1
        assert data['data'][0]['type'] == 'document_parts'
        
        print(f"\n✓ Single document part creation works correctly")
    
    def test_post_document_parts_multiple(self, mock_document_parts_api):
        """Test creating multiple document parts"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "document_parts",
                    "id": "P1/S1/D1/part1",
                    "attributes": {"id": "part1", "level": 0, "type": "workitem"}
                },
                {
                    "type": "document_parts",
                    "id": "P1/S1/D1/part2",
                    "attributes": {"id": "part2", "level": 1, "type": "text"}
                },
                {
                    "type": "document_parts",
                    "id": "P1/S1/D1/part3",
                    "attributes": {"id": "part3", "level": 1, "type": "workitem"}
                }
            ]
        }
        
        parts_data = {
            "data": [
                {
                    "type": "document_parts",
                    "attributes": {"level": 0, "type": "workitem"},
                    "relationships": {
                        "workItem": {"data": {"type": "workitems", "id": "P1/WI-001"}}
                    }
                },
                {
                    "type": "document_parts",
                    "attributes": {"level": 1, "type": "text"}
                },
                {
                    "type": "document_parts",
                    "attributes": {"level": 1, "type": "workitem"},
                    "relationships": {
                        "workItem": {"data": {"type": "workitems", "id": "P1/WI-002"}}
                    }
                }
            ]
        }
        
        with patch.object(mock_document_parts_api, '_post', return_value=mock_response):
            response = mock_document_parts_api.post_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                parts_data=parts_data
            )
        
        assert response.status_code == 201
        data = response.json()
        assert len(data['data']) == 3
        
        print(f"\n✓ Multiple document parts creation works correctly")
    
    def test_post_document_parts_with_relationships(self, mock_document_parts_api):
        """Test creating document parts with relationships (next/previous)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{
                "type": "document_parts",
                "id": "P1/S1/D1/part1",
                "relationships": {
                    "nextPart": {
                        "data": {
                            "type": "document_parts",
                            "id": "P1/S1/D1/part2"
                        }
                    },
                    "previousPart": {
                        "data": {
                            "type": "document_parts",
                            "id": "P1/S1/D1/part0"
                        }
                    }
                }
            }]
        }
        
        parts_data = {
            "data": [{
                "type": "document_parts",
                "attributes": {
                    "level": 0,
                    "type": "workitem"
                },
                "relationships": {
                    "nextPart": {
                        "data": {
                            "type": "document_parts",
                            "id": "P1/S1/D1/part2"
                        }
                    },
                    "previousPart": {
                        "data": {
                            "type": "document_parts",
                            "id": "P1/S1/D1/part0"
                        }
                    },
                    "workItem": {
                        "data": {
                            "type": "workitems",
                            "id": "P1/WI-001",
                            "revision": "1234"
                        }
                    }
                }
            }]
        }
        
        with patch.object(mock_document_parts_api, '_post', return_value=mock_response):
            response = mock_document_parts_api.post_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                parts_data=parts_data
            )
        
        assert response.status_code == 201
        data = response.json()
        assert 'relationships' in data['data'][0]
        
        print(f"\n✓ Document parts with relationships created correctly")
    
    def test_post_document_parts_text_type(self, mock_document_parts_api):
        """Test creating text-type document part"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{
                "type": "document_parts",
                "id": "P1/S1/D1/text1",
                "attributes": {
                    "id": "text1",
                    "level": 0,
                    "type": "text",
                    "content": "<p>This is text content</p>"
                }
            }]
        }
        
        parts_data = {
            "data": [{
                "type": "document_parts",
                "attributes": {
                    "level": 0,
                    "type": "text",
                    "content": "<p>This is text content</p>"
                }
            }]
        }
        
        with patch.object(mock_document_parts_api, '_post', return_value=mock_response):
            response = mock_document_parts_api.post_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                parts_data=parts_data
            )
        
        assert response.status_code == 201
        data = response.json()
        assert data['data'][0]['attributes']['type'] == 'text'
        
        print(f"\n✓ Text-type document part creation works correctly")
    
    def test_post_document_parts_bad_request(self, mock_document_parts_api):
        """Test creating document parts with invalid data"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid data format - missing required field 'type' in attributes"
            }]
        }
        
        invalid_data = {
            "data": [{
                "type": "document_parts",
                "attributes": {
                    "level": 0
                    # Missing 'type' field
                }
            }]
        }
        
        with patch.object(mock_document_parts_api, '_post', return_value=mock_response):
            response = mock_document_parts_api.post_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                parts_data=invalid_data
            )
        
        assert response.status_code == 400
        
        print(f"\n✓ 400 error handling works correctly")
    
    def test_post_document_parts_unauthorized(self, mock_document_parts_api):
        """Test creating document parts without proper authorization"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [{
                "status": "401",
                "title": "Unauthorized",
                "detail": "Authentication token is invalid or expired"
            }]
        }
        
        parts_data = {
            "data": [{
                "type": "document_parts",
                "attributes": {"level": 0, "type": "workitem"}
            }]
        }
        
        with patch.object(mock_document_parts_api, '_post', return_value=mock_response):
            response = mock_document_parts_api.post_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                parts_data=parts_data
            )
        
        assert response.status_code == 401
        
        print(f"\n✓ 401 error handling works correctly")
    
    def test_post_document_parts_forbidden(self, mock_document_parts_api):
        """Test creating document parts without sufficient permissions"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to modify this document"
            }]
        }
        
        parts_data = {
            "data": [{
                "type": "document_parts",
                "attributes": {"level": 0, "type": "workitem"}
            }]
        }
        
        with patch.object(mock_document_parts_api, '_post', return_value=mock_response):
            response = mock_document_parts_api.post_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                parts_data=parts_data
            )
        
        assert response.status_code == 403
        
        print(f"\n✓ 403 error handling works correctly")
    
    def test_post_document_parts_not_found(self, mock_document_parts_api):
        """Test creating document parts for non-existent document"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Document 'NONEXISTENT' not found"
            }]
        }
        
        parts_data = {
            "data": [{
                "type": "document_parts",
                "attributes": {"level": 0, "type": "workitem"}
            }]
        }
        
        with patch.object(mock_document_parts_api, '_post', return_value=mock_response):
            response = mock_document_parts_api.post_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="NONEXISTENT",
                parts_data=parts_data
            )
        
        assert response.status_code == 404
        
        print(f"\n✓ 404 error handling works correctly")
    
    def test_post_document_parts_server_error(self, mock_document_parts_api):
        """Test server error handling"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [{
                "status": "500",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred while creating document parts"
            }]
        }
        
        parts_data = {
            "data": [{
                "type": "document_parts",
                "attributes": {"level": 0, "type": "workitem"}
            }]
        }
        
        with patch.object(mock_document_parts_api, '_post', return_value=mock_response):
            response = mock_document_parts_api.post_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                parts_data=parts_data
            )
        
        assert response.status_code == 500
        
        print(f"\n✓ 500 error handling works correctly")
    
    def test_post_document_parts_empty_array(self, mock_document_parts_api):
        """Test creating document parts with empty array"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Data array cannot be empty"
            }]
        }
        
        parts_data = {
            "data": []
        }
        
        with patch.object(mock_document_parts_api, '_post', return_value=mock_response):
            response = mock_document_parts_api.post_document_parts(
                project_id="P1",
                space_id="S1",
                document_name="D1",
                parts_data=parts_data
            )
        
        assert response.status_code == 400
        
        print(f"\n✓ Empty array validation works correctly")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s', '--tb=short'])
