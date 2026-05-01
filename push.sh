#!/bin/bash

# 颜色输出定义
COLOR_RESET="\033[0m"
COLOR_INFO="\033[1;34m"
COLOR_SUCCESS="\033[1;32m"
COLOR_WARN="\033[1;33m"
COLOR_ERROR="\033[1;31m"
COLOR_DIVIDER="\033[1;36m"

# 辅助输出函数，输出带颜色的日志
log_info() {
    printf "%b[%s] %s%b\n" "$COLOR_INFO" "INFO" "$1" "$COLOR_RESET"
}

log_success() {
    printf "%b[%s] %s%b\n" "$COLOR_SUCCESS" "SUCCESS" "$1" "$COLOR_RESET"
}

log_warn() {
    printf "%b[%s] %s%b\n" "$COLOR_WARN" "WARN" "$1" "$COLOR_RESET"
}

log_error() {
    printf "%b[%s] %s%b\n" "$COLOR_ERROR" "ERROR" "$1" "$COLOR_RESET"
}

log_divider() {
    printf "%b%s%b\n" "$COLOR_DIVIDER" "==================================================" "$COLOR_RESET"
}

# 如果 macOS 没有 readlink -f，则使用 realpath 或 pwd 作为 fallback
resolve_path() {
    if command -v realpath >/dev/null 2>&1; then
        realpath "$1"
    elif command -v readlink >/dev/null 2>&1; then
        readlink -f "$1"
    else
        local dir
        local base
        dir="$(cd "$(dirname "$1")" && pwd)"
        base="$(basename "$1")"
        printf "%s/%s\n" "$dir" "$base"
    fi
}

# 确保全局凭据存储已启用，避免每次重复设置
if ! git config --global credential.helper >/dev/null 2>&1; then
    git config --global credential.helper store
    log_info "已启用 Git 全局凭据存储。"
else
    log_info "Git 全局凭据存储已启用。"
fi

# 提交信息支持传参，不传则使用默认信息
COMMIT_MESSAGE="${1:-Publish......}"

log_divider
log_info "开始执行 Git 自动推送脚本"
log_info "当前远程仓库："
git remote -v
log_divider

log_info "添加所有更改文件到暂存区。"
git add --all

if git diff --cached --quiet; then
    log_warn "暂存区没有新增更改，跳过提交。"
else
    log_info "正在提交更改，提交信息：$COMMIT_MESSAGE"
    if git commit -m "$COMMIT_MESSAGE"; then
        log_success "提交成功。"
    else
        log_error "提交失败，请检查 Git 状态。"
        exit 1
    fi
fi

push_with_retry() {
    local attempt=0
    while true; do
        attempt=$((attempt + 1))
        log_info "第 ${attempt} 次尝试推送到远程仓库..."
        if git push; then
            log_success "第 ${attempt} 次推送成功。"
            break
        else
            log_warn "推送失败，1 秒后重试。"
            sleep 1
        fi
    done
}

push_with_retry

log_divider
log_success "主仓库推送完成。"
log_divider

# 如果存在 ClawSpace 子目录，则进入该目录继续推送
SUBDIR="ClawSpace"
if [ -d "$SUBDIR" ]; then
    echo
    log_divider
    log_info "检测到子目录：$SUBDIR，准备同步子仓库。"
    cd "$SUBDIR" || {
        log_error "无法进入子目录 $SUBDIR。"
        exit 1
    }

    log_info "当前目录：$(pwd)"
    log_info "子仓库绝对路径：$(resolve_path .)"
    log_info "子仓库远程仓库信息："
    git remote -v

    if [ -x "./push.sh" ]; then
        log_info "执行子仓库 push.sh 脚本。"
        ./push.sh "$COMMIT_MESSAGE"
    else
        log_warn "子仓库中未找到可执行 push.sh，跳过子仓库推送。"
    fi

    log_divider
    log_success "子仓库推送完成。"
    log_divider
else
    log_warn "未发现 ClawSpace 子目录，跳过子仓库推送。"
fi
