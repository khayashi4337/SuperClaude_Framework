# SuperClaude エージェントガイド 🤖

SuperClaudeは、Claude Codeが専門的な知識を必要とするときに呼び出すことができる、14のドメイン専門エージェントを提供します。

## 🧪 エージェント起動のテスト

このガイドを使用する前に、エージェントの選択が機能することを確認してください：

```bash
# 手動エージェント呼び出しのテスト
@agent-python-expert "デコレータについて説明して"
# 振る舞いの例: Pythonエキスパートが詳細な説明で応答します

# セキュリティエージェントの自動起動テスト
/sc:implement "JWT認証"
# 振る舞いの例: セキュリティエンジニアが自動的に起動するはずです

# フロントエンドエージェントの自動起動テスト
/sc:implement "レスポンシブなナビゲーションコンポーネント"
# 振る舞いの例: フロントエンドアーキテクト + Magic MCPが起動するはずです

# 体系的分析のテスト
/sc:troubleshoot "遅いAPIパフォーマンス"
# 振る舞いの例: 根本原因アナリスト + パフォーマンスエンジニアが起動します

# 手動と自動の組み合わせテスト
/sc:analyze src/
@agent-refactoring-expert "改善点を提案して"
# 振る舞いの例: 分析に続いてリファクタリングの提案が行われます
```

**テストが失敗した場合**: `~/.claude/agents/`にエージェントファイルが存在するか確認するか、Claude Codeセッションを再起動してください。

## コアコンセプト

### SuperClaudeエージェントとは？
**エージェント**は、Claude Codeの振る舞いを変更するコンテキスト指示として実装された、専門分野のAIドメインエキスパートです。各エージェントは、`SuperClaude/Agents/`ディレクトリにある、ドメイン固有の専門知識、振る舞いパターン、問題解決アプローチを含む、注意深く作成された`.md`ファイルです。

**重要**: エージェントは独立したAIモデルやソフトウェアではありません。これらは、Claude Codeが専門的な振る舞いを採用するために読み込むコンテキスト設定です。

### エージェントの2つの使用方法

#### 1. `@agent-`プレフィックスによる手動呼び出し
```bash
# 特定のエージェントを直接呼び出す
@agent-security "認証の実装をレビューして"
@agent-frontend "レスポンシブなナビゲーションを設計して"
@agent-architect "マイクロサービスへの移行を計画して"
```

#### 2. 自動起動（振る舞いルーティング）
「自動起動」とは、Claude Codeが振る舞いの指示を読み取り、リクエスト内のキーワードやパターンに基づいて適切なコンテキストを呼び出すことを意味します。SuperClaudeは、Claudeが最も適切な専門家にルーティングするために従う振る舞いのガイドラインを提供します。

> **📝 エージェントの「自動起動」の仕組み**:
> エージェントの起動は自動的なシステムロジックではなく、コンテキストファイル内の振る舞いの指示です。
> ドキュメントでエージェントが「自動起動する」と記載されている場合、それはClaude Codeが指示を読み取り、
> リクエスト内のキーワードやパターンに基づいて特定のドメイン専門知識を呼び出すことを意味します。これにより、
> 基盤となるメカニズムについて透明性を保ちながら、インテリジェントなルーティング体験が生み出されます。

```bash
# これらのコマンドは関連するエージェントを自動起動します
/sc:implement "JWT認証"  # → security-engineerが自動起動
/sc:design "Reactダッシュボード"        # → frontend-architectが自動起動
/sc:troubleshoot "メモリリーク"      # → performance-engineerが自動起動
```

**MCPサーバー**は、Context7（ドキュメント）、Sequential（分析）、Magic（UI）、Playwright（テスト）、Morphllm（コード変換）などの専門ツールを通じて強化された機能を提供します。

**ドメイン専門家**は、狭い専門分野に焦点を当て、ジェネラリストのアプローチよりも深く、より正確なソリューションを提供します。

### エージェント選択ルール

**優先順位:**
1. **手動上書き** - `@agent-[name]`は自動起動より優先されます
2. **キーワード** - 直接的なドメイン用語が主要なエージェントをトリガーします
3. **ファイルタイプ** - 拡張子が言語/フレームワークの専門家を起動します
4. **複雑さ** - 複数ステップのタスクは調整エージェントを呼び出します
5. **コンテキスト** - 関連する概念が補完的なエージェントをトリガーします

**競合の解決:**
- 手動呼び出し → 指定されたエージェントが優先されます
- 複数の一致 → マルチエージェントによる調整
- 不明瞭なコンテキスト → 要求アナリストの起動
- 高い複雑さ → システムアーキテクトによる監督
- 品質に関する懸念 → QAエージェントの自動的な参加

**選択決定木:**
```
タスク分析 →
├─ 手動 @agent-? → 指定されたエージェントを使用
├─ 単一ドメインか？ → 主要エージェントを起動
├─ 複数ドメインか？ → 専門エージェントを調整
├─ 複雑なシステムか？ → システムアーキテクトの監督を追加
├─ 品質が重要か？ → セキュリティ + パフォーマンス + 品質エージェントを含める
└─ 学習が焦点か？ → 学習ガイド + テクニカルライターを追加
```

## クイックスタート事例

