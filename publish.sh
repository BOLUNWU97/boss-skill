#!/bin/bash
# 发布 boss-skill 到 GitHub

set -e

echo "🚀 老板.skill 发布脚本"
echo "====================="
echo ""

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装，请先安装 Git"
    exit 1
fi

# 检查 gh CLI
if ! command -v gh &> /dev/null; then
    echo "⚠️  gh CLI 未安装，将使用手动方式"
    USE_GH=false
else
    USE_GH=true
fi

# 初始化 Git（如果需要）
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git add .
    git commit -m "Initial commit: 老板.skill v2.0 - 把老板蒸馏成AI，越苛刻越好"
fi

# 检查远程仓库
if git remote -v | grep -q origin; then
    echo "⚠️  远程仓库已存在"
    read -p "是否更新远程仓库？ (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "取消发布"
        exit 0
    fi
else
    echo ""
    echo "📋 需要创建 GitHub 仓库"
    echo ""
    echo "方式1: 使用 GitHub 网页（推荐）"
    echo "  1. 打开 https://github.com/new"
    echo "  2. 仓库名: boss-skill"
    echo "  3. 描述: 把老板蒸馏成 AI Skill，越苛刻越好"
    echo "  4. 选择 Public"
    echo "  5. 不要勾选 Initialize repository"
    echo "  6. 点击 Create repository"
    echo "  7. 复制仓库 URL"
    echo ""
    echo "方式2: 使用 gh CLI"
    echo "  gh auth login"
    echo "  gh repo create boss-skill --public --source=. --push"
    echo ""
    read -p "请先创建仓库，然后按回车继续..."

    echo ""
    echo "📎 请输入 GitHub 仓库 URL（例如: https://github.com/用户名/boss-skill.git）:"
    read REPO_URL

    if [ -z "$REPO_URL" ]; then
        echo "❌ 未输入仓库 URL，取消发布"
        exit 1
    fi

    echo "🔗 添加远程仓库..."
    git remote add origin "$REPO_URL"
fi

# 检查分支
CURRENT_BRANCH=$(git branch --show-current)
if [ -z "$CURRENT_BRANCH" ]; then
    CURRENT_BRANCH="main"
fi

echo ""
echo "📤 推送到 GitHub..."
echo "   分支: $CURRENT_BRANCH"
echo ""

git branch -M main
git push -u origin main --force

echo ""
echo "====================="
echo "✅ 发布成功！"
echo ""
echo "📝 下一步："
echo "  1. 打开 GitHub 仓库页面"
echo "  2. 创建 Release (可选)"
echo "  3. 提交到 https://clawhub.ai (可选)"
echo ""
echo "🔗 仓库地址:"
git remote -v | grep origin | head -1
echo ""
