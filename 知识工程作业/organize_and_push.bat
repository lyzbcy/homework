@echo off
chcp 65001 >nul
echo 开始组织文件到 Knowledge-Engineering/QAMedicalKG/ 路径...

REM 创建目标目录
if not exist "Knowledge-Engineering\QAMedicalKG" mkdir "Knowledge-Engineering\QAMedicalKG"

REM 获取所有文件并移动到新目录
echo 移动文件...
for /r %%f in (*) do (
    if not "%%f"=="%~f0" (
        if not "%%f"=="organize_and_push.py" (
            set "filepath=%%f"
            set "relpath=%%f"
            setlocal enabledelayedexpansion
            set "relpath=!relpath:%CD%\=!"
            set "relpath=!relpath:\=/!"
            if not "!relpath:~0,25!"=="Knowledge-Engineering/QAMedicalKG/" (
                echo 移动: !relpath!
                git mv "!relpath!" "Knowledge-Engineering/QAMedicalKG/!relpath!" 2>nul
                if errorlevel 1 (
                    echo 使用普通移动...
                    move "!relpath!" "Knowledge-Engineering/QAMedicalKG/!relpath!" >nul 2>&1
                )
            )
            endlocal
        )
    )
)

REM 移动目录
for /d /r %%d in (*) do (
    set "dirpath=%%d"
    setlocal enabledelayedexpansion
    set "dirpath=!dirpath:%CD%\=!"
    set "dirpath=!dirpath:\=/!"
    if not "!dirpath:~0,25!"=="Knowledge-Engineering/QAMedicalKG/" (
        if not "!dirpath!"=="Knowledge-Engineering" (
            if not "!dirpath!"==".git" (
                echo 处理目录: !dirpath!
            )
        )
    )
    endlocal
)

echo 添加所有更改...
git add -A

echo 提交更改...
git commit -m "Reorganize files to Knowledge-Engineering/QAMedicalKG/"

echo 重命名分支为 main...
git branch -M main

echo 推送到远程仓库...
git push -u origin main

echo 完成！
pause

