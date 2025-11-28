"""
Work Item Attachments module for Polarion REST API.
Handles all Work Item Attachments related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class WorkItemAttachments(PolarionBase):
    """
    Class for handling Work Item Attachments operations in Polarion REST API.
    Provides methods for creating, reading, updating, and deleting work item attachments.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete attachments
    - GET methods: Retrieve attachments and related data
    - PATCH methods: Update attachments
    - POST methods: Create attachments
    """
    
    # ========== DELETE methods ==========
    
    def delete_work_item_attachment(self,
                                   project_id: str,
                                   work_item_id: str,
                                   attachment_id: str) -> requests.Response:
        """
        Deletes the specified Work Item Attachment.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            attachment_id: The Attachment ID
            
        Returns:
            Response object
        """
        return self._delete(f'projects/{project_id}/workitems/{work_item_id}/attachments/{attachment_id}')
    
    # ========== GET methods ==========
    
    def get_work_item_attachments(self,
                       project_id: str,
                       work_item_id: str,
                       page_size: Optional[int] = None,
                       page_number: Optional[int] = None,
                       fields: Optional[Dict[str, str]] = None,
                       include: Optional[str] = None,
                       revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Work Item Attachments.
        
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
            Response object with attachments data
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
        
        return self._get(f'projects/{project_id}/workitems/{work_item_id}/attachments', params=params)    
    
    def get_work_item_attachment(self,
                                project_id: str,
                                work_item_id: str,
                                attachment_id: str,
                                fields: Optional[Dict[str, str]] = None,
                                include: Optional[str] = None,
                                revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Work Item Attachment.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
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
            Response object with attachment data
        """
        params = self._apply_default_fields(fields)
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
        
        return self._get(f'projects/{project_id}/workitems/{work_item_id}/attachments/{attachment_id}', 
                        params=params)
    
    def get_work_item_attachment_content(self,
                                        project_id: str,
                                        work_item_id: str,
                                        attachment_id: str,
                                        revision: Optional[str] = None) -> requests.Response:
        """
        Downloads the file content for a specified Work Item Attachment.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            attachment_id: The Attachment ID
            revision: The revision ID
            
        Returns:
            Response object with file content (application/octet-stream)
        """
        params = {}
        if revision:
            params['revision'] = revision
        
        return self._get(f'projects/{project_id}/workitems/{work_item_id}/attachments/{attachment_id}/content', 
                        params=params)
    
    # ========== PATCH methods ==========
    
    def patch_work_item_attachment(self,
                         project_id: str,
                         work_item_id: str,
                         attachment_id: str,
                         attachment_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Work Item Attachment.
        Note: This endpoint uses multipart/form-data content type.
        See REST API User Guide for details.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            attachment_id: The Attachment ID
            attachment_data: The Attachment meta data and file data (multipart/form-data)
            
        Returns:
            Response object
        """
        return self._patch(f'projects/{project_id}/workitems/{work_item_id}/attachments/{attachment_id}', 
                          json=attachment_data)
    
    # ========== POST methods ==========
    
    def post_work_item_attachments(self,
                                  project_id: str,
                                  work_item_id: str,
                                  attachments_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Work Item Attachments.
        Files are identified by order or optionally by the 'lid' attribute.
        Note: This endpoint uses multipart/form-data content type.
        See REST API User Guide for details.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            attachments_data: The Attachment meta data and file data (multipart/form-data)
            
        Returns:
            Response object with created attachments
        """
        return self._post(f'projects/{project_id}/workitems/{work_item_id}/attachments', 
                         json=attachments_data)
