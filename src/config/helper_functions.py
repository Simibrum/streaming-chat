"""Configuration helper functions."""

from __future__ import annotations

import contextlib
import os
from pathlib import Path

import tiktoken


# Load the environment variables if working in weird environments
def load_from_env_file() -> None:
    """Load environment variables from a file."""
    # Load environment variables from project root .env file
    # Set path of .env file
    env_path = Path(__file__).parent.parent.parent.joinpath(".env")
    with contextlib.suppress(FileNotFoundError):
        # Load environment variables from .env file
        load_env_vars(env_path)


def load_env_vars(path: Path) -> None:
    """Load environment variables from a file."""
    with Path.open(path) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                # Split the line into the variable name and value
                var, value = line.split("=")

                # Strip leading and trailing whitespace from the variable name and value
                var = var.strip()
                value = value.strip()

                if var and value:
                    # Set the environment variable
                    os.environ[var] = value


# OpenAI method for counting tokens
def num_tokens_from_messages(messages: list[dict], model: str = "gpt-3.5-turbo-0301") -> int:
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
    else:
        raise NotImplementedError
    return num_tokens
