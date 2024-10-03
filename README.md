
# Hers Validation Discord Bot

A Discord bot that manages validation requests for Discord server users, allowing them to select roles and undergo a manual verification process.

## Features
- Role selection via dropdown menu.
- Modal verification to gather user details.
- Manual approval or denial of requests.
- Administrative commands for role and validation channel setup.

## Prerequisites
- Python 3.8 or higher
- Discord bot token

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/hers_validation.git
    cd hers_validation
    ```

2. Create a virtual environment:

    ```sh
    python -m venv .venv
    ```

3. Activate the virtual environment:

    - On Windows:

      ```sh
      .\.venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```sh
      source .venv/bin/activate
      ```

4. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

5. Create a `.env` file to store your bot token:

    ```sh
    echo "token=YOUR_DISCORD_BOT_TOKEN" > .env
    ```

## Running the Bot

Once the setup is complete, you can start the bot with:

```sh
python bot.py
```

Ensure that your `.env` file contains a valid bot token.

## Usage

Use the `/role` command to set up the role selection in your Discord server.
Place the bot at the very top in the role hierarchy.

- `channel_home`: channel where the main embed with selection for student will be send.
- `channel_validation`: channel where admins will validate students.
## File Structure

```sh
.
├── bot.py                 # Main entry point for the bot
├── cogs
│   └── validation.py      # Role validation logic as a cog
├── config.py              # Bot configuration setup
├── events
│   └── on_interaction.py  # Event listeners, including interactions
├── modals
│   └── verification.py    # Verification modal class
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
└── .gitignore             # Files to ignore in Git
```

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
