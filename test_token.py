"""Utility to test if your Discord token is valid"""
import os
import sys
import logging
import asyncio
import discord
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('token_tester')

async def test_token(token):
    """Test if a Discord token is valid"""
    # Create a minimal client for testing
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    
    try:
        # Try to login with the token
        await client.login(token)
        logger.info(f"Success! Token is valid for {client.user.name} (ID: {client.user.id})")
        return True
    except discord.errors.LoginFailure as e:
        logger.error(f"Login failed: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False
    finally:
        # Always properly close the client
        if client and client._ready.done():
            await client.close()

def main():
    """Main function to run the token test"""
    # Try to load token from .env file first
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    
    # If no token in .env, check command-line arguments
    if not token and len(sys.argv) > 1:
        token = sys.argv[1]
    
    # If still no token, prompt the user
    if not token:
        token = input("Please enter your Discord token: ")
        
    if not token:
        logger.error("No token provided. Exiting.")
        return 1
        
    # Run the test
    result = asyncio.run(test_token(token))
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())
