# SuperClaude 高度なパターン

**高度なコンテキスト利用パターン**: 複雑なプロジェクトに取り組む経験豊富なSuperClaudeユーザー向けの、コマンド、エージェント、フラグの洗練された組み合わせ。

**注意**: SuperClaudeはClaude Codeにコンテキストを提供します。ここでのすべてのパターンは、コードの実行やプロセスの調整ではなく、コンテキストを通じてClaudeの振る舞いをガイドすることに関するものです。

## 目次

### コンテキスト組み合わせパターン
- [マルチエージェントコンテキストパターン](#マルチエージェントコンテキストパターン) - 複数の専門家コンテキストの組み合わせ
- [コマンドシーケンシングパターン](#コマンドシーケンシングパターン) - 効果的なコマンドの組み合わせ
- [フラグ組み合わせ戦略](#フラグ組み合わせ戦略) - 高度なフラグの使用法

### ワークフローパターン
- [複雑なプロジェクトパターン](#複雑なプロジェクトパターン) - 大規模プロジェクトのアプローチ
- [移行パターン](#移行パターン) - レガシーシステムの近代化
- [レビューと監査パターン](#レビューと監査パターン) - 包括的な分析

## マルチエージェントコンテキストパターン

### 専門家コンテキストの組み合わせ

**セキュリティ + バックエンド パターン:**
```bash
# セキュリティに焦点を当てたバックエンド開発
@agent-security "認証要件を定義する"
@agent-backend-architect "セキュリティ要件を満たすAPIを設計する"
/sc:implement "安全なAPIエンドポイント"

# 何が起こるか:
# 1. 最初にセキュリティコンテキストが読み込まれる
# 2. バックエンドコンテキストが追加される
# 3. 両方のコンテキストに導かれて実装が行われる
# 注意: コンテキストは実行時ではなく、Claudeの理解の中で組み合わさる
```

**フロントエンド + UX + アクセシビリティ パターン:**
```bash
# 包括的なフロントエンド開発
@agent-frontend-architect "コンポーネントアーキテクチャを設計する"
/sc:implement "アクセシブルなReactコンポーネント" --magic
@agent-quality-engineer "アクセシビリティ準拠を確認する"

# コンテキストの階層化:
# - フロントエンドのパターンが構造をガイドする
# - Magic MCPがUIコンポーネントを提供する可能性がある (設定されている場合)
# - 品質のコンテキストが標準を保証する
```

### 手動 対 自動のエージェント選択

**明示的な制御パターン:**
```bash
# どのコンテキストを読み込むかを手動で制御する
@agent-python-expert "データパイプラインを実装する"
# Pythonコンテキストのみ、自動起動なし

# 自動選択の場合
/sc:implement "Pythonデータパイプライン"
# キーワードに基づいて複数のエージェントが起動する可能性がある
```

**自動選択の上書き:**
```bash
# 不要なエージェントの起動を防ぐ
/sc:implement "シンプルなユーティリティ" --no-mcp
@agent-backend-architect "シンプルに保つ"
# コンテキストを指定されたエージェントのみに限定する
```

## コマンドシーケンシングパターン

### 段階的洗練パターン

```bash
# 大まかにはじめて、徐々に焦点を絞る
/sc:analyze project/
# 全体的な分析

/sc:analyze project/core/ --focus architecture
# 構造に焦点を当てる

/sc:analyze project/core/auth/ --focus security --think-hard
# 詳細なセキュリティ分析

# 各コマンドは会話内の前のコンテキストに基づいて構築される
```

### 発見から実装へのパターン

```bash
# 完全な機能開発フロー
/sc:brainstorm "機能のアイデア"
# 要件を探る

/sc:design "機能のアーキテクチャ"
# 構造を作成する

@agent-backend-architect "設計をレビューする"
# 専門家によるレビュー

/sc:implement "設計に基づいた機能"
# 設計に従って実装する

/sc:test --validate
# 検証アプローチ
```

### 反復的改善パターン

```bash
# 複数の改善パス
/sc:analyze code/ --focus quality
# 問題を特定する

/sc:improve code/ --fix
# 最初の改善パス

@agent-refactoring-expert "さらなる改善を提案する"
# 専門家による提案

/sc:improve code/ --fix --focus maintainability
# 洗練された改善
```

## フラグ組み合わせ戦略

### 分析深度の制御

```bash
# 簡単な概要
/sc:analyze . --overview --uc
# 高速で圧縮された出力

# 標準的な分析
/sc:analyze . --think
# 構造化された思考

# 詳細な分析
/sc:analyze . --think-hard --verbose
# 包括的な分析

# 最大深度 (控えめに使用)
/sc:analyze . --ultrathink
# 徹底的な分析
```

### MCPサーバーの選択

```bash
# MCPの選択的使用
/sc:implement "Reactコンポーネント" --magic --c7
# MagicとContext7 MCPのみ

# すべてのMCPを無効化
/sc:implement "シンプルな関数" --no-mcp
# 純粋なClaudeコンテキストのみ

# 利用可能なすべてのMCP
/sc:analyze complex-system/ --all-mcp
# 最大限のツール可用性 (設定されている場合)
```

## 複雑なプロジェクトパターン

### 大規模なコードベースの分析

```bash
# 大規模プロジェクトの体系的な探索
# ステップ1: 構造の理解
/sc:load project/
/sc:analyze . --overview --focus architecture

# ステップ2: 問題領域の特定
@agent-quality-engineer "リスクの高いモジュールを特定する"

# ステップ3: 特定領域の詳細な調査
/sc:analyze high-risk-module/ --think-hard --focus quality

# ステップ4: 実装計画
/sc:workflow "分析に基づく改善計画"
```

### マルチモジュール開発

```bash
# 相互接続されたモジュールの開発
# フロントエンドモジュール
/sc:implement "ユーザーインターフェースモジュール"
@agent-frontend-architect "一貫性を確保する"

# バックエンドモジュール
/sc:implement "APIモジュール"
@agent-backend-architect "互換性を確保する"

# 統合レイヤー
/sc:implement "フロントエンドとバックエンドの統合"
# 両方の前の実装からのコンテキストがこれをガイドする
```

### クロス技術プロジェクト

```bash
# 複数の技術を持つプロジェクト
# Pythonバックエンド
@agent-python-expert "FastAPIバックエンドを実装する"

# Reactフロントエンド
@agent-frontend-architect "Reactフロントエンドを実装する"

# DevOps設定
@agent-devops-architect "デプロイメント設定を作成する"

# 統合ドキュメント
/sc:document --type integration
```

## 移行パターン

### レガシーシステムの分析

```bash
# レガシーシステムの理解
/sc:load legacy-system/
/sc:analyze . --focus architecture --verbose

@agent-refactoring-expert "近代化の機会を特定する"
@agent-system-architect "移行戦略を提案する"

/sc:workflow "移行計画を作成する"
```

### 段階的移行

```bash
# ステップバイステップの移行アプローチ
# フェーズ1: 分析
/sc:analyze legacy-module/ --comprehensive

# フェーズ2: 新しいアーキテクチャの設計
@agent-system-architect "近代的な代替案を設計する"

# フェーズ3: 実装
/sc:implement "互換性レイヤーを持つ近代的なモジュール"

# フェーズ4: 検証
/sc:test --focus compatibility
```

## レビューと監査パターン

### セキュリティ監査パターン

```bash
# 包括的なセキュリティレビュー
/sc:analyze . --focus security --think-hard
@agent-security "認証と認可をレビューする"
@agent-security "OWASPの脆弱性をチェックする"
/sc:document --type security-audit
```

### コード品質レビュー

```bash
# 多角的な品質レビュー
/sc:analyze src/ --focus quality
@agent-quality-engineer "テストカバレッジをレビューする"
@agent-refactoring-expert "コードの匂いを特定する"
/sc:improve --fix --preview
```

### アーキテクチャレビュー

```bash
# システムアーキテクチャの評価
@agent-system-architect "現在のアーキテクチャをレビューする"
/sc:analyze . --focus architecture --think-hard
@agent-performance-engineer "ボトルネックを特定する"
/sc:design "最適化の推奨事項"
```

## 重要な明確化

### これらのパターンが実際に何をするか

- ✅ **Claudeの思考をガイドする**: 構造化されたアプローチを提供する
- ✅ **コンテキストを組み合わせる**: 複数の専門知識領域を重ね合わせる
- ✅ **出力品質を向上させる**: より良いコンテキストを通じてより良いコードを生成する
- ✅ **ワークフローを構造化する**: 複雑なタスクを整理する

### これらのパターンがしないこと

- ❌ **並列実行**: すべては逐次的なコンテキスト読み込み
- ❌ **プロセス調整**: 実際のプロセス調整はなし
- ❌ **パフォーマンス最適化**: コードは実行されないため、パフォーマンスへの影響はなし
- ❌ **セッション間の永続化**: 各会話は独立している

## 高度な使用のためのベストプラクティス

### コンテキスト管理

1. **意図的に階層化する**: 論理的な順序でコンテキストを追加する
2. **過負荷を避ける**: 多すぎるエージェントは焦点を薄める可能性がある
3. **手動制御を使用する**: 必要に応じて自動起動を上書きする
4. **会話の流れを維持する**: 関連作業を同じ会話に保つ

### コマンドの効率

1. **論理的に進める**: 大まか → 具体的に → 実装
2. **コンテキストを再利用する**: 後のコマンドは前のコンテキストから利益を得る
3. **決定を文書化する**: 重要な要約には`/sc:save`を使用する
4. **適切にスコープを設定する**: 管理可能なチャンクに焦点を当てる

### フラグの使用

1. **タスクの複雑さに合わせる**: 簡単なタスクに`--ultrathink`は不要
2. **出力を制御する**: 簡潔な結果には`--uc`を使用する
3. **MCPを管理する**: 必要なサーバーのみをアクティブにする
4. **競合を避ける**: 矛盾するフラグを使用しない

## まとめ

SuperClaudeの高度なパターンは、洗練されたコンテキスト管理とコマンドシーケンシングに関するものです。これらは、より豊かで構造化されたコンテキストを提供することで、Claude Codeがより良い出力を生成するのを助けます。注意: すべての「調整」と「最適化」は、実際の実行や並列処理ではなく、Claudeがコンテキストをどのように解釈するかによって起こります。
