"""
Pytest tests for post_documents method.

Tests the post_documents method from Documents class.
All tests use mocks.

Run with:
    pytest test_post_documents.py -v
"""
import pytest
from unittest.mock import Mock


# ============================================================================
# Mock Tests
# ============================================================================

class TestPostDocumentsMock:
    """Mock tests for post_documents method"""
    
    def test_post_documents_single(self, mock_documents_api):
        """Test creating a single document"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyDocument",
                "attributes": {
                    "title": "Test Document",
                    "status": "draft"
                }
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "_default"
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {
                    "moduleName": "MyDocument",
                    "title": "Test Document",
                    "type": "req_specification",
                    "status": "draft"
                }
            }]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id=project_id,
            space_id=space_id,
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 201
        mock_documents_api._session.post.assert_called_once()
        call_args = mock_documents_api._session.post.call_args
        
        # Verify endpoint
        expected_url = f"https://test.polarion.com/polarion/rest/v1/projects/{project_id}/spaces/{space_id}/documents"
        assert call_args[0][0] == expected_url
        
        # Verify JSON body
        assert call_args[1]['json'] == documents_data
    
    def test_post_documents_multiple(self, mock_documents_api):
        """Test creating multiple documents"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "documents",
                    "id": "MyProjectId/MySpaceId/Doc1"
                },
                {
                    "type": "documents",
                    "id": "MyProjectId/MySpaceId/Doc2"
                }
            ]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "_default"
        documents_data = {
            "data": [
                {
                    "type": "documents",
                    "attributes": {
                        "moduleName": "Doc1",
                        "title": "Document 1",
                        "type": "req_specification"
                    }
                },
                {
                    "type": "documents",
                    "attributes": {
                        "moduleName": "Doc2",
                        "title": "Document 2",
                        "type": "test_specification"
                    }
                }
            ]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id=project_id,
            space_id=space_id,
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 201
        assert len(response.json()['data']) == 2
    
    def test_post_documents_with_full_attributes(self, mock_documents_api):
        """Test creating a document with all attributes"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyDocument"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data with all attributes
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {
                    "autoSuspect": True,
                    "homePageContent": {
                        "type": "text/html",
                        "value": "<h1>My Document</h1>"
                    },
                    "moduleName": "MyDocument",
                    "outlineNumbering": {
                        "prefix": "REQ"
                    },
                    "renderingLayouts": [
                        {
                            "type": "task",
                            "label": "Task Layout",
                            "layouter": "paragraph",
                            "properties": [
                                {
                                    "key": "fieldsAtStart",
                                    "value": "id"
                                }
                            ]
                        }
                    ],
                    "status": "draft",
                    "structureLinkRole": "relates_to",
                    "title": "My Document Title",
                    "type": "req_specification",
                    "usesOutlineNumbering": True
                }
            }]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id="TEST_PROJECT",
            space_id="_default",
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        
        # Verify all attributes are in the request
        attrs = call_args[1]['json']['data'][0]['attributes']
        assert attrs['autoSuspect'] == True
        assert attrs['usesOutlineNumbering'] == True
        assert 'homePageContent' in attrs
        assert 'renderingLayouts' in attrs
        assert 'outlineNumbering' in attrs
    
    def test_post_documents_with_home_page_content(self, mock_documents_api):
        """Test creating a document with home page content"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyDocument"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {
                    "moduleName": "MyDocument",
                    "title": "Test Document",
                    "type": "req_specification",
                    "homePageContent": {
                        "type": "text/html",
                        "value": "<p>Welcome to the document</p>"
                    }
                }
            }]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id="TEST_PROJECT",
            space_id="_default",
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        assert 'homePageContent' in call_args[1]['json']['data'][0]['attributes']
    
    def test_post_documents_with_rendering_layouts(self, mock_documents_api):
        """Test creating a document with rendering layouts"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyDocument"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {
                    "moduleName": "MyDocument",
                    "title": "Test Document",
                    "type": "req_specification",
                    "renderingLayouts": [
                        {
                            "type": "requirement",
                            "label": "Requirement Layout",
                            "layouter": "section",
                            "properties": [
                                {
                                    "key": "fieldsAtStart",
                                    "value": "id,status"
                                }
                            ]
                        }
                    ]
                }
            }]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id="TEST_PROJECT",
            space_id="_default",
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        layouts = call_args[1]['json']['data'][0]['attributes']['renderingLayouts']
        assert len(layouts) > 0
        assert layouts[0]['type'] == 'requirement'
    
    def test_post_documents_with_outline_numbering(self, mock_documents_api):
        """Test creating a document with outline numbering"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{
                "type": "documents",
                "id": "MyProjectId/MySpaceId/MyDocument"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {
                    "moduleName": "MyDocument",
                    "title": "Test Document",
                    "type": "req_specification",
                    "usesOutlineNumbering": True,
                    "outlineNumbering": {
                        "prefix": "REQ-"
                    }
                }
            }]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id="TEST_PROJECT",
            space_id="_default",
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 201
        call_args = mock_documents_api._session.post.call_args
        attrs = call_args[1]['json']['data'][0]['attributes']
        assert attrs['usesOutlineNumbering'] == True
        assert 'outlineNumbering' in attrs
    
    def test_post_documents_bad_request(self, mock_documents_api):
        """Test creating documents with invalid data"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid document data"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data - invalid
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {
                    # Missing required fields
                }
            }]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id="TEST_PROJECT",
            space_id="_default",
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 400
    
    def test_post_documents_unauthorized(self, mock_documents_api):
        """Test creating documents without proper authorization"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [{
                "status": "401",
                "title": "Unauthorized"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {
                    "moduleName": "MyDocument",
                    "title": "Test Document"
                }
            }]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id="TEST_PROJECT",
            space_id="_default",
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 401
    
    def test_post_documents_forbidden(self, mock_documents_api):
        """Test creating documents without sufficient permissions"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "Insufficient permissions"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {
                    "moduleName": "MyDocument",
                    "title": "Test Document"
                }
            }]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id="TEST_PROJECT",
            space_id="_default",
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 403
    
    def test_post_documents_not_found(self, mock_documents_api):
        """Test creating documents in non-existent project/space"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Project or space not found"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {
                    "moduleName": "MyDocument",
                    "title": "Test Document"
                }
            }]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id="INVALID_PROJECT",
            space_id="INVALID_SPACE",
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 404
    
    def test_post_documents_conflict(self, mock_documents_api):
        """Test creating documents when document already exists"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "errors": [{
                "status": "409",
                "title": "Conflict",
                "detail": "Document already exists"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {
                    "moduleName": "ExistingDocument",
                    "title": "Test Document"
                }
            }]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id="TEST_PROJECT",
            space_id="_default",
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 409
    
    def test_post_documents_server_error(self, mock_documents_api):
        """Test creating documents with server error"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [{
                "status": "500",
                "title": "Internal Server Error"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {
                    "moduleName": "MyDocument",
                    "title": "Test Document"
                }
            }]
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id="TEST_PROJECT",
            space_id="_default",
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 500
    
    def test_post_documents_url_construction(self, mock_documents_api):
        """Test URL construction for create documents endpoint"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data
        project_id = "TEST_PROJECT"
        space_id = "MySpace"
        documents_data = {
            "data": [{
                "type": "documents",
                "attributes": {"moduleName": "Doc1", "title": "Test"}
            }]
        }
        
        # Execute
        mock_documents_api.post_documents(
            project_id=project_id,
            space_id=space_id,
            documents_data=documents_data
        )
        
        # Assert URL construction
        call_args = mock_documents_api._session.post.call_args
        expected_url = f"https://test.polarion.com/polarion/rest/v1/projects/{project_id}/spaces/{space_id}/documents"
        assert call_args[0][0] == expected_url
    
    def test_post_documents_empty_array(self, mock_documents_api):
        """Test creating documents with empty data array"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Empty data array"
            }]
        }
        mock_documents_api._session.post.return_value = mock_response
        
        # Test data - empty array
        documents_data = {
            "data": []
        }
        
        # Execute
        response = mock_documents_api.post_documents(
            project_id="TEST_PROJECT",
            space_id="_default",
            documents_data=documents_data
        )
        
        # Assert
        assert response.status_code == 400
