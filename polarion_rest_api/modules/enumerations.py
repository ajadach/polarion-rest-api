"""
Enumerations module for Polarion REST API.
Handles all Enumerations related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class Enumerations(PolarionBase):
    """
    Class for handling Enumerations operations in Polarion REST API.
    Provides methods for creating, reading, updating, and deleting enumerations in both Global and Project contexts.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete enumerations
    - GET methods: Retrieve enumerations
    - PATCH methods: Update enumerations
    - POST methods: Create enumerations
    """
    
    # ========== DELETE methods ==========
    
    def delete_global_enumeration(self,
                                  enum_context: str,
                                  enum_name: str,
                                  target_type: str) -> requests.Response:
        """
        Deletes the specified Enumeration from the Global context.
        
        Args:
            enum_context: The Enumeration context (Allowed values: '~', 'plans', 'testing', 'documents'. Use '~' for Work Item or general enumerations)
            enum_name: The Enumeration Name
            target_type: The Enumeration target type (Use '~' when there is no specific type)
            
        Returns:
            Response object (204 No Content on success)
        """
        return self._delete(f'enumerations/{enum_context}/{enum_name}/{target_type}')
    
    def delete_project_enumeration(self,
                                   project_id: str,
                                   enum_context: str,
                                   enum_name: str,
                                   target_type: str) -> requests.Response:
        """
        Deletes the specified Enumeration from the Project context.
        
        Args:
            project_id: The Project ID
            enum_context: The Enumeration context (Allowed values: '~', 'plans', 'testing', 'documents'. Use '~' for Work Item or general enumerations)
            enum_name: The Enumeration Name
            target_type: The Enumeration target type (Use '~' when there is no specific type)
            
        Returns:
            Response object (204 No Content on success)
        """
        return self._delete(
            f'projects/{project_id}/enumerations/{enum_context}/{enum_name}/{target_type}'
        )
    
    # ========== GET methods ==========
    
    def get_global_enumeration(self,
                              enum_context: str,
                              enum_name: str,
                              target_type: str,
                              fields: Optional[Dict[str, str]] = None,
                              include: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Enumeration from the Global context.
        
        Args:
            enum_context: The Enumeration context (Allowed values: '~', 'plans', 'testing', 'documents'. Use '~' for Work Item or general enumerations)
            enum_name: The Enumeration Name
            target_type: The Enumeration target type (Use '~' when there is no specific type)
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
            Response object containing the enumeration
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
            
        return self._get(
            f'enumerations/{enum_context}/{enum_name}/{target_type}',
            params=params if params else None
        )
    
    def get_project_enumeration(self,
                               project_id: str,
                               enum_context: str,
                               enum_name: str,
                               target_type: str,
                               fields: Optional[Dict[str, str]] = None,
                               include: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Enumeration from the Project context.
        
        Args:
            project_id: The Project ID
            enum_context: The Enumeration context (Allowed values: '~', 'plans', 'testing', 'documents'. Use '~' for Work Item or general enumerations)
            enum_name: The Enumeration Name
            target_type: The Enumeration target type (Use '~' when there is no specific type)
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
            Response object containing the enumeration
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
            
        return self._get(
            f'projects/{project_id}/enumerations/{enum_context}/{enum_name}/{target_type}',
            params=params if params else None
        )
    
    # ========== PATCH methods ==========
    
    def patch_global_enumeration(self,
                                enum_context: str,
                                enum_name: str,
                                target_type: str,
                                enumeration_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Enumeration in the Global context.
        
        Args:
            enum_context: The Enumeration context (Allowed values: '~', 'plans', 'testing', 'documents'. Use '~' for Work Item or general enumerations)
            enum_name: The Enumeration Name
            target_type: The Enumeration target type (Use '~' when there is no specific type)
            enumeration_data: The Enumeration(s) body. Expected structure:
                             {
                                 "data": {
                                     "type": "enumerations",
                                     "id": "~/status/~",
                                     "attributes": {
                                         "options": [
                                             {
                                                 "id": "open",
                                                 "name": "Open",
                                                 "color": "#F9FF4D",
                                                 "description": "Description",
                                                 "hidden": false,
                                                 "default": true,
                                                 "parent": true,
                                                 "oppositeName": "Opposite Name",
                                                 "columnWidth": "90%",
                                                 "iconURL": "/polarion/icons/default/enums/status_open.gif",
                                                 "createDefect": true,
                                                 "templateWorkItem": "exampleTemplate",
                                                 "minValue": 30,
                                                 "requiresSignatureForTestCaseExecution": true,
                                                 "terminal": true,
                                                 "limited": true
                                             }
                                         ]
                                     }
                                 }
                             }
            
        Returns:
            Response object (204 No Content on success)
        """
        return self._patch(
            f'enumerations/{enum_context}/{enum_name}/{target_type}',
            json=enumeration_data
        )
    
    def patch_project_enumeration(self,
                                 project_id: str,
                                 enum_context: str,
                                 enum_name: str,
                                 target_type: str,
                                 enumeration_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Enumeration in the Project context.
        
        Args:
            project_id: The Project ID
            enum_context: The Enumeration context (Allowed values: '~', 'plans', 'testing', 'documents'. Use '~' for Work Item or general enumerations)
            enum_name: The Enumeration Name
            target_type: The Enumeration target type (Use '~' when there is no specific type)
            enumeration_data: The Enumeration(s) body. Expected structure:
                             {
                                 "data": {
                                     "type": "enumerations",
                                     "id": "~/status/~",
                                     "attributes": {
                                         "options": [
                                             {
                                                 "id": "open",
                                                 "name": "Open",
                                                 "color": "#F9FF4D",
                                                 "description": "Description",
                                                 "hidden": false,
                                                 "default": true,
                                                 "parent": true,
                                                 "oppositeName": "Opposite Name",
                                                 "columnWidth": "90%",
                                                 "iconURL": "/polarion/icons/default/enums/status_open.gif",
                                                 "createDefect": true,
                                                 "templateWorkItem": "exampleTemplate",
                                                 "minValue": 30,
                                                 "requiresSignatureForTestCaseExecution": true,
                                                 "terminal": true,
                                                 "limited": true
                                             }
                                         ]
                                     }
                                 }
                             }
            
        Returns:
            Response object (204 No Content on success)
        """
        return self._patch(
            f'projects/{project_id}/enumerations/{enum_context}/{enum_name}/{target_type}',
            json=enumeration_data
        )
    
    # ========== POST methods ==========
    
    def post_global_enumeration(self,
                               enumeration_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Enumerations in the Global context.
        
        Args:
            enumeration_data: The Enumeration(s) body. Expected structure:
                             {
                                 "data": [
                                     {
                                         "type": "enumerations",
                                         "attributes": {
                                             "enumContext": "id",
                                             "enumName": "id",
                                             "options": [
                                                 {
                                                     "id": "open",
                                                     "name": "Open",
                                                     "color": "#F9FF4D",
                                                     "description": "Description",
                                                     "hidden": false,
                                                     "default": true,
                                                     "parent": true,
                                                     "oppositeName": "Opposite Name",
                                                     "columnWidth": "90%",
                                                     "iconURL": "/polarion/icons/default/enums/status_open.gif",
                                                     "createDefect": true,
                                                     "templateWorkItem": "exampleTemplate",
                                                     "minValue": 30,
                                                     "requiresSignatureForTestCaseExecution": true,
                                                     "terminal": true,
                                                     "limited": true
                                                 }
                                             ],
                                             "targetType": "id"
                                         }
                                     }
                                 ]
                             }
            
        Returns:
            Response object (201 Created)
        """
        return self._post('enumerations', json=enumeration_data)
    
    def post_project_enumeration(self,
                                project_id: str,
                                enumeration_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Enumerations in the Project context.
        
        Args:
            project_id: The Project ID
            enumeration_data: The Enumeration(s) body. Expected structure:
                             {
                                 "data": [
                                     {
                                         "type": "enumerations",
                                         "attributes": {
                                             "enumContext": "id",
                                             "enumName": "id",
                                             "options": [
                                                 {
                                                     "id": "open",
                                                     "name": "Open",
                                                     "color": "#F9FF4D",
                                                     "description": "Description",
                                                     "hidden": false,
                                                     "default": true,
                                                     "parent": true,
                                                     "oppositeName": "Opposite Name",
                                                     "columnWidth": "90%",
                                                     "iconURL": "/polarion/icons/default/enums/status_open.gif",
                                                     "createDefect": true,
                                                     "templateWorkItem": "exampleTemplate",
                                                     "minValue": 30,
                                                     "requiresSignatureForTestCaseExecution": true,
                                                     "terminal": true,
                                                     "limited": true
                                                 }
                                             ],
                                             "targetType": "id"
                                         }
                                     }
                                 ]
                             }
            
        Returns:
            Response object (201 Created)
        """
        return self._post(f'projects/{project_id}/enumerations', json=enumeration_data)
