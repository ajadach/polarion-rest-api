"""
Test Run Attachments module for Polarion REST API.
Handles all Test Run Attachments related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class TestRunAttachments(PolarionBase):
    """
    Class for handling Test Run Attachments operations in Polarion REST API.
    Provides methods for managing attachments on test runs, including uploading,
    downloading, updating, and deleting attachment files.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete test run attachments
    - GET methods: Retrieve test run attachments and their content
    - PATCH methods: Update test run attachments
    - POST methods: Create test run attachments
    
    Note: POST and PATCH methods use multipart/form-data for file uploads.
    """
    
    # ========== DELETE methods ==========
    
    def delete_test_run_attachment(
        self,
        project_id: str,
        test_run_id: str,
        attachment_id: str
    ) -> requests.Response:
        """
        Deletes the specified Test Run Attachment.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            attachment_id: The Attachment ID
            
        Returns:
            requests.Response: The response from the API (204 No Content on success)
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/attachments/{attachment_id}"
        return self._delete(endpoint)
    
    def delete_test_run_attachments(
        self,
        project_id: str,
        test_run_id: str,
        test_run_attachments_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Deletes a list of Test Run Attachments.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            test_run_attachments_data: The Test Run Attachment(s) body with list of IDs to delete
            
        Returns:
            requests.Response: The response from the API (204 No Content on success)
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/attachments"
        return self._delete_with_body(endpoint, json=test_run_attachments_data)
    
    # ========== GET methods ==========
    
    def get_test_run_attachment(
        self,
        project_id: str,
        test_run_id: str,
        attachment_id: str,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None
    ) -> requests.Response:
        """
        Returns the specified Test Run Attachment.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
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
            requests.Response: The response containing the attachment metadata
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/attachments/{attachment_id}"
        params = self._apply_default_fields(fields)
        
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params if params else None)
    
    def get_test_run_attachment_content(
        self,
        project_id: str,
        test_run_id: str,
        attachment_id: str,
        revision: Optional[str] = None
    ) -> requests.Response:
        """
        Downloads the file content for a specified Test Run Attachment.
        Returns binary file content (application/octet-stream).
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            attachment_id: The Attachment ID
            revision: The revision ID
            
        Returns:
            requests.Response: The response containing the binary file content
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/attachments/{attachment_id}/content"
        params = {}
        
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params if params else None)
    
    def get_test_run_attachments(
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
        Returns a list of Test Run Attachments.
        
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
            requests.Response: The response containing the list of attachments
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/attachments"
        params = self._apply_default_fields(fields)
        
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(endpoint, params=params if params else None)
    
    # ========== PATCH methods ==========
    
    def patch_test_run_attachment(
        self,
        project_id: str,
        test_run_id: str,
        attachment_id: str,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        Updates the specified Test Run Attachment.
        Uses multipart/form-data for file upload.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            attachment_id: The Attachment ID
            files: Dictionary with file data (e.g., {'file': open('path.pdf', 'rb')})
            data: Dictionary with attachment metadata (e.g., {'resource': json.dumps(metadata)})
            
        Returns:
            requests.Response: The response from the API (204 No Content on success)
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/attachments/{attachment_id}"
        return self._patch(endpoint, files=files, data=data)
    
    # ========== POST methods ==========
    
    def post_test_run_attachments(
        self,
        project_id: str,
        test_run_id: str,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        Creates a list of Test Run Attachments.
        Files are identified by order or optionally by the 'lid' attribute.
        Uses multipart/form-data for file upload.
        
        Args:
            project_id: The Project ID
            test_run_id: The Test Run ID
            files: Dictionary with file data (e.g., {'file': open('path.pdf', 'rb')})
            data: Dictionary with attachment metadata (e.g., {'resource': json.dumps(metadata)})
            
        Returns:
            requests.Response: The response containing the created attachments
        """
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/attachments"
        return self._post(endpoint, files=files, data=data)