### 手動エージェント呼び出し
```bash
# @agent- プレフィックスで特定のエージェントを明示的に呼び出す
@agent-python-expert "このデータ処理パイプラインを最適化して"
@agent-quality-engineer "包括的なテストスイートを作成して"
@agent-technical-writer "このAPIを例付きで文書化して"
@agent-socratic-mentor "このデザインパターンを説明して"
```

### 自動エージェント調整
```bash
# 自動起動をトリガーするコマンド
/sc:implement "レート制限付きのJWT認証"
# → トリガー: security-engineer + backend-architect + quality-engineer

/sc:design "ドキュメント付きのアクセシブルなReactダッシュボード"
# → トリガー: frontend-architect + learning-guide + technical-writer

/sc:troubleshoot "断続的な障害を伴う遅いデプロイメントパイプライン"
# → トリガー: devops-architect + performance-engineer + root-cause-analyst

/sc:audit "支払い処理のセキュリティ脆弱性"
# → トリガー: security-engineer + quality-engineer + refactoring-expert
```

### 手動と自動アプローチの組み合わせ
```bash
# コマンドで開始（自動起動）
/sc:implement "ユーザープロファイルシステム"

# その後、専門家のレビューを明示的に追加
@agent-security "OWASPコンプライアンスについてプロファイルシステムをレビューして"
@agent-performance-engineer "データベースクエリを最適化して"
```

---

## SuperClaudeエージェントチーム 👥

### アーキテクチャ & システム設計エージェント 🏗️

### system-architect 🏢
**専門知識**: スケーラビリティとサービスアーキテクチャに焦点を当てた大規模分散システムの設計

**自動起動**:
- キーワード: "architecture", "microservices", "scalability", "system design", "distributed"
- コンテキスト: マルチサービスシステム、アーキテクチャ上の決定、技術選択
- 複雑さ: 5つ以上のコンポーネントまたはドメイン間の統合要件

**能力**:
- サービス境界の定義とマイクロサービスの分割
- 技術スタックの選択と統合戦略
- スケーラビリティ計画とパフォーマンスアーキテクチャ
- イベント駆動型アーキテクチャとメッセージングパターン
- データフロー設計とシステム統合

**事例**:
1. **Eコマースプラットフォーム**: ユーザー、製品、支払い、通知サービスのマイクロサービスをイベントソーシングで設計
2. **リアルタイム分析**: ストリーム処理と時系列ストレージによる高スループットデータ取り込みのためのアーキテクチャ
3. **マルチテナントSaaS**: テナント分離、共有インフラ、水平スケーリング戦略を備えたシステム設計

### 成功基準
- [ ] 応答にシステムレベルの思考が明確に現れている
- [ ] サービス境界と統合パターンに言及している
- [ ] スケーラビリティと信頼性に関する考察が含まれている
- [ ] 技術スタックの推奨が提供されている

**検証:** `/sc:design "microservices platform"` は system-architect を起動するべきです
**テスト:** 出力にはサービスの分割と統合パターンが含まれるべきです
**確認:** インフラに関する懸念事項について devops-architect と調整するべきです

**最適な組み合わせ**: devops-architect (インフラ), performance-engineer (最適化), security-engineer (コンプライアンス)

---

### backend-architect ⚙️
**専門知識**: APIの信頼性とデータの整合性を重視した堅牢なサーバーサイドシステムの設計

**自動起動**:
- キーワード: "API", "backend", "server", "database", "REST", "GraphQL", "endpoint"
- ファイルタイプ: API仕様書, サーバー設定ファイル, データベーススキーマ
- コンテキスト: サーバーサイドロジック, データ永続化, API開発

**能力**:
- RESTfulおよびGraphQL APIのアーキテクチャとデザインパターン
- データベーススキーマ設計とクエリ最適化戦略
- 認証、認可、セキュリティの実装
- エラーハンドリング、ロギング、モニタリングの統合
- キャッシュ戦略とパフォーマンス最適化

**事例**:
1. **ユーザー管理API**: ロールベースのアクセス制御とレート制限を備えたJWT認証
2. **支払い処理**: べき等性と監査証跡を備えたPCI準拠のトランザクション処理
3. **コンテンツ管理**: キャッシュ、ページネーション、リアルタイム通知を備えたRESTful API

**最適な組み合わせ**: security-engineer (認証/セキュリティ), performance-engineer (最適化), quality-engineer (テスト)

---

### frontend-architect 🎨
**専門知識**: アクセシビリティとユーザーエクスペリエンスに焦点を当てたモダンなWebアプリケーションアーキテクチャ

**自動起動**:
- キーワード: "UI", "frontend", "React", "Vue", "Angular", "component", "accessibility", "responsive"
- ファイルタイプ: .jsx, .vue, .ts (フロントエンド), .css, .scss
- コンテキスト: ユーザーインターフェース開発, コンポーネント設計, クライアントサイドアーキテクチャ

**能力**:
- コンポーネントアーキテクチャとデザインシステムの実装
- 状態管理パターン (Redux, Zustand, Pinia)
- アクセシビリティ準拠 (WCAG 2.1) とインクルーシブデザイン
- パフォーマンス最適化とバンドル分析
- プログレッシブWebアプリとモバイルファースト開発

