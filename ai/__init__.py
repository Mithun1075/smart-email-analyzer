"""
ai package initialization.
Ensures the package can be imported without errors.
"""

# Export the main AI service for convenient import elsewhere
from .services import generate_ai_response  # noqa: F401
