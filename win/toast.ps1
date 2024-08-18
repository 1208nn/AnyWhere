param (
  [string]$awpath,
  [string]$scriptname,
  [string]$scriptfilename
)

$targetFilePath = "$awpath\dist\AnyWhere.exe"
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

$xml = @"
<toast>
  <visual>
    <binding template="ToastGeneric">
      <text>New Userscript Detected</text>
      <text>Click to check $scriptname.`nYou can also`ninstall👇 it directly, or 👇dismiss it.`nRight click for mute.</text>
      <image placement='appLogoOverride' src='$awpath\assets\A.png'/>
    </binding>
  </visual>
  <actions>
    <action activationType='protocol' content='✔ Install' arguments='anywhere:install/$scriptfilename'/>
    <action activationType='protocol' content='❌ Dismiss' arguments='anyhwere:dismiss/$scriptfilename'/>
  </actions>
</toast>
"@
$XmlDocument = [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime]::New()
$XmlDocument.loadXml($xml)

$AppId = "$awpath\dist\AnyWhere.exe"

[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
$Toast = [Windows.UI.Notifications.ToastNotification]::new($XmlDocument)
$Toast.ExpirationTime = [DateTimeOffset]::Now.AddMinutes(1)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($AppId).Show($Toast)

#[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]::CreateToastNotifier($AppId).Show($XmlDocument)
