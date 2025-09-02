<div align="center">

# 📦 SuperClaude インストールガイド

### **22個のコマンド、14のエージェント、6つのMCPサーバーでClaude Codeを強化**

<p align="center">
  <img src="https://img.shields.io/badge/version-4.0.8-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Linux%20|%20macOS%20|%20Windows-orange?style=for-the-badge" alt="Platform">
</p>

<p align="center">
  <a href="#-クイックインストール">クイックインストール</a> •
  <a href="#-要件">要件</a> •
  <a href="#-インストール方法">方法</a> •
  <a href="#-検証">検証</a> •
  <a href="#-トラブルシューティング">トラブルシューティング</a>
</p>

</div>

---

## ⚡ **クイックインストール**

<div align="center">

### **お好みの方法を選択してください**

| 方法 | コマンド | プラットフォーム | 最適な用途 |
|:------:|---------|:--------:|----------|
| **🐍 pipx** | `pipx install SuperClaude && SuperClaude install` | Linux/macOS | **✅ 推奨** - 独立した環境 |
| **📦 pip** | `pip install SuperClaude && SuperClaude install` | すべて | 従来のPythonセットアップ |
| **🌐 npm** | `npm install -g @bifrost_inc/superclaude && superclaude install` | すべて | Node.js開発者 |
| **🔧 開発者** | `git clone ... && pip install -e ".[dev]"` | すべて | 貢献者および開発者 |

</div>

---

## 📋 **要件**

<div align="center">

<table>
<tr>
<td align="center" width="50%">

### ✅ **必須**

| コンポーネント | バージョン | 確認コマンド |
|-----------|---------|---------------|
| **Python** | 3.8+ | `python3 --version` |
| **pip** | 最新 | `pip --version` |
| **Claude Code** | 最新 | `claude --version` |
| **ディスク容量** | 50MB | `df -h` |

</td>
<td align="center" width="50%">

### 💡 **任意**

| コンポーネント | 目的 | 確認コマンド |
|-----------|---------|---------------|
| **Node.js** | MCPサーバー | `node --version` |
| **Git** | バージョン管理 | `git --version` |
| **pipx** | 独立インストール | `pipx --version` |
| **RAM** | パフォーマンス | 1GB推奨 |

</td>
</tr>
</table>

</div>

<details>
<summary><b>🔍 クイックシステムチェック</b></summary>

```bash
# これを実行して、すべての要件を一度に確認します
python3 --version && echo "✅ Python OK" || echo "❌ Pythonが見つかりません"
claude --version && echo "✅ Claude Code OK" || echo "❌ Claude Codeが見つかりません"
node --version 2>/dev/null && echo "✅ Node.js OK (任意)" || echo "⚠️ Node.jsが見つかりません (任意)"
git --version 2>/dev/null && echo "✅ Git OK (任意)" || echo "⚠️ Gitが見つかりません (任意)"
```

</details>

---

## 🚀 **インストール方法**

<div align="center">

### **詳細なインストール手順**

</div>

### **方法1：pipx（推奨）**

<table>
<tr>
<td width="60%">

```bash
# pipxがなければインストール
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# SuperClaudeをインストール
pipx install SuperClaude

# インストーラーを実行
SuperClaude install
```

</td>
<td width="40%">

**✅ 利点:**
- 独立した環境
- 依存関係の競合なし
- クリーンなアンインストール
- 自動的なPATH設定

**📍 最適なユーザー:**
- Linux/macOSユーザー
- クリーンなシステムインストール
- 複数のPythonプロジェクト

</td>
</tr>
</table>

### **方法2：pip（従来の方法）**

<table>
<tr>
<td width="60%">

```bash
# 標準インストール
pip install SuperClaude

# またはユーザーインストール
pip install --user SuperClaude

# インストーラーを実行
SuperClaude install
```

</td>
<td width="40%">

