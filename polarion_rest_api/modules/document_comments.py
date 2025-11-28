"""
Document Comments module for Polarion REST API.
Handles all Document Comments related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class DocumentComments(PolarionBase):
    """
    Class for handling Document Comments operations in Polarion REST API.
    Provides methods for creating, reading, and updating document comments.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve document comments
    - PATCH methods: Update document comments
    - POST methods: Create document comments
    """
    
    # ========== GET methods ==========
    
    def get_document_comment(self,
                            project_id: str,
                            space_id: str,
                            document_name: str,
                            comment_id: str,
                            fields: Optional[Dict[str, str]] = None,
                            include: Optional[str] = None,
                            revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Document Comment.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
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
            Response object containing the document comment
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/comments/{comment_id}',
            params=params if params else None
        )
    
    def get_document_comments(self,
                             project_id: str,
                             space_id: str,
                             document_name: str,
                             page_size: Optional[int] = None,
                             page_number: Optional[int] = None,
                             fields: Optional[Dict[str, str]] = None,
                             include: Optional[str] = None,
                             revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Document Comments.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
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
            Response object containing list of document comments
        """
        params = self._apply_default_fields(fields)
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/comments',
            params=params if params else None
        )
    
    # ========== PATCH methods ==========
    
    def patch_document_comment(self,
                              project_id: str,
                              space_id: str,
                              document_name: str,
                              comment_id: str,
                              comment_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Document Comment.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            comment_id: The Comment ID
            comment_data: The Comment body
            
        Returns:
            Response object (204 No Content on success)
        """
        return self._patch(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/comments/{comment_id}',
            json=comment_data
        )
    
    # ========== POST methods ==========
    
    def post_document_comments(self,
                              project_id: str,
                              space_id: str,
                              document_name: str,
                              comments_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Document Comments.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            comments_data: The Comment(s) body
            
        Returns:
            Response object (201 Created)
        """
        return self._post(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/comments',
            json=comments_data
        )
