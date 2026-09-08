# TraceJudge

TraceJudge 是一个面向自动化测试失败日志的本地优先归因工具。它关联来自测试工具、设备、产品服务和环境的日志，以可追溯证据判断失败更可能属于产品/设备、测试工具、环境，或证据不足。

## 快速开始

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

另开终端启动界面：

```bash
cd frontend
npm install
npm run dev
```

打开 `http://localhost:3000`。后端 API 文档位于 `http://localhost:8000/docs`。

默认使用规则分析和本地关键词检索，因而无需 API 密钥即可完成演示。设置 `OPENAI_API_KEY` 后，系统会在规则结果之上调用 OpenAI 生成带引用的增强结论；未配置密钥时界面会明确说明该状态，绝不会伪造 AI 结果。

## 项目结构

- `docs/requirements.md`：唯一需求基线与变更记录
- `backend/`：FastAPI、日志关联、规则、RAG、SQLite 持久化
- `frontend/`：Next.js 界面
- `knowledge-base/`：随仓库版本管理的产品、工具与已验证案例知识
- `sample-data/`：四类归因的可重复样例

## 开发约定

需求一旦确认，先更新 `docs/requirements.md` 中的相关章节及变更记录，再修改实现。
