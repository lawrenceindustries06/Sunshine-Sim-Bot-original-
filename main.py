"""
Sunshine Solar Sim - Main Bot Launcher
An idle solar energy simulation game as a Discord bot.
"""
import logging
import os
from bot import SunshineSolarBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    logging.info("Loaded environment from .env file")
except ImportError:
    logging.warning("python-dotenv not installed, using environment variables directly")

# Get environment variables
def get_token():
    # Try to get token from environment
    token = os.getenv("DISCORD_TOKEN")
    
    # If not found, try to read from .env file directly
    if not token:
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("DISCORD_TOKEN="):
                        token = line.strip().split("=", 1)[1]
                        break
        except Exception as e:
            logging.warning(f"Could not read token from .env file: {e}")
    
    # If still not found, use the token provided directly
    if not token:
        token = "MTM2NzM5OTI1MzM5OTU2ODQ3NA.GTsRCh.arHqCb9QSFPPR52-r9AxVj6fKmpGBe4jrP_8aw"
        logging.info("Using hardcoded token")
    
    return token

# Get application ID (needed for slash commands)
def get_application_id():
    # Try to get application ID from environment
    app_id = os.getenv("APPLICATION_ID")
    
    # If not found, try to read from .env file directly
    if not app_id:
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("APPLICATION_ID="):
                        app_id = line.strip().split("=", 1)[1]
                        break
        except Exception as e:
            logging.warning(f"Could not read application ID from .env file: {e}")
    
    # If still not found, use the ID directly (same as bot ID in most cases)
    if not app_id:
        app_id = "1367399253399568474"  # This should be your bot's application ID
        logging.info("Using hardcoded application ID")
    
    return app_id

if __name__ == "__main__":
    # Get the token and application ID
    token = get_token()
    app_id = get_application_id()
    logging.info(f"Token loaded successfully (length: {len(token)})")
    logging.info(f"Application ID: {app_id}")
    
    # Set the application ID in environment for the bot to use
    os.environ["APPLICATION_ID"] = app_id
    
    # Initialize and run the bot
    bot = SunshineSolarBot()
    bot.run(token)
