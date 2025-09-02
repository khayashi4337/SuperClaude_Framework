# BUSINESS_PANEL_EXAMPLES.md - 使用例と統合パターン

## 基本的な使用例

### 例1: 戦略計画分析
```bash
/sc:business-panel @strategy_doc.pdf

# 出力: Porter, Collins, Meadows, Doumontによるディスカッションモード
# 分析は、競争上のポジショニング、組織能力、
# システムダイナミクス、およびコミュニケーションの明確さに焦点を当てます
```

### 例2: イノベーション評価
```bash
/sc:business-panel "我々はAIを活用した顧客サービスを開発している" --experts "christensen,drucker,godin"

# 出力: ジョブ・トゥ・ビー・ダン、顧客価値、
# および注目度/トライブ構築に焦点を当てたディスカッションモード
```

### 例3: ディベートによるリスク分析
```bash
/sc:business-panel @risk_assessment.md --mode debate

# 出力: Talebが従来のリスク評価に異議を唱えるディベートモード、
# 他の専門家は自身のフレームワークを擁護し、対立に関するシステム的視点
```

### 例4: 戦略的学習セッション
```bash
/sc:business-panel "競争戦略について理解を深めたい" --mode socratic

# 出力: 複数のフレームワークからの戦略的な質問を伴うソクラテスモード、
# ユーザーの応答に基づく段階的な質問
```

## 高度な使用パターン

### 複数ドキュメント分析
```bash
/sc:business-panel @market_research.pdf @competitor_analysis.xlsx @financial_projections.csv --synthesis-only

# 統合に焦点を当てた、複数ドキュメントにわたる包括的な分析
```

### ドメイン特化分析
```bash
/sc:business-panel @product_strategy.md --focus "innovation" --experts "christensen,drucker,meadows"

# 破壊理論、経営原則、システム思考によるイノベーションに焦点を当てた分析
```

### 構造化コミュニケーションへの焦点
```bash
/sc:business-panel @exec_presentation.pptx --focus "communication" --structured

# メッセージの明確さ、聴衆のニーズ、認知的負荷の最適化に焦点を当てた分析
```

## SuperClaudeコマンドとの統合

### /analyzeとの組み合わせ
```bash
/analyze @business_model.md --business-panel

# 技術分析に続く、ビジネス専門家パネルによるレビュー
```

### /improveとの組み合わせ
```bash
/improve @strategy_doc.md --business-panel --iterative

# ビジネス専門家の検証を伴う反復的な改善
```

### /designとの組み合わせ
```bash
/design business-model --business-panel --experts "drucker,porter,kim_mauborgne"

# 専門家のガイダンスによるビジネスモデル設計
```

## 専門家選択戦略

### ビジネスドメイン別
```yaml
strategy_planning:
  experts: ['porter', 'kim_mauborgne', 'collins', 'meadows']
  rationale: "競争分析、ブルーオーシャンの機会、実行の卓越性、システム思考"

innovation_management:
  experts: ['christensen', 'drucker', 'godin', 'meadows']
  rationale: "破壊理論、体系的イノベーション、注目度、システムアプローチ"

organizational_development:
  experts: ['collins', 'drucker', 'meadows', 'doumont']
  rationale: "卓越性の原則、経営の有効性、システム変更、明確なコミュニケーション"

risk_management:
  experts: ['taleb', 'meadows', 'porter', 'collins']
  rationale: "反脆弱性、システムの回復力、競争上の脅威、規律ある実行"

market_entry:
  experts: ['porter', 'christensen', 'godin', 'kim_mauborgne']
  rationale: "業界分析、破壊の可能性、トライブ構築、ブルーオーシャン創出"

business_model_design:
  experts: ['christensen', 'drucker', 'kim_mauborgne', 'meadows']
  rationale: "価値創造、顧客中心、価値イノベーション、システムダイナミクス"
```

### 分析タイプ別
```yaml
comprehensive_audit:
  experts: "all"
  mode: "discussion → debate → synthesis"

strategic_validation:
  experts: ['porter', 'collins', 'taleb']
  mode: "debate"

learning_facilitation:
  experts: ['drucker', 'meadows', 'doumont']
  mode: "socratic"

quick_assessment:
  experts: "auto-select-3"
  mode: "discussion"
  flags: "--synthesis-only"
```

## 出力フォーマットのバリエーション

### エグゼクティブサマリー形式
```bash
/sc:business-panel @doc.pdf --structured --synthesis-only

# 出力:
## 🎯 戦略的評価
**💰 財務的影響**: [主要な経済的要因]
**🏆 競争上の地位**: [優位性分析]
**📈 成長機会**: [拡大の可能性]
**⚠️ リスク要因**: [重大な脅威]
**🧩 統合**: [統合された推奨事項]
```

