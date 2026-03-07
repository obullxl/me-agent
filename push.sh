#!/bin/bash

# 全局配置，永久保存凭据到系统凭据管理器
git config --global credential.helper store

# Git 自动推送脚本 (Ubuntu Shell 版本)
# 功能：添加所有文件 → 提交 → 循环尝试 push 直到成功

echo "=================================================="
echo "Starting Git push script..."
echo "=================================================="

# 增加文件
git add --all

# 提交 (如果提交失败会继续尝试 push)
git commit -m "Publish......"

# 循环尝试 push，直到成功
while true; do
    echo "Attempting to push changes..."
    git push
    if [ $? -ne 0 ]; then
        echo "Git push failed, trying again in 1 second."
        echo "------------------------------------------------------------------------------------------"
        sleep 1
    else
        echo "Git push succeeded."
        break
    fi
done

echo "Script completed."
echo "=================================================="
echo "Git push successful."
echo "=================================================="
