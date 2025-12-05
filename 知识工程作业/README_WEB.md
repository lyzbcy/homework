# 医药问答系统 Web 版使用说明

本项目已升级为现代化的 Web 界面。

## 快速启动

双击运行根目录下的 `start_web.bat` 即可启动整个系统（后端 API + 前端界面）。

## 手动启动

如果您需要手动分别启动服务：

### 1. 启动后端 API (Python)

确保您已安装 Python 依赖：
```bash
pip install fastapi uvicorn
```

在 `QAMedicalKG` 目录下运行：
```bash
python server.py
```
后端服务将在 `http://localhost:8000` 启动。

### 2. 启动前端界面 (React)

确保您已安装 Node.js 依赖。在 `QAMedicalKG/web_ui` 目录下运行：
```bash
npm install
```

然后启动开发服务器：
```bash
npm run dev
```
前端界面将在 `http://localhost:5173` 启动。

## 功能说明

- **智能问答**：在聊天框输入问题，如"感冒吃什么药"，系统将基于知识图谱回答。
- **知识图谱可视化**：右侧面板实时展示相关的知识图谱节点和关系。
- **推荐问题**：左侧侧边栏提供常见问题示例，点击即可发送。

## 注意事项

- 请确保 Neo4j 数据库已启动，否则系统无法获取数据。
- 如果遇到端口冲突，请修改 `server.py` 或 `vite.config.js` 中的端口设置。
