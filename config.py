"""
Configuration Utilities
Provides configuration settings for the Sunshine Solar Sim bot.
"""

# Default starting money for new users
DEFAULT_STARTING_MONEY = 5000

# Default starting generators
DEFAULT_STARTING_GENERATORS = {
    "solar_panel": 1,
    "wind_turbine": 0,
    "gas_generator": 0
}

# Energy generation rates (per minute)
ENERGY_GENERATION_RATES = {
    "solar_panel": 15,   # 15 energy per minute per panel
    "wind_turbine": 25,  # 25 energy per minute per turbine
    "gas_generator": 40  # 40 energy per minute per generator
}

# Generator prices
GENERATOR_PRICES = {
    "solar_panel": 1000,
    "wind_turbine": 2500,
    "gas_generator": 5000
}

# Generator maintenance costs (per day)
MAINTENANCE_COSTS = {
    "solar_panel": 20,
    "wind_turbine": 75,
    "gas_generator": 200
}

# Gas cost per minute of operation
GAS_COST_PER_MINUTE = 5

# Battery capacities and prices
BATTERY_CAPACITIES = {
    1: 1000,    # Tier 1: 1000 energy
    2: 3000,    # Tier 2: 3000 energy
    3: 10000,   # Tier 3: 10000 energy
    4: 50000,   # Tier 4: 50000 energy
    5: 250000   # Tier 5: 250000 energy
}

BATTERY_PRICES = {
    1: 2000,     # Starting tier
    2: 7500,     # Tier 2 upgrade price
    3: 25000,    # Tier 3 upgrade price
    4: 100000,   # Tier 4 upgrade price
    5: 500000    # Tier 5 upgrade price
}

# Energy selling price (per unit)
ENERGY_PRICE = 0.1  # $0.1 per energy unit
