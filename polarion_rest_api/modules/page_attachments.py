"""
Page Attachments module for Polarion REST API.
Handles all Page Attachments related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class PageAttachments(PolarionBase):
    """
    Class for handling Page Attachments operations in Polarion REST API.
    Provides methods for creating, retrieving, and downloading page attachments.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve page attachments and download content
    - POST methods: Create page attachments
    """
    
    # ========== GET methods ==========
    
    def get_page_attachment(self,
                           project_id: str,
                           space_id: str,
                           page_name: str,
                           attachment_id: str,
                           fields: Optional[Dict[str, str]] = None,
                           include: Optional[str] = None,
                           revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Page Attachment.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' without quotes to address the default Space)
            page_name: The Page name
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
            Response object containing the page attachment
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/spaces/{space_id}/pages/{page_name}/attachments/{attachment_id}',
            params=params if params else None
        )
    
    def get_page_attachment_content(self,
                                   project_id: str,
                                   space_id: str,
                                   page_name: str,
                                   attachment_id: str,
                                   revision: Optional[str] = None) -> requests.Response:
        """
        Downloads the file content for a specified Page Attachment.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' without quotes to address the default Space)
            page_name: The Page name
            attachment_id: The Attachment ID
            revision: The revision ID
            
        Returns:
            Response object containing the file content (application/octet-stream)
        """
        params = {}
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/spaces/{space_id}/pages/{page_name}/attachments/{attachment_id}/content',
            params=params if params else None
        )
    
    # ========== POST methods ==========
    
    def post_page_attachments(self,
                             project_id: str,
                             space_id: str,
                             page_name: str,
                             data: Optional[Dict[str, Any]] = None,
                             files: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Creates a list of Page Attachments.
        Files are identified by order or optionally by the 'lid' attribute.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID
            page_name: The Page name
            data: Attachment meta data (form data)
            files: File data for multipart/form-data upload
            
        Returns:
            Response object
        """
        return self._post(
            f'projects/{project_id}/spaces/{space_id}/pages/{page_name}/attachments',
            data=data,
            files=files
        )
