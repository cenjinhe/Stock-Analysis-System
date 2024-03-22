@echo off
setlocal

:check_status
cls
sc query MySQL80 | find "RUNNING" > nul 2>&1
if %errorlevel%==0 (
    echo Current status of MySQL service: Running
    set status="Running"
) else (
    echo Current status of MySQL service: Stopped
    set status="Stopped"
)

if %status%=="Running" (
    echo "启动 Stock-System 系统"
    start cmd /k "echo Startup server && D:\project\Stock-System\script\windows_server.bat"
    start cmd /k "echo Startup web && D:\project\Stock-System\script\windows_web.bat"
)

if %status%=="Stopped" (
    :echo "启动 MySQL80"
    :net start MySQL80
    echo "MySQL服务还没有运行起来，请稍后......"
    timeout /T 5 /NOBREAK
    goto check_status
)
