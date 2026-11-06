# 开发文档

## 使用 uv 为现有项目创建 Python 3.13 虚拟环境

```bash
# 1. 在项目根目录创建虚拟环境（指定 Python 3.13）
uv venv --python 3.13

# 2. 激活虚拟环境
# Windows (cmd)
.venv\Scripts\activate.bat
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Git Bash
source .venv/Scripts/activate

# 3. 安装项目已有依赖
uv sync

# 4. 新增依赖
uv add <包名>

# 5. 用 uv 命令运行脚本（无需手动激活虚拟环境）
uv run main.py
```

### 说明

- `uv venv --python 3.13` 会使用 uv 已管理的 Python 3.13；若本机没有，uv 会自动下载。
- `uv sync` 依据现有的 `pyproject.toml` / `uv.lock` 安装锁定版本的依赖。
- 若项目仅有 `requirements.txt`：先 `uv venv --python 3.13`，再 `uv pip install -r requirements.txt`。
- 查看可用 Python 版本：`uv python list`
