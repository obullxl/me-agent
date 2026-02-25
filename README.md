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
conda create -n AgentME python=3.12.12 -y

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