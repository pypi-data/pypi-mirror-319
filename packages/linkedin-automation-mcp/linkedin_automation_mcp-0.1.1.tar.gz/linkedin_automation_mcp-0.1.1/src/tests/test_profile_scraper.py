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

async def test_profile_scraper():
    """Test the LinkedIn profile scraper tool."""
    try:
        # Test profiles - add more as needed
        TEST_PROFILES = [
            "shreyshahh",
            # Add more profile IDs to test
        ]
        
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
            "id": "test-1",
            "method": "tools/call",
            "params": {
                "name": "get_profile_info",
                "arguments": {
                    "profile_ids": TEST_PROFILES
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
                assert "profiles" in data, "Response missing 'profiles' field"
                
                # Check each profile
                for profile in data["profiles"]:
                    assert "name" in profile, "Profile missing 'name' field"
                    assert "headline" in profile, "Profile missing 'headline' field"
                    assert "location" in profile, "Profile missing 'location' field"
                    assert "about" in profile, "Profile missing 'about' field"
                    
                    # Log profile details
                    logger.info(f"Profile data for {profile.get('name', 'Unknown')}:")
                    logger.info(f"  Headline: {profile.get('headline', 'N/A')}")
                    logger.info(f"  Location: {profile.get('location', 'N/A')}")
                    logger.info(f"  About: {profile.get('about', 'N/A')[:100]}...")
                
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
    asyncio.run(test_profile_scraper()) 