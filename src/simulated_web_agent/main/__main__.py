import asyncio
import base64
import functools
import json
import logging
import os
import signal
import subprocess
import time
import traceback

import click
import gymnasium as gym
import requests
import selenium
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from ..agent.gpt import chat
from ..agent import gpt
from ..executor import amazon_recipes, google_flights_recipes, onestopshop_recipes, bruvi_recipes
from ..executor.env import (
    Browser,  # noqa
    SeleniumEnv,  # noqa
)
# Add AgentQL imports
from ..executor.agentql_env import AgentQLUniversalAgent

from .model import AgentPolicy, HumanPolicy, OpenAIPolicy  # noqa  # noqa

# Website configurations
WEBSITE_CONFIGS = {
    "amazon": {
        "start_url": "https://www.amazon.com",
        "recipes": amazon_recipes.recipes,
        "solve_captcha": True,
    },
    "bruvi": {
        "start_url": "https://bruvi.com",
        "recipes": bruvi_recipes.recipes,
        "solve_captcha": False,
    },
    "google_flights": {
        "start_url": "https://www.google.com/flights",
        "recipes": google_flights_recipes.recipes,
        "solve_captcha": False,
    },
    # Universal AgentQL configuration - works on ANY website!
    "universal": {
        "start_url": None,  # Will be set dynamically
        "recipes": None,    # No recipes needed!
        "solve_captcha": False,
    },
}


def make_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


def solve_captcha(browser: Browser):
    try:
        while True:
            image = browser.driver.find_element(
                By.CSS_SELECTOR,
                "body > div > div.a-row.a-spacing-double-large > div.a-section > div > div > form > div.a-row.a-spacing-large > div > div > div.a-row.a-text-center > img",
            ).get_attribute("src")
            image_file = requests.get(image).content
            image_file = base64.b64encode(image_file).decode("utf-8")
            resp = chat(
                [
                    {
                        "role": "system",
                        "content": 'You are an OCR expert designed to solve CAPTCHAs. You will respond in a single JSON format: {"text": "The text in the image"}. DO NOT include any other text. E.g. {"text": "123456"}',
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_file,
                                },
                            },
                            {"type": "text", "text": "What’s in this image?"},
                        ],
                    },
                ],
                model="large",
                json_mode=True,
            )
            print(resp)
            text = json.loads(resp)["text"]
            input_element = browser.driver.find_element(
                By.CSS_SELECTOR, "#captchacharacters"
            )
            # input_element.send_keys(text)
            # input_element.send_keys(Keys.ENTER)
            for keys in text:
                input_element.send_keys(keys)
                time.sleep(0.2)
            input_element.send_keys(Keys.ENTER)
            time.sleep(1)
    except selenium.common.exceptions.NoSuchElementException:
        # no more captcha
        pass
    return


recording_process = None


def start_recording(output_video: str):
    # screencapture -D 1 -v output.mp4
    # start the background process
    global recording_process
    recording_process = subprocess.Popen(
        ["screencapture", "-D", "2", "-v", output_video],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return recording_process


def stop_recording(result=None):
    # process.terminate()
    # send Ctrl-C=
    time.sleep(3)
    global recording_process
    recording_process.send_signal(signal.SIGINT)


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
    "--website",
    type=click.Choice(["amazon", "bruvi", "google_flights", "universal"]),
    default="amazon",
    help="Which website to test (amazon, bruvi, google_flights, or universal for AgentQL)"
)
@click.option(
    "--target-url",
    type=str,
    help="Target URL for universal AgentQL mode (required when using --website universal)",
    default=None
)
@click.option(
    "--use-agentql",
    is_flag=True,
    show_default=True,
    default=False,
    type=bool,
    help="Use AgentQL for universal web automation (works on any website)",
)
@make_sync
async def main(
    persona: str,
    output: str,
    max_steps: int,
    cookie: tuple[str, str],
    record: bool,
    llm_provider: str,
    website: str,
    target_url: str,
    use_agentql: bool,
):

    load_dotenv()
    logging.basicConfig()
    loggers = [
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("simulated_web_agent")
    ]
    for logger in loggers:
        logger.setLevel(logging.INFO)
    gpt.provider = llm_provider

    persona_info = json.load(open(persona))
    persona_data = persona_info["persona"]
    intent = persona_info["intent"]

    # Check if using AgentQL universal mode
    if use_agentql or website == "universal":
        if not target_url:
            raise click.ClickException("--target-url is required when using AgentQL universal mode")
        
        # Run AgentQL universal automation
        await run_agentql_automation(persona_data, intent, target_url, output, max_steps)
        return

    policy = AgentPolicy(persona_data, intent, output)

    # Get website configuration
    website_config = WEBSITE_CONFIGS[website]

    if record:
        env = gym.make(
            "SeleniumEnv-v0",
            start_url=website_config["start_url"],
            headless=os.environ.get("HEADLESS", "true").lower() == "true",
            recipes=website_config["recipes"],
            start_callback=lambda x: (
                solve_captcha(x) if website_config["solve_captcha"] else None,
                start_recording(f"{output}/recording.mp4"),
            ),
            end_callback=lambda x: stop_recording,
        )
    else:
        env = gym.make(
            "SeleniumEnv-v0",
            start_url=website_config["start_url"],
            headless=os.environ.get("HEADLESS", "true").lower() == "true",
            recipes=website_config["recipes"],
            start_callback=solve_captcha if website_config["solve_captcha"] else lambda x: None,
            end_callback=lambda x: print("end with ", x),
        )
    num_steps = 0
    observation, info = env.reset()

    try:
        if cookie:
            # save cookie
            with open(f"{output}/cookie.json", "w") as f:
                json.dump(cookie, f)
            env.browser.driver.add_cookie({"name": cookie[0], "value": cookie[1]})

        while True:
            if not observation["error_message"]:
                del observation["error_message"]
            # print(observation["page"])
            clickables = observation["clickables"]
            # print("clickables:", clickables)
            action = await policy.forward(observation, clickables)
            print(f"Taking action {action}")
            observation, reward, terminated, truncated, info = env.step(action)
            print("-" * 50)
            if terminated:
                break
            num_steps += 1
            if num_steps >= max_steps:
                print(f"Reached max steps of {max_steps}, stopping.")
                (policy.run_path / "failed.json").write_text("reached max steps")
                break
    except Exception:
        print(traceback.format_exc())

        (policy.run_path / "error.txt").write_text(traceback.format_exc())
    finally:
        await policy.close()
        env.close()


if __name__ == "__main__":
    main()
