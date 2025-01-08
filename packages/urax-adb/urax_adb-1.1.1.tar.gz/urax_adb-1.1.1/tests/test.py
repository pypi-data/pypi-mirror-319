import urax_adb as adb

adb.adbpath("D:\\platform-tools\\adb.exe")
adb.connect("cbbcbcb", "usb")
adb.disconnect("cbbcbcb")
adb.devices()
adb.shell(["ls", "cd /sdcard"])
adb.execute("adb version")