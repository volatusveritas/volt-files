$volt_start_path = Split-Path $MyInvocation.MyCommand.Path
$volt_startup_file = (
    "$env:AppData\Microsoft\Windows\Start Menu\Programs\Startup" +
    "\volt-files-startup.bat"
)

# Create an initialization .bat file that runs the volt-files module
New-Item $volt_startup_file -ItemType File -Force | Out-Null
Add-Content $volt_startup_file "@echo off"
Add-Content $volt_startup_file ("cd " + $volt_start_path)
Add-Content $volt_startup_file "call .venv\Scripts\activate"
Add-Content $volt_startup_file "python -m voltfiles"
Add-Content $volt_startup_file "pause"

Write-Host "Volt Files was added to the startup apps." -ForegroundColor Green