**事例**:
1. **ダッシュボードインターフェース**: リアルタイム更新とレスポンシブグリッドレイアウトを備えたアクセシブルなデータ可視化
2. **フォームシステム**: 検証、エラーハンドリング、アクセシビリティ機能を備えた複雑なマルチステップフォーム
3. **デザインシステム**: 一貫したスタイリングとインタラクションパターンを持つ再利用可能なコンポーネントライブラリ

**最適な組み合わせ**: learning-guide (ユーザーガイダンス), performance-engineer (最適化), quality-engineer (テスト)

---

### devops-architect 🚀
**専門知識**: 信頼性の高いソフトウェア提供のためのインフラ自動化とデプロイメントパイプラインの設計

**自動起動**:
- キーワード: "deploy", "CI/CD", "Docker", "Kubernetes", "infrastructure", "monitoring", "pipeline"
- ファイルタイプ: Dockerfile, docker-compose.yml, k8sマニフェスト, CI設定ファイル
- コンテキスト: デプロイメントプロセス, インフラ管理, 自動化

**能力**:
- 自動テストとデプロイメントを備えたCI/CDパイプライン設計
- コンテナオーケストレーションとKubernetesクラスタ管理
- TerraformとクラウドプラットフォームによるInfrastructure as Code
- モニタリング、ロギング、オブザーバビリティスタックの実装
- セキュリティスキャンとコンプライアンス自動化

**事例**:
1. **マイクロサービスのデプロイ**: サービスメッシュ、オートスケーリング、ブルーグリーンリリースを備えたKubernetesデプロイ
2. **マルチ環境パイプライン**: 自動テスト、セキュリティスキャン、ステージングデプロイを備えたGitOpsワークフロー
3. **モニタリングスタック**: メトリクス、ログ、トレース、アラートシステムによる包括的なオブザーバビリティ

**最適な組み合わせ**: system-architect (インフラ計画), security-engineer (コンプライアンス), performance-engineer (モニタリング)

### 品質 & 分析エージェント 🔍

### security-engineer 🔒
**専門知識**: 脅威モデリングと脆弱性防止に焦点を当てたアプリケーションセキュリティアーキテクチャ

**自動起動**:
- キーワード: "security", "auth", "authentication", "vulnerability", "encryption", "compliance", "OWASP"
- コンテキスト: セキュリティレビュー, 認証フロー, データ保護要件
- リスク指標: 支払い処理, ユーザーデータ, APIアクセス, 規制コンプライアンスの必要性

**能力**:
- 脅威モデリングと攻撃対象領域の分析
- 安全な認証・認可設計 (OAuth, JWT, SAML)
- データ暗号化戦略と鍵管理
- 脆弱性評価と侵入テストのガイダンス
- セキュリティコンプライアンス (GDPR, HIPAA, PCI-DSS) の実装

**事例**:
1. **OAuth実装**: トークンリフレッシュとロールベースアクセスによる安全なマルチテナント認証
2. **APIセキュリティ**: レート制限, 入力検証, SQLインジェクション防止, セキュリティヘッダ
3. **データ保護**: 保存時/転送時の暗号化, 鍵のローテーション, プライバシーバイデザインアーキテクチャ

**最適な組み合わせ**: backend-architect (APIセキュリティ), quality-engineer (セキュリティテスト), root-cause-analyst (インシデント対応)

---

### performance-engineer ⚡
**専門知識**: スケーラビリティとリソース効率に焦点を当てたシステムパフォーマンスの最適化

**自動起動**:
- キーワード: "performance", "slow", "optimization", "bottleneck", "latency", "memory", "CPU"
- コンテキスト: パフォーマンス問題, スケーラビリティの懸念, リソース制約
- メトリクス: 応答時間 >500ms, 高いメモリ使用量, 低いスループット

**能力**:
- パフォーマンスプロファイリングとボトルネックの特定
- データベースクエリの最適化とインデックス戦略
- キャッシュ実装 (Redis, CDN, アプリケーションレベル)
- 負荷テストとキャパシティプランニング
- メモリ管理とリソース最適化

**事例**:
1. **API最適化**: キャッシュとクエリ最適化により応答時間を2秒から200msに短縮
2. **データベーススケーリング**: リードレプリカ、接続プーリング、クエリ結果キャッシュの実装
3. **フロントエンドパフォーマンス**: バンドル最適化、遅延読み込み、CDN実装により3秒未満の読み込み時間を実現

**最適な組み合わせ**: system-architect (スケーラビリティ), devops-architect (インフラ), root-cause-analyst (デバッグ)

---

### root-cause-analyst 🔍
**専門知識**: 証拠に基づく分析と仮説検定を用いた体系的な問題調査

**自動起動**:
- キーワード: "bug", "issue", "problem", "debugging", "investigation", "troubleshoot", "error"
- コンテキスト: システム障害, 予期せぬ振る舞い, 複雑な複数コンポーネントの問題
- 複雑さ: 体系的な調査を必要とするシステム横断的な問題

**能力**:
- 体系的なデバッグ手法と根本原因分析
- システム間のエラー相関と依存関係マッピング
- 障害調査のためのログ分析とパターン認識
- 複雑な問題に対する仮説の形成と検証
- インシデント対応と事後分析の手順

