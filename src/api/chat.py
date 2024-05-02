"""Code to implement the chat API."""

from __future__ import annotations

import json

import fastapi
import pydantic
from config import MODEL

from .globals import clients

router = fastapi.APIRouter()


class Message(pydantic.BaseModel):
    """Message model for the chat API."""

    content: str
    role: str = "user"


class ChatRequest(pydantic.BaseModel):
    """Chat request model for the chat API."""

    messages: list[Message]
    stream: bool = True


@router.post("/chat")
async def chat_handler(chat_request: ChatRequest) -> dict[str, str]:
    """Handle the chat API."""
    messages = [{"role": "system", "content": "You are a helpful assistant."}, *chat_request.messages]
    # Azure Open AI takes the deployment name as the model name
    model = MODEL

    if chat_request.stream:

        async def response_stream() -> fastapi.responses.StreamingResponse:
            """Stream the response."""
            chat_coroutine = clients["openai"].chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )
            async for event in await chat_coroutine:
                yield json.dumps(event.model_dump(), ensure_ascii=False) + "\n"

        return fastapi.responses.StreamingResponse(response_stream())
    else:
        response = await clients["openai"].chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
        )
        return response.model_dump()
