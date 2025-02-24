
# WindowsRPC++

A Discord RPC application that displays system stats such as RAM usage, active window, and uptime in the system tray. The app updates your Discord status with this information.

## Features

- Displays system stats (RAM, active window, uptime) in Discord status.
- Customizable tray icon and tooltip.
- Clickable tray icon with a quit option.
- Optionally shows a link to download Windows 11.

## Requirements

- Python 3.x
- `pystray` - For creating the system tray icon.
- `pywinctl` - To get the active window.
- `psutil` - For system stats (RAM usage, uptime).
- `pypresence` - To update Discord status.
- `Pillow` - For image processing.

## Installation

1. Clone the repository or download the source code.
2. Install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. Replace `CLIENT_ID` with your Discord application's Client ID in the code.
4. Ensure that `icon.png` is placed in the `resources` folder.

## Usage

1. Run the script using Python:
   
   ```bash
   python main.py
   ```

2. The application will run in the system tray and update your Discord status with system information.

3. Right-click the tray icon to quit the application.

## Building the EXE

To create a standalone EXE (without a console window):

1. Install `pyinstaller`:

   ```bash
   pip install pyinstaller
   ```

2. Build the EXE with this command:

   ```bash
   pyinstaller --onefile --noconsole --icon=resources/icon.ico main.py
   ```

   This will generate an executable in the `dist` folder.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.