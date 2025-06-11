import keyboard
import subprocess
import webbrowser
import os
import json
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# ==== Setup ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(BASE_DIR, "config.json")

hotkey_refs = []


# ==== Action Handler ====
def handle_action(action):
    if action.startswith("http"):
        webbrowser.open(action)
    elif os.path.isdir(action):
        os.startfile(action)
    else:
        try:
            subprocess.Popen(action, shell=True)

            # subprocess.Popen(action)
        except Exception as e:
            pass


# ==== Register Hotkeys ====
def register_hotkeys():
    global hotkey_refs
    # Unregister previous hotkeys
    for ref in hotkey_refs:
        keyboard.remove_hotkey(ref)
    hotkey_refs = []
    with open(config_path, "r") as f:
        shortcuts = json.load(f)
    for hotkey, action in shortcuts.items():
        ref = keyboard.add_hotkey(hotkey, handle_action, args=(action,))
        hotkey_refs.append(ref)


# ==== System Tray ====
def create_icon_image():
    img = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(img)
    draw.rectangle((16, 16, 48, 48), fill="white")
    return img


def on_exit(icon, item):
    icon.stop()
    os._exit(0)


def on_reload(icon, item):
    register_hotkeys()


def on_open_editor(icon, item):
    subprocess.Popen(["python", os.path.join(BASE_DIR, "hotkey_editor.py")])


def run_tray_icon():
    icon = Icon("HotkeyLauncher")
    icon.icon = create_icon_image()
    icon.title = "Hotkey Launcher"
    icon.menu = Menu(
        MenuItem("Open Config Editor", on_open_editor),
        MenuItem("Reload", on_reload),
        MenuItem("Exit", on_exit),
    )
    icon.run()


register_hotkeys()

# Start tray icon in background
threading.Thread(target=run_tray_icon, daemon=True).start()


# ==== Keep Running Forever ====
try:
    while True:
        pass
except KeyboardInterrupt:
    pass
