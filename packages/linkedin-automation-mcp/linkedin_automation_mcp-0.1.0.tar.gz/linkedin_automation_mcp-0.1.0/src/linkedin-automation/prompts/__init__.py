from typing import Dict, Any, List
from . import analyze_profile, generate_post, research_and_create_linkedin_post

AVAILABLE_PROMPTS = {
    "analyze-profile": analyze_profile,
    "generate-post": generate_post,
    "research-and-create-linkedin-post": research_and_create_linkedin_post
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