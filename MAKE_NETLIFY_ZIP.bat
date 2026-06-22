@echo off
cd /d "%~dp0"
echo Creating NETLIFY_UPLOAD.zip with forward-slash paths (Netlify/Linux safe)...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$src=(Get-Location).Path; $zip=Join-Path (Split-Path $src) 'NETLIFY_UPLOAD.zip'; if(Test-Path $zip){Remove-Item $zip -Force}; Add-Type -AssemblyName System.IO.Compression; Add-Type -AssemblyName System.IO.Compression.FileSystem; $fs=[System.IO.File]::Open($zip,'CreateNew'); $z=New-Object System.IO.Compression.ZipArchive($fs,'Create'); Get-ChildItem $src -Recurse -File | ForEach-Object { $rel=$_.FullName.Substring($src.Length+1).Replace('\','/'); if($rel -ne 'MAKE_NETLIFY_ZIP.bat'){ $e=$z.CreateEntry($rel,'Optimal'); $o=$e.Open(); $b=[System.IO.File]::ReadAllBytes($_.FullName); $o.Write($b,0,$b.Length); $o.Close() } }; $z.Dispose(); $fs.Close(); Write-Host 'Done.' "
echo.
echo Upload this file to Netlify (Deploys -^> Deploy manually):
echo   %~dp0..\NETLIFY_UPLOAD.zip
echo.
pause
