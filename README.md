# Doabot, a Discord bot

## Model Used

- **Cohere**: `command-a-03-2025`

## Libraries Used

- [`discord.py`](https://pypi.org/project/discord.py/) `v2.3.2`
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) `v1.0.1`
- [`cohere`](https://pypi.org/project/cohere/) `v5.15`

## Info

Edit the `jsonChecker.py` file if you want to add extra variables or modify JSON structure.

## How to Run on Ubuntu

### Step 1: Start a Screen Session and Run the Bot
- `screen -S your_screen_name`

### Step 2: Activate the Virtual Environment
- `source venv/bin/activate`
- `python main.py`

## Step 3: To detach and return to screen:
- Detach: Ctrl + A, then D
- To go back: screen -r
- To kill all the screens: pkill screen

## Useful Commands:
- `git pull`: pulls from the repository
- `git status`: checks if cloned repo is up to date
- `screen -ls`: shows all the running screens in ubuntu
- `htop`: task manager diagnostic screen

## CAUTION
You are most likely needed to be logged in as a root
