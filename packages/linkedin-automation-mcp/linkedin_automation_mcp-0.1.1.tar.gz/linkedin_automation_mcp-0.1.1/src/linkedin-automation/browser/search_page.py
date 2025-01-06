from playwright.async_api import Page
import logging
from typing import List, Dict, Any
from browser.profile_page import ProfilePage

logger = logging.getLogger(__name__)

# Locators and constants
LOCATORS = {
    'PROFILE_CARD': '.jbMBcQpKNgyAzcNKZRnfSGydOUCvqJYidHppp',
    'HEADLINE': '.oTADryLUgiMDrgOUzFvMrgfyhayVgwHRk',
    'LOCATION': '.fNudNcxdGdiIrrwNWmOrvRbyvWHgpRzME',
    'CONNECT_BUTTON': "button:has-text('Connect')",
    'SEND_BUTTON': "button:has-text('Send')",
    'ADD_NOTE_BUTTON': "button:has-text('Add a note')",
    'NOTE_TEXTAREA': "textarea[name='message']",
    'NEXT_BUTTON': "button[aria-label='Next']"
}

TIMEOUTS = {
    'PAGE_LOAD': 2000,
    'BUTTON_WAIT': 2000,
    'NOTE_WAIT': 5000,
    'SEND_WAIT': 10000,
    'STANDARD': 1000
}

