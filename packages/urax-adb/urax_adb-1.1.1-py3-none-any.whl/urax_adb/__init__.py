import subprocess
import os
import argparse
from colorama import Fore, init

init(autoreset=True)

VERSION = "1.1.1"

print(f"urax_adb v{VERSION}\n")

def adbNonExistent():
    print(f"{Fore.RED}adb not found. Make sure you have it configured properly in system Environment Variables or configure it manually with adbpath()")

adb_path = subprocess.run("where adb", capture_output=True, text=True)
if adb_path.returncode == 0:
    adb_path = adb_path.stdout.strip()
else:
    adb_path = ""
    adbNonExistent()

def adbpath(path):
    """Configure path for adb manually
    `path`: Path to adb
    """
    global adb_path
    if adb_path is not None:
        confirm = input(f"{Fore.YELLOW}adb path has been set automatically ({adb_path}). Do you want to change the path of adb? (Y/n): ")

        if confirm.lower() == "y":
            if os.path.exists(path):
                adb_path = path
                print(f"{Fore.GREEN}Custom adb path configuration successful!\n")
            else:
                print(f"{Fore.RED}adb path not found. Please try again!\n")
        else:
            print(f"{Fore.RED}Cancelled\n")
    else:
        if os.path.exists(path):
            adb_path = path
            return "Configured"
        else:
            return "Non-existent"

def connect(device, type="USB", port=5555):
    """Connect to device
    `device`: IP address or Device name
    `type`: Connection type, USB or TCP (Default: USB)
    `port`: Port number (Default: 5555)
    """
    if adb_path == "":
        adbNonExistent()
    else:
        if type.lower() == "usb":
            subprocess.run(f"{adb_path} connect {device}", shell=True)
        elif type.lower() == "tcp":
            subprocess.run(f"{adb_path} connect {device}:{port}", shell=True)
        else:
            print(f"{Fore.RED}Invalid connection type")

def disconnect(device):
    """Disconnect from device
    `device`: IP address or Device name
    """
    if adb_path == "":
        adbNonExistent()
    else:
        subprocess.run(f"{adb_path} disconnect {device}", shell=True)

def devices():
    """List all connected devices"""
    if adb_path == "":
        adbNonExistent()
    else:
        subprocess.run(f"{adb_path} devices", shell=True)

def shell(shell_commands):
    """Execute multiple adb shell commands
    `shell_commands`: List of shell commands
    """
    if adb_path == "":
        adbNonExistent()
    else:
        command_str = "; ".join(shell_commands)
        subprocess.run(f"{adb_path} shell \"{command_str}\"", shell=True)

def execute(command):
    """Execute a adb command
    `command`: Execution command
    """
    if adb_path == "":
        adbNonExistent()
    else:
        if "adb connect" in command:
            print(f"{Fore.RED}You should use 'connect()' to connect to the Android device when using urax_adb")
        subprocess.run(command, shell=True)

def main():
    """Note: Do not use this function in your code. This is only for command line tool"""
    parser = argparse.ArgumentParser(description="urax_adb command line tool")
    parser.add_argument("command", choices=["adbpath", "version"], help="Command to execute")
    parser.add_argument("path", nargs="?", help="Path to adb (required for adbpath command)")

    args = parser.parse_args()

    if args.command == "version":
        print(f"{Fore.GREEN}urax_adb v{VERSION}")
    elif args.command == "adbpath":
        if args.path:
            result = adbpath(args.path)
            print(result)
        else:
            print(f"{Fore.RED}Path to adb is required for adbpath command")

if __name__ == "__main__":
    main()