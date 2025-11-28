"""
Test Records module for Polarion REST API.
Handles all Test Records related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class TestRecords(PolarionBase):
    """
    Class for handling Test Records operations in Polarion REST API.
    Provides methods for managing test records within test runs, including test execution results,
    test parameters, and test record status management.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete test records and test parameters
    - GET methods: Retrieve test records and test parameters
    - PATCH methods: Update test records
    - POST methods: Create test records and test parameters
    """
    
    # ========== DELETE methods ==========
    
    def delete_test_record(
        self,
        project_id: str,
        test_run_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: str
    ) -> requests.Response:
        """
        Deletes the specified Test Record.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            
        Returns:
            requests.Response: The response from the API (204 No Content on success)
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}"
        return self._delete(endpoint)
    
    def delete_test_record_test_parameter(
        self,
        project_id: str,
        test_run_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: str,
        test_param_id: str
    ) -> requests.Response:
        """
        Deletes the specified Test Parameter for the specified Test Record.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_param_id: The Test Parameter ID
            
        Returns:
            requests.Response: The response from the API (204 No Content on success)
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/testparameters/{test_param_id}"
        return self._delete(endpoint)
    
    # ========== GET methods ==========
    
    def get_test_record(
        self,
        project_id: str,
        test_run_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: str,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None
    ) -> requests.Response:
        """
        Returns the specified Test Record.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
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
            requests.Response: The response containing the test record
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}"
        params = {}
        
        if fields:
            params['fields'] = fields
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params if params else None)
    
    def get_test_records(
        self,
        project_id: str,
        test_run_id: str,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None,
        test_case_project_id: Optional[str] = None,
        test_case_id: Optional[str] = None,
        test_result_id: Optional[str] = None
    ) -> requests.Response:
        """
        Returns a list of Test Records.
        
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
            test_case_project_id: Filter by testcase project ID
            test_case_id: Filter by testcase ID
            test_result_id: Filter by test result ID
            
        Returns:
            requests.Response: The response containing the list of test records
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/testrecords"
        params = {}
        
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if fields:
            params['fields'] = fields
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
        if test_case_project_id:
            params['testCaseProjectId'] = test_case_project_id
        if test_case_id:
            params['testCaseId'] = test_case_id
        if test_result_id:
            params['testResultId'] = test_result_id
            
        return self._get(endpoint, params=params if params else None)
    
    def get_test_record_test_parameters(
        self,
        project_id: str,
        test_run_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: str,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None
    ) -> requests.Response:
        """
        Returns a list of Test Parameters for the specified Test Record.
        
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
            requests.Response: The response containing the list of test parameters
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/testparameters"
        params = {}
        
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if fields:
            params['fields'] = fields
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params if params else None)
    
    def get_test_record_test_parameter(
        self,
        project_id: str,
        test_run_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: str,
        test_param_id: str,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None
    ) -> requests.Response:
        """
        Returns the specified Test Parameter for the specified Test Record.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_param_id: The Test Parameter ID
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
            requests.Response: The response containing the test parameter
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/testparameters/{test_param_id}"
        params = {}
        
        if fields:
            params['fields'] = fields
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params if params else None)
    
    # ========== PATCH methods ==========
    
    def patch_test_record(
        self,
        project_id: str,
        test_run_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: str,
        test_record_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Updates the specified Test Record.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_record_data: The Test Record body
            
        Returns:
            requests.Response: The response from the API (204 No Content on success)
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}"
        return self._patch(endpoint, json=test_record_data)
    
    def patch_test_records(
        self,
        project_id: str,
        test_run_id: str,
        test_records_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Updates a list of Test Records.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_records_data: The Test Records body
            
        Returns:
            requests.Response: The response from the API (204 No Content on success)
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/testrecords"
        return self._patch(endpoint, json=test_records_data)
    
    # ========== POST methods ==========
    
    def post_test_records(
        self,
        project_id: str,
        test_run_id: str,
        test_records_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Creates a list of Test Records.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_records_data: The Test Records body
            
        Returns:
            requests.Response: The response containing the created test records
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/testrecords"
        return self._post(endpoint, json=test_records_data)
    
    def post_test_record_test_parameters(
        self,
        project_id: str,
        test_run_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: str,
        test_parameters_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Creates a list of Test Parameters for the specified Test Record.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_parameters_data: The Test Parameters body
            
        Returns:
            requests.Response: The response containing the created test parameters
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/testparameters"
        return self._post(endpoint, json=test_parameters_data)
