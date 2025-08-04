import asyncio
import json
import logging
import os
import time
import traceback
from typing import Any, Dict, List, Optional, Union

import agentql
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from playwright_stealth import stealth_async

# Import existing components
from ..agent import context


class AgentQLEnv:
    """
    AgentQL-powered environment for universal web automation.
    This replaces manual recipes with AI-powered semantic understanding.
    """
    
    def __init__(self, 
                 headless: bool = True,
                 timeout: int = 30000,
                 cache_schemas: bool = True):
        self.headless = headless
        self.timeout = timeout
        self.cache_schemas = cache_schemas
        self.schema_cache = {}  # Your innovation: cache learned schemas
        
        # Playwright/AgentQL setup
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.agentql_page = None
        
        # State tracking
        self.current_url = ""
        self.step_count = 0
        self.max_steps = 50
        
        self.logger = logging.getLogger(__name__)
    
    async def setup(self):
        """Initialize the AgentQL environment"""
        try:
            self.playwright = await async_playwright().start()
            
            # Launch browser with stealth mode
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions',
                    '--disable-plugins-discovery',
                    '--start-maximized'
                ]
            )
            
            # Create context with realistic settings
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            )
            
            # Create page and apply stealth
            self.page = await self.context.new_page()
            await stealth_async(self.page)
            
            # Wrap with AgentQL for AI-powered automation
            self.agentql_page = agentql.wrap(self.page)
            
            self.logger.info("AgentQL environment initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to setup AgentQL environment: {e}")
            raise
    
    async def navigate_to(self, url: str) -> Dict[str, Any]:
        """Navigate to a URL and prepare for automation"""
        try:
            self.current_url = url
            self.step_count = 0
            
            self.logger.info(f"Navigating to: {url}")
            
            # Navigate with timeout
            await self.agentql_page.goto(url, timeout=self.timeout)
            await self.agentql_page.wait_for_load_state('networkidle')
            
            # Get page info
            title = await self.agentql_page.title()
            current_url = self.agentql_page.url
            
            self.logger.info(f"Successfully loaded: {title}")
            
            return {
                "success": True,
                "title": title,
                "url": current_url,
                "step": self.step_count
            }
            
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "step": self.step_count
            }
    
    async def execute_action(self, natural_language_instruction: str) -> Dict[str, Any]:
        """
        Execute an action using natural language instruction.
        This is where AgentQL shines - no need for manual CSS selectors!
        """
        try:
            self.step_count += 1
            
            if self.step_count > self.max_steps:
                return {
                    "success": False,
                    "error": "Maximum steps exceeded",
                    "step": self.step_count
                }
            
            # Validate input parameter
            if isinstance(natural_language_instruction, dict):
                if 'instruction' in natural_language_instruction:
                    instruction_str = str(natural_language_instruction['instruction'])
                elif 'action' in natural_language_instruction:
                    instruction_str = str(natural_language_instruction['action'])
                else:
                    instruction_str = str(natural_language_instruction)
                self.logger.warning(f"Received dictionary instead of string, converted: {instruction_str}")
            elif not isinstance(natural_language_instruction, str):
                instruction_str = str(natural_language_instruction)
                self.logger.warning(f"Received {type(natural_language_instruction)} instead of string, converted: {instruction_str}")
            else:
                instruction_str = natural_language_instruction
            
            self.logger.info(f"Step {self.step_count}: {instruction_str}")
            
            # Check if we have cached schema for this type of action
            cache_key = f"{self.current_url}:{instruction_str}"
            
            if self.cache_schemas and cache_key in self.schema_cache:
                self.logger.info("Using cached schema for faster execution")
                # Future enhancement: use cached schema for faster execution
            
            # More intelligent action parsing
            instruction_lower = instruction_str.lower()
            
            try:
                # Use AgentQL to execute the action based on content analysis
                if any(keyword in instruction_lower for keyword in ["click", "tap", "press", "select", "choose"]):
                    # Handle click-like actions
                    await self._handle_click_action(instruction_str)
                elif any(keyword in instruction_lower for keyword in ["fill", "type", "enter", "input", "write"]):
                    # Handle input actions
                    await self._handle_input_action(instruction_str)
                elif any(keyword in instruction_lower for keyword in ["select", "dropdown", "choose option"]):
                    # Handle select actions
                    await self._handle_select_action(instruction_str)
                elif any(keyword in instruction_lower for keyword in ["scroll", "navigate", "go to"]):
                    # Handle navigation actions
                    await self._handle_navigation_action(instruction_str)
                else:
                    # Generic action handling
                    self.logger.info(f"Using generic action handler for: {instruction_str}")
                    await self._handle_generic_action(instruction_str)
                
                # Wait for any navigation or dynamic content
                await self.agentql_page.wait_for_timeout(1500)
                
            except Exception as action_error:
                self.logger.error(f"Action execution failed: {action_error}")
                # Try a more generic approach if specific action fails
                try:
                    self.logger.info("Attempting fallback with generic action handler")
                    await self._handle_generic_action(instruction_str)
                    await self.agentql_page.wait_for_timeout(1000)
                except Exception as fallback_error:
                    self.logger.error(f"Fallback action also failed: {fallback_error}")
                    raise action_error  # Raise the original error
            
            # Get current state
            title = await self.agentql_page.title()
            current_url = self.agentql_page.url
            
            # Cache successful actions for future optimization
            if self.cache_schemas:
                self.schema_cache[cache_key] = {
                    "action": instruction_str,
                    "success": True,
                    "timestamp": time.time()
                }
            
            return {
                "success": True,
                "action": instruction_str,
                "title": title,
                "url": current_url,
                "step": self.step_count
            }
            
        except Exception as e:
            self.logger.error(f"Action failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": natural_language_instruction,
                "step": self.step_count
            }
    
    async def extract_data(self, query) -> Dict[str, Any]:
        """
        Extract structured data using AgentQL's natural language queries.
        This replaces manual BeautifulSoup parsing!
        """
        try:
            self.logger.info(f"Extracting data: {query}")
            
            # Convert string query to proper AgentQL format
            if isinstance(query, str):
                # Clean the query description for AgentQL format
                import re
                clean_query = query.lower().replace(" ", "_").replace("-", "_")
                clean_query = re.sub(r'[^a-zA-Z0-9_]', '', clean_query)
                
                if not clean_query:
                    clean_query = "page_data"
                
                # Use correct AgentQL syntax for data extraction
                agentql_query = f"""
                {{
                    {clean_query}
                }}
                """
            else:
                # Assume it's already in correct format
                agentql_query = query
            
            self.logger.info(f"AgentQL data query: {agentql_query}")
            
            # Execute the query
            response = await self.agentql_page.query_data(agentql_query)
            
            self.logger.info(f"Extracted data successfully")
            
            return {
                "success": True,
                "data": response,
                "query": query,
                "step": self.step_count
            }
            
        except Exception as e:
            self.logger.error(f"Data extraction failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "step": self.step_count
            }
    
    async def _handle_click_action(self, instruction):
        """Handle clicking actions with AgentQL"""
        # Validate and convert instruction parameter
        if isinstance(instruction, dict):
            # If instruction is a dict, try to extract meaningful information
            if 'instruction' in instruction:
                instruction_str = str(instruction['instruction'])
            elif 'text' in instruction:
                instruction_str = str(instruction['text'])
            elif 'action' in instruction:
                instruction_str = str(instruction['action'])
            else:
                # Convert dict to string representation
                instruction_str = str(instruction)
            self.logger.warning(f"Received dictionary instead of string for instruction, converted: {instruction_str}")
        elif not isinstance(instruction, str):
            # Convert any other type to string
            instruction_str = str(instruction)
            self.logger.warning(f"Received {type(instruction)} instead of string for instruction, converted: {instruction_str}")
        else:
            instruction_str = instruction
        
        self.logger.info(f"Processing click action: {instruction_str}")
        
        # Extract what to click from the instruction
        element_description = instruction_str.replace("click", "").replace("on", "").strip()
        
        # Clean up the description to avoid query syntax issues
        element_description = element_description.replace('"', '').replace("'", "").replace(":", "")
        
        # Handle empty descriptions
        if not element_description:
            raise Exception("No element description found in click instruction")
        
        self.logger.info(f"Looking for element: {element_description}")
        
        # Use AgentQL to find and click the element using correct syntax
        self.logger.info(f"Looking for element: {element_description}")
        
        try:
            # Convert element description to AgentQL format
            # Clean the description to make it suitable for AgentQL
            clean_description = element_description.lower().replace(" ", "_").replace("-", "_")
            # Remove any non-alphanumeric characters except underscores
            import re
            clean_description = re.sub(r'[^a-zA-Z0-9_]', '', clean_description)
            
            if not clean_description:
                clean_description = "clickable_element"
            
            # Use AgentQL's correct syntax format
            query = f"""
            {{
                {clean_description}
            }}
            """
            
            self.logger.info(f"AgentQL query: {query}")
            elements = await self.agentql_page.query_elements(query)
            
            if elements and hasattr(elements, clean_description):
                target_element = getattr(elements, clean_description)
                if target_element:
                    await target_element.click()
                    self.logger.info(f"Successfully clicked element: {element_description}")
                else:
                    raise Exception(f"Element {clean_description} was None")
            else:
                # Try alternative approach with generic button/link query
                try:
                    # Alternative: query for common clickable elements
                    alt_query = """
                    {{
                        clickable_btn
                    }}
                    """
                    alt_elements = await self.agentql_page.query_elements(alt_query)
                    if alt_elements and hasattr(alt_elements, 'clickable_btn') and alt_elements.clickable_btn:
                        await alt_elements.clickable_btn.click()
                        self.logger.info(f"Successfully clicked element using alternative query: {element_description}")
                    else:
                        # Try one more alternative with get_by_prompt
                        prompt_element = await self.agentql_page.get_by_prompt(element_description)
                        if prompt_element:
                            await prompt_element.click()
                            self.logger.info(f"Successfully clicked element using get_by_prompt: {element_description}")
                        else:
                            raise Exception(f"Could not find element: {element_description}")
                except Exception as fallback_error:
                    self.logger.error(f"Alternative query also failed: {fallback_error}")
                    raise Exception(f"Could not find element: {element_description}")
        except Exception as e:
            self.logger.error(f"Click action failed for '{element_description}': {e}")
            raise

    async def _handle_input_action(self, instruction):
        """Handle input/typing actions with AgentQL"""
        # Validate and convert instruction parameter  
        if isinstance(instruction, dict):
            if 'instruction' in instruction:
                instruction_str = str(instruction['instruction'])
            elif 'text' in instruction:
                instruction_str = str(instruction['text'])
            else:
                instruction_str = str(instruction)
            self.logger.warning(f"Received dictionary instead of string for instruction, converted: {instruction_str}")
        elif not isinstance(instruction, str):
            instruction_str = str(instruction)
            self.logger.warning(f"Received {type(instruction)} instead of string for instruction, converted: {instruction_str}")
        else:
            instruction_str = instruction
            
        self.logger.info(f"Processing input action: {instruction_str}")
        
        # Parse the instruction to extract field and value
        if "fill" in instruction_str:
            parts = instruction_str.split("with")
            field_desc = parts[0].replace("fill", "").strip()
            value = parts[1].strip() if len(parts) > 1 else ""
            
            # Clean up the description
            field_desc = field_desc.replace('"', '').replace("'", "").replace(":", "")
            
            if not field_desc:
                raise Exception("No field description found in fill instruction")
                
            self.logger.info(f"Looking for input field: {field_desc}, value: {value}")
            
            # Clean the field description for AgentQL format
            import re
            clean_field_desc = field_desc.lower().replace(" ", "_").replace("-", "_")
            clean_field_desc = re.sub(r'[^a-zA-Z0-9_]', '', clean_field_desc)
            
            if not clean_field_desc:
                clean_field_desc = "input_field"
            elif not clean_field_desc.endswith(('_field', '_box', '_input')):
                clean_field_desc += "_field"
            
            # Use correct AgentQL syntax
            query = f"""
            {{
                {clean_field_desc}
            }}
            """
            
            try:
                self.logger.info(f"AgentQL input query: {query}")
                elements = await self.agentql_page.query_elements(query)
                if elements and hasattr(elements, clean_field_desc):
                    input_element = getattr(elements, clean_field_desc)
                    if input_element:
                        await input_element.fill(value)
                        self.logger.info(f"Successfully filled field '{field_desc}' with '{value}'")
                    else:
                        raise Exception(f"Input element {clean_field_desc} was None")
                else:
                    # Try alternative query with generic input
                    alt_query = """
                    {
                        input_box
                    }
                    """
                    alt_elements = await self.agentql_page.query_elements(alt_query)
                    if alt_elements and hasattr(alt_elements, 'input_box') and alt_elements.input_box:
                        await alt_elements.input_box.fill(value)
                        self.logger.info(f"Successfully filled field using alternative query: {field_desc}")
                    else:
                        # Try get_by_prompt as last resort
                        prompt_element = await self.agentql_page.get_by_prompt(f"input field for {field_desc}")
                        if prompt_element:
                            await prompt_element.fill(value)
                            self.logger.info(f"Successfully filled field using get_by_prompt: {field_desc}")
                        else:
                            raise Exception(f"Could not find input field: {field_desc}")
            except Exception as e:
                self.logger.error(f"Input action failed for '{field_desc}': {e}")
                raise
        else:
            raise Exception(f"Unsupported input instruction format: {instruction_str}")

    async def _handle_select_action(self, instruction):
        """Handle select dropdown actions with AgentQL"""
        # Validate and convert instruction parameter
        if isinstance(instruction, dict):
            if 'instruction' in instruction:
                instruction_str = str(instruction['instruction'])
            else:
                instruction_str = str(instruction)
            self.logger.warning(f"Received dictionary instead of string for instruction, converted: {instruction_str}")
        elif not isinstance(instruction, str):
            instruction_str = str(instruction)
            self.logger.warning(f"Received {type(instruction)} instead of string for instruction, converted: {instruction_str}")
        else:
            instruction_str = instruction
            
        self.logger.info(f"Processing select action: {instruction_str}")
        
        # TODO: Implement select dropdown handling
        # For now, treat as a click action
        await self._handle_click_action(instruction_str)

    async def _handle_generic_action(self, instruction):
        """Handle any other action types"""
        # Validate and convert instruction parameter
        if isinstance(instruction, dict):
            if 'instruction' in instruction:
                instruction_str = str(instruction['instruction'])
            else:
                instruction_str = str(instruction)
            self.logger.warning(f"Received dictionary instead of string for instruction, converted: {instruction_str}")
        elif not isinstance(instruction, str):
            instruction_str = str(instruction)
            self.logger.warning(f"Received {type(instruction)} instead of string for instruction, converted: {instruction_str}")
        else:
            instruction_str = instruction
            
        self.logger.info(f"Processing generic action: {instruction_str}")
        
        # For now, try to parse as a click action
        await self._handle_click_action(instruction_str)
    
    async def _handle_navigation_action(self, instruction):
        """Handle navigation actions like scroll, go to URL, etc."""
        # Validate and convert instruction parameter
        if isinstance(instruction, dict):
            if 'instruction' in instruction:
                instruction_str = str(instruction['instruction'])
            else:
                instruction_str = str(instruction)
            self.logger.warning(f"Received dictionary instead of string for instruction, converted: {instruction_str}")
        elif not isinstance(instruction, str):
            instruction_str = str(instruction)
            self.logger.warning(f"Received {type(instruction)} instead of string for instruction, converted: {instruction_str}")
        else:
            instruction_str = instruction
            
        self.logger.info(f"Processing navigation action: {instruction_str}")
        
        instruction_lower = instruction_str.lower()
        
        if "scroll" in instruction_lower:
            if "down" in instruction_lower:
                await self.agentql_page.evaluate("window.scrollBy(0, 500)")
                self.logger.info("Scrolled down")
            elif "up" in instruction_lower:
                await self.agentql_page.evaluate("window.scrollBy(0, -500)")
                self.logger.info("Scrolled up")
            else:
                # Default scroll down
                await self.agentql_page.evaluate("window.scrollBy(0, 300)")
                self.logger.info("Scrolled (default down)")
        elif "navigate" in instruction_lower or "go to" in instruction_lower:
            # For now, treat as a click action (navigate by clicking links)
            await self._handle_click_action(instruction_str)
        else:
            # Default to click action
            await self._handle_click_action(instruction_str)
    
    async def get_page_info(self) -> Dict[str, Any]:
        """Get current page information"""
        try:
            title = await self.agentql_page.title()
            url = self.agentql_page.url
            
            # Extract key page elements using AgentQL
            page_elements_query = {
                "headings": "all headings on the page",
                "buttons": "all clickable buttons", 
                "links": "all navigation links",
                "forms": "all input forms"
            }
            
            elements = await self.agentql_page.query_data(page_elements_query)
            
            return {
                "title": title,
                "url": url,
                "elements": elements,
                "step": self.step_count
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get page info: {e}")
            return {"error": str(e)}
    
    async def cleanup(self):
        """Clean up resources"""
        try:
            if self.agentql_page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
                
            self.logger.info("AgentQL environment cleaned up")
            
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")


class AgentQLUniversalAgent:
    """
    Universal web agent that can work on ANY website without manual recipes.
    This is your competitive advantage!
    """
    
    def __init__(self, headless: bool = True):
        self.env = AgentQLEnv(headless=headless)
        self.logger = logging.getLogger(__name__)
    
    async def run_persona_task(self, persona: Dict[str, Any], target_url: str) -> Dict[str, Any]:
        """
        Run a persona-based task on any website using AgentQL.
        This replaces your manual recipe approach with universal automation.
        """
        try:
            await self.env.setup()
            
            # Navigate to target website
            nav_result = await self.env.navigate_to(target_url)
            if not nav_result["success"]:
                return nav_result
            
            # Extract persona goal and preferences
            goal = persona.get("goal", "Browse and interact with the website")
            preferences = persona.get("preferences", {})
            
            self.logger.info(f"Running persona task: {goal}")
            
            # Convert goal into actionable steps using AgentQL
            steps = await self._generate_action_steps(goal, preferences)
            
            results = []
            for step in steps:
                result = await self.env.execute_action(step)
                results.append(result)
                
                if not result["success"]:
                    self.logger.warning(f"Step failed: {step}")
                    # Continue with other steps
            
            # Extract final results
            final_data = await self.env.extract_data("summary of actions taken and current page state")
            
            return {
                "success": True,
                "persona": persona,
                "url": target_url,
                "steps_executed": results,
                "final_data": final_data,
                "total_steps": len(steps)
            }
            
        except Exception as e:
            self.logger.error(f"Persona task failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "persona": persona,
                "url": target_url
            }
        finally:
            await self.env.cleanup()
    
    async def _generate_action_steps(self, goal: str, preferences: Dict[str, Any]) -> List[str]:
        """
        Generate action steps from natural language goal.
        This could be enhanced with GPT to break down complex goals.
        """
        # Check if this is an Apple Store or AirPods related goal
        if "airpods" in goal.lower() or "apple" in goal.lower():
            return [
                "scroll down to see page content",
                "click on AirPods link or navigate to AirPods",
                "browse available AirPods models",
                "select a suitable AirPods model",
                "click Buy button or Add to Bag button",
                "proceed to cart or bag"
            ]
        elif "coffee" in goal.lower() or "buy" in goal.lower():
            return [
                "scroll down to see page content",
                "click on Shop button or Get Bruvi button",
                "look for Bruvi Subscription Bundle",
                "click on the subscription bundle offer",
                "add to cart",
                "view cart"
            ]
        elif "browse" in goal.lower():
            return [
                "scroll down to see page content",
                "click on interesting links",
                "explore navigation menu"
            ]
        else:
            # Generic exploration
            return [
                "scroll down to explore the page",
                "identify main navigation elements",
                "explore primary content areas",
                "interact with key features"
            ] 