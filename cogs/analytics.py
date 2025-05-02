"""
Analytics Cog
Provides usage statistics and bot status information.
"""
import discord
import logging
import datetime
from discord import app_commands
from discord.ext import commands

# Setup logger
logger = logging.getLogger(__name__)

class Analytics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Initialize command usage counter if it doesn't exist
        if not hasattr(self.bot, 'command_count'):
            self.bot.command_count = 0
    
    @app_commands.command(
        name="analytics",
        description="View bot usage statistics and status"
    )
    async def analytics(self, interaction: discord.Interaction):
        """Show bot usage statistics and status"""
        # Increment the command counter
        self.bot.command_count += 1
        
        # Get the number of registered users
        user_count = len(self.bot.user_data)
        
        # Create an embed for the analytics
        embed = discord.Embed(
            title="📊 Sunshine Solar Sim - Analytics",
            description="Current bot status and usage statistics",
            color=discord.Color.blue()
        )
        
        # Add uptime information
        if hasattr(self.bot, 'start_time'):
            uptime = datetime.datetime.utcnow() - self.bot.start_time
            days, remainder = divmod(int(uptime.total_seconds()), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        else:
            uptime_str = "Unknown"
        
        # Add fields with analytics data
        embed.add_field(name="⚡ Bot Status", value="🟢 Online" if self.bot.is_ready() else "🔴 Offline", inline=True)
        embed.add_field(name="👥 Total Users", value=f"{user_count} users", inline=True)
        embed.add_field(name="🔄 Uptime", value=uptime_str, inline=True)
        embed.add_field(name="📈 Commands Used", value=f"{self.bot.command_count} commands", inline=True)
        
        # Add server count
        server_count = len(self.bot.guilds)
        embed.add_field(name="🏠 Servers", value=f"{server_count} servers", inline=True)
        
        # Add a field for total energy generated (if tracked)
        if hasattr(self.bot, 'total_energy_generated'):
            embed.add_field(
                name="⚡ Total Energy Generated", 
                value=f"{self.bot.total_energy_generated:,} energy", 
                inline=True
            )
        
        # Set footer with bot version
        embed.set_footer(text=f"Sunshine Solar Sim v1.0.0 | Developed by Lawrence Industries")
        
        # Send the analytics embed
        await interaction.response.send_message(embed=embed, ephemeral=False)
        logger.info(f"Analytics command used by {interaction.user.name} ({interaction.user.id})")

async def setup(bot):
    # Initialize the start_time attribute if this is the first load
    if not hasattr(bot, 'start_time'):
        bot.start_time = datetime.datetime.utcnow()
    
    # Initialize command counter if needed
    if not hasattr(bot, 'command_count'):
        bot.command_count = 0
    
    # Initialize total energy counter if needed
    if not hasattr(bot, 'total_energy_generated'):
        bot.total_energy_generated = 0
    
    await bot.add_cog(Analytics(bot))
