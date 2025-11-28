"""
Test Step Results module for Polarion REST API.
Handles all Test Step Results related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class TestStepResults(PolarionBase):
    """
    Class for handling Test Step Results operations in Polarion REST API.
    Provides methods for creating, reading, and updating test step results.
    
    Test Step Results represent the execution results of individual test steps
    within test records during test runs.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve test step results
    - PATCH methods: Update test step results
    - POST methods: Create test step results
    """
    
    # ========== GET methods ==========
    
    def get_test_step_result(self,
                            project_id: str,
                            test_run_id: str,
                            test_case_project_id: str,
                            test_case_id: str,
                            iteration: str,
                            test_step_index: str,
                            fields: Optional[Dict[str, str]] = None,
                            include: Optional[str] = None,
                            revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Test Step Result.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
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
            Response object containing the test step result data
        """
        params = self._apply_default_fields(fields)
        
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}',
            params=params if params else None
        )
    
    def get_test_step_results(self,
                             project_id: str,
                             test_run_id: str,
                             test_case_project_id: str,
                             test_case_id: str,
                             iteration: str,
                             page_size: Optional[int] = None,
                             page_number: Optional[int] = None,
                             fields: Optional[Dict[str, str]] = None,
                             include: Optional[str] = None,
                             revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Test Step Results.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
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
            Response object containing the list of test step results
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
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults',
            params=params if params else None
        )
    
    # ========== PATCH methods ==========
    
    def patch_test_step_result(self,
                              project_id: str,
                              test_run_id: str,
                              test_case_project_id: str,
                              test_case_id: str,
                              iteration: str,
                              test_step_index: str,
                              test_step_result_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Test Step Result.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_step_index: The Test Step index
            test_step_result_data: The Test Step Result body
            
        Returns:
            Response object
        """
        return self._patch(
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}',
            json=test_step_result_data
        )
    
    def patch_test_step_results(self,
                               project_id: str,
                               test_run_id: str,
                               test_case_project_id: str,
                               test_case_id: str,
                               iteration: str,
                               test_step_results_data: Dict[str, Any]) -> requests.Response:
        """
        Updates a list of Test Step Results.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_step_results_data: The Test Step Result(s) body
            
        Returns:
            Response object
        """
        return self._patch(
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults',
            json=test_step_results_data
        )
    
    # ========== POST methods ==========
    
    def post_test_step_results(self,
                              project_id: str,
                              test_run_id: str,
                              test_case_project_id: str,
                              test_case_id: str,
                              iteration: str,
                              test_step_results_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Test Step Results.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_step_results_data: The Test Step Result(s) body
            
        Returns:
            Response object containing the created test step results
        """
        return self._post(
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults',
            json=test_step_results_data
        )
