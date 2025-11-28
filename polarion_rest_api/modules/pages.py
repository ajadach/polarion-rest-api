"""
Pages module for Polarion REST API.
Handles all Pages related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class Pages(PolarionBase):
    """
    Class for handling Pages operations in Polarion REST API.
    Provides methods for retrieving and updating pages.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve pages
    - PATCH methods: Update pages
    """
    
    # ========== GET methods ==========
    
    def get_page(self,
                project_id: str,
                space_id: str,
                page_name: str,
                fields: Optional[Dict[str, str]] = None,
                include: Optional[str] = None,
                revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Page.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' without quotes to address the default Space)
            page_name: The Page name
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
            Response object containing the page
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(f'projects/{project_id}/spaces/{space_id}/pages/{page_name}',
                        params=params if params else None)
    
    # ========== PATCH methods ==========
    
    def patch_rich_page(self,
                       project_id: str,
                       space_id: str,
                       page_name: str,
                       page_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Page.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' without quotes to address the default Space)
            page_name: The Page name
            page_data: The Page body
            
        Returns:
            Response object
        """
        return self._patch(f'projects/{project_id}/spaces/{space_id}/pages/{page_name}',
                          json=page_data)
