# SuperClaude トラブルシューティングガイド 🔧

SuperClaudeフレームワークの問題に対する、簡単な修正から高度な診断まで。

## 簡単な修正（問題の90%）

**インストール検証:**
```bash
python3 -m SuperClaude --version    # 4.0.8と表示されるはず
SuperClaude install --list-components
```

**コマンドの問題:**
```bash
# Claude Codeでテスト:
/sc:brainstorm "テストプロジェクト"        # 発見的な質問が表示されるはず

# 応答がない場合: Claude Codeセッションを再起動
```

**解決チェックリスト:**
- [ ] バージョンコマンドが機能し、4.0.8と表示される
- [ ] `/sc:`コマンドがClaude Codeで応答する
- [ ] MCPサーバーがリスト表示される: `SuperClaude install --list-components | grep mcp`

## 一般的な問題

### インストールの問題

**パッケージのインストール失敗:**
```bash
# pipxユーザー向け
pipx uninstall SuperClaude
pipx install SuperClaude

# pipユーザー向け
pip uninstall SuperClaude
pip install --upgrade pip
pip install SuperClaude
```

**Permission Denied / PEP 668 エラー:**
```bash
# オプション1: pipxを使用（推奨）
pipx install SuperClaude

# オプション2: --userフラグ付きでpipを使用
pip install --user SuperClaude

# オプション3: パーミッションを修正
sudo chown -R $USER ~/.claude

# オプション4: 強制インストール（注意して使用）
pip install --break-system-packages SuperClaude
```

**コンポーネントの不足:**
```bash
python3 -m SuperClaude install --components core commands agents modes --force
```

### コマンドの問題

**コマンドが認識されない:**
1. Claude Codeを完全に再起動する
2. 検証: `python3 -m SuperClaude --version`
3. テスト: `/sc:brainstorm "test"`

**エージェントが起動しない:**
- 特定のキーワードを使用: `/sc:implement "安全なJWT認証"`
- 手動起動: `@agent-security "認証コードをレビュー"`

**パフォーマンスが遅い:**
```bash
/sc:analyze . --no-mcp               # MCPサーバーなしでテスト
/sc:analyze src/ --scope file        # スコープを制限
```

### MCPサーバーの問題

**サーバー接続の失敗:**
```bash
ls ~/.claude/.claude.json            # 設定が存在するか確認
node --version                       # Node.js 16+を検証
SuperClaude install --components mcp --force
```

**APIキーが必要 (Magic/Morphllm):**
```bash
export TWENTYFIRST_API_KEY="your_key"
export MORPH_API_KEY="your_key"
# または: /sc:command --no-mcp を使用
```

## 高度な診断

**システム分析:**
```bash
SuperClaude install --diagnose
cat ~/.claude/logs/superclaude.log | tail -50
```

**コンポーネント分析:**
```bash
ls -la ~/.claude/                    # インストールされたファイルを確認
grep -r "@" ~/.claude/CLAUDE.md      # インポートを検証
```

**インストールのリセット:**
```bash
SuperClaude backup --create          # まずバックアップ
SuperClaude uninstall
SuperClaude install --fresh
```

## ヘルプの入手

**ドキュメント:**
- [インストールガイド](../Getting-Started-jp/installation.md) - セットアップの問題
- [コマンドガイド](../User-Guide-jp/commands.md) - 使用法の問題

**コミュニティ:**
- [GitHub Issues](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues)
- 含める情報: OS、Pythonバージョン、エラーメッセージ、再現手順
