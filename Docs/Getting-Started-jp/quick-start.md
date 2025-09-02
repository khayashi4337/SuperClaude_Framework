<div align="center">

# 🚀 SuperClaude クイックスタートガイド

### **Claude Codeのためのコンテキストエンジニアリングフレームワーク**

<p align="center">
  <img src="https://img.shields.io/badge/Framework-Context_Engineering-purple?style=for-the-badge" alt="Framework">
  <img src="https://img.shields.io/badge/Version-4.0.8-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Time_to_Start-5_Minutes-green?style=for-the-badge" alt="Quick Start">
</p>

> **💡 主要な洞察**: SuperClaudeはClaude Codeを置き換えるのではなく、振る舞いに関するコンテキスト注入を通じて**設定し、強化します**。

<p align="center">
  <a href="#-仕組み">仕組み</a> •
  <a href="#-すぐに開始">すぐに開始</a> •
  <a href="#-コアコンポーネント">コンポーネント</a> •
  <a href="#-ワークフローパターン">ワークフロー</a> •
  <a href="#-使用する場面">使用する場面</a>
</p>

</div>

---

<div align="center">

## 📊 **フレームワークの能力**

| **コマンド** | **AIエージェント** | **振る舞いモード** | **MCPサーバー** |
|:------------:|:-------------:|:-------------------:|:---------------:|
| **22** | **14** | **6** | **6** |
| `/sc:` トリガー | ドメイン専門家 | コンテキスト適応 | ツール統合 |

</div>

---

## 🎯 **仕組み**

<div align="center">

### **フレームワークのアーキテクチャフロー**

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  ユーザー入力    │────>│   Claude Code    │────>│  コンテキストファイル │
│  /sc:command    │     │  コンテキストを読み込む │     │  (.md 振る舞い)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │                          │
                               ▼                          ▼
┌─────────────────┐      ┌──────────────────┐     ┌─────────────────┐
│   強化された      │<─────│    振る舞いの      │<────│   MCPサーバー   │
│   レスポンス      │      │    アクティベーション │     │ (設定されている場合) │
└─────────────────┘      └──────────────────┘     └─────────────────┘
```

**仕組みの要点**: `/sc:brainstorm` と入力すると、Claudeはインストールされた`.md`ファイルから振る舞いの指示を読み込み、強化された能力で応答します。

</div>

---

## ⚡ **すぐに開始**

<div align="center">

### **インストールから最初のコマンドまで5分の道のり**

</div>

<table>
<tr>
<th width="50%">📦 ステップ1：インストール（ターミナル）</th>
<th width="50%">💬 ステップ2：使用（Claude Code）</th>
</tr>
<tr>
<td valign="top">

```bash
# pipxでのクイックインストール
pipx install SuperClaude && SuperClaude install

# または従来のpip
pip install SuperClaude && SuperClaude install

# またはnpm経由
npm install -g @bifrost_inc/superclaude && superclaude install
```

</td>
<td valign="top">

```text
# 対話的な発見
/sc:brainstorm "タスク管理用のWebアプリ"

# 既存コードの分析
/sc:analyze src/

# 実装の生成
/sc:implement "ユーザー認証"

