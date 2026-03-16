"""
LLM Client Wrapper
Supports both OpenAI and Anthropic (Claude) APIs
"""

import json
import re
from typing import Optional, Dict, Any, List

from ..config import Config


class LLMClient:
    """LLM Client - supports OpenAI-compatible and Anthropic APIs"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        provider: Optional[str] = None
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model = model or Config.LLM_MODEL_NAME
        self.provider = (provider or Config.LLM_PROVIDER or "").lower()

        if not self.api_key:
            raise ValueError("LLM_API_KEY not configured")

        # Auto-detect provider if not specified
        if not self.provider:
            self.provider = self._detect_provider()

        # Initialize the appropriate client
        if self.provider == "anthropic":
            try:
                from anthropic import Anthropic
            except ImportError:
                raise ImportError(
                    "anthropic package required for Claude support. "
                    "Install with: pip install anthropic"
                )
            self.client = Anthropic(api_key=self.api_key)
        else:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )

    def _detect_provider(self) -> str:
        """Auto-detect provider from base_url or model name"""
        model_lower = (self.model or "").lower()
        base_lower = (self.base_url or "").lower()

        # Anthropic detection
        if any(k in model_lower for k in ["claude", "anthropic"]):
            return "anthropic"
        if "anthropic" in base_lower:
            return "anthropic"

        # Default to OpenAI-compatible
        return "openai"

    def _split_system_message(self, messages: List[Dict[str, str]]):
        """
        Split system message from conversation messages.
        Anthropic requires system as a separate parameter.
        Returns (system_text, conversation_messages)
        """
        system_text = None
        conversation = []

        for msg in messages:
            if msg.get("role") == "system":
                if system_text is None:
                    system_text = msg["content"]
                else:
                    system_text += "\n\n" + msg["content"]
            else:
                conversation.append(msg)

        return system_text, conversation

    def _clean_content(self, content: str) -> str:
        """Remove <think> tags from reasoning models"""
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
        return content

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        Send a chat request.

        Args:
            messages: Message list
            temperature: Temperature parameter
            max_tokens: Maximum tokens
            response_format: Response format (e.g., JSON mode, OpenAI only)

        Returns:
            Model response text
        """
        if self.provider == "anthropic":
            return self._chat_anthropic(messages, temperature, max_tokens, response_format)
        else:
            return self._chat_openai(messages, temperature, max_tokens, response_format)

    def _chat_openai(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        response_format: Optional[Dict]
    ) -> str:
        """Chat via OpenAI-compatible API"""
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format:
            kwargs["response_format"] = response_format

        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        return self._clean_content(content)

    def _chat_anthropic(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        response_format: Optional[Dict] = None
    ) -> str:
        """Chat via Anthropic API"""
        system_text, conversation = self._split_system_message(messages)

        # If JSON format requested, add instruction to system prompt
        if response_format and response_format.get("type") == "json_object":
            json_instruction = "\n\nIMPORTANT: You must respond with valid JSON only. No markdown, no explanation, just pure JSON."
            if system_text:
                system_text += json_instruction
            else:
                system_text = json_instruction.strip()

        kwargs = {
            "model": self.model,
            "messages": conversation,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if system_text:
            kwargs["system"] = system_text

        response = self.client.messages.create(**kwargs)
        content = response.content[0].text
        return self._clean_content(content)

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Send a chat request and return JSON.

        Args:
            messages: Message list
            temperature: Temperature parameter
            max_tokens: Maximum tokens

        Returns:
            Parsed JSON object
        """
        response = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        # Clean markdown code block markers
        cleaned_response = response.strip()
        cleaned_response = re.sub(r'^```(?:json)?\s*\n?', '', cleaned_response, flags=re.IGNORECASE)
        cleaned_response = re.sub(r'\n?```\s*$', '', cleaned_response)
        cleaned_response = cleaned_response.strip()

        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON returned by LLM: {cleaned_response}")
