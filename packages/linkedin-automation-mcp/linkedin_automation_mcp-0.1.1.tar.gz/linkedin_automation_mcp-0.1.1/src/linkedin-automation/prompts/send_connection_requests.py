from typing import Dict, Any

def get_prompt(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Return the send connection requests prompt structure."""
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Send connection requests to LinkedIn profiles matching: {arguments.get('search_query')}. Max connections: {arguments.get('max_connections', 10)}. Custom note: {arguments.get('custom_note', '')}"
                }
            }
        ]
    }
    
def get_prompt_info() -> Dict[str, Any]:
    """Return the prompt metadata."""
    return {
        "name": "send-connections",
        "description": "Send LinkedIn connection requests",
        "arguments": [{"name": "search_query", "description": "Search query to find profiles to connect with", "required": True}]
    }