**✅ 利点:**
- どこでも動作
- Pythonユーザーに馴染み深い
- 直接的なインストール

**📍 最適なユーザー:**
- Windowsユーザー
- 仮想環境
- 素早いセットアップ

</td>
</tr>
</table>

### **方法3：npm（クロスプラットフォーム）**

<table>
<tr>
<td width="60%">

```bash
# グローバルインストール
npm install -g @bifrost_inc/superclaude

# インストーラーを実行
superclaude install
```

</td>
<td width="40%">

**✅ 利点:**
- クロスプラットフォーム
- NPMエコシステム
- JavaScriptに精通している方向け

**📍 最適なユーザー:**
- Node.js開発者
- NPMユーザー
- クロスプラットフォームのニーズ

</td>
</tr>
</table>

### **方法4：開発者向けインストール**

<table>
<tr>
<td width="60%">

```bash
# リポジトリをクローン
git clone https://github.com/SuperClaude-Org/SuperClaude_Framework.git
cd SuperClaude_Framework

# 開発モードでインストール
pip install -e ".[dev]"

# インストールをテスト
SuperClaude install --dry-run
```

</td>
<td width="40%">

**✅ 利点:**
- 最新の機能
- プロジェクトへの貢献
- 完全なソースアクセス

**📍 最適なユーザー:**
- 貢献者
- カスタム変更
- 新機能のテスト

</td>
</tr>
</table>

---

## 🎛️ **インストールオプション**

<div align="center">

### **インストールのカスタマイズ**

| オプション | コマンド | 説明 |
|--------|---------|-------------|
| **対話モード** | `SuperClaude install` | プロンプトによるガイド付きセットアップ |
| **特定コンポーネント** | `SuperClaude install --components core mcp modes` | 必要なものだけをインストール |
| **プレビューモード** | `SuperClaude install --dry-run` | 何がインストールされるかを確認 |
| **強制インストール** | `SuperClaude install --force --yes` | すべての確認をスキップ |
| **コンポーネント一覧** | `SuperClaude install --list-components` | 利用可能なコンポーネントを表示 |

</div>

---

## ✅ **検証**

<div align="center">

### **インストールが成功したことを確認**

</div>

### **ステップ1：インストールの確認**

```bash
# SuperClaudeのバージョンを確認
python3 -m SuperClaude --version
# 期待される出力: SuperClaude 4.0.8

# インストールされたコンポーネントを一覧表示
SuperClaude install --list-components
# 期待される出力: 利用可能なコンポーネントのリスト
```

### **ステップ2：Claude Codeでのテスト**

```bash
# Claude Codeを開き、これらのコマンドを試してください：
/sc:brainstorm "test project"     # 発見的な質問がトリガーされるはずです
/sc:analyze README.md              # 構造化された分析が提供されるはずです
@agent-security "review code"     # セキュリティ専門家がアクティブになるはずです
```

### **ステップ3：インストールされるもの**

<div align="center">

| 場所 | 内容 | サイズ |
|----------|----------|------|
| `~/.claude/` | フレームワークファイル | 約50MB |
| `~/.claude/CLAUDE.md` | メインエントリポイント | 約2KB |
| `~/.claude/*.md` | 動作指示 | 約200KB |
| `~/.claude/claude-code-settings.json` | MCP設定 | 約5KB |

</div>

---

## 🛠️ **管理**

<div align="center">

<table>
<tr>
<th>📦 更新</th>
<th>💾 バックアップ</th>
<th>🗑️ アンインストール</th>
</tr>
<tr>
<td>

```bash
# 最新版に更新
pip install --upgrade SuperClaude
SuperClaude update
```

</td>
<td>

```bash
# バックアップを作成
SuperClaude backup --create

# バックアップを復元
SuperClaude backup --restore [file]
```

</td>
<td>

```bash
# フレームワークを削除
SuperClaude uninstall

# パッケージをアンインストール
pip uninstall SuperClaude
```

