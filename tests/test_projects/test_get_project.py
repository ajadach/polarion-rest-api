"""
Pytest tests for get_project method.

Tests the get_project method from Projects class using mocks.

Run with:
    pytest test_get_project.py -v                    # All tests
"""
import pytest
from unittest.mock import Mock, patch


# ============================================================================
# Mock Tests
# ============================================================================

class TestGetProjectMock:
    """Mock tests for get_project method"""
    
    def test_get_project_basic(self, mock_api_with_spy):
        """Test getting a project with basic parameters"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "MyProjectId",
                "revision": "1234",
                "attributes": {
                    "active": True,
                    "color": "Color",
                    "description": {
                        "type": "text/plain",
                        "value": "My text value"
                    },
                    "finish": "1970-01-01",
                    "icon": "Icon",
                    "id": "MyProjectId",
                    "lockWorkRecordsDate": "1970-01-01",
                    "name": "Name",
                    "start": "1970-01-01",
                    "trackerPrefix": "Tracker Prefix"
                },
                "relationships": {
                    "lead": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId",
                            "revision": "1234"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/projects/MyProjectId?revision=1234"
                }
            },
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId?revision=1234"
            }
        }
        
        # Mock the _get method
        with patch.object(mock_api_with_spy, '_get', return_value=mock_response):
            response = mock_api_with_spy.get_project(project_id="MyProjectId")
        
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert data['data']['type'] == 'projects'
        assert data['data']['id'] == 'MyProjectId'
        assert data['data']['attributes']['name'] == 'Name'
        assert data['data']['attributes']['active'] is True
        
        print(f"\n✓ Basic project retrieval works correctly")
    
    def test_get_project_with_fields(self, mock_api_with_spy):
        """Test getting a project with field filtering"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "MyProjectId",
                "attributes": {
                    "name": "Name",
                    "active": True
                }
            }
        }
        
        with patch.object(mock_api_with_spy, '_get', return_value=mock_response):
            response = mock_api_with_spy.get_project(
                project_id="MyProjectId",
                fields={'projects': 'name,active'}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data['data']['id'] == 'MyProjectId'
        
        print(f"\n✓ Field filtering works correctly")
    
    def test_get_project_with_include(self, mock_api_with_spy):
        """Test getting a project with related entities"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "MyProjectId",
                "attributes": {
                    "name": "Name"
                },
                "relationships": {
                    "lead": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId"
                        }
                    }
                }
            },
            "included": [
                {
                    "type": "users",
                    "id": "MyUserId",
                    "attributes": {
                        "name": "John Doe",
                        "email": "john@example.com"
                    }
                }
            ]
        }
        
        with patch.object(mock_api_with_spy, '_get', return_value=mock_response):
            response = mock_api_with_spy.get_project(
                project_id="MyProjectId",
                include='lead'
            )
        
        assert response.status_code == 200
        data = response.json()
        assert 'included' in data
        assert len(data['included']) == 1
        assert data['included'][0]['type'] == 'users'
        
        print(f"\n✓ Include parameter works correctly")
    
    def test_get_project_not_found(self, mock_api_with_spy):
        """Test getting a non-existent project"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [{
                "status": "404",
                "title": "Not Found",
                "detail": "Project not found"
            }]
        }
        
        with patch.object(mock_api_with_spy, '_get', return_value=mock_response):
            response = mock_api_with_spy.get_project(
                project_id='NONEXISTENT_PROJECT_XYZ'
            )
        
        assert response.status_code == 404
        print(f"\n✓ 404 error handling works correctly")
    
    def test_get_project_with_invalid_id(self, mock_api_with_spy):
        """Test getting project with invalid ID format"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [{
                "status": "400",
                "title": "Bad Request",
                "detail": "Invalid project ID format"
            }]
        }
        
        with patch.object(mock_api_with_spy, '_get', return_value=mock_response):
            response = mock_api_with_spy.get_project(
                project_id='invalid@project#id'
            )
        
        assert response.status_code == 400
        print(f"\n✓ 400 error handling works correctly")
    
    def test_get_project_with_revision(self, mock_api_with_spy):
        """Test getting a project with specific revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "MyProjectId",
                "revision": "5678",
                "attributes": {
                    "name": "Name"
                }
            }
        }
        
        with patch.object(mock_api_with_spy, '_get', return_value=mock_response):
            response = mock_api_with_spy.get_project(
                project_id="MyProjectId",
                revision="5678"
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data['data']['revision'] == "5678"
        
        print(f"\n✓ Revision parameter works correctly")

    
    def test_get_project_with_all_params(self, mock_api_with_spy):
        """Test getting a project with all parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "projects",
                "id": "MyProjectId",
                "revision": "1234",
                "attributes": {
                    "name": "Name",
                    "active": True
                }
            }
        }
        
        with patch.object(mock_api_with_spy, '_get', return_value=mock_response):
            response = mock_api_with_spy.get_project(
                project_id="MyProjectId",
                fields={'projects': 'name,active'},
                include='lead',
                revision='1234'
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data['data']['id'] == 'MyProjectId'
        assert data['data']['revision'] == '1234'
        
        print(f"\n✓ All parameters work correctly together")


# ============================================================================
# Unit Tests - Default Fields Logic
# ============================================================================

class TestGetProjectDefaultFields:
    """Unit tests to verify default_fields logic for get_project method"""
    
    def test_get_project_sends_all_default_fields(self, mock_api_with_spy):
        """Test that get_project sends all default fields when no fields provided"""
        # Call without custom fields
        mock_api_with_spy.get_project("TEST_PROJECT")
        
        # Get captured params
        params = mock_api_with_spy._captured_params[0]
        
        # Verify all default fields are present in fields[name] format
        expected_fields = [
            "collections", "categories", "documents", "document_attachments",
            "document_comments", "document_parts", "enumerations", "globalroles",
            "icons", "jobs", "linkedworkitems", "externallylinkedworkitems",
            "linkedoslcresources", "pages", "page_attachments", "plans",
            "projectroles", "projects", "projecttemplates", "testparameters",
            "testparameter_definitions", "testrecords", "teststep_results",
            "testruns", "testrun_attachments", "teststepresult_attachments",
            "testrun_comments", "usergroups", "users", "workitems",
            "workitem_attachments", "workitem_approvals", "workitem_comments",
            "featureselections", "teststeps", "workrecords", "revisions",
            "testrecord_attachments"
        ]
        
        for field in expected_fields:
            field_key = f"fields[{field}]"
            assert field_key in params, f"Default field '{field_key}' not in params"
            assert params[field_key] == "@all", f"Default field '{field_key}' not set to @all"
        
        print("\n✓ All default fields sent with @all values in fields[name] format")
    
    def test_get_project_overrides_only_specified_fields(self, mock_api_with_spy):
        """Test that custom fields override only specified keys"""
        # Call with custom fields
        custom_fields = {
            "workitems": "id,title",
            "users": "name,email"
        }
        mock_api_with_spy.get_project("TEST_PROJECT", fields=custom_fields)
        
        # Get captured params
        params = mock_api_with_spy._captured_params[0]
        
        # Verify custom fields are overridden (in fields[name] format)
        assert params["fields[workitems]"] == "id,title", "Custom workitems field not applied"
        assert params["fields[users]"] == "name,email", "Custom users field not applied"
        
        # Verify other fields remain @all
        assert params["fields[documents]"] == "@all", "Non-overridden field should remain @all"
        assert params["fields[projects]"] == "@all", "Non-overridden field should remain @all"
        
        print("\n✓ Custom fields override only specified keys, others remain @all")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s', '--tb=short'])
