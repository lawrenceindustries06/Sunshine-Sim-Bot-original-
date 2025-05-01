# Contributing to Sunshine Solar Sim

Thank you for your interest in contributing to Sunshine Solar Sim! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We strive to maintain a welcoming and inclusive community.

## How to Contribute

1. **Fork the repository** on GitHub.

2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/sunshine-solar-sim.git
   cd sunshine-solar-sim
   ```

3. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes** and commit them with descriptive commit messages.

5. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Submit a pull request** to the main repository.

## Development Environment

1. Install required dependencies:
   ```bash
   pip install -r render-requirements.txt
   ```

2. Create a `.env` file based on `.env.example` and add your Discord bot token and application ID.

3. Run the bot:
   ```bash
   python main.py
   ```

## Testing

Before submitting a pull request, please test your changes thoroughly with your own Discord bot instance.

## Style Guidelines

- Follow PEP 8 for Python code style
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Keep code modular and maintainable

## Adding New Features

When adding new features, please consider:

1. **Game Balance**: New features should maintain the overall game balance
2. **Scalability**: Code should be efficient and scalable
3. **Documentation**: Update the README.md and add comments to your code

## Questions?

If you have any questions, feel free to open an issue on GitHub or reach out to the maintainers.

Thank you for contributing to Sunshine Solar Sim!
