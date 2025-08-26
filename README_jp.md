<div align="center">

# 🚀 SuperClaude フレームワーク

### **Claude Codeを構造化された開発プラットフォームに変換**

<p align="center">
  <img src="https://img.shields.io/badge/version-4.0.8-blue" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
</p>

<p align="center">
  <a href="https://superclaude.netlify.app/">
    <img src="https://img.shields.io/badge/🌐_Visit_Website-blue" alt="Website">
  </a>
  <a href="https://pypi.org/project/SuperClaude/">
    <img src="https://img.shields.io/pypi/v/SuperClaude.svg?" alt="PyPI">
  </a>
  <a href="https://www.npmjs.com/package/@bifrost_inc/superclaude">
    <img src="https://img.shields.io/npm/v/@bifrost_inc/superclaude.svg" alt="npm">
  </a>
</p>

<p align="center">
  <a href="#-クイックインストール">クイックスタート</a> •
  <a href="#-プロジェクトの支援">支援</a> •
  <a href="#-v4の新機能">機能</a> •
  <a href="#-ドキュメント">ドキュメント</a> •
  <a href="#-貢献">貢献</a>
</p>

</div>

---

<div align="center">

## 📊 **フレームワーク統計**

| **コマンド** | **エージェント** | **モード** | **MCPサーバー** |
|:------------:|:----------:|:---------:|:---------------:|
| **21** | **14** | **5** | **6** |
| スラッシュコマンド | 専門AI | 行動パターン | 統合機能 |

</div>

---

<div align="center">

## 🎯 **概要**

SuperClaudeは、行動指示の注入とコンポーネントオーケストレーションを通じてClaude Codeを構造化開発プラットフォームに変換する**メタプログラミング設定フレームワーク**です。強力なツールとインテリジェントエージェントによる体系的なワークフロー自動化を提供します。

## ⚡ **クイックインストール**

### **インストール方法の選択**

| 方法 | コマンド | 適用対象 |
|:------:|---------|----------|
| **🐍 pipx** | `pipx install SuperClaude && pipx upgrade SuperClaude && SuperClaude install` | **✅ 推奨** - Linux/macOS |
| **📦 pip** | `pip install SuperClaude && pip upgrade SuperClaude && SuperClaude install` | 従来のPython環境 |
| **🌐 npm** | `npm install -g @bifrost_inc/superclaude && superclaude install` | クロスプラットフォーム、Node.jsユーザー |

</div>

<details>
<summary><b>⚠️ 重要：SuperClaude V3からのアップグレード</b></summary>

**SuperClaude V3がインストールされている場合、V4をインストールする前にアンインストールする必要があります：**

```bash
# V3を最初にアンインストール
関連するすべてのファイルとディレクトリを削除：
*.md *.json and commands/

# その後V4をインストール
pipx install SuperClaude && pipx upgrade SuperClaude && SuperClaude install
```

**✅ アップグレード中に保持されるもの：**
- ✓ カスタムスラッシュコマンド（`commands/sc/`外）
- ✓ `CLAUDE.md`内のカスタムコンテンツ
- ✓ Claude Codeの`.claude.json`、`.credentials.json`、`settings.json`、`settings.local.json`
- ✓ 追加したカスタムエージェントとファイル

**⚠️ 注意：** V3の他のSuperClaude関連`.json`ファイルは競合を引き起こす可能性があるため、削除する必要があります。

</details>

<details>
<summary><b>💡 PEP 668エラーのトラブルシューティング</b></summary>

```bash
# オプション1：pipxを使用（推奨）
pipx install SuperClaude

# オプション2：ユーザーインストール
pip install --user SuperClaude

# オプション3：強制インストール（注意して使用）
pip install --break-system-packages SuperClaude
```
</details>

---

<div align="center">

## 💖 **プロジェクトの支援**

