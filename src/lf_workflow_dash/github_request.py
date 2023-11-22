import requests


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

    # Process data
    if status_code == 200:  # API was successful
        response_json = response.json()
        if len(response_json["workflow_runs"]) == 0:  # workflow has no runs
            conclusion = "not yet run"
        else:
            last_run = response_json["workflow_runs"][0]

            # Get the workflow conclusion ("success", "failure", etc)
            conclusion = last_run["conclusion"]

            # Check if the workflow is currently being executed
            if conclusion is None:
                # try next most recent
                if len(response_json["workflow_runs"]) > 1:
                    last_run = response_json["workflow_runs"][1]
                    conclusion = last_run["conclusion"]
                else:
                    conclusion = "pending"
    else:
        print("    ", status_code)
        conclusion = status_code

    workflow_elem.set_status(conclusion)
