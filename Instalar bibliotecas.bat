@echo off
setlocal

set "alvo=%~dp0\Puxar partida no LOL.py" 
set "atalho=%~dp0\Puxar partida no LOL.lnk"

cd /d "%~dp0"

set "dir=%~dp0"
if "%dir:~-1%"=="\" set "dir=%dir:~0,-1%"

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%atalho%'); $s.TargetPath = '%alvo%'; $s.WorkingDirectory = '%dir%'; $s.Save()"

@echo off
setlocal

set "alvo=%~dp0\Fechar instancias.py" 
set "atalho=%~dp0\Puxar uma partida de LOL.lnk"
set "icone=%~dp0\Images\icon.ico"

cd /d "%~dp0"

set "dir=%~dp0"
if "%dir:~-1%"=="\" set "dir=%dir:~0,-1%"

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%atalho%'); $s.TargetPath = '%alvo%'; $s.IconLocation = '%icone%'; $s.WorkingDirectory = '%dir%'; $s.Save()"