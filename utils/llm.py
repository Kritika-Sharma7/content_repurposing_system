"""
LLM utility for OpenAI API calls with structured output support.
Provides a reusable interface for all agents to make LLM calls.
"""

import json
import os
from typing import Type, TypeVar

from openai import OpenAI, APIError, RateLimitError, AuthenticationError
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMError(Exception):
    """Custom exception for LLM-related errors."""
    pass


class LLMClient:
    """
    Reusable LLM client for structured output generation.
    Wraps OpenAI API with Pydantic model parsing.
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        api_key: str | None = None,
    ):
        """
        Initialize the LLM client.

        Args:
            model: OpenAI model to use (default: gpt-4o)
            temperature: Sampling temperature (default: 0.7)
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        
        Raises:
            LLMError: If no API key is provided or found in environment
        """
        self.model = model
        self.temperature = temperature
        
        # Get API key with better error handling
        resolved_key = api_key or os.getenv("OPENAI_API_KEY")
        if not resolved_key:
            raise LLMError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        if resolved_key.startswith("sk-your"):
            raise LLMError(
                "Please replace the placeholder API key with your actual OpenAI API key."
            )
            
        self.client = OpenAI(api_key=resolved_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        output_schema: Type[T],
        temperature: float | None = None,
    ) -> T:
        """
        Generate structured output from the LLM.

        Args:
            system_prompt: System message defining agent role
            user_prompt: User message with the task
            output_schema: Pydantic model class for response parsing
            temperature: Override default temperature if needed

        Returns:
            Parsed Pydantic model instance
            
        Raises:
            LLMError: On API errors with helpful messages
        """
        # Build the JSON schema instruction
        schema_json = json.dumps(output_schema.model_json_schema(), indent=2, ensure_ascii=True)

        # Append schema requirements to system prompt
        full_system_prompt = f"""{system_prompt}

You MUST respond with valid JSON that conforms to this schema:
{schema_json}

Respond ONLY with the JSON object, no additional text or markdown formatting."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=temperature or self.temperature,
                messages=[
                    {"role": "system", "content": full_system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
            )
        except AuthenticationError as e:
            raise LLMError(
                f"Authentication failed. Please check your API key is valid. Error: {e}"
            )
        except RateLimitError as e:
            raise LLMError(
                f"Rate limit exceeded. Please wait and try again, or check your API quota. Error: {e}"
            )
        except APIError as e:
            raise LLMError(
                f"OpenAI API error: {e}"
            )

        # Extract and parse the response
        content = response.choices[0].message.content
        if content is None:
            raise LLMError("LLM returned empty response")

        # Parse JSON and validate against schema
        try:
            data = json.loads(content)
            return output_schema.model_validate(data)
        except json.JSONDecodeError as e:
            raise LLMError(f"Failed to parse LLM response as JSON: {e}")
        except Exception as e:
            raise LLMError(f"Failed to validate response against schema: {e}")

    def generate_with_context(
        self,
        system_prompt: str,
        context: dict,
        task: str,
        output_schema: Type[T],
        temperature: float | None = None,
    ) -> T:
        """
        Generate structured output with additional context data.

        Args:
            system_prompt: System message defining agent role
            context: Dictionary of context data to include
            task: The specific task instruction
            output_schema: Pydantic model class for response parsing
            temperature: Override default temperature if needed

        Returns:
            Parsed Pydantic model instance
        """
        # Format context as readable sections
        context_str = "\n\n".join(
            f"### {key.upper()}\n{json.dumps(value, indent=2) if isinstance(value, (dict, list)) else value}"
            for key, value in context.items()
        )

        user_prompt = f"""CONTEXT:
{context_str}

TASK:
{task}"""

        return self.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=output_schema,
            temperature=temperature,
        )


# Singleton instance for convenience
_default_client: LLMClient | None = None


def get_llm_client(
    model: str = "gpt-4o",
    temperature: float = 0.7,
) -> LLMClient:
    """
    Get or create a default LLM client instance.

    Args:
        model: OpenAI model to use
        temperature: Sampling temperature

    Returns:
        LLMClient instance
    """
    global _default_client
    if _default_client is None:
        _default_client = LLMClient(model=model, temperature=temperature)
    return _default_client
