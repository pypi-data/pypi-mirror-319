from typing import Dict, Any

def get_prompt(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Return the profile info prompt structure."""
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Get detailed information for these LinkedIn profiles: {', '.join(arguments.get('profile_ids', []))}"
                }
            }
        ]
    }

def get_prompt_info() -> Dict[str, Any]:
    """Return the prompt metadata."""
    return {
        "name": "get-profile-info",
        "description": "Get detailed information from LinkedIn profiles",
        "arguments": [
            {
                "name": "profile_ids",
                "description": "List of LinkedIn profile IDs to get information from",
                "required": True
            }
        ]
    } 