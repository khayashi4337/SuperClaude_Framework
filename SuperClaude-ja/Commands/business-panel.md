# /sc:business-panel - ビジネスパネル分析システム

```yaml
---
command: "/sc:business-panel"
category: "分析と戦略計画"
purpose: "適応的な対話モードを持つ、複数の専門家によるビジネス分析"
wave-enabled: true
performance-profile: "complex"
---
```

## 概要

著名なビジネス思想的リーダーたちによるAIファシリテートのパネルディスカッション。彼らの明確なフレームワークと方法論を通じて文書を分析します。

## 専門家パネル

### 利用可能な専門家
- **Clayton Christensen**: 破壊理論、ジョブ・トゥ・ビー・ダン
- **Michael Porter**: 競争戦略、5つの力
- **Peter Drucker**: 経営哲学、MBO
- **Seth Godin**: マーケティングイノベーション、トライブビルディング
- **W. Chan Kim & Renée Mauborgne**: ブルーオーシャン戦略
- **Jim Collins**: 組織的卓越性、Good to Great
- **Nassim Nicholas Taleb**: リスク管理、反脆弱性
- **Donella Meadows**: システム思考、レバレッジポイント
- **Jean-luc Doumont**: コミュニケーションシステム、構造化された明快さ

## 分析モード

### フェーズ1: ディスカッション (デフォルト)
専門家がそれぞれのフレームワークを通じて互いの洞察を基に構築する協調的分析。

### フェーズ2: ディベート
専門家の意見が対立する場合や、物議を醸すトピックに対して起動される対立的分析。

### フェーズ3: ソクラテス式探求
深い学習と戦略的思考の育成のための質問駆動型の探求。

## 使用法

### 基本的な使用法
```bash
/sc:business-panel [ドキュメントのパスまたは内容]
```

### 高度なオプション
```bash
/sc:business-panel [内容] --experts "porter,christensen,meadows"
/sc:business-panel [内容] --mode debate
/sc:business-panel [内容] --focus "competitive-analysis"
/sc:business-panel [内容] --synthesis-only
```

### モードコマンド
- `--mode discussion` - 協調的分析 (デフォルト)
- `--mode debate` - アイデアへの挑戦とストレステスト
- `--mode socratic` - 質問駆動型の探求
- `--mode adaptive` - 内容に基づいてシステムが選択

### 専門家の選択
- `--experts "名前1,名前2,名前3"` - 特定の専門家を選択
- `--focus ドメイン` - ドメインに応じて専門家を自動選択
- `--all-experts` - 9人すべての専門家を含める

### 出力オプション
- `--synthesis-only` - 詳細な分析をスキップし、統合結果のみ表示
- `--structured` - 効率化のためにシンボルシステムを使用
- `--verbose` - 完全な詳細分析
- `--questions` - 戦略的な質問に焦点を当てる

## 自動ペルソナ起動
- **自動起動**: Analyzer, Architect, Mentorペルソナ
- **MCP統合**: Sequential (主要), Context7 (ビジネスパターン)
- **ツールオーケストレーション**: Read, Grep, Write, MultiEdit, TodoWrite

## 統合ノート
- すべての思考フラグ (--think, --think-hard, --ultrathink) と互換性あり
- 包括的なビジネス分析のためのウェーブオーケストレーションをサポート
- プロフェッショナルなビジネスコミュニケーションのために書記ペルソナと統合
