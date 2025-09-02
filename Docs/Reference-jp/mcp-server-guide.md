# MCPサーバー トラブルシューティングガイド

**MCPサーバーフォーカス**: モデルコンテキストプロトコル（MCP）サーバーは、ドキュメント検索（Context7）、UI生成（Magic）、高度な推論（Sequential）などの強化された機能を提供します。このガイドでは、すべてのMCPサーバーのインストール、設定、および運用上のトラブルシューティングについて説明します。

**サーバー固有の解決策**: 各MCPサーバーには固有の要件と一般的な障害パターンがあります。このガイドでは、各サーバータイプに対する対象を絞った解決策と、一般的なMCPトラブルシューティング戦略を提供します。

## MCPサーバーの概要

### 利用可能なMCPサーバー

**コアMCPサーバー:**
- **Context7**: 公式ドキュメントの検索とフレームワークパターン
- **Sequential**: マルチステップの推論と複雑な分析
- **Magic**: 21st.devのパターンに基づいた最新のUIコンポーネント生成
- **Playwright**: ブラウザ自動化とE2Eテスト
- **Morphllm**: トークン最適化を伴うパターンベースのコード編集
- **Serena**: セマンティックなコード理解とプロジェクトメモリ

**サーバー要件:**
- Node.js 16.0.0以上
- npmまたはyarnパッケージマネージャー
- 一部のサーバーには安定したネットワーク接続
- 十分なシステムメモリ（2GB以上推奨）

## インストールと設定の問題

### Node.jsとnpmの問題

#### 問題: Node.jsのバージョン非互換性
**エラーメッセージ**: `ERROR: MCP servers require Node.js 16+ but found Node.js 14.x`

**診断**:
```bash
node --version
npm --version
```

**解決策1**: Node.jsを更新 (Linux/Ubuntu)
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**解決策2**: Node Version Manager (nvm) を使用
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install node
nvm use node
```

**解決策3**: 手動でのNode.jsインストール
- https://nodejs.org/ からダウンロード
- プラットフォーム固有のインストール手順に従う

**検証**:
```bash
node --version  # 16.0.0以上であるべき
npm --version   # 8.0.0以上であるべき
```

**問題: npmのパーミッション問題**
```bash
# エラーメッセージ
ERROR: EACCES: permission denied, access '/usr/local/lib/node_modules'

# 解決策1: ユーザーディレクトリ用にnpmを設定
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
source ~/.profile

# 解決策2: npmのパーミッションを修正
sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}

# 解決策3: パッケージ実行にnpxを使用
npx @context7/mcp-server --version

# 検証
npm list -g --depth=0
npm config get prefix
```

### MCPサーバーのインストール失敗

**問題: Context7 MCPサーバーのインストール失敗**
```bash
# エラーメッセージ
ERROR: Failed to install @context7/mcp-server

# 診断
npm list -g @context7/mcp-server
node --version

# 解決策1: npmキャッシュをクリーンにして再インストール
npm cache clean --force
npm install -g @context7/mcp-server

# 解決策2: 代替レジストリを使用
npm install -g @context7/mcp-server --registry https://registry.npmjs.org/

# 解決策3: 手動でのインストール検証
npm info @context7/mcp-server
npm install -g @context7/mcp-server@latest

# 検証
npm list -g @context7/mcp-server
node -e "console.log('Context7 installation test')"
```

**問題: Sequential MCPサーバーの依存関係が不足**
```bash
# エラーメッセージ
ERROR: Sequential MCP server missing required dependencies

# 診断
npm list -g @sequential/mcp-server
npm list -g | grep -E "typescript|@types"

# 解決策1: 依存関係を明示的にインストール
npm install -g typescript @types/node
npm install -g @sequential/mcp-server

# 解決策2: 依存関係と共に強制再インストール
npm uninstall -g @sequential/mcp-server
npm install -g @sequential/mcp-server --save-dev

# 解決策3: パッケージの整合性を確認
npm audit --global
npm update -g

