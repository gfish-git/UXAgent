import asyncio
import functools
import json
import logging
import os
import traceback

import click
from dotenv import load_dotenv

from ..agent import gpt
from ..executor.agentql_env import AgentQLUniversalAgent

from .model import AgentPolicy, HumanPolicy, OpenAIPolicy  # noqa  # noqa

# Website configurations
WEBSITE_CONFIGS = {}


def make_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


"""Legacy Selenium utilities removed in Browserbase-only mode."""


async def run_agentql_automation(persona_data: dict, intent: str, target_url: str, output: str, max_steps: int):
    """
    Run AgentQL universal web automation.
    This is your breakthrough feature - works on ANY website!
    """
    print(f"🚀 Starting AgentQL Universal Web Automation")
    print(f"   Target URL: {target_url}")
    print(f"   Persona: {type(persona_data).__name__} - {str(persona_data)[:100]}...")
    print(f"   Goal: {intent}")
    print("-" * 80)
    
    # Create output directory
    os.makedirs(output, exist_ok=True)
    
    # Prepare persona with goal
    persona_with_goal = {
        "description": persona_data,
        "goal": intent,
        "target_url": target_url
    }
    
    # Initialize AgentQL Universal Agent
    headless = os.environ.get("HEADLESS", "true").lower() == "true"
    agent = AgentQLUniversalAgent(headless=headless)
    
    try:
        # Run the automation
        print("🤖 Starting persona-based automation...")
        result = await agent.run_persona_task(persona_with_goal, target_url)
        
        if result["success"]:
            print("✅ Automation completed successfully!")
            print(f"   Steps executed: {result['total_steps']}")
            print(f"   Final URL: {result.get('final_data', {}).get('url', target_url)}")
            
            # Save results
            results_file = os.path.join(output, "agentql_results.json")
            with open(results_file, "w") as f:
                json.dump(result, f, indent=2, default=str)
            
            print(f"   Results saved to: {results_file}")
            
        else:
            print("❌ Automation failed:")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            
            # Save error details
            error_file = os.path.join(output, "agentql_error.json")
            with open(error_file, "w") as f:
                json.dump(result, f, indent=2, default=str)
    
    except Exception as e:
        print(f"💥 Critical error during automation: {e}")
        print(traceback.format_exc())
        
        # Save error details
        error_file = os.path.join(output, "agentql_critical_error.txt")
        with open(error_file, "w") as f:
            f.write(f"Critical Error: {e}\n\n")
            f.write(traceback.format_exc())
    
    print("\n🏁 AgentQL automation completed")


@click.command()
@click.option("--persona", type=str, help="Path to the persona file.", required=True)
@click.option("--output", type=str, help="Path to the output file.", required=True)
@click.option("--max-steps", type=int, help="Maximum steps to run.", default=50)
@click.option("--cookie", type=(str, str), help="Cookies to set.")
@click.option(
    "--record",
    is_flag=True,
    show_default=True,
    default=False,
    type=bool,
    help="Record the run.",
)
@click.option("--llm-provider", type=click.Choice(["openai", "aws"]), default="aws")
@click.option(
    "--target-url",
    type=str,
    required=True,
    help="Target URL to test with AgentQL+Browserbase",
)
@make_sync
async def main(
    persona: str,
    output: str,
    max_steps: int,
    cookie: tuple[str, str],
    record: bool,
    llm_provider: str,
    target_url: str,
):

    load_dotenv()
    # Enable INFO logs for our modules and common dependencies
    logging.basicConfig(level=logging.INFO)
    for name in list(logging.root.manager.loggerDict.keys()):
        if name.startswith((
            "simulated_web_agent",
            "src.simulated_web_agent",
            "agentql",
            "playwright",
        )):
            logging.getLogger(name).setLevel(logging.INFO)
    gpt.provider = llm_provider

    persona_info = json.load(open(persona))
    persona_data = persona_info["persona"]
    intent = persona_info["intent"]

    # Browserbase + AgentQL only
    await run_agentql_automation(persona_data, intent, target_url, output, max_steps)


if __name__ == "__main__":
    main()
