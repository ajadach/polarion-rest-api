"""
Pytest tests for patch_project method.

Tests the patch_project method from Projects class.
Uses mocks to avoid modifying real project data.

Run with:
    pytest test_patch_project.py -v
"""
import pytest
from unittest.mock import Mock, patch


# ============================================================================
# Mock Tests - PATCH Method
# ============================================================================

class TestPatchProjectMock:
    """Mock tests for patch_project method"""
    
    def test_patch_project_description_success(self, mock_api_with_spy):
        """Test successful project description update (mocked)"""
        # Setup mock response - PATCH typically returns 204 No Content
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        
        # Prepare update data
        update_data = {
            "data": {
                "type": "projects",
                "id": "MyProjectId",
                "attributes": {
                    "description": {
                        "type": "text/plain",
                        "value": "Test description updated by pytest"
                    }
                }
            }
        }
        
        # Mock the _patch method
        with patch.object(mock_api_with_spy, '_patch', return_value=mock_response):
            response = mock_api_with_spy.patch_project(
                project_id='MyProjectId',
                project_data=update_data
            )
        
        # Assert
        assert response.status_code == 204
        print("\n✓ Mock: Project description updated successfully (204 No Content)")
    
    def test_patch_project_success_with_response(self, mock_api_with_spy):
        """Test project update with 200 response and data (mocked)"""
        # Some APIs return 200 with updated data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "MyProjectId",
                "revision": "1234",
                "attributes": {
                    "name": "My Project",
                    "active": True,
                    "description": {
                        "type": "text/plain",
                        "value": "Updated description"
                    }
                }
            }
        }
        
        update_data = {
            "data": {
                "type": "projects",
                "id": "MyProjectId",
                "attributes": {
                    "description": {
                        "type": "text/plain",
                        "value": "Updated description"
                    }
                }
            }
        }
        
        with patch.object(mock_api_with_spy, '_patch', return_value=mock_response):
            response = mock_api_with_spy.patch_project(
                project_id='MyProjectId',
                project_data=update_data
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data['data']['id'] == 'MyProjectId'
        assert data['data']['attributes']['description']['value'] == 'Updated description'
        print("\n✓ Mock: Project updated successfully (200 with data)")
    
    def test_patch_project_not_found(self, mock_api_with_spy):
        """Test updating non-existent project (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Project with ID 'NONEXISTENT' not found"
            }]
        }
        
        update_data = {
            "data": {
                "type": "projects",
                "id": "NONEXISTENT",
                "attributes": {
                    "description": {
                        "type": "text/plain",
                        "value": "Test"
                    }
                }
            }
        }
        
        with patch.object(mock_api_with_spy, '_patch', return_value=mock_response):
            response = mock_api_with_spy.patch_project(
                project_id='NONEXISTENT',
                project_data=update_data
            )
        
        assert response.status_code == 404
        print("\n✓ Mock: Project not found (404)")
    
    def test_patch_project_forbidden(self, mock_api_with_spy):
        """Test updating project without permissions (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to modify Project."
            }]
        }
        
        update_data = {
            "data": {
                "type": "projects",
                "id": "PROTECTED",
                "attributes": {
                    "description": {
                        "type": "text/plain",
                        "value": "Test"
                    }
                }
            }
        }
        
        with patch.object(mock_api_with_spy, '_patch', return_value=mock_response):
            response = mock_api_with_spy.patch_project(
                project_id='PROTECTED',
                project_data=update_data
            )
        
        assert response.status_code == 403
        print("\n✓ Mock: Insufficient permissions (403)")
    
    def test_patch_project_invalid_data(self, mock_api_with_spy):
        """Test updating project with invalid data (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid data format - type must be 'projects'"
            }]
        }
        
        # Invalid data structure
        invalid_data = {
            "data": {
                "type": "wrong_type",
                "id": "MyProjectId"
            }
        }
        
        with patch.object(mock_api_with_spy, '_patch', return_value=mock_response):
            response = mock_api_with_spy.patch_project(
                project_id='MyProjectId',
                project_data=invalid_data
            )
        
        assert response.status_code == 400
        print("\n✓ Mock: Invalid data format (400)")
    
    def test_patch_project_with_multiple_attributes(self, mock_api_with_spy):
        """Test updating multiple project attributes (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        
        update_data = {
            "data": {
                "type": "projects",
                "id": "MyProjectId",
                "attributes": {
                    "description": {
                        "type": "text/plain",
                        "value": "Updated description"
                    },
                    "active": True,
                    "color": "Blue"
                }
            }
        }
        
        with patch.object(mock_api_with_spy, '_patch', return_value=mock_response):
            response = mock_api_with_spy.patch_project(
                project_id='MyProjectId',
                project_data=update_data
            )
        
        assert response.status_code == 204
        print("\n✓ Mock: Multiple attributes updated successfully")
    
    def test_patch_project_with_relationships(self, mock_api_with_spy):
        """Test updating project with relationships (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        
        update_data = {
            "data": {
                "type": "projects",
                "id": "MyProjectId",
                "attributes": {
                    "name": "Updated Project Name"
                },
                "relationships": {
                    "lead": {
                        "data": {
                            "type": "users",
                            "id": "NewLeadUserId"
                        }
                    }
                }
            }
        }
        
        with patch.object(mock_api_with_spy, '_patch', return_value=mock_response):
            response = mock_api_with_spy.patch_project(
                project_id='MyProjectId',
                project_data=update_data
            )
        
        assert response.status_code == 204
        print("\n✓ Mock: Project with relationships updated successfully")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s', '--tb=short'])
