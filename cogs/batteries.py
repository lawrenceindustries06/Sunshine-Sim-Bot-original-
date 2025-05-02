"""
Batteries Cog
Handles battery upgrades and storage management.
"""
import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

class Batteries(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="upgrade_battery", description="Upgrade your battery storage capacity")
    async def upgrade_battery(self, interaction: discord.Interaction):
        """Upgrade the user's battery to the next tier"""
        user_id = str(interaction.user.id)
        
        # Check if user exists
        if user_id not in self.bot.user_data:
            await interaction.response.send_message(
                "You don't have a solar farm yet! Use `/start` to begin your adventure.",
                ephemeral=True
            )
            return
        
        # Get user data
        user_data = self.bot.user_data[user_id]
        current_tier = user_data.get("battery_tier", 1)
        
        # Check if already at max tier
        if current_tier >= 5:  # Assuming tier 5 is the maximum
            await interaction.response.send_message(
                "Your battery is already at the maximum tier (Tier 5)!",
                ephemeral=True
            )
            return
        
        # Calculate next tier and price
        next_tier = current_tier + 1
        upgrade_price = self.bot.battery_prices[next_tier]
        
        # Check if user has enough money
        if user_data["money"] < upgrade_price:
            await interaction.response.send_message(
                f"You don't have enough money for this upgrade! You need ${upgrade_price} but only have ${user_data['money']:.2f}.",
                ephemeral=True
            )
            return
        
        # Process the upgrade
        old_capacity = self.bot.battery_capacities[current_tier]
        new_capacity = self.bot.battery_capacities[next_tier]
        
        user_data["money"] -= upgrade_price
        user_data["battery_tier"] = next_tier
        
        # Save user data
        self.bot.save_data()
        
        # Create an embed for the upgrade
        embed = discord.Embed(
            title="🔋 Battery Upgraded!",
            description=f"You upgraded your battery from Tier {current_tier} to Tier {next_tier}!",
            color=0x9B59B6  # Purple color
        )
        
        embed.add_field(name="Cost", value=f"${upgrade_price:.2f}", inline=True)
        embed.add_field(name="Remaining Balance", value=f"${user_data['money']:.2f}", inline=True)
        embed.add_field(
            name="New Capacity", 
            value=f"{old_capacity} → {new_capacity} units", 
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
        logger.info(f"User {user_id} upgraded battery to tier {next_tier} for ${upgrade_price:.2f}")

async def setup(bot):
    await bot.add_cog(Batteries(bot))
