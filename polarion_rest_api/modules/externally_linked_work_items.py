"""
Externally Linked Work Items module for Polarion REST API.
Handles all Externally Linked Work Items related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class ExternallyLinkedWorkItems(PolarionBase):
    """
    Class for handling Externally Linked Work Items operations in Polarion REST API.
    Provides methods for creating, reading, and deleting externally linked work items.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete externally linked work items
    - GET methods: Retrieve externally linked work items
    - POST methods: Create externally linked work items
    """
    
    # ========== DELETE methods ==========
    
    def delete_externally_linked_work_item(self,
                                          project_id: str,
                                          work_item_id: str,
                                          role_id: str,
                                          hostname: str,
                                          target_project_id: str,
                                          linked_work_item_id: str) -> requests.Response:
        """
        Deletes the specified Externally Linked Work Item.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            role_id: The Role ID
            hostname: The Target Hostname
            target_project_id: The Target Project ID
            linked_work_item_id: The Linked Work Item ID
            
        Returns:
            Response object (204 No Content on success)
        """
        return self._delete(
            f'projects/{project_id}/workitems/{work_item_id}/externallylinkedworkitems/'
            f'{role_id}/{hostname}/{target_project_id}/{linked_work_item_id}'
        )
    
    def delete_externally_linked_work_items(self,
                                           project_id: str,
                                           work_item_id: str,
                                           external_links_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Externally Linked Work Items.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            external_links_data: The Externally Linked Work Item(s) body. Expected structure:
                                {
                                    "data": [
                                        {
                                            "type": "externallylinkedworkitems",
                                            "id": "MyProjectId/MyWorkItemId/parent/hostname/MyProjectId/MyLinkedWorkItemId"
                                        }
                                    ]
                                }
                                
                                The ID format is: {projectId}/{workItemId}/{role}/{hostname}/{targetProjectId}/{linkedWorkItemId}
                                Common roles: parent, child, relates, duplicates, blocks, depends_on
            
        Returns:
            Response object (204 No Content on success)
        """
        return self._delete_with_body(
            f'projects/{project_id}/workitems/{work_item_id}/externallylinkedworkitems',
            json=external_links_data
        )
    
    # ========== GET methods ==========
    
    def get_externally_linked_work_item(self,
                                       project_id: str,
                                       work_item_id: str,
                                       role_id: str,
                                       hostname: str,
                                       target_project_id: str,
                                       linked_work_item_id: str,
                                       fields: Optional[Dict[str, str]] = None,
                                       include: Optional[str] = None,
                                       revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Externally Linked Work Item.
        Returns the external links to other Work Items.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            role_id: The Role ID
            hostname: The Target Hostname
            target_project_id: The Target Project ID
            linked_work_item_id: The Linked Work Item ID
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
            Response object containing the externally linked work item
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/externallylinkedworkitems/'
            f'{role_id}/{hostname}/{target_project_id}/{linked_work_item_id}',
            params=params if params else None
        )
    
    def get_externally_linked_work_items(self,
                                        project_id: str,
                                        work_item_id: str,
                                        page_size: Optional[int] = None,
                                        page_number: Optional[int] = None,
                                        fields: Optional[Dict[str, str]] = None,
                                        include: Optional[str] = None,
                                        revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Externally Linked Work Items.
        Returns the external links to other Work Items.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            page_size: Limit the number of entities returned in a single response
            page_number: Specify the page number to be returned (counting starts from 1)
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
            Response object containing list of externally linked work items
        """
        params = self._apply_default_fields(fields)
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/externallylinkedworkitems',
            params=params if params else None
        )
    
    # ========== POST methods ==========
    
    def post_externally_linked_work_items(self,
                                         project_id: str,
                                         work_item_id: str,
                                         external_links_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Externally Linked Work Items.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            external_links_data: The Externally Linked Work Item(s) body. Expected structure:
                                {
                                    "data": [
                                        {
                                            "type": "externallylinkedworkitems",
                                            "attributes": {
                                                "role": "relates_to",
                                                "workItemURI": "string"
                                            }
                                        }
                                    ]
                                }
                                
                                Common roles: parent, child, relates_to, duplicates, blocks, depends_on
                                workItemURI: The URI of the external work item
            
        Returns:
            Response object (201 Created). Response structure:
                {
                    "data": [
                        {
                            "type": "externallylinkedworkitems",
                            "id": "MyProjectId/MyWorkItemId/parent/hostname/MyProjectId/MyLinkedWorkItemId",
                            "links": {
                                "self": "server-host-name/application-path/projects/MyProjectId/workitems/MyWorkItemId/externallylinkedworkitems/parent/hostname/MyProjectId/MyLinkedWorkItemId?revision=1234"
                            }
                        }
                    ]
                }
        """
        return self._post(
            f'projects/{project_id}/workitems/{work_item_id}/externallylinkedworkitems',
            json=external_links_data
        )
