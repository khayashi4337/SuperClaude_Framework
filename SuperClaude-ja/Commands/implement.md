---
name: implement
description: "インテリジェントなペルソナ起動とMCP統合による機能およびコードの実装"
category: workflow
complexity: standard
mcp-servers: [context7, sequential, magic, playwright]
personas: [architect, frontend, backend, security, qa-specialist]
---

# /sc:implement - 機能実装

> **コンテキストフレームワークノート**: この振る舞いの指示は、Claude Codeユーザーが`/sc:implement`パターンを入力したときに起動します。これは、Claudeが包括的な実装のために専門家のペルソナとMCPツールを調整するようにガイドします。

## トリガー
- コンポーネント、API、または完全な機能の開発リクエスト
- フレームワーク固有の要件を持つコード実装のニーズ
- 調整された専門知識を必要とするマルチドメイン開発
- テストと検証の統合を必要とする実装プロジェクト

## コンテキストトリガーパターン
```
/sc:implement [機能の説明] [--type component|api|service|feature] [--framework react|vue|express] [--safe] [--with-tests]
```
**使用法**: このパターンをClaude Codeの会話で入力すると、調整された専門知識と体系的な開発アプローチを持つ実装の振る舞いモードが起動します。

## 行動フロー
1. **分析**: 実装要件を調査し、技術コンテキストを検出します
2. **計画**: アプローチを選択し、ドメインの専門知識のために適切なペルソナを起動します
3. **生成**: フレームワーク固有のベストプラクティスを用いて実装コードを作成します
4. **検証**: 開発全体を通じてセキュリティと品質の検証を適用します
5. **統合**: ドキュメントを更新し、テストの推奨事項を提供します

主要な行動:
- コンテキストベースのペルソナ起動（architect, frontend, backend, security, qa）
- Context7およびMagic MCP統合によるフレームワーク固有の実装
- Sequential MCPによる体系的なマルチコンポーネント連携
- 検証のためのPlaywrightとの包括的なテスト統合

## MCP統合
- **Context7 MCP**: React, Vue, Angular, Expressのフレームワークパターンと公式ドキュメント
- **Magic MCP**: UIコンポーネント生成とデザインシステム統合のために自動起動
- **Sequential MCP**: 複雑な多段階分析と実装計画
- **Playwright MCP**: テスト検証と品質保証の統合

## ツール連携
- **Write/Edit/MultiEdit**: 実装のためのコード生成と修正
- **Read/Grep/Glob**: 一貫性のためのプロジェクト分析とパターン検出
- **TodoWrite**: 複雑な複数ファイル実装の進捗追跡
- **Task**: 体系的な連携を必要とする大規模な機能開発のための委任

## 主要パターン
- **コンテキスト検出**: フレームワーク/技術スタック → 適切なペルソナとMCPの起動
- **実装フロー**: 要件 → コード生成 → 検証 → 統合
- **マルチペルソナ連携**: フロントエンド + バックエンド + セキュリティ → 包括的なソリューション
- **品質統合**: 実装 → テスト → ドキュメント → 検証

## 事例

### Reactコンポーネントの実装
```
/sc:implement user profile component --type component --framework react
# Magic MCPがデザインシステム統合でUIコンポーネントを生成
# フロントエンドペルソナがベストプラクティスとアクセシビリティを保証
```

### APIサービスの実装
```
/sc:implement user authentication API --type api --safe --with-tests
# バックエンドペルソナがサーバーサイドロジックとデータ処理を担当
# セキュリティペルソナが認証のベストプラクティスを保証
```

### フルスタック機能
```
/sc:implement payment processing system --type feature --with-tests
# マルチペルソナ連携: architect, frontend, backend, security
# Sequential MCPが複雑な実装ステップを分解
```

### フレームワーク固有の実装
```
/sc:implement dashboard widget --framework vue
# Context7 MCPがVue固有のパターンとドキュメントを提供
# 公式のベストプラクティスを用いたフレームワークに適した実装
```

## 境界

**行うこと:**
- インテリジェントなペルソナ起動とMCP連携で機能を実装する
- フレームワーク固有のベストプラクティスとセキュリティ検証を適用する
- テストとドキュメントの統合を含む包括的な実装を提供する

**行わないこと:**
- 適切なペルソナの相談なしにアーキテクチャの決定を下す
- セキュリティポリシーやアーキテクチャ上の制約に抵触する機能を実装する
- ユーザー指定の安全制約を上書きしたり、品質ゲートをバイパスしたりする
