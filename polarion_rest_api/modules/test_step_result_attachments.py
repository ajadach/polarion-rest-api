"""
Test Step Result Attachments module for Polarion REST API.
Handles all Test Step Result Attachments related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class TestStepResultAttachments(PolarionBase):
    """
    Class for handling Test Step Result Attachments operations in Polarion REST API.
    Provides methods for creating, reading, updating, and deleting test step result attachments.
    
    Test Step Result Attachments are files attached to individual test step results
    within test records during test runs.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete test step result attachments
    - GET methods: Retrieve test step result attachments and content
    - PATCH methods: Update test step result attachments
    - POST methods: Create test step result attachments
    """
    
    # ========== DELETE methods ==========
    
    def delete_test_step_result_attachment(self,
                                          project_id: str,
                                          test_run_id: str,
                                          test_case_project_id: str,
                                          test_case_id: str,
                                          iteration: str,
                                          test_step_index: str,
                                          attachment_id: str) -> requests.Response:
        """
        Deletes the specified Test Step Result Attachment.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_step_index: The Test Step index
            attachment_id: The Attachment ID
            
        Returns:
            Response object
        """
        return self._delete(
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments/{attachment_id}'
        )
    
    def delete_test_step_result_attachments(self,
                                           project_id: str,
                                           test_run_id: str,
                                           test_case_project_id: str,
                                           test_case_id: str,
                                           iteration: str,
                                           test_step_index: str,
                                           attachments_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Test Step Result Attachments.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_step_index: The Test Step index
            attachments_data: The Test Step Result Attachment(s) body
            
        Returns:
            Response object
        """
        return self._delete_with_body(
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments',
            json=attachments_data
        )
    
    # ========== GET methods ==========
    
    def get_test_step_result_attachment(self,
                                       project_id: str,
                                       test_run_id: str,
                                       test_case_project_id: str,
                                       test_case_id: str,
                                       iteration: str,
                                       test_step_index: str,
                                       attachment_id: str,
                                       fields: Optional[Dict[str, str]] = None,
                                       include: Optional[str] = None,
                                       revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Test Step Result Attachment for the specified Test Record.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_step_index: The Test Step index
            attachment_id: The Attachment ID
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
            Response object containing the test step result attachment data
        """
        params = self._apply_default_fields(fields)
        
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments/{attachment_id}',
            params=params if params else None
        )
    
    def get_test_step_result_attachment_content(self,
                                               project_id: str,
                                               test_run_id: str,
                                               test_case_project_id: str,
                                               test_case_id: str,
                                               iteration: str,
                                               test_step_index: str,
                                               attachment_id: str,
                                               revision: Optional[str] = None) -> requests.Response:
        """
        Downloads the file content for a specified Test Step Result Attachment for the specified Test Record.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_step_index: The Test Step index
            attachment_id: The Attachment ID
            revision: The revision ID
            
        Returns:
            Response object containing the attachment file content (application/octet-stream)
        """
        params = {}
        
        if revision:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments/{attachment_id}/content',
            params=params if params else None
        )
    
    def get_test_step_result_attachments(self,
                                        project_id: str,
                                        test_run_id: str,
                                        test_case_project_id: str,
                                        test_case_id: str,
                                        iteration: str,
                                        test_step_index: str,
                                        page_size: Optional[int] = None,
                                        page_number: Optional[int] = None,
                                        fields: Optional[Dict[str, str]] = None,
                                        include: Optional[str] = None,
                                        revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Attachments for the specified Test Step Result.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_step_index: The Test Step index
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
            Response object containing the list of test step result attachments
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
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments',
            params=params if params else None
        )
    
    # ========== PATCH methods ==========
    
    def patch_test_step_result_attachment(self,
                                         project_id: str,
                                         test_run_id: str,
                                         test_case_project_id: str,
                                         test_case_id: str,
                                         iteration: str,
                                         test_step_index: str,
                                         attachment_id: str,
                                         files: Optional[Dict[str, Any]] = None,
                                         data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Updates the specified Test Step Result Attachment.
        
        Uses multipart/form-data for attachment meta data and file data.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_step_index: The Test Step index
            attachment_id: The Attachment ID
            files: Multipart files dictionary (e.g., {'file': open('file.txt', 'rb')})
            data: Multipart form data dictionary (attachment metadata as JSON string)
            
        Returns:
            Response object
        """
        return self._patch(
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments/{attachment_id}',
            files=files,
            data=data
        )
    
    # ========== POST methods ==========
    
    def post_test_step_result_attachments(self,
                                         project_id: str,
                                         test_run_id: str,
                                         test_case_project_id: str,
                                         test_case_id: str,
                                         iteration: str,
                                         test_step_index: str,
                                         files: Optional[Dict[str, Any]] = None,
                                         data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Creates a list of Test Step Result Attachments.
        
        Files are identified by order or optionally by the 'lid' attribute.
        Uses multipart/form-data for attachment meta data and file data.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_case_project_id: The Testcase Project ID
            test_case_id: The Testcase ID
            iteration: The Iteration Number
            test_step_index: The Test Step index
            files: Multipart files dictionary (e.g., {'file': open('file.txt', 'rb')})
            data: Multipart form data dictionary (attachment metadata as JSON string)
            
        Returns:
            Response object containing the created test step result attachments
        """
        return self._post(
            f'projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments',
            files=files,
            data=data
        )
