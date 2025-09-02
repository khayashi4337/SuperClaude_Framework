# SuperClaude 基本例集

**ステータス**: ✅ **ステータス: 最新** - 不可欠なコマンド、単一エージェントのワークフロー、および一般的な開発タスク。

**クイックリファレンスガイド**: 初心者向けのコピー＆ペースト可能な例。不可欠なSuperClaudeの使用パターンと基本的な開発ワークフローに焦点を当てています。

> **📝 コンテキストノート**: これらの例は、`/sc:`コマンドと`@agent-`呼び出しを示しています。これらはClaude Codeに特定のコンテキストファイルを読み込ませ、そこで定義された振る舞いを採用させるトリガーとなります。洗練さは、実行可能なソフトウェアからではなく、振る舞いの指示から生まれます。

## 概要と使用ガイド

**目的**: 日常の開発タスクのための不可欠なSuperClaudeコマンドとパターン。最初のSuperClaude体験はここから始めてください。

**対象読者**: 新規ユーザー、SuperClaudeの基礎を学ぶ開発者、即時のタスク適用

**使用パターン**: コピー → 適応 → 実行 → 結果から学ぶ

**主要な特徴**:
- 例はSuperClaudeのコア機能を示す
- 即時適用のための明確なパターン
- 明確な学習のための単一焦点の例
- 基本的な範囲内での段階的な複雑さ

## 不可欠なワンライナーコマンド

### コア開発コマンド

#### コマンド: /sc:brainstorm
**目的**: 対話的なプロジェクト発見と要件収集
**構文**: `/sc:brainstorm "プロジェクトの説明"`
**例**:
```bash
/sc:brainstorm "フィットネス追跡用のモバイルアプリ"
# 期待される結果: ソクラテス式対話、要件の引き出し、実現可能性分析
```
**振る舞い**: 対話的な発見対話と要件分析をトリガーします

#### コマンド: /sc:analyze
**目的**: 既存のコードベースを問題点と改善のために分析する
**構文**: `/sc:analyze [対象] --focus [ドメイン]`
**例**:
```bash
/sc:analyze src/ --focus security
# 期待される結果: 包括的なセキュリティ監査、脆弱性レポート、改善提案
```
**振る舞い**: 包括的なセキュリティ分析と改善推奨を提供します

#### コマンド: /sc:implement
**目的**: ベストプラクティスを用いて完全な機能を実装する
**構文**: `/sc:implement "要件を含む機能の説明"`
**例**:
```bash
/sc:implement "JWTとレート制限付きのユーザー認証"
# 期待される結果: 完全な認証実装、セキュリティ検証、テストを含む
```
**振る舞い**: セキュリティと品質基準に従った完全な実装を提供します

#### コマンド: /sc:troubleshoot
**目的**: 問題を体系的にトラブルシューティングし、修正する
**構文**: `/sc:troubleshoot "問題の説明"`
**例**:
```bash
/sc:troubleshoot "ユーザーログイン時にAPIが500エラーを返す"
# 期待される結果: ステップバイステップの診断、根本原因の特定、解決策のランキング
```
**検証**: root-cause-analyst + Sequential推論 + 体系的なデバッグをアクティブにします

#### コマンド: /sc:test
**目的**: 既存のコードに対して包括的なテストを生成する
**構文**: `/sc:test [対象] --focus [ドメイン]`
**例**:
```bash
/sc:test --focus quality
# 期待される結果: テストスイート、品質メトリクス、カバレッジレポート
```
**検証**: quality-engineer + テスト自動化をアクティブにします

### クイック分析コマンド

#### コマンド: /sc:analyze (品質フォーカス)
**目的**: プロジェクト構造と品質の概要
**構文**: `/sc:analyze [対象] --focus quality`
**例**:
```bash
/sc:analyze . --focus quality
```
**検証**:

