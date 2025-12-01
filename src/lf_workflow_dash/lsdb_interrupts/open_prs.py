import sys
from datetime import datetime, timezone
from typing import Dict, List

import requests
from jinja2 import Environment, FileSystemLoader

from lf_workflow_dash.lsdb_interrupts.github_api import (
    GITHUB_API_BASE,
    create_github_session,
    get_humanized_updated_at,
    get_lsdb_repos,
    get_org_repos,
    paginate_github_api,
)


def get_open_prs(org: str, repos: List[str], token: str) -> List[Dict]:
    """Find all OPEN PRs."""
    print("Fetching open PRs for all repositories...")
    session = create_github_session(token)
    all_prs = []
    for repo in repos:
        print(f"  {repo}...")
        try:
            url = f"{GITHUB_API_BASE}/repos/{org}/{repo}/pulls?state=open&per_page=100"
            pr_data = paginate_github_api(session, url)

            prs = [
                {
                    "number": pr["number"],
                    "title": pr["title"],
                    "author": pr["user"],
                    "updatedAt": pr["updated_at"],
                    "url": pr["html_url"],
                    "repo": repo,
                    "is_draft": pr["draft"],
                }
                for pr in pr_data
            ]
            print(f"     Found {len(prs)} pull requests.")

            all_prs.extend(prs)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching prs for repo {repo}: {e}")
    print(f"Collected {len(all_prs)} open prs.")
    return all_prs


def write_html_prs(prs: List[Dict], html_file: str):
    """Fill in the jinja template, using the prs found"""
    print(f"Writing HTML output to {html_file} ...")

    now = datetime.now(timezone.utc)
    pr_summaries = []
    for pr in prs:
        author = pr["author"]["login"] if pr["author"] else "unknown"
        pr_summaries.append(
            {
                "updated_human": get_humanized_updated_at(pr["updatedAt"], now),
                "author": author,
                "title": pr["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"),
                "url": pr["url"],
                "repo": pr["repo"],
                "is_draft": "DRAFT" if pr["is_draft"] else "",
                "is_bot": author in ["dependabot[bot]", "Copilot"],
            }
        )

    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("pr_list.jinja")
    with open(html_file, mode="w", encoding="utf-8") as results:
        results.write(template.render({"all_prs": pr_summaries, "num_results": len(pr_summaries)}))
    print(f"HTML output written to {html_file}")


def main(token):
    """Convenience method to do the work."""
    repos = get_lsdb_repos(token)
    prs = get_open_prs("astronomy-commons", repos, token)
    prs.sort(key=lambda x: x["updatedAt"], reverse=True)
    write_html_prs(prs, "html/lsdb_prs.html")

    repos = get_org_repos("lincc-frameworks", token)
    prs = get_open_prs("lincc-frameworks", repos, token)
    prs.sort(key=lambda x: x["updatedAt"], reverse=True)
    write_html_prs(prs, "html/lincc_prs.html")


if __name__ == "__main__":
    TOKEN = sys.argv[1]
    main(TOKEN)
