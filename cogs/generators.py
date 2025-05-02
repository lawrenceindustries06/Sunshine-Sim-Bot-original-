"""
Generators Cog
Handles purchasing and managing power generators.
"""
import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

class Generators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="buy", description="Buy generators for your solar farm")
    @app_commands.describe(
        generator_type="The type of generator to buy",
        amount="How many generators to buy (default: 1)"
    )
    @app_commands.choices(
        generator_type=[
            app_commands.Choice(name="Solar Panel", value="solar_panel"),
            app_commands.Choice(name="Wind Turbine", value="wind_turbine"),
            app_commands.Choice(name="Gas Generator", value="gas_generator")
        ]
    )
    async def buy(
        self, 
        interaction: discord.Interaction, 
        generator_type: str,
        amount: int = 1
    ):
        """Buy generators for energy production"""
        user_id = str(interaction.user.id)
        
        # Check if user exists
        if user_id not in self.bot.user_data:
            await interaction.response.send_message(
                "You don't have a solar farm yet! Use `/start` to begin your adventure.",
                ephemeral=True
            )
            return
        
        # Validate amount
        if amount <= 0:
            await interaction.response.send_message(
                "Please enter a positive number of generators to buy.",
                ephemeral=True
            )
            return
        
        # Get price for the selected generator
        if generator_type not in self.bot.generator_prices:
            await interaction.response.send_message(
                f"Unknown generator type: {generator_type}",
                ephemeral=True
            )
            return
        
        unit_price = self.bot.generator_prices[generator_type]
        total_price = unit_price * amount
        
        # Check if user has enough money
        user_data = self.bot.user_data[user_id]
        if user_data["money"] < total_price:
            await interaction.response.send_message(
                f"You don't have enough money! You need ${total_price} but only have ${user_data['money']:.2f}.",
                ephemeral=True
            )
            return
        
        # Process the purchase
        user_data["money"] -= total_price
        user_data["generators"][generator_type] = user_data["generators"].get(generator_type, 0) + amount
        
        # Save user data
        self.bot.save_data()
        
        # Prepare response message
        generator_names = {
            "solar_panel": "Solar Panel(s)",
            "wind_turbine": "Wind Turbine(s)",
            "gas_generator": "Gas Generator(s)"
        }
        
        generator_name = generator_names.get(generator_type, generator_type)
        
        # Creation an embed for the purchase
        embed = discord.Embed(
            title="🛒 Purchase Successful",
            description=f"You purchased {amount}x {generator_name}!",
            color=0x2ECC71  # Green color
        )
        
        embed.add_field(name="Cost", value=f"${total_price:.2f}", inline=True)
        embed.add_field(name="Remaining Balance", value=f"${user_data['money']:.2f}", inline=True)
        
        # Add generation information
        generation_rate = amount * self.bot.generation_rates[generator_type]
        embed.add_field(
            name="Energy Generation", 
            value=f"+{generation_rate} units/min", 
            inline=True
        )
        
        # Add operating cost information
        maintenance_cost = amount * self.bot.maintenance_costs[generator_type]
        embed.add_field(
            name="Daily Maintenance", 
            value=f"${maintenance_cost:.2f}/day", 
            inline=True
        )
        
        if generator_type == "gas_generator":
            fuel_cost = amount * self.bot.gas_cost * 60  # hourly cost
            embed.add_field(
                name="Fuel Cost", 
                value=f"${fuel_cost:.2f}/hour", 
                inline=True
            )
        
        await interaction.response.send_message(embed=embed)
        logger.info(f"User {user_id} purchased {amount}x {generator_type} for ${total_price:.2f}")

async def setup(bot):
    await bot.add_cog(Generators(bot))
