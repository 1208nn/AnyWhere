# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=invalid-name,consider-using-f-string
import winreg


with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:
    with winreg.CreateKeyEx(
        root, r"Software\Classes\anywhere", 0, winreg.KEY_WRITE
    ) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "URL:anywhere")
        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")

    with winreg.CreateKeyEx(
        root, r"Software\Classes\anywhere\shell\open\command", 0, winreg.KEY_WRITE
    ) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ,
            f'"{__file__.replace('protocol-install-win.py',r'dist\AnyWhere.exe')}" "%1"')
