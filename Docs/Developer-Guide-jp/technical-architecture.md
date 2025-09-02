# SuperClaude コンテキストアーキテクチャガイド

## 概要

このガイドは、SuperClaudeのコンテキスト指向設定フレームワークがどのように構造化され、Claude Codeがこれらのコンテキストファイルを解釈してその振る舞いを変更する方法を文書化します。

**重要**: SuperClaudeは、実行中のプロセス、実行レイヤー、またはパフォーマンスシステムを持つスタンドアロンのソフトウェアではありません。これは、Claude Codeが専門的な振る舞いを採用するために読み込む`.md`指示ファイルのコレクションです。

## 目次

1. [コンテキストファイルアーキテクチャ](#コンテキストファイルアーキテクチャ)
2. [インポートシステム](#インポートシステム)
3. [エージェントコンテキスト構造](#エージェントコンテキスト構造)
4. [コマンドコンテキスト構造](#コマンドコンテキスト構造)
5. [モードコンテキスト構造](#モードコンテキスト構造)
6. [MCPサーバー設定](#mcpサーバー設定)
7. [Claude Codeがコンテキストを読み込む方法](#claude-codeがコンテキストを読み込む方法)
8. [フレームワークの拡張](#フレームワークの拡張)

## コンテキストファイルアーキテクチャ

### ディレクトリ構造

```
~/.claude/ (SuperClaudeフレームワークファイルのみ)
├── CLAUDE.md                       # インポートを含むメインコンテキストファイル
├── FLAGS.md                        # フラグ定義とトリガー
├── RULES.md                        # コアな振る舞いのルール
├── PRINCIPLES.md                   # 指導原則
├── ZIG.md                          # Zig言語統合
├── MCP_Context7.md                 # Context7 MCP統合
├── MCP_Magic.md                    # Magic MCP統合
├── MCP_Morphllm.md                 # Morphllm MCP統合
├── MCP_Playwright.md               # Playwright MCP統合
├── MCP_Sequential.md               # Sequential MCP統合
├── MCP_Serena.md                   # Serena MCP統合
├── MCP_Zig.md                      # Zig MCP統合
├── MODE_Brainstorming.md           # 協調的発見モード
├── MODE_Introspection.md           # 透明な推論モード
├── MODE_Orchestration.md           # ツール調整モード
├── MODE_Task_Management.md         # タスク調整モード
├── MODE_Token_Efficiency.md        # 圧縮通信モード
├── agents/                         # ドメイン専門家コンテキスト (合計14)
│   ├── backend-architect.md        # バックエンド専門知識
│   ├── devops-architect.md         # DevOps専門知識
│   ├── frontend-architect.md       # フロントエンド専門知識
│   ├── learning-guide.md           # 教育専門知識
│   ├── performance-engineer.md     # パフォーマンス専門知識
│   ├── python-expert.md            # Python専門知識
│   ├── quality-engineer.md         # 品質保証専門知識
│   ├── refactoring-expert.md       # コード品質専門知識
│   ├── requirements-analyst.md     # 要件専門知識
│   ├── root-cause-analyst.md       # 問題診断専門知識
│   ├── security-engineer.md        # セキュリティ専門知識
│   ├── socratic-mentor.md          # 教育専門知識
│   ├── system-architect.md         # システム設計専門知識
│   └── technical-writer.md         # ドキュメンテーション専門知識
└── commands/                       # ワークフローパターンコンテキスト
    └── sc/                         # SuperClaudeコマンド名前空間 (合計21)
        ├── analyze.md              # 分析パターン
        ├── brainstorm.md           # 発見パターン
        ├── build.md                # ビルドパターン
        ├── cleanup.md              # クリーンアップパターン
        ├── design.md               # 設計パターン
        ├── document.md             # ドキュメンテーションパターン
        ├── estimate.md             # 見積もりパターン
        ├── explain.md              # 説明パターン
        ├── git.md                  # Gitワークフローパターン
        ├── implement.md            # 実装パターン
        ├── improve.md              # 改善パターン
        ├── index.md                # インデックスパターン
        ├── load.md                 # コンテキスト読み込みパターン
        ├── reflect.md              # 内省パターン
        ├── save.md                 # セッション永続化パターン
        ├── select-tool.md          # ツール選択パターン
        ├── spawn.md                # マルチエージェントパターン
        ├── task.md                 # タスク管理パターン
        ├── test.md                 # テストパターン
        ├── troubleshoot.md         # トラブルシューティングパターン
        └── workflow.md             # ワークフロー計画パターン

注意: 他のディレクトリ (backups/, logs/, projects/, serena/など) はClaude Codeの運用ディレクトリであり、SuperClaudeフレームワークのコンテンツの一部ではありません。
```

### コンテキストファイルの種類

| ファイルの種類 | 目的 | アクティベーション | 例 |
|-----------|---------|------------|---------|
| **コマンド** | ワークフローパターンを定義 | `/sc:[command]` (コンテキストトリガー) | ユーザーが`/sc:implement`と入力 → `implement.md`を読む |
| **エージェント** | ドメイン専門知識を提供 | `@agent-[name]` または自動 | `@agent-security` → `security-engineer.md`を読む |
| **モード** | 対話スタイルを変更 | フラグまたはトリガー | `--brainstorm` → ブレインストーミングモードを有効化 |
| **コア** | 基本的なルールを設定 | 常にアクティブ | `RULES.md`は常に読み込まれる |

## インポートシステム

### CLAUDE.mdの仕組み

メインの`CLAUDE.md`ファイルは、インポートシステムを使用して複数のコンテキストファイルを読み込みます。

```markdown
# CLAUDE

*MANDATORY*
@FLAGS.md                  # フラグ定義とトリガー
@RULES.md                  # コアな振る舞いのルール
@PRINCIPLES.md             # 指導原則
*SECONDARY*
@MCP_Context7.md           # Context7 MCP統合
@MCP_Magic.md              # Magic MCP統合
@MCP_Morphllm.md           # Morphllm MCP統合
@MCP_Playwright.md         # Playwright MCP統合
@MCP_Sequential.md         # Sequential MCP統合
@MCP_Serena.md             # Serena MCP統合
@MCP_Zig.md                # Zig MCP統合
*CRITICAL*
@MODE_Brainstorming.md     # 協調的発見モード
@MODE_Introspection.md     # 透明な推論モード
@MODE_Task_Management.md   # タスク調整モード
@MODE_Orchestration.md     # ツール調整モード
@MODE_Token_Efficiency.md  # 圧縮通信モード
*LANGUAGE SPECIFIC*
@ZIG.md                    # Zig言語統合
```

### インポート処理

1. Claude Codeが`CLAUDE.md`を読み込む
2. `@import`文に遭遇する
3. 参照されているファイルをコンテキストに読み込む
4. 完全な振る舞いのフレームワークを構築する
5. ユーザー入力に基づいて関連するコンテキストを適用する

## エージェントコンテキスト構造

### エージェントファイルの解剖学

各エージェントの`.md`ファイルはこの構造に従います。

```markdown
---
name: agent-name
description: 簡単な説明
category: specialized|architecture|quality
tools: Read, Write, Edit, Bash, Grep
---

# エージェント名

## トリガー
- このエージェントをアクティブにするキーワード
- アクティベーションをトリガーするファイルタイプ
- 複雑さのしきい値

## 振る舞いのマインドセット
中核となる哲学とアプローチ

## フォーカスエリア
- ドメイン専門知識エリア1
- ドメイン専門知識エリア2

## 主要なアクション
1. 特定の振る舞いパターン
2. 問題解決アプローチ
```

### エージェントのアクティベーションロジック

- **手動**: ユーザーが`@agent-python-expert "task"`と入力
- **自動**: リクエスト内のキーワードがエージェントの読み込みをトリガー
- **文脈的**: ファイルタイプやパターンが関連するエージェントをアクティブにする

## コマンドコンテキスト構造

### コマンドファイルの解剖学

```markdown
---
name: command-name
description: コマンドの目的
category: utility|orchestration|analysis
complexity: basic|enhanced|advanced
mcp-servers: [context7, sequential]
personas: [architect, engineer]
---

# /sc:command-name

## トリガー
- このコマンドを使用するタイミング
- コンテキスト指標

## 使用法
/sc:command-name [target] [--options]

## ワークフローパターン
1. ステップ1: 初期アクション
2. ステップ2: 処理
3. ステップ3: 検証

## 例
実用的な使用例
```

### コマンド処理

ユーザーがClaude Codeの会話で`/sc:implement "feature"`と入力した場合:
1. Claudeが`commands/sc/implement.md`を読み込む
2. 実装ワークフローパターンを採用する
3. 関連するエージェントを自動的にアクティブにする可能性がある
4. 定義されたワークフローのステップに従う

## モードコンテキスト構造

### 振る舞いモード

モードはClaudeの対話スタイルを変更します。

```markdown
# MODE_[Name].md

## アクティベーショントリガー
- フラグ: --mode-name
- キーワード: [triggers]
- 複雑さ: しきい値

## 振る舞いの変更
- コミュニケーションスタイルの変更
- 意思決定の調整
- 出力フォーマットの変更

## 対話パターン
- どのように応答するか
- 何を優先するか
```

## MCPサーバー設定

### 設定場所

MCPサーバーは`~/.claude.json`で設定されます（SuperClaudeコンテキストの一部ではありません）。

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "sequential-thinking-mcp@latest"]
    }
  }
}
```

### MCP統合

- **MCPサーバー**: ツールを提供する実際のソフトウェア
- **SuperClaude**: Claudeにいつそれらを使用するかを伝えるコンテキスト
- **アクティベーション**: フラグやキーワードがMCPの使用をトリガー

## Claude Codeがコンテキストを読み込む方法

### コンテキスト読み込みシーケンス

```
ユーザー入力 (Claude Code内): "/sc:analyze src/ --focus security"
                    ↓
1. コマンド解析: 'analyze'コマンドを特定
                    ↓
2. コンテキスト読み込み: commands/sc/analyze.mdを読む
                    ↓
3. フラグ確認: --focus security
                    ↓
4. 自動アクティベーション: security-engineer.mdを読み込む
                    ↓
5. パターン適用: 分析ワークフローに従う
                    ↓
6. 出力生成: 読み込まれたコンテキストを使用
```

### コンテキストの優先順位

1. **明示的なコマンド**: `/sc:`コマンドが優先される
2. **手動エージェント**: `@agent-`が自動アクティベーションを上書きする
3. **フラグ**: コマンド/エージェントの振る舞いを変更する
4. **自動アクティベーション**: キーワード/コンテキストに基づく
5. **デフォルトの振る舞い**: 標準のClaude Code

## フレームワークの拡張

### 新しいコマンドの追加

1. `~/.claude/commands/sc/new-command.md`を作成する
2. メタデータ、トリガー、ワークフローを定義する
3. コードの変更は不要 - コンテキストのみ

### 新しいエージェントの追加

1. `~/.claude/agents/new-specialist.md`を作成する
2. 専門知識、トリガー、振る舞いを定義する
3. エージェントが利用可能になる

### 新しいモードの追加

1. `~/.claude/MODE_NewMode.md`を作成する
2. アクティベーショントリガーと変更点を定義する
3. モードがトリガーに基づいてアクティブになる

### ベストプラクティス

- **コンテキストを集中させる**: 1つのファイルに1つの概念
- **明確なトリガー**: コンテキストがいつアクティブになるかを定義する
- **ワークフローパターン**: ステップバイステップのガイダンスを提供する
- **例**: 実用的な使用例を含める
- **メタデータ**: 設定にはフロントマターを使用する

## 重要な明確化

### SuperClaudeが「そうではない」もの

- ❌ **実行エンジンではない**: コードは実行されず、プロセスも実行されない
- ❌ **パフォーマンスシステムではない**: 最適化は不可能（ただのテキスト）
- ❌ **検出エンジンではない**: Claude Codeはパターンマッチングを行う
- ❌ **オーケストレーションレイヤーではない**: コンテキストファイルはガイドするだけで、制御はしない
- ❌ **品質ゲートではない**: 指示的なパターンにすぎない

### SuperClaudeが「そうである」もの

- ✅ **コンテキストファイル**: Claude Codeのための`.md`指示
- ✅ **振る舞いパターン**: ワークフローとアプローチ
- ✅ **ドメイン専門知識**: 専門知識のコンテキスト
- ✅ **設定**: 実際のツール（MCP）の設定
- ✅ **フレームワーク**: 構造化されたプロンプトエンジニアリング

## まとめ

SuperClaudeのアーキテクチャは意図的にシンプルです。それは、Claude Codeがその振る舞いを変更するために読み込む、よく整理されたコンテキストファイルのコレクションです。その力は、実行されるコードや実行中のプロセスからではなく、これらのコンテキストの慎重な作成と体系的な編成から生まれます。

フレームワークの優雅さはそのシンプルさにあります - コンテキストファイルを通じてClaude Codeに構造化された指示を提供することで、ソフトウェアの複雑さなしに洗練された振る舞いの変更を達成できます。
