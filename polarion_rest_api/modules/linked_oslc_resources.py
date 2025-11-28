"""
Linked Oslc Resources module for Polarion REST API.
Handles all Linked Oslc Resources related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class LinkedOslcResources(PolarionBase):
    """
    Class for handling Linked Oslc Resources operations in Polarion REST API.
    Provides methods for creating, reading, and deleting linked OSLC resources.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete linked OSLC resources
    - GET methods: Retrieve linked OSLC resources
    - POST methods: Create linked OSLC resources
    """
    
    # ========== DELETE methods ==========
    
    def delete_oslc_resources(self,
                             project_id: str,
                             work_item_id: str,
                             oslc_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of instances.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            oslc_data: The Linked Oslc Item(s) body
            
        Returns:
            Response object
        """
        return self._delete_with_body(
            f'projects/{project_id}/workitems/{work_item_id}/linkedoslcresources',
            json=oslc_data
        )
    
    # ========== GET methods ==========
    
    def get_oslc_resources(self,
                          project_id: str,
                          work_item_id: str,
                          page_size: Optional[int] = None,
                          page_number: Optional[int] = None,
                          fields: Optional[Dict[str, str]] = None,
                          include: Optional[str] = None,
                          query: Optional[str] = None,
                          sort: Optional[str] = None,
                          revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of instances.
        
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
            query: The query string
            sort: The sort string
            revision: The revision ID
            
        Returns:
            Response object containing list of linked OSLC resources
        """
        params = {}
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        
        # Apply default fields and merge with existing params
        default_fields = self._apply_default_fields(fields)
        params.update(default_fields)
        
        if include is not None:
            params['include'] = include
        if query is not None:
            params['query'] = query
        if sort is not None:
            params['sort'] = sort
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/linkedoslcresources',
            params=params if params else None
        )
    
    # ========== POST methods ==========
    
    def post_oslc_resources(self,
                           project_id: str,
                           work_item_id: str,
                           oslc_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of instances.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            oslc_data: The Linked Oslc Item(s) body
            
        Returns:
            Response object
        """
        return self._post(
            f'projects/{project_id}/workitems/{work_item_id}/linkedoslcresources',
            json=oslc_data
        )
