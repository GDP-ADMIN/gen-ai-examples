"""Example demonstrating the usage of gllm-plugin library for building a simple pipeline.

This module shows how to create and execute a basic pipeline using the gllm-plugin library.
It takes user input as a question and processes it through the pipeline to generate a response.
"""

import asyncio
import sys

from simple_pipeline.pipeline import SimplePipelineBuilder
from gllm_plugin.supported_models import MODEL_KEY_MAP
from components.provider import get_available_providers, show_missing_providers
from components.ui import print_colored, display_menu, get_user_choice

async def run_pipeline(provider: str, model: str, api_key: str) -> None:
    """Run the pipeline with the selected provider and model."""
    pipeline_builder = SimplePipelineBuilder()
    pipeline_config = {"model_name": f"{provider}/{model}", "api_key": api_key}

    try:
        pipeline = pipeline_builder.build(pipeline_config)
        print_colored("\nPipeline ready! Enter your question below:", "green")
        user_question = input("Question: ")
        state = pipeline_builder.build_initial_state({"message": user_question}, {})
        await pipeline.invoke(
            initial_state=state, config={"user_multimodal_contents": []}
        )
    except Exception as e:
        print_colored(f"\nError running pipeline: {str(e)}", "red")


async def main() -> None:
    """Main entry point for the application."""
    print_colored("\n=== Custom Pipeline Demo ===", "magenta")
    print_colored(
        "This demo will help you execute a custom pipeline with your chosen model.\n",
        "default",
    )

    available_providers = get_available_providers()
    if not available_providers:
        show_missing_providers()
        return

    provider_names = list(available_providers.keys())
    display_menu(provider_names, "Available Providers")
    provider = get_user_choice(provider_names, "Select a provider (number)")
    if not provider:
        return

    model_names = list(available_providers[provider])
    display_menu(model_names, f"Available Models for {provider}")
    model = get_user_choice(model_names, "Select a model (number)")
    if not model:
        return

    api_key_env = MODEL_KEY_MAP[provider]

    print_colored("\nYour configuration:", "cyan")
    print(f"  • Provider: {provider}")
    print(f"  • Model: {model}")

    confirm = input("\nProceed with this configuration? (Y/n): ").strip().lower()
    if confirm == "" or confirm == "y":
        await run_pipeline(provider, model, api_key_env)
    else:
        print_colored(
            "\nOperation cancelled. Restart the program to try again.", "yellow"
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_colored("\n\nProgram interrupted by user. Exiting.", "yellow")
        sys.exit(0)
