"""
User Management Cog
Handles user registration and basic account functionality.
"""
import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

class UserManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="start", description="Start your solar farm adventure!")
    async def start(self, interaction: discord.Interaction):
        """Register a new user and initialize their farm"""
        # Increment command counter
        self.bot.command_count += 1
        
        user_id = str(interaction.user.id)
        
        # Check if user already exists
        if user_id in self.bot.user_data:
            await interaction.response.send_message(
                "You already have a solar farm! Use `/status` to view your progress.",
                ephemeral=True
            )
            return
        
        # Initialize new user data
        self.bot.user_data[user_id] = {
            "name": interaction.user.name,
            "money": 1000,  # Starting money - just enough for one solar panel
            "energy": 0,    # Starting energy
            "battery_tier": 1,  # Starting battery tier
            "generators": {
                "solar_panel": 1,  # Start with one solar panel
                "wind_turbine": 0,
                "gas_generator": 0
            }
        }
        
        # Save user data
        self.bot.save_data()
        
        # Send welcome message
        embed = discord.Embed(
            title="🌞 Welcome to Sunshine Solar Sim! 🌞",
            description="You've started your own solar farm adventure!",
            color=0xF1C40F  # Sunny yellow color
        )
        embed.add_field(name="Starting Balance", value=f"${self.bot.user_data[user_id]['money']}", inline=True)
        embed.add_field(name="Equipment", value="1x Solar Panel", inline=True)
        embed.add_field(name="Battery", value=f"Tier 1 ({self.bot.battery_capacities[1]} capacity)", inline=True)
        embed.add_field(
            name="Getting Started",
            value=(
                "• Use `/status` to check your farm\n"
                "• Buy more generators with `/buy`\n"
                "• Sell your energy with `/sell`\n"
                "• Upgrade your battery with `/upgrade_battery`"
            ),
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
        logger.info(f"New user registered: {interaction.user.name} ({user_id})")
    
    @app_commands.command(name="status", description="Check your solar farm status")
    async def status(self, interaction: discord.Interaction):
        """Show the user's current farm status"""
        # Increment command counter
        self.bot.command_count += 1
        
        user_id = str(interaction.user.id)
        
        # Check if user exists
        if user_id not in self.bot.user_data:
            await interaction.response.send_message(
                "You don't have a solar farm yet! Use `/start` to begin your adventure.",
                ephemeral=True
            )
            return
        
        # Get user data
        data = self.bot.user_data[user_id]
        
        # Calculate total generation rate per minute
        solar_gen = data["generators"]["solar_panel"] * self.bot.generation_rates["solar_panel"]
        wind_gen = data["generators"]["wind_turbine"] * self.bot.generation_rates["wind_turbine"]
        gas_gen = data["generators"]["gas_generator"] * self.bot.generation_rates["gas_generator"]
        total_gen = solar_gen + wind_gen + gas_gen
        
        # Create status embed
        embed = discord.Embed(
            title=f"☀️ {interaction.user.name}'s Solar Farm",
            color=0x3498DB  # Blue color
        )
        
        # Add financial information
        embed.add_field(name="💰 Money", value=f"${data['money']:.2f}", inline=True)
        embed.add_field(
            name="⚡ Energy Storage", 
            value=f"{data['energy']:.0f}/{self.bot.battery_capacities[data['battery_tier']]}",
            inline=True
        )
        embed.add_field(
            name="⚡ Generation Rate", 
            value=f"{total_gen:.0f} units/min",
            inline=True
        )
        
        # Add generator information
        generators_text = ""
        if data["generators"]["solar_panel"] > 0:
            generators_text += f"🌞 Solar Panels: {data['generators']['solar_panel']} " + \
                             f"({solar_gen:.0f} units/min)\n"
        if data["generators"]["wind_turbine"] > 0:
            generators_text += f"🌀 Wind Turbines: {data['generators']['wind_turbine']} " + \
                             f"({wind_gen:.0f} units/min)\n"
        if data["generators"]["gas_generator"] > 0:
            generators_text += f"⛽ Gas Generators: {data['generators']['gas_generator']} " + \
                             f"({gas_gen:.0f} units/min)\n"
        
        embed.add_field(name="🔋 Generators", value=generators_text or "None", inline=False)
        
        # Add battery information
        embed.add_field(
            name="🔋 Battery", 
            value=f"Tier {data['battery_tier']} ({self.bot.battery_capacities[data['battery_tier']]} capacity)",
            inline=False
        )
        
        # Add maintenance costs information
        solar_maint = data["generators"]["solar_panel"] * self.bot.maintenance_costs["solar_panel"]
        wind_maint = data["generators"]["wind_turbine"] * self.bot.maintenance_costs["wind_turbine"]
        gas_maint = data["generators"]["gas_generator"] * self.bot.maintenance_costs["gas_generator"]
        total_maint = solar_maint + wind_maint + gas_maint
        
        gas_fuel_cost = data["generators"]["gas_generator"] * self.bot.gas_cost * 60 * 24  # daily fuel cost
        
        maintenance_text = f"Daily Maintenance: ${total_maint:.2f}\n"
        if gas_fuel_cost > 0:
            maintenance_text += f"Daily Fuel Cost (if running 24/7): ${gas_fuel_cost:.2f}\n"
        
        embed.add_field(name="💸 Operating Costs", value=maintenance_text, inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="help", description="Get help with Sunshine Solar Sim commands")
    async def help_command(self, interaction: discord.Interaction):
        """Display help information about the bot commands"""
        # Increment command counter
        self.bot.command_count += 1
        
        embed = discord.Embed(
            title="☀️ Sunshine Solar Sim - Help",
            description="Welcome to Sunshine Solar Sim! Here are the commands you can use:",
            color=0x2ECC71  # Green color
        )
        
        # Basic commands
        basic_commands = (
            "`/start` - Start your solar farm adventure\n"
            "`/status` - Check your solar farm status\n"
            "`/help` - Show this help message\n"
            "`/analytics` - View bot statistics"
        )
        embed.add_field(name="📋 Basic Commands", value=basic_commands, inline=False)
        
        # Generator commands
        generator_commands = (
            "`/buy [generator] [amount]` - Buy generators\n"
            "Available generators: solar_panel, wind_turbine, gas_generator"
        )
        embed.add_field(name="🔋 Generator Commands", value=generator_commands, inline=False)
        
        # Economy commands
        economy_commands = (
            "`/sell [amount]` - Sell energy for money\n"
            "`/upgrade_battery` - Upgrade your battery storage capacity"
        )
        embed.add_field(name="💰 Economy Commands", value=economy_commands, inline=False)
        
        # Game information
        game_info = (
            "• Energy is generated automatically every minute\n"
            "• Solar panels and wind turbines generate energy for free\n"
            "• Gas generators are more powerful but require fuel costs\n"
            "• All generators have daily maintenance costs\n"
            "• Upgrade your battery to store more energy\n"
            "• Sell energy to make money and expand your farm!"
        )
        embed.add_field(name="ℹ️ Game Information", value=game_info, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    # Add the cog to the bot - this will automatically register app commands
    await bot.add_cog(UserManagement(bot))
