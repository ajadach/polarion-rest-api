"""
Work Item Comments module for Polarion REST API.
Handles all Work Item Comments related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class WorkItemComments(PolarionBase):
    """
    Class for handling Work Item Comments operations in Polarion REST API.
    Provides methods for creating, reading, and updating work item comments.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve work item comments
    - PATCH methods: Update work item comments
    - POST methods: Create work item comments
    """
    
    # ========== GET methods ==========
    
    def get_comments(self, 
                     project_id: str,
                     work_item_id: str,
                     page_size: Optional[int] = None,
                     page_number: Optional[int] = None,
                     fields: Optional[Dict[str, str]] = None,
                     include: Optional[str] = None,
                     revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Work Item Comments.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
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
            Response object with work item comments data
        """
        params = self._apply_default_fields(fields)
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
        
        return self._get(f'projects/{project_id}/workitems/{work_item_id}/comments', params=params)
    
    def get_comment(self, 
                    project_id: str,
                    work_item_id: str,
                    comment_id: str,
                    fields: Optional[Dict[str, str]] = None,
                    include: Optional[str] = None,
                    revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Work Item Comment.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            comment_id: The Comment ID
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
            Response object with work item comment data
        """
        params = self._apply_default_fields(fields)
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
        
        return self._get(f'projects/{project_id}/workitems/{work_item_id}/comments/{comment_id}', 
                        params=params)
    
    # ========== PATCH methods ==========
    
    def patch_comment(self, 
                     project_id: str,
                     work_item_id: str,
                     comment_id: str,
                     comment_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Work Item Comment.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            comment_id: The Comment ID
            comment_data: The Comment body
            
        Returns:
            Response object
        """
        return self._patch(f'projects/{project_id}/workitems/{work_item_id}/comments/{comment_id}', 
                          json=comment_data)
    
    # ========== POST methods ==========
    
    def post_comments(self, 
                     project_id: str,
                     work_item_id: str,
                     comments_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Work Item Comments.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            comments_data: The Comment(s) body
            
        Returns:
            Response object with created comments
        """
        return self._post(f'projects/{project_id}/workitems/{work_item_id}/comments', 
                         json=comments_data)