# 検証
npm list -g @sequential/mcp-server
```

**問題: Magic UIジェネレーターのインストール問題**
```bash
# エラーメッセージ
ERROR: @magic/ui-generator installation failed - build dependencies missing

# 診断
npm list -g @magic/ui-generator
which gcc make  # ビルドツールを確認

# 解決策1: ビルド依存関係をインストール (Linux)
sudo apt install build-essential python3-dev

# 解決策2: ビルド依存関係をインストール (macOS)
xcode-select --install

# 解決策3: 事前ビルド済みバイナリを使用
npm install -g @magic/ui-generator --ignore-scripts

# 検証
npm list -g @magic/ui-generator
```

## 接続と通信の問題

### MCPサーバーの接続失敗

**問題: Context7サーバーが接続できない**
```bash
# エラーメッセージ
ERROR: MCP server 'context7' failed to connect

# 診断
# Node.jsのインストールを確認
node --version  # 16.0.0以上であるべき
npm list -g @context7/mcp-server

# サーバー設定を確認
cat ~/.claude/CLAUDE.md | grep -i context7

# 解決策1: Claude Codeセッションを再起動
# MCPサーバーはClaude Codeセッションの再起動と共に再起動します

# 解決策2: MCPサーバーを再設定
python3 -m SuperClaude install --components mcp --force

# 解決策3: 手動でのサーバーテスト
node -e "console.log('Node.js working')"
npm test @context7/mcp-server

# 解決策4: ネットワーク接続を確認
ping context7-server.example.com  # サーバーがネットワークを必要とする場合
curl -I https://context7-api.example.com/health  # ヘルスチェック

# 検証
# Claude CodeでContext7の機能を試す
# ドキュメントリクエストに応答するはず
```

**問題: MCPサーバー通信タイムアウト**
```bash
# エラーメッセージ
ERROR: MCP server request timeout after 30 seconds

# 診断
# ネットワーク接続とサーバーの健全性を確認
ping 8.8.8.8  # 基本的な接続性
curl -I https://api.example.com/health  # APIヘルス

# システムリソースを確認
top
free -h

# 解決策1: 操作の複雑さを軽減
# 複雑なタスクを小さな部分に分割する

# 解決策2: Claude Codeセッションを再起動
# MCPサーバーはClaude Codeセッションの再起動と共に再起動します

# 解決策3: 問題のあるサーバーを一時的に無効化
# 操作に--no-mcpフラグを使用する

# 解決策4: タイムアウトを増やす (設定可能な場合)
# MCPサーバーの設定ファイルを確認する

# 検証
# まず簡単な操作でテストする
# 徐々に複雑さを増していく
```

**問題: 複数のMCPサーバーが競合**
```bash
# エラーメッセージ
ERROR: MCP server port conflicts detected

# 診断
netstat -tlnp | grep :8000  # ポート使用状況を確認
ps aux | grep -E "context7|sequential|magic"

# 解決策1: 逐次的なサーバー再起動
# Claude Codeを再起動してすべてのMCPサーバーをリセットする

# 解決策2: 異なるポートを設定
# MCPサーバーの設定ファイルを編集する
# 通常は~/.claude/またはサーバー固有のディレクトリにあります

# 解決策3: 選択的なサーバーアクティベーションを使用
# --all-mcpの代わりに特定のサーバーフラグを使用する

# 検証
netstat -tlnp | grep -E "8000|8001|8002"  # ポート割り当てを確認
```

## サーバー固有のトラブルシューティング

### Context7 ドキュメントサーバー

**問題: Context7がドキュメントを見つけられない**
```bash
# 症状: Context7は起動しているが、ドキュメントを返さない

# 診断
# Context7の接続をテスト
node -e "const c7 = require('@context7/mcp-server'); console.log('Context7 loaded');"

# 解決策1: Context7サーバーを更新
npm update -g @context7/mcp-server

