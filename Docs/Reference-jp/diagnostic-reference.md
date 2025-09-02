# SuperClaude 診断リファレンスガイド

## 概要

このガイドは、SuperClaudeのコンテキストファイルと設定に関する問題の診断手順を提供します。SuperClaudeは（実行中のソフトウェアではなく）テキストファイルのコレクションであるため、診断はファイルの検証と設定の確認に焦点を当てます。

**重要**: 監視するプロセス、測定するパフォーマンスメトリクス、分析するシステムリソースはありません。SuperClaudeは純粋にClaude Codeが読み込む設定ファイルです。

## クイック診断

### 1行ヘルスチェック

```bash
# 簡単なステータスチェック
ls ~/.claude/CLAUDE.md && echo "✅ SuperClaudeはインストールされています" || echo "❌ インストールされていません"
```

### 基本的な診断コマンド

```bash
# SuperClaudeがインストールされているか確認
python3 -m SuperClaude --version

# コンテキストファイルの数を数える
find ~/.claude -name "*.md" -type f | wc -l
# 期待される結果: 40以上のファイル

# ファイルサイズを確認 (コンテキストファイルには内容があるべき)
find ~/.claude -name "*.md" -type f -size 0
# 期待される結果: 出力なし (空ファイルなし)

# ディレクトリ構造を検証
tree -L 2 ~/.claude/
# またはtreeコマンドなしで:
ls -la ~/.claude/
```

## ファイルシステム診断

### コンテキストファイルの検証

```bash
#!/bin/bash
# 包括的なコンテキストファイルチェック

echo "=== SuperClaude コンテキストファイル診断 ==="

# 期待される数を定義
EXPECTED_AGENTS=14
EXPECTED_COMMANDS=22
EXPECTED_MODES=6

# 実際のファイルを数える
ACTUAL_AGENTS=$(ls ~/.claude/agents/*.md 2>/dev/null | wc -l)
ACTUAL_COMMANDS=$(ls ~/.claude/commands/sc/*.md 2>/dev/null | wc -l)
ACTUAL_MODES=$(ls ~/.claude/modes/*.md 2>/dev/null | wc -l)

# 結果を報告
echo "エージェント: $ACTUAL_AGENTS/$EXPECTED_AGENTS $([ $ACTUAL_AGENTS -ge $EXPECTED_AGENTS ] && echo ✅ || echo ⚠️)"
echo "コマンド: $ACTUAL_COMMANDS/$EXPECTED_COMMANDS $([ $ACTUAL_COMMANDS -ge $EXPECTED_COMMANDS ] && echo ✅ || echo ⚠️)"
echo "モード: $ACTUAL_MODES/$EXPECTED_MODES $([ $ACTUAL_MODES -ge $EXPECTED_MODES ] && echo ✅ || echo ⚠️)"

# コアファイルの確認
for file in CLAUDE.md FLAGS.md RULES.md PRINCIPLES.md; do
    if [ -f ~/.claude/$file ]; then
        SIZE=$(wc -c < ~/.claude/$file)
        echo "$file: $SIZE バイト ✅"
    else
        echo "$file: 見つかりません ❌"
    fi
done
```

### インポートシステムの確認

```bash
# CLAUDE.mdのインポート文を検証
echo "=== インポートシステムチェック ==="
if [ -f ~/.claude/CLAUDE.md ]; then
    echo "CLAUDE.mdで見つかったインポート:"
    grep "^@import" ~/.claude/CLAUDE.md

    # インポート文の数を数える
    IMPORT_COUNT=$(grep -c "^@import" ~/.claude/CLAUDE.md)
    echo "合計インポート数: $IMPORT_COUNT"

    if [ $IMPORT_COUNT -ge 5 ]; then
        echo "✅ インポートシステムは正しく設定されています"
    else
        echo "⚠️ いくつかのインポートが欠けている可能性があります"
    fi
else
    echo "❌ CLAUDE.mdが見つかりません"
fi
```

