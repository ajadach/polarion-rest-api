"""
Plans module for Polarion REST API.
Handles all Plans related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class Plans(PolarionBase):
    """
    Class for handling Plans operations in Polarion REST API.
    Provides methods for creating, reading, updating, and deleting plans and plan relationships.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - DELETE methods: Delete plans and plan relationships
    - GET methods: Retrieve plans and plan relationships
    - PATCH methods: Update plans and plan relationships
    - POST methods: Create plans and plan relationships
    """
    
    # ========== DELETE methods ==========
    
    def delete_plans(self,
                    project_id: str,
                    plans_data: Dict[str, Any]) -> requests.Response:
        """
        Deletes a list of Plans.
        
        Args:
            project_id: The Project ID
            plans_data: The Plan(s) body
            
        Returns:
            Response object
        """
        return self._delete_with_body(f'projects/{project_id}/plans', json=plans_data)
    
    def delete_plan(self,
                   project_id: str,
                   plan_id: str) -> requests.Response:
        """
        Deletes the specified Plan.
        
        Args:
            project_id: The Project ID
            plan_id: The Plan ID
            
        Returns:
            Response object
        """
        return self._delete(f'projects/{project_id}/plans/{plan_id}')
    
    def delete_plan_relationship(self,
                                project_id: str,
                                plan_id: str,
                                relationship_id: str,
                                relationship_data: Dict[str, Any]) -> requests.Response:
        """
        Removes the specific Relationship from the Plan.
        
        Args:
            project_id: The Project ID
            plan_id: The Plan ID
            relationship_id: The Relationship ID
            relationship_data: The Relationship body
            
        Returns:
            Response object
        """
        return self._delete_with_body(
            f'projects/{project_id}/plans/{plan_id}/relationships/{relationship_id}',
            json=relationship_data
        )
    
    # ========== GET methods ==========
    
    def get_plans(self,
                 project_id: str,
                 page_size: Optional[int] = None,
                 page_number: Optional[int] = None,
                 fields: Optional[Dict[str, str]] = None,
                 include: Optional[str] = None,
                 query: Optional[str] = None,
                 sort: Optional[str] = None,
                 revision: Optional[str] = None,
                 templates: Optional[bool] = None) -> requests.Response:
        """
        Returns a list of Plans.
        
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
            query: The query string
            sort: The sort string
            revision: The revision ID
            templates: If true, only templates will be returned, otherwise only actual instances
            
        Returns:
            Response object containing list of plans
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
        if templates is not None:
            params['templates'] = templates
            
        return self._get(f'projects/{project_id}/plans', params=params if params else None)
    
    def get_plan(self,
                project_id: str,
                plan_id: str,
                fields: Optional[Dict[str, str]] = None,
                include: Optional[str] = None,
                revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Plan.
        
        Args:
            project_id: The Project ID
            plan_id: The Plan ID
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
            Response object containing the plan
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(f'projects/{project_id}/plans/{plan_id}', 
                        params=params if params else None)
    
    def get_plan_relationship(self,
                            project_id: str,
                            plan_id: str,
                            relationship_id: str,
                            page_size: Optional[int] = None,
                            page_number: Optional[int] = None,
                            fields: Optional[Dict[str, str]] = None,
                            include: Optional[str] = None,
                            revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Plan Relationships.
        
        Args:
            project_id: The Project ID
            plan_id: The Plan ID
            relationship_id: The Relationship ID
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
            Response object containing plan relationships
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
            f'projects/{project_id}/plans/{plan_id}/relationships/{relationship_id}',
            params=params if params else None
        )
    
    # ========== PATCH methods ==========
    
    def patch_plan(self,
                  project_id: str,
                  plan_id: str,
                  plan_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified Plan.
        
        Args:
            project_id: The Project ID
            plan_id: The Plan ID
            plan_data: The Plan body
            
        Returns:
            Response object
        """
        return self._patch(f'projects/{project_id}/plans/{plan_id}', json=plan_data)
    
    def patch_plan_relationships(self,
                                project_id: str,
                                plan_id: str,
                                relationship_id: str,
                                relationships_data: Dict[str, Any]) -> requests.Response:
        """
        Updates a list of Plan Relationships.
        
        Args:
            project_id: The Project ID
            plan_id: The Plan ID
            relationship_id: The Relationship ID
            relationships_data: The Work Item(s) body
            
        Returns:
            Response object
        """
        return self._patch(
            f'projects/{project_id}/plans/{plan_id}/relationships/{relationship_id}',
            json=relationships_data
        )
    
    # ========== POST methods ==========
    
    def post_plans(self,
                  project_id: str,
                  plans_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Plans.
        
        Args:
            project_id: The Project ID
            plans_data: The Plan(s) body
            
        Returns:
            Response object
        """
        return self._post(f'projects/{project_id}/plans', json=plans_data)
    
    def post_plan_relationships(self,
                               project_id: str,
                               plan_id: str,
                               relationship_id: str,
                               relationships_data: Dict[str, Any]) -> requests.Response:
        """
        Creates the specific Relationships for the Plan.
        
        Args:
            project_id: The Project ID
            plan_id: The Plan ID
            relationship_id: The Relationship ID
            relationships_data: The Work Item(s) body
            
        Returns:
            Response object
        """
        return self._post(
            f'projects/{project_id}/plans/{plan_id}/relationships/{relationship_id}',
            json=relationships_data
        )
