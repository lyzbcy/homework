# GitHub 上传操作指南

## 目标
将 QAMedicalKG 项目上传到 `https://github.com/lyzbcy/homework` 仓库的 `Knowledge-Engineering/QAMedicalKG/` 路径下。

## 当前状态
- ✅ Git 仓库已初始化
- ✅ 远程仓库已添加 (origin: https://github.com/lyzbcy/homework)
- ✅ 文件已提交到本地仓库
- ✅ 目录结构已创建 (Knowledge-Engineering/QAMedicalKG/)

## 操作步骤

### 方法一：使用 Git Bash 或命令行（推荐）

1. **打开 Git Bash 或命令行，切换到项目目录**
   ```bash
   cd "E:\学委\作业\大三上\知识工程\第五章：基于知识图谱的医药问答系统实战\QAMedicalKG"
   ```

2. **移动所有文件到目标目录**
   
   由于文件较多，可以使用以下脚本批量移动：
   
   **Windows (Git Bash):**
   ```bash
   # 移动所有文件（排除 .git 和 Knowledge-Engineering 目录）
   find . -maxdepth 1 -type f ! -name '.git*' ! -path './Knowledge-Engineering/*' -exec git mv {} Knowledge-Engineering/QAMedicalKG/ \;
   
   # 移动所有目录（排除 .git 和 Knowledge-Engineering）
   find . -maxdepth 1 -type d ! -name '.' ! -name '.git' ! -name 'Knowledge-Engineering' -exec git mv {} Knowledge-Engineering/QAMedicalKG/ \;
   ```
   
   **或者手动移动主要文件：**
   ```bash
   git mv *.py Knowledge-Engineering/QAMedicalKG/
   git mv *.txt Knowledge-Engineering/QAMedicalKG/
   git mv *.md Knowledge-Engineering/QAMedicalKG/
   git mv *.bat Knowledge-Engineering/QAMedicalKG/
   git mv *.sh Knowledge-Engineering/QAMedicalKG/
   git mv data Knowledge-Engineering/QAMedicalKG/
   git mv dict Knowledge-Engineering/QAMedicalKG/
   git mv prepare_data Knowledge-Engineering/QAMedicalKG/
   git mv web_ui Knowledge-Engineering/QAMedicalKG/
   git mv __pycache__ Knowledge-Engineering/QAMedicalKG/ 2>/dev/null || true
   ```

3. **提交更改**
   ```bash
   git add -A
   git commit -m "Reorganize files to Knowledge-Engineering/QAMedicalKG/"
   ```

4. **重命名分支并推送**
   ```bash
   git branch -M main
   git push -u origin main
   ```

### 方法二：使用 Python 脚本

运行已创建的 `organize_and_push.py` 脚本：

```bash
python organize_and_push.py
```

### 方法三：使用 GitHub Desktop

1. 打开 GitHub Desktop
2. 在本地文件管理器中，手动创建 `Knowledge-Engineering/QAMedicalKG/` 目录
3. 将所有文件（除了 .git 目录）移动到该目录
4. 在 GitHub Desktop 中提交更改
5. 推送到远程仓库

### 方法四：直接推送后重新组织

如果上述方法都有问题，可以：

1. **先推送当前内容**
   ```bash
   git branch -M main
   git push -u origin main --force
   ```

2. **在 GitHub Web 界面上重新组织文件**
   - 访问 https://github.com/lyzbcy/homework
   - 使用 GitHub 的文件移动功能将文件移动到 `Knowledge-Engineering/QAMedicalKG/` 目录

## 注意事项

1. **分支名称**: 确保使用 `main` 分支（远程仓库使用 main）
2. **文件路径**: 确保所有文件都在 `Knowledge-Engineering/QAMedicalKG/` 路径下
3. **.gitignore**: 已创建，会忽略不必要的文件（如 __pycache__, node_modules 等）
4. **权限**: 确保您有推送到 `lyzbcy/homework` 仓库的权限

## 验证

推送成功后，访问以下 URL 验证：
- https://github.com/lyzbcy/homework/tree/main/Knowledge-Engineering/QAMedicalKG

## 如果遇到问题

1. **权限错误**: 检查是否有推送到仓库的权限
2. **分支冲突**: 使用 `git pull origin main --rebase` 先拉取远程更改
3. **路径问题**: 确保使用正确的路径分隔符（Windows 使用反斜杠，但在 Git 命令中使用正斜杠）