## 設定診断

### MCPサーバー設定の確認

```bash
# MCP設定を確認
echo "=== MCP設定診断 ==="

CONFIG_FILE=~/.claude.json

if [ -f "$CONFIG_FILE" ]; then
    echo "✅ 設定ファイルが存在します"

    # JSON構文を検証
    if python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
        echo "✅ 有効なJSON構文です"

        # 設定されているサーバーを一覧表示
        echo "設定済みのMCPサーバー:"
        python3 -c "
import json
with open('$HOME/.claude.json') as f:
    config = json.load(f)
    if 'mcpServers' in config:
        for server in config['mcpServers']:
            print(f'  - {server}')
    else:
        print('  設定されているサーバーはありません')
        "
    else
        echo "❌ $CONFIG_FILE のJSON構文が無効です"
    fi
else
    echo "⚠️ MCP設定ファイルが見つかりません"
    echo "  MCPサーバーを使用しない場合は問題ありません"
fi
```

### パーミッション診断

```bash
# ファイルパーミッションを確認
echo "=== ファイルパーミッションチェック ==="

# ファイルが読み取り可能か確認
UNREADABLE_COUNT=0
for file in ~/.claude/**/*.md; do
    if [ ! -r "$file" ]; then
        echo "❌ 読み取り不可: $file"
        ((UNREADABLE_COUNT++))
    fi
done

if [ $UNREADABLE_COUNT -eq 0 ]; then
    echo "✅ すべてのコンテキストファイルは読み取り可能です"
else
    echo "⚠️ 読み取り不可能なファイルが $UNREADABLE_COUNT 個見つかりました"
    echo "修正するには: chmod 644 ~/.claude/**/*.md"
fi

# ディレクトリパーミッションを確認
for dir in ~/.claude ~/.claude/agents ~/.claude/commands ~/.claude/modes; do
    if [ -d "$dir" ]; then
        if [ -x "$dir" ]; then
            echo "✅ $dir はアクセス可能です"
        else
            echo "❌ $dir はアクセスできません"
        fi
    else
        echo "❌ $dir は存在しません"
    fi
done
```

## 一般的な問題の診断

### 問題: コマンドが認識されない

```bash
# コマンドの問題を診断
COMMAND="implement"  # テストするコマンドを変更

echo "=== コマンド診断: $COMMAND ==="

FILE=~/.claude/commands/sc/$COMMAND.md

if [ -f "$FILE" ]; then
    echo "✅ コマンドファイルが存在します"

    # ファイルサイズを確認
    SIZE=$(wc -c < "$FILE")
    if [ $SIZE -gt 100 ]; then
        echo "✅ ファイルに内容があります ($SIZE バイト)"
    else
        echo "⚠️ ファイルが小さすぎるようです ($SIZE バイト)"
    fi

    # メタデータを確認
    if head -10 "$FILE" | grep -q "^---"; then
        echo "✅ メタデータヘッダーがあります"
    else
        echo "⚠️ メタデータヘッダーがありません"
    fi

    # コマンドパターンを確認
    if grep -q "/sc:$COMMAND" "$FILE"; then
        echo "✅ コマンドパターンが含まれています"
    else
        echo "⚠️ コマンドパターンがありません"
    fi
else
    echo "❌ コマンドファイルが見つかりません: $FILE"
    echo "利用可能なコマンド:"
    ls ~/.claude/commands/sc/ | sed 's/.md$//'
fi
```

### 問題: エージェントが起動しない

