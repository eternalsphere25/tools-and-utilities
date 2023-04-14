# https://learn.microsoft.com/en-us/windows-server/administration/
# windows-commands/robocopy

#Define variables (input)
$Source = Read-Host -Prompt "Enter source directory"
$Destination = Read-Host -Prompt "Enter destination directory"
$Date = Read-Host -Prompt "Enter date to transfer (Format: YYYY-MM-DD)"
$Date_Now = Get-Date -UFormat "%Y%m%d_%H%M%S"
$Logfile = "D:\写真\Robocopy Transfer Logs\$Date_Now.txt"

#Convert input date to datetime object
$convertDate = [DateTime]$Date

#Generate date range to select a single day
$Date_1 = '{0:yyyyMMdd}' -f $convertDate
$Date_2 = '{0:yyyyMMdd}' -f $convertDate.AddDays(1)

#Run robocopy
robocopy $Source $Destination /s /xo /v /maxage:$Date_1 /minage:$Date_2 `
/unilog+:$Logfile /tee /eta

#Display exit code in terminal
Write-Output $LASTEXITCODE