# 解決策2: Context7のキャッシュをクリア
rm -rf ~/.context7/cache/  # キャッシュディレクトリが存在する場合

# 解決策3: 明示的なライブラリキーワードを使用
# リクエストに特定のフレームワーク名を含める

# 解決策4: インターネット接続を確認
curl -I https://docs.react.dev/  # APIテストの例

# 検証
# 特定のドキュメントリクエストを試す
# 関連するフレームワーク情報を返すはず
```

**問題: Context7が古い情報を返す**
```bash
# 症状: Context7が古いバージョンのドキュメントを返す

# 解決策1: Context7サーバーを更新
npm uninstall -g @context7/mcp-server
npm install -g @context7/mcp-server@latest

# 解決策2: ドキュメントキャッシュをクリア
rm -rf ~/.context7/  # キャッシュが存在する場合にクリア

# 解決策3: ドキュメントの強制リフレッシュ
# Claude Codeセッションを完全に再起動する

# 検証
# 応答のドキュメントの日付を確認する
# 現在のフレームワークバージョンを返すはず
```

### Sequential 推論サーバー

**問題: Sequentialサーバーの内部エラー**
```bash
# エラーメッセージ
ERROR: Sequential reasoning server encountered internal error

# 診断
# Sequentialサーバーのログを確認
tail -f ~/.claude/logs/sequential-mcp.log  # ログが存在する場合

# サーバーのインストールを確認
npm list -g @sequential/mcp-server

# 解決策1: Claude Codeセッションを再起動
# これによりSequentialを含むすべてのMCPサーバーが再起動します

# 解決策2: 代替の推論アプローチを使用
# MCPサーバーなしでネイティブのClaude推論を使用する

# 解決策3: Sequential MCPを再インストール
npm uninstall -g @sequential/mcp-server
npm install -g @sequential/mcp-server@latest

# 解決策4: メモリの空き容量を確認
free -h  # 複雑な推論に十分なメモリがあることを確認

# 検証
# まず簡単な分析タスクでテストする
# 構造化された推論出力を提供するはず
```

**問題: Sequentialサーバーのメモリ過負荷**
```bash
# 症状: Sequentialサーバーがクラッシュまたは無応答になる

# 診断
top | grep -E "sequential|node"
free -h

# 解決策1: 分析の複雑さを軽減
# 複雑な問題を小さな部分に分割する

# 解決策2: システムメモリまたはスワップを増やす
sudo swapon --show  # スワップの状態を確認

# 解決策3: スコープ制限を使用
# 分析を特定のコンポーネントに集中させる

# 検証
ps aux | grep sequential  # プロセスの状態を確認
```

### Magic UIジェネレーター

**問題: MagicがUIコンポーネントを生成しない**
```bash
# 症状: UIコンポーネントのリクエストが期待される出力を生成しない

# 診断
# Magicサーバーのインストールを確認
npm list -g @magic/ui-generator
cat ~/.claude/CLAUDE.md | grep -i magic

# 解決策1: Magicサーバーのインストールを検証
npm list -g @magic/ui-generator
npm install -g @magic/ui-generator@latest

# 解決策2: 明示的なMagicのアクティベーションを使用
# "component", "UI", "interface"などのキーワードを含める

# 解決策3: コンポーネントリクエストの形式を確認
# より良いMagicの起動のために、説明的なリクエストを使用する

# 解決策4: Magicサーバーを直接テスト
node -e "const magic = require('@magic/ui-generator'); console.log('Magic loaded');"

# 検証
# 最新のパターンを持つ完全なUIコンポーネントを生成するはず
```

**問題: Magicコンポーネントがフレームワークに準拠していない**
```bash
# 症状: 生成されたコンポーネントがフレームワークのパターンと一致しない

# 解決策1: フレームワーク固有のキーワードを使用
# リクエストに"React", "Vue", "Angular"を含める

# 解決策2: Context7と組み合わせる
# フレームワーク準拠のコンポーネントのためにMagicとContext7の両方を使用する

