"""Visits all of the organization's repositories, collects open
issues, filters out all issues created by members of the organization,
or only commented by members of the "astronomy-commons/lincc-frameworks"
organization, and writes them to HTML for human monitoring.
"""

import sys
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Set

import requests
from jinja2 import Environment, FileSystemLoader

from lf_workflow_dash.lsdb_interrupts.github_api import (
    GITHUB_API_BASE,
    TEAM_MEMBERS,
    create_github_session,
    get_humanized_updated_at,
    get_lsdb_repos,
    paginate_github_api,
)


def get_open_issues(org: str, repos: List[str], org_members: Set[str], token: str) -> List[Dict]:
    """Find all OPEN issues that were either CREATED or COMMENTED on by folks
    NOT in the core team."""
    print("Fetching open issues for all repositories...")
    session = create_github_session(token)
    all_issues = []
    for repo in repos:
        print(f"  {repo}...")
        try:
            ## First, find all issues with some external interest, in the form of comments.
            url = f"{GITHUB_API_BASE}/repos/{org}/{repo}/issues/comments?per_page=100"
            comments_data = paginate_github_api(session, url)

            issue_numbers = [
                (int(comment["issue_url"].split("/")[-1]), comment["user"]["login"])
                for comment in comments_data
                if comment["user"]["login"] not in org_members and comment["user"]["type"] == "User"
            ]

            issues_with_comments = defaultdict(dict)
            for issue_num, commenter in issue_numbers:
                issues_with_comments.setdefault(issue_num, [])
                issues_with_comments[issue_num].append(commenter)

            ## Now, get all of the issues for the repo.
            url = f"{GITHUB_API_BASE}/repos/{org}/{repo}/issues?state=open&per_page=100"
            issues_data = paginate_github_api(session, url)

            # Filter out pull requests (they also come through the issues API)
            issues = [
                {
                    "number": issue["number"],
                    "title": issue["title"],
                    "author": issue["user"],
                    "updatedAt": issue["updated_at"],
                    "url": issue["html_url"],
                    "commenters": set(issues_with_comments[issue["number"]]),
                }
                for issue in issues_data
                if "pull_request" not in issue
            ]

            ## Only keep issue if it was created by an external user, or they've left a comment.
            issues = [
                issue
                for issue in issues
                if ((issue["author"] and issue["author"]["login"] not in org_members) or issue["commenters"])
            ]
            print(f"     Found {len(issues)} external issues.")

            all_issues.extend(issues)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issues for repo {repo}: {e}")
    print(f"Collected {len(all_issues)} open issues.")
    return all_issues


def write_html_issues(external_issues: List[Dict], html_file: str):
    """Fill in the jinja template, using the external interest issues found"""
    print(f"Writing HTML output to {html_file} ...")

    now = datetime.now(timezone.utc)
    issue_summaries = []
    for issue in external_issues:
        issue_summaries.append(
            {
                "updated_human": get_humanized_updated_at(issue["updatedAt"], now),
                "author": issue["author"]["login"] if issue["author"] else "unknown",
                "title": issue["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"),
                "url": issue["url"],
                "commenters": ", ".join(issue["commenters"] - set([issue["author"]["login"]])),
            }
        )

    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("issue_list.jinja")
    with open(html_file, mode="w", encoding="utf-8") as results:
        results.write(template.render({"external_issues": issue_summaries}))
    print(f"HTML output written to {html_file}")


def main(token, out_file):
    """Convenience method to do the work."""
    repos = get_lsdb_repos("astronomy-commons", token)
    external_issues = get_open_issues("astronomy-commons", repos, TEAM_MEMBERS, token)
    # Sort by most recent activity
    external_issues.sort(key=lambda x: x["updatedAt"], reverse=True)

    write_html_issues(external_issues, out_file)


if __name__ == "__main__":
    TOKEN = sys.argv[1]
    OUT_FILE = sys.argv[2]
    main(TOKEN, OUT_FILE)
