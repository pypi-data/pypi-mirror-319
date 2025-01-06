from typing import Dict, Any


def get_prompt(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Return the scrape content and post to LinkedIn prompt structure."""
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""
                            Scrape {arguments.get('number_of_posts')} posts from LinkedIn profile: {arguments.get('profile_url')} and then ask me for edits on each post
                            and then refine the fetched content to Write a post in my style and post to LinkedIn: {arguments.get('post_content')}
                            
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
                            Post to LinkedIn: {arguments.get('post_content')}
                            
                            use sequential thinking and write the post in a way that is according to the instructions.
                    """
                },
            }
        ]
    }


def get_prompt_info() -> Dict[str, Any]:
    """Return the prompt metadata."""
    return {
        "name": "scrape-content-and-post-to-linkedin",
        "description": "Scrape content from LinkedIn profile and post to LinkedIn",
        "arguments": [
            {
                "name": "profile_url",
                "description": "URL of the LinkedIn profile to scrape content from",
                "required": True,
            },
            {
                "name": "post_content",
                "description": "Content of the post to be posted",
                "required": True,
            },
            {
                "name": "number_of_posts",
                "description": "Number of posts to scrape",
                "required": True,
            },
        ],
    }
