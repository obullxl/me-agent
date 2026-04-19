# me-agent

## 配置环境

+ 安装Miniconda: `https://www.anaconda.com/docs/getting-started/miniconda/install`

+ 配置/更新Miniconda:

```
# 清理镜像源（官方源）
conda config --remove-key channels

# 更新Minicodna
conda update conda

# 或者，清华镜像源
#conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
#conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
#conda config --set show_channel_urls yes

# 或者，阿里云镜像源
#conda config --add channels https://mirrors.aliyun.com/anaconda/pkgs/main/
#conda config --add channels https://mirrors.aliyun.com/anaconda/pkgs/free/
#conda config --set show_channel_urls yes
```

+ 配置研发环境：

```
# 配置环境
conda create -n AgentME python=3.14.4 -y

# 激活环境
conda activate AgentME
# conda deactivate
```

## Conda环境管理

```
conda env list：查看所有环境
conda activate env_name：激活环境
conda deactivate：退出环境
conda remove --name env_name --all：删除环境
```

## 复制研发环境

```
# 导出研发环境
conda env export > environment.yml

# 导入研发环境
conda env create -f environment.yml
```

## Win11下VS Code-Jupyter配置

Win11 安装：VS Code，同时安装 Microsoft Jupyter 插件

WSL Ubuntu中安装 Jupyter 内核：

```shell
# 升级
pip install --upgrade pip jupyter ipykernel

# 注册内核
python -m ipykernel install --user --name=wsl-python
```

重启 VS Code 和 WSL Ubuntu 系统：

```powershell
wsl --shutdown
```
