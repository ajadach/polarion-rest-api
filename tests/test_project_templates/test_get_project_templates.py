"""
Tests for ProjectTemplates.get_project_templates method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetProjectTemplates:
    """Test suite for get_project_templates method"""
    
    def test_get_project_templates_success(self, mock_project_templates_api):
        """Test successful retrieval of project templates"""
        # Mock response data based on example
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 1
            },
            "data": [
                {
                    "type": "projecttemplates",
                    "id": "MyProjectId",
                    "revision": "1234",
                    "attributes": {
                        "customIcon": "string",
                        "description": "string",
                        "distributions": ["string"],
                        "id": "string",
                        "isDefault": True,
                        "name": "string",
                        "parameters": {}
                    },
                    "links": {
                        "self": "server-host-name/application-path/projecttemplates/MyProjectId?revision=1234"
                    }
                }
            ],
            "links": {
                "self": "server-host-name/application-path/projecttemplates?page%5Bsize%5D=10&page%5Bnumber%5D=5"
            }
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_project_templates_api.get_project_templates()
        
        # Verify the call
        mock_project_templates_api._session.get.assert_called_once()
        call_args = mock_project_templates_api._session.get.call_args
        
        # Check URL
        assert 'projecttemplates' in call_args[0][0]
        
        # Verify response
        assert response.status_code == 200
        assert response.json()['meta']['totalCount'] == 1
        assert len(response.json()['data']) == 1
        assert response.json()['data'][0]['type'] == 'projecttemplates'
    
    def test_get_project_templates_with_pagination(self, mock_project_templates_api):
        """Test get_project_templates with pagination parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 50},
            "data": [
                {"type": "projecttemplates", "id": "Template1"},
                {"type": "projecttemplates", "id": "Template2"}
            ],
            "links": {
                "self": "server-host-name/application-path/projecttemplates?page%5Bsize%5D=123&page%5Bnumber%5D=456",
                "next": "server-host-name/application-path/projecttemplates?page%5Bsize%5D=123&page%5Bnumber%5D=457"
            }
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        # Call with pagination
        response = mock_project_templates_api.get_project_templates(
            page_size=123,
            page_number=456
        )
        
        # Verify pagination parameters
        call_args = mock_project_templates_api._session.get.call_args
        params = call_args[1]['params']
        
        assert params['page[size]'] == 123
        assert params['page[number]'] == 456
        assert response.status_code == 200
    
    def test_get_project_templates_with_all_parameters(self, mock_project_templates_api):
        """Test get_project_templates with all optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "projecttemplates", "id": "Template1"}
            ]
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        # Call with all parameters
        response = mock_project_templates_api.get_project_templates(
            page_size=50,
            page_number=2,
            fields={'projecttemplates': 'name,description'},
            include='distributions'
        )
        
        # Verify the call
        call_args = mock_project_templates_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom fields override default
        assert 'fields[projecttemplates]' in params
        assert params['fields[projecttemplates]'] == 'name,description'
        
        # Verify other parameters
        assert params['page[size]'] == 50
        assert params['page[number]'] == 2
        assert params['include'] == 'distributions'
        
        assert response.status_code == 200
    
    def test_get_project_templates_default_fields_applied(self, mock_project_templates_api):
        """Test that default fields are properly applied when no custom fields provided"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        # Call without fields parameter
        response = mock_project_templates_api.get_project_templates()
        
        # Verify default fields are applied
        call_args = mock_project_templates_api._session.get.call_args
        params = call_args[1]['params']
        
        # Check that all default collection fields are set to @all
        expected_collections = [
            'collections', 'categories', 'documents', 'document_attachments',
            'document_comments', 'document_parts', 'enumerations', 'globalroles',
            'icons', 'jobs', 'linkedworkitems', 'externallylinkedworkitems',
            'linkedoslcresources', 'pages', 'page_attachments', 'plans',
            'projectroles', 'projects', 'projecttemplates', 'testparameters',
            'testparameter_definitions', 'testrecords', 'teststep_results',
            'testruns', 'testrun_attachments', 'teststepresult_attachments',
            'testrun_comments', 'usergroups', 'users', 'workitems',
            'workitem_attachments', 'workitem_approvals', 'workitem_comments',
            'featureselections', 'teststeps', 'workrecords', 'revisions',
            'testrecord_attachments'
        ]
        
        for collection in expected_collections:
            field_key = f'fields[{collection}]'
            assert field_key in params
            assert params[field_key] == '@all'
    
    def test_get_project_templates_error_400(self, mock_project_templates_api):
        """Test handling of 400 Bad Request error"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Unexpected token, BEGIN_ARRAY expected, but was : BEGIN_OBJECT (at $.data)",
                    "source": {
                        "pointer": "$.data",
                        "parameter": "revision",
                        "resource": {
                            "id": "MyProjectId/id",
                            "type": "type"
                        }
                    }
                }
            ]
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates()
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
    
    def test_get_project_templates_error_401(self, mock_project_templates_api):
        """Test handling of 401 Unauthorized error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "No access token"
                }
            ]
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates()
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
    
    def test_get_project_templates_attributes(self, mock_project_templates_api):
        """Test that response contains expected template attributes"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "projecttemplates",
                    "id": "ScramTemplate",
                    "attributes": {
                        "name": "Scrum Template",
                        "description": "Template for Scrum projects",
                        "isDefault": True,
                        "distributions": ["polarion"],
                        "customIcon": "icon.png",
                        "parameters": {"param1": "value1"}
                    }
                }
            ]
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates()
        
        # Verify attributes
        attrs = response.json()['data'][0]['attributes']
        assert attrs['name'] == 'Scrum Template'
        assert attrs['description'] == 'Template for Scrum projects'
        assert attrs['isDefault'] is True
        assert 'polarion' in attrs['distributions']
    
    def test_get_project_templates_url_structure(self, mock_project_templates_api):
        """Test that URL is properly constructed"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates()
        
        # Verify URL structure
        call_args = mock_project_templates_api._session.get.call_args
        url = call_args[0][0]
        
        assert 'projecttemplates' in url
        assert response.status_code == 200
    
    def test_get_project_templates_with_include(self, mock_project_templates_api):
        """Test get_project_templates with include parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "projecttemplates", "id": "Template1"}
            ],
            "included": [
                {"type": "distributions", "id": "dist1"}
            ]
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates(
            include='distributions'
        )
        
        # Verify include parameter
        call_args = mock_project_templates_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'distributions'
        assert len(response.json()['included']) == 1
    
    def test_get_project_templates_links(self, mock_project_templates_api):
        """Test that response contains proper pagination links"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "projecttemplates", "id": "Template1"}
            ],
            "links": {
                "self": "server-host-name/application-path/projecttemplates?page%5Bsize%5D=10&page%5Bnumber%5D=5",
                "first": "server-host-name/application-path/projecttemplates?page%5Bsize%5D=10&page%5Bnumber%5D=1",
                "prev": "server-host-name/application-path/projecttemplates?page%5Bsize%5D=10&page%5Bnumber%5D=4",
                "next": "server-host-name/application-path/projecttemplates?page%5Bsize%5D=10&page%5Bnumber%5D=6",
                "last": "server-host-name/application-path/projecttemplates?page%5Bsize%5D=10&page%5Bnumber%5D=9"
            }
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates(
            page_size=10,
            page_number=5
        )
        
        # Verify links
        links = response.json()['links']
        assert 'self' in links
        assert 'first' in links
        assert 'prev' in links
        assert 'next' in links
        assert 'last' in links
    
    def test_get_project_templates_empty_list(self, mock_project_templates_api):
        """Test get_project_templates with empty result"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {
                "totalCount": 0
            },
            "data": []
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates()
        
        # Verify empty result
        assert response.status_code == 200
        assert len(response.json()['data']) == 0
        assert response.json()['meta']['totalCount'] == 0
    
    def test_get_project_templates_multiple_templates(self, mock_project_templates_api):
        """Test retrieving multiple project templates"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 3},
            "data": [
                {"type": "projecttemplates", "id": "Template1", "attributes": {"name": "Scrum"}},
                {"type": "projecttemplates", "id": "Template2", "attributes": {"name": "Kanban"}},
                {"type": "projecttemplates", "id": "Template3", "attributes": {"name": "Waterfall"}}
            ]
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates()
        
        # Verify multiple templates
        data = response.json()['data']
        assert len(data) == 3
        assert all(item['type'] == 'projecttemplates' for item in data)
        assert data[0]['attributes']['name'] == 'Scrum'
    
    def test_get_project_templates_custom_fields_override(self, mock_project_templates_api):
        """Test that custom fields override default fields"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        custom_fields = {
            'projecttemplates': 'name,description,isDefault'
        }
        
        response = mock_project_templates_api.get_project_templates(
            fields=custom_fields
        )
        
        call_args = mock_project_templates_api._session.get.call_args
        params = call_args[1]['params']
        
        # Custom field should override
        assert params['fields[projecttemplates]'] == 'name,description,isDefault'
        
        # Other collections should still be @all
        assert params['fields[projects]'] == '@all'
        assert params['fields[plans]'] == '@all'
    
    def test_get_project_templates_with_distributions(self, mock_project_templates_api):
        """Test project template with distributions"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "projecttemplates",
                    "id": "Template1",
                    "attributes": {
                        "name": "Standard Template",
                        "distributions": ["polarion", "custom"]
                    }
                }
            ]
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates()
        
        # Verify distributions
        attrs = response.json()['data'][0]['attributes']
        assert 'distributions' in attrs
        assert len(attrs['distributions']) == 2
        assert 'polarion' in attrs['distributions']
    
    def test_get_project_templates_default_template(self, mock_project_templates_api):
        """Test identifying default template"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "projecttemplates",
                    "id": "DefaultTemplate",
                    "attributes": {
                        "name": "Default Project Template",
                        "isDefault": True
                    }
                }
            ]
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates()
        
        # Verify default flag
        assert response.json()['data'][0]['attributes']['isDefault'] is True
    
    def test_get_project_templates_pagination_first_page(self, mock_project_templates_api):
        """Test get_project_templates with first page"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"totalCount": 25},
            "data": [
                {"type": "projecttemplates", "id": "Template1"},
                {"type": "projecttemplates", "id": "Template2"}
            ],
            "links": {
                "self": "server-host-name/application-path/projecttemplates?page[number]=1",
                "next": "server-host-name/application-path/projecttemplates?page[number]=2"
            }
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates(
            page_size=10,
            page_number=1
        )
        
        # Verify pagination
        call_args = mock_project_templates_api._session.get.call_args
        params = call_args[1]['params']
        assert params['page[size]'] == 10
        assert params['page[number]'] == 1
        
        # Verify response has next link but no prev
        assert 'next' in response.json()['links']
    
    def test_get_project_templates_with_parameters(self, mock_project_templates_api):
        """Test project template with custom parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "projecttemplates",
                    "id": "Template1",
                    "attributes": {
                        "name": "Configurable Template",
                        "parameters": {
                            "teamSize": "small",
                            "sprintLength": "2weeks"
                        }
                    }
                }
            ]
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        response = mock_project_templates_api.get_project_templates()
        
        # Verify parameters
        params_data = response.json()['data'][0]['attributes']['parameters']
        assert 'teamSize' in params_data
        assert params_data['teamSize'] == 'small'
    
    def test_get_project_templates_minimal_parameters(self, mock_project_templates_api):
        """Test get_project_templates with no optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"type": "projecttemplates", "id": "Template1"}
            ]
        }
        
        mock_project_templates_api._session.get.return_value = mock_response
        
        # Call with no parameters
        response = mock_project_templates_api.get_project_templates()
        
        # Verify call was made
        mock_project_templates_api._session.get.assert_called_once()
        
        # Verify only default fields are in params
        call_args = mock_project_templates_api._session.get.call_args
        params = call_args[1]['params']
        
        # Should have default fields but no pagination or include
        assert 'page[size]' not in params
        assert 'page[number]' not in params
        assert 'include' not in params
        
        assert response.status_code == 200
