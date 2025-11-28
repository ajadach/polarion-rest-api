"""
Polarion REST API - Roles Module

This module provides access to Polarion Roles endpoints.
It handles operations related to Global Roles in Polarion.

API Documentation:
- Get Role: GET /roles/{roleId}

Author: Auto-generated
Date: 2025
"""

from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class Roles(PolarionBase):
    """
    Handles Polarion Roles operations.
    
    This class provides methods to interact with Global Roles in Polarion,
    including retrieving role information.
    
    Methods are organized by HTTP method type:
    - GET methods: Retrieve roles
    """
    
    # ========== GET methods ==========
    
    def get_role(
        self,
        role_id: str,
        fields: Optional[Dict[str, str]] = None,
        include: Optional[str] = None
    ) -> requests.Response:
        """
        Get a specific Global Role by its ID.
        
        Retrieves detailed information about a Global Role identified by role_id.
        
        Args:
            role_id: The Role ID (required).
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
            include: Comma-separated list of related resources to include (optional).
                Example: 'permissions,users'
                
        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = f"/roles/{role_id}"
        params = self._apply_default_fields(fields)
        
        if include:
            params['include'] = include
        
        return self._get(endpoint, params=params if params else None)
