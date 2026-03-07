@echo off
setlocal

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
