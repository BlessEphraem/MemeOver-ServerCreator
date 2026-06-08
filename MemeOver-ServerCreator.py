import os
import shutil
import subprocess
import sys


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


# ─────────────────────────────────────────────────────────────────────────────

print("""
 ╔══════════════════════════════════════════╗
 ║       MemeOver Bot - Installer           ║
 ║  Self-host your own bot in a few steps   ║
 ╚══════════════════════════════════════════╝

 Before you continue, here is what this installer will set up:

   MemeOver-Server/
   ├── MemeOver/       ← bot source code (server only, do not launch from here)
   └── Server.py       ← the script you will double-click to start the server

 The MemeOver desktop app is a SEPARATE program.
 Download and install it normally from:
   https://github.com/SimonHazard/MemeOver/releases/latest

 The "MemeOver" folder created here is NOT the app — it is only the
 server engine. Never try to run MemeOver from that folder.
 Always use the installed desktop app for the overlay.
""")
pause("  Press ENTER to start, or close this window to cancel...")

# ── STEP 1: Install directory ─────────────────────────────────────────────────
box("STEP 1 - Install location")
script_dir = os.path.dirname(os.path.abspath(__file__))
default_dir = os.path.join(script_dir, "MemeOver-Server")
info("Where do you want to create the MemeOver-Server folder?")
info(f"Default: {default_dir}")
info("(Press ENTER to use the default, or type a full path)\n")
server_root = input("  Install path: ").strip()
if not server_root:
    server_root = default_dir

install_dir = os.path.join(server_root, "MemeOver")
ok(f"Server folder : {server_root}")
ok(f"Bot source    : {install_dir}")

# ── STEP 2: WebSocket port ────────────────────────────────────────────────────
box("STEP 2 - WebSocket port")
info("The server communicates with the MemeOver app through a port.")
info("Default port: 3001 — press ENTER to keep it, or type another number.\n")
ws_port = input("  Port: ").strip()
if not ws_port:
    ws_port = "3001"
ok(f"Port set to: {ws_port}")

print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  ⚠  You must now open port {ws_port} in TWO places so your friends  │
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
  │       (the exact name depends on your router brand)              │
  │     → Add a rule with:                                           │
  │         Protocol      : TCP                                      │
  │         Internal port : {ws_port}                                        │
  │         External port : {ws_port}                                        │
  │         Destination IP: your PC's local IPv4 address             │
  │           (find it: Win+R → type cmd → type ipconfig             │
  │            → look for "IPv4 Address" under Ethernet or Wi-Fi)    │
  │                                                                  │
  │  Your public IP (to share with friends):                         │
  │     Open a terminal and run: curl -4 ifconfig.me                 │
  └──────────────────────────────────────────────────────────────────┘
""")
pause("  Press ENTER once you have opened the ports...")

# ── STEP 3: Discord bot creation guide ───────────────────────────────────────
box("STEP 3 - Create your Discord Bot")
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

# ── STEP 4: Credentials ───────────────────────────────────────────────────────
box("STEP 4 - Enter your Discord credentials")
info('Paste the TOKEN you copied from the "Bot" page:')
discord_token = input("  Discord Token: ").strip()
print()
info('Paste the APPLICATION ID you copied from "General Information":')
discord_client_id = input("  Client ID: ").strip()
print()

# ── STEP 5: Install Bun ───────────────────────────────────────────────────────
box("STEP 5 - Installing Bun")
bun_path = os.path.join(os.environ.get("USERPROFILE", ""), ".bun", "bin", "bun.exe")

if which("bun") or os.path.exists(bun_path):
    ok("Bun is already installed. Skipping.")
else:
    info("Installing Bun (JavaScript runtime)...")
    result = subprocess.run(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            "irm bun.sh/install.ps1 | iex",
        ],
        shell=False,
    )
    if result.returncode != 0:
        err("Failed to install Bun.")
        info("Please install it manually from https://bun.sh then re-run this script.")
        input("\nPress ENTER to exit.")
        sys.exit(1)
    ok("Bun installed.")

bun_bin = os.path.join(os.environ.get("USERPROFILE", ""), ".bun", "bin")
os.environ["PATH"] = bun_bin + os.pathsep + os.environ.get("PATH", "")

# ── STEP 6: Download the repo ─────────────────────────────────────────────────
box("STEP 6 - Downloading MemeOver server source")
if not which("git"):
    err("Git is not installed.")
    info("Please install it from https://git-scm.com then re-run this script.")
    input("\nPress ENTER to exit.")
    sys.exit(1)

os.makedirs(server_root, exist_ok=True)

if os.path.exists(install_dir):
    ok("Source folder already exists. Skipping download.")
else:
    info("Downloading from GitHub...")
    result = subprocess.run(
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

# ── STEP 7: Install dependencies ─────────────────────────────────────────────
box("STEP 7 - Installing dependencies")
os.chdir(install_dir)
bun_exe = bun_path if os.path.exists(bun_path) else "bun"
result = subprocess.run([bun_exe, "install"])
if result.returncode != 0:
    err("Failed to install dependencies.")
    input("\nPress ENTER to exit.")
    sys.exit(1)
ok("Dependencies installed.")

# ── Write .env ────────────────────────────────────────────────────────────────
env_path = os.path.join(install_dir, "bot", ".env")
with open(env_path, "w", encoding="utf-8") as f:
    f.write(f"DISCORD_TOKEN={discord_token}\n")
    f.write(f"DISCORD_CLIENT_ID={discord_client_id}\n")
    f.write(f"WS_PORT={ws_port}\n")
ok("Configuration file saved.")

# ── Generate Server.py ────────────────────────────────────────────────────────
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

# ── STEP 8: First launch ──────────────────────────────────────────────────────
box("STEP 8 - First launch")
print("""  Follow these steps IN ORDER — the order matters:

  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │  1. The server will start in a new window.                       │
  │     Wait until you see: "WebSocket server running"               │
  │                                                                  │
  │  2. Go to your Discord server and type in any channel:           │
  │        /memeover setup                                           │
  │     The bot will reply with your Server ID and Token.            │
  │     Note them down.                                              │
  │                                                                  │
  │  3. Close the server window.                                     │
  │                                                                  │
  │  4. Reopen Server.py (double-click it).                          │
  │     This is required so the server registers your Discord        │
  │     server properly before accepting connections.                │
  │                                                                  │
  │  5. Open the MemeOver desktop app and fill in the credentials.   │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
