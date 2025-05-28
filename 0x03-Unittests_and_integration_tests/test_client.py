#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value and get_json is called once with the right URL."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_payload)

    # --- New test case example below ---

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the correct URL based on the org payload.
        """
        # Mock the 'org' property to return a specific payload
        test_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_org.return_value = test_payload

        # Instantiate GithubOrgClient (org_name doesn't strictly matter here as 'org' is mocked)
        client = GithubOrgClient("google")

        # Call the method being tested
        result = client._public_repos_url

        # Assertions
        self.assertEqual(result, test_payload["repos_url"])
        mock_org.assert_called_once() # Ensure the 'org' property was accessed


if __name__ == "__main__":
    unittest.main()