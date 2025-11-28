"""
Pytest tests for get_global_enumeration method in Enumerations class.

Tests the GET /enumerations/{enumContext}/{enumName}/{targetType} endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_get_global_enumeration.py -v
"""
import pytest
from unittest.mock import Mock
import json


@pytest.mark.get
class TestGetGlobalEnumeration:
    """Unit tests for get_global_enumeration method using mocks"""
    
    def test_get_global_enumeration_success(self, mock_enumerations_api):
        """Test successful retrieval of global enumeration (mocked)"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "enumerations",
                "id": "~/status/~",
                "revision": "1234",
                "attributes": {
                    "enumContext": "~",
                    "enumName": "status",
                    "options": [
                        {
                            "id": "open",
                            "name": "Open",
                            "color": "#F9FF4D",
                            "default": True
                        }
                    ],
                    "targetType": "~"
                },
                "links": {
                    "self": "server-host-name/application-path/enumerations/%7E/status/%7E"
                }
            }
        }
        mock_enumerations_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_enumerations_api.get_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='~'
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['data']['type'] == 'enumerations'
        assert data['data']['id'] == '~/status/~'
        assert 'options' in data['data']['attributes']
        
        # Verify correct endpoint was called
        call_args = mock_enumerations_api._session.get.call_args
        assert 'enumerations/~/status/~' in call_args[0][0]
        print("\n✓ Mock: Global enumeration retrieved successfully")
    
    def test_get_global_enumeration_with_fields(self, mock_enumerations_api):
        """Test retrieval with custom fields filter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "enumerations", "id": "~/status/~"}}
        mock_enumerations_api._session.get.return_value = mock_response
        
        # Execute with custom fields
        response = mock_enumerations_api.get_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='~',
            fields={'enumerations': 'id,attributes'}
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_enumerations_api._session.get.call_args
        params = call_args[1]['params']
        assert 'fields[enumerations]' in params
        assert params['fields[enumerations]'] == 'id,attributes'
        print("\n✓ Mock: Custom fields parameter applied correctly")
    
    def test_get_global_enumeration_with_include(self, mock_enumerations_api):
        """Test retrieval with include parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"type": "enumerations", "id": "~/status/~"},
            "included": [{}]
        }
        mock_enumerations_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_enumerations_api.get_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='~',
            include='related'
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_enumerations_api._session.get.call_args
        params = call_args[1]['params']
        assert 'include' in params
        assert params['include'] == 'related'
        print("\n✓ Mock: Include parameter applied correctly")
    
    def test_get_global_enumeration_not_found(self, mock_enumerations_api):
        """Test retrieving non-existent enumeration (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Enumeration not found"
        mock_enumerations_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_enumerations_api.get_global_enumeration(
            enum_context='~',
            enum_name='nonexistent',
            target_type='~'
        )
        
        # Assert
        assert response.status_code == 404
        print("\n✓ Mock: Non-existent enumeration returns 404")
    
    def test_get_global_enumeration_different_contexts(self, mock_enumerations_api):
        """Test retrieval with different enum contexts"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "enumerations"}}
        mock_enumerations_api._session.get.return_value = mock_response
        
        contexts = ['~', 'plans', 'testing', 'documents']
        
        for context in contexts:
            response = mock_enumerations_api.get_global_enumeration(
                enum_context=context,
                enum_name='testEnum',
                target_type='~'
            )
            
            assert response.status_code == 200
            call_args = mock_enumerations_api._session.get.call_args
            assert f'enumerations/{context}/testEnum/~' in call_args[0][0]
        
        print(f"\n✓ Mock: Tested {len(contexts)} different enum contexts")
    
    def test_get_global_enumeration_default_fields(self, mock_enumerations_api):
        """Test that default fields are applied automatically"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "enumerations"}}
        mock_enumerations_api._session.get.return_value = mock_response
        
        # Execute without specifying fields
        response = mock_enumerations_api.get_global_enumeration(
            enum_context='~',
            enum_name='status',
            target_type='~'
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_enumerations_api._session.get.call_args
        params = call_args[1]['params']
        
        # Check that default fields are present
        assert 'fields[collections]' in params
        assert params['fields[collections]'] == '@all'
        assert 'fields[enumerations]' in params
        assert params['fields[enumerations]'] == '@all'
        print("\n✓ Mock: Default fields applied automatically")
