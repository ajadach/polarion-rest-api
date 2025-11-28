"""
Pytest tests for delete_global_enumeration method in Enumerations class.

Tests the DELETE /enumerations/{enumContext}/{enumName}/{targetType} endpoint.
Uses mocks to avoid deleting real data.

Run with:
    pytest test_delete_global_enumeration.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.delete
class TestDeleteGlobalEnumeration:
    """Unit tests for delete_global_enumeration method using mocks"""
    
    def test_delete_global_enumeration_success(self, mock_enumerations_api):
        """Test successful global enumeration deletion (mocked)"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_enumerations_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_enumerations_api.delete_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='~'
        )
        
        # Assert
        assert response.status_code == 204
        mock_enumerations_api._session.delete.assert_called_once()
        
        # Verify correct endpoint was called
        call_args = mock_enumerations_api._session.delete.call_args
        assert 'enumerations/~/status/~' in call_args[0][0]
        print("\n✓ Mock: Global enumeration deleted successfully (204 No Content)")
    
    def test_delete_global_enumeration_not_found(self, mock_enumerations_api):
        """Test deleting non-existent global enumeration (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Enumeration not found"
        mock_enumerations_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_enumerations_api.delete_global_enumeration(
            enum_context='~',
            enum_name='nonexistent',
            target_type='~'
        )
        
        # Assert
        assert response.status_code == 404
        print("\n✓ Mock: Non-existent enumeration returns 404")
    
    def test_delete_global_enumeration_different_contexts(self, mock_enumerations_api):
        """Test deletion with different enum contexts"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_enumerations_api._session.delete.return_value = mock_response
        
        contexts = ['~', 'plans', 'testing', 'documents']
        
        for context in contexts:
            response = mock_enumerations_api.delete_global_enumeration(
                enum_context=context,
                enum_name='testEnum',
                target_type='~'
            )
            
            assert response.status_code == 204
            call_args = mock_enumerations_api._session.delete.call_args
            assert f'enumerations/{context}/testEnum/~' in call_args[0][0]
        
        print(f"\n✓ Mock: Tested {len(contexts)} different enum contexts")
    
    def test_delete_global_enumeration_unauthorized(self, mock_enumerations_api):
        """Test deletion without proper authorization (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_enumerations_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_enumerations_api.delete_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='~'
        )
        
        # Assert
        assert response.status_code == 401
        print("\n✓ Mock: Unauthorized access returns 401")
    
    def test_delete_global_enumeration_forbidden(self, mock_enumerations_api):
        """Test deletion without sufficient permissions (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_enumerations_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_enumerations_api.delete_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='~'
        )
        
        # Assert
        assert response.status_code == 403
        print("\n✓ Mock: Insufficient permissions return 403")
    
    def test_delete_global_enumeration_with_special_target_type(self, mock_enumerations_api):
        """Test deletion with specific target type"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_enumerations_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_enumerations_api.delete_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='workitem'
        )
        
        # Assert
        assert response.status_code == 204
        call_args = mock_enumerations_api._session.delete.call_args
        assert 'enumerations/~/status/workitem' in call_args[0][0]
        print("\n✓ Mock: Deletion with specific target type works correctly")
