#!/bin/bash

# 李居明Agent - GitHub API 上傳腳本（使用 curl）
# 需要 GitHub Personal Access Token

echo "=========================================="
echo "  李居明Agent - GitHub API 上傳腳本"
echo "=========================================="
echo ""

# 檢查是否提供了 token
if [ -z "$1" ]; then
    echo "使用方法: ./upload_api.sh YOUR_GITHUB_TOKEN"
    echo ""
    echo "如果沒有 Personal Access Token，請："
    echo "1. 打開 https://github.com/settings/tokens"
    echo "2. 點擊 'Generate new token (classic)'"
    echo "3. 勾選 'repo' 權限"
    echo "4. 複製 token 並執行："
    echo "   ./upload_api.sh YOUR_TOKEN_HERE"
    echo ""
    echo "=========================================="
    exit 1
fi

TOKEN="$1"
REPO_NAME="likuiming-agent"
GITHUB_USER="catalpachan"

echo "正在創建倉庫 $REPO_NAME ..."
echo ""

# 創建 GitHub 倉庫
curl -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO_NAME\",\"description\":\"李居明Agent 風水命理起名系統\",\"private\":false}" \
  2>/dev/null | grep -E '"message"|"full_name"' || true

echo ""
echo "添加遠程倉庫..."
git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git 2>/dev/null || true

echo ""
echo "推送代碼..."
git branch -M main
git push -u origin main

echo ""
echo "=========================================="
echo "✅ 完成！"
echo "https://github.com/$GITHUB_USER/$REPO_NAME"
echo "=========================================="