**事例**:
1. **データベース接続障害**: 接続プール、ネットワークタイムアウト、リソース制限にわたる断続的な障害を追跡
2. **支払い処理エラー**: APIログ、データベースの状態、外部サービスの応答を通じてトランザクションの失敗を調査
3. **パフォーマンス低下**: メトリクスの相関、リソース使用量、コード変更を通じて段階的な速度低下を分析

**最適な組み合わせ**: performance-engineer (パフォーマンス問題), security-engineer (セキュリティインシデント), quality-engineer (テスト失敗)

---

### quality-engineer ✅
**専門知識**: 自動化とカバレッジに焦点を当てた包括的なテスト戦略と品質保証

**自動起動**:
- キーワード: "test", "testing", "quality", "QA", "validation", "coverage", "automation"
- コンテキスト: テスト計画, 品質ゲート, 検証要件
- 品質懸念: コードカバレッジ < 80%, テスト自動化の欠如, 品質問題

**能力**:
- テスト戦略設計 (単体, 統合, E2E, パフォーマンステスト)
- テスト自動化フレームワークの実装とCI/CD統合
- 品質メトリクスの定義と監視 (カバレッジ, 欠陥率)
- エッジケースの特定と境界値テストのシナリオ
- アクセシビリティテストとコンプライアンス検証

**事例**:
1. **Eコマーステスト**: ユーザーフロー、支払い処理、在庫管理をカバーする包括的なテストスイート
2. **APIテスト**: REST/GraphQL APIの自動契約テスト、負荷テスト、セキュリティテスト
3. **アクセシビリティ検証**: 自動および手動のアクセシビリティ監査によるWCAG 2.1準拠テスト

**最適な組み合わせ**: security-engineer (セキュリティテスト), performance-engineer (負荷テスト), frontend-architect (UIテスト)

---

### refactoring-expert 🔧
**専門知識**: 体系的なリファクタリングと技術的負債管理によるコード品質の改善

**自動起動**:
- キーワード: "refactor", "clean code", "technical debt", "SOLID", "maintainability", "code smell"
- コンテキスト: レガシーコードの改善, アーキテクチャの更新, コード品質問題
- 品質指標: 高い複雑度, コードの重複, 低いテストカバレッジ

**能力**:
- SOLID原則の適用とデザインパターンの実装
- コードの匂いの特定と体系的な排除
- レガシーコードの近代化戦略と移行計画
- 技術的負債の評価と優先順位付けフレームワーク
- コード構造の改善とアーキテクチャのリファクタリング

**事例**:
1. **レガシーモダナイゼーション**: モノリシックなアプリケーションを、テスト容易性を向上させたモジュラーアーキテクチャに変換
2. **デザインパターン**: 支払い処理にStrategyパターンを実装し、結合度を下げて拡張性を向上
3. **コードクリーンアップ**: 重複コードの削除、命名規則の改善、再利用可能なコンポーネントの抽出

**最適な組み合わせ**: system-architect (アーキテクチャ改善), quality-engineer (テスト戦略), python-expert (言語固有パターン)

### 専門開発エージェント 🎯

### python-expert 🐍
**専門知識**: モダンなフレームワークとパフォーマンスを重視した本番環境対応のPython開発

**自動起動**:
- キーワード: "Python", "Django", "FastAPI", "Flask", "asyncio", "pandas", "pytest"
- ファイルタイプ: .py, requirements.txt, pyproject.toml, Pipfile
- コンテキスト: Python開発タスク, API開発, データ処理, テスト

**能力**:
- モダンなPythonアーキテクチャパターンとフレームワーク選択
- asyncioとconcurrent futuresによる非同期プログラミング
- プロファイリングとアルゴリズム改善によるパフォーマンス最適化
- pytest、フィクスチャ、テスト自動化によるテスト戦略
- pip、poetry、Dockerによるパッケージ管理とデプロイ

**事例**:
1. **FastAPIマイクロサービス**: Pydantic検証、依存性注入、OpenAPIドキュメントを備えた高性能非同期API
2. **データパイプライン**: エラーハンドリング、ロギング、大規模データセットの並列処理を備えたPandasベースのETL
3. **Djangoアプリケーション**: カスタムユーザーモデル、APIエンドポイント、包括的なテストカバレッジを備えたフルスタックWebアプリ

**最適な組み合わせ**: backend-architect (API設計), quality-engineer (テスト), performance-engineer (最適化)

---

### requirements-analyst 📝
**専門知識**: 体系的なステークホルダー分析による要求発見と仕様策定

**自動起動**:
- キーワード: "requirements", "specification", "PRD", "user story", "functional", "scope", "stakeholder"
- コンテキスト: プロジェクト開始, 不明瞭な要求, スコープ定義の必要性
- 複雑さ: 複数ステークホルダーのプロジェクト, 不明瞭な目標, 矛盾する要求

**能力**:
- ステークホルダーインタビューとワークショップによる要求引き出し
- 受け入れ基準と完了の定義を持つユーザーストーリーの作成
- 機能的および非機能的な仕様書の文書化
- ステークホルダー分析と要求の優先順位付けフレームワーク
- スコープ管理と変更管理プロセス

**事例**:
1. **製品要求仕様書(PRD)**: ユーザーペルソナ、機能仕様、成功指標を含むフィンテックモバイルアプリの包括的なPRD
2. **API仕様書**: エラーハンドリング、セキュリティ、パフォーマンス基準を含む支払い処理APIの詳細な要求
3. **移行要求**: データ移行、ユーザートレーニング、ロールバック手順を含むレガシーシステムの近代化要求

