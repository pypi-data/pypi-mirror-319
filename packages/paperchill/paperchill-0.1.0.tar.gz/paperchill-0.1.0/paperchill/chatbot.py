import os
import re
from logging import Logger
from typing import List

from openai import AzureOpenAI

from paperchill.with_logger import WithLogger

SUMMARY_LENGTH = 3000
BASE_URL = 'https://ai.exxeta.com/api/v2/azure/openai'
API_KEY = os.environ.get('OPENAI_API_KEY', 'None')
LLM_MODEL = 'gpt-4o-mini'
MAX_TOKENS = 16000
TEMPERATURE = 0.5


class Chatbot(WithLogger):
    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)
        self.client = self.get_client()

    def summarize(self, text: str) -> str:
        self.logger.info(f'Summarizing {len(text)} characters')
        summarize_prompt = f'''
            Please summarize the paper in the system prompt in {SUMMARY_LENGTH} characters or less.
        '''
        summary = self.get_completion(text, summarize_prompt)
        self.logger.info(f'Summarized to {len(summary)} characters:')
        self.logger.info(summary[:80] + '...')
        return summary

    def get_questions(self, text: str, summary: str) -> List[str]:
        questions_prompt = f'''
            Please suggest five questions that could be asked about the paper in the system prompt,
            given that its summary is {summary}.
        '''
        questions_response = self.get_completion(text, questions_prompt)
        self.info(f'Generated {len(questions_response)} characters of questions')
        questions = [
            re.sub(r'\d\.', '', line).strip()
            for line in questions_response.split('\n')
            if line
        ]
        self.info(str(questions))
        return questions

    def get_answer(self, question: str, full_text: str) -> str:
        answer = self.get_completion(full_text, question)
        return answer

    def get_completion(self, full_text: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            messages=[
                {'role': 'system', 'content': system_prompt(full_text)},
                {'role': 'user', 'content': user_prompt}
            ],
            model=LLM_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        return str(response.choices[0].message.content) if response.choices else 'No response'

    def get_client(self) -> AzureOpenAI:
        client = AzureOpenAI(
            api_key=API_KEY,
            api_version='2023-07-01-preview',
            base_url=BASE_URL
        )
        self.info(f'Azure OpenAPI client instantiated with API key {API_KEY[:4]}...')
        return client


def system_prompt(text: str) -> str:
    return f'''
            You are a science communicator who explains scientific papers to highly educated people
            with little specific knowledge of the subject the paper is about.
            The text of the paper is:
            {text}
            '''
