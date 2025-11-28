"""
Project Templates module for Polarion REST API.
Handles all Project Templates related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class ProjectTemplates(PolarionBase):
    """
    Class for handling Project Templates operations in Polarion REST API.
    Provides methods for retrieving project templates.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve project templates
    """
    
    # ========== GET methods ==========
    
    def get_project_templates(self,
                             page_size: Optional[int] = None,
                             page_number: Optional[int] = None,
                             fields: Optional[Dict[str, str]] = None,
                             include: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Project Templates.
        
        Args:
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
            
        Returns:
            Response object containing list of project templates
        """
        params = self._apply_default_fields(fields)
        
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if include is not None:
            params['include'] = include
            
        return self._get('projecttemplates', params=params if params else None)
