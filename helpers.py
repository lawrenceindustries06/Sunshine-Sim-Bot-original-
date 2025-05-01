"""
Helper Utilities
Provides helper functions for the Sunshine Solar Sim bot.
"""
import discord
from typing import Dict, Any

def format_money(amount: float) -> str:
    """Format money amount with commas and two decimal places"""
    return f"${amount:,.2f}"

def format_energy(amount: float) -> str:
    """Format energy amount with commas and no decimal places"""
    return f"{amount:,.0f}"

def create_status_embed(user_name: str, user_data: Dict[str, Any], config: Dict[str, Any]) -> discord.Embed:
    """Create a status embed for displaying a user's farm information"""
    # Calculate total generation rate per minute
    solar_gen = user_data["generators"]["solar_panel"] * config["generation_rates"]["solar_panel"]
    wind_gen = user_data["generators"]["wind_turbine"] * config["generation_rates"]["wind_turbine"]
    gas_gen = user_data["generators"]["gas_generator"] * config["generation_rates"]["gas_generator"]
    total_gen = solar_gen + wind_gen + gas_gen
    
    # Create the embed
    embed = discord.Embed(
        title=f"☀️ {user_name}'s Solar Farm",
        color=0x3498DB  # Blue color
    )
    
    # Add financial information
    embed.add_field(name="💰 Money", value=format_money(user_data['money']), inline=True)
    embed.add_field(
        name="⚡ Energy Storage", 
        value=f"{format_energy(user_data['energy'])}/{format_energy(config['battery_capacities'][user_data['battery_tier']])}",
        inline=True
    )
    embed.add_field(
        name="⚡ Generation Rate", 
        value=f"{format_energy(total_gen)} units/min",
        inline=True
    )
    
    # Add generator information
    generators_text = ""
    if user_data["generators"]["solar_panel"] > 0:
        generators_text += f"🌞 Solar Panels: {user_data['generators']['solar_panel']} " + \
                         f"({format_energy(solar_gen)} units/min)\n"
    if user_data["generators"]["wind_turbine"] > 0:
        generators_text += f"🌀 Wind Turbines: {user_data['generators']['wind_turbine']} " + \
                         f"({format_energy(wind_gen)} units/min)\n"
    if user_data["generators"]["gas_generator"] > 0:
        generators_text += f"⛽ Gas Generators: {user_data['generators']['gas_generator']} " + \
                         f"({format_energy(gas_gen)} units/min)\n"
    
    embed.add_field(name="🔋 Generators", value=generators_text or "None", inline=False)
    
    # Add battery information
    embed.add_field(
        name="🔋 Battery", 
        value=f"Tier {user_data['battery_tier']} ({format_energy(config['battery_capacities'][user_data['battery_tier']])} capacity)",
        inline=False
    )
    
    return embed

def calculate_maintenance_costs(user_data: Dict[str, Any], config: Dict[str, Any]) -> float:
    """Calculate the total daily maintenance costs for a user's generators"""
    total_maintenance = 0
    for generator_type, count in user_data["generators"].items():
        maintenance_cost = config["maintenance_costs"].get(generator_type, 0) * count
        total_maintenance += maintenance_cost
    return total_maintenance

def calculate_daily_fuel_costs(user_data: Dict[str, Any], config: Dict[str, Any]) -> float:
    """Calculate the daily fuel costs if all gas generators run continuously"""
    gas_generators = user_data["generators"].get("gas_generator", 0)
    return gas_generators * config["gas_cost"] * 60 * 24  # cost per minute * minutes per day
