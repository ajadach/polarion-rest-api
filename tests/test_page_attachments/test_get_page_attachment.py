"""
Tests for PageAttachments.get_page_attachment method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetPageAttachment:
    """Test suite for get_page_attachment method"""
    
    def test_get_page_attachment_success(self, mock_page_attachments_api):
        """Test successful retrieval of a page attachment"""
        # Mock response data based on example
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "page_attachments",
                "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId",
                "revision": "1234",
                "attributes": {
                    "fileName": "File Name",
                    "id": "MyAttachmentId",
                    "length": 0,
                    "title": "Title",
                    "updated": "1970-01-01T00:00:00Z"
                },
                "relationships": {
                    "author": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId",
                            "revision": "1234"
                        }
                    },
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "MyProjectId",
                            "revision": "1234"
                        }
                    }
                },
                "meta": {
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
                },
                "links": {
                    "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments/MyAttachmentId?revision=1234",
                    "content": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments/MyAttachmentId/content?revision=1234"
                }
            },
            "included": [
                {}
            ],
            "links": {
                "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments/MyAttachmentId?revision=1234"
            }
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_page_attachments_api.get_page_attachment(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify the call
        mock_page_attachments_api._session.get.assert_called_once()
        call_args = mock_page_attachments_api._session.get.call_args
        
        # Check URL
        assert 'projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments/MyAttachmentId' in call_args[0][0]
        
        # Verify response
        assert response.status_code == 200
        assert response.json()['data']['type'] == 'page_attachments'
        assert response.json()['data']['attributes']['fileName'] == 'File Name'
        assert response.json()['data']['attributes']['id'] == 'MyAttachmentId'
    
    def test_get_page_attachment_with_all_parameters(self, mock_page_attachments_api):
        """Test get_page_attachment with all optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "page_attachments",
                "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId"
            }
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call with all parameters
        response = mock_page_attachments_api.get_page_attachment(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId',
            fields={'page_attachments': 'fileName,title'},
            include='author,project',
            revision='1234'
        )
        
        # Verify the call
        call_args = mock_page_attachments_api._session.get.call_args
        params = call_args[1]['params']
        
        # Verify custom fields override default
        assert 'fields[page_attachments]' in params
        assert params['fields[page_attachments]'] == 'fileName,title'
        
        # Verify other parameters
        assert params['include'] == 'author,project'
        assert params['revision'] == '1234'
        
        assert response.status_code == 200
    
    def test_get_page_attachment_with_default_space(self, mock_page_attachments_api):
        """Test get_page_attachment with _default space"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "page_attachments"}}
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call with _default space
        response = mock_page_attachments_api.get_page_attachment(
            project_id='MyProjectId',
            space_id='_default',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify URL contains _default
        call_args = mock_page_attachments_api._session.get.call_args
        assert 'spaces/_default/' in call_args[0][0]
        assert response.status_code == 200
    
    def test_get_page_attachment_default_fields_applied(self, mock_page_attachments_api):
        """Test that default fields are properly applied when no custom fields provided"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call without fields parameter
        response = mock_page_attachments_api.get_page_attachment(
            project_id='TEST_PROJECT',
            space_id='TEST_SPACE',
            page_name='TEST_PAGE',
            attachment_id='TEST_ATTACHMENT'
        )
        
        # Verify default fields are applied
        call_args = mock_page_attachments_api._session.get.call_args
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
    
    def test_get_page_attachment_custom_fields_override(self, mock_page_attachments_api):
        """Test that custom fields override default fields for specified keys only"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call with custom fields for page_attachments only
        custom_fields = {
            'page_attachments': 'fileName,title,length'
        }
        
        response = mock_page_attachments_api.get_page_attachment(
            project_id='TEST_PROJECT',
            space_id='TEST_SPACE',
            page_name='TEST_PAGE',
            attachment_id='TEST_ATTACHMENT',
            fields=custom_fields
        )
        
        call_args = mock_page_attachments_api._session.get.call_args
        params = call_args[1]['params']
        
        # Custom field should override
        assert params['fields[page_attachments]'] == 'fileName,title,length'
        
        # Other collections should still be @all
        assert params['fields[workitems]'] == '@all'
        assert params['fields[projects]'] == '@all'
    
    def test_get_page_attachment_error_400(self, mock_page_attachments_api):
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
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_page_attachments_api.get_page_attachment(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify error response
        assert response.status_code == 400
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '400'
        assert errors[0]['title'] == 'Bad Request'
        assert 'Unexpected token' in errors[0]['detail']
    
    def test_get_page_attachment_error_401(self, mock_page_attachments_api):
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
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_page_attachments_api.get_page_attachment(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify error response
        assert response.status_code == 401
        errors = response.json()['errors']
        assert len(errors) == 1
        assert errors[0]['status'] == '401'
        assert errors[0]['title'] == 'Unauthorized'
        assert errors[0]['detail'] == 'No access token'
    
    def test_get_page_attachment_with_revision(self, mock_page_attachments_api):
        """Test get_page_attachment with specific revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "page_attachments",
                "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId",
                "revision": "1234"
            }
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call with revision
        response = mock_page_attachments_api.get_page_attachment(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId',
            revision='1234'
        )
        
        # Verify revision parameter
        call_args = mock_page_attachments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['revision'] == '1234'
        
        # Verify response
        assert response.status_code == 200
        assert response.json()['data']['revision'] == '1234'
    
    def test_get_page_attachment_with_include(self, mock_page_attachments_api):
        """Test get_page_attachment with include parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "page_attachments",
                "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId"
            },
            "included": [
                {
                    "type": "users",
                    "id": "MyUserId"
                },
                {
                    "type": "projects",
                    "id": "MyProjectId"
                }
            ]
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call with include
        response = mock_page_attachments_api.get_page_attachment(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId',
            include='author,project'
        )
        
        # Verify include parameter
        call_args = mock_page_attachments_api._session.get.call_args
        params = call_args[1]['params']
        assert params['include'] == 'author,project'
        
        # Verify response contains included entities
        assert response.status_code == 200
        assert 'included' in response.json()
        assert len(response.json()['included']) == 2
    
    def test_get_page_attachment_relationships(self, mock_page_attachments_api):
        """Test that response contains proper relationships"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "page_attachments",
                "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId",
                "relationships": {
                    "author": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId",
                            "revision": "1234"
                        }
                    },
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": "MyProjectId",
                            "revision": "1234"
                        }
                    }
                }
            }
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        response = mock_page_attachments_api.get_page_attachment(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify relationships structure
        data = response.json()['data']
        assert 'relationships' in data
        assert 'author' in data['relationships']
        assert 'project' in data['relationships']
        assert data['relationships']['author']['data']['type'] == 'users'
        assert data['relationships']['project']['data']['type'] == 'projects'
    
    def test_get_page_attachment_links(self, mock_page_attachments_api):
        """Test that response contains proper links"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "page_attachments",
                "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId",
                "links": {
                    "self": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments/MyAttachmentId?revision=1234",
                    "content": "server-host-name/application-path/projects/MyProjectId/spaces/MySpaceId/pages/MyRichPageId/attachments/MyAttachmentId/content?revision=1234"
                }
            }
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        response = mock_page_attachments_api.get_page_attachment(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify links structure
        data = response.json()['data']
        assert 'links' in data
        assert 'self' in data['links']
        assert 'content' in data['links']
        assert 'attachments/MyAttachmentId' in data['links']['self']
        assert 'content' in data['links']['content']
    
    def test_get_page_attachment_attributes(self, mock_page_attachments_api):
        """Test that response contains all expected attributes"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "page_attachments",
                "id": "MyProjectId/MySpaceId/MyRichPageId/MyAttachmentId",
                "revision": "1234",
                "attributes": {
                    "fileName": "test_file.pdf",
                    "id": "MyAttachmentId",
                    "length": 1024,
                    "title": "Test Attachment",
                    "updated": "1970-01-01T00:00:00Z"
                }
            }
        }
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        response = mock_page_attachments_api.get_page_attachment(
            project_id='MyProjectId',
            space_id='MySpaceId',
            page_name='MyRichPageId',
            attachment_id='MyAttachmentId'
        )
        
        # Verify attributes
        attrs = response.json()['data']['attributes']
        assert attrs['fileName'] == 'test_file.pdf'
        assert attrs['id'] == 'MyAttachmentId'
        assert attrs['length'] == 1024
        assert attrs['title'] == 'Test Attachment'
        assert 'updated' in attrs
    
    def test_get_page_attachment_url_encoding(self, mock_page_attachments_api):
        """Test that special characters in parameters are handled correctly"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "page_attachments"}}
        
        mock_page_attachments_api._session.get.return_value = mock_response
        
        # Call with special characters
        response = mock_page_attachments_api.get_page_attachment(
            project_id='MyProject-123',
            space_id='My Space',
            page_name='My Page Name',
            attachment_id='file-2023.pdf'
        )
        
        # Verify the call was made
        mock_page_attachments_api._session.get.assert_called_once()
        call_args = mock_page_attachments_api._session.get.call_args
        
        # URL should contain the parameters (encoding handled by requests library)
        assert 'MyProject-123' in call_args[0][0]
        assert response.status_code == 200
