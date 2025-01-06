import logging
import sys
import subprocess
import os
from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

class LinkedInBrowser:
    def __init__(self):
        """Initialize browser-related attributes."""
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def _ensure_browser_install(self):
        """Ensure Playwright browsers are installed."""
        try:
            # Check if PLAYWRIGHT_BROWSERS_PATH is set
            browsers_path = os.getenv('PLAYWRIGHT_BROWSERS_PATH')
            if browsers_path and os.path.exists(browsers_path):
                logger.info(f"Using custom browser path: {browsers_path}")
                return

            # Try to install browsers
            logger.info("Installing Playwright browsers")
            result = subprocess.run(['playwright', 'install', 'chromium'], 
                                 capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.warning(f"Browser installation failed: {result.stderr}")
                logger.warning("Will attempt to proceed anyway as browsers might be installed")
            else:
                logger.info("Browser installation successful")
                
        except Exception as e:
            logger.warning(f"Error during browser installation: {str(e)}")
            logger.warning("Will attempt to proceed with browser launch")

    async def _ensure_browser(self) -> bool:
        """Ensure browser is initialized."""
        # Close any existing sessions
        await self._cleanup()
        
        try:
            # Ensure browsers are installed
            await self._ensure_browser_install()
            
            # Use the same configuration as our working direct test
            logger.info("Starting Playwright")
            self.playwright = await async_playwright().start()
            
            logger.info("Launching browser")
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                slow_mo=100
            )
            
            logger.info("Creating browser context")
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720}
            )
            
            logger.info("Creating new page")
            self.page = await self.context.new_page()
            
            logger.info("Browser session initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}")
            return False

    async def _cleanup(self):
        """Clean up browser context, browser, and Playwright instance."""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        finally:
            # Reset all browser-related instances after cleanup
            self.playwright = None
            self.browser = None
            self.context = None
            self.page = None

    async def initialize_browser(self) -> bool:
        """Initialize browser components for LinkedIn automation."""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,  # Set to True in production
                slow_mo=50  # Slows down operations to make them visible
            )
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            return True
        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}")
            await self._cleanup()
            raise
