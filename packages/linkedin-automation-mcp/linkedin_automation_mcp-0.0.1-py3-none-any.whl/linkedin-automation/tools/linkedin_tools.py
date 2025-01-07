from typing import Dict, Any, List
import logging
from browser.browser import LinkedInBrowser
from browser.login_page import LoginPage
from browser.profile_page import ProfilePage
from browser.search_page import SearchPage
from browser.feed_page import FeedPage
from .models import (
    ScrapePostsInput,
    SendConnectionInput,
    GetProfileInput,
    PostContentToLinkedinInput
)

logger = logging.getLogger(__name__)

class LinkedInTools:
    """Class handling LinkedIn tool implementations."""
    
    def __init__(self, email: str, password: str) -> None:
        """Initialize LinkedIn tools with credentials."""
        self.email = email
        self.password = password
        self.browser = LinkedInBrowser()
        self.login_page = None
        self.profile_page = None
        self.search_page = None
        self.feed_page = None

    async def _ensure_browser(self) -> bool:
        """Ensure browser is initialized and logged in."""
        try:
            await self.browser._ensure_browser()
            
            logger.info("Initializing pages")
            self.login_page = LoginPage(self.browser.page)
            self.profile_page = ProfilePage(self.browser.page)
            self.search_page = SearchPage(self.browser.page)
            self.feed_page = FeedPage(self.browser.page)
            
            # Login if needed
            if not await self.login_page.is_logged_in():
                login_success = await self.login_page.login(self.email, self.password)
                if not login_success:
                    raise Exception("Failed to log in to LinkedIn")
            
            logger.info("Browser session initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}")
            await self.cleanup()
            raise

    async def cleanup(self) -> None:
        """Clean up browser resources."""
        await self.browser._cleanup()
        self.login_page = None
        self.profile_page = None
        self.search_page = None
        self.feed_page = None

    async def scrape_posts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle LinkedIn post scraping."""
        try:
            input_data = ScrapePostsInput(**params)
            await self._ensure_browser()
            
            posts = await self.profile_page.scrape_linkedin_posts(
                input_data.profile_ids,
                input_data.max_posts
            )

            return {
                "content": [{
                    "type": "text",
                    "text": {
                        "success": True,
                        "posts": posts
                    }
                }]
            }

        except Exception as e:
            logger.error(f"Failed to scrape posts: {str(e)}")
            return {
                "content": [{
                    "type": "text",
                    "text": {
                        "success": False,
                        "error": str(e)
                    }
                }],
                "isError": True
            }
        finally:
            await self.cleanup()

    async def send_connections(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle LinkedIn connection requests."""
        try:
            input_data = SendConnectionInput(**params)
            await self._ensure_browser()
            
            results = await self.search_page.send_connection_requests(
                search_query=input_data.search_query,
                max_connections=input_data.max_connections,
                custom_note=input_data.custom_note,
                user_profile_id=input_data.user_profile_id
            )

            return {
                "content": [{
                    "type": "text",
                    "text": {
                        "success": True,
                        "results": results
                    }
                }]
            }

        except Exception as e:
            logger.error(f"Failed to send connection requests: {str(e)}")
            return {
                "content": [{
                    "type": "text",
                    "text": {
                        "success": False,
                        "error": str(e)
                    }
                }],
                "isError": True
            }
        finally:
            await self.cleanup()

    async def get_profile_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle LinkedIn profile information requests."""
        try:
            input_data = GetProfileInput(**params)
            await self._ensure_browser()
            
            profiles = []
            for profile_id in input_data.profile_ids:
                profile_info = await self.profile_page.get_linkedin_profile_info(profile_id)
                profiles.append(profile_info)

            return {
                "content": [{
                    "type": "text",
                    "text": {
                        "success": True,
                        "profiles": profiles
                    }
                }]
            }

        except Exception as e:
            logger.error(f"Failed to get profile info: {str(e)}")
            return {
                "content": [{
                    "type": "text",
                    "text": {
                        "success": False,
                        "error": str(e)
                    }
                }],
                "isError": True
            }
        finally:
            await self.cleanup()

    async def post_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle posting content to LinkedIn."""
        try:
            input_data = PostContentToLinkedinInput(**params)
            await self._ensure_browser()
            
            success = await self.feed_page.create_post(input_data.content)

            return {
                "content": [{
                    "type": "text",
                    "text": {
                        "success": success,
                        "message": "Post created successfully"
                    }
                }]
            }

        except Exception as e:
            logger.error(f"Failed to create post: {str(e)}")
            return {
                "content": [{
                    "type": "text",
                    "text": {
                        "success": False,
                        "error": str(e)
                    }
                }],
                "isError": True
            }
        finally:
            await self.cleanup() 