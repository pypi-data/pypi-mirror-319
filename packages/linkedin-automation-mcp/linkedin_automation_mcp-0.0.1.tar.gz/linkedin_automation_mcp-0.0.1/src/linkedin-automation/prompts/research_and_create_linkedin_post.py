from typing import Dict, Any

def get_prompt(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Return the research and create LinkedIn post prompt structure."""
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Search about {arguments.get('topic')} and create a linkedin post on it in my writing style based on researched content "
                }
            }
        ]
    }

def get_prompt_info() -> Dict[str, Any]:
    """Return the prompt metadata."""
    return {
        "name": "research-and-create-linkedin-post",
        "description": "Research and create a LinkedIn post",
        "arguments": [{"name": "topic", "description": "Topic to write about", "required": True}]
    }