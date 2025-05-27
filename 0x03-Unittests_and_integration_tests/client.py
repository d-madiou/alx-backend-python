#!/usr/bin/env python3
"""
Client module to interact with GitHub organization data.
"""

import requests


class GithubOrgClient:
    """GitHub Organization client"""

    def __init__(self, org_name: str):
        self.org_name = org_name

    def org(self) -> dict:
        """Fetches organization data from GitHub API"""
        url = f"https://api.github.com/orgs/{self.org_name}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