# 解決策3: Magicサーバーを更新
npm update -g @magic/ui-generator

# 検証
# 生成されたコンポーネントはフレームワークの慣習に従うべき
```

### Playwright ブラウザ自動化

**問題: Playwrightブラウザのインストール失敗**
```bash
# エラーメッセージ
ERROR: Playwright browser automation failed - browser not installed

# 診断
npm list -g playwright
npx playwright --version

# 解決策1: Playwrightブラウザをインストール
npx playwright install
npx playwright install-deps

# 解決策2: 特定のブラウザをインストール
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit

# 解決策3: ブラウザの依存関係を修正 (Linux)
sudo apt-get install libnss3 libatk-bridge2.0-0 libdrm2 libgtk-3-0

# 検証
npx playwright --version
ls ~/.cache/ms-playwright/  # ブラウザのインストールを確認
```

**問題: Playwrightブラウザの起動失敗**
```bash
# エラーメッセージ
ERROR: Browser launch failed - display not available

# 診断
echo $DISPLAY  # X11ディスプレイを確認
ps aux | grep Xvfb  # 仮想ディスプレイを確認

# 解決策1: ヘッドレスモードを使用
# Playwright設定でheadless: trueを設定

# 解決策2: 仮想ディスプレイをインストール (Linux)
sudo apt-get install xvfb
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &

# 解決策3: ブラウザテストにDockerを使用
docker run -it --rm playwright:latest

# 検証
# ヘッドレスモードでブラウザを正常に起動するはず
```

### Morphllm パターンエディタ

**問題: Morphllmのパターン適用失敗**
```bash
# 症状: パターンベースの編集が正しく適用されない

# 診断
npm list -g @morphllm/mcp-server

# 解決策1: Morphllmサーバーを更新
npm update -g @morphllm/mcp-server

# 解決策2: より具体的なパターンを使用
# 明示的なパターンの説明を提供する

# 解決策3: ファイルパーミッションを確認
ls -la target-files/  # 書き込み権限を確認

# 検証
# パターン編集はファイル間で一貫して適用されるべき
```

### Serena プロジェクトメモリ

**問題: Serenaのセッション永続化失敗**
```bash
# 症状: プロジェクトコンテキストがセッション間で永続化されない

# 診断
ls ~/.claude/sessions/  # セッションストレージを確認
ls ~/.serena/  # Serena固有のストレージを確認

# 解決策1: セッション保存操作を検証
# 閉じる前に適切なセッション保存を確認

# 解決策2: ストレージのパーミッションを確認
ls -la ~/.claude/sessions/
chmod 755 ~/.claude/sessions/

# 解決策3: Serenaサーバーを再インストール
npm uninstall -g @serena/mcp-server
npm install -g @serena/mcp-server@latest

# 検証
# セッションコンテキストはClaude Codeの再起動後も永続化されるべき
```

## パフォーマンスと最適化

### MCPサーバーのパフォーマンス問題

**問題: MCPサーバーの応答時間が遅い**
```bash
# 症状: MCPサーバーの操作が遅延を引き起こす

# 診断
# MCPサーバーのインストールと健全性を確認
npm list -g | grep -E "context7|sequential|magic|playwright"
top | grep node

# 解決策1: 選択的なMCPサーバーの使用
# 特定のタスクに必要なサーバーのみを使用する

# 解決策2: Claude Codeセッションを再起動
# これによりすべてのMCPサーバーが新規に再起動します

# 解決策3: ローカルフォールバックモード
# 純粋なネイティブ操作のために--no-mcpフラグを使用する

# 解決策4: すべてのMCPサーバーを更新
npm update -g

# 検証
time node -e "console.log('Node.js speed test')"
# 正常に完了するはず
```

**問題: MCPサーバーのメモリリーク**
```bash
# 症状: 時間の経過とともにメモリ使用量が増加する

# 診断
top | grep node  # Node.jsプロセスを監視
ps aux --sort=-%mem | head -10

