"""
Main Polarion REST API class.
This class provides access to all Polarion REST API modules.
"""
from typing import Optional

try:
    # Try relative import (when used as package)
    from .modules.base import PolarionBase
except ImportError:
    # Fall back to absolute import (when used as standalone script)
    import os
    import sys
    current_dir = os.path.dirname(os.path.abspath(__file__))
    modules_dir = os.path.join(current_dir, 'modules')
    if modules_dir not in sys.path:
        sys.path.insert(0, modules_dir)
    from modules.base import PolarionBase


class PolarionRestApi(PolarionBase):
    """
    Main class for Polarion REST API.
    Provides access to all API modules and endpoints.
    
    Available modules:
        - collections: Collections operations
        - document_attachments: Document Attachments operations
        - document_comments: Document Comments operations
        - document_parts: Document Parts operations
        - documents: Documents operations
        - enumerations: Enumerations operations
        - externally_linked_work_items: Externally Linked Work Items operations
        - feature_selections: Feature Selections operations
        - icons: Icons operations
        - jobs: Jobs operations
        - linked_oslc_resources: Linked OSLC Resources operations
        - linked_work_items: Linked Work Items operations
        - page_attachments: Page Attachments operations
        - pages: Pages operations
        - plans: Plans operations
        - project_templates: Project Templates operations
        - projects: Projects operations
        - revisions: Revisions operations
        - roles: Roles operations
        - test_record_attachments: Test Record Attachments operations
        - test_records: Test Records operations
        - test_run_attachments: Test Run Attachments operations
        - test_run_comments: Test Run Comments operations
        - test_runs: Test Runs operations
        - test_step_result_attachments: Test Step Result Attachments operations
        - test_step_results: Test Step Results operations
        - test_steps: Test Steps operations
        - user_groups: User Groups operations
        - users: Users operations
        - work_item_approvals: Work Item Approvals operations
        - work_item_attachments: Work Item Attachments operations
        - work_item_comments: Work Item Comments operations
        - work_item_work_records: Work Item Work Records operations
        - work_items: Work Items operations
    """
    
    def __init__(self, base_url: str = "https://testdrive.polarion.com/polarion/rest/v1",
                 token: Optional[str] = None,
                 debug_request: bool = False):
        """
        Initialize Polarion API client.
        
        Args:
            base_url: Base URL for Polarion REST API
            token: Bearer token for authentication (can be set later using set_token())
            debug_request: Enable debug mode to print request details (default: False)
            
        Example:
            api = PolarionRestApi(token="your_bearer_token", debug_request=True)
            # Access work items module
            work_items = api.work_items.get_work_items("project_id")
            # Access work item comments module
            work_item_comments = api.work_item_comments.get_comments("project_id", "work_item_id")
            # Access work item attachments module
            work_item_attachments = api.work_item_attachments.get_attachments("project_id", "work_item_id")
            # Access work item approvals module
            work_item_approvals = api.work_item_approvals.get_approvals("project_id", "work_item_id")
            # Access work records module
            work_records = api.work_item_work_records.get_work_records("project_id", "work_item_id")
            # Access users module
            users = api.users.get_users()
            # Access user groups module
            user_group = api.user_groups.get_user_group("group_id")
            # Access test steps module
            test_steps = api.test_steps.get_test_steps("project_id", "work_item_id")
            # Access test step results module
            test_step_results = api.test_step_results.get_test_step_results("project_id", "test_run_id", "test_case_project_id", "test_case_id", "iteration")
            # Access test step result attachments module
            attachments = api.test_step_result_attachments.get_test_step_result_attachments("project_id", "test_run_id", "test_case_project_id", "test_case_id", "iteration", "test_step_index")
            # Access test runs module
            test_runs = api.test_runs.get_test_runs("project_id")
            # Access test run comments module
            comments = api.test_run_comments.get_test_run_comments("project_id", "test_run_id")
            # Access test run attachments module
            attachments = api.test_run_attachments.get_test_run_attachments("project_id", "test_run_id")
            # Access test records module
            test_records = api.test_records.get_test_records("project_id", "test_run_id")
            # Access test record attachments module
            record_attachments = api.test_record_attachments.get_test_record_attachments("project_id", "test_run_id", "test_case_project_id", "test_case_id", "0")
            # Access roles module
            role = api.roles.get_role("administrator")
            # Access revisions module
            revisions = api.revisions.get_revisions()
            # Access projects module
            projects = api.projects.get_projects()
            # Access project templates module
            templates = api.project_templates.get_project_templates()
            # Access plans module
            plans = api.plans.get_plans("project_id")
            # Access pages module
            page = api.pages.get_page("project_id", "space_id", "page_name")
            # Access page attachments module
            attachment = api.page_attachments.get_page_attachment("project_id", "space_id", "page_name", "attachment_id")
            # Access linked work items module
            linked = api.linked_work_items.get_linked_work_items("project_id", "work_item_id")
            # Access linked OSLC resources module
            oslc = api.linked_oslc_resources.get_oslc_resources("project_id", "work_item_id")
            # Access jobs module
            job = api.jobs.get_job("job_id")
            # Access icons module
            icons = api.icons.get_global_icons()
            # Access externally linked work items module
            external_links = api.externally_linked_work_items.get_externally_linked_work_items("project_id", "work_item_id")
            # Access feature selections module
            selections = api.feature_selections.get_feature_selections("project_id", "work_item_id")
            # Access enumerations module
            enum = api.enumerations.get_global_enumeration("~", "status", "~")
            # Access documents module
            document = api.documents.get_document("project_id", "space_id", "document_name")
            # Access document parts module
            parts = api.document_parts.get_document_parts("project_id", "space_id", "document_name")
            # Access document comments module
            comments = api.document_comments.get_document_comments("project_id", "space_id", "document_name")
            # Access document attachments module
            attachments = api.document_attachments.get_document_attachments("project_id", "space_id", "document_name")
        """
        super().__init__(base_url, token, debug_request)
        self._load_modules()
    
    def _load_modules(self):
        """
        Dynamically load all module classes from the modules directory.
        This method will automatically discover and initialize all module classes.
        """
        try:
            from .modules.work_items import WorkItems
            self.work_items = WorkItems(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.work_item_comments import WorkItemComments
            self.work_item_comments = WorkItemComments(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.work_item_attachments import WorkItemAttachments
            self.work_item_attachments = WorkItemAttachments(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.work_item_approvals import WorkItemApprovals
            self.work_item_approvals = WorkItemApprovals(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.work_item_work_records import WorkItemWorkRecords
            self.work_item_work_records = WorkItemWorkRecords(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.users import Users
            self.users = Users(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.user_groups import UserGroups
            self.user_groups = UserGroups(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.test_steps import TestSteps
            self.test_steps = TestSteps(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.test_step_results import TestStepResults
            self.test_step_results = TestStepResults(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.test_step_result_attachments import TestStepResultAttachments
            self.test_step_result_attachments = TestStepResultAttachments(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.test_runs import TestRuns
            self.test_runs = TestRuns(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.test_run_comments import TestRunComments
            self.test_run_comments = TestRunComments(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.test_run_attachments import TestRunAttachments
            self.test_run_attachments = TestRunAttachments(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.test_records import TestRecords
            self.test_records = TestRecords(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.test_record_attachments import TestRecordAttachments
            self.test_record_attachments = TestRecordAttachments(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.roles import Roles
            self.roles = Roles(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.revisions import Revisions
            self.revisions = Revisions(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.projects import Projects
            self.projects = Projects(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.project_templates import ProjectTemplates
            self.project_templates = ProjectTemplates(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.plans import Plans
            self.plans = Plans(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.pages import Pages
            self.pages = Pages(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.page_attachments import PageAttachments
            self.page_attachments = PageAttachments(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.linked_work_items import LinkedWorkItems
            self.linked_work_items = LinkedWorkItems(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.linked_oslc_resources import LinkedOslcResources
            self.linked_oslc_resources = LinkedOslcResources(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.jobs import Jobs
            self.jobs = Jobs(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.icons import Icons
            self.icons = Icons(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.externally_linked_work_items import ExternallyLinkedWorkItems
            self.externally_linked_work_items = ExternallyLinkedWorkItems(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.feature_selections import FeatureSelections
            self.feature_selections = FeatureSelections(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.enumerations import Enumerations
            self.enumerations = Enumerations(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.documents import Documents
            self.documents = Documents(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.document_parts import DocumentParts
            self.document_parts = DocumentParts(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.document_comments import DocumentComments
            self.document_comments = DocumentComments(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.document_attachments import DocumentAttachments
            self.document_attachments = DocumentAttachments(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
        
        try:
            from .modules.collections import Collections
            self.collections = Collections(self.base_url, self._token, self.debug_request)
        except ImportError:
            pass
    
    def __enter__(self):
        """
        Context manager entry.
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit - closes the session.
        """
        self.close()
