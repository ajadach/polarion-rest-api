"""
Linked Work Items module for Polarion REST API.
Handles all Linked Work Items related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class LinkedWorkItems(PolarionBase):
    """
    Class for handling Linked Work Items operations in Polarion REST API.
    Provides methods for creating, reading, updating, and deleting linked work items.
    
    Returns the direct outgoing links to other Work Items (same as the corresponding Java API method).
    Does not pertain to external links or backlinks.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete linked work items
    - GET methods: Retrieve linked work items
    - PATCH methods: Update linked work items
    - POST methods: Create linked work items
    """
    
    # ========== DELETE methods ==========   
    
    def delete_linked_work_items(self,
                                 project_id: str,
                                 work_item_id: str,
                                 linked_items_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Linked Work Items.
        Deletes the direct outgoing links to other Work Items.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            linked_items_data: The Linked Work Item(s) body
            
        Returns:
            Response object
        """
        return self._delete_with_body(
            f'projects/{project_id}/workitems/{work_item_id}/linkedworkitems',
            json=linked_items_data
        )
    
    def delete_linked_work_item(self,
                                project_id: str,
                                work_item_id: str,
                                role_id: str,
                                target_project_id: str,
                                linked_work_item_id: str) -> requests.Response:
        """
        Deletes the specified Linked Work Item.
        Deletes the direct outgoing links to other Work Items.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            role_id: The Role ID
            target_project_id: The Target Project ID
            linked_work_item_id: The Linked Work Item ID
            
        Returns:
            Response object
        """
        return self._delete(
            f'projects/{project_id}/workitems/{work_item_id}/linkedworkitems/{role_id}/{target_project_id}/{linked_work_item_id}'
        )
    
    # ========== GET methods ==========
    
    def get_linked_work_items(self,
                             project_id: str,
                             work_item_id: str,
                             page_size: Optional[int] = None,
                             page_number: Optional[int] = None,
                             fields: Optional[Dict[str, str]] = None,
                             include: Optional[str] = None,
                             revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Linked Work Items.
        Returns the direct outgoing links to other Work Items.
        
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
            Response object containing list of linked work items
        """
        # Start with default fields
        params = self._apply_default_fields(fields)
        
        # Add pagination parameters (these override any fields settings)
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/linkedworkitems',
            params=params if params else None
        )

    def get_linked_work_item(self,
                            project_id: str,
                            work_item_id: str,
                            role_id: str,
                            target_project_id: str,
                            linked_work_item_id: str,
                            fields: Optional[Dict[str, str]] = None,
                            include: Optional[str] = None,
                            revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Linked Work Item.
        Returns the direct outgoing links to other Work Items.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            role_id: The Role ID
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
            Response object containing the linked work item
        """
        # Start with default fields
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/linkedworkitems/{role_id}/{target_project_id}/{linked_work_item_id}',
            params=params if params else None
        )
    
    # ========== PATCH methods ==========
    
    def patch_linked_work_item(self,
                               project_id: str,
                               work_item_id: str,
                               role_id: str,
                               target_project_id: str,
                               linked_work_item_id: str,
                               linked_item_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Linked Work Item.
        Updates the direct outgoing links to other Work Items.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            role_id: The Role ID
            target_project_id: The Target Project ID
            linked_work_item_id: The Linked Work Item ID
            linked_item_data: The Linked Work Item(s) body
            
        Returns:
            Response object
        """
        return self._patch(
            f'projects/{project_id}/workitems/{work_item_id}/linkedworkitems/{role_id}/{target_project_id}/{linked_work_item_id}',
            json=linked_item_data
        )
    
    # ========== POST methods ==========
    
    def post_linked_work_items(self,
                              project_id: str,
                              work_item_id: str,
                              linked_items_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Linked Work Items.
        Creates the direct outgoing links to other Work Items.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            linked_items_data: The Linked Work Item(s) body
            
        Returns:
            Response object
        """
        return self._post(
            f'projects/{project_id}/workitems/{work_item_id}/linkedworkitems',
            json=linked_items_data
        )
