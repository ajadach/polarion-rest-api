"""
Jobs module for Polarion REST API.
Handles all Jobs related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class Jobs(PolarionBase):
    """
    Class for handling Jobs operations in Polarion REST API.
    Provides methods for retrieving jobs and downloading job results.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve jobs and download job result files
    """
    
    # ========== GET methods ==========
    
    def get_job_result_file_content(self,
                                    job_id: str,
                                    filename: str) -> requests.Response:
        """
        Downloads the file content for a specified job.
        
        Args:
            job_id: The Job ID
            filename: The Download File Name
            
        Returns:
            Response object containing the file content
        """
        return self._get(f'jobs/{job_id}/actions/download/{filename}')
    
    def get_job(self,
               job_id: str,
               fields: Optional[Dict[str, str]] = None,
               include: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Job.
        
        Args:
            job_id: The Job ID
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
            Response object containing the job
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
            
        return self._get(f'jobs/{job_id}', params=params if params else None)
