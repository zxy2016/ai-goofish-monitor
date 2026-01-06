# Gemini 上下文指南

## 项目概览

这是一个基于 Playwright 和 AI 的闲鱼智能监控系统，旨在通过自动化手段实时监控商品，并利用多模态大模型进行价值分析。项目采用前后端分离架构，提供完整的 Web 管理界面。

### 核心技术栈

*   **后端**: Python 3.10+, FastAPI, Playwright (爬虫), APScheduler (任务调度), OpenAI (AI 分析)。
*   **前端**: Vue 3, TypeScript, Vite, Tailwind CSS, shadcn-vue。
*   **部署**: Docker, Docker Compose。

### 目录结构摘要

*   `src/`: 后端源代码。
    *   `app.py`: FastAPI 应用入口。
    *   `scraper.py`: Playwright 爬虫核心逻辑。
    *   `services/`: 业务逻辑层 (任务、通知、AI 分析等)。
    *   `api/`: API 路由定义。
    *   `domain/`: 数据模型定义。
*   `web-ui/`: 前端源代码 (Vue 3)。
*   `spider_v2.py`: 传统的命令行任务执行入口。
*   `config.json` / `.env`: 配置文件。
*   `docker-compose.yaml`: 容器编排文件。

## 开发与运行

### 后端 (Python)

1.  **环境**: 确保 Python 3.10+，并运行 `pip install -r requirements.txt`。
2.  **浏览器驱动**: `playwright install chromium`。
3.  **运行**:
    *   开发模式: `uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload`
    *   爬虫脚本: `python spider_v2.py`
4.  **测试**: 使用 `pytest` 运行单元测试。

### 前端 (Vue 3)

1.  **目录**: `cd web-ui`
2.  **依赖**: `npm install`
3.  **运行**: `npm run dev` (开发服务默认在端口 5173)
4.  **构建**: `npm run build`

### Docker 部署

*   **启动**: `docker-compose up --build -d`
*   **日志**: `docker-compose logs -f`

## 开发约定与规范

**重要：作为 AI 助手，请严格遵守以下规则：**

1.  **语言**: 所有回答、代码注释和文档必须使用 **简体中文**。
2.  **测试驱动**: 所有的代码开发任务必须包含相应的 **单元测试**，确保功能正确性。
3.  **Git 提交消息格式**:
    *   必须严格按照以下格式生成：
        ```text
        类型: [feat/fix/docs/style/refactor/test/build/chore]
        描述: [简洁说明修改内容，不超过50字]
        详细说明: [可选，复杂修改需补充]
        关联Issue: [可选，如#123]
        ```
    *   **类型说明**:
        *   `feat`: 新功能
        *   `fix`: 修复 bug
        *   `docs`: 文档修改
        *   `style`: 代码格式修改（不影响代码运行的变动）
        *   `refactor`: 代码重构（即不是新增功能，也不是修改 bug 的代码变动）
        *   `test`: 增加测试
        *   `build`: 影响构建系统或外部依赖的修改
        *   `chore`: 其他修改
    *   如果只是简单修改，省略"详细说明"和"关联Issue"。

## 常用命令参考

*   **运行测试**: `pytest`
*   **前端类型检查**: `npm run build` (在 `web-ui` 目录，包含 `vue-tsc`)
*   **代码格式化**: 遵循现有的代码风格 (Python: PEP 8, JS/TS: Prettier/ESLint)。
