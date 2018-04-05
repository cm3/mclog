cd %~dp0
call setting.bat

cd %mclogpath%
start "" "C:\\Users\\User\\bin\\TresGrep\\TresGrep.exe" /D:./ /C:%~1% /I /start