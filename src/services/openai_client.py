"""Small server-side OpenAI Responses API client for KMS AI activities."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.contracts import ValidationError


class OpenAIClientError(RuntimeError):
    """Raised when an OpenAI API call cannot produce a valid response."""


@dataclass(frozen=True)
class OpenAIResponsesClient:
    api_key: str
    model: str = "gpt-4o"
    timeout_seconds: float = 30.0
    endpoint: str = "https://api.openai.com/v1/responses"

    def create_json_response(self, *, instructions: str, user_input: str) -> Mapping[str, Any]:
        if not self.api_key.strip():
            raise OpenAIClientError("OPENAI_API_KEY is required for AI extraction")
        payload = {
            "model": self.model,
            "instructions": instructions,
            "input": user_input,
            "temperature": 0,
        }
        request = Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise OpenAIClientError(f"OpenAI API request failed with HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise OpenAIClientError(f"OpenAI API request failed: {exc.reason}") from exc
        try:
            response_payload = json.loads(raw)
            output_text = _extract_output_text(response_payload)
            parsed = json.loads(output_text)
        except (json.JSONDecodeError, KeyError, TypeError, ValidationError) as exc:
            raise OpenAIClientError("OpenAI API response did not contain valid candidate JSON") from exc
        if not isinstance(parsed, Mapping):
            raise OpenAIClientError("OpenAI API response JSON must be an object")
        return parsed


def _extract_output_text(payload: Mapping[str, Any]) -> str:
    direct = payload.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct
    for output in payload.get("output", []):
        if not isinstance(output, Mapping):
            continue
        for content in output.get("content", []):
            if isinstance(content, Mapping) and isinstance(content.get("text"), str):
                return content["text"]
    raise ValidationError("missing output text")


__all__ = ["OpenAIClientError", "OpenAIResponsesClient"]
