# Sunshine Solar Sim

An idle solar energy simulation game as a Discord bot. Manage your virtual solar farm, collect energy, and build a renewable energy empire!

## Features

- 🌞 Build and manage a virtual solar farm
- ⚡ Collect energy over time from solar panels, wind turbines, and more
- 💰 Sell energy for money to expand your operation
- 🔋 Upgrade batteries to store more energy
- 🏭 Strategic resource management and economic simulation

## Commands

- `/start` - Register your account and start your solar farm
- `/status` - View your current farm status
- `/buy [generator_type] [amount]` - Purchase generators for energy production
- `/upgrade_battery` - Upgrade your battery to store more energy
- `/sell [amount]` - Sell stored energy for money
- `/help` - Display help information

## Setup Instructions

1. **Prerequisites**
   - Python 3.11 or higher
   - A Discord account and registered application/bot

2. **Environment Variables**
   - Create a `.env` file based on the `.env.example` template
   - Add your Discord bot token and application ID

3. **Installation**
   ```bash
   # Clone this repository
   git clone https://github.com/YourUsername/sunshine-solar-sim.git
   cd sunshine-solar-sim
   
   # Install dependencies
   pip install -r render-requirements.txt
   ```

4. **Running the Bot**
   ```bash
   python main.py
   ```

## Deployment

This bot is set up for easy deployment to Render.com:

1. Fork/clone this repository to your GitHub account
2. In Render, create a new Web Service pointing to your GitHub repository
3. Select "Python" as the environment
4. Set the build command to: `pip install -r render-requirements.txt`
5. Set the start command to: `python main.py`
6. Add the environment variables: `DISCORD_TOKEN` and `APPLICATION_ID`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# Sunshine-Sim-Bot
# Sunshine-Sim-Bot
