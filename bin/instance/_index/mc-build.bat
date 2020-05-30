cd %~dp0
call setting.bat

echo ----- %date% %time% ----- >>mc.log
python gen_metainf.py %mclogpath% >>mc.log
python build.py %mclogpath% >>mc.log
mc-view %mclogpath%

cd %mclogpath%
