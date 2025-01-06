from __future__ import annotations
from typing import Dict, Any, Optional, Set, Union, TYPE_CHECKING
from functools import cached_property

from edsl.prompts.Prompt import Prompt

from dataclasses import dataclass

from .prompt_helpers import PromptPlan
from .QuestionTemplateReplacementsBuilder import (
    QuestionTemplateReplacementsBuilder,
)
from .question_option_processor import QuestionOptionProcessor

if TYPE_CHECKING:
    from edsl.agents.InvigilatorBase import InvigilatorBase
    from edsl.questions.QuestionBase import QuestionBase
    from edsl.agents.Agent import Agent
    from edsl.surveys.Survey import Survey
    from edsl.language_models.LanguageModel import LanguageModel
    from edsl.surveys.MemoryPlan import MemoryPlan
    from edsl.questions.QuestionBase import QuestionBase
    from edsl.scenarios.Scenario import Scenario


class BasePlaceholder:
    """Base class for placeholder values when a question is not yet answered."""

    def __init__(self, placeholder_type: str = "answer"):
        self.value = "N/A"
        self.comment = "Will be populated by prior answer"
        self._type = placeholder_type

    def __getitem__(self, index):
        return ""

    def __str__(self):
        return f"<<{self.__class__.__name__}:{self._type}>>"

    def __repr__(self):
        return self.__str__()


class PlaceholderAnswer(BasePlaceholder):
    def __init__(self):
        super().__init__("answer")


class PlaceholderComment(BasePlaceholder):
    def __init__(self):
        super().__init__("comment")


class PlaceholderGeneratedTokens(BasePlaceholder):
    def __init__(self):
        super().__init__("generated_tokens")


