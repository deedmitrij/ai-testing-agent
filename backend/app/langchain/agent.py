from langchain.agents import AgentExecutor, StructuredChatAgent
from langchain.prompts import MessagesPlaceholder
from langchain.prompts.chat import ChatPromptTemplate
from backend.app.langchain.tools import all_tools
from backend.services.gemini_service import GeminiService


gemini_service = GeminiService()


def run_agent_with_tools(user_input: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ('system',
         "You are a smart and helpful AI assistant "
         "specializing in tasks related to Business Analysis and Quality Assurance. "
         "Your responsibilities include understanding and analyzing JIRA tickets, "
         "generating user stories, creating test cases, writing automation test scripts. "
         "You support users through structured, multi-step workflows "
         "to ensure quality and clarity in product requirements and test coverage.\n"
         "Use the context to determine if the user is:\n"
         "- Providing a JIRA ticket number or asking for JIRA ticket details.\n"
         "- Expecting a generated user story based on a ticket or input.\n"
         "- Asking for manual or automated test cases.\n"
         "- Reviewing or confirming a previously generated item (user story, test case, etc.).\n"
         "- Moving to a new task, or needs clarification or help."),
        MessagesPlaceholder(variable_name='chat_history'),
        ('human', '{input}')
    ])

    agent = StructuredChatAgent.from_llm_and_tools(
        llm=gemini_service.langchain_model,
        tools=all_tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        llm=gemini_service.langchain_model,
        tools=all_tools,
        memory_key='chat_history',
        verbose=True,
        handle_parsing_errors=True
    )

    response = agent_executor.run(user_input)
    return response
