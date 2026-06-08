import json
import os
import shutil
import subprocess
import sys
import urllib.request


# ── Helpers ───────────────────────────────────────────────────────────────────
def box(title):
    print(f"\n {'═' * 50}")
    print(f"   {title}")
    print(f" {'═' * 50}\n")


def ok(msg):
    print(f"  [OK] {msg}")


def err(msg):
    print(f"  [ERROR] {msg}")


def info(msg):
    print(f"  {msg}")


def pause(msg="  Press ENTER to continue..."):
    input(msg)


def which(cmd):
    return shutil.which(cmd) is not None


def choose(prompt, options):
    """Simple numbered menu. Returns the index (0-based)."""
    print(f"\n  {prompt}\n")
    for i, opt in enumerate(options, 1):
        print(f"    {i}) {opt}")
    print()
    while True:
        raw = input("  Your choice: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw) - 1
        print("  Invalid choice, try again.")


def get_public_ip():
    try:
        ip = (
            urllib.request.urlopen("https://api4.my-ip.io/ip", timeout=5)
            .read()
            .decode()
            .strip()
        )
        ok(f"Public IP: {ip}")
        return ip
    except Exception:
        err("Could not retrieve public IP automatically.")
        return input("  Enter your public IP manually: ").strip()


def run(cmd, **kwargs):
    return subprocess.run(cmd, **kwargs)


def popen(cmd):
    subprocess.Popen(cmd, shell=True)


# ── Shared: Discord bot guide + credentials ───────────────────────────────────
def discord_bot_guide():
    box("Create your Discord Bot")
    print("""  You need to create a bot on the Discord Developer Portal.
  Follow these steps carefully:

  ┌──────────────────────────────────────────────────────────────────┐
  │  A) Go to: https://discord.com/developers/applications           │
  │     Click "New Application" (top right)                          │
  │     Give it any name (e.g. "MemeOver") → click "Create"          │
  │                                                                  │
  │  B) In the left menu, click "Bot"                                │
  │     Click "Reset Token" → confirm → COPY the token               │
  │     (you will paste it in this script in a moment)               │
  │                                                                  │
  │  C) Still on the "Bot" page, scroll down to:                     │
  │     "Privileged Gateway Intents"                                 │
  │     Enable ALL THREE of these:                                   │
  │       ✅  PRESENCE INTENT                                        │
  │       ✅  SERVER MEMBERS INTENT                                  │
  │       ✅  MESSAGE CONTENT INTENT                                 │
  │     Click "Save Changes"                                         │
  │                                                                  │
  │  D) In the left menu, click "General Information"                │
  │     Copy the "Application ID" (also called Client ID)            │
  │     (you will paste it in this script in a moment)               │
  │                                                                  │
  │  E) Invite the bot to your Discord server:                       │
  │     In the left menu, click "OAuth2" → "URL Generator"           │
  │     Under "Scopes", check: bot + applications.commands           │
  │     Under "Bot Permissions", check: Administrator                │
  │     Copy the generated URL at the bottom → open it in browser    │
  │     Select your server → Authorize                               │
  └──────────────────────────────────────────────────────────────────┘
""")
    pause("  Press ENTER once you have done all of the above...")


def discord_credentials():
    box("Enter your Discord credentials")
    info('Paste the TOKEN you copied from the "Bot" page:')
    token = input("  Discord Token: ").strip()
    print()
    info('Paste the APPLICATION ID you copied from "General Information":')
    client_id = input("  Client ID: ").strip()
    print()
    return token, client_id


def discord_setup_credentials():
    box("Retrieve your Server ID and Token")
    print("""  In your Discord server, type this command in any channel:

     /memeover setup

  The bot will reply with your Server ID and Token.
  Note them down, then come back here.
""")
    pause("  Press ENTER once you have run /memeover setup...")
    print()
    info("Paste the values from the /memeover setup reply:\n")
    guild_id = input("  Server ID: ").strip()
    guild_token = input("  Token: ").strip()
    return guild_id, guild_token


# ══════════════════════════════════════════════════════════════════════════════
#   MODE A — LOCAL
# ══════════════════════════════════════════════════════════════════════════════
def mode_local():
    box("LOCAL SERVER SETUP")

    # Install directory
    box("STEP 1 - Install location")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_dir = os.path.join(script_dir, "MemeOver-Server")
    info("Where do you want to create the MemeOver-Server folder?")
    info(f"Default: {default_dir}")
    info("(Press ENTER to use the default, or type a full path)\n")
    server_root = input("  Install path: ").strip().strip('"') or default_dir
    install_dir = os.path.join(server_root, "MemeOver")
    ok(f"Server folder : {server_root}")
    ok(f"Bot source    : {install_dir}")

    # Port
    box("STEP 2 - WebSocket port")
    info("The server communicates with the MemeOver app through a port.")
    info("Default port: 3001 — press ENTER to keep it, or type another number.\n")
    ws_port = input("  Port: ").strip() or "3001"
    ok(f"Port set to: {ws_port}")

    print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  ⚠  You must open port {ws_port} in TWO places so your friends      │
  │     can connect to your server remotely.                         │
  │                                                                  │
  │  1. Windows Firewall                                             │
  │     → Search "Windows Defender Firewall" in the Start menu       │
  │     → Click "Advanced Settings" on the left                      │
  │     → "Inbound Rules" → "New Rule..." → choose "Port" → Next     │
  │     → Select TCP → type {ws_port} → Next                             │
  │     → "Allow the connection" → Next → Next → give it a name      │
  │                                                                  │
  │  2. Your router / internet box (NAT/PAT port forwarding)         │
  │     → Open your router admin page (usually http://192.168.1.1)   │
  │     → Find "NAT/PAT", "Port Forwarding" or "Redirections"        │
  │     → Add a rule with:                                           │
  │         Protocol      : TCP                                      │
  │         Internal port : {ws_port}                                        │
  │         External port : {ws_port}                                        │
  │         Destination IP: your PC's local IPv4 address             │
  │           (Win+R → cmd → ipconfig → IPv4 Address)                │
  └──────────────────────────────────────────────────────────────────┘
""")
    pause("  Press ENTER once you have opened the ports...")

    # Discord
    discord_bot_guide()
    discord_token, discord_client_id = discord_credentials()

    # Bun
    box("STEP 5 - Installing Bun")
    bun_path = os.path.join(os.environ.get("USERPROFILE", ""), ".bun", "bin", "bun.exe")
    if which("bun") or os.path.exists(bun_path):
        ok("Bun is already installed. Skipping.")
    else:
        info("Installing Bun...")
        result = run(
            [
                "powershell",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                "irm bun.sh/install.ps1 | iex",
            ]
        )
        if result.returncode != 0:
            err("Failed to install Bun. Install manually from https://bun.sh")
            input("\nPress ENTER to exit.")
            sys.exit(1)
        ok("Bun installed.")
    bun_bin = os.path.join(os.environ.get("USERPROFILE", ""), ".bun", "bin")
    os.environ["PATH"] = bun_bin + os.pathsep + os.environ.get("PATH", "")

    # Clone
    box("STEP 6 - Downloading MemeOver server source")
    if not which("git"):
        err("Git is not installed. Install from https://git-scm.com")
        input("\nPress ENTER to exit.")
        sys.exit(1)
    os.makedirs(server_root, exist_ok=True)
    if os.path.exists(install_dir):
        ok("Source folder already exists. Skipping download.")
    else:
        info("Downloading from GitHub...")
        result = run(
            [
                "git",
                "clone",
                "--depth=1",
                "https://github.com/SimonHazard/MemeOver",
                install_dir,
            ]
        )
        if result.returncode != 0:
            err("Download failed. Check your internet connection.")
            input("\nPress ENTER to exit.")
            sys.exit(1)
        ok("Downloaded successfully.")

    # Dependencies
    box("STEP 7 - Installing dependencies")
    os.chdir(install_dir)
    bun_exe = bun_path if os.path.exists(bun_path) else "bun"
    result = run([bun_exe, "install"])
    if result.returncode != 0:
        err("Failed to install dependencies.")
        input("\nPress ENTER to exit.")
        sys.exit(1)
    ok("Dependencies installed.")

    # .env
    env_path = os.path.join(install_dir, "bot", ".env")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(f"DISCORD_TOKEN={discord_token}\n")
        f.write(f"DISCORD_CLIENT_ID={discord_client_id}\n")
        f.write(f"WS_PORT={ws_port}\n")
    ok("Configuration file saved.")

    # Generate Server.py
    server_script = os.path.join(server_root, "Server.py")
    with open(server_script, "w", encoding="utf-8") as f:
        f.write(f'''import os
import subprocess

bun_bin = os.path.join(os.environ.get("USERPROFILE", ""), ".bun", "bin")
os.environ["PATH"] = bun_bin + os.pathsep + os.environ.get("PATH", "")
bot_dir = r"{os.path.join(install_dir, "bot")}"

print("""
 ╔══════════════════════════════════════════╗
 ║   MemeOver Server is running             ║
 ║   Keep this window open!                 ║
 ║   Close it to stop the server.           ║
 ╚══════════════════════════════════════════╝
""")

os.chdir(bot_dir)
bun_exe = os.path.join(bun_bin, "bun.exe")
if not os.path.exists(bun_exe):
    bun_exe = "bun"

try:
    subprocess.run([bun_exe, "run", "dev"])
except KeyboardInterrupt:
    print("\\n  Server stopped.")

input("\\n  Press ENTER to exit.")
''')
    ok(f"Server.py created in: {server_root}")

    # First launch
    box("STEP 8 - First launch")
    print("""  Follow these steps IN ORDER — the order matters:

  ┌──────────────────────────────────────────────────────────────────┐
  │  1. The server will start in a new window.                       │
  │     Wait until you see: "WebSocket server running"               │
  │                                                                  │
  │  2. Go to your Discord server and type:  /memeover setup         │
  │     Note down the Server ID and Token from the reply.            │
  │                                                                  │
  │  3. Close the server window, then reopen Server.py.              │
  │     This registers your Discord server before accepting          │
  │     connections.                                                 │
  │                                                                  │
  │  4. Open the MemeOver desktop app and fill in the credentials.   │
  └──────────────────────────────────────────────────────────────────┘
""")
    pause("  Press ENTER to launch the server...")
    popen(f'start "MemeOver Server" python "{server_script}"')
    print()
    info("Server window opened.")
    print()
    pause(
        "  Press ENTER once you have run /memeover setup and noted your credentials..."
    )

    guild_id, guild_token = discord_setup_credentials()

    info("Retrieving your public IP automatically...")
    public_ip = get_public_ip()

    ws_url_local = f"ws://localhost:{ws_port}/ws"
    ws_url_public = (
        f"ws://{public_ip}:{ws_port}/ws"
        if public_ip
        else f"ws://YOUR_PUBLIC_IP:{ws_port}/ws"
    )

    print(f"""
 ╔══════════════════════════════════════════════════════════════════╗
 ║                                                                  ║
 ║   ✅  LOCAL SERVER READY                                         ║
 ║                                                                  ║
 ║   {server_root[:62]:<62} ║
 ║   ├── MemeOver/   (server source — do not launch from here)      ║
 ║   └── Server.py   (double-click this to start the server)        ║
 ║                                                                  ║
 ╠══════════════════════════════════════════════════════════════════╣
 ║                                                                  ║
 ║   YOUR settings (MemeOver app → Expert Mode):                    ║
 ║   WebSocket URL  →  {ws_url_local:<45} ║
 ║   Server ID      →  {guild_id:<45} ║
 ║   Token          →  {guild_token:<45} ║
 ║                                                                  ║
 ╠══════════════════════════════════════════════════════════════════╣
 ║                                                                  ║
 ║   SEND THIS TO YOUR FRIENDS:                                     ║
 ║   1. Download: https://github.com/SimonHazard/MemeOver/releases  ║
 ║   2. App → Bot Connection → Expert Mode                          ║
 ║   3. Fill in:                                                    ║
 ║      WebSocket URL  →  {ws_url_public:<41} ║
 ║      Server ID      →  {guild_id:<41} ║
 ║      Token          →  {guild_token:<41} ║
 ║   4. Click Save & Connect                                        ║
 ║                                                                  ║
 ╚══════════════════════════════════════════════════════════════════╝
""")


# ══════════════════════════════════════════════════════════════════════════════
#   MODE B — ONLINE: existing server
# ══════════════════════════════════════════════════════════════════════════════
def mode_online_existing():
    box("ONLINE — EXISTING SERVER")
    print("""  You already have a server (VPS, cloud VM, etc.) with SSH access.
  This script will connect to it, install the bot, and configure everything.
""")

    info("Enter your server's connection details:\n")
    ssh_host = input("  Server IP or hostname: ").strip()
    ssh_user = input("  SSH username (e.g. ubuntu, root): ").strip()
    ssh_key = input(
        "  Path to your SSH private key (press ENTER if using password): "
    ).strip()

    ws_port = input("\n  WebSocket port [press ENTER for 3001]: ").strip() or "3001"

    discord_bot_guide()
    discord_token, discord_client_id = discord_credentials()

    # Build SSH command base
    ssh_base = ["ssh"]
    if ssh_key:
        ssh_base += ["-i", ssh_key]
    ssh_base += [f"{ssh_user}@{ssh_host}"]

    def ssh(cmd):
        return run(ssh_base + [cmd])

    def ssh_check(cmd, label):
        info(f"Running on server: {label}...")
        result = ssh(cmd)
        if result.returncode != 0:
            err(f"Failed: {label}")
            input("\nPress ENTER to exit.")
            sys.exit(1)
        ok(label)

    box("Connecting and setting up the server")
    info("Testing SSH connection...")
    result = ssh("echo ok")
    if result.returncode != 0:
        err("Could not connect via SSH. Check your credentials and try again.")
        input("\nPress ENTER to exit.")
        sys.exit(1)
    ok("SSH connection successful.")

    ssh_check(
        "sudo apt-get update -qq && sudo apt-get install -y -qq git curl unzip",
        "System packages",
    )
    ssh_check("curl -fsSL https://bun.sh/install | bash", "Bun installation")
    ssh_check(
        f"git clone --depth=1 https://github.com/SimonHazard/MemeOver /opt/memeover 2>/dev/null || git -C /opt/memeover pull",
        "MemeOver source",
    )
    ssh_check("cd /opt/memeover && ~/.bun/bin/bun install", "Dependencies")

    env_content = f"DISCORD_TOKEN={discord_token}\\nDISCORD_CLIENT_ID={discord_client_id}\\nWS_PORT={ws_port}\\n"
    ssh_check(f"printf '{env_content}' > /opt/memeover/bot/.env", "Configuration file")

    # Systemd service
    service = f"""[Unit]
Description=MemeOver Bot
After=network.target

[Service]
Type=simple
User={ssh_user}
WorkingDirectory=/opt/memeover/bot
ExecStart=/root/.bun/bin/bun run dev
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target"""

    ssh_check(
        f"printf '{service}' | sudo tee /etc/systemd/system/memeover.service > /dev/null && sudo systemctl daemon-reload && sudo systemctl enable memeover && sudo systemctl restart memeover",
        "Systemd service (auto-start)",
    )

    info("Waiting for the bot to start...")
    import time

    time.sleep(5)

    box("Run /memeover setup in Discord")
    print("""  The bot is now running on your server.
  Go to your Discord server and type:

     /memeover setup

  Note down the Server ID and Token from the reply.
""")
    pause("  Press ENTER once you have done /memeover setup...")

    guild_id, guild_token = discord_setup_credentials()

    ssh_check("sudo systemctl restart memeover", "Server restarted")

    ws_url = f"wss://{ssh_host}:{ws_port}/ws"

    print(f"""
 ╔══════════════════════════════════════════════════════════════════╗
 ║                                                                  ║
 ║   ✅  ONLINE SERVER READY                                        ║
 ║                                                                  ║
 ║   The bot runs 24/7 on your server and restarts automatically.  ║
 ║                                                                  ║
 ╠══════════════════════════════════════════════════════════════════╣
 ║                                                                  ║
 ║   YOUR settings (MemeOver app → Expert Mode):                    ║
 ║   WebSocket URL  →  {ws_url:<45} ║
 ║   Server ID      →  {guild_id:<45} ║
 ║   Token          →  {guild_token:<45} ║
 ║                                                                  ║
 ╠══════════════════════════════════════════════════════════════════╣
 ║                                                                  ║
 ║   SEND THIS TO YOUR FRIENDS:                                     ║
 ║   1. Download: https://github.com/SimonHazard/MemeOver/releases  ║
 ║   2. App → Bot Connection → Expert Mode                          ║
 ║   3. Fill in:                                                    ║
 ║      WebSocket URL  →  {ws_url:<41} ║
 ║      Server ID      →  {guild_id:<41} ║
 ║      Token          →  {guild_token:<41} ║
 ║   4. Click Save & Connect                                        ║
 ║                                                                  ║
 ╚══════════════════════════════════════════════════════════════════╝
""")


# ══════════════════════════════════════════════════════════════════════════════
#   MAIN
# ══════════════════════════════════════════════════════════════════════════════
print("""
 ╔══════════════════════════════════════════╗
 ║       MemeOver Server Creator            ║
 ║  Self-host your own bot in a few steps   ║
 ╚══════════════════════════════════════════╝

 The MemeOver desktop app is a SEPARATE program.
 Download and install it normally from:
   https://github.com/SimonHazard/MemeOver/releases/latest

 This script sets up the SERVER only — not the app.
""")
pause("  Press ENTER to start, or close this window to cancel...")

mode = choose(
    "Where do you want to host the server?",
    [
        "Local  — runs on this PC (your PC must stay on for friends to connect)",
        "Online — I already have a remote server (VPS, cloud VM, etc.)",
    ],
)

if mode == 0:
    mode_local()
else:
    mode_online_existing()

input("\n  Press ENTER to exit.")
