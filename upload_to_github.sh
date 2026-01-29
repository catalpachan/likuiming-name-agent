#!/bin/bash

# 李居明Agent - GitHub 上傳腳本
# 請在終端執行此腳本

echo "=========================================="
echo "  李居明Agent - GitHub 上傳腳本"
echo "=========================================="
echo ""

# 檢查是否已安裝 gh (GitHub CLI)
if ! command -v gh &> /dev/null; then
    echo "⚠️  未安裝 GitHub CLI (gh)"
    echo "請選擇以下方式之一："
    echo ""
    echo "方式 1: 使用 Homebrew 安裝 (需要管理員權限)"
    echo "  brew install gh"
    echo ""
    echo "方式 2: 手動創建倉庫"
    echo "  1. 打開 https://github.com/new"
    echo "  2. Repository name 輸入: likuiming-agent"
    echo "  3. 選擇 Public"
    echo "  4. 不要勾選任何選項"
    echo "  5. 點擊 Create repository"
    echo "  6. 執行以下命令："
    echo ""
    echo "  git remote add origin https://github.com/catalpachan/likuiming-agent.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
    echo ""
    echo "=========================================="
    exit 1
fi

echo "請登入 GitHub（如果尚未登入）..."
gh auth login

echo ""
echo "創建倉庫 likuiming-agent ..."
gh repo create likuiming-agent --public --description "李居明Agent 風水命理起名系統"

echo ""
echo "添加遠程倉庫..."
git remote add origin https://github.com/catalpachan/likuiming-agent.git

echo ""
echo "推送代碼到 GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "=========================================="
echo "✅ 完成！倉庫已創建並上傳"
echo "https://github.com/catalpachan/likuiming-agent"
echo "=========================================="
