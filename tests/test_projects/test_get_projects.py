"""
Pytest tests for get_projects method.

Tests the get_projects method from Projects class.
Unit tests for default fields logic.

Run with:
    pytest test_get_projects.py -v
"""
import pytest


# ============================================================================
# Unit Tests - Default Fields Logic
# ============================================================================

class TestGetProjectsDefaultFields:
    """Unit tests to verify default_fields logic for get_projects method"""
    
    def test_get_projects_sends_all_default_fields(self, mock_api_with_spy):
        """Test that get_projects sends all default fields when no fields provided"""
        # Call without custom fields
        mock_api_with_spy.get_projects()
        
        # Get captured params
        params = mock_api_with_spy._captured_params[0]
        
        # Verify all default fields are present in fields[name] format
        expected_fields = [
            "categories", "documents", "document_attachments",
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
        
        print("\n✓ get_projects: All default fields sent with @all values in fields[name] format")
    
    def test_get_projects_overrides_only_specified_fields(self, mock_api_with_spy):
        """Test that get_projects custom fields override only specified keys"""
        # Call with custom fields
        custom_fields = {
            "projects": "id,name",
            "workitems": "id,status"
        }
        mock_api_with_spy.get_projects(fields=custom_fields)
        
        # Get captured params
        params = mock_api_with_spy._captured_params[0]
        
        # Verify custom fields are overridden (in fields[name] format)
        assert params["fields[projects]"] == "id,name", "Custom projects field not applied"
        assert params["fields[workitems]"] == "id,status", "Custom workitems field not applied"
        
        # Verify other fields remain @all
        assert params["fields[users]"] == "@all", "Non-overridden field should remain @all"
        assert params["fields[documents]"] == "@all", "Non-overridden field should remain @all"
        
        print("\n✓ get_projects: Custom fields override only specified keys")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s', '--tb=short'])
