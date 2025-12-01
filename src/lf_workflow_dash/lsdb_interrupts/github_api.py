import re
from datetime import datetime, timezone
from typing import Dict, List

import human_readable
import requests

GITHUB_API_BASE = "https://api.github.com"
TEAM_MEMBERS = [
    "delucchi-cmu",
    "nevencaplar",
    "hombit",
    "smcguire-cmu",
    "gitosaurus",
    "dougbrn",
    "olivialynn",
    "camposandro",
    "wilsonbb",
    "mjuric",
]


def create_github_session(token) -> requests.Session:
    """Create a requests session with GitHub authentication."""
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }
    )
    return session


def paginate_github_api(session: requests.Session, url: str) -> List[Dict]:
    """Paginate through GitHub API responses.

    Follows the Link header for pagination as documented in:
    https://docs.github.com/en/rest/guides/using-pagination-in-the-rest-api
    """
    results = []
    while url:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()

        # Handle both list and dict responses
        if isinstance(data, list):
            results.extend(data)
        else:
            results.append(data)

        # Check for pagination using Link header (RFC 8288)
        # Format: <https://api.github.com/...?page=2>; rel="next", <...>; rel="last"
        link_header = response.headers.get("Link", "")
        url = None
        if link_header:
            # Match URLs within angle brackets that have rel="next"
            # Pattern: <URL>; rel="next"
            match = re.search(r'<([^>]+)>;\s*rel="next"', link_header)
            if match:
                url = match.group(1)

    return results


def get_org_repos(org: str, token: str) -> List[str]:
    """Get all repos in the org"""
    print("Fetching org repositories...")
    session = create_github_session(token)
    url = f"{GITHUB_API_BASE}/orgs/{org}/repos?per_page=100"
    repos_data = paginate_github_api(session, url)
    repos = [repo["name"] for repo in repos_data if not repo["archived"]]
    print(f"Found {len(repos)} repositories.")
    return repos


def get_lsdb_repos(token: str) -> List[str]:
    """Get all repos that are related to HATS or LSDB"""
    print("Fetching org repositories...")
    session = create_github_session(token)
    url = f"{GITHUB_API_BASE}/orgs/astronomy-commons/repos?per_page=100"
    repos_data = paginate_github_api(session, url)
    repos = [repo["name"] for repo in repos_data]
    repos = [repo for repo in repos if "hats" in repo or "lsdb" in repo]
    print(f"Found {len(repos)} repositories.")
    return repos


def get_humanized_updated_at(iso_time: str, now: datetime) -> str:
    """Convenience method to get a human readable duration, like '2 days ago'."""
    try:
        dt = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return human_readable.date_time(dt, when=now)
    except Exception:  # pylint: disable=broad-except
        return iso_time
