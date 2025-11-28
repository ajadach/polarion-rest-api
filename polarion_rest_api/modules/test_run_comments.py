"""
Test Run Comments module for Polarion REST API.
Handles all Test Run Comments related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class TestRunComments(PolarionBase):
    """
    Class for handling Test Run Comments operations in Polarion REST API.
    Provides methods for creating, reading, and updating test run comments.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve test run comments
    - PATCH methods: Update test run comments
    - POST methods: Create test run comments
    """
    
    # ========== GET methods ==========
    
    def get_test_run_comments(
        self,
        project_id: str,
        test_run_id: str,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None
    ) -> requests.Response:
        """
        Returns a list of Test Run Comments.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
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
            Response object containing list of Test Run Comments
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/comments"
        params = self._apply_default_fields(fields)
        
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params)
    
    def get_test_run_comment(
        self,
        project_id: str,
        test_run_id: str,
        comment_id: str,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None
    ) -> requests.Response:
        """
        Returns the specified Test Run Comment.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
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
            Response object containing the Test Run Comment
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/comments/{comment_id}"
        params = self._apply_default_fields(fields)
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params)
    
    # ========== PATCH methods ==========
    
    def patch_test_run_comments(
        self,
        project_id: str,
        test_run_id: str,
        comments_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Updates a list of Test Run Comments.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            comments_data: The Comment body
            
        Returns:
            Response object (204 No Content on success)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/comments"
        return self._patch(endpoint, json=comments_data)
    
    def patch_test_run_comment(
        self,
        project_id: str,
        test_run_id: str,
        comment_id: str,
        comment_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Updates the specified Test Run Comment.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            comment_id: The Comment ID
            comment_data: The Comment body
            
        Returns:
            Response object (204 No Content on success)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/comments/{comment_id}"
        return self._patch(endpoint, json=comment_data)
    
    # ========== POST methods ==========
    
    def post_test_run_comments(
        self,
        project_id: str,
        test_run_id: str,
        comments_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Creates a list of Test Run Comments.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            comments_data: The Comment(s) body
            
        Returns:
            Response object (201 Created)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/comments"
        return self._post(endpoint, json=comments_data)
