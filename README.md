# MemeOver Server Creator

A guided Python installer that sets up a self-hosted [MemeOver](https://github.com/SimonHazard/MemeOver) server on your machine — no technical knowledge required.

It will guide you to create a bot, and a local server to make it run with MemeOver.

> **MemeOver** is a desktop overlay app that lets friends send images, GIFs, videos, audio and text directly onto each other's screens via Discord. This installer sets up the **server component** only. The desktop app must be installed separately.

---

## Why this exists

The official MemeOver bot is hosted by its author and works out of the box, but cannot be added to new Discord servers once it reaches Discord's unverified bot limit (100 servers). This installer lets you run your own private bot instance so your friend group can use MemeOver independently.

---

## What it does

Runs you through a step-by-step terminal wizard that:

1. Asks where to create the server folder
2. Asks which port to use and explains how to open it (Windows Firewall + router NAT/PAT)
3. Guides you through creating a Discord bot on the Developer Portal
4. Collects your Discord Token and Client ID
5. Installs Bun (JavaScript runtime) if not already present
6. Clones the MemeOver source from GitHub
7. Installs dependencies
8. Generates a `Server.py` launcher
9. Walks you through the first launch and `/memeover setup`
10. Displays a ready-to-send connection block for your friends

The result is a clean folder structure:

```
MemeOver-Server/
├── MemeOver/    ← bot source (do not launch the app from here)
└── Server.py    ← double-click this to start the server
```

---

## Requirements

- **Windows** (tested on Windows 10/11)
- **Python 3.10+** (pre-installed on modern Windows)
- **Git** — [git-scm.com](https://git-scm.com)
- An internet connection

Bun is installed automatically if missing.

---

## Usage

1. Download [`MemeOverBotInstaller.py`](https://github.com/BlessEphraem/MemeOver-ServerCreator/releases)
2. Double-click it, or run it from a terminal:
   ```
   python MemeOverBotInstaller.py
   ```
3. Follow the on-screen instructions

---

## MemeOver desktop app

**[Download MemeOver →](https://github.com/SimonHazard/MemeOver/releases/latest)**

Once the server is running and `/memeover setup` has been done in Discord, open the app, enable **Expert Mode** in Bot Connection, and fill in the three fields shown at the end of the installer.

---

## Notes

- The server must be running for the overlay to work. Start it by double-clicking `Server.py`.
- Your friends connect using your **public IPv4 address** and the port you chose (default `3001`).
- You connect locally using `ws://localhost:3001/ws`.
- Port forwarding must be configured on your router (NAT/PAT, TCP, internal + external port identical).
- If you change your public IP (e.g. router reboot), share the new IP with your friends.

---

## License

This installer is an unofficial tool and is not affiliated with Simon Hazard or the MemeOver project. MemeOver itself is licensed under the [MIT License](https://github.com/SimonHazard/MemeOver/blob/main/LICENSE).
