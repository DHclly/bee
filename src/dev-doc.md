# 开发文档

## 使用 uv 初始化 Python 3.13 虚拟环境

```bash
# 1. 安装 uv（已安装可跳过）
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. 在项目根目录初始化项目（生成 pyproject.toml，并指定 Python 3.13）
uv init --python 3.13

# 3. 创建虚拟环境（自动使用 Python 3.13）
uv venv --python 3.13

# 4. 激活虚拟环境
# Windows (cmd)
.venv\Scripts\activate.bat
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Git Bash
source .venv/Scripts/activate

# 5. 安装依赖
uv add <包名>

# 6. 用 uv 命令运行脚本（无需手动激活虚拟环境）
uv run main.py
```

### 说明

- `uv venv --python 3.13` 会使用已由 uv 管理的 Python 3.13；若本机没有，uv 会自动下载。
- `uv sync` 可依据 `pyproject.toml` / `uv.lock` 重装全部依赖，适合新环境初始化。
- 查看可用 Python 版本：`uv python list`
