from typing import Dict, Any, List
from . import generate_post, research_and_create_linkedin_post, send_connection_requests, get_profile_info, scrape_posts, scrape_content_and_post_to_linkedin

AVAILABLE_PROMPTS = {
    "generate-post": generate_post,
    "research-and-create-linkedin-post": research_and_create_linkedin_post,
    "send-connections": send_connection_requests,
    "get-profile-info": get_profile_info,
    "scrape-posts": scrape_posts,
    "scrape-content-and-post-to-linkedin": scrape_content_and_post_to_linkedin,
}

def list_prompts() -> Dict[str, List[Dict[str, Any]]]:
    """Return a list of all available prompts and their metadata."""
    return {
        "prompts": [
            prompt.get_prompt_info()
            for prompt in AVAILABLE_PROMPTS.values()
        ]
    }

def get_prompt(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Get a specific prompt by name with the given arguments."""
    if name not in AVAILABLE_PROMPTS:
        raise ValueError(f"Unknown prompt: {name}")
    
    return AVAILABLE_PROMPTS[name].get_prompt(arguments) 