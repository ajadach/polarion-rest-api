"""
Document Attachments module for Polarion REST API.
Handles all Document Attachments related endpoints.
"""
from typing import Optional, Dict, Any
import requests
from .base import PolarionBase


class DocumentAttachments(PolarionBase):
    """
    Class for handling Document Attachments operations in Polarion REST API.
    Provides methods for creating, reading, and updating document attachments.
    
    Methods are organized by HTTP method type (same order as Swagger documentation):
    - GET methods: Retrieve document attachments
    - PATCH methods: Update document attachments
    - POST methods: Create document attachments
    """
    
    # ========== GET methods ==========
    
    def get_document_attachment(self,
                               project_id: str,
                               space_id: str,
                               document_name: str,
                               attachment_id: str,
                               fields: Optional[Dict[str, str]] = None,
                               include: Optional[str] = None,
                               revision: Optional[str] = None) -> requests.Response:
        """
        Returns the specified Document Attachment.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            attachment_id: The Attachment ID
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
            Response object containing the document attachment
        """
        params = self._apply_default_fields(fields)
        
        if include is not None:
            params['include'] = include
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/attachments/{attachment_id}',
            params=params if params else None
        )
    
    def get_document_attachment_content(self,
                                       project_id: str,
                                       space_id: str,
                                       document_name: str,
                                       attachment_id: str,
                                       revision: Optional[str] = None) -> requests.Response:
        """
        Downloads the file content for a specified Document Attachment.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            attachment_id: The Attachment ID
            revision: The revision ID
            
        Returns:
            Response object containing the file content
        """
        params = {}
        if revision is not None:
            params['revision'] = revision
            
        return self._get(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/attachments/{attachment_id}/content',
            params=params if params else None
        )
    
    def get_document_attachments(self,
                                project_id: str,
                                space_id: str,
                                document_name: str,
                                page_size: Optional[int] = None,
                                page_number: Optional[int] = None,
                                fields: Optional[Dict[str, str]] = None,
                                include: Optional[str] = None,
                                revision: Optional[str] = None) -> requests.Response:
        """
        Returns a list of Document Attachments.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
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
            Response object containing list of document attachments
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
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/attachments',
            params=params if params else None
        )
    
    # ========== PATCH methods ==========
    
    def patch_document_attachment(self,
                                 project_id: str,
                                 space_id: str,
                                 document_name: str,
                                 attachment_id: str,
                                 attachment_data: Dict[str, Any],
                                 file_content: Optional[tuple] = None) -> requests.Response:
        """
        Updates the specified Document Attachment.
        
        This method uses multipart/form-data to update attachment metadata and optionally the file content.
        The attachment_data is sent as a 'resource' field in the multipart request.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            attachment_id: The Attachment ID
            attachment_data: Attachment metadata in JSON:API format.
                           Example:
                           {
                               "data": {
                                   "type": "document_attachments",
                                   "id": "MyProjectId/MySpaceId/MyDocumentId/MyAttachmentId",
                                   "attributes": {
                                       "title": "Updated Title"
                                   }
                               }
                           }
            file_content: Optional tuple for file upload in format (filename, file_object, content_type).
                         Example: ('image.png', open('image.png', 'rb'), 'image/png')
                         If None, only metadata will be updated.
            
        Returns:
            Response object (204 No Content on success)
            
        Example:
            # Update only metadata
            data = {
                "data": {
                    "type": "document_attachments",
                    "id": "MyProject/MySpace/MyDoc/MyAttachment",
                    "attributes": {"title": "New Title"}
                }
            }
            response = api.patch_document_attachment(
                project_id="MyProject",
                space_id="MySpace",
                document_name="MyDoc",
                attachment_id="MyAttachment",
                attachment_data=data
            )
            
            # Update metadata and file content
            import json
            with open('new_file.pdf', 'rb') as f:
                response = api.patch_document_attachment(
                    project_id="MyProject",
                    space_id="MySpace",
                    document_name="MyDoc",
                    attachment_id="MyAttachment",
                    attachment_data=data,
                    file_content=('new_file.pdf', f, 'application/pdf')
                )
        """
        import json
        
        # Prepare multipart/form-data
        # The 'resource' field contains JSON metadata
        data = {
            'resource': json.dumps(attachment_data)
        }
        
        # Prepare files dict for multipart request
        files = None
        if file_content is not None:
            # file_content should be tuple: (filename, file_object, content_type)
            files = {'file': file_content}
        
        return self._patch(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/attachments/{attachment_id}',
            data=data,
            files=files
        )
    
    # ========== POST methods ==========
    
    def post_document_attachments(self,
                                 project_id: str,
                                 space_id: str,
                                 document_name: str,
                                 attachments_data: Dict[str, Any],
                                 files: Optional[list] = None) -> requests.Response:
        """
        Creates a list of Document Attachments.
        
        This method uses multipart/form-data to create attachments with metadata and file content.
        Files are identified by order or optionally by the 'lid' attribute in the metadata.
        
        Args:
            project_id: The Project ID
            space_id: The Space ID (Use '_default' for the default Space)
            document_name: The Document name
            attachments_data: Attachment metadata in JSON:API format with array of attachments.
                            Example:
                            {
                                "data": [
                                    {
                                        "type": "document_attachments",
                                        "lid": "attachment1",
                                        "attributes": {
                                            "fileName": "document.pdf",
                                            "title": "My Document"
                                        }
                                    }
                                ]
                            }
            files: Optional list of file tuples in format (filename, file_object, content_type).
                  Files are matched with attachments by order, or by 'lid' if specified.
                  Example: [('doc.pdf', open('doc.pdf', 'rb'), 'application/pdf')]
            
        Returns:
            Response object (201 Created) with created attachments data
            
        Example:
            # Create attachment with metadata and file
            import json
            
            data = {
                "data": [
                    {
                        "type": "document_attachments",
                        "lid": "attachment1",
                        "attributes": {
                            "fileName": "report.pdf",
                            "title": "Monthly Report"
                        }
                    }
                ]
            }
            
            with open('report.pdf', 'rb') as f:
                response = api.post_document_attachments(
                    project_id="MyProject",
                    space_id="MySpace",
                    document_name="MyDocument",
                    attachments_data=data,
                    files=[('report.pdf', f, 'application/pdf')]
                )
        """
        import json
        
        # Prepare multipart/form-data
        # The 'resource' field contains JSON metadata
        data = {
            'resource': json.dumps(attachments_data)
        }
        
        # Prepare files dict for multipart request
        files_dict = None
        if files is not None and len(files) > 0:
            # Create files dict with proper format for requests library
            # Multiple files with same key name will be sent as separate parts
            files_dict = [('files', file_tuple) for file_tuple in files]
        
        return self._post(
            f'projects/{project_id}/spaces/{space_id}/documents/{document_name}/attachments',
            data=data,
            files=files_dict
        )
