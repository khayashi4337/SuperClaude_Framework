# SuperClaudeフレームワーク リファレンスドキュメント

**ナビゲーションハブ**: すべてのスキルレベルに対応した、構造化された学習パスと技術リファレンス。

**ドキュメントステータス**: ✅ **ステータス: 最新** - すべてのコンテンツの正確性と完全性が検証済みです。

## このリファレンスライブラリの使い方

このドキュメントは、複数のエントリーポイントを持つ**段階的学習**のために構成されています：

- **📱 クイックリファレンス**: 緊急のニーズに対応する特定のソリューションにジャンプ
- **📚 学習パス**: 初心者からエキスパートへの構造化された進捗
- **🔍 問題解決**: 対象を絞ったトラブルシューティングと診断ガイダンス
- **⚡ パフォーマンス**: 最適化パターンと高度なテクニック

**検証基準**: すべての例はテスト済み、コマンドは検証済み、パターンは実際の使用で証明済みです。

---

## ドキュメントナビゲーションマトリックス

| ドキュメント | 目的 | 対象読者 | 複雑度 | |
|----------|---------|-----------------|------------|-----------------|
| **[basic-examples.md](./basic-examples.md)** | コピペ可能なコマンドとパターン | 全ユーザー、クイックリファレンス | **基本** | |
| **[examples-cookbook.md](./examples-cookbook.md)** | レシピコレクションハブと構成 | 全ユーザー、ナビゲーション | **リファレンス** | |
| **[common-issues.md](./common-issues.md)** | 不可欠なトラブルシューティングと解決策 | 全ユーザー、問題解決 | **基本** | 必要に応じて |
| **[mcp-server-guide.md](./mcp-server-guide.md)** | MCPサーバーの設定と使用法 | 技術ユーザー、統合 | **中級** | |

| **[advanced-patterns.md](./advanced-patterns.md)** | エキスパートの連携とオーケストレーション | 経験豊富なユーザー | **上級** | |
| **[advanced-workflows.md](./advanced-workflows.md)** | 複雑なマルチエージェントオーケストレーション | エキスパートユーザー | **上級** | |
| **[integration-patterns.md](./integration-patterns.md)** | フレームワークとシステムの統合 | アーキテクト、エキスパート | **上級** | |
| **[troubleshooting.md](./troubleshooting.md)** | 包括的な診断ガイド | 全レベル、詳細なデバッグ | **可変** | 必要に応じて |
| **[diagnostic-reference.md](./diagnostic-reference.md)** | 高度なデバッグと分析 | エキスパートユーザー、複雑な問題 | **上級** | |

---

## 推奨学習パス

### 新規ユーザー (1週目 基礎)
**目標**: 不可欠なワークフローでSuperClaudeを自信を持って使用できるようになる

```
1-2日目: ../Getting-Started-jp/quick-start.md
   ↓ 基礎構築と最初のコマンド
3-4日目: basic-examples.md
   ↓ 実践的な応用とパターン認識
5-7日目: common-issues.md
   ↓ 問題解決と自信の構築
```

**成功の指標**: 基本的なコマンドを実行し、セッションを管理し、一般的な問題を自力で解決できる。

### 中級ユーザー (2-3週目 強化)
**目標**: 連携パターンと技術的な深さをマスターする

```
2週目: advanced-patterns.md
   ↓ マルチエージェント連携とオーケストレーションの習得
3週目: mcp-server-guide.md + advanced-workflows.md
   ↓ パフォーマンスの卓越性と技術的な設定
```

**成功の指標**: 複雑なワークフローをオーケストレーションし、パフォーマンスを最適化し、MCPサーバーを設定できる。

### エキスパートユーザー (上級者向け習得)
**目標**: 完全なフレームワークの習得と複雑なシステム統合

```
フェーズ1: advanced-workflows.md
   ↓ 複雑なオーケストレーションとエンタープライズパターン
フェーズ2: integration-patterns.md
   ↓ フレームワーク統合とアーキテクチャの習得
フェーズ3: diagnostic-reference.md
   ↓ 高度なデバッグとシステム分析
```

**成功の指標**: カスタムワークフローを設計し、任意のフレームワークと統合し、複雑な問題を診断できる。