**最適な組み合わせ**: system-architect (技術的実現可能性), technical-writer (文書化), learning-guide (ユーザーガイダンス)

### コミュニケーション & 学習エージェント 📚

### technical-writer 📚
**専門知識**: 読者分析と明確さに焦点を当てた技術文書とコミュニケーション

**自動起動**:
- キーワード: "documentation", "readme", "API docs", "user guide", "technical writing", "manual"
- コンテキスト: 文書化要求, APIドキュメント, ユーザーガイド, 技術的説明
- ファイルタイプ: .md, .rst, API仕様書, 文書ファイル

**能力**:
- 技術文書のアーキテクチャと情報デザイン
- 異なるスキルレベルに対する読者分析とコンテンツターゲティング
- 実用的な例と統合ガイダンスを含むAPI文書化
- ステップバイステップの手順とトラブルシューティングを含むユーザーガイド作成
- アクセシビリティ基準の適用とインクルーシブな言語の使用

**事例**:
1. **APIドキュメント**: 認証、エンドポイント、例、SDK統合ガイドを含む包括的なREST APIドキュメント
2. **ユーザーマニュアル**: スクリーンショット、トラブルシューティング、FAQセクションを含むステップバイステップのインストール・設定ガイド
3. **技術仕様書**: ダイアグラム、データフロー、実装詳細を含むシステムアーキテクチャ文書

**最適な組み合わせ**: requirements-analyst (仕様の明確化), learning-guide (教育コンテンツ), frontend-architect (UI文書化)

---

### learning-guide 🎓
**専門知識**: スキル開発とメンターシップに焦点を当てた教育コンテンツデザインと段階的学習

**自動起動**:
- キーワード: "explain", "learn", "tutorial", "beginner", "teaching", "education", "training"
- コンテキスト: 教育的要求, 概念説明, スキル開発, 学習パス
- 複雑さ: ステップバイステップの分解と段階的な理解を必要とする複雑なトピック

**能力**:
- 段階的なスキル開発を伴う学習パスの設計
- 類推と例による複雑な概念の説明
- 実践的な演習を含むインタラクティブなチュートリアル作成
- スキル評価と能力評価フレームワーク
- メンターシップ戦略と個別化された学習アプローチ

**事例**:
1. **プログラミングチュートリアル**: 実践的な演習、コード例、段階的な複雑さを備えたインタラクティブなReactチュートリアル
2. **概念説明**: 現実世界の例、視覚的な図、練習問題を通してデータベースの正規化を説明
3. **スキル評価**: 実践的なプロジェクトとフィードバックによるフルスタック開発のための包括的な評価フレームワーク

**最適な組み合わせ**: technical-writer (教育文書), frontend-architect (インタラクティブ学習), requirements-analyst (学習目標)

---

## エージェントの調整と統合 🤝

### 調整パターン

**アーキテクチャチーム**:
- **フルスタック開発**: frontend-architect + backend-architect + security-engineer + quality-engineer
- **システム設計**: system-architect + devops-architect + performance-engineer + security-engineer
- **レガシーモダナイゼーション**: refactoring-expert + system-architect + quality-engineer + technical-writer

**品質チーム**:
- **セキュリティ監査**: security-engineer + quality-engineer + root-cause-analyst + requirements-analyst
- **パフォーマンス最適化**: performance-engineer + system-architect + devops-architect + root-cause-analyst
- **テスト戦略**: quality-engineer + security-engineer + performance-engineer + frontend-architect

**コミュニケーションチーム**:
- **ドキュメンテーションプロジェクト**: technical-writer + requirements-analyst + learning-guide + ドメイン専門家
- **学習プラットフォーム**: learning-guide + frontend-architect + technical-writer + quality-engineer
- **APIドキュメント**: backend-architect + technical-writer + security-engineer + quality-engineer

### MCPサーバー統合

**MCPサーバーによる強化された能力**:
- **Context7**: すべてのアーキテクトと専門家のための公式ドキュメントパターン
- **Sequential**: 根本原因アナリスト、システムアーキテクト、パフォーマンスエンジニアのためのマルチステップ分析
- **Magic**: フロントエンドアーキテクト、学習ガイドのインタラクティブコンテンツのためのUI生成
- **Playwright**: 品質エンジニアのためのブラウザテスト、フロントエンドアーキテクトのためのアクセシビリティ検証
- **Morphllm**: リファクタリングエキスパートのためのコード変換、Pythonエキスパートのための一括変更
- **Serena**: すべてのエージェントのプロジェクトメモリ、セッション間のコンテキスト保存

### エージェント起動のトラブルシューティング

## トラブルシューティング

トラブルシューティングのヘルプについては、以下を参照してください：
- [一般的な問題](../Reference-jp/common-issues.md) - よくある問題の簡単な修正
- [トラブルシューティングガイド](../Reference-jp/troubleshooting.md) - 包括的な問題解決

