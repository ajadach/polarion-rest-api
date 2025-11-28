"""
Pytest tests for delete_externally_linked_work_item method in ExternallyLinkedWorkItems class.

Tests the DELETE /projects/{projectId}/workitems/{workItemId}/externallylinkedworkitems/{roleId}/{hostname}/{targetProjectId}/{linkedWorkItemId} endpoint.
Uses mocks to avoid deleting real data.

Run with:
    pytest test_delete_externally_linked_work_item.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.delete
class TestDeleteExternallyLinkedWorkItem:
    """Unit tests for delete_externally_linked_work_item method using mocks"""
    
    def test_delete_externally_linked_work_item_success(self, mock_externally_linked_work_items_api):
        """Test successful deletion of externally linked work item (mocked)"""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 204
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_item(
            project_id='MyProject',
            work_item_id='WI-001',
            role_id='parent',
            hostname='external-server.com',
            target_project_id='ExternalProject',
            linked_work_item_id='EXT-WI-123'
        )
        
        # Assert
        assert response.status_code == 204
        mock_externally_linked_work_items_api._session.delete.assert_called_once()
        
        # Verify correct endpoint was called
        call_args = mock_externally_linked_work_items_api._session.delete.call_args
        endpoint = call_args[0][0]
        assert 'projects/MyProject/workitems/WI-001/externallylinkedworkitems/' in endpoint
        assert 'parent/external-server.com/ExternalProject/EXT-WI-123' in endpoint
        print("\n✓ Mock: Externally linked work item deleted successfully (204 No Content)")
    
    def test_delete_externally_linked_work_item_not_found(self, mock_externally_linked_work_items_api):
        """Test deleting non-existent externally linked work item (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Externally linked work item not found"
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_item(
            project_id='MyProject',
            work_item_id='WI-001',
            role_id='parent',
            hostname='external-server.com',
            target_project_id='ExternalProject',
            linked_work_item_id='NONEXISTENT'
        )
        
        # Assert
        assert response.status_code == 404
        print("\n✓ Mock: Non-existent externally linked work item returns 404")
    
    def test_delete_externally_linked_work_item_work_item_not_found(self, mock_externally_linked_work_items_api):
        """Test deletion when source work item doesn't exist (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Work item not found"
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_item(
            project_id='MyProject',
            work_item_id='NONEXISTENT-WI',
            role_id='parent',
            hostname='external-server.com',
            target_project_id='ExternalProject',
            linked_work_item_id='EXT-WI-123'
        )
        
        # Assert
        assert response.status_code == 404
        print("\n✓ Mock: Non-existent work item returns 404")
    
    def test_delete_externally_linked_work_item_different_roles(self, mock_externally_linked_work_items_api):
        """Test deletion with different link role types"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Common roles in work item linking
        roles = ['parent', 'child', 'relates', 'duplicates', 'blocks', 'depends_on']
        
        for role in roles:
            response = mock_externally_linked_work_items_api.delete_externally_linked_work_item(
                project_id='MyProject',
                work_item_id='WI-001',
                role_id=role,
                hostname='external-server.com',
                target_project_id='ExternalProject',
                linked_work_item_id='EXT-WI-123'
            )
            
            assert response.status_code == 204
            call_args = mock_externally_linked_work_items_api._session.delete.call_args
            assert f'{role}/external-server.com/ExternalProject/EXT-WI-123' in call_args[0][0]
        
        print(f"\n✓ Mock: Tested {len(roles)} different role types")
    
    def test_delete_externally_linked_work_item_unauthorized(self, mock_externally_linked_work_items_api):
        """Test deletion without proper authorization (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_item(
            project_id='MyProject',
            work_item_id='WI-001',
            role_id='parent',
            hostname='external-server.com',
            target_project_id='ExternalProject',
            linked_work_item_id='EXT-WI-123'
        )
        
        # Assert
        assert response.status_code == 401
        print("\n✓ Mock: Unauthorized access returns 401")
    
    def test_delete_externally_linked_work_item_forbidden(self, mock_externally_linked_work_items_api):
        """Test deletion without sufficient permissions (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_item(
            project_id='MyProject',
            work_item_id='WI-001',
            role_id='parent',
            hostname='external-server.com',
            target_project_id='ExternalProject',
            linked_work_item_id='EXT-WI-123'
        )
        
        # Assert
        assert response.status_code == 403
        print("\n✓ Mock: Insufficient permissions return 403")
    
    def test_delete_externally_linked_work_item_different_hostnames(self, mock_externally_linked_work_items_api):
        """Test deletion with different external hostnames"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        hostnames = ['jira.company.com', 'github.com', 'gitlab.com', 'external-polarion.com']
        
        for hostname in hostnames:
            response = mock_externally_linked_work_items_api.delete_externally_linked_work_item(
                project_id='MyProject',
                work_item_id='WI-001',
                role_id='relates',
                hostname=hostname,
                target_project_id='ExternalProject',
                linked_work_item_id='EXT-WI-123'
            )
            
            assert response.status_code == 204
            call_args = mock_externally_linked_work_items_api._session.delete.call_args
            assert f'relates/{hostname}/ExternalProject/EXT-WI-123' in call_args[0][0]
        
        print(f"\n✓ Mock: Tested {len(hostnames)} different hostnames")
    
    def test_delete_externally_linked_work_item_with_special_characters(self, mock_externally_linked_work_items_api):
        """Test deletion with special characters in IDs"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute with special characters (will be URL encoded by requests library)
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_item(
            project_id='My-Project',
            work_item_id='WI-001',
            role_id='parent',
            hostname='external.server.com',
            target_project_id='External-Project',
            linked_work_item_id='EXT-WI-123'
        )
        
        # Assert
        assert response.status_code == 204
        call_args = mock_externally_linked_work_items_api._session.delete.call_args
        assert 'My-Project' in call_args[0][0]
        assert 'External-Project' in call_args[0][0]
        print("\n✓ Mock: Special characters in IDs handled correctly")
    
    def test_delete_externally_linked_work_item_project_not_found(self, mock_externally_linked_work_items_api):
        """Test deletion when project doesn't exist (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Project not found"
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_item(
            project_id='NonExistentProject',
            work_item_id='WI-001',
            role_id='parent',
            hostname='external-server.com',
            target_project_id='ExternalProject',
            linked_work_item_id='EXT-WI-123'
        )
        
        # Assert
        assert response.status_code == 404
        print("\n✓ Mock: Non-existent project returns 404")
    
    def test_delete_externally_linked_work_item_complete_path_validation(self, mock_externally_linked_work_items_api):
        """Test that complete path is correctly constructed"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_externally_linked_work_items_api._session.delete.return_value = mock_response
        
        # Execute
        response = mock_externally_linked_work_items_api.delete_externally_linked_work_item(
            project_id='TestProject',
            work_item_id='TEST-123',
            role_id='depends_on',
            hostname='jira.example.com',
            target_project_id='TargetProj',
            linked_work_item_id='JIRA-456'
        )
        
        # Assert
        assert response.status_code == 204
        call_args = mock_externally_linked_work_items_api._session.delete.call_args
        endpoint = call_args[0][0]
        
        # Verify all components are in correct order
        assert 'projects/TestProject/workitems/TEST-123/externallylinkedworkitems/' in endpoint
        assert 'depends_on/jira.example.com/TargetProj/JIRA-456' in endpoint
        print("\n✓ Mock: Complete path constructed correctly with all 6 parameters")