> 正直なところ、SuperClaudeの維持には時間とリソースが必要です。
> 
> *テストのためのClaude Maxサブスクリプションだけで月額$100かかり、これはドキュメント作成、バグ修正、機能開発にかかる時間は含まれていません。*
> *日常業務でSuperClaudeに価値を見出している場合は、プロジェクトの支援をご検討ください。*
> *わずかな金額でも基本的な費用をカバーし、開発を継続する助けになります。*
> 
> すべての貢献者が重要です。コード、フィードバック、支援を通じて。このコミュニティの一員であることに感謝します！🙏

<table>
<tr>
<td align="center" width="33%">
  
### ☕ **Ko-fi**
[![Ko-fi](https://img.shields.io/badge/Support_on-Ko--fi-ff5e5b?logo=ko-fi)](https://ko-fi.com/superclaude)

*単発の貢献*

</td>
<td align="center" width="33%">

### 🎯 **Patreon**
[![Patreon](https://img.shields.io/badge/Become_a-Patron-f96854?logo=patreon)](https://patreon.com/superclaude)

*月額支援*

</td>
<td align="center" width="33%">

### 💜 **GitHub**
[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsor-30363D?logo=github-sponsors)](https://github.com/sponsors/SuperClaude-Org)

*柔軟な階層*

</td>
</tr>
</table>

### **あなたの支援により実現されるもの：**

| 項目 | コスト/影響 |
|------|-------------|
| 🔬 **Claude Maxテスト** | 検証・テストのため月額$100 |
| ⚡ **機能開発** | 新機能・改善 |
| 📚 **ドキュメント** | 包括的ガイド・例 |
| 🤝 **コミュニティサポート** | 迅速な問題対応・ヘルプ |
| 🔧 **MCP統合** | 新サーバー接続のテスト |
| 🌐 **インフラ** | ホスティング・デプロイコスト |

> **注意：** プレッシャーはありません - フレームワークは関係なくオープンソースです。人々が使用し、評価していることを知るだけでもモチベーションになります。コード、ドキュメントの貢献や普及も助けになります！🙏

</div>

---

<div align="center">

## 🎉 **V4の新機能**

> *バージョン4では、コミュニティのフィードバックと実際の使用パターンに基づく大幅な改善を実現しました。*

<table>
<tr>
<td width="50%">

### 🤖 **よりスマートなエージェントシステム**
**14の専門エージェント**によるドメインエキスパート：
- セキュリティエンジニアが実際の脆弱性を発見
- フロントエンドアーキテクトがUIパターンを理解
- コンテキストに基づく自動調整
- オンデマンドドメイン専門知識

</td>
<td width="50%">

### 📝 **改良された名前空間**
全コマンドに**`/sc:`プレフィックス**：
- カスタムコマンドとの競合なし
- 完全なライフサイクルをカバーする21コマンド
- ブレインストーミングからデプロイメントまで
- 清潔で整理されたコマンド構造

</td>
</tr>
<tr>
<td width="50%">

### 🔧 **MCPサーバー統合**
連携する**6つの強力なサーバー**：
- **Context7** → 最新ドキュメント
- **Sequential** → 複雑な分析
- **Magic** → UIコンポーネント生成
- **Playwright** → ブラウザテスト
- **Morphllm** → バルク変換
- **Serena** → セッション永続化

</td>
<td width="50%">

### 🎯 **行動モード**
異なるコンテキスト向けの**5つの適応モード**：
- **Brainstorming** → 適切な質問
- **Orchestration** → 効率的なツール調整
- **Token-Efficiency** → 30-50%のコンテキスト節約
- **Task Management** → 体系的な組織
- **Introspection** → メタ認知分析

</td>
</tr>
<tr>
<td width="50%">

### ⚡ **最適化されたパフォーマンス**
**小さなフレームワーク、大きなプロジェクト：**
- フレームワークフットプリントの削減
- コードにより多くのコンテキスト
- より長い会話が可能
- 複雑な操作の有効化

</td>
<td width="50%">

### 📚 **ドキュメントの全面刷新**
開発者向けの**完全な書き直し**：
- 実例・ユースケース
- よくある落とし穴の文書化
- 実践的なワークフローの包含
- より良いナビゲーション構造

</td>
</tr>
</table>

</div>

---

<div align="center">

## 📚 **ドキュメント**

### **SuperClaude完全ガイド**

<table>
<tr>
<th align="center">🚀 入門</th>
<th align="center">📖 ユーザーガイド</th>
<th align="center">🛠️ 開発者リソース</th>
<th align="center">📋 リファレンス</th>
</tr>
<tr>
<td valign="top">

- 📝 [**クイックスタートガイド**](Docs/Getting-Started/quick-start.md)  
  *迅速な起動と実行*

- 💾 [**インストールガイド**](Docs/Getting-Started/installation.md)  
  *詳細なセットアップ手順*

</td>
<td valign="top">

- 🎯 [**コマンドリファレンス**](Docs/User-Guide/commands.md)  
  *全21スラッシュコマンド*

- 🤖 [**エージェントガイド**](Docs/User-Guide/agents.md)  
  *14の専門エージェント*

- 🎨 [**行動モード**](Docs/User-Guide/modes.md)  
  *5つの適応モード*

- 🚩 [**フラグガイド**](Docs/User-Guide/flags.md)  
  *行動制御*

- 🔧 [**MCPサーバー**](Docs/User-Guide/mcp-servers.md)  
  *6つのサーバー統合*

- 💼 [**セッション管理**](Docs/User-Guide/session-management.md)  
  *状態の保存と復元*

</td>
<td valign="top">

- 🏗️ [**技術アーキテクチャ**](Docs/Developer-Guide/technical-architecture.md)  
  *システム設計詳細*

- 💻 [**コード貢献**](Docs/Developer-Guide/contributing-code.md)  
  *開発ワークフロー*

- 🧪 [**テスト・デバッグ**](Docs/Developer-Guide/testing-debugging.md)  
  *品質保証*

</td>
<td valign="top">

- ✨ [**ベストプラクティス**](Docs/Reference/quick-start-practices.md)  
  *プロのヒント・パターン*

- 📓 [**サンプルクックブック**](Docs/Reference/examples-cookbook.md)  
  *実世界のレシピ*

- 🔍 [**トラブルシューティング**](Docs/Reference/troubleshooting.md)  
  *よくある問題・修正*

</td>
</tr>
</table>

</div>

---

<div align="center">

## 🤝 **貢献**

### **SuperClaudeコミュニティに参加**

あらゆる種類の貢献を歓迎します！以下のように助けることができます：

| 優先度 | 領域 | 説明 |
|:--------:|------|-------------|
| 📝 **高** | ドキュメント | ガイドの改善、例の追加、誤字修正 |
| 🔧 **高** | MCP統合 | サーバー設定の追加、統合テスト |
| 🎯 **中** | ワークフロー | コマンドパターン・レシピの作成 |
| 🧪 **中** | テスト | テストの追加、機能の検証 |
| 🌐 **低** | i18n | 他言語へのドキュメント翻訳 |

<p align="center">
  <a href="CONTRIBUTING.md">
    <img src="https://img.shields.io/badge/📖_Read-Contributing_Guide-blue" alt="Contributing Guide">
  </a>
  <a href="https://github.com/SuperClaude-Org/SuperClaude_Framework/graphs/contributors">
    <img src="https://img.shields.io/badge/👥_View-All_Contributors-green" alt="Contributors">
  </a>
</p>

</div>

---

<div align="center">

## ⚖️ **ライセンス**

このプロジェクトは**MITライセンス**の下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください。

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?" alt="MIT License">
</p>

</div>

---

<div align="center">

## ⭐ **スター履歴**

<a href="https://www.star-history.com/#SuperClaude-Org/SuperClaude_Framework&Timeline">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=SuperClaude-Org/SuperClaude_Framework&type=Timeline&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=SuperClaude-Org/SuperClaude_Framework&type=Timeline" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=SuperClaude-Org/SuperClaude_Framework&type=Timeline" />
 </picture>
</a>


</div>

---

<div align="center">

### **🚀 SuperClaudeコミュニティによる情熱的な構築**

<p align="center">
  <sub>境界を押し広げる開発者のために❤️を込めて作成</sub>
</p>

<p align="center">
  <a href="#-superclaude-フレームワーク">トップに戻る ↑</a>
</p>

</div>