### 一般的な問題
- **エージェントが起動しない**: "security", "performance", "frontend" などのドメインキーワードを使用する
- **間違ったエージェントが選択される**: エージェントのドキュメントでトリガーキーワードを確認する
- **エージェントが多すぎる**: 主要なドメインにキーワードを集中させるか、`/sc:focus [domain]` を使用する
- **エージェントが連携しない**: タスクの複雑度を上げるか、複数ドメインのキーワードを使用する
- **エージェントの専門知識の不一致**: より具体的な技術用語を使用する

### 即時修正
- **エージェントの強制起動**: リクエストに明示的なドメインキーワードを使用する
- **エージェント選択のリセット**: エージェントの状態をリセットするためにClaude Codeセッションを再起動する
- **エージェントパターンの確認**: エージェントのドキュメントでトリガーキーワードを確認する
- **基本的な起動テスト**: `/sc:implement "security auth"` を試してsecurity-engineerをテストする

### エージェント固有のトラブルシューティング

**セキュリティエージェントがいない:**
```bash
# 問題: セキュリティに関する懸念がsecurity-engineerをトリガーしない
# 簡単な修正: 明示的なセキュリティキーワードを使用する
"implement authentication"              # 一般的 - トリガーしないかもしれない
"implement JWT authentication security" # 明示的 - security-engineerをトリガーする
"secure user login with encryption"    # セキュリティに焦点 - security-engineerをトリガーする
```

**パフォーマンスエージェントがいない:**
```bash
# 問題: パフォーマンス問題がperformance-engineerをトリガーしない
# 簡単な修正: パフォーマンス固有の用語を使用する
"make it faster"                       # 曖昧 - トリガーしないかもしれない
"optimize slow database queries"       # 具体的 - performance-engineerをトリガーする
"reduce API latency and bottlenecks"   # パフォーマンスに焦点 - performance-engineerをトリガーする
```

**アーキテクチャエージェントがいない:**
```bash
# 問題: システム設計がアーキテクチャエージェントをトリガーしない
# 簡単な修正: アーキテクチャ関連のキーワードを使用する
"build an app"                         # 一般的 - 基本的なエージェントをトリガーする
"design microservices architecture"    # 具体的 - system-architectをトリガーする
"scalable distributed system design"   # アーキテクチャに焦点 - system-architectをトリガーする
```

**間違ったエージェントの組み合わせ:**
```bash
# 問題: バックエンドのタスクにフロントエンドエージェントが表示される
# 簡単な修正: ドメイン固有の用語を使用する
"create user interface"                # frontend-architectをトリガーするかもしれない
"create REST API endpoints"            # 具体的 - backend-architectをトリガーする
"implement server-side authentication" # バックエンドに焦点 - backend-architectをトリガーする
```

### サポートレベル

**簡単な修正:**
- エージェントトリガーテーブルから明示的なドメインキーワードを使用する
- Claude Codeセッションの再起動を試す
- 混乱を避けるために単一のドメインに焦点を当てる

**詳細なヘルプ:**
- エージェントのインストール問題については、[一般的な問題ガイド](../Reference-jp/common-issues.md)を参照
- 対象エージェントのトリガーキーワードを確認する

**専門家によるサポート:**
- `SuperClaude install --diagnose` を使用する
- 連携分析については[診断リファレンスガイド](../Reference-jp/diagnostic-reference.md)を参照

**コミュニティサポート:**
- [GitHub Issues](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues)で問題を報告する
- 期待されるエージェント起動と実際のエージェント起動の例を含める

### 成功の検証

エージェントの修正を適用した後、以下でテストします：
- [ ] ドメイン固有のリクエストが正しいエージェントを起動する (security → security-engineer)
- [ ] 複雑なタスクがマルチエージェント連携をトリガーする (3+エージェント)
- [ ] エージェントの専門知識がタスク要件に一致する (API → backend-architect)
- [ ] 品質エージェントが適切な場合に自動的に含まれる (セキュリティ, パフォーマンス, テスト)
- [ ] 応答がドメインの専門知識と専門的な知識を示している

## クイックトラブルシューティング（レガシー）
- **エージェントが起動しない** → ドメインキーワードを使用: "security", "performance", "frontend"
- **間違ったエージェント** → エージェントのドキュメントでトリガーキーワードを確認
- **エージェントが多すぎる** → 主要なドメインにキーワードを集中させる
- **エージェントが連携しない** → タスクの複雑度を上げるか、複数ドメインのキーワードを使用する

**エージェントが起動しない？**
1. **キーワードを確認**: ドメイン固有の用語を使用する (例: security-engineerには "login" ではなく "authentication")
2. **コンテキストを追加**: ファイルタイプ、フレームワーク、または特定の技術を含める
3. **複雑度を上げる**: 複数ドメインの問題はより多くのエージェントをトリガーする
4. **例を使用**: エージェントの専門知識に一致する具体的なシナリオを参照する

**エージェントが多すぎる？**
- 主要なドメインのニーズにキーワードを集中させる
- スコープを制限するために `/sc:focus [domain]` を使用する
- 特定のエージェントから始め、必要に応じて拡張する

**間違ったエージェント？**
- エージェントのドキュメントでトリガーキーワードを確認する
- 対象ドメインに対してより具体的な用語を使用する
- 明示的な要求や制約を追加する

## クイックリファレンス 📋

### エージェントトリガー検索

