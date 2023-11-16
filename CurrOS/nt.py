import os

appdata_path = os.path.join(os.getenv("APPDATA"))


def setProxy(host, port):
    # set system proxy for windows
    import winreg

    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    key = winreg.OpenKey(
        registry,
        r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        0,
        winreg.KEY_WRITE,
    )
    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, f"{host}:{port}")
    winreg.CloseKey(key)
    winreg.CloseKey(registry)


def clearProxy():
    # clear system proxy for windows
    import winreg

    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    key = winreg.OpenKey(
        registry,
        r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        0,
        winreg.KEY_WRITE,
    )
    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)
    winreg.CloseKey(registry)
