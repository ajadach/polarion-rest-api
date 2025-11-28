"""
Base module for Polarion REST API communication.
Contains the base class for storing authentication token and common HTTP methods.
"""
import requests
from typing import Optional, Dict, Any


class PolarionBase:
    """
    Base class for Polarion REST API communication.
    Stores authentication token and provides common HTTP methods.
    """
    
    def __init__(self, base_url: str, token: Optional[str] = None):
        """
        Initialize the base class.
        
        Args:
            base_url: Base URL for Polarion REST API (e.g., 'https://testdrive.polarion.com/polarion/rest/v1')
            token: Bearer token for authentication
        """
        self.base_url = base_url.rstrip('/')
        self._token = token
        self._session = requests.Session()
        self._update_headers()
    
    def set_token(self, token: str):
        """
        Set or update the authentication token.
        
        Args:
            token: Bearer token for authentication
        """
        self._token = token
        self._update_headers()
    
    def get_token(self) -> Optional[str]:
        """
        Get the current authentication token.
        
        Returns:
            Current bearer token or None if not set
        """
        return self._token
    
    def _update_headers(self):
        """
        Update session headers with authentication token.
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if self._token:
            headers['Authorization'] = f'Bearer {self._token}'
        
        self._session.headers.update(headers)
    
    def _apply_default_fields(self, user_fields: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Apply default fields configuration for GET requests.
        
        This internal method ensures that all GET requests include default fields
        set to "@all" for all collections. User-provided fields override only
        the specified keys, while all other fields remain set to "@all".
        
        The method converts field names to the proper Polarion API format: fields[name]=value
        
        Default fields include: collections, categories, documents, document_attachments,
        document_comments, document_parts, enumerations, globalroles, icons, jobs,
        linkedworkitems, externallylinkedworkitems, linkedoslcresources, pages,
        page_attachments, plans, projectroles, projects, projecttemplates,
        testparameters, testparameter_definitions, testrecords, teststep_results,
        testruns, testrun_attachments, teststepresult_attachments, testrun_comments,
        usergroups, users, workitems, workitem_attachments, workitem_approvals,
        workitem_comments, featureselections, teststeps, workrecords, revisions,
        testrecord_attachments
        
        Args:
            user_fields: Optional dictionary of user-specified field overrides.
                        Keys can be either "field_name" or "fields[field_name]" format.
            
        Returns:
            Dictionary with default fields in proper format (fields[name]) and user overrides applied
        """
        # Default field names (without fields[] wrapper)
        default_field_names = [
            "collections", "categories", "documents", "document_attachments",
            "document_comments", "document_parts", "enumerations", "globalroles",
            "icons", "jobs", "linkedworkitems", "externallylinkedworkitems",
            "linkedoslcresources", "pages", "page_attachments", "plans",
            "projectroles", "projects", "projecttemplates", "testparameters",
            "testparameter_definitions", "testrecords", "teststep_results",
            "testruns", "testrun_attachments", "teststepresult_attachments",
            "testrun_comments", "usergroups", "users", "workitems",
            "workitem_attachments", "workitem_approvals", "workitem_comments",
            "featureselections", "teststeps", "workrecords", "revisions",
            "testrecord_attachments"
        ]
        
        # Start with default fields in proper format: fields[name]=@all
        result = {f"fields[{name}]": "@all" for name in default_field_names}
        
        # Override with user-provided fields (if any)
        if user_fields is not None:
            for key, value in user_fields.items():
                # If user provides key without fields[] wrapper, add it
                if not key.startswith("fields["):
                    result[f"fields[{key}]"] = value
                else:
                    # User already provided proper format
                    result[key] = value
        
        return result
    
    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Perform GET request.
        
        Args:
            endpoint: API endpoint (will be appended to base_url)
            params: Query parameters
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self._session.get(url, params=params)
        return response
    
    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
              json: Optional[Dict[str, Any]] = None,
              files: Optional[Any] = None,
              params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Perform POST request.
        
        Args:
            endpoint: API endpoint (will be appended to base_url)
            data: Form data
            json: JSON data
            files: Files for multipart/form-data upload (can be dict or list of tuples)
            params: Query parameters
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        # Remove Content-Type header for multipart/form-data (requests will set it automatically)
        headers = None
        if files is not None or (data is not None and json is None):
            # Remove Content-Type for multipart or form data
            headers = {k: v for k, v in self._session.headers.items() if k.lower() != 'content-type'}
        response = self._session.post(url, data=data, json=json, files=files, headers=headers, params=params)
        return response
    
    def _patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
               json: Optional[Dict[str, Any]] = None,
               files: Optional[Dict[str, Any]] = None,
               params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Perform PATCH request.
        
        Args:
            endpoint: API endpoint (will be appended to base_url)
            data: Form data
            json: JSON data
            files: Files for multipart/form-data upload
            params: Query parameters
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        # Remove Content-Type header for multipart/form-data (requests will set it automatically)
        headers = None
        if files is not None or (data is not None and json is None):
            # Remove Content-Type for multipart or form data
            headers = {k: v for k, v in self._session.headers.items() if k.lower() != 'content-type'}
        response = self._session.patch(url, data=data, json=json, files=files, headers=headers, params=params)
        return response
    
    def _delete(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Perform DELETE request.
        
        Args:
            endpoint: API endpoint (will be appended to base_url)
            json: JSON data (for DELETE requests with body)
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self._session.delete(url, json=json)
        return response
    
    def _delete_with_body(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Perform DELETE request with JSON body.
        This is an alias for _delete with json parameter for clarity.
        
        Args:
            endpoint: API endpoint (will be appended to base_url)
            json: JSON data
            
        Returns:
            Response object
        """
        return self._delete(endpoint, json=json)
    
    def close(self):
        """
        Close the session.
        """
        self._session.close()
