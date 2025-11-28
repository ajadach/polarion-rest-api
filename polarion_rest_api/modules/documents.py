"""
Documents module for Polarion REST API.
Handles all Documents related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class Documents(PolarionBase):
    """
    Class for handling Documents operations in Polarion REST API.
    Provides methods for creating, reading, updating documents, and document-specific actions.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve documents and document field options
    - PATCH methods: Update documents
    - POST methods: Create documents and perform document actions (branch, copy, merge)
    """
    
    # ========== GET methods ==========

    def get_document(self,
                    project_id: str,
                    space_id: str,
                    document_name: str,
                    fields: Optional[Dict[str, str]] = None,
                    include: Optional[str] = None,
                    revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Document.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
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
            Response object containing the document
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}',
            params=params if params else None
        )

    def get_available_enum_options_for_document(self,
                                               project_id: str,
                                               space_id: str,
                                               document_name: str,
                                               field_id: str,
                                               page_size: Optional[int] = None,
                                               page_number: Optional[int] = None) -> requests.Response:
        """
        Returns a list of available options for the requested field in the specified Document.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            field_id: The Field ID
            page_size: Limit the number of entities returned in a single response
            page_number: Specify the page number to be returned (counting starts from 1)
            
        Returns:
            Response object containing available enum options
        """
        params = {}
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
            
        return self._get(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/fields/{field_id}/actions/getAvailableOptions',
            params=params if params else None
        )    
   
    def get_current_enumeration_options_for_document(self,
                                                    project_id: str,
                                                    space_id: str,
                                                    document_name: str,
                                                    field_id: str,
                                                    page_size: Optional[int] = None,
                                                    page_number: Optional[int] = None,
                                                    revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of selected options for the requested field in the specified Document.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            field_id: The Field ID
            page_size: Limit the number of entities returned in a single response
            page_number: Specify the page number to be returned (counting starts from 1)
            revision: The revision ID
            
        Returns:
            Response object containing current enum options
        """
        params = {}
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/fields/{field_id}/actions/getCurrentOptions',
            params=params if params else None
        )          

    def get_available_enum_options_for_document_type(self,
                                                    project_id: str,
                                                    field_id: str,
                                                    page_size: Optional[int] = None,
                                                    page_number: Optional[int] = None,
                                                    document_type: Optional[str] = None) -> requests.Response:
        """
        Returns a list of available options for the requested field for the specified Document type.
        
        Args:
            project_id: The Project ID
            field_id: The Field ID
            page_size: Limit the number of entities returned in a single response
            page_number: Specify the page number to be returned (counting starts from 1)
            document_type: The Type of the document
            
        Returns:
            Response object containing available enum options
        """
        params = {}
        if page_size is not None:
            params['page[size]'] = page_size
        if page_number is not None:
            params['page[number]'] = page_number
        if document_type is not None:
            params['type'] = document_type
            
        return self._get(
            f'projects/{project_id}/documents/fields/{field_id}/actions/getAvailableOptions',
            params=params if params else None
        )
 
    # ========== PATCH methods ==========
    
    def patch_document(self,
                      project_id: str,
                      space_id: str,
                      document_name: str,
                      document_data: Dict[str, Any],
                      workflow_action: Optional[str] = None) -> requests.Response:
        """
        Updates the specified Document.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            document_data: The Document body
            workflow_action: The Workflow Action
            
        Returns:
            Response object (204 No Content on success)
        """
        params = {}
        if workflow_action is not None:
            params['workflowAction'] = workflow_action
            
        return self._patch(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}',
            json=document_data,
            params=params if params else None
        )
    
    # ========== POST methods ==========

    def post_branch_document(self,
                       project_id: str,
                       space_id: str,
                       document_name: str,
                       branch_data: Dict[str, Any],
                       revision: Optional[str] = None) -> requests.Response:
        """
        Creates a Branch of the Document.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            branch_data: Branch Document parameters. Example structure:
                {
                    "targetProjectId": "MyProjectId",
                    "targetSpaceId": "MySpaceId",
                    "targetDocumentName": "MyDocumentId",
                    "copyWorkflowStatusAndSignatures": False,
                    "query": "status:open"
                }
                Fields (all optional):
                - targetProjectId (str): Project where new document will be created
                - targetSpaceId (str): Space where new document will be created
                - targetDocumentName (str): Name for new Document
                - copyWorkflowStatusAndSignatures (bool): Copy workflow status and signatures
                - query (str): Optional filtering query
            revision: The revision ID
            
        Returns:
            Response object (201 Created)
        """
        params = {}
        if revision is not None:
            params['revision'] = revision
            
        return self._post(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/branch',
            json=branch_data,
            params=params if params else None
        )            
    
    def post_copy_document(self,
                     project_id: str,
                     space_id: str,
                     document_name: str,
                     copy_data: Dict[str, Any],
                     revision: Optional[str] = None) -> requests.Response:
        """
        Creates a copy of the Document.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            copy_data: Copy Document parameters. Example structure:
                {
                    "targetProjectId": "MyProjectId",
                    "targetSpaceId": "MySpaceId",
                    "targetDocumentName": "MyDocumentId",
                    "removeOutgoingLinks": True,
                    "linkOriginalItemsWithRole": "duplicates"
                }
                Fields (all optional):
                - targetProjectId (str): Project where new document will be created
                - targetSpaceId (str): Space where new document will be created
                - targetDocumentName (str): Name for new Document
                - removeOutgoingLinks (bool): Should outgoing links be removed?
                - linkOriginalItemsWithRole (str): Link a copy of the document to the original
            revision: The revision ID
            
        Returns:
            Response object (201 Created)
        """
        params = {}
        if revision is not None:
            params['revision'] = revision
            
        return self._post(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/copy',
            json=copy_data,
            params=params if params else None
        )
    
    def post_documents(self,
                      project_id: str,
                      space_id: str,
                      documents_data: Dict[str, Any]) -> requests.Response:
        """
        Creates a list of Documents.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            documents_data: The Document body. Example structure:
                {
                    "data": [
                        {
                            "type": "documents",
                            "attributes": {
                                "autoSuspect": True,
                                "homePageContent": {
                                    "type": "text/html",
                                    "value": "My text value"
                                },
                                "moduleName": "MyDocumentId",
                                "outlineNumbering": {
                                    "prefix": "ABC"
                                },
                                "renderingLayouts": [
                                    {
                                        "type": "task",
                                        "label": "My label",
                                        "layouter": "paragraph",
                                        "properties": [
                                            {
                                                "key": "fieldsAtStart",
                                                "value": "id"
                                            }
                                        ]
                                    }
                                ],
                                "status": "draft",
                                "structureLinkRole": "relates_to",
                                "title": "Title",
                                "type": "req_specification",
                                "usesOutlineNumbering": True
                            }
                        }
                    ]
                }
            
        Returns:
            Response object (201 Created)
        """
        return self._post(
            f'projects/{project_id}/spaces/{space_id}/documents',
            json=documents_data
        )
        
    def post_merge_document_from_master(self,
                                  project_id: str,
                                  space_id: str,
                                  document_name: str,
                                  merge_data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Merges Master Work Item changes to the specified Branched Document.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Branch Document Name
            merge_data: Merge Document parameters. Example structure:
                {
                    "createBaseline": True,
                    "userFilter": "status:open"
                }
                Fields (all optional):
                - createBaseline (bool): Specifies whether the Baseline should be created
                - userFilter (str): Specifies the query to filter the source Work Items for the merge
            
        Returns:
            Response object (202 Accepted)
        """
        return self._post(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/mergeFromMaster',
            json=merge_data if merge_data else {}
        )
    
    def post_merge_document_to_master(self,
                                project_id: str,
                                space_id: str,
                                document_name: str,
                                merge_data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Merges Work Item changes from specified Branched Document to Master.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Branch Document Name
            merge_data: Merge Document parameters. Example structure:
                {
                    "createBaseline": True,
                    "userFilter": "status:open"
                }
                Fields (all optional):
                - createBaseline (bool): Specifies whether the Baseline should be created
                - userFilter (str): Specifies the query to filter the source Work Items for the merge
            
        Returns:
            Response object (202 Accepted)
        """
        return self._post(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/mergeToMaster',
            json=merge_data if merge_data else {}
        )
    
    def post_branch_documents(self,
                        branch_data: Dict[str, Any]) -> requests.Response:
        """
        Creates branches of multiple Documents.
        
        Args:
            branch_data: Branch Documents parameters (REQUIRED). Example structure:
                {
                    "documentConfigurations": [
                        {
                            "sourceDocument": "MyProjectId/MySpaceId/MyDocumentId",
                            "sourceRevision": "1234",
                            "targetProjectId": "MyProjectId",
                            "targetSpaceId": "MySpaceId",
                            "targetDocumentName": "MyDocumentId",
                            "copyWorkflowStatusAndSignatures": False,
                            "query": "status:open",
                            "targetDocumentTitle": "My Document Title",
                            "updateTitleHeading": False,
                            "overwriteWorkItems": False,
                            "initializedFields": ["severity"]
                        }
                    ]
                }
                Fields:
                - documentConfigurations (array, REQUIRED): List of document configurations, minimum 1 item
                  Each configuration object:
                  - sourceDocument (str, REQUIRED): Reference path of the source Document
                  - sourceRevision (str): Revision of the source Document
                  - targetProjectId (str): Project where new document will be created
                  - targetSpaceId (str): Space where new document will be created
                  - targetDocumentName (str): Name for new Document
                  - copyWorkflowStatusAndSignatures (bool): Copy workflow status and signatures
                  - query (str): Optional filtering query
                  - targetDocumentTitle (str): Title for new Document
                  - updateTitleHeading (bool): Set title heading to the new Document's title
                  - overwriteWorkItems (bool): Overwrite Work Items instead of referencing them
                  - initializedFields (array of str): Fields to initialize instead of copying
            
        Returns:
            Response object (202 Accepted - asynchronous operation)
        """
        return self._post(
            'all/documents/actions/branch',
            json=branch_data
        )
