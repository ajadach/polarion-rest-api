"""
Document Parts module for Polarion REST API.
Handles all Document Parts related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class DocumentParts(PolarionBase):
    """
    Class for handling Document Parts operations in Polarion REST API.
    Provides methods for creating and reading document parts.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve document parts
    - POST methods: Create document parts
    """
    
    # ========== GET methods ==========
    
    def get_document_part(self,
                         project_id: str,
                         space_id: str,
                         document_name: str,
                         part_id: str,
                         fields: Optional[Dict[str, str]] = None,
                         include: Optional[str] = None,
                         revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Document Part.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            part_id: The Document Part ID
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
            Response object containing the document part
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/parts/{part_id}',
            params=params if params else None
        )
    
    def get_document_parts(self,
                          project_id: str,
                          space_id: str,
                          document_name: str,
                          page_size: Optional[int] = None,
                          page_number: Optional[int] = None,
                          fields: Optional[Dict[str, str]] = None,
                          include: Optional[str] = None,
                          revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Document Parts.
        
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
            Response object containing list of document parts
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
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/parts',
            params=params if params else None
        )
    
    # ========== POST methods ==========
    
    def post_document_parts(self,
                           project_id: str,
                           space_id: str,
                           document_name: str,
                           parts_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Document Parts.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            parts_data: The Document Part(s) body
            
        Returns:
            Response object (201 Created)
        """
        return self._post(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/parts',
            json=parts_data
        )