#### コマンド: /sc:analyze (セキュリティフォーカス)
**目的**: セキュリティに焦点を当てたコードレビュー
**構文**: `/sc:analyze [対象] --focus security [--think]`
**例**:
```bash
/sc:analyze src/ --focus security --think
```
**検証**:

#### コマンド: /sc:analyze (パフォーマンスフォーカス)
**目的**: パフォーマンスのボトルネック特定
**構文**: `/sc:analyze [対象] --focus performance`
**例**:
```bash
/sc:analyze api/ --focus performance
```
**検証**:

#### コマンド: /sc:analyze (アーキテクチャフォーカス)
**目的**: リファクタリングのためのアーキテクチャ評価
**構文**: `/sc:analyze [対象] --focus architecture [--serena]`
**例**:
```bash
/sc:analyze . --focus architecture --serena
```
**検証**:

## 手動エージェント呼び出しの例

### 直接的な専門家の起動

#### パターン: @agent-[専門家]
**目的**: 自動起動の代わりに特定のドメイン専門家を手動で呼び出す
**構文**: `@agent-[専門家] "タスクや質問"`

#### Pythonエキスパート
```bash
@agent-python-expert "このデータ処理パイプラインをパフォーマンスのために最適化して"
# 期待される結果: Python固有の最適化、非同期パターン、メモリ管理
```

#### セキュリティエンジニア
```bash
@agent-security "この認証システムを脆弱性のためにレビューして"
# 期待される結果: OWASPコンプライアンスチェック、脆弱性評価、セキュアコーディングの推奨
```

#### フロントエンドアーキテクト
```bash
@agent-frontend-architect "レスポンシブなコンポーネントアーキテクチャを設計して"
# 期待される結果: コンポーネントパターン、状態管理、アクセシビリティへの配慮
```

#### 品質エンジニア
```bash
@agent-quality-engineer "支払いモジュールのための包括的なテストカバレッジを作成して"
# 期待される結果: テスト戦略、単体/統合/E2Eテスト、エッジケース
```

### 自動と手動パターンの組み合わせ

#### パターン: コマンド + 手動上書き
```bash
# ステップ1: 自動起動付きのコマンドを使用
/sc:implement "ユーザープロファイル管理システム"
# 自動起動: backend-architect, 場合によってはfrontend

# ステップ2: 特定の専門家レビューを追加
@agent-security "データプライバシーコンプライアンスのためにプロファイルシステムをレビューして"
# 対象を絞ったレビューのための手動起動

# ステップ3: パフォーマンス最適化
@agent-performance-engineer "プロファイル取得のためのデータベースクエリを最適化して"
# 特定の最適化のための手動起動
```

#### パターン: 逐次的な専門家チェーン
```bash
# 設計フェーズ
@agent-system-architect "eコマースのためのマイクロサービスアーキテクチャを設計して"

# セキュリティレビュー
@agent-security "セキュリティ境界のためにアーキテクチャをレビューして"

# 実装ガイダンス
@agent-backend-architect "サービス通信パターンを実装して"

# DevOpsセットアップ
@agent-devops-architect "マイクロサービスのためのCI/CDを設定して"
```

## 基本的な使用パターン

### 発見 → 実装 パターン
```bash
# ステップ1: 要件を探り、理解する
/sc:brainstorm "プロジェクト管理用のWebダッシュボード"
# 期待される結果: 要件発見、機能の優先順位付け、技術的スコープ

# ステップ2: 技術的アプローチを分析する
/sc:analyze "ダッシュボードアーキテクチャパターン" --focus architecture --c7
# 期待される結果: アーキテクチャパターン、技術推奨、実装戦略

# ステップ3: コア機能を実装する
/sc:implement "タスク管理とチームコラボレーションを備えたReactダッシュボード"
# 期待される結果: 最新のReactパターンによる完全なダッシュボード実装
```

