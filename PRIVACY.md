# Privacy Policy for Doabot

**Last updated:** 21 August 2026

## 1. Introduction
This Privacy Policy explains how Doabot ("we", "our", "the bot") collects, uses, and protects data when operating within Discord servers. By participating in Doaenel's Discord server where Doabot operates, you agree to the practices described in this policy.

Doabot is a Discord moderation bot created for streamer Doaenel and his community. We are committed to handling data responsibly and transparently.

## 2. Data We Collect
Doabot collects only the minimum data necessary for its core functionality. All data is obtained through Discord's official API.

### 2.1 User IDs & Usernames
*   **Purpose:** Track users for the ban reversal functionality and moderation actions.
*   **Examples:** User IDs and usernames of the 3 most recently banned users.
*   **Storage:** Stored in local JSON files on the host machine.

### 2.2 Server IDs
*   **Purpose:** Bot is hardcoded to operate exclusively in Doaenel's Discord server (ID: `713475017957965945`). The server ID acts as a hard lock — the bot will not respond to events or commands in any other server.
*   **Storage:** Stored in local JSON files on the host machine.

### 2.3 Message Content
*   **Purpose:** Real-time processing for anti-spam detection, blacklist keyword matching, and link fixing.
*   **Important:** Message content is processed in real-time only and is **not permanently stored**. The bot reads message text to identify spam patterns or prohibited words, but does not save this text to any database.
*   **Exception:** The `/expose` command temporarily stores the content of deleted messages in memory/local cache for moderation review. These entries are automatically deleted after the configured duration (default: 1–24 hours).

### 2.4 What We Do NOT Collect
*   We do not collect email addresses, passwords, or personal information outside of Discord.
*   We do not log or store full message history.
*   We do not track user activity (presence/status) outside of direct moderation needs.
*   We do not use cookies or tracking pixels.
*   We do not operate in multiple servers. Doabot is restricted to a single Discord server.

## 3. How We Use Your Data

| Data Type | Purpose |
| :--- | :--- |
| User IDs & usernames | Ban reversal tracking, moderation commands (`/ban`, `/warn`) |
| Server ID | Hardcoded server restriction — bot operates exclusively in one server |
| Message content (real-time) | Anti-spam filtering, blacklist enforcement, link fixing |

## 4. Data Storage & Security
*   All data is stored in local JSON files on the private server hosting the bot.
*   Data is not transmitted to any third-party services except Discord's API, which is required for the bot to function.
*   Access to the bot's host machine is restricted to the bot owner.

## 5. Data Retention

| Data Type | Retention Period |
| :--- | :--- |
| User IDs (bans) & usernames | Only the 3 most recent bans are kept; older entries are overwritten |
| Message content (expose) | Automatically deleted after the configured `expose_delete_hours` (default: 1 hour) |
| Warnings | Stored indefinitely until manually cleared by an administrator via `/clearwarns` |

## 6. Data Sharing
We do not sell, trade, rent, or share user data with any third parties. Data is only shared with Discord Inc. as required for the bot to function via Discord's API.

## 7. Your Rights
As a user of Doaenel's Discord server, you have the right to:
*   **Request data deletion:** Contact the bot owner. Note that most data is dynamically generated and tied to active server participation.
*   **Access your data:** Request a copy of the data we hold about you (e.g., your warning history).

To exercise these rights, contact:
*   **Discord:** KenshiroTM
*   **Email:** kenshirotm@gmail.com
*   **GitHub Issues:** [https://github.com/KenshiroTM/Doabot/issues](https://github.com/KenshiroTM/Doabot/issues)

## 8. Children's Privacy
Doabot is not intended for use by individuals under the age of 13 (or the minimum age required by Discord in your region). We do not knowingly collect data from children.

## 9. Changes to This Policy
We may update this Privacy Policy from time to time. Changes will be posted on this page with an updated "Last updated" date. Continued use of the bot after changes constitutes acceptance of the revised policy.

## 10. Contact
For privacy-related questions, data deletion requests, or concerns:
*   **Discord:** KenshiroTM
*   **Email:** kenshirotm@gmail.com
*   **GitHub Issues:** [https://github.com/KenshiroTM/Doabot/issues](https://github.com/KenshiroTM/Doabot/issues)

*This bot is not affiliated with Discord Inc.*
