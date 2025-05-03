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

# Load .env for local development only
try:
    from dotenv import load_dotenv
    load_dotenv()
    logging.info("Loaded environment from .env file")
except ImportError:
    logging.warning("python-dotenv not installed, using environment variables directly")

def get_token():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logging.critical("DISCORD_TOKEN not found in environment!")
        exit(1)
    return token

def get_application_id():
    return os.getenv("APPLICATION_ID", "1367399253399568474")

if __name__ == "__main__":
    token = get_token()
    app_id = get_application_id()
    
    logging.info(f"Token loaded successfully (length: {len(token)})")
    logging.info(f"Application ID: {app_id}")

    # Optional: pass app_id to bot class instead of setting env
    os.environ["APPLICATION_ID"] = app_id

    bot = SunshineSolarBot()
    bot.run(token)