### 開発 → 品質 パターン
```bash
# ステップ1: 機能を構築する
/sc:implement "メール検証付きのユーザー登録"
# 期待される結果: メール統合を備えた登録システム

# ステップ2: 徹底的にテストする
/sc:test --focus quality
# 期待される結果: 包括的なテストカバレッジと検証

# ステップ3: レビューと改善
/sc:analyze . --focus quality && /sc:implement "品質改善"
# 期待される結果: 品質評価と対象を絞った改善
```

### 問題 → 解決 パターン
```bash
# ステップ1: 問題を理解する
/sc:troubleshoot "ユーザーダッシュボードでの遅いデータベースクエリ"
# 期待される結果: 体系的な問題診断と根本原因分析

# ステップ2: 影響を受けるコンポーネントを分析する
/sc:analyze db/ --focus performance
# 期待される結果: データベースパフォーマンス分析と最適化の機会

# ステップ3: 解決策を実装する
/sc:implement "データベースクエリの最適化とキャッシング"
# 期待される結果: 測定可能な影響を持つパフォーマンス改善
```

## はじめての例

### 初めてのプロジェクト分析
```bash
# 完全なプロジェクト理解ワークフロー
/sc:load . && /sc:analyze --focus quality

# 期待される結果:
# - プロジェクト構造分析とドキュメント
# - 全ファイルにわたるコード品質評価
# - コンポーネント関係を含むアーキテクチャ概要
# - セキュリティ監査とパフォーマンス推奨

# 起動するエージェント: Serena (プロジェクト読み込み) + analyzer + security-engineer + performance-engineer
# 出力: 実用的な洞察を含む包括的なプロジェクトレポート


# 異なる焦点のためのバリエーション:
/sc:analyze src/ --focus quality          # コード品質のみ
/sc:analyze . --scope file               # 簡単なファイル分析
/sc:analyze backend/ --focus security    # バックエンドのセキュリティレビュー
```

### 対話的な要件発見
```bash
# 曖昧なアイデアを具体的な要件に変換する
/sc:brainstorm "リモートチーム向けの生産性アプリ"

# 期待される対話:
# - ユーザーのニーズとペインポイントに関するソクラテス式質問
# - 機能の優先順位付けとスコープ定義
# - 技術的な実現可能性評価
# - 構造化された要件ドキュメントの生成

# 起動するエージェント: Brainstormingモード + system-architect + requirements-analyst
# 出力: 明確な仕様を持つ製品要件ドキュメント (PRD)

# 進行のためのフォローアップコマンド:
/sc:analyze "チームコラボレーションアーキテクチャ" --focus architecture --c7
/sc:implement "ReactとWebSocketによるリアルタイムメッセージングシステム"
```

### 簡単な機能実装
```bash
# 完全な認証システム
/sc:implement "JWTトークンとパスワードハッシュによるユーザーログイン"

# 期待される実装:
# - bcryptによる安全なパスワードハッシュ
# - JWTトークンの生成と検証
# - 適切なエラーハンドリングを備えたログイン/ログアウトエンドポイント
# - 検証付きのフロントエンドログインフォーム

# 起動するエージェント: security-engineer + backend-architect + Context7
# 出力: 本番環境対応の認証システム


# 異なる認証ニーズのためのバリエーション:
/sc:implement "GoogleとGitHubによるOAuth統合"
/sc:implement "メール検証付きのパスワードリセットフロー"
/sc:implement "TOTPによる二要素認証"
```

## 一般的な開発タスク

### API開発の基本
```bash
# CRUD操作を備えたREST API
/sc:implement "検証付きのExpress.js REST API for blog posts"
# 期待される結果: 適切なHTTPメソッド、検証、エラーハンドリングを備えた完全なREST API


# APIドキュメント生成
/sc:analyze api/ --focus architecture --c7
# 期待される結果: 使用例を含む包括的なAPIドキュメント


# APIテスト設定
/sc:test --focus api --type integration
# 期待される結果: APIエンドポイントのための統合テストスイート

```