```bash
# エージェントの問題を診断
AGENT="python-expert"  # テストするエージェントを変更

echo "=== エージェント診断: $AGENT ==="

FILE=~/.claude/agents/$AGENT.md

if [ -f "$FILE" ]; then
    echo "✅ エージェントファイルが存在します"

    # トリガーキーワードを確認
    echo "見つかったトリガーキーワード:"
    grep -A 5 "## Triggers" "$FILE" | tail -n +2

    # メタデータを確認
    if head -10 "$FILE" | grep -q "^name:"; then
        echo "✅ メタデータがあります"
    else
        echo "⚠️ メタデータがありません"
    fi
else
    echo "❌ エージェントファイルが見つかりません: $FILE"
    echo "利用可能なエージェント:"
    ls ~/.claude/agents/ | sed 's/.md$//'
fi
```

## インストールの修復

### クイック修正スクリプト

```bash
#!/bin/bash
# SuperClaude クイック修正スクリプト

echo "=== SuperClaude クイック修正 ==="

# 一般的な問題を確認して修正する
ISSUES_FOUND=0

# パーミッションを修正
echo "ファイルパーミッションを修正中..."
chmod 644 ~/.claude/*.md 2>/dev/null
chmod 644 ~/.claude/**/*.md 2>/dev/null
chmod 755 ~/.claude ~/.claude/agents ~/.claude/commands ~/.claude/modes 2>/dev/null

# 不足しているディレクトリを確認
for dir in agents commands modes; do
    if [ ! -d ~/.claude/$dir ]; then
        echo "⚠️ 不足しているディレクトリ: $dir"
        echo "  実行: SuperClaude install --components $dir"
        ((ISSUES_FOUND++))
    fi
done

# 空のファイルを確認
EMPTY_FILES=$(find ~/.claude -name "*.md" -type f -size 0 2>/dev/null)
if [ -n "$EMPTY_FILES" ]; then
    echo "⚠️ 空のファイルが見つかりました:"
    echo "$EMPTY_FILES"
    echo "  実行: SuperClaude install --force"
    ((ISSUES_FOUND++))
fi

if [ $ISSUES_FOUND -eq 0 ]; then
    echo "✅ 問題は見つかりませんでした"
else
    echo "$ISSUES_FOUND 個の問題が見つかりました - 上記の推奨事項を参照してください"
fi
```

### 完全な再インストール

```bash
# 完全なクリーン再インストール
echo "=== クリーン再インストール ==="

# 現在のインストールをバックアップ
BACKUP_DIR=~/.claude.backup.$(date +%Y%m%d_%H%M%S)
if [ -d ~/.claude ]; then
    cp -r ~/.claude "$BACKUP_DIR"
    echo "✅ $BACKUP_DIR にバックアップしました"
fi

# 現在のインストールを削除
rm -rf ~/.claude

# 再インストール
SuperClaude install

# インストールを検証
if [ -f ~/.claude/CLAUDE.md ]; then
    echo "✅ 再インストールに成功しました"
else
    echo "❌ 再インストールに失敗しました"
    echo "バックアップを復元中..."
    cp -r "$BACKUP_DIR" ~/.claude
fi
```

## これらの診断が「行わない」こと

### 適用外の概念

- **CPU/メモリ監視**: 監視するプロセスなし
- **パフォーマンスメトリクス**: 測定するコード実行なし
- **ネットワーク分析**: ネットワーク操作なし (MCPを除く)
- **プロセス管理**: 実行中のプロセスなし
- **リソース最適化**: 消費されるリソースなし
- **実行時間計測**: 実行されるコードなし

### 重要な点に焦点を当てる

- **ファイルの存在**: コンテキストファイルはインストールされているか？
- **ファイルの整合性**: ファイルは読み取り可能で完全か？
- **設定の有効性**: JSON構文は正しいか？
- **ディレクトリ構造**: 構成は正しいか？
- **パーミッション**: Claude Codeはファイルを読み取れるか？

## まとめ

SuperClaudeの診断はシンプルです: ファイルの存在を確認し、読み取り可能であることをチェックし、設定が有効であることを確認します。Claude Codeが読み込むただのテキストファイルなので、複雑なシステム監視やパフォーマンス分析は不要です。ファイルが存在し、読み取り可能であれば、SuperClaudeは機能しています。
