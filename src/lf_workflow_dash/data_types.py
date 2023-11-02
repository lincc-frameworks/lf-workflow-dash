from dataclasses import dataclass, field
from typing import List

import yaml


@dataclass
class WorkflowElemData:
    """Per-workflow information"""

    workflow_name: str = ""
    workflow_url: str = ""
    workflow_status: str = ""
    display_class: str = ""
    last_run_url: str = ""

    def __init__(self, workflow_name, repo_url):
        self.workflow_name = workflow_name
        self.workflow_url = f"{repo_url}/actions/workflows/{self.workflow_name}"
        self.workflow_status = "pending"
        self.display_class = "yellow-cell"

        ## silly temporary data
        if "doc" in self.workflow_name:
            self.workflow_status = "FAILED"
            self.display_class = "red-cell"
        elif "smoke" in self.workflow_name:
            self.workflow_status = "success"
            self.display_class = ""

    def set_status(self, status):
        self.workflow_status = status
        if status == "success":
            self.display_class = ""
        elif status == "failure":
            self.display_class = "red-cell"


@dataclass
class ProjectData:
    """Per-repo project workflow data"""

    owner: str = ""
    repo: str = ""
    icon: str = ""
    repo_url: str = ""

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

    page_title = data.get(
        "page_title", None
    )  # Get the page_title if it exists, otherwise set it to None

    repos = data.get("repos", [])
    all_projects = []
    for item in repos:
        owner = item["owner"]
        repo = item["repo"]
        project_data = ProjectData(owner=owner, repo=repo)

        if "smoke-test" in item:
            project_data.smoke_test = WorkflowElemData(
                item["smoke-test"], repo_url=project_data.repo_url
            )
        if "build-docs" in item:
            project_data.build_docs = WorkflowElemData(
                item["build-docs"], repo_url=project_data.repo_url
            )
        if "benchmarks" in item:
            project_data.benchmarks = WorkflowElemData(
                item["benchmarks"], repo_url=project_data.repo_url
            )
        if "live-build" in item:
            project_data.live_build = WorkflowElemData(
                item["live-build"], repo_url=project_data.repo_url
            )

        all_projects.append(project_data)

    return {
        "page_title": page_title,
        "all_projects": all_projects,
        "dash_name": "LINCC Frameworks Builds",
        "dash_repo": "lf-workflow-dash",
        "last_updated": "just now!",
    }