### フロントエンドコンポーネント開発
```bash
# 最新のパターンを持つReactコンポーネント
/sc:implement "フォーム検証と画像アップロードを備えたReactユーザープロファイルコンポーネント"
# 起動するエージェント: frontend-architect + Magic MCP + アクセシビリティパターン
# 期待される結果: フック、検証、アクセシビリティを備えた最新のReactコンポーネント


# コンポーネントテスト
/sc:test src/components/ --focus quality
# 期待される結果: React Testing Libraryによるコンポーネントテスト


# レスポンシブデザイン実装
/sc:implement "モバイルメニュー付きのレスポンシブナビゲーションコンポーネント"
# 期待される結果: アクセシビリティを備えたモバイルファーストのレスポンシブナビゲーション

```

### データベース統合
```bash
# ORMによるデータベース設定
/sc:implement "Prisma ORMとマイグレーションによるPostgreSQL統合"
# 期待される結果: データベーススキーマ、ORM設定、マイグレーションシステム


# データベースクエリ最適化
/sc:analyze db/ --focus performance
# 期待される結果: クエリパフォーマンス分析と最適化提案


# データ検証とセキュリティ
/sc:implement "入力検証とSQLインジェクション防止"
# 期待される結果: 包括的な入力検証とセキュリティ対策

```

## 基本的なトラブルシューティングの例

### 一般的なAPIの問題
```bash
# パフォーマンス問題
/sc:troubleshoot "API応答時間が200msから2秒に増加"
# 起動するエージェント: root-cause-analyst + performance-engineer + Sequential推論
# 期待される結果: 体系的な診断、根本原因の特定、解決策のランキング

# 認証エラー
/sc:troubleshoot "有効なユーザーに対してJWTトークン検証が失敗する"
# 期待される結果: トークン検証分析、セキュリティ評価、修正実装

# データベース接続問題
/sc:troubleshoot "負荷時にデータベース接続プールが枯渇する"
# 期待される結果: 接続分析、設定修正、スケーリング推奨
```

### フロントエンドのデバッグ
```bash
# Reactのレンダリング問題
/sc:troubleshoot "データが変更されてもReactコンポーネントが更新されない"
# 期待される結果: 状態管理分析、再レンダリング最適化、デバッグガイド

# パフォーマンス問題
/sc:troubleshoot "大きなコンポーネントツリーでReactアプリの読み込みが遅い"
# 期待される結果: パフォーマンス分析、最適化戦略、コード分割推奨

# ビルド失敗
/sc:troubleshoot "依存関係の競合でwebpackビルドが失敗する"
# 期待される結果: 依存関係分析、競合解決、ビルド最適化
```

### 開発環境の問題
```bash
# セットアップ問題
/sc:troubleshoot "npm install後にNode.jsアプリケーションが起動しない"
# 期待される結果: 環境分析、依存関係トラブルシューティング、設定修正

# テスト失敗
/sc:troubleshoot "テストはローカルで成功するがCIで失敗する"
# 期待される結果: 環境比較、CI設定分析、修正推奨

# デプロイ問題
/sc:troubleshoot "本番デプロイでアプリケーションがクラッシュする"
# 期待される結果: 本番環境分析、設定検証、デプロイ修正
```

## コピー＆ペースト クイックソリューション

### 即時のプロジェクト設定
```bash
# TypeScriptによる新しいReactプロジェクト
/sc:implement "ルーティング、状態管理、テスト設定を備えたReact TypeScriptプロジェクト"
@agent-frontend-architect "プロジェクト構造をレビューし、最適化して"

# 新しいNode.js APIサーバー
/sc:implement "JWT認証とPostgreSQL統合を備えたExpress.js REST API"
@agent-backend-architect "スケーラビリティとベストプラクティスを確保して"

# Python Web API
/sc:implement "非同期PostgreSQLと認証ミドルウェアを備えたFastAPIアプリケーション"
@agent-python-expert "非同期パターンと依存性注入を最適化して"

# Next.jsフルスタックアプリ
/sc:implement "App Router、TypeScript、Tailwind CSSを備えたNext.js 14アプリケーション"
@agent-system-architect "最適なデータ取得戦略を設計して"
```

