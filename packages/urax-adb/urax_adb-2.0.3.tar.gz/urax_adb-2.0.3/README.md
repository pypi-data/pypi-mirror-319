# Urax ADB
![PyPI](https://img.shields.io/pypi/v/urax-adb?label=pypi%20package) ![PyPI - Downloads](https://img.shields.io/pypi/dm/urax-adb)
Running adb on Python made it easier.

# Installation
To install with `pip`, run the command:
```bash
pip install urax_adb
```

For specific versions, run the command:
```bash
pip install urax_adb==<VERSION>
```

# Functions
| Functions | Feature |
|:-:|:-:|
| `urax_adb.connect(device, type, port)` | Connect to device |
| `urax_adb.disconnect(device)` | Disconnect from device |
| `urax_adb.devices()` | List all connected devices |
| `urax_adb.shell(shell_commands)` | Execute multiple adb shell commands |
| `urax_adb.execute(command)` | Execute a adb command |
