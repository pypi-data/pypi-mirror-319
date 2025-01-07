from pydantic import BaseModel, Field
from typing import List

class Tool(BaseModel):
    """Base model for tool definitions."""
    name: str = Field(description="Name of the tool")
    description: str = Field(description="Description of what the tool does")
    inputSchema: dict = Field(description="JSON schema for the tool's input")

class ScrapePostsInput(BaseModel):
    """Input model for post scraping tool."""
    profile_ids: List[str] = Field(
        description="List of LinkedIn profile IDs to scrape"
    )
    max_posts: int = Field(
        default=5,
        description="Maximum number of posts to scrape per profile"
    )

class SendConnectionInput(BaseModel):
    """Input model for connection request tool."""
    search_query: str = Field(
        description="Search query to find LinkedIn profiles (e.g., 'AI recruiter in San Francisco')"
    )
    max_connections: int = Field(
        default=10,
        description="Maximum number of connection requests to send"
    )
    custom_note: str = Field(
        default="",
        description="""Optional custom note to include with connection requests
        you can use {name}, {headline}, {location} to include profile info when available) to make the note more personalized
        use {user_info} to include user info when available"""
    )
    user_profile_id: str = Field(
        default="",
        description="User profile ID to include in the note"
    )

class GetProfileInput(BaseModel):
    """Input model for profile info tool."""
    profile_ids: List[str] = Field(
        description="List of LinkedIn profile IDs to get information for"
    )

class PostContentToLinkedinInput(BaseModel):
    """Input model for posting content tool."""
    content: str = Field(
        description="The text content to post on LinkedIn"
    )

class PostScraperTool(Tool):
    """Tool definition for post scraping."""
    name: str = Field(default="scrape_posts")
    description: str = Field(default="Scrape LinkedIn posts from specified profiles (handles login automatically)")
    inputSchema: dict = Field(default_factory=lambda: ScrapePostsInput.model_json_schema())

class ConnectionTool(Tool):
    """Tool definition for connection requests."""
    name: str = Field(default="send_connections")
    description: str = Field(default="Search for LinkedIn profiles and send connection requests")
    inputSchema: dict = Field(default_factory=lambda: SendConnectionInput.model_json_schema())

class ProfileInfoTool(Tool):
    """Tool definition for profile info."""
    name: str = Field(default="get_profile_info")
    description: str = Field(default="Get basic profile information for LinkedIn profiles")
    inputSchema: dict = Field(default_factory=lambda: GetProfileInput.model_json_schema())

class PostContentToLinkedinTool(Tool):
    """Tool definition for posting content."""
    name: str = Field(default="post_content_to_linkedin")
    description: str = Field(default="Post content to LinkedIn")
    inputSchema: dict = Field(default_factory=lambda: PostContentToLinkedinInput.model_json_schema())

class ToolsList(BaseModel):
    """Model for list of available tools."""
    tools: List[Tool] 