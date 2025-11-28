"""
Pytest tests for DELETE methods in Projects class.

Tests delete_project, delete_project_test_parameter_definitions,
and delete_project_test_parameter_definition methods.
Uses mocks to avoid deleting real data.

Run with:
    pytest test_delete_project.py -v
"""
import pytest
from unittest.mock import Mock


# ============================================================================
# Unit Tests - DELETE Methods (with mocks)
# ============================================================================

@pytest.mark.delete
class TestDeleteProjectMocked:
    """Unit tests for delete_project method using mocks"""
    
    def test_delete_project_success(self, mock_projects_api):
        """Test successful project deletion (mocked)"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_projects_api.delete_project(
            project_id='test_project'
        )
        
        # Assert
        assert response.status_code == 204
        mock_projects_api._session.delete.assert_called_once()
        
        # Verify correct endpoint was called
        call_args = mock_projects_api._session.delete.call_args
        assert 'projects/test_project' in call_args[0][0]
        print("\n✓ Mock: Project deleted successfully (204 No Content)")
    
    def test_delete_project_not_found(self, mock_projects_api):
        """Test deleting non-existent project (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Project not found"
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project(
            project_id='nonexistent_project'
        )
        
        assert response.status_code == 404
        print("\n✓ Mock: Project not found (404)")
    
    def test_delete_project_forbidden(self, mock_projects_api):
        """Test deleting project without permissions (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Insufficient permissions"
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project(
            project_id='protected_project'
        )
        
        assert response.status_code == 403
        print("\n✓ Mock: Insufficient permissions (403)")


@pytest.mark.delete
class TestDeleteProjectTestParameterDefinitionsMocked:
    """Unit tests for deleting test parameter definitions using mocks"""
    
    def test_delete_project_test_parameter_definitions_success(self, mock_projects_api):
        """Test successful deletion of test parameter definitions (mocked)"""
        # Create a proper mock response
        mock_response = Mock()
        mock_response.status_code = 204
        
        # Mock the _delete_with_body helper method
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        # Test with list of test parameter definitions
        test_param_definitions = [
            {
                "type": "param1",
                "id": "test_project/param_001"
            },
            {
                "type": "param2",
                "id": "test_project/param_002"
            }
        ]
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='test_project',
            test_param_definitions=test_param_definitions
        )
        
        assert response.status_code == 204
        mock_projects_api._delete_with_body.assert_called_once()
        
        # Verify the correct body was sent
        call_args = mock_projects_api._delete_with_body.call_args
        sent_data = call_args[1]['json']
        assert 'data' in sent_data
        assert len(sent_data['data']) == 2
        assert sent_data['data'][0]['type'] == 'param1'
        assert sent_data['data'][0]['id'] == 'test_project/param_001'
        assert sent_data['data'][1]['type'] == 'param2'
        assert sent_data['data'][1]['id'] == 'test_project/param_002'
        print("\n✓ Mock: Test parameter definitions deleted successfully")
    
    def test_delete_project_test_parameter_definitions_single(self, mock_projects_api):
        """Test deleting single test parameter definition via bulk delete (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        # Test with single parameter definition
        test_param_definitions = [
            {
                "type": "testparameter_definitions",
                "id": "test_project/param_001"
            }
        ]
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='test_project',
            test_param_definitions=test_param_definitions
        )
        
        assert response.status_code == 204
        
        # Verify the correct body was sent
        call_args = mock_projects_api._delete_with_body.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 1
        assert sent_data['data'][0]['type'] == 'testparameter_definitions'
        assert sent_data['data'][0]['id'] == 'test_project/param_001'
        print("\n✓ Mock: Single test parameter definition deleted via bulk")
    
    def test_delete_project_test_parameter_definitions_empty_list(self, mock_projects_api):
        """Test deleting with empty list (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        # Test with empty list
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='test_project',
            test_param_definitions=[]
        )
        
        assert response.status_code == 204
        
        # Verify empty data array was sent
        call_args = mock_projects_api._delete_with_body.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data'] == []
        print("\n✓ Mock: Empty list handled correctly")
    
    def test_delete_project_test_parameter_definition_single(self, mock_projects_api):
        """Test deleting single test parameter definition (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._session.delete.return_value = mock_response
        
        response = mock_projects_api.delete_project_test_parameter_definition(
            project_id='test_project',
            test_param_id='param_001'
        )
        
        assert response.status_code == 204
        
        # Verify correct endpoint
        call_args = mock_projects_api._session.delete.call_args
        assert 'projects/test_project/testparameterdefinitions/param_001' in call_args[0][0]
        print("\n✓ Mock: Single test parameter definition deleted")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s', '--tb=short'])
