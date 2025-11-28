"""
Work Item Work Records module for Polarion REST API.
Handles all Work Item Work Records related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class WorkItemWorkRecords(PolarionBase):
    """
    Class for handling Work Item Work Records operations in Polarion REST API.
    Provides methods for creating, reading, and deleting work records associated with work items.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete work records
    - GET methods: Retrieve work records
    - POST methods: Create work records
    """
    
    # ========== DELETE methods ==========
    
    def delete_work_record(self,
                          project_id: str,
                          work_item_id: str,
                          work_record_id: str) -> requests.Response:
        """
        Deletes the specified Work Record.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            work_record_id: The Work Record ID
            
        Returns:
            Response object
        """
        return self._delete(
            f'projects/{project_id}/workitems/{work_item_id}/workrecords/{work_record_id}'
        )
    
    def delete_work_records(self,
                           project_id: str,
                           work_item_id: str,
                           work_records_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Work Records.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            work_records_data: The Work Record(s) body
            
        Returns:
            Response object
        """
        return self._delete_with_body(
            f'projects/{project_id}/workitems/{work_item_id}/workrecords',
            json=work_records_data
        )
    
    # ========== GET methods ==========
    
    def get_work_record(self,
                       project_id: str,
                       work_item_id: str,
                       work_record_id: str,
                       fields: Optional[Dict[str, str]] = None,
                       include: Optional[str] = None,
                       revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified instance.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            work_record_id: The Work Record ID
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
            Response object with work record data
        """
        params = self._apply_default_fields(fields)
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
        
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/workrecords/{work_record_id}',
            params=params
        )
    
    def get_work_records(self,
                        project_id: str,
                        work_item_id: str,
                        page_size: Optional[int] = None,
                        page_number: Optional[int] = None,
                        fields: Optional[Dict[str, str]] = None,
                        include: Optional[str] = None,
                        revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of instances.
        
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
            Response object with work records data
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
        
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/workrecords',
            params=params
        )
    
    # ========== POST methods ==========
    
    def post_work_records(self,
                         project_id: str,
                         work_item_id: str,
                         work_records_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Work Records.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            work_records_data: The Work Record(s) body
            
        Returns:
            Response object with created work records
        """
        return self._post(
            f'projects/{project_id}/workitems/{work_item_id}/workrecords',
            json=work_records_data
        )
    
    # ========== Helper methods ==========
    
    def _delete_with_body(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Helper method for DELETE requests with body (not standard in requests library).
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments for the request
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._session.request('DELETE', url, **kwargs)