""")
pause("  Press ENTER to launch the server...")

subprocess.Popen(
    f'start "MemeOver Server" python "{server_script}"',
    shell=True,
)

print()
info("Server window opened.")
info("Run /memeover setup in Discord, note your Server ID and Token,")
info("then close and reopen Server.py before connecting the app.")
print()
pause("  Press ENTER once you have your Server ID and Token from Discord...")

# ── Collect credentials for the summary ──────────────────────────────────────
print()
info("Paste the values from the /memeover setup reply in Discord:\n")
guild_id = input("  Server ID: ").strip()
guild_token = input("  Token: ").strip()
print()
info("Retrieving your public IP automatically...")
try:
    import urllib.request

    public_ip = (
        urllib.request.urlopen("https://api4.my-ip.io/ip", timeout=5)
        .read()
        .decode()
        .strip()
    )
    ok(f"Public IP: {public_ip}")
except Exception:
    public_ip = ""
    err("Could not retrieve public IP. Replace YOUR_PUBLIC_IP manually in the summary.")

# ── STEP 9: Final summary ─────────────────────────────────────────────────────
ws_url_local = f"ws://localhost:{ws_port}/ws"
ws_url_public = (
    f"ws://{public_ip}:{ws_port}/ws"
    if public_ip
    else f"ws://YOUR_PUBLIC_IP:{ws_port}/ws"
)

print(f"""
 ╔══════════════════════════════════════════════════════════════════╗
 ║                                                                  ║
 ║   ✅  INSTALLATION COMPLETE                                      ║
 ║                                                                  ║
 ║   Your server folder:                                            ║
 ║   {server_root[:62]:<62} ║
 ║                                                                  ║
 ║   ├── MemeOver/   (server source — do not launch from here)      ║
 ║   └── Server.py   (double-click this to start the server)        ║
 ║                                                                  ║
 ╠══════════════════════════════════════════════════════════════════╣
 ║                                                                  ║
 ║   YOUR settings (MemeOver app → Expert Mode):                    ║
 ║                                                                  ║
 ║   WebSocket URL  →  {ws_url_local:<45} ║
 ║   Server ID      →  {guild_id:<45} ║
 ║   Token          →  {guild_token:<45} ║
 ║                                                                  ║
 ╠══════════════════════════════════════════════════════════════════╣
 ║                                                                  ║
 ║   SEND THIS TO YOUR FRIENDS:                                     ║
 ║                                                                  ║
 ║   Hey! To connect to my MemeOver server:                         ║
 ║   1. Download the app:                                           ║
 ║      https://github.com/SimonHazard/MemeOver/releases/latest     ║
 ║   2. Open the app → Bot Connection → enable Expert Mode          ║
 ║   3. Fill in:                                                    ║
 ║      WebSocket URL  →  {ws_url_public:<41} ║
 ║      Server ID      →  {guild_id:<41} ║
 ║      Token          →  {guild_token:<41} ║
 ║   4. Click Save & Connect                                        ║
 ║                                                                  ║
 ╚══════════════════════════════════════════════════════════════════╝
""")
input("  Press ENTER to exit.")
