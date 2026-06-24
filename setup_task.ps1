$taskName = "CQUT-Monitor"
$scriptPath = "C:\Users\28497\Desktop\新建文件夹 (2)\cqut-monitor\run_silent.bat"

$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force

Write-Host "Task '$taskName' created successfully!"
Write-Host "It will run every 1 hour."
Write-Host "You can check it in Task Scheduler (taskschd.msc)"
