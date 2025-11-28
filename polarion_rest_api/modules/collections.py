"""
Collections module for Polarion REST API.
Handles all Collections related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class Collections(PolarionBase):
    """
    Class for handling Collections operations in Polarion REST API.
    Provides methods for creating, reading, updating, and deleting collections.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete collections
    - GET methods: Retrieve collections and related data
    - PATCH methods: Update collections
    - POST methods: Create collections and perform actions
    """
    
    # ========== DELETE methods ==========
        
    def delete_collections_relationship(self,
                                       project_id: str,
                                       collection_id: str,
                                       relationship_id: str,
                                       collections_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Collection Relationships.
        
        Args:
            project_id: The Project ID
            collection_id: The Collection ID
            relationship_id: The Relationship ID
            collections_data: The Collection(s) body in format:
                {
                  "data": [
                    {
                      "type": "collections",
                      "id": "MyProjectId/MyCollectionId"
                    }
                  ]
                }
            
        Returns:
            Response object (204 No Content on success)
            
        Returns:
            Response object
        """
        return self._delete_with_body(
            f'projects/{project_id}/collections/{collection_id}/relationships/{relationship_id}',
            json=collections_data
        )
    
    def delete_collections(self,
                          project_id: str,
                          collections_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Collections from a project.
        
        Args:
            project_id: The Project ID
            collections_data: The Collection(s) body in format:
                {
                  "data": [
                    {
                      "type": "collections",
                      "id": "MyProjectId/MyCollectionId"
                    }
                  ]
                }
            
        Returns:
            Response object (204 No Content on success)
        """
        return self._delete_with_body(
            f'projects/{project_id}/collections',
            json=collections_data
        )
    
    def delete_collection(self,
                         project_id: str,
                         collection_id: str) -> requests.Response:
        """
        Deletes the specified Collection.
        
        Args:
            project_id: The Project ID
            collection_id: The Collection ID
            
        Returns:
            Response object
        """
        return self._delete(f'projects/{project_id}/collections/{collection_id}')

    
    # ========== GET methods ==========
        
    def get_collections_relationship(self,
                                    project_id: str,
                                    collection_id: str,
                                    relationship_id: str,
                                    page_size: Optional[int] = None,
                                    page_number: Optional[int] = None,
                                    fields: Optional[Dict[str, str]] = None,
                                    include: Optional[str] = None,
                                    revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Collection Relationships.
        
        Args:
            project_id: The Project ID
            collection_id: The Collection ID
            relationship_id: The Relationship ID
            page_size: Limit the number of entities returned
            page_number: Specify the page number (starts from 1)
            fields: Filter returned resource fields (sparse fieldsets).
                   Default fields are ALWAYS applied first with all collections set to "@all".
                   If you provide custom fields, they will OVERRIDE only the specified keys,
                   while all other collections remain set to their default "@all" value.
                   
                   Default fields include:
                   - collections, categories, documents, document_attachments, document_comments
                   - document_parts, enumerations, globalroles, icons, jobs
                   - linkedworkitems, externallylinkedworkitems, linkedoslcresources
                   - pages, page_attachments, plans, projectroles, projects, projecttemplates
                   - testparameters, testparameter_definitions, testrecords, teststep_results
                   - testruns, testrun_attachments, teststepresult_attachments, testrun_comments
                   - usergroups, users, workitems, workitem_attachments, workitem_approvals
                   - workitem_comments, featureselections, teststeps, workrecords, revisions
                   - testrecord_attachments
                   
                   All default to "@all" unless overridden.
            include: Include related entities
            revision: The revision ID
            
        Returns:
            Response object with relationships
        """
        params = self._apply_default_fields(fields)
        
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if include:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
        
        return self._get(
            f'projects/{project_id}/collections/{collection_id}/relationships/{relationship_id}',
            params=params
        )
    
    def get_collections(self,
                       project_id: str,
                       page_size: Optional[int] = None,
                       page_number: Optional[int] = None,
                       fields: Optional[Dict[str, str]] = None,
                       include: Optional[str] = None,
                       query: Optional[str] = None,
                       sort: Optional[str] = None,
                       revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Collections in a project.
        
        Args:
            project_id: The Project ID
            page_size: Limit the number of entities returned
            page_number: Specify the page number (starts from 1)
            fields: Filter returned resource fields (sparse fieldsets).
                   Default fields are ALWAYS applied first with all collections set to "@all".
                   If you provide custom fields, they will OVERRIDE only the specified keys,
                   while all other collections remain set to their default "@all" value.
                   
                   Default fields include:
                   - collections, categories, documents, document_attachments, document_comments
                   - document_parts, enumerations, globalroles, icons, jobs
                   - linkedworkitems, externallylinkedworkitems, linkedoslcresources
                   - pages, page_attachments, plans, projectroles, projects, projecttemplates
                   - testparameters, testparameter_definitions, testrecords, teststep_results
                   - testruns, testrun_attachments, teststepresult_attachments, testrun_comments
                   - usergroups, users, workitems, workitem_attachments, workitem_approvals
                   - workitem_comments, featureselections, teststeps, workrecords, revisions
                   - testrecord_attachments
                   
                   All default to "@all" unless overridden.
            include: Include related entities
            query: The query string
            sort: The sort string
            revision: The revision ID
            
        Returns:
            Response object with collections data
        """
        params = self._apply_default_fields(fields)
        
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if include:
            params['include'] = include
        if query:
            params['query'] = query
        if sort:
            params['sort'] = sort
        if revision is not None:
            params['revision'] = revision
        
        return self._get(f'projects/{project_id}/collections', params=params)
    
    def get_collection(self,
                      project_id: str,
                      collection_id: str,
                      fields: Optional[Dict[str, str]] = None,
                      include: Optional[str] = None,
                      revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Collection.
        
        Args:
            project_id: The Project ID
            collection_id: The Collection ID
            fields: Filter returned resource fields (sparse fieldsets).
                   Default fields are ALWAYS applied first with all collections set to "@all".
                   If you provide custom fields, they will OVERRIDE only the specified keys,
                   while all other collections remain set to their default "@all" value.
                   
                   Default fields include:
                   - collections, categories, documents, document_attachments, document_comments
                   - document_parts, enumerations, globalroles, icons, jobs
                   - linkedworkitems, externallylinkedworkitems, linkedoslcresources
                   - pages, page_attachments, plans, projectroles, projects, projecttemplates
                   - testparameters, testparameter_definitions, testrecords, teststep_results
                   - testruns, testrun_attachments, teststepresult_attachments, testrun_comments
                   - usergroups, users, workitems, workitem_attachments, workitem_approvals
                   - workitem_comments, featureselections, teststeps, workrecords, revisions
                   - testrecord_attachments
                   
                   All default to "@all" unless overridden.
            include: Include related entities
            revision: The revision ID
            
        Returns:
            Response object with collection data
        """
        params = self._apply_default_fields(fields)
        if include:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
        
        return self._get(f'projects/{project_id}/collections/{collection_id}', params=params)
    
    # ========== PATCH methods ==========
    
    def patch_collections(self,
                         project_id: str,
                         collection_id: str,
                         collection_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Collection.
        
        Args:
            project_id: The Project ID
            collection_id: The Collection ID
            collection_data: The Collection body in format:
                {
                  "data": {
                    "type": "collections",
                    "id": "MyProjectId/MyCollectionId",
                    "attributes": {
                      "description": {
                        "type": "text/html",
                        "value": "My text value"
                      },
                      "name": "Name"
                    },
                    "relationships": {
                      "documents": {
                        "data": [
                          {
                            "type": "documents",
                            "id": "MyProjectId/MySpaceId/MyDocumentId",
                            "revision": "1234"
                          }
                        ]
                      },
                      "richPages": {
                        "data": [
                          {
                            "type": "pages",
                            "id": "MyProjectId/MySpaceId/MyRichPageId"
                          }
                        ]
                      },
                      "upstreamCollections": {
                        "data": [
                          {
                            "type": "collections",
                            "id": "MyProjectId/MyCollectionId",
                            "revision": "1234"
                          }
                        ]
                      }
                    }
                  }
                }
            
        Returns:
            Response object (204 No Content on success)
            
        Example:
            >>> collection_data = {
            ...     "data": {
            ...         "type": "collections",
            ...         "id": "MyProject/MyCollection",
            ...         "attributes": {
            ...             "name": "Updated Collection Name",
            ...             "description": {
            ...                 "type": "text/html",
            ...                 "value": "<p>Updated description</p>"
            ...             }
            ...         }
            ...     }
            ... }
            >>> response = api.patch_collections(
            ...     project_id="MyProject",
            ...     collection_id="MyCollection",
            ...     collection_data=collection_data
            ... )
        """
        return self._patch(
            f'projects/{project_id}/collections/{collection_id}',
            json=collection_data
        )
    
    def patch_collections_relationships(self,
                                       project_id: str,
                                       collection_id: str,
                                       relationship_id: str,
                                       relationships_data: Dict[str, Any]) -> requests.Response:
        """
        Updates a list of Collection Relationships.
        
        Args:
            project_id: The Project ID
            collection_id: The Collection ID
            relationship_id: The Relationship ID
            relationships_data: The Relationship body in format:
                {
                  "data": [
                    {
                      "type": "MyResourceType",
                      "id": "MyProjectId/MyResourceId",
                      "revision": "1234"
                    }
                  ]
                }
            
        Returns:
            Response object (204 No Content on success)
            
        Example:
            >>> relationships_data = {
            ...     "data": [
            ...         {
            ...             "type": "workitems",
            ...             "id": "MyProject/WI-123",
            ...             "revision": "1234"
            ...         }
            ...     ]
            ... }
            >>> response = api.patch_collections_relationships(
            ...     project_id="MyProject",
            ...     collection_id="MyCollection",
            ...     relationship_id="workitems",
            ...     relationships_data=relationships_data
            ... )
        """
        return self._patch(
            f'projects/{project_id}/collections/{collection_id}/relationships/{relationship_id}',
            json=relationships_data
        )
    
    # ========== POST methods ==========
    
    def post_collections(self,
                        project_id: str,
                        collections_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Collections.
        
        Args:
            project_id: The Project ID
            collections_data: The Collection(s) body in format:
                {
                  "data": [
                    {
                      "type": "collections",
                      "attributes": {
                        "description": {
                          "type": "text/html",
                          "value": "My text value"
                        },
                        "id": "ID",
                        "name": "Name"
                      },
                      "relationships": {
                        "documents": {
                          "data": [
                            {
                              "type": "documents",
                              "id": "MyProjectId/MySpaceId/MyDocumentId",
                              "revision": "1234"
                            }
                          ]
                        },
                        "richPages": {
                          "data": [
                            {
                              "type": "pages",
                              "id": "MyProjectId/MySpaceId/MyRichPageId"
                            }
                          ]
                        },
                        "upstreamCollections": {
                          "data": [
                            {
                              "type": "collections",
                              "id": "MyProjectId/MyCollectionId",
                              "revision": "1234"
                            }
                          ]
                        }
                      }
                    }
                  ]
                }
            
        Returns:
            Response object (201 Created)
            
        Example:
            >>> collections_data = {
            ...     "data": [
            ...         {
            ...             "type": "collections",
            ...             "attributes": {
            ...                 "id": "MyNewCollection",
            ...                 "name": "My New Collection",
            ...                 "description": {
            ...                     "type": "text/html",
            ...                     "value": "<p>Collection description</p>"
            ...                 }
            ...             },
            ...             "relationships": {
            ...                 "documents": {
            ...                     "data": [
            ...                         {
            ...                             "type": "documents",
            ...                             "id": "MyProject/MySpace/Doc1",
            ...                             "revision": "1234"
            ...                         }
            ...                     ]
            ...                 }
            ...             }
            ...         }
            ...     ]
            ... }
            >>> response = api.post_collections(
            ...     project_id="MyProject",
            ...     collections_data=collections_data
            ... )
        """
        return self._post(
            f'projects/{project_id}/collections',
            json=collections_data
        )
    
    def post_close_collection(self,
                        project_id: str,
                        collection_id: str) -> requests.Response:
        """
        Closes the specified Collection.
        
        Args:
            project_id: The Project ID
            collection_id: The Collection ID
            
        Returns:
            Response object
        """
        return self._post(
            f'projects/{project_id}/collections/{collection_id}/actions/close',
            json={}
        )
    
    def post_reopen_collection(self,
                         project_id: str,
                         collection_id: str) -> requests.Response:
        """
        Reopens the specified Collection.
        
        Args:
            project_id: The Project ID
            collection_id: The Collection ID
            
        Returns:
            Response object
        """
        return self._post(
            f'projects/{project_id}/collections/{collection_id}/actions/reopen',
            json={}
        )
    
    def post_collections_relationships(self,
                                      project_id: str,
                                      collection_id: str,
                                      relationship_id: str,
                                      relationships_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Collection Relationships.
        
        Args:
            project_id: The Project ID
            collection_id: The Collection ID
            relationship_id: The Relationship ID
            relationships_data: The Relationship body in format:
                {
                  "data": [
                    {
                      "type": "MyResourceType",
                      "id": "MyProjectId/MyResourceId",
                      "revision": "1234"
                    }
                  ]
                }
            
        Returns:
            Response object (201 Created)
            
        Example:
            >>> relationships_data = {
            ...     "data": [
            ...         {
            ...             "type": "workitems",
            ...             "id": "MyProject/WI-123",
            ...             "revision": "1234"
            ...         },
            ...         {
            ...             "type": "workitems",
            ...             "id": "MyProject/WI-456",
            ...             "revision": "5678"
            ...         }
            ...     ]
            ... }
            >>> response = api.post_collections_relationships(
            ...     project_id="MyProject",
            ...     collection_id="MyCollection",
            ...     relationship_id="workitems",
            ...     relationships_data=relationships_data
            ... )
        """
        return self._post(
            f'projects/{project_id}/collections/{collection_id}/relationships/{relationship_id}',
            json=relationships_data
        )
    
    # ========== Helper methods ==========
    
    def _delete_with_body(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Helper method for DELETE requests with body (not standard in requests library).
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments for the request
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._session.request('DELETE', url, **kwargs)
