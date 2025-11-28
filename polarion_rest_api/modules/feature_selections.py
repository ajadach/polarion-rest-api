"""
Feature Selections module for Polarion REST API.
Handles all Feature Selections related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class FeatureSelections(PolarionBase):
    """
    Class for handling Feature Selections operations in Polarion REST API.
    Provides methods for retrieving feature selections.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve feature selections
    """
    
    # ========== GET methods ==========
    
    def get_feature_selection(self,
                             project_id: str,
                             work_item_id: str,
                             selection_type_id: str,
                             target_project_id: str,
                             target_work_item_id: str,
                             fields: Optional[Dict[str, str]] = None,
                             include: Optional[str] = None,
                             revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Feature Selection.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            selection_type_id: The Selection Type ID
            target_project_id: The Target Project ID
            target_work_item_id: The Target Work Item ID
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
            Response object containing the feature selection
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/featureselections/'
            f'{selection_type_id}/{target_project_id}/{target_work_item_id}',
            params=params if params else None
        )
    
    def get_feature_selections(self,
                              project_id: str,
                              work_item_id: str,
                              page_size: Optional[int] = None,
                              page_number: Optional[int] = None,
                              fields: Optional[Dict[str, str]] = None,
                              include: Optional[str] = None,
                              revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Feature Selections.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
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
            Response object containing list of feature selections
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
            f'projects/{project_id}/workitems/{work_item_id}/featureselections',
            params=params if params else None
        )
