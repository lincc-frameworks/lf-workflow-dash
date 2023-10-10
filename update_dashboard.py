from datetime import datetime
import requests
import sys
import yaml

import pytz


class WorkflowData:
    def __init__(self, token, owner, repo, workflow, timezone=""):
        self.owner = owner
        self.repo = repo
        self.workflow = workflow
        self.icon = ""
        self.workflow_url = ""
        self.conclusion = ""
        self.created_at = ""
        self.updated_at = ""
        self.run_time = ""
        self.run_url = ""

        self.get_data(token, timezone)

    def get_data(self, token, timezone):
        self.workflow_url = (
            f"https://github.com/{self.owner}/{self.repo}/actions/workflows/{self.workflow}"
        )
        print(self.workflow_url)

        # Make request
        request_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/actions/workflows/{self.workflow}/runs"
        payload = {}
        headers = {"accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"}
        response = requests.request("GET", request_url, headers=headers, data=payload)
        self.status_code = response.status_code

        # Process data
        if self.status_code == 200:  # API was successful
            if len(response.json()["workflow_runs"]) == 0:  # workflow has no runs
                self.conclusion = "not yet run"
            else:
                last_run = response.json()["workflow_runs"][0]

                # Get the workflow conclusion ("success", "failure", etc)
                self.conclusion = last_run["conclusion"]

                # Check if the workflow is currently being executed
                if (
                    self.conclusion == None
                ):  # maybe should change to last_run["status"] != "completed"?
                    if len(response.json()["workflow_runs"]) > 1:  # get next most recent
                        last_run = response.json()["workflow_runs"][1]
                        self.conclusion = last_run["conclusion"]
                    else:
                        # TODO update data to say in progress, then skip out
                        self.conclusion = "in progress"

                # Calculate how long it took to run this workflow
                self.run_time = self.get_run_time(last_run)

                # Determine the status icon at the left of the row
                if self.conclusion == "success":
                    self.icon = '<i class="fa fa-check-circle">'
                else:
                    self.icon = '<i class="fa fa-exclamation-triangle">'

                # Get the url to the log of the last run workflow
                self.run_url = last_run["html_url"]

                # If we've specified a timezone, calculate it
                if timezone:
                    utc_timestamp = datetime.strptime(self.updated_at, "%Y-%m-%dT%H:%M:%SZ")
                    self.updated_at = utc_timestamp.astimezone(timezone).strftime("%H:%M %B %d, %Y")
                    self.updated_at_time = utc_timestamp.astimezone(timezone).strftime("%H:%M")
                    self.updated_at_date = utc_timestamp.astimezone(timezone).strftime("%B %d, %Y")
        else:
            self.conclusion = self.status_code

    def get_run_time(self, last_run):
        self.created_at = last_run["created_at"]
        self.updated_at = last_run["updated_at"]

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
        return f"{int(total_minutes)}m {int(remaining_seconds)}s"

    def html_row(self):
        if self.conclusion == "success":
            return (
                f"<tr>"
                f'<td class="green-icon">{self.icon}</td>'
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
                f'<tr class="alert">'
                f'<td class="red-icon">{self.icon}</td>'
                f"<td>{self.repo}</td>"
                f'<td><a href="{self.workflow_url}">{self.workflow}</a></td>'
                f"<td>{self.conclusion}</td>"
                f"<td>{self.updated_at}</td>"
                f"<td>{self.run_time}</td>"
                f"</tr>"
                f"\n"
            )


def update_html(out_file_name, token, timezone, page_title, data_rows):
    with open(out_file_name, "w") as file_out:
        # Write preamble
        html_preamble = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <title>{page_title}</title>
                <link rel="icon" type="image/x-icon" href="img/favicon.png">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                <link rel="stylesheet" href="css/styles.css">
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

        # Write the data
        for row in data_rows:
            file_out.write(WorkflowData(token, *row, timezone=timezone).html_row())

        # Write postamble
        html_postamble = (
            f"</table>"
            f"<p>"
            f"Last Updated {datetime.now(timezone).strftime('%H:%M %B %d, %Y')}"
            f" | "
            f"<a href='https://github.com/lincc-frameworks/lf-workflow-dash'><i class=\"fa fa-github\"></i> lf-workflow-dash</a>"
            f"</p>"
            f"</body>"
            f"</html>"
        )
        file_out.write(html_postamble)


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
    with open(file_path, "r") as yaml_file:
        data = yaml.safe_load(yaml_file)

    page_title = data.get(
        "page_title", None
    )  # Get the page_title if it exists, otherwise set it to None

    repos = data.get("repos", [])
    result = []
    for item in repos:
        owner = item["owner"]
        repo = item["repo"]
        workflows = item["workflows"]
        for workflow in workflows:
            result.append((owner, repo, workflow))

    return page_title, result


if __name__ == "__main__":
    TOKEN = sys.argv[1]
    DATA_FILE = sys.argv[2]
    OUT_FILE = sys.argv[3]

    TIMEZONE = pytz.timezone("America/New_York")

    (page_title, data) = read_yaml_file(DATA_FILE)
    update_html(OUT_FILE, TOKEN, TIMEZONE, page_title, data)
