"""
Economy Cog
Handles energy selling and money management.
"""
import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="sell", description="Sell your stored energy for money")
    @app_commands.describe(
        amount="Amount of energy to sell (use 'all' to sell everything)"
    )
    async def sell(self, interaction: discord.Interaction, amount: str = "all"):
        """Sell stored energy for money"""
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
        
        # Check if user has any energy
        if user_data["energy"] <= 0:
            await interaction.response.send_message(
                "You don't have any energy to sell! Wait for your generators to produce some.",
                ephemeral=True
            )
            return
        
        # Determine how much energy to sell
        energy_to_sell = 0
        if amount.lower() == "all":
            energy_to_sell = user_data["energy"]
        else:
            try:
                energy_to_sell = float(amount)
            except ValueError:
                await interaction.response.send_message(
                    "Please enter a valid amount or 'all'.",
                    ephemeral=True
                )
                return
        
        # Validate amount
        if energy_to_sell <= 0:
            await interaction.response.send_message(
                "Please enter a positive amount of energy to sell.",
                ephemeral=True
            )
            return
        
        if energy_to_sell > user_data["energy"]:
            await interaction.response.send_message(
                f"You only have {user_data['energy']:.0f} units of energy to sell.",
                ephemeral=True
            )
            return
        
        # Calculate earnings
        earnings = energy_to_sell * self.bot.energy_price
        
        # Update user data
        user_data["energy"] -= energy_to_sell
        user_data["money"] += earnings
        
        # Save user data
        self.bot.save_data()
        
        # Create an embed for the sale
        embed = discord.Embed(
            title="💸 Energy Sold!",
            description=f"You sold {energy_to_sell:.0f} units of energy for ${earnings:.2f}!",
            color=0xE74C3C  # Red color
        )
        
        embed.add_field(name="Price per Unit", value=f"${self.bot.energy_price}", inline=True)
        embed.add_field(name="New Balance", value=f"${user_data['money']:.2f}", inline=True)
        embed.add_field(
            name="Remaining Energy", 
            value=f"{user_data['energy']:.0f}/{self.bot.battery_capacities[user_data['battery_tier']]}",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
        logger.info(f"User {user_id} sold {energy_to_sell:.0f} energy for ${earnings:.2f}")

async def setup(bot):
    await bot.add_cog(Economy(bot))
