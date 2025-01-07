from playwright.async_api import Page
import asyncio
from typing import List, Union
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class ProfilePage:
    """Handles LinkedIn profile page interactions and post scraping."""
    
    def __init__(self, page: Page):
        self._page = page
        self._base_url = "https://www.linkedin.com/in"

    async def _navigate_to_profile_activity(self, linkedin_profile_id: str) -> None:
        """Navigate to a specific LinkedIn profile's activity page."""
        try:
            await self._page.goto(
                f"{self._base_url}/{linkedin_profile_id}/recent-activity/all/",
                timeout=60000
            )
        except Exception as e:
            logger.error(f"Failed to navigate to profile '{linkedin_profile_id}': {str(e)}")
            raise

    async def _scroll_page(self, scrolls: int = 2) -> None:
        """Scroll the page to load more content with improved handling."""
        try:
            previous_height = 0
            for _ in range(scrolls):
                # Get current scroll height
                current_height = await self._page.evaluate("document.body.scrollHeight")
                
                # If height hasn't changed, we've reached the bottom
                if current_height == previous_height:
                    break
                    
                await self._page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)  # Wait for content to load
                
                # Update previous height
                previous_height = current_height
                
            # Final wait for any remaining content
            await asyncio.sleep(2)
        except Exception as e:
            logger.error(f"Error while scrolling: {str(e)}")
            raise

    def _parse_html_content(self, page_source: str) -> List[BeautifulSoup]:
        """Parse HTML content to find post containers."""
        try:
            linkedin_soup = BeautifulSoup(page_source, "lxml")
            return [
                container
                for container in linkedin_soup.find_all(
                    "div", {"class": "feed-shared-update-v2"}
                )
                if "activity" in container.get("data-urn", "")
            ]
        except Exception as e:
            logger.error(f"Error parsing HTML content: {str(e)}")
            raise

    def _get_post_content(self, container: BeautifulSoup) -> str:
        """Extract post content from a container."""
        try:
            element = container.find("div", {"class": "update-components-text"})
            return element.text.strip() if element else ""
        except Exception as e:
            logger.error(f"Error extracting post content: {str(e)}")
            return ""

    def _get_timestamp(self, container) -> str:
        """Extract timestamp from the post container."""
        try:
            timestamp_element = container.find('time', {'class': 'artdeco-entity-lockup__caption'})
            return timestamp_element.get_text().strip() if timestamp_element else ""
        except Exception as e:
            logger.error(f"Error extracting timestamp: {str(e)}")
            return ""

    def _get_profile_name(self, page_source: str) -> str:
        """Extract profile name from the page content."""
        try:
            soup = BeautifulSoup(page_source, "lxml")
            name_element = soup.find('h1', {'class': 'XIEcXyPwYVMBFQidDozxmUdjjnWOjbHrDBnxmCNkg'})
            if not name_element:
                raise ValueError("Name element not found on page")
            return name_element.text.strip()
        except Exception as e:
            logger.error(f"Error extracting profile name: {str(e)}")
            raise

    def _get_headline(self, page_source: str) -> str:
        """Extract headline from the page content."""
        try:
            soup = BeautifulSoup(page_source, "lxml")
            headline_element = soup.find('div', {'class': 'text-body-medium break-words'})
            if not headline_element:
                raise ValueError("Headline element not found on page")
            return headline_element.text.strip()
        except Exception as e:
            logger.error(f"Error extracting headline: {str(e)}")
            raise

    def _get_location(self, page_source: str) -> str:
        """Extract location from the page content."""
        try:
            soup = BeautifulSoup(page_source, "lxml")
            location_container = soup.find('div', {'class': 'mt2'})
            if not location_container:
                raise ValueError("Location container not found")
                
            location_element = location_container.find(
                'span', {'class': 'text-body-small inline t-black--light break-words'}
            )
            if not location_element:
                raise ValueError("Location element not found")
            
            return location_element.text.strip()
        except Exception as e:
            logger.error(f"Error extracting location: {str(e)}")
            raise

    def _get_about(self, page_source: str) -> str:
        """Extract about section content from the page content."""
        try:
            soup = BeautifulSoup(page_source, "lxml")
            # Look for the div with the about text content
            about_element = soup.find('div', {'class': 'glDZdGhAxCZVKtyvSLjKQDzzNawEZsFwxVM'})
            if not about_element:
                raise ValueError("About section not found")
            return about_element.text.strip()
        except Exception as e:
            logger.error(f"Error extracting about section: {str(e)}")
            raise

    def _get_profile_info(self, page_source: str) -> dict:
        """Extract basic profile information from the page content."""
        try:
            return {
                "name": self._get_profile_name(page_source),
                "headline": self._get_headline(page_source),
                "location": self._get_location(page_source),
                "about": self._get_about(page_source)
            }
        except Exception as e:
            logger.error(f"Error extracting profile info: {str(e)}")
            return {}

    async def scrape_linkedin_posts(self, linkedin_profile_ids: Union[str, List[str]], max_posts: int = 5) -> List[dict]:
        """Scrape posts from LinkedIn profiles with improved error handling and rate limiting."""
        profile_ids = [linkedin_profile_ids] if isinstance(linkedin_profile_ids, str) else linkedin_profile_ids
        all_posts = []

        for profile_id in profile_ids:
            try:
                logger.info(f"Starting to scrape profile: {profile_id}")
                
                # Add rate limiting between profiles
                if len(all_posts) > 0:
                    await asyncio.sleep(3)  # Delay between profiles
                    
                await self._navigate_to_profile_activity(profile_id)
                
                # Wait for content to load
                try:
                    await self._page.wait_for_selector(
                        'div.feed-shared-update-v2',
                        timeout=30000
                    )
                except Exception as e:
                    logger.error(f"No posts found for profile {profile_id}: {str(e)}")
                    continue
                    
                await self._scroll_page()
                
                page_content = await self._page.content()
                containers = self._parse_html_content(page_content)
                
                profile_posts = [
                    {
                        "profile_id": profile_id,
                        "content": self._get_post_content(container),
                        "timestamp": self._get_timestamp(container)
                    }
                    for container in containers[:max_posts]
                    if self._get_post_content(container)
                ]
                
                all_posts.extend(profile_posts)
                logger.info(f"Successfully scraped {len(profile_posts)} posts from {profile_id}")
                logger.info(f"All posts: {all_posts}")
                
            except Exception as e:
                logger.error(f"Error scraping profile {profile_id}: {str(e)}")
                continue
                
        return all_posts 
    
    async def _navigate_to_profile_page(self, linkedin_profile_id: str) -> None:
        """Navigate directly to a LinkedIn profile page."""
        try:
            profile_url = f"{self._base_url}/{linkedin_profile_id}/"
            logger.info(f"Navigating to profile: {profile_url}")
            await self._page.goto(
                profile_url,
                timeout=60000
            )
            # Wait for the main profile content to load
            await self._page.wait_for_selector('h1.inline', timeout=10000)
        except Exception as e:
            logger.error(f"Failed to navigate to profile '{linkedin_profile_id}': {str(e)}")
            raise

    async def get_linkedin_profile_info(self, linkedin_profile_id: str) -> dict:
        """Get basic profile information."""
        try:
            # Use the new navigation method instead of _navigate_to_profile
            await self._navigate_to_profile_page(linkedin_profile_id)
            page_content = await self._page.content()
            
            # Debug logging
            logger.info(f"Page URL: {self._page.url}")
            logger.info("First 500 chars of page content:")
            logger.info(page_content[:500])
            
            return self._get_profile_info(page_content)
        except Exception as e:
            logger.error(f"Failed to get profile info for {linkedin_profile_id}: {str(e)}")
            raise