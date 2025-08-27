---
name: workflow
description: "PRDと機能要件から構造化された実装ワークフローを生成する"
category: orchestration
complexity: advanced
mcp-servers: [sequential, context7, magic, playwright, morphllm, serena]
personas: [architect, analyzer, frontend, backend, security, devops, project-manager]
---

# /sc:workflow - 実装ワークフロー生成

## トリガー
- 実装計画用PRDと機能仕様の分析
- 開発プロジェクト用構造化ワークフロー生成
- 複雑実装戦略用マルチペルソナ連携
- セッション間ワークフロー管理と依存関係マッピング

## 使用法
```
/sc:workflow [prd-file|feature-description] [--strategy systematic|agile|enterprise] [--depth shallow|normal|deep] [--parallel]
```

## 動作フロー
1. **分析**: PRDと機能仕様を解析し実装要件を理解
2. **計画**: 依存関係マッピングとタスクオーケストレーションを含む包括的ワークフロー構造を生成
3. **連携**: ドメイン専門知識と実装戦略用に複数ペルソナを活性化
4. **実行**: 自動タスク連携で構造化ステップバイステップワークフローを作成
5. **検証**: 品質ゲートを適用しドメイン間ワークフロー完全性を確保

主な動作:
- アーキテクチャ、フロントエンド、バックエンド、セキュリティ、DevOpsドメインを跨いだマルチペルソナオーケストレーション
- 専門ワークフロー分析用の高度MCP連携とインテリジェントルーティング
- 漸進的ワークフロー強化と並列処理での体系的実行
- 包括的依存関係追跡付きクロスセッションワークフロー管理

## MCP統合
- **Sequential MCP**: 複雑マルチステップワークフロー分析と体系的実装計画
- **Context7 MCP**: フレームワーク固有ワークフローパターンと実装ベストプラクティス
- **Magic MCP**: UI/UXワークフロー生成とデザインシステム統合戦略
- **Playwright MCP**: テストワークフロー統合と品質保証自動化
- **Morphllm MCP**: 大規模ワークフロー変換とパターンベース最適化
- **Serena MCP**: セッション間ワークフロー永続化、メモリ管理、プロジェクトコンテキスト

## ツール連携
- **Read/Write/Edit**: PRD分析とワークフロードキュメント生成
- **TodoWrite**: 複雑マルチフェーズワークフロー実行の進捗追跡
- **Task**: 並列ワークフロー生成とマルチエージェント連携用高度委任
- **WebSearch**: 技術調査、フレームワーク検証、実装戦略分析
- **sequentialthinking**: 複雑ワークフロー依存関係分析用構造化推論

## 主要パターン
- **PRD分析**: ドキュメント解析 → 要件抽出 → 実装戦略策定
- **ワークフロー生成**: タスク分解 → 依存関係マッピング → 構造化実装計画
- **マルチドメイン連携**: 部門横断専門知識 → 包括的実装戦略
- **品質統合**: ワークフロー検証 → テスト戦略 → デプロイ計画

## 例

### 体系的PRDワークフロー
```
/sc:workflow ClaudeDocs/PRD/feature-spec.md --strategy systematic --depth deep
# 体系的ワークフロー生成での包括的PRD分析
# 完全実装戦略用マルチペルソナ連携
```

### アジャイル機能ワークフロー
```
/sc:workflow "ユーザー認証システム" --strategy agile --parallel
# 並列タスク連携でのアジャイルワークフロー生成
# フレームワークとUIワークフローパターン用Context7とMagic MCP
```

### エンタープライズ実装計画
```
/sc:workflow enterprise-prd.md --strategy enterprise --validate
# 包括的検証付きエンタープライズ規模ワークフロー
# コンプライアンスとスケーラビリティ用security、devops、architectペルソナ
```

### セッション間ワークフロー管理
```
/sc:workflow project-brief.md --depth normal
# Serena MCPがセッション間ワークフローコンテキストと永続性を管理
# メモリ駆動洞察での漸進的ワークフロー強化
```

## 境界

**実行可能:**
- PRDと機能仕様からの包括的実装ワークフロー生成
- 完全実装戦略用マルチペルソナとMCPサーバーの連携
- セッション間ワークフロー管理と漸進的機能強化の提供

**実行不可:**
- ワークフロー計画と戦略を超えた実装タスクの実行
- 適切な分析と検証なしでの確立済み開発プロセスの無視
- 包括的要件分析と依存関係マッピングなしでのワークフロー生成