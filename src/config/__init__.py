"""File to initialise the configuration for the application."""

import os

from .helper_functions import load_from_env_file

# Load the environment variables from the .env file
load_from_env_file()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RUNNING_IN_PRODUCTION = os.getenv("RUNNING_IN_PRODUCTION")
MODEL = os.getenv("MODEL", "gpt-3.5-turbo")
