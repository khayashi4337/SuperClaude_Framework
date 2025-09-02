# SuperClaudeフレームワーク 開発者ガイド インデックス

## ドキュメントナビゲーションガイド

このインデックスは、効率的な情報発見のためにトピックとスキルレベル別に整理された、すべてのSuperClaudeフレームワーク開発ドキュメントへの包括的なアクセスを提供します。

### クイックナビゲーション

**新規貢献者向け**: [貢献ガイド → セットアップ](contributing-code.md#development-setup) から始める

**システム理解のため**: [技術アーキテクチャガイド → コンテキストアーキテクチャ](technical-architecture.md#context-file-architecture) から始める

**検証のため**: [検証ガイド → インストールチェック](testing-debugging.md#installation-verification) から始める

---

## 主要ドキュメント

### 📋 [コンテキストファイル貢献ガイド](contributing-code.md)
**目的**: 完全なコンテキストファイル開発と貢献のガイドライン
**対象読者**: フレームワーク貢献者とコンテキストファイル開発者
**長さ**: コンテキストファイルの実体に焦点を当てた約1,000行

**主要セクション**:
- [開発セットアップ](contributing-code.md#development-setup) - 環境設定と前提条件
- [コンテキストファイルガイドライン](contributing-code.md#context-file-guidelines) - 標準と構造
- [開発ワークフロー](contributing-code.md#development-workflow) - Gitワークフローと提出プロセス
- [コンポーネントへの貢献](contributing-code.md#contributing-to-components) - エージェント、コマンド、モードの開発
- [ファイル検証](contributing-code.md#file-validation) - コンテキストファイルの検証方法

### 🏗️ [コンテキストアーキテクチャガイド](technical-architecture.md)
**目的**: コンテキストファイルがどのように機能し、構造化されているかを理解する
**対象読者**: SuperClaudeを理解または拡張したいすべての人
**長さ**: コンテキストファイルパターンとClaude Code統合に焦点を当てた約800行

**主要セクション**:
- [コンテキストファイルアーキテクチャ](technical-architecture.md#context-file-architecture) - ディレクトリ構造とファイルタイプ
- [インポートシステム](technical-architecture.md#the-import-system) - Claude Codeがコンテキストを読み込む方法
- [エージェントコンテキスト構造](technical-architecture.md#agent-context-structure) - ドメイン専門家コンテキスト
- [コマンドコンテキスト構造](technical-architecture.md#command-context-structure) - ワークフローパターン
- [Claude Codeがコンテキストを読み込む方法](technical-architecture.md#how-claude-code-reads-context) - 処理シーケンス
- [フレームワークの拡張](technical-architecture.md#extending-the-framework) - 新しいコンポーネントの追加

### 🧪 [検証＆トラブルシューティングガイド](testing-debugging.md)
**目的**: インストールの検証とコンテキストファイルの問題のトラブルシューティング
**対象読者**: ユーザーとメンテナー
**長さ**: ファイル検証とClaude Code統合に焦点を当てた約500行

**主要セクション**:
- [インストール検証](testing-debugging.md#installation-verification) - コンテキストファイルのインストールを確認
- [コンテキストファイル検証](testing-debugging.md#context-file-verification) - ファイル構造の検証
- [MCPサーバー検証](testing-debugging.md#mcp-server-verification) - 外部ツール設定
- [一般的な問題](testing-debugging.md#common-issues) - アクティベーション問題のトラブルシューティング
- [トラブルシューティングコマンド](testing-debugging.md#troubleshooting-commands) - 診断手順

---

## トピックベースのインデックス

### 🚀 はじめに

**完全な初心者**:
1. [貢献ガイド → セットアップ](contributing-code.md#development-setup) - 環境設定
2. [アーキテクチャガイド → 概要](technical-architecture.md#overview) - コンテキストファイルの理解
3. [検証ガイド → インストールチェック](testing-debugging.md#installation-verification) - 基本的な検証

**環境設定**:
- [開発セットアップ](contributing-code.md#development-setup) - 前提条件と設定
- [インストール検証](testing-debugging.md#installation-verification) - ファイルインストールの確認

### 🏗️ アーキテクチャと設計

**コンテキストファイルアーキテクチャ**:
- [コンテキストファイルアーキテクチャ](technical-architecture.md#context-file-architecture) - 完全なシステム設計
- [インポートシステム](technical-architecture.md#the-import-system) - Claude Codeがコンテキストを読み込む方法
- [エージェントコンテキスト構造](technical-architecture.md#agent-context-structure) - ドメイン専門家パターン
- [コマンドコンテキスト構造](technical-architecture.md#command-context-structure) - ワークフロー定義

**コンポーネント開発**:
- [コンポーネントへの貢献](contributing-code.md#contributing-to-components) - エージェント、コマンド、モード開発
- [新しいエージェントの追加](contributing-code.md#adding-new-agents) - ドメイン専門家の作成
- [新しいコマンドの追加](contributing-code.md#adding-new-commands) - ワークフローパターンの開発
- [フレームワークの拡張](technical-architecture.md#extending-the-framework) - フレームワークの拡張

### 🧪 検証と品質

**ファイル検証**:
- [コンテキストファイル検証](testing-debugging.md#context-file-verification) - ファイル構造の検証
- [ファイル検証](contributing-code.md#file-validation) - コンテキストファイルの検証方法

**トラブルシューティング**:
- [一般的な問題](testing-debugging.md#common-issues) - アクティベーションと設定の問題
- [トラブルシューティングコマンド](testing-debugging.md#troubleshooting-commands) - 診断手順

### 🔧 開発ワークフロー

**コンテキストファイル開発**:
- [開発ワークフロー](contributing-code.md#development-workflow) - Gitワークフロー
- [コンテキストファイルガイドライン](contributing-code.md#context-file-guidelines) - 標準と実践
- [プルリクエストプロセス](contributing-code.md#pull-request-template) - 提出プロセス

**コンポーネント開発**:
- [エージェント開発](contributing-code.md#adding-new-agents) - ドメイン専門家の作成
- [コマンド開発](contributing-code.md#adding-new-commands) - ワークフローパターンの作成
- [モード開発](contributing-code.md#adding-new-modes) - 振る舞い変更パターン

### 🛠️ MCP統合

**MCP設定**:
- [MCPサーバー設定](technical-architecture.md#mcp-server-configuration) - 外部ツール設定
- [MCPサーバー検証](testing-debugging.md#mcp-server-verification) - 設定検証

### 🚨 サポートとトラブルシューティング

**一般的な問題**:
- [コマンドが機能しない](testing-debugging.md#issue-commands-not-working) - コンテキストトリガーの問題
- [エージェントがアクティブにならない](testing-debugging.md#issue-agents-not-activating) - アクティベーションの問題
- [コンテキストが読み込まれない](testing-debugging.md#issue-context-not-loading) - 読み込みの問題

**サポートリソース**:
- [ヘルプ](contributing-code.md#getting-help) - サポートチャネル
- [問題報告](contributing-code.md#issue-reporting) - バグ報告と機能

---

## スキルレベル別のパス

### 🟢 初心者パス (SuperClaudeの理解)

**1週目: 基礎**
1. [アーキテクチャ概要](technical-architecture.md#overview) - SuperClaudeとは何か
2. [インストール検証](testing-debugging.md#installation-verification) - セットアップの確認
3. [コンテキストファイルアーキテクチャ](technical-architecture.md#context-file-architecture) - ディレクトリ構造

**2週目: 基本的な使用法**
1. [Claude Codeがコンテキストを読み込む方法](technical-architecture.md#how-claude-code-reads-context) - 処理シーケンス
2. [一般的な問題](testing-debugging.md#common-issues) - トラブルシューティングの基本
3. [コンテキストファイルガイドライン](contributing-code.md#context-file-guidelines) - ファイル標準

### 🟡 中級者パス (コンテキストファイルの貢献)

**1ヶ月目: コンテキスト開発**
1. [開発セットアップ](contributing-code.md#development-setup) - 環境準備
2. [エージェントコンテキスト構造](technical-architecture.md#agent-context-structure) - ドメイン専門家
3. [コマンドコンテキスト構造](technical-architecture.md#command-context-structure) - ワークフローパターン

**2ヶ月目: コンポーネント作成**
1. [新しいエージェントの追加](contributing-code.md#adding-new-agents) - ドメイン専門家開発
2. [新しいコマンドの追加](contributing-code.md#adding-new-commands) - ワークフロー作成
3. [ファイル検証](contributing-code.md#file-validation) - コンテキスト検証

### 🔴 上級者パス (フレームワークの拡張)

**高度な理解**
1. [インポートシステム](technical-architecture.md#the-import-system) - コンテキスト読み込みの仕組み
2. [フレームワークの拡張](technical-architecture.md#extending-the-framework) - フレームワークの拡張
3. [MCPサーバー設定](technical-architecture.md#mcp-server-configuration) - 外部ツール統合

---

## 参考資料

### 📚 主要概念

**フレームワークの基礎**:
- コンテキスト指向設定フレームワーク
- エージェントドメイン専門家
- コマンドワークフローパターン
- モード振る舞い変更
- MCP統合パターン

### 🔗 相互参照

**開発 → アーキテクチャ**:
- [コンテキストファイルガイドライン](contributing-code.md#context-file-guidelines) → [コンテキストファイルアーキテクチャ](technical-architecture.md#context-file-architecture)
- [コンポーネントの追加](contributing-code.md#contributing-to-components) → [エージェント/コマンド構造](technical-architecture.md#agent-context-structure)

**開発 → 検証**:
- [開発ワークフロー](contributing-code.md#development-workflow) → [ファイル検証](testing-debugging.md#context-file-verification)
- [ファイル検証](contributing-code.md#file-validation) → [インストール検証](testing-debugging.md#installation-verification)

**アーキテクチャ → 検証**:
- [Claude Codeがコンテキストを読み込む方法](technical-architecture.md#how-claude-code-reads-context) → [トラブルシューティング](testing-debugging.md#common-issues)
- [MCP設定](technical-architecture.md#mcp-server-configuration) → [MCP検証](testing-debugging.md#mcp-server-verification)

---

## 品質基準

### ✅ ドキュメントの正確性
- **技術的な精度**: すべての例はSuperClaudeの実体（ソフトウェアではなくコンテキストファイル）を反映
- **コマンドの正確性**: 正しいPythonモジュール実行パスとClaude Codeコンテキストトリガー
- **フィクションの排除**: 存在しないテストフレームワークやパフォーマンスシステムへの言及をすべて削除

### ✅ コンテンツの焦点
- **コンテキストファイル**: ドキュメントは.md指示ファイルとClaude Codeの振る舞いに焦点を当てる
- **ファイル検証**: コンテキストファイルのインストールと構造を検証するための実践的なアプローチ
- **実際のワークフロー**: コンテキストファイル貢献のための実際の開発プロセス

### ✅ ユーザー体験
- **明確な進捗**: 理解から貢献までのスキルベースの学習パス
- **実践的な例**: 実用的なコンテキストファイルの例とClaude Code統合
- **サポート統合**: 実際の問題に対するヘルプリソースへの明確なガイダンス

---

## 利用ガイドライン

### 貢献者向け
1. **開始点**: [開発セットアップ](contributing-code.md#development-setup)
2. **コンテキスト開発**: [コンテキストファイルガイドライン](contributing-code.md#context-file-guidelines)に従う
3. **検証**: [ファイル検証](contributing-code.md#file-validation)を使用
4. **サポート**: [ヘルプ](contributing-code.md#getting-help)を参照

### アーキテクト向け
1. **システム理解**: [コンテキストファイルアーキテクチャ](technical-architecture.md#context-file-architecture)
2. **コンポーネントパターン**: [エージェントとコマンドの構造](technical-architecture.md#agent-context-structure)
3. **拡張**: [フレームワークの拡張](technical-architecture.md#extending-the-framework)
4. **統合**: [MCP設定](technical-architecture.md#mcp-server-configuration)

### 検証担当者向け
1. **インストールチェック**: [インストール検証](testing-debugging.md#installation-verification)
2. **ファイル検証**: [コンテキストファイル検証](testing-debugging.md#context-file-verification)
3. **トラブルシューティング**: [一般的な問題](testing-debugging.md#common-issues)
4. **診断**: [トラブルシューティングコマンド](testing-debugging.md#troubleshooting-commands)

この包括的なインデックスは、実践的なコンテキストファイル開発とClaude Code統合に焦点を当て、コンテキスト指向設定フレームワークとしてのSuperClaudeの実体を反映しています。