### 簡単な品質改善
```bash
# コード品質向上
/sc:analyze . --focus quality && /sc:implement "コード品質改善"
@agent-quality-engineer "品質メトリクスダッシュボードを作成して"

# セキュリティ強化
/sc:analyze . --focus security && /sc:implement "セキュリティ改善"

# テストカバレッジ改善
/sc:test --focus quality && /sc:implement "追加のテストカバレッジ"
```

### 一般的な機能実装
```bash
# ユーザー認証システム
/sc:implement "登録、ログイン、パスワードリセットを備えた完全なユーザー認証"

# ファイルアップロード機能
/sc:implement "画像リサイズとクラウドストレージを備えた安全なファイルアップロード"

# リアルタイム機能
/sc:implement "WebSocketとメッセージ永続化を備えたリアルタイムチャット"

# 支払い処理
/sc:implement "サブスクリプション管理を備えたStripe支払い統合"

# メール機能
/sc:implement "テンプレートと配信追跡を備えたメールサービス"
```

## 基本的なフラグの例

### 分析深度の制御
```bash
# 簡単な分析
/sc:analyze src/ --scope file

# 標準的な分析
/sc:analyze . --think

# 詳細な分析
/sc:analyze . --think-hard --focus architecture

```

### フォーカスエリアの選択
```bash
# セキュリティに焦点を当てた分析
/sc:analyze . --focus security


# 特定の焦点を持つ実装
/sc:implement "API最適化" --focus architecture


# 品質に焦点を当てたテスト
/sc:test --focus quality

```

### ツール統合
```bash
# 公式パターンのためにContext7を使用
/sc:implement "Reactフックの実装" --c7


# プロジェクトメモリのためにSerenaを使用
/sc:analyze . --serena --focus architecture


# 効率的なトークン使用
/sc:analyze large-project/ --uc

```

## 学習進行ワークフロー

### 1週目: 基礎
```bash
# 1-2日目: 基本コマンド
/sc:analyze . --focus quality
/sc:implement "簡単な機能"
/sc:test --focus quality

# 3-4日目: トラブルシューティング
/sc:troubleshoot "特定の問題"
/sc:analyze problem-area/ --focus relevant-domain

# 5-7日目: 統合
/sc:brainstorm "プロジェクトのアイデア"
/sc:implement "コア機能"
/sc:test --focus quality
```

### 2週目: パターン
```bash
# ワークフローパターン
/sc:brainstorm → /sc:analyze → /sc:implement → /sc:test

# 問題解決パターン
/sc:troubleshoot → /sc:analyze → /sc:implement

# 品質パターン
/sc:analyze → /sc:implement → /sc:test → /sc:analyze
```

### 3-4週目: 統合
```bash
# マルチステッププロジェクト
/sc:brainstorm "より大きなプロジェクト"
/sc:implement "フェーズ1"
/sc:test --focus quality
/sc:implement "フェーズ2"
/sc:test --focus integration
```

## 次のステップ

### 中級者になる準備はできましたか？
- すべての基本コマンドに慣れている
- 簡単なワークフローを自力で完了できる
- エージェントの起動とツールの選択を理解している
- より複雑なプロジェクトに取り組む準備ができている

### 学習を続ける:
- **高度なワークフロー**: 複雑なオーケストレーションとマルチエージェント連携
- **統合パターン**: フレームワーク統合とクロスツール連携
- **ベストプラクティスガイド**: 最適化戦略とエキスパートテクニック

### 成功の指標:
- 一般的な開発問題を自力で解決できる
- 異なるフラグとフォーカスをいつ使用するか理解している
- 特定のプロジェクトニーズに合わせて例を適応できる
- より複雑なSuperClaudeの機能を探索する準備ができている

---

**覚えておいてください**: シンプルに始め、頻繁に練習し、徐々に複雑さを増してください。これらの基本例は、すべての高度なSuperClaude使用の基盤を形成します。
