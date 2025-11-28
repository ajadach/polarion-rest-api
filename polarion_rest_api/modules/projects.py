"""
Projects module for Polarion REST API.
Handles all Projects related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class Projects(PolarionBase):
    """
    Class for handling Projects operations in Polarion REST API.
    Provides methods for creating, reading, updating, and deleting projects.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete projects and test parameter definitions
    - GET methods: Retrieve projects and test parameter definitions
    - PATCH methods: Update projects
    - POST methods: Create projects and perform actions
    """
    
    # ========== DELETE methods ==========
    
    def delete_project(self, project_id: str) -> requests.Response:
        """
        Deletes the specified Project.
        
        Args:
            project_id: The Project ID
            
        Returns:
            Response object
        """
        return self._delete(f'projects/{project_id}')
    
    def delete_project_test_parameter_definitions(self,
                                                  project_id: str,
                                                  test_param_definitions: list[Dict[str, str]]) -> requests.Response:
        """
        Deletes a list of Test Parameter Definitions for the specified Project.
        
        Args:
            project_id: The Project ID
            test_param_definitions: List of test parameter definitions to delete.
                                   Each item must be a dict with 'type' and 'id' keys.
            
        Returns:
            Response object
            
        Example:
            delete_project_test_parameter_definitions(
                project_id="MyProject",
                test_param_definitions=[
                    {
                        "type": "param1",
                        "id": "MyProject/MyTestParamDefinition1"
                    },
                    {
                        "type": "param2",
                        "id": "MyProject/MyTestParamDefinition2"
                    }
                ]
            )
        """
        # Build request body
        data = {
            "data": test_param_definitions
        }
        
        return self._delete_with_body(f'projects/{project_id}/testparameterdefinitions', 
                                     json=data)
    
    def delete_project_test_parameter_definition(self,
                                                project_id: str,
                                                test_param_id: str) -> requests.Response:
        """
        Deletes the specified Test Parameter Definition for the specified Project.
        
        Args:
            project_id: The Project ID
            test_param_id: The Test Parameter ID
            
        Returns:
            Response object
        """
        return self._delete(f'projects/{project_id}/testparameterdefinitions/{test_param_id}')
    
    # ========== GET methods ==========
    
    def get_project(self,
                   project_id: str,
                   fields: Optional[Dict[str, str]] = None,
                   include: Optional[str] = None,
                   revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Project.
        
        Args:
            project_id: The Project ID
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
                   
                   Example:
                       # All fields use default "@all"
                       get_project("YOUR_PROJECT_ID")
                       
                       # Override only "workitems" and "users", rest stays "@all"
                       get_project("YOUR_PROJECT_ID", fields={"workitems": "id,title", "users": "name"})
                   
            include: Include related entities
            revision: The revision ID
            
        Returns:
            Response object containing the project
        """
        params = self._apply_default_fields(fields)
            
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(f'projects/{project_id}', params=params if params else None)
    
    def get_project_test_parameter_definitions(self,
                                              project_id: str,
                                              page_size: Optional[int] = None,
                                              page_number: Optional[int] = None,
                                              fields: Optional[Dict[str, str]] = None,
                                              include: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Test Parameter Definitions for the specified Project.
        
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
            include: Include related entities
            
        Returns:
            Response object containing list of test parameter definitions
        """
        params = self._apply_default_fields(fields)
            
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if include is not None:
            params['include'] = include
            
        return self._get(f'projects/{project_id}/testparameterdefinitions', 
                        params=params if params else None)
    
    def get_project_test_parameter_definition(self,
                                             project_id: str,
                                             test_param_id: str,
                                             fields: Optional[Dict[str, str]] = None,
                                             include: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Test Parameter Definition for the specified Project.
        
        Args:
            project_id: The Project ID
            test_param_id: The Test Parameter ID
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
            Response object containing the test parameter definition
        """
        params = self._apply_default_fields(fields)
            
        if include is not None:
            params['include'] = include
            
        return self._get(f'projects/{project_id}/testparameterdefinitions/{test_param_id}', 
                        params=params if params else None)
    
    def get_projects(self,
                    page_size: Optional[int] = None,
                    page_number: Optional[int] = None,
                    fields: Optional[Dict[str, str]] = None,
                    include: Optional[str] = None,
                    query: Optional[str] = None,
                    sort: Optional[str] = None,
                    revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Projects.
        
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
            revision: The revision ID
            
        Returns:
            Response object containing list of projects
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
        if revision is not None:
            params['revision'] = revision
            
        return self._get('projects', params=params if params else None)
    
    # ========== PATCH methods ==========
    
    def patch_project(self,
                     project_id: str,
                     project_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Project.
        
        Args:
            project_id: The Project ID
            project_data: The Project body
            
        Returns:
            Response object
        """
        return self._patch(f'projects/{project_id}', json=project_data)
    
    # ========== POST methods ==========
    
    def post_mark_project(self, **kwargs) -> requests.Response:
        """
        Marks the Project.
        
        Args:
            **kwargs: Create project parameters with the following keys:
                - projectId (str, required): The Project ID
                - trackerPrefix (str, required): The tracker prefix
                - location (str, required): The location
                - templateId (str, required): The project template ID
                - params (dict, optional): Additional parameters (defaults to empty dict)
            
        Returns:
            Response object
            
        Raises:
            ValueError: If any required parameter is missing
            
        Example:
            post_mark_project(
                projectId="MyProjectId",
                trackerPrefix="MyTrackerPrefix",
                location="MyLocation",
                templateId="MyProjectTemplateId",
                params={}
            )
        """
        required_params = ['projectId', 'trackerPrefix', 'location', 'templateId']
        missing_params = [param for param in required_params if param not in kwargs]
        
        if missing_params:
            raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")
        
        data = {
            "projectId": kwargs['projectId'],
            "trackerPrefix": kwargs['trackerPrefix'],
            "location": kwargs['location'],
            "templateId": kwargs['templateId'],
            "params": kwargs.get('params', {})
        }
        
        return self._post('projects/actions/markProject', json=data)
    
    def post_move_project_action(self,
                          project_id: str,
                          **kwargs) -> requests.Response:
        """
        Moves project to a different location.
        
        Args:
            project_id: The Project ID
            **kwargs: Move project parameters with the following keys:
                - location (str, required): The new location for the project
            
        Returns:
            Response object
            
        Raises:
            ValueError: If the required parameter is missing
            
        Example:
            post_move_project_action(
                project_id="OT",
                location="MyLocation"
            )
        """
        if 'location' not in kwargs:
            raise ValueError("Missing required parameter: location")
        
        data = {
            "location": kwargs['location']
        }
        
        return self._post(f'projects/{project_id}/actions/moveProject', json=data)
    
    def post_project_test_parameter_definitions(self,
                                               project_id: str,
                                               test_params_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Test Parameter Definitions for the specified Project.
        
        Args:
            project_id: The Project ID
            test_params_data: The Test Parameter Definition(s) body.
                             Must follow the JSON API format with a 'data' array containing
                             test parameter definition objects.
                             
                             Example structure:
                             {
                                 "data": [
                                     {
                                         "type": "testparameter_definitions",
                                         "attributes": {
                                             "name": "Test Parameter Definition example"
                                         }
                                     }
                                 ]
                             }
            
        Returns:
            Response object
        """
        return self._post(f'projects/{project_id}/testparameterdefinitions', 
                         json=test_params_data)
    
    def post_create_project(self, **kwargs) -> requests.Response:
        """
        Creates a new Project.
        
        Required kwargs:
            projectId (str): The project ID
            trackerPrefix (str): The tracker prefix
            location (str): The location
            templateId (str): The template ID
        
        Optional kwargs:
            Any other project creation parameters
            
        Returns:
            Response object
            
        Example:
            response = projects.post_create_project(
                projectId='MY_PROJECT',
                trackerPrefix='MYP',
                location='default/MY_PROJECT',
                templateId='agile'
            )
            
        Curl equivalent:
            curl --location 'http://localhost:8080/polarion/rest/v1/projects/actions/createProject' \\
            --header 'Content-Type: application/json' \\
            --header 'Authorization: Basic ...' \\
            --data '{
                "data": {
                    "attributes": {
                        "projectId": "MY_PROJECT",
                        "trackerPrefix": "MYP",
                        "location": "default/MY_PROJECT",
                        "templateId": "agile"
                    },
                    "type": "projects"
                }
            }'
        """
        # Validate required parameters
        required_params = ['projectId', 'trackerPrefix', 'location', 'templateId']
        missing_params = [param for param in required_params if param not in kwargs]
        if missing_params:
            raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")
        
        # Build the request body matching curl format
        data = {
            "projectId": kwargs['projectId'],
            "trackerPrefix": kwargs['trackerPrefix'],
            "location": kwargs['location'],
            "templateId": kwargs['templateId'],
            "params": kwargs.get('params', {})
        }
        
        return self._post('projects/actions/createProject', json=data)
    
    def post_unmark_project(self, project_id: str) -> requests.Response:
        """
        Unmarks the Project.
        
        Args:
            project_id: The Project ID
            
        Returns:
            Response object
        """
        return self._post(f'projects/{project_id}/actions/unmarkProject')
