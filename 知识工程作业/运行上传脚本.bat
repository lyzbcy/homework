@echo off
chcp 65001 >nul
echo ========================================
echo 开始组织文件并上传到 GitHub
echo ========================================
echo.

python organize_and_push.py

echo.
echo ========================================
echo 如果脚本执行成功，文件已经上传到 GitHub
echo 如果遇到问题，请查看 "GitHub上传操作指南.md"
echo ========================================
pause

