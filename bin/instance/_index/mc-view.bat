cd %~dp0
call setting.bat

rundll32.exe url.dll,FileProtocolHandler "%~1%index.html"

cd %mclogpath%