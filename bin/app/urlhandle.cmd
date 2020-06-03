@echo off

:: current directory
cd %~dp0
set p=%~1%
if "%~1" == "" goto error
if not "%p:mclog://new/=%" == "%p%" (goto new)
if not "%p:mclog://edit/=%" == "%p%" (goto edit)
if not "%p:mclog://edit-metadata/=%" == "%p%" (goto editmetadata)
if not "%p:mclog://dir/=%" == "%p%" (goto dir)
if not "%p:mclog://create-assets-list/=%" == "%p%" (goto createassetslist)
if not "%p:mclog://console/=%" == "%p%" (goto openconsole)

:error
echo "error. input is:">>mc.log
echo %p%>>mc.log
exit

:new
set p=%p:mclog://new/=%
if exist %p% (goto error) else (mc-console.bat %p%)
exit

:edit
set p=%p:mclog://edit/=%
if exist %p%/index.md (atom -a %p%\index.md) else (goto error)
exit

:editmetadata
set p=%p:mclog://edit-metadata/=%
if exist %p%/META-INF/metadata.json (atom -a %p%/META-INF/metadata.json) else (goto error)
exit

:dir
set p=%p:mclog://dir/=%
if exist %p% (start "" %p%) else (goto error)
exit

:createassetslist
set p=%p:mclog://create-assets-list/=%
python %p%/../_index/mclib.py get_assetstemplate %p% | clip
exit

:openconsole
set p=%p:mclog://console/?=%
mc-console.bat %p%
exit