"""
Test Runs module for Polarion REST API.
Handles all Test Runs related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class TestRuns(PolarionBase):
    """
    Class for handling Test Runs operations in Polarion REST API.
    Provides methods for creating, reading, updating, and deleting test runs,
    as well as managing test parameters, importing/exporting test results.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete test runs and test parameters
    - GET methods: Retrieve test runs, test parameters, and workflow actions
    - PATCH methods: Update test runs
    - POST methods: Create test runs, import/export results, manage test parameters
    """
    
    # ========== DELETE methods ==========
    
    def delete_test_runs(self, project_id: str, test_runs_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Test Runs.
        
        Args:
            project_id: The Project ID
            test_runs_data: The Test Run(s) body
            
        Returns:
            Response object (204 No Content on success)
        """
        endpoint = f"/projects/{project_id}/testruns"
        return self._delete_with_body(endpoint, json=test_runs_data)
    
    def delete_test_run(self, project_id: str, test_run_id: str) -> requests.Response:
        """
        Deletes the specified Test Run.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            
        Returns:
            Response object (204 No Content on success)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}"
        return self._delete(endpoint)
    
    def delete_test_run_test_parameter_definition(
        self, 
        project_id: str, 
        test_run_id: str, 
        test_param_id: str
    ) -> requests.Response:
        """
        Deletes the specified Test Parameter Definition for the specified Test Run.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_param_id: The Test Parameter
            
        Returns:
            Response object (204 No Content on success)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/testparameterdefinitions/{test_param_id}"
        return self._delete(endpoint)
    
    def delete_test_run_test_parameters(
        self, 
        project_id: str, 
        test_run_id: str, 
        test_parameters_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Deletes a list of Test Parameters for the specified Test Run.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_parameters_data: The Test Parameter(s) body
            
        Returns:
            Response object (204 No Content on success)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/testparameters"
        return self._delete_with_body(endpoint, json=test_parameters_data)
    
    def delete_test_run_test_parameter(
        self, 
        project_id: str, 
        test_run_id: str, 
        test_param_id: str
    ) -> requests.Response:
        """
        Deletes the specified Test Parameter for the specified Test Run.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_param_id: The Test Parameter
            
        Returns:
            Response object (204 No Content on success)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/testparameters/{test_param_id}"
        return self._delete(endpoint)
    
    # ========== GET methods ==========
    
    def get_test_runs(
        self, 
        project_id: str,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None,
        query: Optional[str] = None,
        sort: Optional[str] = None,
        revision: Optional[str] = None,
        templates: Optional[bool] = None
    ) -> requests.Response:
        """
        Returns a list of Test Runs.
        
        Args:
            project_id: The Project ID
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
            templates: If set to true, only templates will be returned, otherwise only actual instances
            
        Returns:
            Response object containing list of Test Runs
        """
        endpoint = f"/projects/{project_id}/testruns"
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
        if revision:
            params['revision'] = revision
        if templates is not None:
            params['templates'] = str(templates).lower()
            
        return self._get(endpoint, params=params)
    
    def get_test_run(
        self, 
        project_id: str,
        test_run_id: str,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None
    ) -> requests.Response:
        """
        Returns the specified Test Run.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
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
            Response object containing the Test Run
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}"
        params = self._apply_default_fields(fields)
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params)
    
    def get_export_excel_tests(
        self, 
        project_id: str,
        test_run_id: str,
        query: Optional[str] = None,
        sort_by: Optional[str] = None,
        template: Optional[str] = None
    ) -> requests.Response:
        """
        Exports tests to Excel.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            query: The query string
            sort_by: The property to sort the test results
            template: The export template string
            
        Returns:
            Response object (202 Accepted)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/actions/exportTestsToExcel"
        params = {}
        
        if query:
            params['query'] = query
        if sort_by:
            params['sortBy'] = sort_by
        if template:
            params['template'] = template
            
        return self._get(endpoint, params=params)
    
    def get_test_run_test_parameter_definitions(
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
        Returns a list of Test Parameter Definitions for the specified Test Run.
        
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
            Response object containing list of Test Parameter Definitions
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/testparameterdefinitions"
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
    
    def get_test_run_test_parameter_definition(
        self, 
        project_id: str,
        test_run_id: str,
        test_param_id: str,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None
    ) -> requests.Response:
        """
        Returns the specified Test Parameter Definition for the specified Test Run.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_param_id: The Test Parameter
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
            Response object containing the Test Parameter Definition
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/testparameterdefinitions/{test_param_id}"
        params = self._apply_default_fields(fields)
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params)
    
    def get_test_run_test_parameters(
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
        Returns a list of Test Parameters for the specified Test Run.
        
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
            Response object containing list of Test Parameters
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/testparameters"
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
    
    def get_test_run_test_parameter(
        self, 
        project_id: str,
        test_run_id: str,
        test_param_id: str,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None
    ) -> requests.Response:
        """
        Returns the specified Test Parameter for the specified Test Run.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_param_id: The Test Parameter
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
            Response object containing the Test Parameter
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/testparameters/{test_param_id}"
        params = self._apply_default_fields(fields)
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params)
    
    def get_workflow_actions_for_test_run(
        self, 
        project_id: str,
        test_run_id: str,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        revision: Optional[str] = None
    ) -> requests.Response:
        """
        Returns a list of Workflow Actions.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            page_size: Limit the number of entities returned in a single response
            page_number: Specify the page number to be returned (counting starts from 1)
            revision: The revision ID
            
        Returns:
            Response object containing list of Workflow Actions
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/actions/getWorkflowActions"
        params = {}
        
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params)
    
    # ========== PATCH methods ==========
    
    def patch_test_runs(self, project_id: str, test_runs_data: Dict[str, Any]) -> requests.Response:
        """
        Updates a list of Test Runs.
        
        Args:
            project_id: The Project ID
            test_runs_data: The Test Run(s) body
            
        Returns:
            Response object (204 No Content on success)
        """
        endpoint = f"/projects/{project_id}/testruns"
        return self._patch(endpoint, json=test_runs_data)
    
    def patch_test_run(
        self, 
        project_id: str, 
        test_run_id: str, 
        test_run_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Updates the specified Test Run.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_run_data: The Test Run(s) body
            
        Returns:
            Response object (204 No Content on success)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}"
        return self._patch(endpoint, json=test_run_data)
    
    # ========== POST methods ==========
    
    def post_test_runs(self, project_id: str, test_runs_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Test Runs.
        
        Args:
            project_id: The Project ID
            test_runs_data: The Test Run(s) body
            
        Returns:
            Response object (201 Created)
        """
        endpoint = f"/projects/{project_id}/testruns"
        return self._post(endpoint, json=test_runs_data)
    
    def import_x_unit_test_results(
        self, 
        project_id: str, 
        test_run_id: str, 
        xunit_file_data: bytes
    ) -> requests.Response:
        """
        Imports XUnit test results.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            xunit_file_data: XUnit File data (binary)
            
        Returns:
            Response object (202 Accepted)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/actions/importXUnitTestResults"
        headers = {'Content-Type': 'application/octet-stream'}
        return self._post(endpoint, data=xunit_file_data, headers=headers)
    
    def import_excel_test_results(
        self, 
        project_id: str, 
        test_run_id: str, 
        files: Dict[str, Any],
        data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        Imports Excel test results.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            files: Dictionary containing file(s) to upload (multipart/form-data)
            data: Optional metadata dictionary
            
        Returns:
            Response object (202 Accepted)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/actions/importExcelTestResults"
        return self._post(endpoint, files=files, data=data)
    
    def post_test_run_parameter_definitions(
        self, 
        project_id: str, 
        test_run_id: str, 
        parameter_definitions_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Creates a list of Test Parameter Definitions for the specified Test Run.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            parameter_definitions_data: The Test Parameter Definition(s) body
            
        Returns:
            Response object (201 Created)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/testparameterdefinitions"
        return self._post(endpoint, json=parameter_definitions_data)
    
    def post_test_run_test_parameters(
        self, 
        project_id: str, 
        test_run_id: str, 
        test_parameters_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Creates a list of Test Parameters for the specified Test Run.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_parameters_data: The Test Parameter(s) body
            
        Returns:
            Response object (201 Created)
        """
        endpoint = f"/projects/{project_id}/testruns/{test_run_id}/testparameters"
        return self._post(endpoint, json=test_parameters_data)
    
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
