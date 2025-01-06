from typing import Dict, Any

def get_prompt(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Return the analyze profile prompt structure."""
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Please get info about this LinkedIn profile: {arguments.get('profile_url')}"
                }
            }
        ]
    }

def get_prompt_info() -> Dict[str, Any]:
    """Return the prompt metadata."""
    return {
        "name": "analyze-profile",
        "description": "Analyze a LinkedIn profile",
        "arguments": [
            {
                "name": "profile_url",
                "description": "URL of the LinkedIn profile to analyze",
                "required": True
            }
        ]
    } 