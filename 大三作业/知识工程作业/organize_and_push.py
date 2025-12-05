#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
脚本用于将当前目录的文件重新组织到 Knowledge-Engineering/QAMedicalKG/ 路径下
并推送到 GitHub 仓库
"""
import os
import subprocess
import shutil

def run_git_command(cmd, check=True):
    """执行 git 命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode != 0:
            if check:
                print(f"警告: {result.stderr}")
            return False
        else:
            if result.stdout.strip():
                print(f"  {result.stdout.strip()}")
            return True
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False

def main():
    # 获取当前目录
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 检查是否在 git 仓库中
    if not os.path.exists('.git'):
        print("错误: 当前目录不是 git 仓库")
        return
    
    # 获取所有文件（排除 .git 目录）
    files_to_move = []
    for root, dirs, files in os.walk('.'):
        # 跳过 .git 目录
        if '.git' in root:
            continue
        # 跳过 Knowledge-Engineering 目录（如果已存在）
        if 'Knowledge-Engineering' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            # 跳过脚本本身
            if file_path == './organize_and_push.py':
                continue
            files_to_move.append(file_path)
    
    print(f"找到 {len(files_to_move)} 个文件需要移动")
    
    # 创建目标目录结构
    target_dir = 'Knowledge-Engineering/QAMedicalKG'
    os.makedirs(target_dir, exist_ok=True)
    
    # 使用 git mv 移动文件
    print("\n开始移动文件...")
    moved_count = 0
    for file_path in files_to_move:
        # 规范化路径
        normalized_path = file_path.replace('\\', '/').lstrip('./')
        # 跳过已经在目标目录中的文件
        if normalized_path.startswith('Knowledge-Engineering/'):
            continue
        # 跳过脚本本身和临时文件
        if 'organize_and_push' in normalized_path or '上传说明' in normalized_path:
            continue
            
        target_path = f"{target_dir}/{normalized_path}"
        
        # 创建目标目录（如果需要）
        target_file_dir = os.path.dirname(target_path)
        if target_file_dir and target_file_dir != target_dir:
            os.makedirs(target_file_dir, exist_ok=True)
        
        # 使用 git mv 移动文件
        if os.path.exists(normalized_path):
            # 转义路径中的特殊字符
            src = normalized_path.replace('"', '\\"')
            dst = target_path.replace('"', '\\"')
            cmd = f'git mv "{src}" "{dst}"'
            print(f"移动: {normalized_path}")
            if run_git_command(cmd, check=False):
                moved_count += 1
            else:
                # 如果 git mv 失败，使用普通移动然后 git add
                try:
                    if os.path.exists(normalized_path):
                        shutil.move(normalized_path, target_path)
                        run_git_command(f'git add "{target_path}"', check=False)
                        moved_count += 1
                except Exception as e:
                    print(f"  跳过: {e}")
    
    print(f"\n成功移动 {moved_count} 个文件")
    
    # 提交更改
    print("\n提交更改...")
    run_git_command('git add -A')
    run_git_command('git commit -m "Reorganize files to Knowledge-Engineering/QAMedicalKG/"')
    
    # 推送到远程仓库
    print("\n推送到远程仓库...")
    run_git_command('git branch -M main')
    run_git_command('git push -u origin main')
    
    print("\n完成！")

if __name__ == '__main__':
    main()

