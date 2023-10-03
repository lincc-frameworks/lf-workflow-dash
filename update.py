from datetime import datetime
import requests
import sys
import yaml

import pytz


class WorkflowData:
    def __init__(self, token, owner, repo, workflow, tz=""):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.workflow = workflow
        self.icon = '<i class="fa fa-exclamation-triangle">'

        self.workflow_url = f"https://github.com/{owner}/{repo}/actions/workflows/{workflow}"
        print(self.workflow_url)

        # View API details:
        # https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#list-workflow-runs-for-a-workflow
        request_url = (
            f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow}/runs"
        )
        payload = {}
        headers = {"accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"}
        response = requests.request("GET", request_url, headers=headers, data=payload)
        self.status_code = response.status_code

        self.run_time = ""
        if self.status_code == 200:  # success
            last_run = response.json()["workflow_runs"][0]
            self.conclusion = last_run["conclusion"]
            if self.conclusion == "None":  # if the workflow is currently being executed
                last_run = response.json()["workflow_runs"][1]
                self.conclusion = last_run["conclusion"]
            self.created_at = last_run["created_at"]
            self.updated_at = last_run["updated_at"]

            # Get run time
            # Convert the timestamps to datetime objects
            created_time = datetime.fromisoformat(self.created_at.replace("Z", "+00:00"))
            updated_time = datetime.fromisoformat(self.updated_at.replace("Z", "+00:00"))

            # Calculate the time difference
            time_difference = updated_time - created_time

            # Calculate total minutes and seconds
            total_seconds = time_difference.total_seconds()
            total_minutes = total_seconds // 60
            remaining_seconds = total_seconds % 60

            # Create a formatted string for total run time
            self.run_time = f"{int(total_minutes)}m {int(remaining_seconds)}s"

            self.run_url = ""
            if self.conclusion == "success":
                self.icon = '<i class="fa fa-check-circle">'
                self.run_url = last_run["html_url"]
            if tz:
                utc_timestamp = datetime.strptime(self.updated_at, "%Y-%m-%dT%H:%M:%SZ")
                self.updated_at = utc_timestamp.astimezone(tz).strftime("%H:%M %B %d, %Y")
                self.updated_at_time = utc_timestamp.astimezone(tz).strftime("%H:%M")
                self.updated_at_date = utc_timestamp.astimezone(tz).strftime("%B %d, %Y")

    def html_row(self):
        icon_color = 'class="red-icon"'
        tr_class = 'class="alert"'
        if self.status_code == 200 and self.conclusion == "success":
            icon_color = 'class="green-icon"'
            tr_class = ""

        if self.status_code == 200:
            return (
                f"<tr {tr_class}>"
                f"<td {icon_color}>{self.icon}</td>"
                f"<td>{self.repo}</td>"
                f'<td><a href="{self.workflow_url}">{self.workflow}</a></td>'
                f"<td>{self.conclusion}</td>"
                f"<td>{self.updated_at}</td>"
                f"<td>{self.run_time}</td>"
                f"</tr>"
                f"\n"
            )
        else:
            return (
                f"<tr {tr_class}>"
                f"<td {icon_color}>{self.icon}</td>"
                f"<td>{self.repo}</td>"
                f'<td><a href="{self.workflow_url}">{self.workflow}</a></td>'
                f"<td>{self.status_code}</td>"
                f"<td></td>"
                f"<td>{self.run_time}</td>"
                f"</tr>"
                f"\n"
            )


def update_html(token, tz, data_rows):
    file_name = "index.html"

    with open(file_name, "w") as file_out:

        def add_row(owner, repo, workflow):
            file_out.write(WorkflowData(token, owner, repo, workflow, tz=tz).html_row())
            file_out.write("\n")

        # Write preamble
        html_preamble = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <title>LF Workflow Dashboard</title>
                <link rel="icon" type="image/x-icon" href="favicon.png">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                <link rel="stylesheet" href="style.css">
            </head>
            <body>
            <table>
            <tr>
                <th></th>
                <th>Repository</th>
                <th>Workflow</th>
                <th>Conclusion</th>
                <th>Last Run</th>
                <th>Run Time</th>
            </tr>
            """
        file_out.write(html_preamble)

        for row in data_rows:
            file_out.write(WorkflowData(token, *row, tz=tz).html_row())

        # add_row("lincc-frameworks", "asv-formatter", "smoke-test.yml")

        # Write postamble
        file_out.write("</table>")
        file_out.write(
            f"<p>"
            f"Last Updated {datetime.now(tz).strftime('%H:%M %B %d, %Y')}"
            f" | "
            f"<a href='https://github.com/OliviaLynn/workflow-dash'><i class=\"fa fa-github\"></i> lf-workflow-dash</a>"
            f"</p>"
        )
        file_out.write("</body></html>")


def read_yaml_file(file_path):
    """Read data from a YAML file and return a list of tuples.

    Parameters
    ----------
    file_path : str
        Path to the YAML file.

    Returns
    -------
    list of tuple
        List of tuples containing ('owner', 'repo', 'workflow').
    """
    with open(file_path, "r") as yaml_file:
        data = yaml.safe_load(yaml_file)

    result = []
    for item in data:
        owner = item["owner"]
        repo = item["repo"]
        workflows = item["workflows"]
        for workflow in workflows:
            result.append((owner, repo, workflow))

    return result


if __name__ == "__main__":
    token = sys.argv[1]

    tz = pytz.timezone("America/New_York")

    file_path = "tracked_workflows.yaml"
    data_as_tuples = read_yaml_file(file_path)

    update_html(token, tz, data_as_tuples)