| トリガータイプ | キーワード/パターン | 起動するエージェント |
|---|---|---|
| **セキュリティ** | "auth", "security", "vulnerability", "encryption" | security-engineer |
| **パフォーマンス** | "slow", "optimization", "bottleneck", "latency" | performance-engineer |
| **フロントエンド** | "UI", "React", "Vue", "component", "responsive" | frontend-architect |
| **バックエンド** | "API", "server", "database", "REST", "GraphQL" | backend-architect |
| **テスト** | "test", "QA", "validation", "coverage" | quality-engineer |
| **DevOps** | "deploy", "CI/CD", "Docker", "Kubernetes" | devops-architect |
| **アーキテクチャ** | "architecture", "microservices", "scalability" | system-architect |
| **Python** | ".py", "Django", "FastAPI", "asyncio" | python-expert |
| **問題** | "bug", "issue", "debugging", "troubleshoot" | root-cause-analyst |
| **コード品質** | "refactor", "clean code", "technical debt" | refactoring-expert |
| **ドキュメンテーション** | "documentation", "readme", "API docs" | technical-writer |
| **学習** | "explain", "tutorial", "beginner", "teaching" | learning-guide |
| **要求** | "requirements", "PRD", "specification" | requirements-analyst |

### コマンド-エージェントマッピング

| コマンド | 主要エージェント | サポートエージェント |
|---|---|---|
| `/sc:implement` | ドメインアーキテクト (フロントエンド, バックエンド) | security-engineer, quality-engineer |
| `/sc:analyze` | quality-engineer, security-engineer | performance-engineer, root-cause-analyst |
| `/sc:troubleshoot` | root-cause-analyst | ドメイン専門家, performance-engineer |
| `/sc:improve` | refactoring-expert | quality-engineer, performance-engineer |
| `/sc:document` | technical-writer | ドメイン専門家, learning-guide |
| `/sc:design` | system-architect | ドメインアーキテクト, requirements-analyst |
| `/sc:test` | quality-engineer | security-engineer, performance-engineer |
| `/sc:explain` | learning-guide | technical-writer, ドメイン専門家 |

### 効果的なエージェントの組み合わせ

**開発ワークフロー**:
- Webアプリケーション: frontend-architect + backend-architect + security-engineer + quality-engineer + devops-architect
- API開発: backend-architect + security-engineer + technical-writer + quality-engineer
- データプラットフォーム: python-expert + performance-engineer + security-engineer + system-architect

**分析ワークフロー**:
- セキュリティ監査: security-engineer + quality-engineer + root-cause-analyst + technical-writer
- パフォーマンス調査: performance-engineer + root-cause-analyst + system-architect + devops-architect
- レガシー評価: refactoring-expert + system-architect + quality-engineer + security-engineer + technical-writer

**コミュニケーションワークフロー**:
- 技術文書: technical-writer + requirements-analyst + ドメイン専門家 + learning-guide
- 教育コンテンツ: learning-guide + technical-writer + frontend-architect + quality-engineer

## ベストプラクティス 💡

### はじめての方へ (シンプルなアプローチ)

**まずは自然言語で:**
1. **目標を説明する**: ドメイン固有のキーワードを含む自然言語を使用する
2. **自動起動を信頼する**: システムが適切なエージェントに自動的にルーティングさせる
3. **パターンから学ぶ**: どのエージェントがどのリクエストタイプで起動するかを観察する
4. **反復と改善**: より専門的なエージェントを呼び出すために具体性を追加する

### エージェント選択の最適化

**効果的なキーワードの使用:**
- **具体的 > 一般的**: security-engineerには「login」ではなく「authentication」を使用する
- **技術用語**: フレームワーク名、技術、特定の課題を含める
- **コンテキストの手がかり**: ファイルタイプ、プロジェクトのスコープ、複雑さの指標に言及する
- **品質キーワード**: 包括的なカバレッジのために「security」、「performance」、「accessibility」を追加する

**リクエストの最適化例:**
```bash
# 一般的 (限定的なエージェント起動)
"Fix the login feature"

# 最適化済み (マルチエージェント連携)
"Implement secure JWT authentication with rate limiting and accessibility compliance"
# → トリガー: security-engineer + backend-architect + frontend-architect + quality-engineer
```

### 一般的な使用パターン

**開発ワークフロー:**
```bash
# フルスタック機能開発
/sc:implement "responsive user dashboard with real-time notifications"
# → frontend-architect + backend-architect + performance-engineer

# ドキュメント付きAPI開発
/sc:create "REST API for payment processing with comprehensive docs"
# → backend-architect + security-engineer + technical-writer + quality-engineer

# パフォーマンス最適化調査
/sc:troubleshoot "slow database queries affecting user experience"
# → performance-engineer + root-cause-analyst + backend-architect
```

**分析ワークフロー:**
```bash
# セキュリティ評価
/sc:analyze "authentication system for GDPR compliance vulnerabilities"
# → security-engineer + quality-engineer + requirements-analyst

# コード品質レビュー
/sc:review "legacy codebase for modernization opportunities"
# → refactoring-expert + system-architect + quality-engineer + technical-writer

# 学習と説明
/sc:explain "microservices patterns with hands-on examples"
# → system-architect + learning-guide + technical-writer
```

### 高度なエージェント連携

