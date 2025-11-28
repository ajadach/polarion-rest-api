"""
Icons module for Polarion REST API.
Handles all Icons related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class Icons(PolarionBase):
    """
    Class for handling Icons operations in Polarion REST API.
    Provides methods for retrieving and creating icons in different contexts (default, global, project).
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve icons from different contexts
    - POST methods: Create icons in global and project contexts
    """
    
    # ========== GET methods ==========
    
    def get_default_icons(self,
                         page_size: Optional[int] = None,
                         page_number: Optional[int] = None,
                         fields: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Returns a list of Icons from the default context.
        
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
            
        Returns:
            Response object containing list of default icons
        """
        params = {}
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        
        # Apply default fields and merge with existing params
        default_fields = self._apply_default_fields(fields)
        params.update(default_fields)
            
        return self._get('enumerations/defaulticons', params=params if params else None)
    
    def get_default_icon(self,
                        icon_id: str,
                        fields: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Returns the specified Icon from the default context.
        
        Args:
            icon_id: The Icon ID
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
            
        Returns:
            Response object containing the default icon
        """
        params = self._apply_default_fields(fields)
                    
        return self._get(f'enumerations/defaulticons/{icon_id}', 
                        params=params if params else None)
    
    def get_global_icon(self,
                       icon_id: str,
                       fields: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Returns the specified Icon from the Global context.
        
        Args:
            icon_id: The Icon ID
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
            
        Returns:
            Response object containing the global icon
        """
        params = self._apply_default_fields(fields)       
            
        return self._get(f'enumerations/icons/{icon_id}', 
                        params=params if params else None)
    
    def get_global_icons(self,
                        page_size: Optional[int] = None,
                        page_number: Optional[int] = None,
                        fields: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Returns a list of Icons from the Global context.
        
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
            
        Returns:
            Response object containing list of global icons
        """
        params = {}
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        
        # Apply default fields and merge with existing params
        default_fields = self._apply_default_fields(fields)
        params.update(default_fields)
            
        return self._get('enumerations/icons', params=params if params else None)
    
    def get_project_icon(self,
                        project_id: str,
                        icon_id: str,
                        fields: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Returns the specified Icon from the Project context.
        
        Args:
            project_id: The Project ID
            icon_id: The Icon ID
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
            
        Returns:
            Response object containing the project icon
        """
        params = self._apply_default_fields(fields)
            
        return self._get(f'projects/{project_id}/enumerations/icons/{icon_id}',
                        params=params if params else None)
    
    def get_project_icons(self,
                         project_id: str,
                         page_size: Optional[int] = None,
                         page_number: Optional[int] = None,
                         fields: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Returns a list of Icons from the Project context.
        
        Args:
            project_id: The Project ID
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
            
        Returns:
            Response object containing list of project icons
        """
        params = {}
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        
        # Apply default fields and merge with existing params
        default_fields = self._apply_default_fields(fields)
        params.update(default_fields)
            
        return self._get(f'projects/{project_id}/enumerations/icons',
                        params=params if params else None)
    
    # ========== POST methods ==========
    
    def post_global_icons(self,
                         data: Optional[Dict[str, Any]] = None,
                         files: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Creates a list of Icons in the Global context.
        Icons are identified by order.
        
        Args:
            data: Icon meta data (form data)
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
            
        Returns:
            Response object
        """
        return self._post('enumerations/icons', data=data, files=files)
    
    def post_project_icons(self,
                          project_id: str,
                          data: Optional[Dict[str, Any]] = None,
                          files: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Creates a list of Icons in the Project context.
        Icons are identified by order.
        
        Request Body (multipart/form-data):
            - resource: Icon metadata as JSON string containing:
                {
                    "data": [
                        {
                            "type": "icons"
                        }
                    ]
                }
            - files: Binary icon file(s) to upload (format: binary)
        
        Args:
            project_id: The Project ID
            data: Icon meta data (form data) - should contain 'resource' key with JSON string
            files: Binary file(s) to upload as icons
            
        Returns:
            Response object
        """
        return self._post(f'projects/{project_id}/enumerations/icons',
                         data=data, files=files)
