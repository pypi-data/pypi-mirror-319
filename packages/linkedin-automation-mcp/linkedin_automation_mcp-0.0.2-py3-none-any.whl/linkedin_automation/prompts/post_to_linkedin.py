from typing import Dict, Any


def get_prompt(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Return the post to LinkedIn prompt structure."""
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f""" 
                            You are an expert writer tasked with creating a LinkedIn post that mimics a specific writer's style. 
                            To accomplish this, you will first analyze some examples of the writer's previous posts, then create a new post on a given topic in their style.

                            First, here are some examples of the writer's previous LinkedIn posts:

                            <writer_posts>
                            {arguments.get('user_writing_style_examples')}
                            </writer_posts>

                            Your task is to carefully analyze these posts to understand the writer's unique style, tone, and writing patterns. Pay attention to:

                            1. The overall structure of their posts
                            2. The length of their sentences and paragraphs
                            3. Their use of punctuation and formatting (e.g., bullet points, emojis)
                            4. The type of language they use (formal, casual, technical, etc.)
                            5. Any recurring phrases or expressions
                            6. How they start and end their posts
                            7. Their use of hashtags or mentions

                            After analyzing the writer's style, you will write a new LinkedIn post on the topic provided by the user. you must ask user to provide you with a topic before processing.

                            When writing the new post, adhere to the following guidelines:

                            1. Maintain the same overall tone and style as the example posts
                            2. Use a similar structure and formatting
                            3. Incorporate any recurring phrases or expressions if appropriate
                            4. Match the typical length of the writer's posts
                            5. Use hashtags or mentions in a similar manner, if applicable
                            6. Ensure the content is relevant to the given topic while staying true to the writer's style
                            7. do not use * in the final output, no bold text

                            Before writing the final post, use <scratchpad> tags to briefly outline your observations about the writer's style and how you plan to incorporate these elements into the new post.

                            Make sure the final LinkedIn post reads naturally and authentically mimics the writer's style while addressing the given topic.

                            Assume that the first message you get is the topic which will be used to create a linkedin post, strictly following above instructions.
                            Post to LinkedIn: {arguments.get('post_content')}""",
                },
            }
        ]
    }


def get_prompt_info() -> Dict[str, Any]:
    """Return the prompt metadata."""
    return {
        "name": "post-to-linkedin",
        "description": "Post to LinkedIn",
        "arguments": [
            {
                "name": "post_content",
                "description": "Content of the post to be posted",
                "required": True,
            }
        ],
    }
