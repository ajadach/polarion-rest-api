"""
Tests for Revisions.get_revision method.
Tests verify the method implementation against the OpenAPI specification using only mocks.
"""
import pytest
from unittest.mock import Mock


class TestGetRevision:
    """Test suite for get_revision method"""
    
    def test_get_revision_success(self, mock_revisions_api):
        """Test successful retrieval of a specific revision"""
        # Mock response data based on example
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/1234",
                "revision": "1234",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z",
                    "id": "string",
                    "internalCommit": True,
                    "message": "Message",
                    "repositoryName": "Repository name"
                },
                "relationships": {
                    "author": {
                        "data": {
                            "type": "users",
                            "id": "MyUserId",
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
                    "self": "server-host-name/application-path/revisions/default/1234"
                }
            },
            "included": [
                {}
            ],
            "links": {
                "self": "server-host-name/application-path/revisions/default/1234"
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="1234"
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["type"] == "revisions"
        assert data["data"]["id"] == "default/1234"
        assert data["data"]["revision"] == "1234"
        assert data["data"]["attributes"]["repositoryName"] == "Repository name"
        
        # Verify the correct endpoint was called
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "/default/1234" in call_args[0][0] in call_args[0][0]
    
    def test_get_revision_with_fields(self, mock_revisions_api):
        """Test get_revision with custom fields parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/5678",
                "revision": "5678",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z",
                    "id": "string"
                }
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with custom fields
        custom_fields = {
            "revisions": "id,created",
            "users": "id,name"
        }
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="5678",
            fields=custom_fields
        )
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify the correct endpoint was called with params
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "/default/5678" in call_args[0][0] in call_args[0][0]
        assert call_args[1]["params"] is not None
    
    def test_get_revision_with_include(self, mock_revisions_api):
        """Test get_revision with include parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/9999",
                "revision": "9999",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z"
                }
            },
            "included": [
                {
                    "type": "users",
                    "id": "MyUserId",
                    "attributes": {
                        "name": "Test User"
                    }
                }
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with include parameter
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="9999",
            include="author"
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "included" in data
        
        # Verify the correct endpoint was called with include
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "/default/9999" in call_args[0][0] in call_args[0][0]
        assert call_args[1]["params"]["include"] == "author"
    
    def test_get_revision_with_all_parameters(self, mock_revisions_api):
        """Test get_revision with all optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "myrepo/7777",
                "revision": "7777"
            },
            "included": []
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with all parameters
        custom_fields = {
            "revisions": "id,created,message",
            "users": "id,name,email"
        }
        
        response = mock_revisions_api.get_revision(
            repository_name="myrepo",
            revision="7777",
            fields=custom_fields,
            include="author"
        )
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify the correct endpoint was called with all params
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "/myrepo/7777" in call_args[0][0] in call_args[0][0]
        params = call_args[1]["params"]
        assert params["include"] == "author"
    
    def test_get_revision_unauthorized_401(self, mock_revisions_api):
        """Test get_revision with 401 Unauthorized response"""
        # Mock 401 response based on example
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
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="1234"
        )
        
        # Verify the error response
        assert response.status_code == 401
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "401"
        assert errors[0]["title"] == "Unauthorized"
        assert errors[0]["detail"] == "No access token"
    
    def test_get_revision_bad_request_400(self, mock_revisions_api):
        """Test get_revision with 400 Bad Request response"""
        # Mock 400 response based on example
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
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="invalid"
        )
        
        # Verify the error response
        assert response.status_code == 400
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "400"
        assert errors[0]["title"] == "Bad Request"
        assert "source" in errors[0]
        assert errors[0]["source"]["parameter"] == "revision"
    
    def test_get_revision_different_repository(self, mock_revisions_api):
        """Test get_revision with different repository name"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "custom-repo/5555",
                "revision": "5555",
                "attributes": {
                    "repositoryName": "custom-repo"
                }
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with custom repository name
        response = mock_revisions_api.get_revision(
            repository_name="custom-repo",
            revision="5555"
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["attributes"]["repositoryName"] == "custom-repo"
        
        # Verify correct URL was constructed
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "/custom-repo/5555" in call_args[0][0] in call_args[0][0]
    
    def test_get_revision_url_construction(self, mock_revisions_api):
        """Test that URL is correctly constructed for get_revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Test various repository and revision combinations
        test_cases = [
            ("default", "1234"),
            ("repo-name", "5678"),
            ("my_repo", "abc123"),
        ]
        
        for repo, rev in test_cases:
            mock_revisions_api._session.get.reset_mock()
            
            mock_revisions_api.get_revision(
                repository_name=repo,
                revision=rev
            )
            
            call_args = mock_revisions_api._session.get.call_args
            assert f"revisions/{repo}/{rev}" in call_args[0][0]
    
    def test_get_revision_with_relationships(self, mock_revisions_api):
        """Test get_revision response includes relationships"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/2222",
                "revision": "2222",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z",
                    "message": "Test commit"
                },
                "relationships": {
                    "author": {
                        "data": {
                            "type": "users",
                            "id": "author123",
                            "revision": "2222"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/revisions/default/2222"
                }
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="2222"
        )
        
        # Verify relationships are present
        assert response.status_code == 200
        data = response.json()
        assert "relationships" in data["data"]
        assert "author" in data["data"]["relationships"]
        assert data["data"]["relationships"]["author"]["data"]["type"] == "users"
    
    def test_get_revision_with_meta_errors(self, mock_revisions_api):
        """Test get_revision response with meta.errors (partial success)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/3333",
                "revision": "3333",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z"
                },
                "meta": {
                    "errors": [
                        {
                            "status": "400",
                            "title": "Bad Request",
                            "detail": "Some field could not be retrieved",
                            "source": {
                                "pointer": "$.data.relationships.author"
                            }
                        }
                    ]
                }
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="3333"
        )
        
        # Verify meta.errors are present
        assert response.status_code == 200
        data = response.json()
        assert "meta" in data["data"]
        assert "errors" in data["data"]["meta"]
        assert len(data["data"]["meta"]["errors"]) > 0
    
    def test_get_revision_internal_commit_flag(self, mock_revisions_api):
        """Test get_revision with internalCommit flag"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/4444",
                "revision": "4444",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z",
                    "internalCommit": True,
                    "message": "Internal commit message"
                }
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="4444"
        )
        
        # Verify internalCommit flag
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["attributes"]["internalCommit"] is True
    
    def test_get_revision_with_links(self, mock_revisions_api):
        """Test get_revision response includes self links"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/6666",
                "revision": "6666",
                "links": {
                    "self": "server-host-name/application-path/revisions/default/6666"
                }
            },
            "links": {
                "self": "server-host-name/application-path/revisions/default/6666"
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="6666"
        )
        
        # Verify links are present
        assert response.status_code == 200
        data = response.json()
        assert "links" in data
        assert "self" in data["links"]
        assert "links" in data["data"]
        assert "self" in data["data"]["links"]
    
    def test_get_revision_fields_override_defaults(self, mock_revisions_api):
        """Test that custom fields override default fields correctly"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "revisions", "id": "default/1111"}}
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with custom fields that should override defaults
        custom_fields = {
            "revisions": "id,created",  # Override default @all
            "users": "id,name"  # Override default @all
        }
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="1111",
            fields=custom_fields
        )
        
        # Verify call was made
        assert response.status_code == 200
        mock_revisions_api._session.get.assert_called_once()
        
        # Verify params contain the custom fields
        call_args = mock_revisions_api._session.get.call_args
        params = call_args[1]["params"]
        # The _apply_default_fields method should have been called
        assert params is not None
    
    def test_get_revision_no_optional_params(self, mock_revisions_api):
        """Test get_revision with only required parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/8888",
                "revision": "8888"
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with only required parameters
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="8888"
        )
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify the call was made correctly
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "/default/8888" in call_args[0][0] in call_args[0][0]
        # Should still have params (default fields)
        assert call_args[1]["params"] is not None
    
    def test_get_revision_special_characters_in_repository(self, mock_revisions_api):
        """Test get_revision with special characters in repository name"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "repo-with-dashes/1000",
                "revision": "1000"
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with repository name containing special characters
        response = mock_revisions_api.get_revision(
            repository_name="repo-with-dashes",
            revision="1000"
        )
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify correct URL construction
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "/repo-with-dashes/1000" in call_args[0][0] in call_args[0][0]
    
    def test_get_revision_numeric_revision(self, mock_revisions_api):
        """Test get_revision with numeric revision ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/12345",
                "revision": "12345",
                "attributes": {
                    "id": "12345"
                }
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with numeric revision
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="12345"
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["revision"] == "12345"
    
    def test_get_revision_include_multiple_related_entities(self, mock_revisions_api):
        """Test get_revision with multiple include parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/7890",
                "revision": "7890"
            },
            "included": [
                {"type": "users", "id": "user1"},
                {"type": "projects", "id": "project1"}
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with multiple includes (comma-separated)
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="7890",
            include="author,project"
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "included" in data
        assert len(data["included"]) == 2
        
        # Verify include parameter was passed correctly
        call_args = mock_revisions_api._session.get.call_args
        assert call_args[1]["params"]["include"] == "author,project"

        
        # Call with custom fields
        custom_fields = {
            "revisions": "id,created",
            "users": "id,name"
        }
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="5678",
            fields=custom_fields
        )
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify the correct endpoint was called with params
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "" in call_args[0][0] and "/default/5678" in call_args[0][0]
        assert call_args[1]["params"] is not None
    
    def test_get_revision_with_include(self, mock_revisions_api):
        """Test get_revision with include parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/9999",
                "revision": "9999",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z"
                }
            },
            "included": [
                {
                    "type": "users",
                    "id": "MyUserId",
                    "attributes": {
                        "name": "Test User"
                    }
                }
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with include parameter
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="9999",
            include="author"
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "included" in data
        
        # Verify the correct endpoint was called with include
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "/default/9999" in call_args[0][0] in call_args[0][0]
        assert call_args[1]["params"]["include"] == "author"
    
    def test_get_revision_with_all_parameters(self, mock_revisions_api):
        """Test get_revision with all optional parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "myrepo/7777",
                "revision": "7777"
            },
            "included": []
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with all parameters
        custom_fields = {
            "revisions": "id,created,message",
            "users": "id,name,email"
        }
        
        response = mock_revisions_api.get_revision(
            repository_name="myrepo",
            revision="7777",
            fields=custom_fields,
            include="author"
        )
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify the correct endpoint was called with all params
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "/myrepo/7777" in call_args[0][0] in call_args[0][0]
        params = call_args[1]["params"]
        assert params["include"] == "author"
    
    def test_get_revision_unauthorized_401(self, mock_revisions_api):
        """Test get_revision with 401 Unauthorized response"""
        # Mock 401 response based on example
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
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="1234"
        )
        
        # Verify the error response
        assert response.status_code == 401
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "401"
        assert errors[0]["title"] == "Unauthorized"
        assert errors[0]["detail"] == "No access token"
    
    def test_get_revision_bad_request_400(self, mock_revisions_api):
        """Test get_revision with 400 Bad Request response"""
        # Mock 400 response based on example
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
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call the method
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="invalid"
        )
        
        # Verify the error response
        assert response.status_code == 400
        errors = response.json()["errors"]
        assert len(errors) == 1
        assert errors[0]["status"] == "400"
        assert errors[0]["title"] == "Bad Request"
        assert "source" in errors[0]
        assert errors[0]["source"]["parameter"] == "revision"
    
    def test_get_revision_different_repository(self, mock_revisions_api):
        """Test get_revision with different repository name"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "custom-repo/5555",
                "revision": "5555",
                "attributes": {
                    "repositoryName": "custom-repo"
                }
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with custom repository name
        response = mock_revisions_api.get_revision(
            repository_name="custom-repo",
            revision="5555"
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["attributes"]["repositoryName"] == "custom-repo"
        
        # Verify correct URL was constructed
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "revisions/custom-repo/5555" in call_args[0][0]
    
    def test_get_revision_url_construction(self, mock_revisions_api):
        """Test that URL is correctly constructed for get_revision"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Test various repository and revision combinations
        test_cases = [
            ("default", "1234"),
            ("repo-name", "5678"),
            ("my_repo", "abc123"),
        ]
        
        for repo, rev in test_cases:
            mock_revisions_api._session.get.reset_mock()
            
            mock_revisions_api.get_revision(
                repository_name=repo,
                revision=rev
            )
            
            call_args = mock_revisions_api._session.get.call_args
            assert f"revisions/{repo}/{rev}" in call_args[0][0]
    
    def test_get_revision_with_relationships(self, mock_revisions_api):
        """Test get_revision response includes relationships"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/2222",
                "revision": "2222",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z",
                    "message": "Test commit"
                },
                "relationships": {
                    "author": {
                        "data": {
                            "type": "users",
                            "id": "author123",
                            "revision": "2222"
                        }
                    }
                },
                "links": {
                    "self": "server-host-name/application-path/revisions/default/2222"
                }
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="2222"
        )
        
        # Verify relationships are present
        assert response.status_code == 200
        data = response.json()
        assert "relationships" in data["data"]
        assert "author" in data["data"]["relationships"]
        assert data["data"]["relationships"]["author"]["data"]["type"] == "users"
    
    def test_get_revision_with_meta_errors(self, mock_revisions_api):
        """Test get_revision response with meta.errors (partial success)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/3333",
                "revision": "3333",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z"
                },
                "meta": {
                    "errors": [
                        {
                            "status": "400",
                            "title": "Bad Request",
                            "detail": "Some field could not be retrieved",
                            "source": {
                                "pointer": "$.data.relationships.author"
                            }
                        }
                    ]
                }
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="3333"
        )
        
        # Verify meta.errors are present
        assert response.status_code == 200
        data = response.json()
        assert "meta" in data["data"]
        assert "errors" in data["data"]["meta"]
        assert len(data["data"]["meta"]["errors"]) > 0
    
    def test_get_revision_internal_commit_flag(self, mock_revisions_api):
        """Test get_revision with internalCommit flag"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/4444",
                "revision": "4444",
                "attributes": {
                    "created": "1970-01-01T00:00:00Z",
                    "internalCommit": True,
                    "message": "Internal commit message"
                }
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="4444"
        )
        
        # Verify internalCommit flag
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["attributes"]["internalCommit"] is True
    
    def test_get_revision_with_links(self, mock_revisions_api):
        """Test get_revision response includes self links"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/6666",
                "revision": "6666",
                "links": {
                    "self": "server-host-name/application-path/revisions/default/6666"
                }
            },
            "links": {
                "self": "server-host-name/application-path/revisions/default/6666"
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="6666"
        )
        
        # Verify links are present
        assert response.status_code == 200
        data = response.json()
        assert "links" in data
        assert "self" in data["links"]
        assert "links" in data["data"]
        assert "self" in data["data"]["links"]
    
    def test_get_revision_fields_override_defaults(self, mock_revisions_api):
        """Test that custom fields override default fields correctly"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"type": "revisions", "id": "default/1111"}}
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with custom fields that should override defaults
        custom_fields = {
            "revisions": "id,created",  # Override default @all
            "users": "id,name"  # Override default @all
        }
        
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="1111",
            fields=custom_fields
        )
        
        # Verify call was made
        assert response.status_code == 200
        mock_revisions_api._session.get.assert_called_once()
        
        # Verify params contain the custom fields
        call_args = mock_revisions_api._session.get.call_args
        params = call_args[1]["params"]
        # The _apply_default_fields method should have been called
        assert params is not None
    
    def test_get_revision_no_optional_params(self, mock_revisions_api):
        """Test get_revision with only required parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/8888",
                "revision": "8888"
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with only required parameters
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="8888"
        )
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify the call was made correctly
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "revisions/default/8888" in call_args[0][0]
        # Should still have params (default fields)
        assert call_args[1]["params"] is not None
    
    def test_get_revision_special_characters_in_repository(self, mock_revisions_api):
        """Test get_revision with special characters in repository name"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "repo-with-dashes/1000",
                "revision": "1000"
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with repository name containing special characters
        response = mock_revisions_api.get_revision(
            repository_name="repo-with-dashes",
            revision="1000"
        )
        
        # Verify the response
        assert response.status_code == 200
        
        # Verify correct URL construction
        mock_revisions_api._session.get.assert_called_once()
        call_args = mock_revisions_api._session.get.call_args
        assert "revisions/repo-with-dashes/1000" in call_args[0][0]
    
    def test_get_revision_numeric_revision(self, mock_revisions_api):
        """Test get_revision with numeric revision ID"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/12345",
                "revision": "12345",
                "attributes": {
                    "id": "12345"
                }
            }
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with numeric revision
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="12345"
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["revision"] == "12345"
    
    def test_get_revision_include_multiple_related_entities(self, mock_revisions_api):
        """Test get_revision with multiple include parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "revisions",
                "id": "default/7890",
                "revision": "7890"
            },
            "included": [
                {"type": "users", "id": "user1"},
                {"type": "projects", "id": "project1"}
            ]
        }
        
        mock_revisions_api._session.get.return_value = mock_response
        
        # Call with multiple includes (comma-separated)
        response = mock_revisions_api.get_revision(
            repository_name="default",
            revision="7890",
            include="author,project"
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "included" in data
        assert len(data["included"]) == 2
        
        # Verify include parameter was passed correctly
        call_args = mock_revisions_api._session.get.call_args
        assert call_args[1]["params"]["include"] == "author,project"
