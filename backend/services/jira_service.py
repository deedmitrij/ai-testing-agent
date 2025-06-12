import requests
from typing import Dict
from backend.config import JIRA_API_KEY, JIRA_USER_EMAIL, JIRA_BASE_URL
from requests.auth import HTTPBasicAuth


class JiraService:
    """Service for interacting with the Jira API to fetch and create tickets."""

    def __init__(self):
        """Initializes the service. Constructs the API endpoint URLs and sets up HTTP Basic Authentication."""
        self.base_url = JIRA_BASE_URL
        self.api_url = f"{self.base_url}/rest/api/2/issue"
        self.auth = HTTPBasicAuth(JIRA_USER_EMAIL, JIRA_API_KEY)

    def fetch_ticket(self, ticket_number: str) -> str:
        """
        Fetches the description of a Jira ticket.

        Args:
            ticket_number (str): The Jira ticket ID (e.g., "SHAS-123").

        Returns:
            str: The description field of the Jira ticket.
        """
        url = f"{self.api_url}/{ticket_number}"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()['fields']['description']

    def _create_ticket(self, data: Dict[str, str], issuetype: str, linked_ticket_id: str) -> str:
        """
        Creates a Jira ticket and links it to another ticket.

        Args:
            data (Dict[str, str]): A dictionary containing:
                                    - 'summary' (str): The summary (title) of the new ticket.
                                    - 'description' (str): The detailed description of the new ticket.
            issuetype (str): The type of Jira issue to create (e.g., 'Story', 'Test Case').
            linked_ticket_id (str): Jira ticket ID to link this new ticket to (e.g., "SHAS-456").

        Returns:
            str: The URL of the created Jira ticket.
        """
        payload = {
            "fields": {
                "project": {"key": "SHAS"},
                "summary": data["summary"],
                "description": data["description"],
                "issuetype": {"name": issuetype}
            },
            "update": {
                "issuelinks": [
                    {
                        "add": {
                            "type": {
                                "name": "Relates"
                            },
                            "outwardIssue": {
                                "key": linked_ticket_id
                            }
                        }
                    }
                ]
            }
        }
        response = requests.post(self.api_url, json=payload, auth=self.auth)
        response.raise_for_status()
        return f"{self.base_url}/browse/{response.json()['key']}"

    def create_user_story(self, data: dict, linked_ticket_id: str) -> str:
        """Creates a Jira 'Story' type ticket."""
        return self._create_ticket(data, 'Story', linked_ticket_id)

    def create_test_case(self, data: dict, linked_ticket_id: str) -> str:
        """Creates a Jira 'Test Case' type ticket."""
        return self._create_ticket(data, 'Test Case', linked_ticket_id)
