"""Provider and model selection utilities."""

import os

from components.ui import print_colored
from gllm_plugin.supported_models import MODEL_KEY_MAP, MODEL_MAP

def get_available_providers() -> dict[str, list[str]]:
    """
    Get providers that have API keys configured in environment variables.

    Returns:
        Dict mapping provider names to their available models.
    """
    available_providers = {}
    missing_keys = []

    for provider, model_map in MODEL_MAP.items():
        env_var_name = MODEL_KEY_MAP.get(provider)
        if not env_var_name:
            continue

        key = os.getenv(env_var_name)
        if key and not key.strip().startswith("#"):
            available_providers[provider] = model_map
        else:
            missing_keys.append((provider, env_var_name))

    if missing_keys:
        print_colored("\nSome providers are missing API keys:", "yellow")
        for provider, env_var in missing_keys:
            print_colored(
                f"  • {provider}: Set environment variable '{env_var}'", "yellow"
            )
        print()

    return available_providers

def show_missing_providers():
    """Display information about missing provider API keys."""
    print_colored("No provider API keys found in environment variables.", "red")
    print_colored(
        "Please set at least one of the following environment variables:", "yellow"
    )
    for provider, env_var in MODEL_KEY_MAP.items():
        print(f"  • {provider}: {env_var}")