# https://devblogs.microsoft.com/scripting/
# easily-compare-two-folders-by-using-powershell/
# https://learn.microsoft.com/en-us/powershell/module/
# microsoft.powershell.management/get-childitem?view=powershell-7.3
# https://learn.microsoft.com/en-us/powershell/module/
# microsoft.powershell.utility/compare-object?view=powershell-7.3

#Define variables (input)
$Directory_1 = Read-Host -Prompt "Enter directory to use as reference"
$Directory_2 = Read-Host -Prompt "Enter directory to use for comparison"