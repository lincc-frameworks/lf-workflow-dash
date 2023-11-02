import requests


def update_workflow_status(workflow_elem, token):
    if workflow_elem is None:
        return

    # Make request
    request_url = f"{workflow_elem.workflow_url}/runs"
    payload = {}
    headers = {
        "accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
    }
    response = requests.request("GET", request_url, headers=headers, data=payload)
    status_code = response.status_code
    conclusion = "pending"

    # Process data
    if status_code == 200:  # API was successful
        if len(response.json()["workflow_runs"]) == 0:  # workflow has no runs
            conclusion = "not yet run"
        else:
            last_run = response.json()["workflow_runs"][0]

            # Get the workflow conclusion ("success", "failure", etc)
            conclusion = last_run["conclusion"]

            # Check if the workflow is currently being executed
            if conclusion is None:
                # try next most recent
                if len(response.json()["workflow_runs"]) > 1:
                    last_run = response.json()["workflow_runs"][1]
                    conclusion = last_run["conclusion"]
                else:
                    conclusion = "pending"
    else:
        conclusion = status_code