</td>
</tr>
</table>

</div>

---

## 🔧 **トラブルシューティング**

<details>
<summary><b>❌ PEP 668 エラー（Pythonパッケージ管理）</b></summary>

このエラーは、外部で管理されているPython環境を持つシステムで発生します。

**解決策（推奨順）：**

```bash
# オプション1：pipxを使用（推奨）
pipx install SuperClaude

# オプション2：ユーザーインストール
pip install --user SuperClaude

# オプション3：仮想環境
python3 -m venv superclaude-env
source superclaude-env/bin/activate  # Linux/macOS
# または
superclaude-env\Scripts\activate  # Windows
pip install SuperClaude

# オプション4：強制（注意して使用）
pip install --break-system-packages SuperClaude
```

</details>

<details>
<summary><b>❌ コマンドが見つかりません</b></summary>

インストール後に `SuperClaude` コマンドが見つからない場合：

```bash
# パッケージがインストールされているか確認
python3 -m pip show SuperClaude

# Pythonモジュールとして実行
python3 -m SuperClaude install

# PATHに追加（--userを使用した場合）
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # Linux
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # macOS
```

</details>

<details>
<summary><b>❌ Claude Codeが見つかりません</b></summary>

Claude Codeがインストールされていないか、PATHにない場合：

1. [https://claude.ai/code](https://claude.ai/code) からダウンロード
2. プラットフォームの指示に従ってインストール
3. `claude --version` で確認
4. インストール後にターミナルを再起動

</details>

<details>
<summary><b>❌ パーミッションが拒否されました</b></summary>

インストール中にパーミッションエラーが発生した場合：

```bash
# ユーザーインストールを使用
pip install --user SuperClaude

# またはsudoを使用（非推奨）
sudo pip install SuperClaude

# より良い方法：pipxを使用
pipx install SuperClaude
```

</details>

<details>
<summary><b>❌ Pythonまたはpipが見つかりません</b></summary>

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**macOS:**
```bash
# 必要に応じてHomebrewを先にインストール
brew install python3
```

**Windows:**
- [python.org](https://python.org) からダウンロード
- インストール中に「Add Python to PATH」をチェック
- インストール後にターミナルを再起動

</details>

---

## 📚 **次のステップ**

<div align="center">

### **学習の道のり**

<table>
<tr>
<th>🌱 ここから始める</th>
<th>🌿 スキルを広げる</th>
<th>🌲 フレームワークをマスターする</th>
</tr>
<tr>
<td valign="top">

**最初の1週間:**
- [クイックスタートガイド](quick-start.md)
- [コマンドリファレンス](../User-Guide-jp/commands.md)
- `/sc:brainstorm` を試す

</td>
<td valign="top">

**2〜3週目:**
- [動作モード](../User-Guide-jp/modes.md)
- [エージェントガイド](../User-Guide-jp/agents.md)
- [サンプル集](../Reference-jp/examples-cookbook.md)

</td>
<td valign="top">

**上級:**
- [MCPサーバー](../User-Guide-jp/mcp-servers.md)
- [技術アーキテクチャ](../Developer-Guide-jp/technical-architecture.md)
- [コード貢献](../Developer-Guide-jp/contributing-code.md)

</td>
</tr>
</table>

</div>

---

<div align="center">

### **🎉 インストール完了！**

これで以下にアクセスできます：

<p align="center">
  <b>22個のコマンド</b> • <b>14のAIエージェント</b> • <b>6つの動作モード</b> • <b>6つのMCPサーバー</b>
</p>

**準備はいいですか？** Claude Codeで `/sc:brainstorm` を試して、最初のSuperClaude体験を始めましょう！

<p align="center">
  <a href="quick-start.md">
    <img src="https://img.shields.io/badge/📖_続きを読む-クイックスタートガイド-blue?style=for-the-badge" alt="Quick Start">
  </a>
</p>

</div>
