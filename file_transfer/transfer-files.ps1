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
$File_Type = Read-Host -Prompt "Enter file type ('jpg' or 'nef')"
$Date = Read-Host -Prompt "Enter date to transfer (Format: YYYY-MM-DD)"
$Date_Now = Get-Date -UFormat "%Y%m%d_%H%M%S"
$Logfile = "D:\写真\Robocopy Transfer Logs\$Date_Now.txt"

#Convert input date to datetime object
$convertDate = [DateTime]$Date

#Generate date range to select a single day
$Date_1 = '{0:yyyyMMdd}' -f $convertDate
$Date_2 = '{0:yyyyMMdd}' -f $convertDate.AddDays(1)
$Date_Year = '{0:yyyy}' -f $convertDate

#Set file mode - this determines exactly which folder the files end up in
#File structure: [Year]\<Date>\<Raws>
#.JPG files go under <Date> while .NEF files go under <Raws>
$Destination_JPG = "D:\写真\[" + $Date_Year + "]\" + $Date
$Destination_NEF = "D:\写真\[" + $Date_Year + "]\" + $Date + "\Raws"
If ($File_Type -eq "jpg")
{
    $Destination = $Destination_JPG
}
ElseIf ($File_Type -eq "nef")
{
    $Destination = $Destination_NEF
}
Else
{
    Write-Output "WARNING: Invalid file type '$File_Type'"
    Write-Output "Terminating script..."
    Exit
}

#Generate new directory for files if it doesn't already exist
If (Test-Path -LiteralPath $Destination)
{
    Write-Ouptut "----------"
    Write-Output "Directory already exists!"
}
Else
{
    New-Item -ItemType Directory -Path $Destination | Out-Null
    Write-Output "----------"
    Write-Output "New directory made: $Destination"
}

#Run robocopy
robocopy $Source $Destination /s /xo /v /maxage:$Date_1 /minage:$Date_2 `
/unilog+:$Logfile /mt:128 /tee /eta

#Display exit code in terminal
Write-Output $LASTEXITCODE