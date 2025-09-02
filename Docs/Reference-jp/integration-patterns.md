# SuperClaude 統合パターンコレクション

**ステータス**: ✅ **ステータス: 最新** - フレームワーク統合とツール連携のためのコンテキストパターン。

**コンテキスト統合ガイド**: SuperClaudeコマンドを異なるフレームワークやツールで効果的に使用するためのパターン。注意: SuperClaudeはClaude Codeにコンテキストを提供します - 実際の作業はすべてClaudeが行います。

## 概要と使用ガイド

**目的**: さまざまな開発フレームワークやツールでSuperClaudeコンテキストを効果的に使用するためのパターン。

**これは何か**: 特定の技術に適したコマンドの組み合わせとフラグのパターン
**これは何かではない**: パフォーマンス最適化や並列実行（コードは実行されません）

**主要原則**: SuperClaudeはClaude Codeに何をすべきか、そしてそれについてどう考えるべきかを伝えます。実際の作業はClaude Codeが行います。

## フレームワークコンテキストパターン

### React開発パターン

```bash
# 適切なコンテキストでのReact開発
/sc:implement "TypeScriptを使用したReact 18アプリケーション" --c7
# Context7 MCPが利用可能であれば、Reactのドキュメントを提供する可能性があります
# Magic MCPが設定されていれば、UIコンポーネントの作成を支援できます

# 実際に何が起こるか:
# 1. Claudeは実装パターンのためにimplement.mdを読み込む
# 2. --c7フラグはドキュメントのためにContext7 MCPを使用することを提案する
# 3. Claudeはこれらのコンテキストに基づいてReactコードを生成する

# コンポーネント開発パターン
@agent-frontend-architect "コンポーネントアーキテクチャを設計する"
/sc:implement "再利用可能なコンポーネントライブラリ"

# Reactのテストパターン
/sc:test --focus react
# ClaudeはReact Testing Libraryのパターンを提案します
```

### Node.jsバックエンドパターン

```bash
# Node.jsバックエンド開発パターン
/sc:implement "TypeScriptを使用したExpress.js API" --c7
# ClaudeはNode.jsのパターンに従ってExpress APIを作成します

# これが意味すること:
# - Claudeはバックエンドパターンに関するコンテキストを読み込む
# - 適切なミドルウェアと構造を提案する
# - コードの実行や最適化は行わない

# データベース統合パターン
/sc:implement "Prismaを使用したデータベースモデル"
@agent-backend-architect "データベーススキーマをレビューする"

# APIテストパターン
/sc:test --focus api
# ClaudeはAPIテストのアプローチを提案します
```

### Python開発パターン

```bash
# Python Web開発
/sc:implement "FastAPIアプリケーション" --c7
@agent-python-expert "実装をレビューする"

# 何が起こるか:
# - ClaudeはPython固有のコンテキストを使用する
# - コンテキストからFastAPIのパターンに従う
# - コードを生成する（実行はしない）

# データサイエンスコンテキスト
/sc:implement "データ分析パイプライン"
@agent-python-expert "pandasの操作を最適化する"
# Claudeは最適化の提案を提供します（実際の最適化は行いません）

# テストパターン
/sc:test --focus python
# Claudeはpytestのパターンを提案します
```

### フルスタック開発パターン

```bash
# フルスタックアプリケーションパターン
/sc:brainstorm "フルスタックアプリケーションアーキテクチャ"
@agent-system-architect "システムコンポーネントを設計する"

# フロントエンド実装
/sc:implement "TypeScriptを使用したReactフロントエンド"
@agent-frontend-architect "コンポーネント構造をレビューする"

# バックエンド実装
/sc:implement "認証付きのNode.js API"
@agent-backend-architect "API設計をレビューする"

# 統合
/sc:implement "フロントエンドとバックエンドAPIを接続する"
```

## ツール連携パターン

### MCPサーバーの効果的な使用

```bash
# ドキュメントのためのContext7
/sc:explain "Reactフック" --c7
# Context7が設定されていれば、Reactのドキュメントを取得する可能性があります

# 複雑な推論のためのSequential
/sc:troubleshoot "複雑なバグ" --seq
# Sequential MCPは構造化された問題解決を支援します

# UIコンポーネントのためのMagic
/sc:implement "UIコンポーネント" --magic
# Magic MCPは最新のUIパターンの生成を支援できます

# 簡単なタスクにはMCPなし
/sc:implement "ユーティリティ関数" --no-mcp
# Claudeの組み込み知識のみを使用します
```

### エージェントとコマンドの組み合わせ

```bash
# セキュリティに焦点を当てた開発
@agent-security "認証要件をレビューする"
/sc:implement "安全な認証システム"
/sc:analyze --focus security

# 品質に焦点を当てたワークフロー
/sc:implement "新機能"
@agent-quality-engineer "コード品質をレビューする"
/sc:test --focus quality

# アーキテクチャに焦点を当てたアプローチ
@agent-system-architect "マイクロサービスを設計する"
/sc:design "サービス境界"
/sc:implement "サービス間通信"
```

