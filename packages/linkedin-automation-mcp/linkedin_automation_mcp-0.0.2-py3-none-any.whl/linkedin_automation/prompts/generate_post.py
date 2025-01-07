from typing import Dict, Any

def get_prompt(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Return the generate post prompt structure."""
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Generate a professional LinkedIn post about: {arguments.get('topic')}"
                }
            }
        ]
    }

def get_prompt_info() -> Dict[str, Any]:
    """Return the prompt metadata."""
    return {
        "name": "generate-post",
        "description": "Generate a LinkedIn post",
        "arguments": [
            {
                "name": "topic",
                "description": "Topic to write about",
                "required": True
            }
        ]
    } 