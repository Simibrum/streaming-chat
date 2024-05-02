"""App configuration functions."""

import contextlib
import logging
import os

import fastapi
import openai
from config import OPENAI_API_KEY
from environs import Env
from fastapi.middleware.cors import CORSMiddleware

from .globals import clients


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> None:  # noqa: ARG001 - app is needed for context manager
    """Async context manager for the lifespan of the FastAPI app."""
    client_args = {"api_key": OPENAI_API_KEY}

    clients["openai"] = openai.AsyncOpenAI(
        **client_args,
    )
    yield

    await clients["openai"].close()


def create_app() -> fastapi.FastAPI:
    """Create the FastAPI application."""
    env = Env()

    if not os.getenv("RUNNING_IN_PRODUCTION"):
        env.read_env(".env")
        logging.basicConfig(level=logging.DEBUG)

    app = fastapi.FastAPI(docs_url="/", lifespan=lifespan)

    origins = env.list("ALLOWED_ORIGINS", ["http://localhost", "http://localhost:8080"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from . import chat

    app.include_router(chat.router)

    return app