### フレームワーク別形式
```bash
/sc:business-panel @doc.pdf --verbose

# 出力:
## 📚 CHRISTENSEN - 破壊分析
[ジョブ・トゥ・ビー・ダンと破壊評価の詳細]

## 📊 PORTER - 競争戦略
[5つの力とバリューチェーン分析]

## 🧩 フレームワーク横断的な統合
[統合と戦略的意味合い]
```

### 質問駆動形式
```bash
/sc:business-panel @doc.pdf --questions

# 出力:
## 🤔 検討すべき戦略的質問
**🔨 イノベーションに関する質問** (Christensen):
- これは何のジョブのために雇われているのか？

**⚔️ 競争に関する質問** (Porter):
- 持続可能な優位性は何か？

**🧭 経営に関する質問** (Drucker):
- 我々の事業はどうあるべきか？
```

## 統合ワークフロー

### ビジネス戦略開発
```yaml
workflow_stages:
  stage_1: "/sc:business-panel @market_research.pdf --mode discussion"
  stage_2: "/sc:business-panel @competitive_analysis.md --mode debate"
  stage_3: "/sc:business-panel 'synthesize findings' --mode socratic"
  stage_4: "/design strategy --business-panel --experts 'porter,kim_mauborgne'"
```

### イノベーションパイプライン評価
```yaml
workflow_stages:
  stage_1: "/sc:business-panel @innovation_portfolio.xlsx --focus innovation"
  stage_2: "/improve @product_roadmap.md --business-panel"
  stage_3: "/analyze @market_opportunities.pdf --business-panel --think"
```

### リスク管理レビュー
```yaml
workflow_stages:
  stage_1: "/sc:business-panel @risk_register.pdf --experts 'taleb,meadows,porter'"
  stage_2: "/sc:business-panel 'challenge risk assumptions' --mode debate"
  stage_3: "/implement risk_mitigation --business-panel --validate"
```

## カスタマイズオプション

### 専門家の振る舞いの変更
```bash
# 特定の側面に特定の専門家を集中させる
/sc:business-panel @doc.pdf --christensen-focus "disruption-potential"
/sc:business-panel @doc.pdf --porter-focus "competitive-moats"

# 専門家の対話スタイルを調整する
/sc:business-panel @doc.pdf --interaction "collaborative" # より穏やかなディベートモード
/sc:business-panel @doc.pdf --interaction "challenging" # より強いディベートモード
```

### 出力のカスタマイズ
```bash
# シンボル密度の制御
/sc:business-panel @doc.pdf --symbols minimal  # シンボルの使用を減らす
/sc:business-panel @doc.pdf --symbols rich     # 完全なシンボルシステムを使用

# 分析深度の制御
/sc:business-panel @doc.pdf --depth surface    # 高レベルの概要
/sc:business-panel @doc.pdf --depth detailed   # 包括的な分析
```

### 時間とリソースの管理
```bash
# 時間制約のある場合の迅速な分析
/sc:business-panel @doc.pdf --quick --experts-max 3

# 重要な決定のための包括的な分析
/sc:business-panel @doc.pdf --comprehensive --all-experts

# リソースを意識した分析
/sc:business-panel @doc.pdf --budget 10000  # トークン制限
```

## 品質検証

### 分析品質チェック
```yaml
authenticity_validation:
  voice_consistency: "各専門家が特徴的なスタイルを維持している"
  framework_fidelity: "分析が本物の方法論に従っている"
  interaction_realism: "専門家のダイナミクスがプロのパターンを反映している"

business_relevance:
  strategic_focus: "分析が真の戦略的懸念に対処している"
  actionable_insights: "推奨事項が実行可能である"
  evidence_based: "結論がフレームワークの論理によって裏付けられている"

integration_quality:
  synthesis_value: "統合された洞察が個々の分析を超える"
  framework_preservation: "統合がフレームワークの独自性を維持している"
  practical_utility: "結果が戦略的な意思決定をサポートする"
```

### パフォーマンス基準
```yaml
response_time:
  simple_analysis: "< 30秒"
  comprehensive_analysis: "< 2分"
  multi_document: "< 5分"

token_efficiency:
  discussion_mode: "8-15K トークン"
  debate_mode: "10-20K トークン"
  socratic_mode: "12-25K トークン"
  synthesis_only: "3-8K トークン"

accuracy_targets:
  framework_authenticity: "> 90%"
  strategic_relevance: "> 85%"
  actionable_insights: "> 80%"
```
