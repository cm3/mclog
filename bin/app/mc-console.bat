@echo off
setlocal enabledelayedexpansion

:: first argument is path

IF NOT EXIST "%~1%" (
echo not implemented.
echo "%~1%"
set command=new "%~1%"
echo !command!
set /p yn="Issue the command above?: "
if /i !yn!==y (goto new)
if /i !yn!==yes (goto new)
pause
exit
) else (
cd "%~1%"
echo Current Directory:
echo %~1%
)

:input
set /p command=Ë

if not "%command:new=%" == "%command%" (goto new)
if not "%command:build=%" == "%command%" (goto build)
if not "%command:exit=%" == "%command%" (goto exit)
if not "%command:search=%" == "%command%" (goto search)
if not "%command:help=%" == "%command%" (goto help)
if "%command%" == "" (goto input)
call %command%
set command=
goto input

:help
echo `new [something]` to make a new mc file.
echo `build` to build json data and open the html.
echo `search [something]` to search something in mc files.
echo `exit` to exit.
echo `help` to show this list of commands.
goto input

:new
IF "%command%" == "new " goto help
IF "%command%" == "new" goto help

echo create new Markdown Container here.
set title=%command:new =%
echo %title%
pause

IF EXIST "%title%" (
echo ERROR: directory "%title%" is already exist.
goto input
) else (
mkdir %title%
echo # %title%>%title%\index.md
echo application/x-ml-container>%title%\mimetype
mkdir %title%\META-INF
echo {"rootfile":{"path":"index.md","media-type":"text/markdown"},"tags":[],"title":"%title%"}>%title%\META-INF\metadata.json
call atom %title%\index.md
)
goto input

:build
:: build as cms by default. 
call "./_index/mc-build.bat"
goto input

:search
set p=%command:search =%
call "./_index/mc-search.bat" %p%
goto input

:exit
exit