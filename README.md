# Doabot

Doabot is a Discord bot focused on **server moderation**, **anti-spam protection**, and **community engagement** through a leveling system. Originally created for the streamer Doaenel, the bot is used only in his community server.

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

### Leveling System
- `lvl` — Check your level or another user's level
- `lvlroles` — View configured level-based roles
- `setbasevlexp` — Set base EXP for level 1
- `setlvl` — Manually set a user's level
- `setlvlscaling` — Set level scaling factor
- `setxpgain` — Set EXP gained per message

### Utility
- `linkfix` / `swap` — Link fixer functionality
- `setserver` — Restrict bot to a specific server (owner only)

---

## Model Used

- **Cohere**: `command-a-03-2025` (for AI chatbot functionality)

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
  "logging_channel": 1264171411296227370,
  "logging_on": false,
  "blacklist_on": false,
  "chatbot_on": false,
  "linkfixer_on": false,
  "antispam_on": true,
  "spammer_timeout": 20,
  "bot_max_tokens": 150,
  "last_bans": [],
  "bot_read_msg": 10,
  "expose_delete_hours": 1,
  "instagram_fixer_idx": 0
}
```

**Leveling config (`leveling.json`):**
```json
{
  "leveling_on": false,
  "exp_per_msg": 10,
  "level_scaling": 1.2,
  "base_lvl_exp": 100,
  "level_roles": [
    {"level_required": 5, "role_id": 1353471576263360704}
  ]
}
```

**Users data (`users.json`):**
```json
{
  "users": [
    {"user_id": 383722279089078272, "level": 4, "exp": 200, "exp_to_next": 206}
  ]
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

Doabot collects minimal data necessary for moderation and leveling functionality:
- **User IDs** — for ban reversal tracking and leveling system
- **Server IDs** — for per-server configuration
- **Message content** — processed in real-time for anti-spam and auto-moderation only

No message content is permanently stored. See our full [Privacy Policy](../../../home/kenshirotm/Downloads/README/PRIVACY.md) and [Terms of Service](../../../home/kenshirotm/Downloads/README/TERMS.md).

---

## License

[MIT](LICENSE)

---

> Built for twitch.tv/Dantes
