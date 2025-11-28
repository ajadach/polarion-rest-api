"""
Test Steps module for Polarion REST API.
Handles all Test Steps related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class TestSteps(PolarionBase):
    """
    Class for handling Test Steps operations in Polarion REST API.
    Provides methods for creating, reading, updating, and deleting test steps.
    
    Test Steps are components of test work items that define individual test actions.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete test steps
    - GET methods: Retrieve test steps
    - PATCH methods: Update test steps
    - POST methods: Create test steps
    """
    
    # ========== DELETE methods ==========
    
    def delete_test_step(self,
                        project_id: str,
                        work_item_id: str,
                        test_step_index: str) -> requests.Response:
        """
        Deletes the specified Test Step.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            test_step_index: The Test Step index
            
        Returns:
            Response object
        """
        return self._delete(f'projects/{project_id}/workitems/{work_item_id}/teststeps/{test_step_index}')
    
    def delete_test_steps(self,
                         project_id: str,
                         work_item_id: str,
                         test_steps_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Test Steps.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            test_steps_data: The Test Step(s) body
            
        Returns:
            Response object
        """
        return self._delete_with_body(
            f'projects/{project_id}/workitems/{work_item_id}/teststeps',
            json=test_steps_data
        )
    
    # ========== GET methods ==========
    
    def get_test_step(self,
                     project_id: str,
                     work_item_id: str,
                     test_step_index: str,
                     fields: Optional[Dict[str, str]] = None,
                     include: Optional[str] = None,
                     revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Test Step.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            test_step_index: The Test Step index
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
            Response object containing the test step data
        """
        params = self._apply_default_fields(fields)
        
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/teststeps/{test_step_index}',
            params=params if params else None
        )
    
    def get_test_steps(self,
                      project_id: str,
                      work_item_id: str,
                      page_size: Optional[int] = None,
                      page_number: Optional[int] = None,
                      fields: Optional[Dict[str, str]] = None,
                      include: Optional[str] = None,
                      revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Test Steps.
        
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
            Response object containing the list of test steps
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
            
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/teststeps',
            params=params if params else None
        )
    
    # ========== PATCH methods ==========
    
    def patch_test_step(self,
                       project_id: str,
                       work_item_id: str,
                       test_step_index: str,
                       test_step_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Test Step.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            test_step_index: The Test Step index
            test_step_data: The Test Step body
            
        Returns:
            Response object
        """
        return self._patch(
            f'projects/{project_id}/workitems/{work_item_id}/teststeps/{test_step_index}',
            json=test_step_data
        )
    
    def patch_test_steps(self,
                        project_id: str,
                        work_item_id: str,
                        test_steps_data: Dict[str, Any]) -> requests.Response:
        """
        Updates a list of Test Steps.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            test_steps_data: The Test Step(s) body
            
        Returns:
            Response object
        """
        return self._patch(
            f'projects/{project_id}/workitems/{work_item_id}/teststeps',
            json=test_steps_data
        )
    
    # ========== POST methods ==========
    
    def post_test_steps(self,
                       project_id: str,
                       work_item_id: str,
                       test_steps_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Test Steps.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            test_steps_data: The Test Step(s) body
            
        Returns:
            Response object containing the created test steps
        """
        return self._post(
            f'projects/{project_id}/workitems/{work_item_id}/teststeps',
            json=test_steps_data
        )
