from dataclasses import dataclass, field
from datetime import datetime
from typing import List

import pytz
import yaml


@dataclass
class WorkflowElemData:
    """Per-workflow information"""

    workflow_name: str = ""
    workflow_url: str = ""
    workflow_status: str = ""
    display_class: str = ""
    icon_class: str = ""
    last_run_url: str = ""
    owner: str = ""
    repo: str = ""
    conclusion_time: str = ""
    is_stale: bool = False

    def __init__(self, workflow_name, repo_url, owner, repo):
        self.workflow_name = workflow_name
        self.owner = owner
        self.repo = repo
        self.workflow_url = f"{repo_url}/actions/workflows/{self.workflow_name}"
        self.workflow_status = "pending"
        self.display_class = "yellow-cell"
        self.icon_class = "fa fa-question-circle"

    def set_status(self, status, conclusion_time, is_stale):
        """Set the completion status of a workflow. This will also update the display class
        to suit the warning level.

        Args:
            status (str): how the workflow completed (e.g. "success" or "failure")
            conclusion_time (str): pretty print of the conclusion of the last workflow run
            is_stale (bool): if True, the last workflow run was a long time ago
        """
        self.workflow_status = status
        self.conclusion_time = conclusion_time
        self.is_stale = is_stale
        if status == "success":
            self.display_class = "green-cell"
            self.icon_class = "fa fa-check-circle"
        elif status == "failure":
            self.display_class = "red-cell"
            self.icon_class = "fa fa-times-circle"


@dataclass
class ProjectData:
    """Per-repo project workflow data"""

    owner: str = ""
    repo: str = ""
    icon: str = ""
    repo_url: str = ""
    copier_version: str = ""

    smoke_test: WorkflowElemData = None
    build_docs: WorkflowElemData = None
    benchmarks: WorkflowElemData = None
    live_build: WorkflowElemData = None

    other_workflows: List[WorkflowElemData] = field(default_factory=list)

    def __post_init__(self):
        self.repo_url = f"https://github.com/{self.owner}/{self.repo}"


def read_yaml_file(file_path):
    """Read data from a YAML file and return a tuple with page title and a list of repository tuples.

    Parameters
    ----------
    file_path : str
        Path to the YAML file.

    Returns
    -------
    tuple
        A tuple containing the page title (str) and a list of tuples containing ('owner', 'repo', 'workflow').
    """
    with open(file_path, "r", encoding="utf8") as yaml_file:
        data = yaml.safe_load(yaml_file)

    # Get the page_title if it exists, otherwise set it to None
    page_title = data.get("page_title", None)

    repos = data.get("repos", [])
    all_projects = []
    for item in repos:
        owner = item["owner"]
        repo = item["repo"]
        project_data = ProjectData(owner=owner, repo=repo)

        if "smoke-test" in item:
            project_data.smoke_test = WorkflowElemData(
                item["smoke-test"], repo_url=project_data.repo_url, owner=owner, repo=repo
            )
        if "build-docs" in item:
            project_data.build_docs = WorkflowElemData(
                item["build-docs"], repo_url=project_data.repo_url, owner=owner, repo=repo
            )
        if "benchmarks" in item:
            project_data.benchmarks = WorkflowElemData(
                item["benchmarks"], repo_url=project_data.repo_url, owner=owner, repo=repo
            )
        if "live-build" in item:
            project_data.live_build = WorkflowElemData(
                item["live-build"], repo_url=project_data.repo_url, owner=owner, repo=repo
            )

        all_projects.append(project_data)

    timezone = pytz.timezone("America/New_York")
    last_updated = datetime.now(timezone).strftime("%H:%M %B %d, %Y (US-NYC)")

    return {
        "page_title": page_title,
        "all_projects": all_projects,
        "dash_name": "LINCC Frameworks Builds",
        "dash_repo": "lf-workflow-dash",
        "last_updated": last_updated,
    }
