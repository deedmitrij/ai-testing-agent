import json
import re
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.config import GEMINI_API_KEY, PROJECT_ROOT


class GeminiService:
    """Handles AI interactions with Google Gemini."""

    def __init__(self):
        """Initializes the service with native and LangChain-based models."""
        genai.configure(api_key=GEMINI_API_KEY)
        model = "gemini-1.5-flash"
        self.native_model = genai.GenerativeModel(model)
        self.langchain_model = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=GEMINI_API_KEY,
            temperature=0.3,
            max_output_tokens=2048,
        )

    @staticmethod
    def _get_prompt(prompt_file: str) -> str:
        """
        Loads a prompt template from a file.

        Args:
            prompt_file (str): The name of the prompt file to load.

        Returns:
            str: The content of the prompt file.
        """
        prompt_path = PROJECT_ROOT / f'backend/prompts/{prompt_file}'
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read()
        return prompt

    def _generate_ticket(self, data: str, prompt_file: str) -> dict:
        """
        Generates a structured ticket data.

        Args:
            data (str): The input data for generation (e.g., requirements).
            prompt_file (str): Filename of the prompt template to use.

        Returns:
            dict: A dictionary (with 'summary' and 'description' fields) containing the generated ticket information.
        """
        prompt = PromptTemplate(
            input_variables=['requirements'],
            template=self._get_prompt(prompt_file)
        )
        response = self.native_model.generate_content(prompt.format(requirements=data))
        str_json_text = re.search(r"```(?:json)?\s*([\[{].*?[\]}])\s*```", response.text, re.DOTALL).group(1)
        return json.loads(str_json_text)

    def generate_user_story(self, ticket_data: str) -> dict:
        """
        Generates a user story from given requirement data.

        Args:
            ticket_data (str): The plain text requirements.

        Returns:
            dict: A structured user story.
        """
        # Generate a user story based on the ticket data
        return self._generate_ticket(data=ticket_data, prompt_file='generate_user_story.txt')

    def generate_test_cases(self, user_story_data: str) -> dict:
        """
        Generates test cases based on a user story.

        Args:
            user_story_data (str): The plain text user story.

        Returns:
            dict: A structured list of test cases.
        """
        return self._generate_ticket(data=user_story_data, prompt_file='generate_test_cases.txt')
