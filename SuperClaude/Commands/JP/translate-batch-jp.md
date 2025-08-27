---
name: translate-batch
description: "プロジェクト内のすべてのターゲットファイルをバッチ操作で翻訳"
category: workflow
complexity: advanced
personas: [translation-agent-jp]
---

# /sc:translate-batch - プロジェクトファイルのバッチ翻訳

> **コンテキスト フレームワーク ノート**: このコマンドは、指定されたすべてのドキュメントと構成ファイルを体系的に日本語に翻訳します。

## 使用法
```
/sc:translate-batch [--dry-run]
```
**使用方法**: 引数なしで実行すると、すべてのターゲットファイルが翻訳されます。`--dry-run` を使用すると、翻訳対象ファイルをリストするだけで、実際には翻訳を実行しません。

## 動作フロー
1. **ファイル検出**: `find_by_name`でターゲットパターンに一致するすべてのファイルを識別
    - **ターゲット**: `README.md`、`Docs/**/*.md`、`SuperClaude/Commands/**/*.md`
    - **除外**: `scripts/`、`bin/`、`.github/`、`*.py`、`*.js`
2. **ドライラン処理**: `--dry-run`指定時は検出ファイル一覧表示で停止
3. **ペルソナ活性化**: `translation-agent-jp`ペルソナを呼び出し
4. **並列実行**: 検出された全ファイルの翻訳をエージェントに指示（効率化のため並列化）
5. **サマリー**: 翻訳ファイル数、エラー、翻訳ログ場所を報告

## 例

### 翻訳対象確認用ドライラン実行
```
/sc:translate-batch --dry-run
```

### 完全バッチ翻訳実行
```
/sc:translate-batch
```