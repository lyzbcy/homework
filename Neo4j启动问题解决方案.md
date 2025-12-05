# Neo4j启动问题快速解决方案

## 🔴 问题描述

### 情况一：创建数据库时出错
在Neo4j Desktop中创建数据库时，出现错误：
```
Error Cannot connect to stopped DBMS. 
Suggested Action(s): - Start the DBMS
```

### 情况二：点击Connect → Query后出错 ⚠️ 常见
点击实例卡片上的 **"Connect"** 按钮，选择 **"Query"** 后，出现错误对话框：
- **错误标题**：Connection to Instance Failed
- **错误详情**：ServiceUnavailable - "Could not perform discovery. No routing servers available"
- **连接URL**：neo4j://127.0.0.1:7687

虽然实例显示为 **"RUNNING"**，但DBMS实际上没有运行。

---

## ✅ 解决方法（按顺序尝试）

### 方法一：通过Connect按钮启动（最简单）⭐ 推荐

**重要提示**：如果你点击 Connect → Query 后出现连接失败错误，说明DBMS没有运行。请按以下步骤操作：

1. 在Neo4j Desktop中，找到你的实例（例如：`Knowledge Engineering`）
2. 在实例卡片上，找到 **"Connect"** 按钮（带下拉箭头）
3. **不要点击 Query**，而是：
   - 点击 **"Connect"** 按钮，选择 **"Explore"** 或 **"Open Browser"**
   - 或者直接点击 **"Connect"** 按钮（不带下拉箭头，如果存在）
4. 这会自动启动DBMS并打开浏览器（http://localhost:7474）
5. 等待浏览器成功打开并显示Neo4j界面
6. 现在可以：
   - 返回Neo4j Desktop，再次点击 Connect → Query（这次应该能成功）
   - 或者直接创建数据库
   - 或者直接在浏览器中使用Neo4j

**为什么Query不行但Explore/Browser可以？**
- Query 需要DBMS已经运行才能连接
- Explore/Browser 会自动启动DBMS（如果还没运行）

---

### 方法二：停止并重新启动

1. 在实例卡片上，点击 **"Stop"** 按钮（即使显示RUNNING也点击）
2. 等待状态变为 **"STOPPED"**
3. 然后点击 **"Start"** 重新启动
4. 等待状态变为 **"RUNNING"**（绿色圆点）
5. 再次尝试创建数据库

---

### 方法三：验证DBMS是否真的运行

1. 打开浏览器，访问：http://localhost:7474
2. **如果看到Neo4j登录界面**：
   - 说明DBMS正在运行
   - 可以尝试直接在浏览器中登录（用户名：`neo4j`，密码：`tangyudiadid0`）
   - 然后返回Neo4j Desktop创建数据库
3. **如果显示"无法访问此网站"**：
   - 说明DBMS没有启动
   - 返回使用方法一或方法二

---

## 🔍 为什么会出现这个问题？

在Neo4j Desktop中，有两个不同的概念：

- **实例（Instance）**：容器，可以包含多个数据库
- **DBMS（Database Management System）**：数据库管理系统，需要单独启动

**问题原因：**
- 实例可能显示为"RUNNING"，但DBMS实际上没有启动
- 创建数据库需要DBMS运行，而不仅仅是实例运行
- 这是一个常见的混淆点

---

## 📋 完整操作流程（首次使用）

1. **创建实例**
   - 点击 "Create instance"
   - 输入名称（例如：`Knowledge Engineering`）

2. **启动DBMS**
   - 点击实例卡片上的 "Start" 按钮
   - 设置密码：`tangyudiadid0`

3. **验证DBMS运行**
   - 点击 "Connect" → "Open Browser"
   - 或访问 http://localhost:7474

4. **创建数据库**
   - 展开 "Databases" 部分
   - 点击 "Create database"
   - 输入数据库名称（例如：`neo4j`）

5. **开始使用**
   - 现在可以运行 `python build_medicalgraph.py` 构建知识图谱了

---

## ❓ 如果以上方法都不行

1. **检查Neo4j Desktop版本**
   - 确保使用最新版本
   - 访问 https://neo4j.com/download/ 下载最新版

2. **检查系统要求**
   - 确保有足够的磁盘空间
   - 确保没有端口冲突（7474端口）

3. **尝试删除并重新创建实例**
   - 在Neo4j Desktop中删除现有实例
   - 重新创建新实例

4. **查看日志**
   - 在Neo4j Desktop中，点击实例的 "..." 菜单
   - 选择 "View logs" 查看错误信息

---

## 📞 需要更多帮助？

查看详细使用指南：
- 📄 [详细使用指南.md](详细使用指南.md) - 第3.2节

