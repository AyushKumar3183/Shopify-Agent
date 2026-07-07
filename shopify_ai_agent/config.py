"""Shared configuration for the support automation service."""

import os

from dotenv import load_dotenv

from constants import GEMINI_MODEL

load_dotenv()

# Re-export for callers that import from config.
__all__ = ["APP_NAME", "GEMINI_MODEL"]

APP_NAME: str = os.getenv("APP_NAME", "shopify_support")
