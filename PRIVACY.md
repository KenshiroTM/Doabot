# Privacy Policy for Doabot

**Last updated:** 18 July 2026

---

## 1. Introduction

This Privacy Policy explains how Doabot ("we", "our", "the bot") collects, uses, and protects data when operating within Discord servers. By participating in Doaenel's Discord server where Doabot operates, you agree to the practices described in this policy.

Doabot is a Discord moderation bot created for streamer Doaenel and his community. We are committed to handling data responsibly and transparently.

---

## 2. Data We Collect

Doabot collects only the minimum data necessary for its core functionality. All data is obtained through Discord's official API.

### 2.1 User IDs & Usernames
- **Purpose**: Track users for the leveling system, ban reversal functionality, and moderation actions.
- **Examples**: User IDs and usernames of banned users (up to 3–5 most recent), user IDs and usernames in the leveling database.
- **Storage**: Stored in local JSON files (`users.json`, `config.json`).

### 2.2 Server IDs
- **Purpose**: Bot is hardcoded to operate exclusively in Doaenel's Discord server (ID: `713475017957965945`). The server ID acts as a hard lock — the bot will not respond to events or commands in any other server.
- **Storage**: Stored in local JSON files (`config.json`).

### 2.3 Message Content
- **Purpose**: Real-time processing for anti-spam detection, auto-moderation, and command parsing.
- **Important**: Message content is **processed in real-time only** and is **not permanently stored**.
- **Exception**: The `expose` command temporarily collects deleted message metadata for moderation purposes. These are automatically deleted after the configured duration (default: 1 hour).

### 2.4 Role IDs
- **Purpose**: Leveling system — assign roles when users reach specific levels.
- **Storage**: Stored in `leveling.json`.

### 2.5 What We Do NOT Collect
- We do **not** collect email addresses, passwords, or personal information outside of Discord.
- We do **not** log or store message history.
- We do **not** track user activity outside of Discord.
- We do **not** use cookies or tracking pixels.
- We do not operate in multiple servers. Doabot is restricted to a single Discord server.

---

## 3. How We Use Your Data

| Data Type | Purpose |
|-----------|---------|
| User IDs & usernames | Ban reversal tracking, leveling system, moderation logs |
| Server ID | Hardcoded server restriction — bot operates exclusively in Doaenel's Discord server and refuses all events from other servers |
| Message content (real-time) | Anti-spam filtering, auto-moderation, command processing |
| Role IDs | Automatic role assignment in the leveling system |

---

## 4. Data Storage & Security

- All data is stored in **local JSON files** on the server hosting the bot.
- Data is **not transmitted to any third-party services** except Discord's API, which is required for the bot to function.
- Access to the bot's server is restricted to the bot owner.

---

## 5. Data Retention

| Data Type | Retention Period |
|-----------|-----------------|
| User IDs (leveling) | Until the user is removed from the server or data is manually cleared |
| User IDs (bans) & usernames | Up to 3–5 most recent bans; older entries are overwritten |
| Message content (expose) | Automatically deleted after the configured `expose_delete_hours` |

---

## 6. Data Sharing

We do **not** sell, trade, rent, or share user data with any third parties. Data is only shared with **Discord Inc.** as required for the bot to function via Discord's API.

---

## 7. Your Rights

As a user of Doaenel's Discord server, you have the right to:

- **Request data deletion**: Contact the bot owner. Note that most data (leveling progress, moderation logs) is dynamically generated and tied to active server participation.
- **Access your data**: Request a copy of the data we hold about you.

To exercise these rights, contact:

- **Discord**: KenshiroTM
- **Email**: kenshirotm@gmail.com
- **GitHub Issues**: [https://github.com/KenshiroTM/Doabot/issues](https://github.com/KenshiroTM/Doabot/issues)

---

## 8. Children's Privacy

Doabot is not intended for use by individuals under the age of 13 (or the minimum age required by Discord in your region). We do not knowingly collect data from children.

---

## 9. Changes to This Policy

We may update this Privacy Policy from time to time. Changes will be posted on this page with an updated "Last updated" date. Continued use of the bot after changes constitutes acceptance of the revised policy.

---

## 10. Contact

For privacy-related questions, data deletion requests, or concerns:

- **Discord**: KenshiroTM
- **Email**: kenshirotm@gmail.com
- **GitHub Issues**: [https://github.com/KenshiroTM/Doabot/issues](https://github.com/KenshiroTM/Doabot/issues)

---

*This bot is not affiliated with Discord Inc.*
