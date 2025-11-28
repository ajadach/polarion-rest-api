"""
User Groups module for Polarion REST API.
Handles all User Groups related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class UserGroups(PolarionBase):
    """
    Class for handling User Groups operations in Polarion REST API.
    Provides methods for retrieving user group information.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve user group data
    """
    
    # ========== GET methods ==========
    
    def get_user_group(self,
                       group_id: str,
                       fields: Optional[Dict[str, str]] = None,
                       include: Optional[str] = None,
                       revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified User Group.
        
        Args:
            group_id: The Group ID
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
            Response object containing the user group data
        """
        params = self._apply_default_fields(fields)
        
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
            
        return self._get(f'usergroups/{group_id}', params=params if params else None)
