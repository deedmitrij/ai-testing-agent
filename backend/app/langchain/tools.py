from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from backend.services.gemini_service import GeminiService
from backend.services.jira_service import JiraService


gemini_service = GeminiService()
jira_service = JiraService()


class TicketID(BaseModel):
    ticket_id: str = Field(description="Unique identifier of the JIRA ticket")


def create_user_story(ticket_id: str) -> str:
    ticket_details = jira_service.fetch_ticket(ticket_id)
    user_story = gemini_service.generate_user_story(ticket_details)
    created_user_story_link = jira_service.create_user_story(data=user_story, linked_ticket_id=ticket_id)
    return f"The following User Story has been created: {created_user_story_link}"


create_user_story_tool = StructuredTool.from_function(
    name="Create JIRA User Story",
    func=create_user_story,
    description="Use this tool to create a user story. Requires JIRA ticket ID with requirements.",
    args_schema=TicketID,
    return_direct=True
)


def create_test_cases(ticket_id: str) -> str:
    ticket_details = jira_service.fetch_ticket(ticket_id)
    test_cases = gemini_service.generate_test_cases(ticket_details)
    links = []
    for tc in test_cases:
        link = jira_service.create_test_case(data=tc, linked_ticket_id=ticket_id)
        links.append(link)
    return "The following Test Cases have been created:\n" + "\n".join(f"{i}. {el}" for i, el in enumerate(links, 1))


create_test_cases_tool = StructuredTool.from_function(
    name="Create Test Cases",
    func=create_test_cases,
    description="Use this tool to create test cases. Requires JIRA ticket ID with requirements.",
    args_schema=TicketID,
    return_direct=True
)


# === Export All Tools as a List ===
all_tools = [
    create_user_story_tool,
    create_test_cases_tool
]
