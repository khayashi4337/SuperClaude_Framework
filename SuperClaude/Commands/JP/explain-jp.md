---
name: explain
description: 「コード、概念、システム動作を教育的にわかりやすく説明」
category: workflow
complexity: standard
mcp-servers: [sequential, context7]
personas: [educator, architect, security]
---

# /sc:explain - コードとコンセプトの説明

## トリガー
- 複雑な機能に関するコードの理解とドキュメントの要求
- アーキテクチャコンポーネントのシステム動作の説明の必要性
- 知識移転のための教育コンテンツの生成
- フレームワーク固有の概念明確化要件

## 使用法
```
/sc:explain [target] [--level basic|intermediate|advanced] [--format text|examples|interactive] [--context domain]
```

## 動作フロー
1. **分析**: 対象のコード、概念、またはシステムを包括的に理解するために調査する
2. **評価**: 対象者のレベルと適切な説明の深さと形式を決定する
3. **構造**: 段階的な複雑さと論理的な流れを備えた説明シーケンスを計画する
4. **生成**: 例、図、インタラクティブな要素を使って明確な説明を作成します
5. **検証**:説明の正確さと教育効果を検証する

主要動作:
- ドメイン専門知識用マルチペルソナ連携（educator、architect、security）
- Context7統合によるフレームワーク固有の説明
- 複雑な概念を分解するためのシーケンシャルMCPによる体系的な分析
- 対象者と複雑さに基づいて説明の深さを適応的に調整

## MCP連携
- **Sequential MCP**: 複雑マルチコンポーネント分析と構造化推論用自動有効化
- **Context7 MCP**: フレームワークドキュメントと公式パターン説明
- **ペルソナ連携**: educator（学習）、architect（システム）、security（実践）

## ツール連携
- **Read/Grep/Glob**: 説明コンテンツのコード分析とパターン識別
- **TodoWrite**: 複雑な複数パートの説明の進捗状況を追跡します
- **Task**: 体系的内訳必要包括的説明ワークフロー委任

## 主要パターン
- **漸進的学習**: 基本概念 → 中級詳細 → 高度な実装
- **フレームワーク統合**: Context7ドキュメント → 正確な公式パターンとプラクティス
- **マルチドメイン分析**: 技術的な正確さ + 教育的な明確さ + セキュリティ意識
- **インタラクティブな説明**: 静的コンテンツ → 例 → インタラクティブな探索

## 例

### 基本コード説明
```
/sc:explain authentication.js --level basic
# 初心者向け実例交えてわかりやすく解説
# educatorペルソナが学習最適化構造提供
```

### フレームワーク概念説明
```
/sc:explain react-hooks --level intermediate --context react
# 公式ReactドキュメントパターンのContext7連携
# 段階的複雑化する構造化説明
```

### システムアーキテクチャ説明
```
/sc:explain microservices-system --level advanced --format interactive
# architectペルソナがシステム設計とパターン説明
# Sequential分析内訳でのインタラクティブ探索
```

### セキュリティ概念説明
```
/sc:explain jwt-authentication --context security --level basic
# securityペルソナが認証概念とベストプラクティス説明
# フレームワーク非依存セキュリティ原則と実例
```

## 境界

**実行可能:**
- 教育的に明確かつ包括的な説明を提供する
- ドメインの専門知識と正確な分析のために、関連するペルソナを自動的にアクティブ化します
- 公式ドキュメントの統合によりフレームワーク固有の説明を生成

**実行不可:**
- 徹底分析や正確性検証なしでの説明生成
- プロジェクト固有ドキュメント標準無視や機密情報公開
- 確立済み説明検証や教育品質要件回避