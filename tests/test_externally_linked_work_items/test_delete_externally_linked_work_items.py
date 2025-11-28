"""
Pytest tests for delete_externally_linked_work_items method in ExternallyLinkedWorkItems class.

Tests the DELETE /projects/{projectId}/workitems/{workItemId}/externallylinkedworkitems endpoint.
Uses mocks to avoid deleting real data.

Run with:
    pytest test_delete_externally_linked_work_items.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.delete
class TestDeleteExternallyLinkedWorkItems:
    """Unit tests for delete_externally_linked_work_items method using mocks"""
    
    def test_delete_externally_linked_work_items_success(self, mock_externally_linked_work_items_api):
        """Test successful deletion of externally linked work items (mocked)"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Prepare data matching curl example
        external_links_data = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "id": "MyProjectId/MyWorkItemId/parent/hostname/MyProjectId/MyLinkedWorkItemId"
                }
            ]
        }
        
        # Execute
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_items(
            project_id='test_project',
            work_item_id='TEST-123',
            external_links_data=external_links_data
        )
        
        # Assert
        assert response.status_code == 204
        mock_externally_linked_work_items_api._session.delete.assert_called_once()
        
        # Verify correct endpoint was called
        call_args = mock_externally_linked_work_items_api._session.delete.call_args
        assert 'projects/test_project/workitems/TEST-123/externallylinkedworkitems' in call_args[0][0]
        
        # Verify JSON data was sent
        assert call_args[1]['json'] == external_links_data
        print("\n✓ Mock: Externally linked work items deleted successfully (204 No Content)")
    
    def test_delete_externally_linked_work_items_multiple(self, mock_externally_linked_work_items_api):
        """Test deletion of multiple externally linked work items (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Multiple links
        external_links_data = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "id": "Project1/WI1/parent/host1/Project2/WI2"
                },
                {
                    "type": "externallylinkedworkitems",
                    "id": "Project1/WI1/relates/host2/Project3/WI3"
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_items(
            project_id='Project1',
            work_item_id='WI1',
            external_links_data=external_links_data
        )
        
        assert response.status_code == 204
        call_args = mock_externally_linked_work_items_api._session.delete.call_args
        assert len(call_args[1]['json']['data']) == 2
        print("\n✓ Mock: Multiple externally linked work items deleted successfully")
    
    def test_delete_externally_linked_work_items_not_found(self, mock_externally_linked_work_items_api):
        """Test deletion of non-existent externally linked work items (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Externally linked work item not found"
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        external_links_data = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "id": "Project/WI/parent/host/Project/NonExistent"
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_items(
            project_id='Project',
            work_item_id='WI',
            external_links_data=external_links_data
        )
        
        assert response.status_code == 404
        print("\n✓ Mock: Non-existent externally linked work item returns 404")
    
    def test_delete_externally_linked_work_items_work_item_not_found(self, mock_externally_linked_work_items_api):
        """Test deletion when work item doesn't exist (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Work Item not found"
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        external_links_data = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "id": "Project/NonExistent/parent/host/Project/WI"
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_items(
            project_id='Project',
            work_item_id='NonExistent',
            external_links_data=external_links_data
        )
        
        assert response.status_code == 404
        print("\n✓ Mock: Non-existent work item returns 404")
    
    def test_delete_externally_linked_work_items_bad_request(self, mock_externally_linked_work_items_api):
        """Test deletion with invalid data format (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request: Invalid data format"
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Invalid data structure
        external_links_data = {
            "data": [
                {
                    "type": "wrong_type",
                    "id": "invalid_id_format"
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_items(
            project_id='Project',
            work_item_id='WI',
            external_links_data=external_links_data
        )
        
        assert response.status_code == 400
        print("\n✓ Mock: Invalid data format returns 400")
    
    def test_delete_externally_linked_work_items_unauthorized(self, mock_externally_linked_work_items_api):
        """Test deletion without proper authorization (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        external_links_data = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "id": "Project/WI/parent/host/Project/LinkedWI"
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_items(
            project_id='Project',
            work_item_id='WI',
            external_links_data=external_links_data
        )
        
        assert response.status_code == 401
        print("\n✓ Mock: Unauthorized access returns 401")
    
    def test_delete_externally_linked_work_items_forbidden(self, mock_externally_linked_work_items_api):
        """Test deletion without sufficient permissions (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        external_links_data = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "id": "Project/WI/parent/host/Project/LinkedWI"
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_items(
            project_id='Project',
            work_item_id='WI',
            external_links_data=external_links_data
        )
        
        assert response.status_code == 403
        print("\n✓ Mock: Insufficient permissions return 403")
    
    def test_delete_externally_linked_work_items_with_different_roles(self, mock_externally_linked_work_items_api):
        """Test deletion with different link roles (parent, relates, etc.)"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        roles = ['parent', 'child', 'relates', 'duplicates', 'blocks']
        
        for role in roles:
            external_links_data = {
                "data": [
                    {
                        "type": "externallylinkedworkitems",
                        "id": f"Project/WI/{role}/hostname/TargetProject/LinkedWI"
                    }
                ]
            }
            
            response = mock_externally_linked_work_items_api.delete_externally_linked_work_items(
                project_id='Project',
                work_item_id='WI',
                external_links_data=external_links_data
            )
            
            assert response.status_code == 204
            call_args = mock_externally_linked_work_items_api._session.delete.call_args
            assert role in call_args[1]['json']['data'][0]['id']
        
        print(f"\n✓ Mock: Tested {len(roles)} different link roles")
    
    def test_delete_externally_linked_work_items_empty_data(self, mock_externally_linked_work_items_api):
        """Test deletion with empty data array"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request: Empty data array"
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        external_links_data = {
            "data": []
        }
        
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_items(
            project_id='Project',
            work_item_id='WI',
            external_links_data=external_links_data
        )
        
        assert response.status_code == 400
        print("\n✓ Mock: Empty data array returns 400")
    
    def test_delete_externally_linked_work_items_endpoint_structure(self, mock_externally_linked_work_items_api):
        """Test that the endpoint structure is correct"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        external_links_data = {
            "data": [
                {
                    "type": "externallylinkedworkitems",
                    "id": "MyProject/WI-001/parent/external.host.com/ExternalProject/EXT-123"
                }
            ]
        }
        
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_items(
            project_id='MyProject',
            work_item_id='WI-001',
            external_links_data=external_links_data
        )
        
        # Verify endpoint structure
        call_args = mock_externally_linked_work_items_api._session.delete.call_args
        endpoint = call_args[0][0]
        
        assert 'projects/MyProject' in endpoint
        assert 'workitems/WI-001' in endpoint
        assert 'externallylinkedworkitems' in endpoint
        assert endpoint.endswith('externallylinkedworkitems')
        
        print("\n✓ Mock: Endpoint structure is correct")
