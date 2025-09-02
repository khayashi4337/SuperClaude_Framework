#!/usr/bin/env python3
"""
SuperClaude フレームワーク管理ハブ
すべてのSuperClaude操作の統一エントリポイント

使用法:
    SuperClaude install [options]
    SuperClaude update [options]
    SuperClaude uninstall [options]
    SuperClaude backup [options]
    SuperClaude --help
"""

import sys
import argparse
import subprocess
import difflib
from pathlib import Path
from typing import Dict, Callable

# Add the local 'setup' directory to the Python import path
current_dir = Path(__file__).parent
project_root = current_dir.parent
setup_dir = project_root / "setup"

# Insert the setup directory at the beginning of sys.path
if setup_dir.exists():
    sys.path.insert(0, str(setup_dir.parent))
else:
    print(f"警告: セットアップディレクトリが見つかりません: {setup_dir}")
    sys.exit(1)


# Try to import utilities from the setup package
try:
    from setup.utils.ui import (
        display_header, display_info, display_success, display_error,
        display_warning, Colors
    )
    from setup.utils.logger import setup_logging, get_logger, LogLevel
    from setup import DEFAULT_INSTALL_DIR
except ImportError:
    # Provide minimal fallback functions and constants if imports fail
    class Colors:
        RED = YELLOW = GREEN = CYAN = RESET = ""

    def display_error(msg): print(f"[ERROR] {msg}")
    def display_warning(msg): print(f"[WARN] {msg}")
    def display_success(msg): print(f"[OK] {msg}")
    def display_info(msg): print(f"[INFO] {msg}")
    def display_header(title, subtitle): print(f"{title} - {subtitle}")
    def get_logger(): return None
    def setup_logging(*args, **kwargs): pass
    class LogLevel:
        ERROR = 40
        INFO = 20
        DEBUG = 10


def create_global_parser() -> argparse.ArgumentParser:
    """すべてのコマンドで使用されるグローバルフラグの共有パーサーを作成"""
    global_parser = argparse.ArgumentParser(add_help=False)

    global_parser.add_argument("--verbose", "-v", action="store_true",
                               help="詳細ロギングを有効にする")
    global_parser.add_argument("--quiet", "-q", action="store_true",
                               help="エラー以外のすべての出力を抑制")
    global_parser.add_argument("--install-dir", type=Path, default=DEFAULT_INSTALL_DIR,
                               help=f"ターゲットインストールディレクトリ (デフォルト: {DEFAULT_INSTALL_DIR})")
    global_parser.add_argument("--dry-run", action="store_true",
                               help="変更を加えずに操作をシミュレート")
    global_parser.add_argument("--force", action="store_true",
                               help="チェックをスキップして実行を強制")
    global_parser.add_argument("--yes", "-y", action="store_true",
                               help="すべてのプロンプトに自動的に「はい」と答える")
    global_parser.add_argument("--no-update-check", action="store_true",
                               help="更新の確認をスキップ")
    global_parser.add_argument("--auto-update", action="store_true",
                               help="プロンプトなしで更新を自動的にインストールする")

    return global_parser


