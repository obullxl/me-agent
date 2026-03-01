@echo off
setlocal

:: 源文件路径
set "SRC=C:\Users\obull\output\mihomo.yaml"

:: 目标目录
set "DEST_FILE=D:\CodeSpace\me-agent\tech\mihomo.yaml"

:: 检查源文件是否存在
if not exist "%SRC%" (
    echo Source File not exists！
    echo  %SRC%
    pause
    exit /b 1
)

:: 复制并覆盖（使用 /Y 参数静默覆盖）
echo Copying "%SRC%" to "%DEST_FILE%" ...
copy /Y "%SRC%" "%DEST_FILE%" >nul

if %ERRORLEVEL% equ 0 (
    echo Copy successfull.
) else (
    echo Copy failure!!!
    pause
    exit /b 1
)

:: 可选：暂停查看结果（调试时保留，正式使用可删除下一行）
:: pause

:: 增加文件
git add --all
git commit -m Publish......


:loop
echo Attempting to push changes...
git push

REM Check the error level after git push
if %ERRORLEVEL% neq 0 (
    echo Git push failed, trying again in 1 second.
    echo ------------------------------------------------------------------------------------------
    timeout /t 1 >nul
    goto loop
) else (
    echo Git push succeeded.
    goto end
)

:end
echo Script completed.
echo ==================================================
echo Git push successful.
echo ==================================================
