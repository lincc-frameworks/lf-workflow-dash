from datetime import datetime
import pytz
import requests
import sys


class WorkflowData:
    def __init__(self, token, owner, repo, workflow, tz=""):
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

            if tz:
                utc_timestamp = datetime.strptime(self.updated_at, "%Y-%m-%dT%H:%M:%SZ")
                self.updated_at = utc_timestamp.astimezone(tz).strftime("%H:%M %b %d, %Y")

    def __str__(self):
        if self.status_code == 200:
            icon = "⚠"
            if self.conclusion == "success":
                icon = "✓"
            return f"{icon} {self.repo} → {self.workflow}: {self.conclusion} (_completed {self.updated_at}_)"
        else:
            icon = "⚠"
            return f"{icon} {self.repo} → {self.workflow}: bad api call"

    def as_row(self):
        if self.status_code == 200:
            icon = "**⚠**"
            if self.conclusion == "success":
                icon = "✓"
            return f"| {icon} | {self.repo} | {self.workflow} | {self.conclusion} | {self.updated_at} |"
        else:
            icon = "**⚠**"
            return f"| {icon} | {self.repo} | {self.workflow} | bad api call | --- |"


if __name__ == "__main__":
    token = sys.argv[1]

    tz = pytz.timezone("America/New_York")

    file_name = "README.md"
    with open(file_name, "w") as file_out:

        def add_text(line):
            file_out.write(line)
            file_out.write("\n\n")

        def add_workflow(owner, repo, workflow):
            file_out.write(str(WorkflowData(token, owner, repo, workflow)))
            file_out.write("\n\n")

        def add_row(owner, repo, workflow):
            file_out.write(WorkflowData(token, owner, repo, workflow, tz=tz).as_row())
            file_out.write("\n")

        add_text(f"Last Updated: {datetime.now(tz).strftime('%H:%M %b %d, %Y')}")

        file_out.write("| ? | repo | workflow | conclusion | updated at |\n")
        file_out.write("| - | ---- | -------- | ---------- | ---------- |\n")

        add_row("OliviaLynn", "workflow-dash", "always-fails.yml")
        add_row("OliviaLynn", "workflow-dash", "70388660")
        # ^ workflow id for pages-build-deployment -> in the future would like to display name even when given id

        add_row("astronomy-commons", "lsdb", "smoke-test.yml")
        add_row("astronomy-commons", "lsdb", "testing-and-coverage.yml")
        add_row("astronomy-commons", "lsdb", "asv-nightly.yml")
        add_row("astronomy-commons", "lsdb", "build-documentation.yml")

        add_row("astronomy-commons", "hipscat", "smoke-test.yml")
        add_row("astronomy-commons", "hipscat", "testing-and-coverage.yml")
        add_row("astronomy-commons", "hipscat", "asv-nightly.yml")
        add_row("astronomy-commons", "hipscat", "build-documentation.yml")

        add_row("astronomy-commons", "hipscat-import", "smoke-test.yml")
        add_row("astronomy-commons", "hipscat-import", "testing-and-coverage.yml")
        add_row("astronomy-commons", "hipscat-import", "asv-nightly.yml")
        add_row("astronomy-commons", "hipscat-import", "build-documentation.yml")

        add_row("lincc-frameworks", "tape", "build-documentation.yml")
        add_row("lincc-frameworks", "tape", "smoke-test.yml")
        add_row("lincc-frameworks", "tape", "testing-and-coverage.yml")
