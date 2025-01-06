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

async def test_connection_requests():
    """Test the LinkedIn connection requests tool."""
    try:
        # Test search parameters
        TEST_PARAMS = {
            "search_query": "AI recruiter in San Francisco",
            "max_connections": 2,  # Keep low for testing
            "custom_note": "Hi {name}, I noticed you work at {headline}. Would love to connect! {headline} {location} {user_info}",
            "user_profile_id": "shreyshahh"
        }
        
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
            "id": "test-connections-1",
            "method": "tools/call",
            "params": {
                "name": "send_connections",
                "arguments": TEST_PARAMS
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
                assert "results" in data, "Response missing 'results' field"
                
                # Check each connection result
                for result in data["results"]:
                    assert "status" in result, "Result missing 'status' field"
                    assert "profile" in result, "Result missing 'profile' field"
                    assert "note_sent" in result, "Result missing 'note_sent' field"
                    
                    profile = result["profile"]
                    # Log connection attempt details
                    logger.info(f"Connection attempt for {profile.get('name', 'Unknown')}:")
                    logger.info(f"  Status: {result['status']}")
                    logger.info(f"  Note sent: {result['note_sent']}")
                    logger.info(f"  Headline: {profile.get('headline', 'N/A')}")
                    logger.info(f"  Location: {profile.get('location', 'N/A')}")
                
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
    asyncio.run(test_connection_requests()) 