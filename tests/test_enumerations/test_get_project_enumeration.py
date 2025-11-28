"""
Pytest tests for get_project_enumeration method in Enumerations class.

Tests the GET /projects/{projectId}/enumerations/{enumContext}/{enumName}/{targetType} endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_get_project_enumeration.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.get
class TestGetProjectEnumeration:
    """Unit tests for get_project_enumeration method using mocks"""
    
    def test_get_project_enumeration_success(self, mock_enumerations_api):
        """Test successful retrieval of project enumeration (mocked)"""
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
                    "self": "server-host-name/application-path/projects/test_project/enumerations/%7E/status/%7E"
                }
            }
        }
        mock_enumerations_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_enumerations_api.get_project_enumeration(
            project_id='test_project',
            enum_context='~',
            enum_name='status',
            target_type='~'
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['data']['type'] == 'enumerations'
        assert data['data']['id'] == '~/status/~'
        
        # Verify correct endpoint was called
        call_args = mock_enumerations_api._session.get.call_args
        assert 'projects/test_project/enumerations/~/status/~' in call_args[0][0]
        print("\n✓ Mock: Project enumeration retrieved successfully")
    
    def test_get_project_enumeration_with_fields(self, mock_enumerations_api):
        """Test retrieval with custom fields filter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "enumerations"}}
        mock_enumerations_api._session.get.return_value = mock_response
        
        # Execute with custom fields
        response = mock_enumerations_api.get_project_enumeration(
            project_id='test_project',
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
    
    def test_get_project_enumeration_with_include(self, mock_enumerations_api):
        """Test retrieval with include parameter (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"type": "enumerations"},
            "included": [{}]
        }
        mock_enumerations_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_enumerations_api.get_project_enumeration(
            project_id='test_project',
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
    
    def test_get_project_enumeration_project_not_found(self, mock_enumerations_api):
        """Test retrieving enumeration from non-existent project (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Project not found"
        mock_enumerations_api._session.get.return_value = mock_response
        
        # Execute
        response = mock_enumerations_api.get_project_enumeration(
            project_id='nonexistent_project',
            enum_context='~',
            enum_name='status',
            target_type='~'
        )
        
        # Assert
        assert response.status_code == 404
        print("\n✓ Mock: Non-existent project returns 404")
    
    def test_get_project_enumeration_default_fields(self, mock_enumerations_api):
        """Test that default fields are applied automatically"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "enumerations"}}
        mock_enumerations_api._session.get.return_value = mock_response
        
        # Execute without specifying fields
        response = mock_enumerations_api.get_project_enumeration(
            project_id='test_project',
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
        print("\n✓ Mock: Default fields applied automatically")