# 解決策1: 定期的なClaude Codeセッションの再起動
# 重い使用中に定期的にセッションを再起動する

# 解決策2: 特定のサーバーを監視
htop  # 個々のMCPサーバープロセスを監視

# 解決策3: メモリ効率の良いパターンを使用
# MCPサーバーメモリに大きなデータセットを保持しない

# 検証
free -h  # メモリ使用量の傾向を監視
```

### リソース管理

**問題: 複数のMCPサーバーがリソースを競合**
```bash
# 症状: 複数のサーバーがアクティブなときにシステムが遅くなる

# 診断
top | grep -E "node|mcp"
iostat 1 3  # I/O使用状況を確認

# 解決策1: 対象を絞ったサーバーアクティベーションを使用
# タスクごとに必要なサーバーのみをアクティブにする

# 解決策2: システムリソースを増やす
# 可能であればRAMやCPUコアを追加する

# 解決策3: MCP操作をキューに入れる
# 同時に重い操作を避ける

# 解決策4: MCPサーバーの優先順位を使用
# MCP設定でリソース割り当てを設定する

# 検証
top  # 操作中のリソース使用状況を監視
```

## 高度なMCP設定

### カスタムMCPサーバー設定

**問題: デフォルトのMCP設定が最適でない**
```bash
# 症状: MCPサーバーが特定のユースケースで最適に動作しない

# 解決策1: 設定ファイルを見つける
find ~/.claude/ -name "*mcp*" -type f
find ~/.config/ -name "*mcp*" -type f

# 解決策2: サーバー設定をカスタマイズ
# サーバー固有の設定ファイルを編集する
# 一般的な場所: ~/.claude/mcp-config.json

# 解決策3: 環境変数による設定
export MCP_CONTEXT7_TIMEOUT=60
export MCP_SEQUENTIAL_MEMORY_LIMIT=2048

# 検証
# カスタム設定でテストする
# 特定のユースケースでパフォーマンスが向上するはず
```

**問題: MCPサーバーのロードバランシング**
```bash
# 症状: MCPサーバー間で負荷が不均等に分散される

# 解決策1: サーバーの優先順位を設定
# 負荷を分散するためにMCP設定を編集する

# 解決策2: ラウンドロビンサーバー選択を使用
# サーバー呼び出しでローテーションロジックを実装する

# 解決策3: サーバーのパフォーマンスを監視
# 応答時間を追跡し、それに応じて調整する

# 検証
# サーバー間でリソース使用量が均等になることを観察する
```

## デバッグと診断

### MCPサーバーの健全性監視

**包括的なMCPヘルスチェック:**
```bash
# MCPサーバーシステム診断
echo "=== MCPサーバーヘルスチェック ==="

# Node.js環境
echo "Node.jsバージョン: $(node --version)"
echo "npmバージョン: $(npm --version)"

# サーバーのインストール
echo "=== インストール済みMCPサーバー ==="
npm list -g | grep -E "context7|sequential|magic|playwright|morphllm|serena"

# 実行中のMCPプロセス
echo "=== 実行中のMCPプロセス ==="
ps aux | grep -E "node.*mcp|mcp.*server" | head -5

# リソース使用状況
echo "=== リソース使用状況 ==="
echo "メモリ: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo "CPU負荷: $(uptime | awk -F'load average:' '{print $2}')"

# ネットワーク接続 (必要な場合)
echo "=== ネットワークステータス ==="
ping -c 1 8.8.8.8 > /dev/null && echo "✅ ネットワークOK" || echo "❌ ネットワーク問題"
```

**MCPサーバー機能テスト:**
```bash
# 各MCPサーバーを個別にテスト
echo "=== MCPサーバー機能テスト ==="

# Context7テスト
if npm list -g @context7/mcp-server > /dev/null 2>&1; then
    echo "✅ Context7はインストールされています"
else
    echo "❌ Context7が見つかりません"
fi

# Sequentialテスト
if npm list -g @sequential/mcp-server > /dev/null 2>&1; then
    echo "✅ Sequentialはインストールされています"
