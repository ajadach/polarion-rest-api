"""
Pytest test suite for delete_project_test_parameter_definitions method.
Tests the bulk deletion of test parameter definitions for a project.

Test Strategy:
- All tests use mocks to avoid modifying real data
- Tests cover success cases, error cases, and edge cases

Test Coverage:
- Successful deletion of multiple test parameter definitions
- Successful deletion of single test parameter definition
- Empty list handling
- Project not found (404)
- Insufficient permissions (403)
- Invalid data format (400)
- Large batch deletion

Run with:
    pytest test_delete_project_test_parameter_definitions.py -v
    pytest test_delete_project_test_parameter_definitions.py -v --tb=short
"""
import pytest
import json
from unittest.mock import Mock


@pytest.fixture
def sample_test_param_definitions():
    """Sample test parameter definitions for testing"""
    return [
        {
            "type": "testparameterdefinitions",
            "id": "TEST_PROJECT/param_001"
        },
        {
            "type": "testparameterdefinitions",
            "id": "TEST_PROJECT/param_002"
        },
        {
            "type": "testparameterdefinitions",
            "id": "TEST_PROJECT/param_003"
        }
    ]


# ============================================================================
# Unit Tests - delete_project_test_parameter_definitions
# ============================================================================

class TestDeleteProjectTestParameterDefinitions:
    """Unit tests for delete_project_test_parameter_definitions method"""
    
    def test_delete_multiple_success(self, mock_projects_api, sample_test_param_definitions):
        """Test successful deletion of multiple test parameter definitions"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        
        # Mock the _delete_with_body method
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        # Execute
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_param_definitions=sample_test_param_definitions
        )
        
        # Assert
        assert response.status_code == 204
        mock_projects_api._delete_with_body.assert_called_once()
        
        # Verify correct endpoint
        call_args = mock_projects_api._delete_with_body.call_args
        assert 'projects/TEST_PROJECT/testparameterdefinitions' in call_args[0][0]
        
        # Verify correct body structure
        sent_data = call_args[1]['json']
        assert 'data' in sent_data
        assert len(sent_data['data']) == 3
        assert sent_data['data'][0]['type'] == 'testparameterdefinitions'
        assert sent_data['data'][0]['id'] == 'TEST_PROJECT/param_001'
        assert sent_data['data'][1]['id'] == 'TEST_PROJECT/param_002'
        assert sent_data['data'][2]['id'] == 'TEST_PROJECT/param_003'
        
        print("\n✓ Successfully deleted 3 test parameter definitions (204)")
    
    def test_delete_single_via_bulk(self, mock_projects_api):
        """Test deletion of single test parameter definition via bulk delete"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        single_param = [
            {
                "type": "testparameterdefinitions",
                "id": "TEST_PROJECT/single_param"
            }
        ]
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_param_definitions=single_param
        )
        
        assert response.status_code == 204
        
        # Verify single item was sent
        call_args = mock_projects_api._delete_with_body.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 1
        assert sent_data['data'][0]['id'] == 'TEST_PROJECT/single_param'
        
        print("\n✓ Successfully deleted single parameter via bulk delete (204)")
    
    def test_delete_empty_list(self, mock_projects_api):
        """Test deletion with empty list"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_param_definitions=[]
        )
        
        assert response.status_code == 204
        
        # Verify empty array was sent
        call_args = mock_projects_api._delete_with_body.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data'] == []
        
        print("\n✓ Empty list handled correctly (204)")
    
    def test_delete_project_not_found(self, mock_projects_api, sample_test_param_definitions):
        """Test deletion when project doesn't exist"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = json.dumps({
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Project 'NONEXISTENT' not found"
            }]
        })
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='NONEXISTENT',
            test_param_definitions=sample_test_param_definitions
        )
        
        assert response.status_code == 404
        print("\n✓ Project not found handled correctly (404)")
    
    def test_delete_insufficient_permissions(self, mock_projects_api, sample_test_param_definitions):
        """Test deletion without sufficient permissions"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = json.dumps({
            "errors": [{
                "status": "403",
                "title": "Forbidden",
                "detail": "You do not have permission to delete test parameter definitions"
            }]
        })
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='PROTECTED_PROJECT',
            test_param_definitions=sample_test_param_definitions
        )
        
        assert response.status_code == 403
        print("\n✓ Insufficient permissions handled correctly (403)")
    
    def test_delete_invalid_data_format(self, mock_projects_api):
        """Test deletion with invalid data format"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid test parameter definition format"
            }]
        })
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        # Invalid data - missing required fields
        invalid_params = [
            {
                "type": "wrong_type"
                # Missing 'id' field
            }
        ]
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_param_definitions=invalid_params
        )
        
        assert response.status_code == 400
        print("\n✓ Invalid data format handled correctly (400)")
    
    def test_delete_param_not_found(self, mock_projects_api):
        """Test deletion when test parameter definition doesn't exist"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = json.dumps({
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Test parameter definition 'nonexistent_param' not found"
            }]
        })
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        nonexistent_params = [
            {
                "type": "testparameterdefinitions",
                "id": "TEST_PROJECT/nonexistent_param"
            }
        ]
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_param_definitions=nonexistent_params
        )
        
        assert response.status_code == 404
        print("\n✓ Nonexistent parameter handled correctly (404)")
    
    def test_delete_large_batch(self, mock_projects_api):
        """Test deletion of large batch of test parameter definitions"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        # Create large batch (50 parameters)
        large_batch = [
            {
                "type": "testparameterdefinitions",
                "id": f"TEST_PROJECT/param_{i:03d}"
            }
            for i in range(50)
        ]
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_param_definitions=large_batch
        )
        
        assert response.status_code == 204
        
        # Verify all 50 items were sent
        call_args = mock_projects_api._delete_with_body.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 50
        assert sent_data['data'][0]['id'] == 'TEST_PROJECT/param_000'
        assert sent_data['data'][49]['id'] == 'TEST_PROJECT/param_049'
        
        print("\n✓ Large batch (50 items) deleted successfully (204)")
    
    def test_delete_with_different_types(self, mock_projects_api):
        """Test deletion with different parameter types"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        mixed_params = [
            {
                "type": "testparameterdefinitions",
                "id": "TEST_PROJECT/string_param"
            },
            {
                "type": "testparameterdefinitions",
                "id": "TEST_PROJECT/number_param"
            },
            {
                "type": "testparameterdefinitions",
                "id": "TEST_PROJECT/boolean_param"
            }
        ]
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_param_definitions=mixed_params
        )
        
        assert response.status_code == 204
        
        # Verify all different types were sent
        call_args = mock_projects_api._delete_with_body.call_args
        sent_data = call_args[1]['json']
        assert len(sent_data['data']) == 3
        
        print("\n✓ Mixed parameter types deleted successfully (204)")
    
    def test_delete_with_special_characters_in_id(self, mock_projects_api):
        """Test deletion with special characters in parameter IDs"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        special_params = [
            {
                "type": "testparameterdefinitions",
                "id": "TEST_PROJECT/param-with-dashes"
            },
            {
                "type": "testparameterdefinitions",
                "id": "TEST_PROJECT/param_with_underscores"
            },
            {
                "type": "testparameterdefinitions",
                "id": "TEST_PROJECT/param.with.dots"
            }
        ]
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_param_definitions=special_params
        )
        
        assert response.status_code == 204
        
        # Verify special characters were preserved
        call_args = mock_projects_api._delete_with_body.call_args
        sent_data = call_args[1]['json']
        assert sent_data['data'][0]['id'] == 'TEST_PROJECT/param-with-dashes'
        assert sent_data['data'][1]['id'] == 'TEST_PROJECT/param_with_underscores'
        assert sent_data['data'][2]['id'] == 'TEST_PROJECT/param.with.dots'
        
        print("\n✓ Special characters in IDs handled correctly (204)")
    
    def test_delete_server_error(self, mock_projects_api, sample_test_param_definitions):
        """Test deletion with server error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = json.dumps({
            "errors": [{
                "status": "500",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred"
            }]
        })
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_param_definitions=sample_test_param_definitions
        )
        
        assert response.status_code == 500
        print("\n✓ Server error handled correctly (500)")
    
    def test_delete_partial_success_with_200(self, mock_projects_api, sample_test_param_definitions):
        """Test deletion that returns 200 with partial success info"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "deleted": 2,
                "failed": 1,
                "errors": [
                    {
                        "id": "TEST_PROJECT/param_003",
                        "detail": "Parameter is referenced by test runs"
                    }
                ]
            }
        }
        mock_projects_api._delete_with_body = Mock(return_value=mock_response)
        
        response = mock_projects_api.delete_project_test_parameter_definitions(
            project_id='TEST_PROJECT',
            test_param_definitions=sample_test_param_definitions
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['data']['deleted'] == 2
        assert result['data']['failed'] == 1
        
        print("\n✓ Partial success handled correctly (200)")


# ============================================================================
# Test Configuration and Markers
# ============================================================================

def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line(
        "markers", "delete: mark test as delete operation (uses mocks)"
    )


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([
        __file__,
        '-v',
        '-s',
        '--tb=short'
    ])