### 問題解決パス (必要に応じて)
**目標**: 即時の問題解決と診断ガイダンス

```
簡単な問題: common-issues.md
   ↓ 一般的な問題と即時の解決策
複雑なデバッグ: troubleshooting.md
   ↓ 包括的な診断アプローチ
高度な分析: diagnostic-reference.md
   ↓ エキスパートレベルのデバッグと分析
```

---

## コマンドクイックリファレンス

### 不可欠なSuperClaudeコマンド

| コマンドパターン | 目的 | 例 |
|----------------|---------|---------|
| `/sc:load` | セッションコンテキストを復元 | `/sc:load project_name` |
| `/sc:save` | セッション状態を保存 | `/sc:save "milestone checkpoint"` |
| `--think` | 構造化された分析を有効化 | `--think analyze performance bottlenecks` |
| `--brainstorm` | 協調的な要件発見 | `--brainstorm new authentication system` |
| `--task-manage` | マルチステップ操作のオーケストレーション | `--task-manage refactor user module` |

### パフォーマンスと効率のフラグ

| フラグ | 目的 | 最適な用途 |
|------|---------|----------|
| `--uc` / `--ultracompressed` | トークン効率の良い通信 | 大規模な操作、コンテキストの圧迫 |
| `--orchestrate` | ツール選択を最適化 | マルチツール操作、パフォーマンスのニーズ |
| `--loop` | 反復的な改善サイクル | コードの洗練、品質向上 |
| `--validate` | 実行前のリスク評価 | 本番環境、重要な操作 |

### MCPサーバーのアクティベーション

| フラグ | サーバー | 最適な用途 |
|------|---------|----------|
| `--c7` / `--context7` | Context7 | 公式ドキュメント、フレームワークパターン |
| `--seq` / `--sequential` | Sequential | 複雑な分析、デバッグ、システム設計 |
| `--magic` | Magic | UIコンポーネント、デザインシステム、フロントエンド作業 |
| `--morph` / `--morphllm` | Morphllm | 一括変換、パターンベースの編集 |
| `--serena` | Serena | シンボル操作、プロジェクトメモリ、大規模なコードベース |
| `--play` / `--playwright` | Playwright | ブラウザテスト、E2Eシナリオ、視覚的検証 |

---

## フレームワーク統合クイックスタート

### React/Next.jsプロジェクト
```bash
# Reactパターンで初期化
--c7 --magic "implement Next.js authentication with TypeScript"

# コンポーネント開発ワークフロー
--magic --think "create responsive dashboard component"
```

### Node.js/Expressバックエンド
```bash
# ベストプラクティスによるAPI開発
--c7 --seq "design RESTful API with Express and MongoDB"

# パフォーマンス最適化
--think --orchestrate "optimize database queries and caching"
```

### フルスタック開発
```bash
# 完全なアプリケーションワークフロー
--task-manage --all-mcp "build full-stack e-commerce platform"

# 統合テスト
--play --seq "implement end-to-end testing strategy"
```

---

## 問題解決クイックリファレンス

### 即時の問題
- **コマンドが機能しない**: [common-issues.md](./common-issues.md) → 一般的なSuperClaudeの問題を確認
- **セッションが失われた**: `/sc:load` を使用 → [セッション管理](../User-Guide-jp/session-management.md)を参照
- **フラグがわからない**: [basic-examples.md](./basic-examples.md) → フラグ使用例を確認

### 開発のブロッカー
- **パフォーマンスが遅い**: [高度なワークフロー](./advanced-workflows.md) → パフォーマンスパターンを参照
- **複雑なデバッグ**: [troubleshooting.md](./troubleshooting.md) → 体系的なデバッグを使用
- **統合の問題**: [integration-patterns.md](./integration-patterns.md) → フレームワークパターンを確認

### システムレベルの問題
- **アーキテクチャの問題**: [advanced-workflows.md](./advanced-workflows.md) → システム設計を使用
- **エキスパートデバッグ**: [diagnostic-reference.md](./diagnostic-reference.md) → 高度な分析を適用
- **カスタムワークフローのニーズ**: [advanced-patterns.md](./advanced-patterns.md) → カスタムオーケストレーションを学ぶ

