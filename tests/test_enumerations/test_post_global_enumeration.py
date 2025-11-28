"""
Pytest tests for post_global_enumeration method in Enumerations class.

Tests the POST /enumerations endpoint.
Uses mocks to avoid creating real data.

Run with:
    pytest test_post_global_enumeration.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.post
class TestPostGlobalEnumeration:
    """Unit tests for post_global_enumeration method using mocks"""
    
    def test_post_global_enumeration_success(self, mock_enumerations_api):
        """Test successful creation of global enumeration (mocked)"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "enumerations",
                    "id": "~/customStatus/~",
                    "links": {
                        "self": "server-host-name/application-path/enumerations/%7E/customStatus/%7E"
                    }
                }
            ]
        }
        mock_enumerations_api._session.post.return_value = mock_response
        
        # Prepare data
        enumeration_data = {
            "data": [
                {
                    "type": "enumerations",
                    "attributes": {
                        "enumContext": "~",
                        "enumName": "customStatus",
                        "options": [
                            {
                                "id": "open",
                                "name": "Open",
                                "color": "#F9FF4D",
                                "default": True
                            }
                        ],
                        "targetType": "~"
                    }
                }
            ]
        }
        
        # Execute
        response = mock_enumerations_api.post_global_enumeration(
            enumeration_data=enumeration_data
        )
        
        # Assert
        assert response.status_code == 201
        mock_enumerations_api._session.post.assert_called_once()
        
        # Verify correct endpoint was called
        call_args = mock_enumerations_api._session.post.call_args
        assert 'enumerations' in call_args[0][0]
        
        # Verify JSON data was sent
        assert call_args[1]['json'] == enumeration_data
        
        # Verify response contains created resource
        data = response.json()
        assert 'data' in data
        assert len(data['data']) == 1
        assert data['data'][0]['id'] == '~/customStatus/~'
        print("\n✓ Mock: Global enumeration created successfully (201 Created)")
    
    def test_post_global_enumeration_with_multiple_enumerations(self, mock_enumerations_api):
        """Test creation of multiple enumerations at once"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [
                {"type": "enumerations", "id": "~/status1/~"},
                {"type": "enumerations", "id": "~/status2/~"}
            ]
        }
        mock_enumerations_api._session.post.return_value = mock_response
        
        enumeration_data = {
            "data": [
                {
                    "type": "enumerations",
                    "attributes": {
                        "enumContext": "~",
                        "enumName": "status1",
                        "options": [{"id": "open", "name": "Open"}],
                        "targetType": "~"
                    }
                },
                {
                    "type": "enumerations",
                    "attributes": {
                        "enumContext": "~",
                        "enumName": "status2",
                        "options": [{"id": "closed", "name": "Closed"}],
                        "targetType": "~"
                    }
                }
            ]
        }
        
        response = mock_enumerations_api.post_global_enumeration(
            enumeration_data=enumeration_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert len(data['data']) == 2
        print("\n✓ Mock: Multiple enumerations created successfully")
    
    def test_post_global_enumeration_bad_request(self, mock_enumerations_api):
        """Test creation with invalid data (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request: Missing required fields"
        mock_enumerations_api._session.post.return_value = mock_response
        
        enumeration_data = {
            "data": [
                {
                    "type": "enumerations",
                    "attributes": {}  # Invalid: missing required fields
                }
            ]
        }
        
        response = mock_enumerations_api.post_global_enumeration(
            enumeration_data=enumeration_data
        )
        
        assert response.status_code == 400
        print("\n✓ Mock: Invalid data returns 400")
    
    def test_post_global_enumeration_conflict(self, mock_enumerations_api):
        """Test creation of enumeration that already exists (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.text = "Conflict: Enumeration already exists"
        mock_enumerations_api._session.post.return_value = mock_response
        
        enumeration_data = {
            "data": [
                {
                    "type": "enumerations",
                    "attributes": {
                        "enumContext": "~",
                        "enumName": "status",  # Already exists
                        "options": [],
                        "targetType": "~"
                    }
                }
            ]
        }
        
        response = mock_enumerations_api.post_global_enumeration(
            enumeration_data=enumeration_data
        )
        
        assert response.status_code == 409
        print("\n✓ Mock: Duplicate enumeration returns 409")
    
    def test_post_global_enumeration_with_complex_options(self, mock_enumerations_api):
        """Test creation with complex enumeration options"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": [{"type": "enumerations", "id": "~/complexEnum/~"}]
        }
        mock_enumerations_api._session.post.return_value = mock_response
        
        enumeration_data = {
            "data": [
                {
                    "type": "enumerations",
                    "attributes": {
                        "enumContext": "~",
                        "enumName": "complexEnum",
                        "options": [
                            {
                                "id": "open",
                                "name": "Open",
                                "color": "#F9FF4D",
                                "description": "Task is open",
                                "hidden": False,
                                "default": True,
                                "parent": True,
                                "oppositeName": "Closed",
                                "columnWidth": "90%",
                                "iconURL": "/polarion/icons/default/enums/status_open.gif",
                                "createDefect": True,
                                "templateWorkItem": "exampleTemplate",
                                "minValue": 30,
                                "requiresSignatureForTestCaseExecution": True,
                                "terminal": False,
                                "limited": True
                            }
                        ],
                        "targetType": "~"
                    }
                }
            ]
        }
        
        response = mock_enumerations_api.post_global_enumeration(
            enumeration_data=enumeration_data
        )
        
        assert response.status_code == 201
        call_args = mock_enumerations_api._session.post.call_args
        options = call_args[1]['json']['data'][0]['attributes']['options']
        assert len(options) == 1
        assert 'iconURL' in options[0]
        assert 'requiresSignatureForTestCaseExecution' in options[0]
        print("\n✓ Mock: Enumeration with complex options created successfully")
    
    def test_post_global_enumeration_unauthorized(self, mock_enumerations_api):
        """Test creation without authorization (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_enumerations_api._session.post.return_value = mock_response
        
        enumeration_data = {
            "data": [
                {
                    "type": "enumerations",
                    "attributes": {
                        "enumContext": "~",
                        "enumName": "testEnum",
                        "options": [],
                        "targetType": "~"
                    }
                }
            ]
        }
        
        response = mock_enumerations_api.post_global_enumeration(
            enumeration_data=enumeration_data
        )
        
        assert response.status_code == 401
        print("\n✓ Mock: Unauthorized access returns 401")
    
    def test_post_global_enumeration_different_contexts(self, mock_enumerations_api):
        """Test creation with different enum contexts"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": [{"type": "enumerations"}]}
        mock_enumerations_api._session.post.return_value = mock_response
        
        contexts = ['~', 'plans', 'testing', 'documents']
        
        for context in contexts:
            enumeration_data = {
                "data": [
                    {
                        "type": "enumerations",
                        "attributes": {
                            "enumContext": context,
                            "enumName": "testEnum",
                            "options": [],
                            "targetType": "~"
                        }
                    }
                ]
            }
            
            response = mock_enumerations_api.post_global_enumeration(
                enumeration_data=enumeration_data
            )
            
            assert response.status_code == 201
            call_args = mock_enumerations_api._session.post.call_args
            assert call_args[1]['json']['data'][0]['attributes']['enumContext'] == context
        
        print(f"\n✓ Mock: Tested {len(contexts)} different enum contexts")
