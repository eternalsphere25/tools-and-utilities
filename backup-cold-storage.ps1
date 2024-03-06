# https://learn.microsoft.com/en-us/windows-server/administration/
# windows-commands/robocopy
#
# /s Copies subdirectories. Automatically excludes empty directories.
# /xo Source directory files older than the destination are excluded.
# /v Produces verbose output, and shows all skipped files.
# /tee Writes the status output to the console window, and to the log file.
# /eta Shows the estimated time of arrival (ETA) of the copied files.

#Define variables (input)
$Source = Read-Host -Prompt "Enter source directory"
$Destination = Read-Host -Prompt "Enter destination directory"
$Date_Now = Get-Date -UFormat "%Y%m%d_%H%M%S"
$Logfile = "Y:\Robocopy File Logs\$Date_Now.txt"

#Run robocopy
robocopy $Source $Destination /mir /s /v  `
/unilog+:$Logfile /mt:128 /tee /eta

#Display exit code in terminal
Write-Output $LASTEXITCODE