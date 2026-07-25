# Doabot

Doabot is a Discord bot focused on **server moderation**, **anti-spam protection**. Originally created for the streamer Doaenel, the bot is used only in his community server.

---

## Features

### Moderation
- `ban` / `unban` — Ban or unban users by mention or ID
- `banrev` — Revert a recent ban (1st, 2nd, or 3rd most recent)
- `mute` / `unmute` — Mute or unmute users by mention or ID
- `warn` / `warns` / `clearwarns` — Warn system with persistent tracking
- `purge` — Bulk delete recent messages
- `expose` — Track and collect deleted messages of a user (auto-deletes after configured time)
- `showbans` — Display the 3 most recent bans
- `sync` — Sync slash commands with the bot

### Anti-Spam & Auto-Mod
- `antispam` — Toggle anti-spam functionality
- `spammer_timeout` — Set anti-spam timeout duration
- `bl` — Blacklist management (view, add, remove)
- `link` — Anti-spam link blacklist system

### Utility
- `linkfix` / `swap` — Link fixer functionality
- `setserver` — Restrict bot to a specific server (owner only)

---

## Tech Stack

| Component | Version |
|-----------|---------|
| Python | 3.12 |
| [discord.py](https://pypi.org/project/discord.py/) | 2.3.2 |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | 1.0.1 |
| [cohere](https://pypi.org/project/cohere/) | 5.15 |

---

## Installation

### Using pip

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Using Conda

```bash
conda create -n Doabot python=3.12
conda activate Doabot
pip install -r requirements.txt
```

---

## Configuration

Edit `jsonChecker.py` if you want to add extra variables or modify the JSON structure.

### Example Configs

**Main config (`config.json`):**
```json
{
  "Version": "1.0.0",
  "server_id": 713475017957965945,
  "delete_msg_days": 7,
  "mute_amount": 2,
  "prefix": "^",
  "blacklist_on": false,
  "linkfixer_on": false,
  "antispam_on": true,
  "spammer_timeout": 20,
  "last_bans": [],
  "expose_delete_hours": 1,
  "instagram_fixer_idx": 0
}
```

---

## Running the Bot

### On Ubuntu / Linux

```bash
# Step 1: Start a screen or tmux session
screen -S doabot
# or: tmux new -s doabot

# Step 2: Activate environment
source venv/bin/activate      # pip
# or: conda activate Doabot   # conda

# Step 3: Run the bot
python main.py

# Detach: Ctrl+A then D (screen) / Ctrl+B then D (tmux)
# Reattach: screen -r doabot  /  tmux attach -t doabot
```

### Useful Server Commands

| Command | Description |
|---------|-------------|
| `git pull` | Pull latest changes from repository |
| `git status` | Check if repo is up to date |
| `screen -ls` / `tmux ls` | List running sessions |
| `htop` | Task manager / diagnostic screen |
| `pkill screen` / `tmux kill-server` | Kill all sessions |

> ⚠️ **CAUTION**: You may need to run some commands as root.

---

## Data & Privacy

Doabot collects minimal data necessary for moderation functionality:
- **User IDs** — for ban reversal tracking
- **Server IDs** — for per-server configuration
- **Message content** — processed in real-time for anti-spam and auto-moderation only

No message content is permanently stored. See our full [Privacy Policy](https://github.com/KenshiroTM/Doabot/blob/main/PRIVACY.md) and [Terms of Service](https://github.com/KenshiroTM/Doabot/blob/main/TERMS.md).

---

## License

[MIT](LICENSE)

---

> Built for twitch.tv/Dantes
