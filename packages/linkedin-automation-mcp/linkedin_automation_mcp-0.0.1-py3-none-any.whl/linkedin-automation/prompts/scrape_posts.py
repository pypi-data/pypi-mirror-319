from typing import Dict, Any

def get_prompt(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Return the scrape posts prompt structure."""
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Scrape posts from LinkedIn profile: {arguments.get('profile_url')}"
                }
            }
        ]
    }

def get_prompt_info() -> Dict[str, Any]:
    """Return the prompt metadata."""
    return {
        "name": "scrape-posts",
        "description": "Scrape posts from LinkedIn profile",
        "arguments": [
            { "name": "profile_url", "description": "URL of the LinkedIn profile to scrape posts from", "required": True }
        ]
    }