"""
Pytest tests for patch_global_enumeration method in Enumerations class.

Tests the PATCH /enumerations/{enumContext}/{enumName}/{targetType} endpoint.
Uses mocks to avoid modifying real data.

Run with:
    pytest test_patch_global_enumeration.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.patch
class TestPatchGlobalEnumeration:
    """Unit tests for patch_global_enumeration method using mocks"""
    
    def test_patch_global_enumeration_success(self, mock_enumerations_api):
        """Test successful update of global enumeration (mocked)"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_enumerations_api._session.patch.return_value = mock_response
        
        # Prepare data
        enumeration_data = {
            "data": {
                "type": "enumerations",
                "id": "~/status/~",
                "attributes": {
                    "options": [
                        {
                            "id": "open",
                            "name": "Open",
                            "color": "#F9FF4D",
                            "default": True
                        }
                    ]
                }
            }
        }
        
        # Execute
        response = mock_enumerations_api.patch_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='~',
            enumeration_data=enumeration_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_enumerations_api._session.patch.assert_called_once()
        
        # Verify correct endpoint was called
        call_args = mock_enumerations_api._session.patch.call_args
        assert 'enumerations/~/status/~' in call_args[0][0]
        
        # Verify JSON data was sent
        assert call_args[1]['json'] == enumeration_data
        print("\n✓ Mock: Global enumeration updated successfully (204 No Content)")
    
    def test_patch_global_enumeration_with_multiple_options(self, mock_enumerations_api):
        """Test update with multiple enumeration options"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_enumerations_api._session.patch.return_value = mock_response
        
        enumeration_data = {
            "data": {
                "type": "enumerations",
                "id": "~/status/~",
                "attributes": {
                    "options": [
                        {
                            "id": "open",
                            "name": "Open",
                            "color": "#F9FF4D",
                            "default": True
                        },
                        {
                            "id": "closed",
                            "name": "Closed",
                            "color": "#808080",
                            "default": False
                        }
                    ]
                }
            }
        }
        
        response = mock_enumerations_api.patch_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='~',
            enumeration_data=enumeration_data
        )
        
        assert response.status_code == 204
        call_args = mock_enumerations_api._session.patch.call_args
        assert len(call_args[1]['json']['data']['attributes']['options']) == 2
        print("\n✓ Mock: Update with multiple options successful")
    
    def test_patch_global_enumeration_not_found(self, mock_enumerations_api):
        """Test updating non-existent enumeration (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Enumeration not found"
        mock_enumerations_api._session.patch.return_value = mock_response
        
        enumeration_data = {
            "data": {
                "type": "enumerations",
                "id": "~/nonexistent/~",
                "attributes": {"options": []}
            }
        }
        
        response = mock_enumerations_api.patch_global_enumeration(
            enum_context='~',
            enum_name='nonexistent',
            target_type='~',
            enumeration_data=enumeration_data
        )
        
        assert response.status_code == 404
        print("\n✓ Mock: Non-existent enumeration returns 404")
    
    def test_patch_global_enumeration_bad_request(self, mock_enumerations_api):
        """Test update with invalid data (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_enumerations_api._session.patch.return_value = mock_response
        
        enumeration_data = {
            "data": {
                "type": "enumerations",
                "id": "~/status/~",
                "attributes": {}  # Invalid: missing options
            }
        }
        
        response = mock_enumerations_api.patch_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='~',
            enumeration_data=enumeration_data
        )
        
        assert response.status_code == 400
        print("\n✓ Mock: Invalid data returns 400")
    
    def test_patch_global_enumeration_different_contexts(self, mock_enumerations_api):
        """Test update with different enum contexts"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_enumerations_api._session.patch.return_value = mock_response
        
        contexts = ['~', 'plans', 'testing', 'documents']
        
        for context in contexts:
            enumeration_data = {
                "data": {
                    "type": "enumerations",
                    "id": f"{context}/testEnum/~",
                    "attributes": {"options": []}
                }
            }
            
            response = mock_enumerations_api.patch_global_enumeration(
                enum_context=context,
                enum_name='testEnum',
                target_type='~',
                enumeration_data=enumeration_data
            )
            
            assert response.status_code == 204
            call_args = mock_enumerations_api._session.patch.call_args
            assert f'enumerations/{context}/testEnum/~' in call_args[0][0]
        
        print(f"\n✓ Mock: Tested {len(contexts)} different enum contexts")
    
    def test_patch_global_enumeration_unauthorized(self, mock_enumerations_api):
        """Test update without authorization (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_enumerations_api._session.patch.return_value = mock_response
        
        enumeration_data = {"data": {"type": "enumerations", "id": "~/status/~", "attributes": {"options": []}}}
        
        response = mock_enumerations_api.patch_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='~',
            enumeration_data=enumeration_data
        )
        
        assert response.status_code == 401
        print("\n✓ Mock: Unauthorized access returns 401")
