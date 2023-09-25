from datetime import datetime
import requests
import sys


class WorkflowData:
    def __init__(self, token, owner, repo, workflow):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.workflow = workflow

        # View API details:
        # https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#list-workflow-runs-for-a-workflow
        url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow}/runs"
        payload = {}
        headers = {"accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"}
        response = requests.request("GET", url, headers=headers, data=payload)
        self.status_code = response.status_code

        if self.status_code == 200:  # success
            last_run = response.json()["workflow_runs"][0]
            self.conclusion = last_run["conclusion"]
            self.updated_at = last_run["updated_at"]

    def __str__(self):
        if self.status_code == 200:
            icon = "⚠"
            if self.conclusion == "success":
                icon = "✓"
            return f"{icon} {self.repo} → {self.workflow}: {self.conclusion} ({self.updated_at})"
        else:
            return f"{icon} {self.repo} → {self.workflow}: bad api call"


if __name__ == "__main__":
    token = sys.argv[1]

    file_name = "README.md"
    with open(file_name, "w") as file_out:

        def add_text(line):
            file_out.write(line)
            file_out.write("\n\n")

        def add_workflow(owner, repo, workflow):
            file_out.write(str(WorkflowData(token, owner, repo, workflow)))
            file_out.write("\n\n")

        add_text(f"Last Updated (UTC) {datetime.now().strftime('%b %d, %Y %H:%M')}")
        add_text(
            "API reference: [list-workflow-runs-for-a-workflow](https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#list-workflow-runs-for-a-workflow)"
        )
        add_text("repo_name → workflow_name: workflow_conclusion (last_run_at)")

        add_text("## WD")
        add_workflow("OliviaLynn", "workflow-dash", "always-fails.yml")
        add_workflow(
            "OliviaLynn", "workflow-dash", "70388660"
        )  # id for pages-build-deployment -> in the future would like to display name in output instead

        add_text("## LSDB")
        add_workflow("astronomy-commons", "lsdb", "smoke-test.yml")
        add_workflow("astronomy-commons", "lsdb", "testing-and-coverage.yml")
        add_workflow("astronomy-commons", "lsdb", "asv-nightly.yml")
        add_workflow("astronomy-commons", "lsdb", "build-documentation.yml")

        add_text("## HIPSCAT")
        add_workflow("astronomy-commons", "hipscat", "smoke-test.yml")
        add_workflow("astronomy-commons", "hipscat", "testing-and-coverage.yml")
        add_workflow("astronomy-commons", "hipscat", "asv-nightly.yml")
        add_workflow("astronomy-commons", "hipscat", "build-documentation.yml")
        
        add_text("## HIPSCAT-IMPORT")
        add_workflow("astronomy-commons", "hipscat-import", "smoke-test.yml")
        add_workflow("astronomy-commons", "hipscat-import", "testing-and-coverage.yml")
        add_workflow("astronomy-commons", "hipscat-import", "asv-nightly.yml")
        add_workflow("astronomy-commons", "hipscat-import", "build-documentation.yml")

        add_text("## TAPE")
        add_workflow("lincc-frameworks", "tape", "build-documentation.yml")
        add_workflow("lincc-frameworks", "tape", "smoke-test.yml")
        add_workflow("lincc-frameworks", "tape", "testing-and-coverage.yml")
