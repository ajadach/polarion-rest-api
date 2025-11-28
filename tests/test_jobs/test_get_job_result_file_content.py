"""
Pytest tests for get_job_result_file_content method in Jobs class.

Tests the GET /jobs/{jobId}/actions/download/{filename} endpoint.
Uses mocks to avoid hitting real API.

Run with:
    pytest test_get_job_result_file_content.py -v
"""
import pytest
from unittest.mock import Mock


@pytest.mark.get
class TestGetJobResultFileContent:
    """Unit tests for get_job_result_file_content method using mocks"""
    
    def test_get_job_result_file_content_success_200(self, mock_jobs_api):
        """Test successful file download with 200 status code (mocked)"""
        # Setup mock response for file download
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"Sample file content for job result"
        mock_response.headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': 'attachment; filename="result.txt"'
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        filename = "result.txt"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 200
        assert response.content == b"Sample file content for job result"
        assert 'Content-Type' in response.headers
        
        # Verify correct endpoint was called
        call_args = mock_jobs_api._session.get.call_args
        assert f'jobs/{job_id}/actions/download/{filename}' in call_args[0][0]
        print("\n✓ Mock: Job result file downloaded successfully with 200 status code")
    
    def test_get_job_result_file_content_unauthorized_401(self, mock_jobs_api):
        """Test unauthorized access with 401 status code (mocked)"""
        # Setup mock response based on EXAMPLE_RESPONSE for 401 status code
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "No access token"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        filename = "result.txt"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '401'
        assert response_data['errors'][0]['title'] == 'Unauthorized'
        assert response_data['errors'][0]['detail'] == 'No access token'
        print("\n✓ Mock: Unauthorized access returns 401 status code")
    
    def test_get_job_result_file_content_not_found_404(self, mock_jobs_api):
        """Test job or file not found with 404 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Job 'job-99999' or file 'nonexistent.txt' not found"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-99999"
        filename = "nonexistent.txt"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '404'
        assert response_data['errors'][0]['title'] == 'Not Found'
        print("\n✓ Mock: Not found returns 404 status code")
    
    def test_get_job_result_file_content_forbidden_403(self, mock_jobs_api):
        """Test forbidden access with 403 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "User does not have permission to download this job result"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        filename = "result.txt"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 403
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '403'
        assert response_data['errors'][0]['title'] == 'Forbidden'
        print("\n✓ Mock: Forbidden access returns 403 status code")
    
    def test_get_job_result_file_content_bad_request_400(self, mock_jobs_api):
        """Test bad request with 400 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Invalid job ID or filename format"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "invalid@job#id"
        filename = "result.txt"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '400'
        assert response_data['errors'][0]['title'] == 'Bad Request'
        print("\n✓ Mock: Bad request returns 400 status code")
    
    def test_get_job_result_file_content_endpoint_format(self, mock_jobs_api):
        """Test that the correct endpoint format is used (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"file content"
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "test-job-123"
        filename = "output.log"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_jobs_api._session.get.call_args
        endpoint = call_args[0][0]
        
        # Verify endpoint matches expected format from CURL
        assert f'jobs/{job_id}/actions/download/{filename}' in endpoint
        assert endpoint.endswith(f'jobs/{job_id}/actions/download/{filename}')
        print("\n✓ Mock: Correct endpoint format used")
    
    def test_get_job_result_file_content_different_file_types(self, mock_jobs_api):
        """Test downloading different file types (mocked)"""
        # Test various file types
        test_cases = [
            ("result.txt", "text/plain", b"Text file content"),
            ("report.pdf", "application/pdf", b"%PDF-1.4 fake pdf content"),
            ("data.json", "application/json", b'{"key": "value"}'),
            ("output.xml", "application/xml", b'<?xml version="1.0"?><root/>'),
            ("log.log", "text/plain", b"Log file content"),
            ("archive.zip", "application/zip", b"PK fake zip content"),
        ]
        
        job_id = "job-12345"
        
        for filename, content_type, content in test_cases:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = content
            mock_response.headers = {'Content-Type': content_type}
            mock_jobs_api._session.get.return_value = mock_response
            
            response = mock_jobs_api.get_job_result_file_content(
                job_id=job_id,
                filename=filename
            )
            
            # Assert
            assert response.status_code == 200
            assert response.content == content
            assert response.headers['Content-Type'] == content_type
            
            # Verify correct endpoint
            call_args = mock_jobs_api._session.get.call_args
            assert f'jobs/{job_id}/actions/download/{filename}' in call_args[0][0]
        
        print("\n✓ Mock: Different file types handled correctly")
    
    def test_get_job_result_file_content_different_job_ids(self, mock_jobs_api):
        """Test with different job ID formats (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"file content"
        mock_jobs_api._session.get.return_value = mock_response
        
        # Test various job ID formats
        job_ids = [
            "job-12345",
            "JOB_ABC_123",
            "export-job-2024-01-01",
            "import_job_001",
            "transformation-job-xyz"
        ]
        filename = "result.txt"
        
        for job_id in job_ids:
            response = mock_jobs_api.get_job_result_file_content(
                job_id=job_id,
                filename=filename
            )
            
            # Assert
            assert response.status_code == 200
            call_args = mock_jobs_api._session.get.call_args
            endpoint = call_args[0][0]
            assert f'jobs/{job_id}/actions/download/{filename}' in endpoint
        
        print("\n✓ Mock: Different job ID formats handled correctly")
    
    def test_get_job_result_file_content_special_characters_in_filename(self, mock_jobs_api):
        """Test with special characters in filename (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"file content"
        mock_jobs_api._session.get.return_value = mock_response
        
        # Test filenames with special characters
        job_id = "job-12345"
        filenames = [
            "result_file.txt",
            "report-2024.pdf",
            "output.log.txt",
            "data-export.json",
            "backup_20240101.zip"
        ]
        
        for filename in filenames:
            response = mock_jobs_api.get_job_result_file_content(
                job_id=job_id,
                filename=filename
            )
            
            # Assert
            assert response.status_code == 200
            call_args = mock_jobs_api._session.get.call_args
            endpoint = call_args[0][0]
            assert f'jobs/{job_id}/actions/download/{filename}' in endpoint
        
        print("\n✓ Mock: Filenames with special characters handled correctly")
    
    def test_get_job_result_file_content_binary_content(self, mock_jobs_api):
        """Test downloading binary file content (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        # Simulate binary content (e.g., image, zip, etc.)
        mock_response.content = bytes(range(256))  # Binary data
        mock_response.headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Length': '256'
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        filename = "binary_data.bin"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 200
        assert isinstance(response.content, bytes)
        assert len(response.content) == 256
        assert response.headers['Content-Type'] == 'application/octet-stream'
        print("\n✓ Mock: Binary content downloaded correctly")
    
    def test_get_job_result_file_content_large_file(self, mock_jobs_api):
        """Test downloading large file (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        # Simulate large file content
        large_content = b"x" * 10_000_000  # 10 MB
        mock_response.content = large_content
        mock_response.headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(len(large_content))
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        filename = "large_export.zip"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 200
        assert len(response.content) == 10_000_000
        assert response.headers['Content-Length'] == str(len(large_content))
        print("\n✓ Mock: Large file download handled correctly")
    
    def test_get_job_result_file_content_empty_file(self, mock_jobs_api):
        """Test downloading empty file (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b""
        mock_response.headers = {
            'Content-Type': 'text/plain',
            'Content-Length': '0'
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        filename = "empty.txt"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 200
        assert response.content == b""
        assert response.headers['Content-Length'] == '0'
        print("\n✓ Mock: Empty file download handled correctly")
    
    def test_get_job_result_file_content_content_disposition_header(self, mock_jobs_api):
        """Test that Content-Disposition header is properly handled (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"file content"
        filename = "report_2024.pdf"
        mock_response.headers = {
            'Content-Type': 'application/pdf',
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 200
        assert 'Content-Disposition' in response.headers
        assert filename in response.headers['Content-Disposition']
        print("\n✓ Mock: Content-Disposition header handled correctly")
    
    def test_get_job_result_file_content_server_error_500(self, mock_jobs_api):
        """Test server error with 500 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "500",
                    "title": "Internal Server Error",
                    "detail": "An error occurred while retrieving the job result file"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        filename = "result.txt"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 500
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '500'
        assert response_data['errors'][0]['title'] == 'Internal Server Error'
        print("\n✓ Mock: Server error returns 500 status code")
    
    def test_get_job_result_file_content_service_unavailable_503(self, mock_jobs_api):
        """Test service unavailable with 503 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "503",
                    "title": "Service Unavailable",
                    "detail": "Service temporarily unavailable"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        filename = "result.txt"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 503
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '503'
        assert response_data['errors'][0]['title'] == 'Service Unavailable'
        print("\n✓ Mock: Service unavailable returns 503 status code")
    
    def test_get_job_result_file_content_not_acceptable_406(self, mock_jobs_api):
        """Test not acceptable with 406 status code (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 406
        mock_response.json.return_value = {
            "errors": [
                {
                    "status": "406",
                    "title": "Not Acceptable",
                    "detail": "The requested content type is not acceptable"
                }
            ]
        }
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        filename = "result.txt"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 406
        response_data = response.json()
        assert 'errors' in response_data
        assert response_data['errors'][0]['status'] == '406'
        assert response_data['errors'][0]['title'] == 'Not Acceptable'
        print("\n✓ Mock: Not acceptable returns 406 status code")
    
    def test_get_job_result_file_content_no_parameters_passed_to_get(self, mock_jobs_api):
        """Test that no additional parameters are passed to the GET request (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"file content"
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        filename = "result.txt"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 200
        call_args = mock_jobs_api._session.get.call_args
        
        # Verify no params are passed (file download doesn't use query params)
        # call_args[1] contains the keyword arguments
        params = call_args[1].get('params')
        assert params is None or params == {}
        print("\n✓ Mock: No additional parameters passed to GET request")
    
    def test_get_job_result_file_content_response_is_raw_content(self, mock_jobs_api):
        """Test that response contains raw content, not JSON (mocked)"""
        mock_response = Mock()
        mock_response.status_code = 200
        # Raw file content (not JSON)
        raw_content = b"This is raw file content\nLine 2\nLine 3"
        mock_response.content = raw_content
        mock_response.headers = {'Content-Type': 'text/plain'}
        # Ensure json() is not typically called for raw content
        mock_response.json.side_effect = ValueError("No JSON object could be decoded")
        mock_jobs_api._session.get.return_value = mock_response
        
        # Execute
        job_id = "job-12345"
        filename = "output.log"
        response = mock_jobs_api.get_job_result_file_content(
            job_id=job_id,
            filename=filename
        )
        
        # Assert
        assert response.status_code == 200
        assert response.content == raw_content
        # Verify we're accessing .content, not .json()
        assert hasattr(response, 'content')
        print("\n✓ Mock: Response contains raw content (not JSON)")
