param (
    [string]$awpath
)
$targetFilePath = "$awpath\dist\launcher.exe"
$arguments = ""
$shortcutName = "AnyWhere"
$shortcutDescription = "The universal userscript manager"
$iconPath = "$awpath\assets\A.ico"
$shortcutPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\$shortcutName.lnk"

$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetFilePath
$shortcut.Arguments = $arguments
$shortcut.Description = $shortcutDescription
$shortcut.IconLocation = $iconPath
$shortcut.Save()
