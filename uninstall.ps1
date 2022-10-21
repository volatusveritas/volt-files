$volt_startup_file = (
    "$env:AppData\Microsoft\Windows\Start Menu\Programs\Startup" +
    "\volt-files-startup.bat"
)

If (Test-Path $volt_startup_file)
{
    Remove-Item $volt_startup_file -Force
    Write-Host "Volt Files was removed from the startup apps." -ForegroundColor Green
}
Else
{
    Write-Host "Volt Files is not in the startup apps." -ForegroundColor Red
}
