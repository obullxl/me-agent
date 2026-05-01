# me-agent

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

一个基于 Python 的 AI 代理项目，支持多种工具集成和自动化任务执行。

## 项目简介

me-agent 是一个多功能 AI 代理框架，集成了 LangChain、DeepSeek 等工具，支持语音识别、文本处理、文件操作等多种功能。项目采用模块化设计，便于扩展和定制。

## 目录结构

```
me-agent/
├── config.py                 # 配置文件
├── deepagents_01.py          # 深度代理主程序
├── langchain_01.py           # LangChain 集成示例
├── langchain_chat.py         # LangChain 聊天功能
├── langchain_tools.py        # LangChain 工具集成
├── requirements.txt          # Python 依赖
├── push.sh                   # Git 自动推送脚本
├── push.bat                  # Windows 推送脚本
├── LICENSE                   # 许可证文件
├── README.md                 # 项目文档
├── data/                     # 数据目录
├── mcp/                      # MCP (Model Context Protocol) 相关
│   ├── client/               # MCP 客户端
│   └── server/               # MCP 服务端
├── tech/                     # 技术工具
│   ├── feishu_client.py      # 飞书客户端
│   ├── mihomo.yaml           # Mihomo 配置
│   ├── PhotoResize.py        # 图片处理工具
│   └── tts_pyttsx3.py        # 语音合成工具
├── tools/                    # 实用工具
│   ├── pdf_2_png.py          # PDF 转 PNG 工具
│   ├── README.md             # 工具说明
│   ├── requirements.txt      # 工具依赖
│   └── files/                # 工具文件目录
└── vector/                   # 向量数据库相关
    ├── __init__.py
    ├── langchain_RAG.py      # RAG 检索增强生成
    └── langchain_vector.py   # 向量操作
```

## 快速开始

### 环境要求

- Python 3.12+
- Git
- Miniconda/Anaconda (推荐)

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/your-username/me-agent.git
cd me-agent
```

#### 2. 配置 Python 环境

##### 安装 Miniconda

访问 [Miniconda 官网](https://www.anaconda.com/docs/getting-started/miniconda/install) 下载并安装。

##### 配置/更新 Miniconda

```bash
# 清理镜像源（官方源）
conda config --remove-key channels

# 更新 Miniconda
conda update conda

# 可选：配置国内镜像源加速下载
# 清华镜像源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes

# 或阿里云镜像源
conda config --add channels https://mirrors.aliyun.com/anaconda/pkgs/main/
conda config --add channels https://mirrors.aliyun.com/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```

##### 创建研发环境

```bash
# 创建环境
conda create -n AgentME python=3.12 -y

# 激活环境
conda activate AgentME
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### Conda 环境管理

```bash
# 查看所有环境
conda env list

# 激活环境
conda activate AgentME

# 退出环境
conda deactivate

# 删除环境
conda remove --name AgentME --all
```

### 复制研发环境

```bash
# 导出环境配置
conda env export > environment.yml

# 导入环境配置
conda env create -f environment.yml
```

## VS Code + Jupyter 配置

### Windows 11 配置

1. 安装 VS Code
2. 安装 Microsoft Jupyter 扩展

### WSL Ubuntu 配置

在 WSL Ubuntu 中安装 Jupyter 内核：

```bash
# 升级相关包
pip install --upgrade pip jupyter ipykernel

# 注册内核
python -m ipykernel install --user --name=wsl-python
```

重启 VS Code 和 WSL：

```powershell
wsl --shutdown
```

## Git 推送脚本

项目包含 `push.sh` 脚本，用于自动执行 Git 推送操作，支持主仓库和子仓库同步。

### 基本用法

```bash
# 使用默认提交信息
./push.sh

# 自定义提交信息
./push.sh "更新功能：添加新特性"
```

### 功能特性

- ✅ **自动添加文件**：将所有更改添加到暂存区
- ✅ **智能提交**：仅在有更改时进行提交
- ✅ **推送重试**：失败时自动重试，每秒尝试一次
- ✅ **子仓库支持**：检测并推送 `ClawSpace` 子目录中的仓库
- ✅ **彩色日志**：提供清晰的中文状态信息
- ✅ **凭据管理**：自动启用 Git 凭据存储

### 输出示例

```
==================================================
[INFO] 开始执行 Git 自动推送脚本
[INFO] 当前远程仓库：
origin  https://github.com/user/me-agent.git (fetch)
origin  https://github.com/user/me-agent.git (push)
==================================================
[INFO] 添加所有更改文件到暂存区。
[INFO] 正在提交更改，提交信息：更新功能
[SUCCESS] 提交成功。
[INFO] 第 1 次尝试推送到远程仓库...
[SUCCESS] 第 1 次推送成功。
==================================================
[SUCCESS] 主仓库推送完成。
==================================================
```

### 注意事项

- 确保脚本有执行权限：`chmod +x push.sh`
- 首次运行可能需要输入 Git 凭据，后续会自动存储
- 子仓库需要有自己的 `push.sh` 脚本才能被推送

## 开发指南

### 运行测试

```bash
python deepagents_01.py
```

### 添加新功能

1. 在相应模块中实现功能
2. 更新 `requirements.txt` 添加依赖
3. 更新本文档说明

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request
