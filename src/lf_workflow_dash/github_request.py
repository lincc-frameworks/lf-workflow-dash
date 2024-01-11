from datetime import datetime

import pytz
import requests


def get_conclusion_time(last_run):
    """Get the workflow conclusion time and set the proper timezone

    Args:
        last_run (dict): the most recent run of the workflow
    """
    timestamp_str = last_run["updated_at"]

    # Parse the timestamp
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")

    # Define the time zones for UTC and New York
    utc_timezone = pytz.timezone("UTC")
    ny_timezone = pytz.timezone("America/New_York")

    # Convert the timestamp to New York time
    timestamp_ny = timestamp.replace(tzinfo=utc_timezone).astimezone(ny_timezone)

    # Format the timestamp
    formatted_timestamp = timestamp_ny.strftime("%H:%M<br>%m/%d/%y")

    # Figure out how old this conclusion time is. If it's more than 2 weeks, it's stale.
    current_date = datetime.now()
    date_diff = current_date - timestamp
    is_stale = date_diff.days > 14

    return (formatted_timestamp, is_stale)


def update_workflow_status(workflow_elem, token):
    """Determine the status of a workflow run, using the github API.

    Args:
        workflow_elem (WorkflowElemData): the workflow to request
        token (str): auth token for hitting the github API
    """
    if workflow_elem is None:
        return

    print("  ", workflow_elem.workflow_name)
    # Make request
    request_url = (
        f"https://api.github.com/repos/{workflow_elem.owner}/{workflow_elem.repo}"
        f"/actions/workflows/{workflow_elem.workflow_name}/runs"
    )
    payload = {}
    headers = {
        "accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
    }
    response = requests.request("GET", request_url, headers=headers, data=payload, timeout=15)
    status_code = response.status_code
    conclusion = "pending"
    conclusion_time = ""
    is_stale = False

    # Process data
    if status_code == 200:  # API was successful
        response_json = response.json()
        if len(response_json["workflow_runs"]) == 0:  # workflow has no runs
            conclusion = "not yet run"

        else:
            last_run = response_json["workflow_runs"][0]

            # Get the workflow conclusion ("success", "failure", etc)
            conclusion = last_run["conclusion"]

            # Get the time this workflow concluded (in New York time)
            (conclusion_time, is_stale) = get_conclusion_time(last_run)

            # Check if the workflow is currently being executed
            if conclusion is None:
                # try next most recent
                if len(response_json["workflow_runs"]) > 1:
                    last_run = response_json["workflow_runs"][1]
                    conclusion = last_run["conclusion"]
                    (conclusion_time, is_stale) = get_conclusion_time(last_run)
                else:
                    conclusion = "pending"
                    conclusion_time = ""

    else:
        print("    ", status_code)
        conclusion = status_code

    workflow_elem.set_status(conclusion, conclusion_time, is_stale)
