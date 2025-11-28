"""
Revisions module for Polarion REST API.
Handles all Revisions related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class Revisions(PolarionBase):
    """
    Class for handling Revisions operations in Polarion REST API.
    Provides methods for retrieving revision information.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve revisions and related data
    """
    
    # ========== GET methods ==========
    
    def get_revisions(self,
                     page_size: Optional[int] = None,
                     page_number: Optional[int] = None,
                     fields: Optional[Dict[str, str]] = None,
                     include: Optional[str] = None,
                     query: Optional[str] = None,
                     sort: Optional[str] = None) -> requests.Response:
        """
        Returns a list of revision instances.
        
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
            query: The query string
            sort: The sort string
            
        Returns:
            Response object containing list of revisions
        """
        params = self._apply_default_fields(fields)
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        
        if include is not None:
            params['include'] = include
        if query is not None:
            params['query'] = query
        if sort is not None:
            params['sort'] = sort
            
        return self._get('revisions', params=params if params else None)
    
    def get_revision(self,
                    repository_name: str,
                    revision: str,
                    fields: Optional[Dict[str, str]] = None,
                    include: Optional[str] = None) -> requests.Response:
        """
        Returns the specified revision instance.
        
        Args:
            repository_name: The Repository Name
            revision: The revision ID
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
            Response object containing the specified revision
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
            
        return self._get(f'revisions/{repository_name}/{revision}', 
                        params=params if params else None)