class SearchPage:
    """Handles LinkedIn search page interactions and connection requests."""
    
    def __init__(self, page: Page):
        self._page = page
        self._base_url = "https://www.linkedin.com/search/results/people"
        self._profile_page = ProfilePage(page)
        
    async def _navigate_to_search(self, search_query: str) -> None:
        """Navigate to LinkedIn search results for the given query."""
        try:
            await self._page.goto(f"{self._base_url}/?keywords={search_query}")
            await self._page.wait_for_timeout(TIMEOUTS['PAGE_LOAD'])
        except Exception as e:
            logger.error(f"Failed to navigate to search page: {str(e)}")
            raise

    async def _get_profile_info(self, button) -> Dict[str, str]:
        """Extract profile information from search result card."""
        try:
            profile_data = await button.evaluate(f"""
                (button) => {{
                    const card = button.closest('{LOCATORS["PROFILE_CARD"]}');
                    if (!card) return null;

                    const anchor = card.querySelector('a[href*="/in/"]');
                    const nameElement = anchor ? anchor.querySelector('img[alt]') : null;
                    const headlineElement = card.querySelector('{LOCATORS["HEADLINE"]}');
                    const locationElement = card.querySelector('{LOCATORS["LOCATION"]}');

                    return anchor ? {{
                        profileUrl: anchor.href.split('?')[0],
                        name: nameElement ? nameElement.alt.trim() : '',
                        headline: headlineElement ? headlineElement.textContent.trim() : '',
                        location: locationElement ? locationElement.textContent.trim() : ''
                    }} : null;
                }}
            """)

            if not profile_data:
                return self._get_empty_profile()

            return {
                **profile_data,
                'profileId': profile_data['profileUrl'].split('/in/')[1].split('/')[0]
            }

        except Exception as e:
            logger.error(f"Error extracting profile info: {str(e)}")
            return self._get_empty_profile()

    def _get_empty_profile(self) -> Dict[str, str]:
        """Return empty profile structure"""
        return {
            'profileUrl': '',
            'profileId': '',
            'name': '',
            'headline': '',
            'location': '',
        }

    async def _send_connection_request(self, button, custom_note: str = "") -> Dict[str, str]:
        """Send a connection request to a profile."""
        try:
            await button.click()
            await self._page.wait_for_timeout(TIMEOUTS['STANDARD'])
            
            if not custom_note:
                send_button = await self._page.wait_for_selector(LOCATORS['SEND_BUTTON'], timeout=TIMEOUTS['BUTTON_WAIT'])
                if not send_button:
                    raise ValueError("Could not find 'Send' button")
                await send_button.click()
                return {"status": "success"}

            add_note_button = await self._page.wait_for_selector(LOCATORS['ADD_NOTE_BUTTON'], timeout=TIMEOUTS['BUTTON_WAIT'])
            if not add_note_button:
                raise ValueError("Could not find 'Add a note' button")
            
            await add_note_button.click()
            await self._page.fill(LOCATORS['NOTE_TEXTAREA'], custom_note)
            await self._page.wait_for_timeout(TIMEOUTS['NOTE_WAIT'])
            
            send_button = await self._page.wait_for_selector(LOCATORS['SEND_BUTTON'], timeout=TIMEOUTS['BUTTON_WAIT'])
            if not send_button:
                raise ValueError("Could not find 'Send' button after adding note")
            
            await self._page.wait_for_timeout(TIMEOUTS['SEND_WAIT'])
            await send_button.click()
            return {"status": "success"}

        except Exception as e:
            logger.error(f"Error sending connection request: {str(e)}")
            raise

    async def send_connection_requests(
        self,
        search_query: str,
        max_connections: int,
        custom_note: str = "",
        user_profile_id: str = ""
    ) -> List[Dict[str, Any]]:
        """Search for profiles and send connection requests."""
        try:
            results = []
            sent_requests = 0

            if user_profile_id:
                user_info = await self.get_user_info(user_profile_id)
                logger.info(f"User info: {user_info}")
            
            await self._navigate_to_search(search_query)
            
            for _ in range(min(max_connections, 3)):
                connect_buttons = await self._page.query_selector_all(LOCATORS['CONNECT_BUTTON'])
                if not connect_buttons:
                    raise ValueError("No connect buttons found on page")
                    
                logger.info(f"Found {len(connect_buttons)} connect buttons on the page.")
                
                results, sent_requests = await self._process_connect_buttons(
                    connect_buttons, max_connections, custom_note, user_info if user_profile_id else "", 
                    results, sent_requests
                )
                
                if sent_requests >= max_connections:
                    return results

                if not await self._try_next_page():
                    break
            
            return results
            
        except Exception as e:
            logger.error(f"Error sending connection requests: {str(e)}")
            raise

    async def _process_connect_buttons(
        self, 
        connect_buttons, 
        max_connections: int, 
        custom_note: str,
        user_info: str,
        results: List[Dict[str, Any]],
        sent_requests: int
    ) -> tuple[List[Dict[str, Any]], int]:
        """Process connection buttons and send requests."""
        for button in connect_buttons[:max_connections]:
            try:
                profile_info = await self._get_profile_info(button)
                if not profile_info:
                    continue

                formatted_note = await self._format_custom_note(custom_note, profile_info, user_info)
                connection_result = await self._send_connection_request(button, formatted_note)
                
                results.append({
                    "status": connection_result["status"],
                    "profile": profile_info,
                    "note_sent": bool(formatted_note)
                })
                
                sent_requests += 1
                if sent_requests >= max_connections:
                    return results, sent_requests

                await self._page.wait_for_timeout(TIMEOUTS['STANDARD'])

            except Exception as e:
                logger.error(f"Error processing connection request: {str(e)}")
                raise

        return results, sent_requests

    async def _try_next_page(self) -> bool:
        """Attempt to navigate to next page of results."""
        next_button = await self._page.query_selector(LOCATORS['NEXT_BUTTON'])
        if not next_button:
            logger.info("No more pages to navigate.")
            return False

        logger.info("Navigating to the next page of search results.")
        await next_button.click()
        await self._page.wait_for_timeout(TIMEOUTS['PAGE_LOAD'])
        return True

    async def _format_custom_note(
        self, 
        custom_note: str, 
        profile_info: Dict[str, str],
        user_info: str
    ) -> str:
        """Format custom note with profile information."""
        if not custom_note:
            return ""

        try:
            return custom_note.format(
                name=profile_info.get('name', ''),
                headline=profile_info.get('headline', ''),
                location=profile_info.get('location', ''),
                user_info=user_info
            )
        except Exception as e:
            logger.warning(f"Failed to format custom note: {str(e)}")
            raise ValueError(f"Failed to format custom note: {str(e)}")