class PromptConstructor:
    """
    This class constructs the prompts for the language model.

    The pieces of a prompt are:
    - The agent instructions - "You are answering questions as if you were a human. Do not break character."
    - The persona prompt - "You are an agent with the following persona: {'age': 22, 'hair': 'brown', 'height': 5.5}"
    - The question instructions - "You are being asked the following question: Do you like school? The options are 0: yes 1: no Return a valid JSON formatted like this, selecting only the number of the option: {"answer": <put answer code here>, "comment": "<put explanation here>"} Only 1 option may be selected."
    - The memory prompt - "Before the question you are now answering, you already answered the following question(s): Question: Do you like school? Answer: Prior answer"
    """

    def __init__(
        self, invigilator: "InvigilatorBase", prompt_plan: Optional["PromptPlan"] = None
    ):
        self.invigilator = invigilator
        self.prompt_plan = prompt_plan or PromptPlan()

        self.agent = invigilator.agent
        self.question = invigilator.question
        self.scenario = invigilator.scenario
        self.survey = invigilator.survey
        self.model = invigilator.model
        self.current_answers = invigilator.current_answers
        self.memory_plan = invigilator.memory_plan

    def get_question_options(self, question_data):
        """Get the question options."""
        return QuestionOptionProcessor(self).get_question_options(question_data)

    @cached_property
    def agent_instructions_prompt(self) -> Prompt:
        """
        >>> from edsl.agents.InvigilatorBase import InvigilatorBase
        >>> i = InvigilatorBase.example()
        >>> i.prompt_constructor.agent_instructions_prompt
        Prompt(text=\"""You are answering questions as if you were a human. Do not break character.\""")
        """
        from edsl.agents.Agent import Agent

        if self.agent == Agent():  # if agent is empty, then return an empty prompt
            return Prompt(text="")

        return Prompt(text=self.agent.instruction)

    @cached_property
    def agent_persona_prompt(self) -> Prompt:
        """
        >>> from edsl.agents.InvigilatorBase import InvigilatorBase
        >>> i = InvigilatorBase.example()
        >>> i.prompt_constructor.agent_persona_prompt
        Prompt(text=\"""Your traits: {'age': 22, 'hair': 'brown', 'height': 5.5}\""")
        """
        from edsl.agents.Agent import Agent

        if self.agent == Agent():  # if agent is empty, then return an empty prompt
            return Prompt(text="")

        return self.agent.prompt()

    def prior_answers_dict(self) -> dict[str, "QuestionBase"]:
        """This is a dictionary of prior answers, if they exist."""
        return self._add_answers(
            self.survey.question_names_to_questions(), self.current_answers
        )

    @staticmethod
    def _extract_quetion_and_entry_type(key_entry) -> tuple[str, str]:
        """
        Extracts the question name and type for the current answer dictionary key entry.

        >>> PromptConstructor._extract_quetion_and_entry_type("q0")
        ('q0', 'answer')
        >>> PromptConstructor._extract_quetion_and_entry_type("q0_comment")
        ('q0', 'comment')
        >>> PromptConstructor._extract_quetion_and_entry_type("q0_alternate_generated_tokens")
        ('q0_alternate', 'generated_tokens')
        >>> PromptConstructor._extract_quetion_and_entry_type("q0_alt_comment")
        ('q0_alt', 'comment')
        """
        split_list = key_entry.rsplit("_", maxsplit=1)
        if len(split_list) == 1:
            question_name = split_list[0]
            entry_type = "answer"
        else:
            if split_list[1] == "comment":
                question_name = split_list[0]
                entry_type = "comment"
            elif split_list[1] == "tokens":  # it's actually 'generated_tokens'
                question_name = key_entry.replace("_generated_tokens", "")
                entry_type = "generated_tokens"
            else:
                question_name = key_entry
                entry_type = "answer"
        return question_name, entry_type

    @staticmethod
    def _augmented_answers_dict(current_answers: dict) -> dict:
        """
        >>> PromptConstructor._augmented_answers_dict({"q0": "LOVE IT!", "q0_comment": "I love school!"})
        {'q0': {'answer': 'LOVE IT!', 'comment': 'I love school!'}}
        """
        from collections import defaultdict

        d = defaultdict(dict)
        for key, value in current_answers.items():
            question_name, entry_type = (
                PromptConstructor._extract_quetion_and_entry_type(key)
            )
            d[question_name][entry_type] = value
        return dict(d)

    @staticmethod
    def _add_answers(
        answer_dict: dict, current_answers: dict
    ) -> dict[str, "QuestionBase"]:
        """
        >>> from edsl import QuestionFreeText
        >>> d = {"q0": QuestionFreeText(question_text="Do you like school?", question_name = "q0")}
        >>> current_answers = {"q0": "LOVE IT!"}
        >>> PromptConstructor._add_answers(d, current_answers)['q0'].answer
        'LOVE IT!'
        """
        augmented_answers = PromptConstructor._augmented_answers_dict(current_answers)

        for question in answer_dict:
            if question in augmented_answers:
                for entry_type, value in augmented_answers[question].items():
                    setattr(answer_dict[question], entry_type, value)
            else:
                answer_dict[question].answer = PlaceholderAnswer()
                answer_dict[question].comment = PlaceholderComment()
                answer_dict[question].generated_tokens = PlaceholderGeneratedTokens()
        return answer_dict

    @cached_property
    def question_file_keys(self) -> list:
        """Extracts the file keys from the question text.
        It checks if the variables in the question text are in the scenario file keys.
        """
        return QuestionTemplateReplacementsBuilder(self).question_file_keys()

    @cached_property
    def question_instructions_prompt(self) -> Prompt:
        """
        >>> from edsl.agents.InvigilatorBase import InvigilatorBase
        >>> i = InvigilatorBase.example()
        >>> i.prompt_constructor.question_instructions_prompt
        Prompt(text=\"""...
        ...
        """
        return self.build_question_instructions_prompt()

    def build_question_instructions_prompt(self) -> Prompt:
        """Buils the question instructions prompt."""
        from edsl.agents.QuestionInstructionPromptBuilder import (
            QuestionInstructionPromptBuilder,
        )

        return QuestionInstructionPromptBuilder(self).build()

    @cached_property
    def prior_question_memory_prompt(self) -> Prompt:
        memory_prompt = Prompt(text="")
        if self.memory_plan is not None:
            memory_prompt += self.create_memory_prompt(
                self.question.question_name
            ).render(self.scenario | self.prior_answers_dict())
        return memory_prompt

    def create_memory_prompt(self, question_name: str) -> Prompt:
        """Create a memory for the agent.

        The returns a memory prompt for the agent.

        >>> from edsl.agents.InvigilatorBase import InvigilatorBase
        >>> i = InvigilatorBase.example()
        >>> i.current_answers = {"q0": "Prior answer"}
        >>> i.memory_plan.add_single_memory("q1", "q0")
        >>> p = i.prompt_constructor.create_memory_prompt("q1")
        >>> p.text.strip().replace("\\n", " ").replace("\\t", " ")
        'Before the question you are now answering, you already answered the following question(s):          Question: Do you like school?  Answer: Prior answer'
        """
        return self.memory_plan.get_memory_prompt_fragment(
            question_name, self.current_answers
        )

    def get_prompts(self) -> Dict[str, Prompt]:
        """Get both prompts for the LLM call.

        >>> from edsl import QuestionFreeText
        >>> from edsl.agents.InvigilatorBase import InvigilatorBase
        >>> q = QuestionFreeText(question_text="How are you today?", question_name="q_new")
        >>> i = InvigilatorBase.example(question = q)
        >>> i.get_prompts()
        {'user_prompt': ..., 'system_prompt': ...}
        """
        prompts = self.prompt_plan.get_prompts(
            agent_instructions=self.agent_instructions_prompt,
            agent_persona=self.agent_persona_prompt,
            question_instructions=Prompt(self.question_instructions_prompt),
            prior_question_memory=self.prior_question_memory_prompt,
        )
        if self.question_file_keys:
            files_list = []
            for key in self.question_file_keys:
                files_list.append(self.scenario[key])
            prompts["files_list"] = files_list
        return prompts


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
