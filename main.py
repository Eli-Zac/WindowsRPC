import time
import psutil
import pywinctl
from pypresence import Presence
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import pkg_resources
import threading
import os

# Replace with your Discord application's Client ID
CLIENT_ID = "1343190535585665024"

# Connect to Discord's local IPC
def connect_rpc():
    try:
        rpc = Presence(CLIENT_ID)
        rpc.connect()
        print("Connected to Discord RPC")
        return rpc
    except Exception as e:
        print("Failed to connect to Discord RPC:", e)
        exit(1)

rpc = connect_rpc()

# Windows logo (must be uploaded as an asset in your Discord Developer Portal)
LARGE_IMAGE_KEY = "https://i.imgur.com/MX5mtCn_d.webp?maxwidth=760&fidelity=grand"  # Make sure this matches the key from the portal

def get_system_stats():
    """ Get RAM usage, active window title, and uptime """
    # Get RAM usage and total
    ram_usage = psutil.virtual_memory().percent
    ram_total_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # Convert bytes to GB
    ram_used_gb = round(psutil.virtual_memory().used / (1024 ** 3), 2)  # Convert bytes to GB

    # Get the active window
    active_window = pywinctl.getActiveWindow()
    window_title = active_window.title if active_window else "No Active Window"

    # Get system uptime
    boot_time = psutil.boot_time()  # Time when the system was booted
    uptime_seconds = int(time.time() - boot_time)  # Time in seconds since boot
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))  # Format as hours:minutes:seconds

    return ram_usage, ram_used_gb, ram_total_gb, window_title, boot_time

# Function to create an icon image
def create_image():
    # Access the bundled image 'icon.png' from the 'resources' folder
    image_path = pkg_resources.resource_filename(
        __name__, 'resources/icon.png')  # Make sure your image is in the 'resources' folder
    image = Image.open(image_path)
    image = image.resize((64, 64))  # Ensure the icon is 64x64 pixels
    return image

# Function to update Discord status
def update_rpc():
    global rpc  # Ensure we're using the global rpc variable

    while True:
        try:
            # Get system stats
            ram, ram_used_gb, ram_total_gb, window, boot_time = get_system_stats()

            # New state string
            new_state = f"Window: {window}"
            new_details = f"RAM: {ram_used_gb}GB/{ram_total_gb}GB ({ram}%)"

            try:
                # Update the RPC with the new system stats and uptime as the timestamp
                rpc.update(
                    state=new_state,
                    details=new_details,
                    large_image=LARGE_IMAGE_KEY,
                    large_text="Windows",  # Optional description of the large image
                    start=int(boot_time),  # Set the start time to the boot time to show uptime as timestamp
                    buttons=[  # Adding the button with a link
                        {"label": "Download Windows", "url": "https://www.microsoft.com/en-au/software-download/windows11"}  # Replace with your URL
                    ]
                )
            except Exception as e:
                print(f"Error updating RPC: {e}")
                rpc = connect_rpc()  # Reconnect if update fails

            time.sleep(5)  # Update every 5 seconds

        except Exception as e:
            print("Error:", e)
            time.sleep(5)  # Retry after 5 seconds

# Function to quit the tray application
def quit_action(icon, item):
    icon.stop()
    os._exit(0)

# Function to set up the system tray
def setup_tray():
    icon = pystray.Icon("Discord RPC Tray", create_image(), title="WindowsRPC++", menu=(
        (item("Quit", quit_action),)  # Notice the trailing comma to make it a tuple
    ))
    # Start the tray icon in a separate thread
    icon_thread = threading.Thread(target=icon.run)
    icon_thread.daemon = True
    icon_thread.start()

# Run tray and RPC in parallel
def run():
    # Start tray icon
    setup_tray()

    # Start updating Discord RPC
    update_rpc()

if __name__ == "__main__":
    run()