# 専門家を起動
@agent-security "認証フローをレビュー"
```

</td>
</tr>
</table>

<details>
<summary><b>🎥 舞台裏で何が起きているか</b></summary>

1. **コンテキストの読み込み**: Claude Codeが`CLAUDE.md`経由で振る舞いの`.md`ファイルをインポートします。
2. **パターン認識**: `/sc:`と`@agent-`のトリガーパターンを認識します。
3. **振る舞いのアクティベーション**: コンテキストファイルから対応する指示を適用します。
4. **MCP統合**: 利用可能な場合、設定された外部ツールを使用します。
5. **応答の強化**: 包括的な応答のためにフレームワークのパターンに従います。

</details>

---

## 🔧 **コアコンポーネント**

<div align="center">

### **SuperClaudeの4つの柱**

<table>
<tr>
<td align="center" width="25%">

### 📝 **コマンド**
<h2>22</h2>

**スラッシュコマンド**

`/sc:brainstorm`
`/sc:implement`
`/sc:analyze`
`/sc:workflow`

*ワークフロー自動化*

</td>
<td align="center" width="25%">

### 🤖 **エージェント**
<h2>14</h2>

**AI専門家**

`@agent-architect`
`@agent-security`
`@agent-frontend`
`@agent-backend`

*ドメイン専門知識*

</td>
<td align="center" width="25%">

### 🎯 **モード**
<h2>6</h2>

**振る舞いモード**

ブレインストーミング
内省
オーケストレーション
タスク管理

*コンテキスト適応*

</td>
<td align="center" width="25%">

### 🔌 **MCP**
<h2>6</h2>

**サーバー統合**

Context7 (ドキュメント)
Sequential (分析)
Magic (UI)
Playwright (テスト)

*強化されたツール*

</td>
</tr>
</table>

</div>

---

## 📚 **ワークフローパターン**

<div align="center">

### **完全な開発ライフサイクル**

</div>

### **🌟 最初のプロジェクトセッション**

<table>
<tr>
<th>ステップ</th>
<th>コマンド</th>
<th>何が起こるか</th>
</tr>
<tr>
<td><b>1. 発見</b></td>
<td><code>/sc:brainstorm "eコマースアプリ"</code></td>
<td>対話的な要件の探求</td>
</tr>
<tr>
<td><b>2. コンテキスト読み込み</b></td>
<td><code>/sc:load src/</code></td>
<td>既存のプロジェクト構造をインポート</td>
</tr>
<tr>
<td><b>3. 分析</b></td>
<td><code>/sc:analyze --focus architecture</code></td>
<td>詳細なアーキテクチャレビュー</td>
</tr>
<tr>
<td><b>4. 計画</b></td>
<td><code>/sc:workflow "決済統合"</code></td>
<td>実装ロードマップを生成</td>
</tr>
<tr>
<td><b>5. 実装</b></td>
<td><code>/sc:implement "Stripeチェックアウト"</code></td>
<td>ベストプラクティスに基づき構築</td>
</tr>
<tr>
<td><b>6. 検証</b></td>
<td><code>/sc:test --coverage</code></td>
<td>包括的なテスト</td>
</tr>
<tr>
<td><b>7. セッション保存</b></td>
<td><code>/sc:save "payment-complete"</code></td>
<td>次のセッションのために永続化</td>
</tr>
</table>

### **🎨 ドメイン固有のワークフロー**

<div align="center">

| ドメイン | トリガー | 専門家の起動 | MCPサーバー |
|--------|---------|----------------------|------------|
| **フロントエンド** | UIコンポーネント要求 | `@agent-frontend` | Magic |
| **バックエンド** | APIエンドポイント作成 | `@agent-backend` | Sequential |
| **セキュリティ** | 認証の実装 | `@agent-security` | Context7 |
| **テスト** | E2Eテストシナリオ | `@agent-qa` | Playwright |
| **DevOps** | デプロイメント設定 | `@agent-devops` | Morphllm |

</div>

---

## 🎯 **使用する場面**

<div align="center">

### **SuperClaude vs 標準のClaude Code**

<table>
<tr>
<th width="50%">✅ SuperClaudeを使うべき時</th>
<th width="50%">💭 標準のClaudeを使うべき時</th>
</tr>
<tr>
<td valign="top">

**最適な用途:**
- 🏗️ 完全なソフトウェアプロジェクトの構築
- 📊 品質ゲートを持つ体系的なワークフロー
- 🔄 複雑なマルチコンポーネントシステム
- 💾 永続性が必要な長期プロジェクト
- 👥 標準を伴うチームコラボレーション
- 🎯 ドメイン固有の専門知識が必要な場合

**例:**
- 「フルスタックアプリケーションを構築して」
- 「安全な認証を実装して」
- 「レガシーコードベースをリファクタリングして」
- 「包括的なテストスイートを作成して」

</td>
<td valign="top">

**より適している用途:**
- 💡 簡単な質問や説明
- ⚡ 一度きりのコーディングタスク
- 📚 プログラミングコンセプトの学習
- 🧪 素早いプロトタイプや実験
- 🔍 コードスニペットの生成
- ❓ 一般的なプログラミングの助け

**例:**
- 「async/awaitの仕組みを説明して」
- 「ソート関数を書いて」
- 「このエラーメッセージをデバッグして」
- 「このループを関数型に変換して」

</td>
</tr>
</table>

</div>

---

## 🎓 **学習パス**

<div align="center">

### **マスターへの4週間の道のり**

<table>
<tr>
<th>週</th>
<th>フォーカス</th>
<th>スキル</th>
<th>マイルストーン</th>
</tr>
<tr>
<td align="center"><b>1</b><br/>🌱</td>
<td><b>コアコマンド</b></td>
<td>
• <code>/sc:brainstorm</code><br/>
• <code>/sc:analyze</code><br/>
• <code>/sc:implement</code>
</td>
<td>最初のプロジェクトを完了</td>
</tr>
<tr>
<td align="center"><b>2</b><br/>🌿</td>
<td><b>振る舞いモード</b></td>
<td>
• モードの組み合わせ<br/>
• フラグの使用<br/>
• コンテキストの最適化
</td>
<td>ワークフローを最適化</td>
</tr>
<tr>
<td align="center"><b>3</b><br/>🌿</td>
<td><b>MCPサーバー</b></td>
<td>
• サーバー設定<br/>
• ツール統合<br/>
• 強化された能力
</td>
<td>ツールの完全活用</td>
</tr>
<tr>
<td align="center"><b>4</b><br/>🌲</td>
<td><b>高度なパターン</b></td>
<td>
• カスタムワークフロー<br/>
• セッション管理<br/>
• チームパターン
</td>
<td>フレームワークの習得</td>
</tr>
</table>

</div>

---

## 💡 **主要な洞察**

<div align="center">

### **SuperClaudeの価値を理解する**

<table>
<tr>
<td width="33%" align="center">

### 🧠 **ソフトウェアではない**
**フレームワークです**

SuperClaudeは振る舞いの設定であり、スタンドアロンのソフトウェアではありません。すべてがClaude Codeを通じて実行されます。

</td>
<td width="33%" align="center">

### 🔄 **体系的**
**アドホックではない**

ランダムなリクエストを、品質ゲートと検証を備えた構造化されたワークフローに変換します。

</td>
<td width="33%" align="center">

### 🚀 **進歩的**
**複雑ではない**

基本的なコマンドから始められます。複雑さは必要に応じて自然に現れます。

</td>
</tr>
</table>

</div>

---

## 📖 **次のステップ**

<div align="center">

### **学習の旅を続ける**

<table>
<tr>
<th>🌱 初級者</th>
<th>🌿 中級者</th>
<th>🌲 上級者</th>
</tr>
<tr>
<td valign="top">

**最初の1週間:**
- [インストールガイド](installation.md)
- [コマンドリファレンス](../User-Guide-jp/commands.md)
- [サンプル集](../Reference-jp/examples-cookbook.md)

`/sc:brainstorm` から始める

</td>
<td valign="top">

**スキルの向上:**
- [振る舞いモード](../User-Guide-jp/modes.md)
- [エージェントガイド](../User-Guide-jp/agents.md)
- [セッション管理](../User-Guide-jp/session-management.md)

モードの組み合わせを探る

</td>
<td valign="top">

**エキスパートの利用法:**
- [MCPサーバー](../User-Guide-jp/mcp-servers.md)
- [技術アーキテクチャ](../Developer-Guide-jp/technical-architecture.md)
- [貢献](../Developer-Guide-jp/contributing-code.md)

カスタムワークフローを作成する

</td>
</tr>
</table>

<p align="center">
  <a href="../User-Guide-jp/commands.md">
    <img src="https://img.shields.io/badge/📚_探す-全22コマンド-blue?style=for-the-badge" alt="Commands">
  </a>
  <a href="../Reference-jp/examples-cookbook.md">
    <img src="https://img.shields.io/badge/🍳_試す-実例-green?style=for-the-badge" alt="Examples">
  </a>
</p>

</div>

---

<div align="center">

### **🎉 開発ワークフローを変革する準備はできましたか？**

<p align="center">
  <b>今すぐClaude Codeで </b><code>/sc:brainstorm</code><b> から始めましょう！</b>
</p>

<p align="center">
  <sub>SuperClaude v4.0.8 - Claude Codeのためのコンテキストエンジニアリング</sub>
</p>

</div>
