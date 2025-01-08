import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from flexrag.prompt import ChatPrompt
from flexrag.retriever import RetrievedContext
from flexrag.utils import Register


class AssistantBase(ABC):
    @abstractmethod
    def answer(
        self, question: str
    ) -> tuple[str, Optional[list[RetrievedContext]], Optional[dict]]:
        """Answer the given question.

        Args:
            question (str): The question to answer.

        Returns:
            response (str): The response to the question.
            contexts (Optional[list[RetrievedContext]]): The contexts used to answer the question.
            metadata (Optional[dict]): The metadata of the assistant.
        """
        return


@dataclass
class SearchHistory:
    query: str
    contexts: list[RetrievedContext]

    def to_dict(self) -> dict[str, str | list[dict]]:
        return {
            "query": self.query,
            "contexts": [ctx.to_dict() for ctx in self.contexts],
        }


ASSISTANTS = Register[AssistantBase]("assistant")


PREDEFINED_PROMPTS = {
    "shortform_with_context": ChatPrompt.from_json(
        os.path.join(
            os.path.dirname(__file__),
            "assistant_prompts",
            "shortform_generate_prompt_with_context.json",
        )
    ),
    "shortform_without_context": ChatPrompt.from_json(
        os.path.join(
            os.path.dirname(__file__),
            "assistant_prompts",
            "shortform_generate_prompt_without_context.json",
        )
    ),
    "longform_with_context": ChatPrompt.from_json(
        os.path.join(
            os.path.dirname(__file__),
            "assistant_prompts",
            "longform_generate_prompt_with_context.json",
        )
    ),
    "longform_without_context": ChatPrompt.from_json(
        os.path.join(
            os.path.dirname(__file__),
            "assistant_prompts",
            "longform_generate_prompt_without_context.json",
        )
    ),
}
