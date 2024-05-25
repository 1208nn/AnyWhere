param (
  [string]$awpath,
  [string]$scriptname
)
$xml = @"
<toast>
  <visual>
    <binding template="ToastGeneric">
      <text>New Userscript Detected</text>
      <text>Click to check $scriptname.`nYou can also`ninstall👇 it directly, or 👇ignore it.</text>
      <image placement='appLogoOverride' src='$awpath\assets\A.png'/>
    </binding>
  </visual>
  <actions>
    <action activationType='protocol' content='✔ Install' arguments='anywhere:install/'/>
    <action activationType='protocol' content='❌ Ignore' arguments='anyhwere:decline/'/>
  </actions>
</toast>
"@
$XmlDocument = [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime]::New()
$XmlDocument.loadXml($xml)

$AppId = "$awpath\dist\protocol.exe"

[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
$Toast = [Windows.UI.Notifications.ToastNotification]::new($XmlDocument)
$Toast.ExpirationTime = [DateTimeOffset]::Now.AddMinutes(1)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($AppId).Show($Toast)

#[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]::CreateToastNotifier($AppId).Show($XmlDocument)
