"""
Environment configuration for testing.

This module provides functionality to initialize environment variables
for testing purposes. Note that this is for testing only and should not
be used in production environments.
"""

import os


def initialize_environment():
    """
    Initialize environment variables for testing.
    
    Sets up environment variables for:
    - API keys (Gemini, Pulse, Azure)
    - Service endpoints
    - Monitoring configuration
    
    Warning: This is for testing only! Contains sensitive information
    that should be properly secured in production.
    """
    environmental_variables = {
        "GEMINI_API_KEY": "AIzaSyC0N9NCAVKKTJ9A73RXQ5P1pqW0R0o4USc",
        "PULSE_API_KEY": "c37dcf42-7c84-4e2e-9067-e91e039ee999",
        "OPENAI_AZURE_API_KEY": "G2EFa1vxn38g7u5gXian2n3pYFIEKXpRqoR95BnOOZM3gL9D7Kc1JQQJ99ALACLArgHXJ3w3AAABACOGyfb5",
        
        # TODO - apisix uris
        "INFERENCE_URL": "http://localhost:4016",
        
        "LANGFUSE_SECRET_KEY": "sk-lf-1b9882ca-1c4d-413c-8361-ccea19a1a742",
        "LANGFUSE_PUBLIC_KEY": "pk-lf-ce18fc07-fcb4-46bc-a205-5eb081c999de",
        "LANGFUSE_HOST": "http://localhost:3000",
    }

    for key, value in environmental_variables.items():
        os.environ[key] = value
    
    
    
    