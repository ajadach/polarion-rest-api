"""
Work Items module for Polarion REST API.
Handles all Work Items related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class WorkItems(PolarionBase):
    """
    Class for handling Work Items operations in Polarion REST API.
    Provides methods for creating, reading, updating, and deleting work items.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete work items
    - GET methods: Retrieve work items and related data
    - PATCH methods: Update work items
    - POST methods: Create work items and perform actions
    """
    
    # ========== DELETE methods ==========
    
    def delete_all_work_items(self, work_items_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Work Items from the Global context.
        
        Args:
            work_items_data: The Work Item(s) body. Must contain a 'data' key with a list of work items.
            
        Returns:
            Response object
            
        Raises:
            ValueError: If work_items_data doesn't have the correct structure
            
        Example:
            >>> work_items_data = {
            ...     "data": [
            ...         {
            ...             "type": "workitems",
            ...             "id": "MyProjectId/MyWorkItemId"
            ...         }
            ...     ]
            ... }
            >>> response = api.delete_all_work_items(work_items_data)
        """
        self._validate_delete_body(work_items_data, "work_items_data")
        return self._delete_with_body('all/workitems', json=work_items_data)
    
    def delete_work_items(self, 
                         project_id: str,
                         work_items_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Work Items from a project.
        
        Args:
            project_id: The Project ID
            work_items_data: The Work Item(s) body. Must contain a 'data' key with a list of work items.
            
        Returns:
            Response object
            
        Raises:
            ValueError: If work_items_data doesn't have the correct structure
            
        Example:
            >>> work_items_data = {
            ...     "data": [
            ...         {
            ...             "type": "workitems",
            ...             "id": "MyProjectId/MyWorkItemId"
            ...         },
            ...         {
            ...             "type": "workitems",
            ...             "id": "MyProjectId/MyWorkItemId2"
            ...         }
            ...     ]
            ... }
            >>> response = api.delete_work_items("MyProjectId", work_items_data)
        """
        self._validate_delete_body(work_items_data, "work_items_data")
        return self._delete_with_body(f'projects/{project_id}/workitems', json=work_items_data)
    
    def delete_work_items_relationship(self,
                                      project_id: str,
                                      work_item_id: str,
                                      relationship_id: str,
                                      relationships_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Work Item Relationships.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            relationship_id: The Relationship ID (e.g., 'parent', 'child', 'relates_to')
            relationships_data: The Relationship body. Must contain a 'data' key with a list of related work items.
            
        Returns:
            Response object
            
        Raises:
            ValueError: If relationships_data doesn't have the correct structure
            
        Example:
            >>> relationships_data = {
            ...     "data": [
            ...         {
            ...             "type": "workitems",
            ...             "id": "MyProjectId/RelatedWorkItemId"
            ...         }
            ...     ]
            ... }
            >>> response = api.delete_work_items_relationship(
            ...     "MyProjectId", 
            ...     "MyWorkItemId", 
            ...     "parent", 
            ...     relationships_data
            ... )
        """
        self._validate_delete_body(relationships_data, "relationships_data")
        return self._delete_with_body(
            f'projects/{project_id}/workitems/{work_item_id}/relationships/{relationship_id}',
            json=relationships_data
        )
    
    # ========== GET methods ==========
    
    def get_all_work_items(self, 
                          page_size: Optional[int] = None,
                          page_number: Optional[int] = None,
                          fields: Optional[Dict[str, str]] = None,
                          include: Optional[str] = None,
                          query: Optional[str] = None,
                          sort: Optional[str] = None,
                          revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Work Items from the Global context.
        
        Args:
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
            query: The query string
            sort: The sort string
            revision: The revision ID
            
        Returns:
            Response object with work items data
        """
        params = self._apply_default_fields(fields)
        
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if include:
            params['include'] = include
        if query:
            params['query'] = query
        if sort:
            params['sort'] = sort
        if revision:
            params['revision'] = revision
        
        return self._get('all/workitems', params=params)
    
    def get_work_items(self, 
                      project_id: str,
                      page_size: Optional[int] = None,
                      page_number: Optional[int] = None,
                      fields: Optional[Dict[str, str]] = None,
                      include: Optional[str] = None,
                      query: Optional[str] = None,
                      sort: Optional[str] = None,
                      revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Work Items from a project.
        
        Args:
            project_id: The Project ID
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
            query: The query string
            sort: The sort string
            revision: The revision ID
            
        Returns:
            Response object with work items data
        """
        params = self._apply_default_fields(fields)
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if include:
            params['include'] = include
        if query:
            params['query'] = query
        if sort:
            params['sort'] = sort
        if revision:
            params['revision'] = revision
        
        return self._get(f'projects/{project_id}/workitems', params=params)
    
    def get_work_item(self, 
                     project_id: str,
                     work_item_id: str,
                     fields: Optional[Dict[str, str]] = None,
                     include: Optional[str] = None,
                     revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Work Item.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
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
            Response object with work item data
        """
        params = self._apply_default_fields(fields)
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
        
        return self._get(f'projects/{project_id}/workitems/{work_item_id}', params=params)
    
    def get_current_enum_options_for_work_item(self,
                                project_id: str,
                                work_item_id: str,
                                field_id: str,
                                page_size: Optional[int] = None,
                                page_number: Optional[int] = None,
                                revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of selected options for the requested field for specific Work Item.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            field_id: The Field ID
            page_size: Limit the number of entities returned
            page_number: Specify the page number (starts from 1)
            revision: The revision ID
            
        Returns:
            Response object with enum options
        """
        params = {}
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if revision:
            params['revision'] = revision
        
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/fields/{field_id}/actions/getCurrentOptions',
            params=params
        )
    
    def get_available_enum_options_for_work_item(self,
                                                 project_id: str,
                                                 work_item_id: str,
                                                 field_id: str,
                                                 page_size: Optional[int] = None,
                                                 page_number: Optional[int] = None) -> requests.Response:
        """
        Returns a list of available options for the requested field for the specified Work Item.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            field_id: The Field ID
            page_size: Limit the number of entities returned
            page_number: Specify the page number (starts from 1)
            
        Returns:
            Response object with enum options
        """
        params = {}
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/fields/{field_id}/actions/getAvailableOptions',
            params=params
        )
    
    def get_available_enum_options_for_work_item_type(self,
                                           project_id: str,
                                           field_id: str,
                                           work_item_type: Optional[str] = None,
                                           page_size: Optional[int] = None,
                                           page_number: Optional[int] = None) -> requests.Response:
        """
        Returns a list of available options for the requested field for the specified Work Item Type.
        
        Args:
            project_id: The Project ID
            field_id: The Field ID
            work_item_type: The Type of the object
            page_size: Limit the number of entities returned
            page_number: Specify the page number (starts from 1)
            
        Returns:
            Response object with enum options
        """
        params = {}
        if work_item_type:
            params['type'] = work_item_type
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        
        return self._get(
            f'projects/{project_id}/workitems/fields/{field_id}/actions/getAvailableOptions',
            params=params
        )
    
    def get_workflow_actions_for_work_item(self,
                           project_id: str,
                           work_item_id: str,
                           page_size: Optional[int] = None,
                           page_number: Optional[int] = None) -> requests.Response:
        """
        Returns a list of Workflow Actions for a Work Item.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            page_size: Limit the number of entities returned
            page_number: Specify the page number (starts from 1)
            
        Returns:
            Response object with workflow actions
        """
        params = {}
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/actions/getWorkflowActions',
            params=params
        )
    
    def get_work_item_test_parameter_definitions(self,
                                      project_id: str,
                                      work_item_id: str,
                                      page_size: Optional[int] = None,
                                      page_number: Optional[int] = None,
                                      fields: Optional[Dict[str, str]] = None,
                                      include: Optional[str] = None,
                                      revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Test Parameter Definitions for a Work Item.
        
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
            Response object with test parameter definitions
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
            f'projects/{project_id}/workitems/{work_item_id}/testparameterdefinitions',
            params=params
        )
    
    def get_work_item_test_parameter_definition(self,
                                     project_id: str,
                                     work_item_id: str,
                                     test_param_id: str,
                                     fields: Optional[Dict[str, str]] = None,
                                     include: Optional[str] = None,
                                     revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Test Parameter Definition for a Work Item.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
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
            revision: The revision ID
            
        Returns:
            Response object with test parameter definition
        """
        params = self._apply_default_fields(fields)
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
        
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/testparameterdefinitions/{test_param_id}',
            params=params
        )
    
    def get_work_items_relationships(self,
                                   project_id: str,
                                   work_item_id: str,
                                   relationship_id: str,
                                   page_size: Optional[int] = None,
                                   page_number: Optional[int] = None,
                                   revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Work Item Relationships.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            relationship_id: The Relationship ID
            page_size: Limit the number of entities returned
            page_number: Specify the page number (starts from 1)
            revision: The revision ID
            
        Returns:
            Response object with relationships
        """
        params = {}
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if revision:
            params['revision'] = revision
        
        return self._get(
            f'projects/{project_id}/workitems/{work_item_id}/relationships/{relationship_id}',
            params=params
        )
    
    # ========== PATCH methods ==========
    
    def patch_all_work_items(self, 
                            work_items_data: Dict[str, Any],
                            workflow_action: Optional[str] = None,
                            change_type_to: Optional[str] = None) -> requests.Response:
        """
        Updates a list of Work Items in the Global context.
        
        Args:
            work_items_data: The Work Item(s) body
            workflow_action: The Workflow Action
            change_type_to: The Type the Workitem to change to
            
        Returns:
            Response object
        """
        params = {}
        if workflow_action:
            params['workflowAction'] = workflow_action
        if change_type_to:
            params['changeTypeTo'] = change_type_to
        
        return self._patch('all/workitems', json=work_items_data, params=params)
    
    def patch_work_items(self, 
                         project_id: str,
                         work_items_data: Dict[str, Any],
                         workflow_action: Optional[str] = None,
                         change_type_to: Optional[str] = None) -> requests.Response:
        """
        Updates a list of Work Items in a project.
        
        Args:
            project_id: The Project ID
            work_items_data: The Work Item(s) body
            workflow_action: The Workflow Action
            change_type_to: The Type the Workitem to change to
            
        Returns:
            Response object
        """
        params = {}
        if workflow_action:
            params['workflowAction'] = workflow_action
        if change_type_to:
            params['changeTypeTo'] = change_type_to
        
        return self._patch(f'projects/{project_id}/workitems', json=work_items_data, params=params)
    
    def patch_work_item(self, 
                        project_id: str,
                        work_item_id: str,
                        work_item_data: Dict[str, Any],
                        workflow_action: Optional[str] = None,
                        change_type_to: Optional[str] = None) -> requests.Response:
        """
        Updates the specified Work Item.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            work_item_data: The Work Item body
            workflow_action: The Workflow Action
            change_type_to: The Type the Workitem to change to
            
        Returns:
            Response object
        """
        params = {}
        if workflow_action:
            params['workflowAction'] = workflow_action
        if change_type_to:
            params['changeTypeTo'] = change_type_to
        
        return self._patch(f'projects/{project_id}/workitems/{work_item_id}', 
                          json=work_item_data, params=params)
    
    def patch_work_item_relationships(self,
                                      project_id: str,
                                      work_item_id: str,
                                      relationship_id: str,
                                      relationships_data: Dict[str, Any]) -> requests.Response:
        """
        Updates a list of Work Item Relationships.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            relationship_id: The Relationship ID
            relationships_data: The Relationship body
            
        Returns:
            Response object
        """
        return self._patch(
            f'projects/{project_id}/workitems/{work_item_id}/relationships/{relationship_id}',
            json=relationships_data
        )
    
    # ========== POST methods ==========
    
    def post_work_items(self, 
                         project_id: str,
                         work_items_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Work Items in a project.
        
        Args:
            project_id: The Project ID
            work_items_data: The Work Item(s) body
            
        Returns:
            Response object with created work items
        """
        return self._post(f'projects/{project_id}/workitems', json=work_items_data)
    
    def post_work_item_relationships(self,
                                      project_id: str,
                                      work_item_id: str,
                                      relationship_id: str,
                                      relationships_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Work Item Relationships.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            relationship_id: The Relationship ID
            relationships_data: The Relationship body
            
        Returns:
            Response object
        """
        return self._post(
            f'projects/{project_id}/workitems/{work_item_id}/relationships/{relationship_id}',
            json=relationships_data
        )
    
    def move_from_document(self,
                          project_id: str,
                          work_item_id: str) -> requests.Response:
        """
        Moves the specified Work Item from the Document.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            
        Returns:
            Response object
        """
        return self._post(
            f'projects/{project_id}/workitems/{work_item_id}/actions/moveFromDocument',
            json={}
        )
    
    def move_to_document(self,
                        project_id: str,
                        work_item_id: str,
                        request_body: Dict[str, Any]) -> requests.Response:
        """
        Moves the specified Work Item to the Document.
        
        Args:
            project_id: The Project ID
            work_item_id: The Work Item ID
            request_body: Request body with targetDocument, previousPart, nextPart
            
        Returns:
            Response object
        """
        return self._post(
            f'projects/{project_id}/workitems/{work_item_id}/actions/moveToDocument',
            json=request_body
        )
    
    # ========== Helper methods ==========
    
    def _validate_delete_body(self, body_data: Dict[str, Any], param_name: str) -> None:
        """
        Validates the structure of DELETE request body.
        
        Args:
            body_data: The body data to validate
            param_name: Name of the parameter (for error messages)
            
        Raises:
            ValueError: If body_data doesn't have the correct structure
            
        Expected structure:
            {
                "data": [
                    {
                        "type": "workitems",
                        "id": "ProjectId/WorkItemId"
                    }
                ]
            }
        """
        if not isinstance(body_data, dict):
            raise ValueError(
                f"{param_name} must be a dictionary. "
                f"Expected format: {{'data': [{{'type': '...', 'id': '...'}}]}}"
            )
        
        if 'data' not in body_data:
            raise ValueError(
                f"{param_name} must contain a 'data' key. "
                f"Expected format: {{'data': [{{'type': '...', 'id': '...'}}]}}"
            )
        
        if not isinstance(body_data['data'], list):
            raise ValueError(
                f"{param_name}['data'] must be a list (array). "
                f"Got {type(body_data['data']).__name__} instead. "
                f"Expected format: {{'data': [{{'type': '...', 'id': '...'}}]}}"
            )
        
        # Validate each item in the data array
        for idx, item in enumerate(body_data['data']):
            if not isinstance(item, dict):
                raise ValueError(
                    f"{param_name}['data'][{idx}] must be a dictionary. "
                    f"Expected format: {{'type': '...', 'id': '...'}}"
                )
            
            if 'type' not in item:
                raise ValueError(
                    f"{param_name}['data'][{idx}] must contain a 'type' key. "
                    f"Expected format: {{'type': '...', 'id': '...'}}"
                )
            
            if 'id' not in item:
                raise ValueError(
                    f"{param_name}['data'][{idx}] must contain an 'id' key. "
                    f"Expected format: {{'type': '...', 'id': '...'}}"
                )
    
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
