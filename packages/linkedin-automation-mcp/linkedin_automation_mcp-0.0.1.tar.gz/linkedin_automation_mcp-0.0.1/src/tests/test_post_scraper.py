import asyncio
import os
import sys
import json
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

async def test_post_scraper():
    """Test the LinkedIn post scraper tool."""
    try:
        # Test profiles - add more as needed
        TEST_PROFILES = [
            "shreyshahh",
            # Add more profile IDs to test
        ]
        MAX_POSTS = 3  # Limit posts for testing
        
        # Create subprocess to run server
        server_process = await asyncio.create_subprocess_exec(
            'python', 'server.py',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Prepare the JSON-RPC request
        request = {
            "jsonrpc": "2.0",
            "id": "test-posts-1",
            "method": "tools/call",
            "params": {
                "name": "scrape_posts",
                "arguments": {
                    "profile_ids": TEST_PROFILES,
                    "max_posts": MAX_POSTS
                }
            }
        }
        
        # Print the request for debugging
        logger.info(f"Sending request: {json.dumps(request, indent=2)}")
        
        # Send the request to server's stdin
        server_process.stdin.write(f"{json.dumps(request)}\n".encode())
        await server_process.stdin.drain()
        
        # Read the response from server's stdout
        response_line = await server_process.stdout.readline()
        response = json.loads(response_line.decode().strip())
        
        # Print the full response for debugging
        logger.info(f"Received response: {json.dumps(response, indent=2)}")
        
        # Parse and validate the response
        if "result" in response:
            result = response["result"]
            content = result.get("content", [])
            if content and len(content) > 0:
                data = json.loads(content[0]["text"])
                
                # Validate the response structure
                assert "success" in data, "Response missing 'success' field"
                assert "posts" in data, "Response missing 'posts' field"
                assert isinstance(data["posts"], list), "'posts' field should be a list"
                
                # Check each post
                for post in data["posts"]:
                    assert "profile_id" in post, "Post missing 'profile_id' field"
                    assert "content" in post, "Post missing 'content' field"
                    assert "timestamp" in post, "Post missing 'timestamp' field"
                    
                    # Log post details
                    logger.info(f"Post from profile {post['profile_id']}:")
                    logger.info(f"  Timestamp: {post['timestamp']}")
                    logger.info(f"  Content preview: {post['content'][:100]}...")
                    logger.info("---")
                
                # Verify post count
                total_posts = len(data["posts"])
                logger.info(f"Total posts scraped: {total_posts}")
                assert total_posts <= len(TEST_PROFILES) * MAX_POSTS, \
                    f"Too many posts returned: {total_posts}"
                
                logger.info("Test completed successfully!")
            else:
                raise AssertionError("Response content is empty")
        else:
            raise AssertionError(f"Error in response: {response.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        # Cleanup: terminate the server process
        if 'server_process' in locals():
            server_process.terminate()
            await server_process.wait()

if __name__ == "__main__":
    # Verify environment variables
    required_vars = ["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    # Run the test
    asyncio.run(test_post_scraper()) 