## 一般的な統合パターン

### API開発パターン

```bash
# ステップ1: 設計
/sc:design "REST API構造"

# ステップ2: 実装
/sc:implement "検証付きのAPIエンドポイント"

# ステップ3: ドキュメンテーション
/sc:document --type api

# ステップ4: テスト
/sc:test --focus api
```

### データベース統合パターン

```bash
# スキーマ設計
@agent-backend-architect "データベーススキーマを設計する"

# モデル実装
/sc:implement "データベースモデル"

# マイグレーション作成
/sc:implement "データベースマイグレーション"

# クエリ最適化の提案
@agent-backend-architect "クエリ最適化を提案する"
# 注意: Claudeは最適化を提案するだけで、実際には最適化しません
```

### テスト戦略パターン

```bash
# テスト計画
/sc:design "テスト戦略"

# ユニットテスト
/sc:test --type unit

# 統合テスト
/sc:test --type integration

# E2Eテストの提案
/sc:test --type e2e
# Claudeはテストコードを提供しますが、実行はしません
```

## 特定技術のパターン

### React + TypeScript パターン

```bash
# プロジェクト設定ガイダンス
/sc:implement "React TypeScriptプロジェクト構造"

# コンポーネント開発
/sc:implement "プロップス検証付きのTypeScript Reactコンポーネント"

# 状態管理
@agent-frontend-architect "状態管理アプローチを推奨する"
/sc:implement "Zustand/Reduxによる状態管理"

# テスト
/sc:test --focus react --type unit
```

### Python FastAPI パターン

```bash
# API構造
/sc:implement "FastAPIプロジェクト構造"

# エンドポイント開発
@agent-python-expert "非同期エンドポイントを実装する"

# データベース統合
/sc:implement "Alembic付きのSQLAlchemyモデル"

# テスト
/sc:test --focus python --type integration
```

### Node.js マイクロサービス パターン

```bash
# アーキテクチャ設計
@agent-system-architect "マイクロサービスアーキテクチャを設計する"

# サービス実装
/sc:implement "Expressを使用したユーザーサービス"
/sc:implement "JWTを使用した認証サービス"

# サービス間通信
/sc:implement "サービス間通信パターン"

# テストアプローチ
/sc:test --focus microservices
```

## トラブルシューティングパターン

### デバッグワークフロー

```bash
# 問題分析
/sc:troubleshoot "問題を説明する"

# 根本原因調査
@agent-root-cause-analyst "症状を分析する"

# 解決策の実装
/sc:implement "分析に基づく修正"

# 検証
/sc:test --validate
```

### コードレビューパターン

```bash
# コード分析
/sc:analyze code/ --focus quality

# セキュリティレビュー
@agent-security "脆弱性をレビューする"

# パフォーマンスレビュー
@agent-performance-engineer "改善を提案する"
# 注意: 提案のみで、実際のパフォーマンス測定はありません

# 改善の実装
/sc:improve code/ --fix
```

## 重要な明確化

### これらのパターンが「行う」こと

- ✅ 開発タスクへの構造化されたアプローチを提供する
- ✅ コマンドとエージェントを効果的に組み合わせる
- ✅ 適切なツールとフレームワークを提案する
- ✅ より良いコードを生成するようにClaudeをガイドする

### これらのパターンが「行わない」こと

- ❌ コードの実行やパフォーマンスの測定
- ❌ テストの実行やアプリケーションのデプロイ
- ❌ 実際の実行速度の最適化
- ❌ 実際の監視やメトリクスの提供
- ❌ 並列プロセスの調整（すべては逐次的なテキスト）

## ベストプラクティス

### 効果的なパターンの使用法

1. **コンテキストから始める**: `/sc:load`を使用してプロジェクトの理解を確立する
2. **専門知識を重ねる**: 一般的なコマンドと特定のージェントを組み合わせる
3. **適切に焦点を合わせる**: 対象を絞った結果を得るために`--focus`フラグを使用する
4. **スコープを管理する**: コードベース全体ではなく、特定のモジュールで作業する
5. **決定を文書化する**: 要約を作成するために`/sc:save`を使用する

### パターンの選択

- **簡単なタスク**: MCPなしの基本コマンドを使用する
- **複雑なタスク**: 適切なエージェントとMCPサーバーを追加する
- **セキュリティが重要な場合**: 常に`@agent-security`を含める
- **UI開発**: 設定されていれば`--magic`フラグを検討する
- **ドキュメントが必要な場合**: フレームワークのドキュメントには`--c7`を使用する

## まとめ

これらの統合パターンは、さまざまな開発シナリオでSuperClaudeのコマンド、エージェント、フラグを効果的に組み合わせる方法を示しています。すべてのパターンはClaude Codeにより良いコンテキストを提供することに関するものであることを忘れないでください - 実際のコード生成は、実行ではなく、これらのコンテキストに基づいてClaudeが行います。