---

## ドキュメントの健全性と検証

### 品質保証
- ✅ **コマンドテスト済み**: すべての例がテスト済みで機能的
- ✅ **パターン証明済み**: 本番環境での実世界使用検証
- ✅ **相互参照**: 内部リンクの検証と維持
- ✅ **定期的な更新**: ドキュメントはフレームワークの進化と同期

### 正確性の基準
- **コマンド構文**: 最新のSuperClaude実装に対して検証済み
- **フラグの振る舞い**: 複数のシナリオと環境でテスト済み
- **MCP統合**: 現在のMCPサーバーバージョンとの互換性を確認済み
- **パフォーマンス主張**: 現実的な条件下でベンチマークおよび測定済み

### 問題の報告
古い情報や壊れた例を見つけましたか？

1. **簡単な修正**: まず[common-issues.md](./common-issues.md)を確認
2. **ドキュメントのバグ**: 特定のファイルと行を添えてプロジェクトのissueで報告
3. **欠けているパターン**: ユースケースの説明を添えて追加を提案
4. **検証リクエスト**: 特定の例の再テストをリクエスト

---

## 生産性を最大化するためのエキスパートのヒント

### 日常のワークフロー最適化
1. **セッション管理**: 常に`/sc:load`で始め、`/sc:save`で終わる
2. **フラグの組み合わせ**: 補完的なフラグを組み合わせる: `--think --c7`で文書化された分析
3. **段階的な複雑さ**: シンプルに始め、徐々に洗練度を上げる
4. **ツールの専門化**: タスクにツールを合わせる: UIにはMagic、分析にはSequential

### 学習の加速
1. **パスに従う**: 構造化された成長のために推奨される学習シーケンスを使用する
2. **パターンを練習する**: 直感的になるまで一般的なワークフローを繰り返す
3. **安全に実験する**: 探索のために機能ブランチとチェックポイントを使用する
4. **コミュニティ学習**: 発見を共有し、他者のアプローチから学ぶ

### トラブルシューティングの習得
1. **体系的なアプローチ**: 常に[common-issues.md](./common-issues.md)から始める
2. **証拠収集**: 複雑な問題分析のために`--think`を使用する
3. **根本原因に焦点を当てる**: 症状だけでなく、根本的な問題に対処する
4. **ドキュメント第一**: 実験的な解決策の前に公式ドキュメントを確認する

---

## 高度なリソースと統合

### フレームワーク固有のガイド
- **React/Next.js**: [integration-patterns.md](./integration-patterns.md) → React統合を参照
- **Vue/Nuxt**: [integration-patterns.md](./integration-patterns.md) → Vueエコシステムを参照
- **Node.js/Express**: [integration-patterns.md](./integration-patterns.md) → バックエンドパターンを参照
- **Python/Django**: [integration-patterns.md](./integration-patterns.md) → Pythonワークフローを参照

### 特化したワークフロー
- **DevOps統合**: [advanced-workflows.md](./advanced-workflows.md) → CI/CDパターン
- **テスト戦略**: [advanced-patterns.md](./advanced-patterns.md) → テストオーケストレーション
- **パフォーマンスエンジニアリング**: [高度なパターン](./advanced-patterns.md) → 複雑な連携
- **セキュリティ実装**: [integration-patterns.md](./integration-patterns.md) → セキュリティパターン

### コミュニティとサポート
- **ベストプラクティス**: コミュニティのフィードバックに基づいて継続的に更新
- **パターンライブラリ**: 実証済みのワークフローパターンの成長するコレクション
- **エキスパートネットワーク**: 経験豊富なSuperClaude実践者とつながる
- **定期的な更新**: ドキュメントはフレームワークの能力と共に進化

---

**旅を始めよう**: SuperClaudeは初めてですか？ [クイックスタートガイド](../Getting-Started-jp/quick-start.md)から始めて、即時の生産性向上を実現しましょう。

**今すぐ答えが必要**: [basic-examples.md](./basic-examples.md)にジャンプして、コピペできる解決策を入手しましょう。

**上級者向け**: [advanced-patterns.md](./advanced-patterns.md)を探索して、エキスパートレベルのオーケストレーションを学びましょう。
