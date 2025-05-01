"""
Sunshine Solar Sim - Bot Class
Handles the main functionality of the Discord bot.
"""
import asyncio
import discord
import json
import logging
import os
from discord.ext import commands, tasks
from pathlib import Path

# Setup logger
logger = logging.getLogger(__name__)

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Create empty users.json file if it doesn't exist
users_file = data_dir / "users.json"
if not users_file.exists():
    with open(users_file, "w") as f:
        json.dump({}, f)

class SunshineSolarBot(commands.Bot):
    def __init__(self):
        # Initialize the bot with intents
        # Using default intents only to avoid requiring privileged intents
        intents = discord.Intents.default()
        
        # This is a comment explaining the situation with intents:
        # The message_content intent is privileged and requires enabling in the Discord Developer Portal
        # If you've enabled it in the portal, you can uncomment the next line:
        # intents.message_content = True

        super().__init__(
            command_prefix=commands.when_mentioned,  # Only respond to @mentions for text commands
            intents=intents,
            help_command=None,  # We'll create our own help command
            application_id=os.getenv("APPLICATION_ID")  # App ID is needed for slash commands
        )
        
        # Store of user data
        self.user_data = {}
        
        # Energy generation rates (per minute)
        self.generation_rates = {
            "solar_panel": 15,   # 15 energy per minute per panel
            "wind_turbine": 25,  # 25 energy per minute per turbine
            "gas_generator": 40, # 40 energy per minute per generator
        }
        
        # Generator prices
        self.generator_prices = {
            "solar_panel": 1000,
            "wind_turbine": 2500,
            "gas_generator": 5000
        }
        
        # Generator maintenance costs (per day)
        self.maintenance_costs = {
            "solar_panel": 20,
            "wind_turbine": 75,
            "gas_generator": 200
        }
        
        # Gas costs (per minute of operation)
        self.gas_cost = 5
        
        # Battery capacity per tier
        self.battery_capacities = {
            1: 1000,    # Tier 1: 1000 energy
            2: 3000,    # Tier 2: 3000 energy
            3: 10000,   # Tier 3: 10000 energy
            4: 50000,   # Tier 4: 50000 energy
            5: 250000   # Tier 5: 250000 energy
        }
        
        # Battery tier prices
        self.battery_prices = {
            1: 2000,
            2: 7500,
            3: 25000,
            4: 100000,
            5: 500000
        }
        
        # Energy selling price (per unit)
        self.energy_price = 0.1  # $0.1 per energy unit
    
    async def setup_hook(self):
        """Called when the bot is setting up"""
        logger.info("Setting up Sunshine Solar Sim Bot...")
        
        # Load user data
        self.load_data()
        
        # Register cogs
        await self.load_extension("cogs.user_management")
        await self.load_extension("cogs.generators")
        await self.load_extension("cogs.batteries")
        await self.load_extension("cogs.economy")
        
        # Start background tasks
        self.generate_energy.start()
        self.apply_maintenance_costs.start()
        
        logger.info("Bot setup complete!")
    
    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f"Logged in as {self.user.name} ({self.user.id})")
        
        # Sync application commands with Discord
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} application commands with Discord")
        except Exception as e:
            logger.error(f"Failed to sync application commands: {str(e)}")
        
        await self.change_presence(activity=discord.Game(name="⚡ Sunshine Solar Sim"))
        
    def load_data(self):
        """Load user data from JSON file"""
        # Define the path to user data
        users_file_path = "data/users.json"
        default_file_path = "data/default_users.json"
        
        try:
            # Try to load existing user data
            with open(users_file_path, "r") as f:
                self.user_data = json.load(f)
            logger.info(f"Loaded data for {len(self.user_data)} users")
        except FileNotFoundError:
            # If the main file is not found, try to use the default file
            logger.warning(f"User data file {users_file_path} not found")
            try:
                with open(default_file_path, "r") as f:
                    self.user_data = json.load(f)
                logger.info(f"Loaded default data template")
            except (FileNotFoundError, json.JSONDecodeError):
                # If no default file or it's invalid, start with empty data
                logger.warning("No default user data found. Starting with empty data.")
                self.user_data = {}
            
            # Create the users.json file
            self.save_data()
        except json.JSONDecodeError:
            logger.error("Error decoding user data. Creating a new data file.")
            self.user_data = {}
            self.save_data()
    
    def save_data(self):
        """Save user data to JSON file"""
        users_file_path = "data/users.json"
        
        # Make sure the directory exists
        os.makedirs(os.path.dirname(users_file_path), exist_ok=True)
        
        try:
            with open(users_file_path, "w") as f:
                json.dump(self.user_data, f, indent=4)
            logger.debug("User data saved successfully")
        except Exception as e:
            logger.error(f"Failed to save user data: {str(e)}")
            # In a production environment, you might want to implement a backup mechanism here
    
    @tasks.loop(minutes=1.0)
    async def generate_energy(self):
        """Background task to generate energy for all users every minute"""
        for user_id, data in self.user_data.items():
            # Calculate energy generated by each type of generator
            solar_energy = data.get("generators", {}).get("solar_panel", 0) * self.generation_rates["solar_panel"]
            wind_energy = data.get("generators", {}).get("wind_turbine", 0) * self.generation_rates["wind_turbine"]
            
            # Gas generators require money for fuel
            gas_generators = data.get("generators", {}).get("gas_generator", 0)
            gas_energy = 0
            if gas_generators > 0:
                gas_cost_total = gas_generators * self.gas_cost
                if data["money"] >= gas_cost_total:
                    # User can afford to run gas generators
                    data["money"] -= gas_cost_total
                    gas_energy = gas_generators * self.generation_rates["gas_generator"]
            
            # Calculate total energy generated
            energy_generated = solar_energy + wind_energy + gas_energy
            
            # Add energy to storage, respecting battery capacity
            battery_tier = data.get("battery_tier", 1)
            max_capacity = self.battery_capacities[battery_tier]
            data["energy"] = min(data["energy"] + energy_generated, max_capacity)
        
        # Save the updated data
        self.save_data()
    
    @generate_energy.before_loop
    async def before_generate_energy(self):
        """Wait until the bot is ready before starting the task"""
        await self.wait_until_ready()
    
    @tasks.loop(hours=24.0)
    async def apply_maintenance_costs(self):
        """Apply daily maintenance costs to generators"""
        for user_id, data in self.user_data.items():
            total_maintenance = 0
            
            # Calculate maintenance costs for each type of generator
            for generator_type, count in data.get("generators", {}).items():
                maintenance_cost = self.maintenance_costs.get(generator_type, 0) * count
                total_maintenance += maintenance_cost
            
            # Apply maintenance costs
            if total_maintenance > 0:
                data["money"] = max(0, data["money"] - total_maintenance)
        
        # Save the updated data
        self.save_data()
    
    @apply_maintenance_costs.before_loop
    async def before_apply_maintenance_costs(self):
        """Wait until the bot is ready before starting the task"""
        await self.wait_until_ready()