**複数ドメインのプロジェクト:**
- **広く始める**: システムレベルのキーワードで始めてアーキテクチャエージェントを呼び出す
- **具体性を追加**: ドメイン固有のニーズを含めて専門エージェントを起動する
- **品質統合**: セキュリティ、パフォーマンス、テストの観点を自動的に含める
- **ドキュメントの包含**: 包括的なカバレッジのために学習やドキュメントのニーズを追加する

**エージェント選択のトラブルシューティング:**

**問題: 間違ったエージェントが起動する**
- 解決策: より具体的なドメイン用語を使用する
- 例: "database optimization" → performance-engineer + backend-architect

**問題: エージェントが少なすぎる**
- 解決策: 複雑さの指標と複数ドメインのキーワードを増やす
- 例: リクエストに "security", "performance", "documentation" を追加する

**問題: エージェントが多すぎる**
- 解決策: 主要なドメインに特定の技術用語で焦点を合わせる
- 例: スコープを制限するために "/sc:focus backend" を使用する

### 品質駆動開発

**セキュリティ第一のアプローチ:**
開発リクエストには常にセキュリティに関する考慮事項を含め、ドメイン専門家と共にセキュリティエンジニアを自動的に呼び出します。

**パフォーマンス統合:**
パフォーマンス関連のキーワード（「fast」、「efficient」、「scalable」）を含め、最初からパフォーマンスエンジニアの連携を確保します。

**アクセシビリティ準拠:**
「accessible」、「WCAG」、「inclusive」を使用して、フロントエンド開発にアクセシビリティ検証を自動的に含めます。

**ドキュメンテーション文化:**
リクエストに「documented」、「explained」、「tutorial」を追加して、テクニカルライターの自動的な参加と知識移転を促します。

---

## エージェントの知能を理解する 🧠

### エージェントが効果的である理由

**ドメイン専門知識**: 各エージェントは、そのドメインに特化した専門知識パターン、振る舞いアプローチ、問題解決手法を持っています。

**コンテキストによる起動**: エージェントはキーワードだけでなく、リクエストのコンテキストを分析して関連性とエンゲージメントレベルを判断します。

**協調的知能**: マルチエージェントの連携は、個々のエージェントの能力を超える相乗効果を生み出します。

**適応学習**: エージェントの選択は、リクエストパターンと成功した連携結果に基づいて改善されます。

### エージェント vs 従来のAI

**従来のアプローチ**: 単一のAIが、さまざまな専門知識レベルですべてのドメインを処理する
**エージェントアプローチ**: 専門家が深いドメイン知識と集中的な問題解決で協力する

**利点**:
- ドメイン固有のタスクにおけるより高い精度
- より洗練された問題解決手法
- 専門家によるレビューによるより良い品質保証
- 調整された多角的な分析

### システムを信頼し、パターンを理解する

**期待されること**:
- 適切なドメイン専門家への自動ルーティング
- 複雑なタスクのためのマルチエージェント連携
- 自動QAエージェントの参加による品質統合
- 教育エージェントの起動による学習機会

**心配する必要がないこと**:
- 手動でのエージェント選択や設定
- 複雑なルーティングルールやエージェント管理
- エージェントの設定や連携
- エージェントの相互作用のマイクロマネジメント

---

## 関連リソース 📚

### 必須ドキュメント
- **[コマンドガイド](commands.md)** - 最適なエージェント連携をトリガーするSuperClaudeコマンドをマスターする
- **[MCPサーバー](mcp-servers.md)** - 専門ツール統合によるエージェント能力の強化
- **[セッション管理](session-management.md)** - 永続的なエージェントコンテキストを持つ長期ワークフロー

### 高度な使用法
- **[振る舞いモード](modes.md)** - 強化されたエージェント連携のためのコンテキスト最適化
- **[はじめに](../Getting-Started-jp/quick-start.md)** - エージェント最適化のための専門技術
- **[事例クックブック](../Reference-jp/examples-cookbook.md)** - 現実世界のエージェント連携パターン

### 開発リソース
- **[技術アーキテクチャ](../Developer-Guide-jp/technical-architecture.md)** - SuperClaudeのエージェントシステム設計を理解する
- **[貢献](../Developer-Guide-jp/contributing-code.md)** - エージェント能力と連携パターンの拡張

---

## あなたのエージェントとしての旅 🚀

**1週目: 自然な使用**
自然言語での説明から始めます。どのエージェントがなぜ起動するのかに気づきましょう。プロセスを考えすぎずに、キーワードパターンの直感を養います。

**2-3週目: パターン認識**
エージェントの連携パターンを観察します。複雑さとドメインキーワードがエージェント選択にどのように影響するかを理解します。より良い連携のためにリクエストの表現を最適化し始めます。

**2ヶ月目以降: エキスパート連携**
最適なエージェントの組み合わせをトリガーする複数ドメインのリクエストをマスターします。効果的なエージェント選択のためにトラブルシューティング技術を活用します。複雑なワークフローのために高度なパターンを使用します。

**SuperClaudeの利点:**
14人の専門AIエキスパートが連携して応答する力を、シンプルで自然な言語のリクエストを通じて体験してください。設定も管理も不要で、あなたのニーズに合わせてスケールするインテリジェントなコラボレーションです。

🎯 **インテリジェントなエージェント連携を体験する準備はできましたか？ `/sc:implement` から始めて、専門的なAIコラボレーションの魔法を発見してください。**