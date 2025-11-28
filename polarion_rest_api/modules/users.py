"""
Users module for Polarion REST API.
Handles all Users related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class Users(PolarionBase):
    """
    Class for handling Users operations in Polarion REST API.
    Provides methods for creating, reading, and updating users.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve users and related data
    - PATCH methods: Update users
    - POST methods: Create users and perform actions
    """
    
    # ========== GET methods ==========
    
    def get_users(self,
                  page_size: Optional[int] = None,
                  page_number: Optional[int] = None,
                  fields: Optional[Dict[str, str]] = None,
                  include: Optional[str] = None,
                  query: Optional[str] = None,
                  sort: Optional[str] = None,
                  revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Users.
        
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
            Response object with users data
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
        
        return self._get('users', params=params)
    
    def get_user(self,
                 user_id: str,
                 fields: Optional[Dict[str, str]] = None,
                 include: Optional[str] = None,
                 revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified User.
        
        Args:
            user_id: The User ID
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
            Response object with user data
        """
        params = self._apply_default_fields(fields)
        if include:
            params['include'] = include
        if revision:
            params['revision'] = revision
        
        return self._get(f'users/{user_id}', params=params)
    
    def get_avatar(self,
                   user_id: str) -> requests.Response:
        """
        Returns the specified User Avatar.
        
        Args:
            user_id: The User ID
            
        Returns:
            Response object with avatar data (application/octet-stream)
        """
        return self._get(f'users/{user_id}/actions/getAvatar')
    
    # ========== PATCH methods ==========
    
    def patch_user(self,
                   user_id: str,
                   user_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified User.
        
        Args:
            user_id: The User ID
            user_data: The User body
            
        Returns:
            Response object
        """
        return self._patch(f'users/{user_id}', json=user_data)
    
    # ========== POST methods ==========
    
    def post_users(self,
                   users_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Users.
        
        Args:
            users_data: The User(s) body
            
        Returns:
            Response object with created users
        """
        return self._post('users', json=users_data)
    
    def update_avatar(self,
                     user_id: str,
                     avatar_data: Dict[str, Any]) -> requests.Response:
        """
        Updates the specified User Avatar.
        Note: This endpoint uses multipart/form-data content type.
        
        Args:
            user_id: The User ID
            avatar_data: Avatar file data (multipart/form-data)
            
        Returns:
            Response object
        """
        return self._post(f'users/{user_id}/actions/updateAvatar', json=avatar_data)
    
    def set_license(self,
                   user_id: str,
                   license_data: Dict[str, Any]) -> requests.Response:
        """
        Sets the User's license.
        
        Args:
            user_id: The User ID
            license_data: The user license body
            
        Returns:
            Response object
        """
        return self._post(f'users/{user_id}/actions/setLicense', json=license_data)
