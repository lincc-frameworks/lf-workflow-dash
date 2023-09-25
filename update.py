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

        def add_line(line):
            file_out.write(line)
            file_out.write("\n\n")

        add_line(f"Last Updated (UTC) {datetime.now().strftime('%b %d, %Y %H:%M')}")

        TODO : quick explanation/link to api call used

        add_line("## GAD")
        add_line(str(WorkflowData(token, "OliviaLynn", "gh-action-dash", "main.yml")))
        add_line(str(WorkflowData(token, "OliviaLynn", "gh-action-dash", "always-fails.yml")))
        add_line(
            str(
                WorkflowData(token, "OliviaLynn", "gh-action-dash", "70388660")
            )  # id for pages-build-deployment -> in the future would like to display name in output instead
        )

        add_line("## LSDB")
        add_line(str(WorkflowData(token, "astronomy-commons", "lsdb", "smoke-test.yml")))
        add_line(str(WorkflowData(token, "astronomy-commons", "lsdb", "testing-and-coverage.yml")))
        add_line(str(WorkflowData(token, "astronomy-commons", "lsdb", "asv-nightly.yml")))
        add_line(str(WorkflowData(token, "astronomy-commons", "lsdb", "build-documentation.yml")))

        add_line("## HIPSCAT")
        add_line(str(WorkflowData(token, "astronomy-commons", "hipscat", "asv-nightly.yml")))

        add_line("## TAPE")
        add_line(str(WorkflowData(token, "lincc-frameworks", "tape", "build-documentation.yml")))
        add_line(str(WorkflowData(token, "lincc-frameworks", "tape", "smoke-test.yml")))
        add_line(str(WorkflowData(token, "lincc-frameworks", "tape", "testing-and-coverage.yml")))