def create_parser():
    """メインCLIパーサーを作成し、サブコマンドパーサーをアタッチ"""
    global_parser = create_global_parser()

    parser = argparse.ArgumentParser(
        prog="SuperClaude",
        description="SuperClaude フレームワーク管理ハブ - 統一CLI",
        epilog="""
例:
  SuperClaude install --dry-run
  SuperClaude update --verbose
  SuperClaude backup --create
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[global_parser]
    )

    from SuperClaude import __version__
    parser.add_argument("--version", action="version", version=f"SuperClaude {__version__}")

    subparsers = parser.add_subparsers(
        dest="operation",
        title="Operations",
        description="実行するフレームワーク操作"
    )

    return parser, subparsers, global_parser


def setup_global_environment(args: argparse.Namespace):
    """引数に基づいてロギングと共有ランタイム環境を設定"""
    # Determine log level
    if args.quiet:
        level = LogLevel.ERROR
    elif args.verbose:
        level = LogLevel.DEBUG
    else:
        level = LogLevel.INFO

    # Define log directory unless it's a dry run
    log_dir = args.install_dir / "logs" if not args.dry_run else None
    setup_logging("superclaude_hub", log_dir=log_dir, console_level=level)

    # Log startup context
    logger = get_logger()
    if logger:
        logger.debug(f"SuperClaudeが操作で呼び出されました: {getattr(args, 'operation', 'None')}")
        logger.debug(f"引数: {vars(args)}")


def get_operation_modules() -> Dict[str, str]:
    """サポートされている操作とその説明を返す"""
    return {
        "install": "SuperClaudeフレームワークコンポーネントをインストール",
        "update": "既存のSuperClaudeインストールを更新",
        "uninstall": "SuperClaudeのインストールを削除",
        "backup": "バックアップと復元操作"
    }


def load_operation_module(name: str):
    """操作モジュールを動的にインポートしようとします"""
    try:
        return __import__(f"setup.cli.commands.{name}", fromlist=[name])
    except ImportError as e:
        logger = get_logger()
        if logger:
            logger.error(f"モジュール '{name}' の読み込みに失敗しました: {e}")
        return None


def register_operation_parsers(subparsers, global_parser) -> Dict[str, Callable]:
    """サブコマンドパーサーを登録し、操作名をその実行関数にマッピング"""
    operations = {}
    for name, desc in get_operation_modules().items():
        module = load_operation_module(name)
        if module and hasattr(module, 'register_parser') and hasattr(module, 'run'):
            module.register_parser(subparsers, global_parser)
            operations[name] = module.run
        else:
            # If module doesn't exist, register a stub parser and fallback to legacy
            parser = subparsers.add_parser(name, help=f"{desc} (レガシーフォールバック)", parents=[global_parser])
            parser.add_argument("--legacy", action="store_true", help="レガシースクリプトを使用")
            operations[name] = None
    return operations


def handle_legacy_fallback(op: str, args: argparse.Namespace) -> int:
    """モジュールが利用できない場合にレガシー操作スクリプトを実行"""
    script_path = Path(__file__).parent / f"{op}.py"

    if not script_path.exists():
        display_error(f"操作 ' にモジュールまたはレガシースクリプトが見つかりません{op}'")
        return 1

    display_warning(f"' のレガシースクリプトにフォールバックしています{op}'...")

    cmd = [sys.executable, str(script_path)]

    # Convert args into CLI flags
    for k, v in vars(args).items():
        if k in ['operation', 'install_dir'] or v in [None, False]:
            continue
        flag = f"--{k.replace('_', '-')}"
        if v is True:
            cmd.append(flag)
        else:
            cmd.extend([flag, str(v)])

    try:
        return subprocess.call(cmd)
    except Exception as e:
        display_error(f"レガシー実行に失敗しました: {e}")
        return 1


def main() -> int:
    """メインエントリポイント"""
    try:
        parser, subparsers, global_parser = create_parser()
        operations = register_operation_parsers(subparsers, global_parser)
        args = parser.parse_args()
        
        # Check for updates unless disabled
        if not args.quiet and not getattr(args, 'no_update_check', False):
            try:
                from setup.utils.updater import check_for_updates
                # Check for updates in the background
                from SuperClaude import __version__
                updated = check_for_updates(
                    current_version=__version__,
                    auto_update=getattr(args, 'auto_update', False)
                )
                # If updated, suggest restart
                if updated:
                    print("\n🔄 SuperClaude was updated. Please restart to use the new version.")
                    return 0
            except ImportError:
                # Updater module not available, skip silently
                pass
            except Exception:
                # Any other error, skip silently
                pass

        # No operation provided? Show help manually unless in quiet mode
        if not args.operation:
            if not args.quiet:
                from SuperClaude import __version__
                display_header(f"SuperClaude フレームワーク v{__version__}", "すべての操作のための統一CLI")
                print(f"{Colors.CYAN}利用可能な操作:{Colors.RESET}")
                for op, desc in get_operation_modules().items():
                    print(f"  {op:<12} {desc}")
            return 0

        # Handle unknown operations and suggest corrections
        if args.operation not in operations:
            close = difflib.get_close_matches(args.operation, operations.keys(), n=1)
            suggestion = f"もしかして: {close[0]}?" if close else ""
            display_error(f"不明な操作: '{args.operation}'. {suggestion}")
            return 1

        # Setup global context (logging, install path, etc.)
        setup_global_environment(args)
        logger = get_logger()

        # Execute operation
        run_func = operations.get(args.operation)
        if run_func:
            if logger:
                logger.info(f"操作を実行中: {args.operation}")
            return run_func(args)
        else:
            # Fallback to legacy script
            if logger:
                logger.warning(f"' のモジュール{args.operation}' が見つからないため、レガシーフォールバックを使用します")
            return handle_legacy_fallback(args.operation, args)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}ユーザーによって操作がキャンセルされました{Colors.RESET}")
        return 130
    except Exception as e:
        try:
            logger = get_logger()
            if logger:
                logger.exception(f"未処理のエラー: {e}")
        except:
            print(f"{Colors.RED}[ERROR] {e}{Colors.RESET}")
        return 1


# Entrypoint guard
if __name__ == "__main__":
    sys.exit(main())
    