else
    echo "❌ Sequentialが見つかりません"
fi

# Magicテスト
if npm list -g @magic/ui-generator > /dev/null 2>&1; then
    echo "✅ Magicはインストールされています"
else
    echo "❌ Magicが見つかりません"
fi

# Playwrightテスト
if npx playwright --version > /dev/null 2>&1; then
    echo "✅ Playwrightはインストールされています"
else
    echo "❌ Playwrightが見つかりません"
fi
```

### MCPサーバーログ分析

**ログ収集と分析:**
```bash
# MCPサーバーログを収集
echo "=== MCPサーバーログ ==="

# 一般的なログの場所を確認
find ~/.claude/ -name "*.log" -type f 2>/dev/null
find /tmp/ -name "*mcp*.log" -type f 2>/dev/null
find /var/log/ -name "*mcp*.log" -type f 2>/dev/null

# npmログを確認
npm config get logs-max
ls ~/.npm/_logs/ 2>/dev/null | tail -5

# Node.jsプロセスのシステムログ
journalctl -u node* --since "1 hour ago" 2>/dev/null | tail -10
```

## 緊急復旧

### 完全なMCPリセット

**完全なMCPサーバーリセット手順:**
```bash
# 緊急MCPリセット
echo "=== 緊急MCPサーバーリセット ==="

# ステップ1: すべてのClaude Codeセッションを停止
echo "すべてのClaude Codeセッションを停止し、30秒待ってください"

# ステップ2: 現在の状態をバックアップ
cp -r ~/.claude ~/.claude.mcp.backup.$(date +%Y%m%d)

# ステップ3: すべてのMCPサーバーを削除
npm list -g | grep -E "context7|sequential|magic|playwright|morphllm|serena" | awk '{print $2}' | xargs npm uninstall -g

# ステップ4: npmキャッシュをクリア
npm cache clean --force

# ステップ5: MCPサーバーを再インストール
python3 -m SuperClaude install --components mcp --force

# ステップ6: 検証
npm list -g | grep -E "context7|sequential|magic|playwright|morphllm|serena"

# ステップ7: 機能テスト
echo "再起動後にClaude CodeでMCPサーバーをテストしてください"
```

## 関連リソース

### MCP固有のドキュメント
- **コアSuperClaudeガイド**: [../User-Guide/mcp-servers.md](../User-Guide-jp/mcp-servers.md) - MCPサーバーの概要と使用法
- **一般的な問題**: [common-issues.md](./common-issues.md) - 一般的なトラブルシューティング手順
- **診断リファレンス**: [diagnostic-reference.md](./diagnostic-reference.md) - 高度な診断手順

### 外部リソース
- **Node.js公式**: [https://nodejs.org/](https://nodejs.org/) - Node.jsのインストールとドキュメント
- **npmドキュメント**: [https://docs.npmjs.com/](https://docs.npmjs.com/) - パッケージマネージャのドキュメント
- **Playwrightガイド**: [https://playwright.dev/](https://playwright.dev/) - ブラウザ自動化ドキュメント

### サポートチャネル
- **GitHub Issues**: [MCP固有の問題](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues)
- **GitHub Discussions**: [MCPサーバーコミュニティサポート](https://github.com/SuperClaude-Org/SuperClaude_Framework/discussions)

---

**MCPサーバーの優先順位**: トラブルシューティングの際は、依存関係の順にサーバーに対処してください: Node.js → npm → 個々のサーバー → Claude Code統合。ほとんどのMCPの問題は、適切なNode.jsのセットアップとサーバーの再インストールで解決します。

**検証パターン**: MCPの解決策の後、常に以下で検証してください:
- ✅ `node --version` - 16.0.0以上であるべき
- ✅ `npm list -g | grep mcp` - インストール済みのサーバーが表示されるべき
- ✅ Claude Codeでサーバーの機能をテスト - エラーなしで応答するべき
