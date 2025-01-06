# LinkedIn Automation MCP

A Model Context Protocol (MCP) server that provides LinkedIn automation and scraping functionality. This package allows you to automate various LinkedIn tasks including profile scraping, post creation, and connection management.

## Features

- **Scrape LinkedIn Posts**: Retrieve recent posts from specified LinkedIn profiles
- **Send LinkedIn Connection Requests**: Find profiles based on a search query and send connection requests, optionally including a personalized note
- **Get Profile Information**: Obtain basic information about specific LinkedIn profiles
- **Post Content to LinkedIn**: Create and post new content on LinkedIn on behalf of the user
- Combine all these to automate a lot of linkedin tasks together

## Components

### Prompts

The server provides several prompts for different LinkedIn automation tasks:

- `scrape_content_and_post_to_linkedin`: Scrape content and create LinkedIn posts
- `research_and_create_linkedin_post`: Research topics and generate posts
- `post_to_linkedin`: Publish content to LinkedIn
- `get_profile_info`: Extract LinkedIn profile information
- `scrape_posts`: Collect posts from LinkedIn
- `send_connection_requests`: Manage connection requests
- `generate_post`: Create engaging LinkedIn content

### Tools

The package implements various tools in the `tools` directory:
- LinkedIn automation utilities
- Browser interaction helpers
- Content generation tools
- Data models for structured information

## Installation

Requires UV (Fast Python package and project manager)

If UV isn't installed:

```bash
# Using Homebrew on macOS 
brew install uv

# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Install the package:

```bash
# Install from PyPI
uv pip install linkedin-automation-mcp

# Install from source
uv pip install git+https://github.com/shahshrey/linkedin-automation.git
```

## Claude Desktop
Add this tool as a mcp server by editing the Claude config file.

The config file location depends on your operating system:
- MacOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "linkedin-automation": {
    "command": "uv",
    "args": ["run", "linkedin-automation-mcp"],
    "env": {
      "LINKEDIN_EMAIL": "your_email@example.com",
      "LINKEDIN_PASSWORD": "your_password"
    }
  }
}
```

To verify the server is working. Open the Claude client and use a prompt like "search about RAG, write a post on it in my style and post it on my linkedin". You should see an alert box open to confirm tool usage. Click "Allow for this chat"

![alt text](image.png)
## Development

1. Clone the repository
2. Install dependencies:
```bash
uv pip install -e .
```
3. Run tests:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

