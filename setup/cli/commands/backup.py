"""
SuperClaude Backup Operation Module
Refactored from backup.py for unified CLI hub
"""

import sys
import time
import tarfile
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
import argparse

from ...services.settings import SettingsService
from ...utils.ui import (
    display_header, display_info, display_success, display_error, 
    display_warning, Menu, confirm, ProgressBar, Colors, format_size
)
from ...utils.logger import get_logger
from ... import DEFAULT_INSTALL_DIR
from . import OperationBase


class BackupOperation(OperationBase):
    """バックアップ操作の実装"""
    
    def __init__(self):
        super().__init__("backup")


def register_parser(subparsers, global_parser=None) -> argparse.ArgumentParser:
    """バックアップCLI引数を登録"""
    parents = [global_parser] if global_parser else []
    
    parser = subparsers.add_parser(
        "backup",
        help="SuperClaudeのインストールをバックアップおよび復元します",
        description="SuperClaudeのインストールバックアップを作成、一覧表示、復元、管理します",
        epilog="""
例:
  SuperClaude backup --create               # 新しいバックアップを作成
  SuperClaude backup --list --verbose       # 利用可能なバックアップを一覧表示（詳細）
  SuperClaude backup --restore              # 対話的に復元
  SuperClaude backup --restore backup.tar.gz  # 特定のバックアップを復元
  SuperClaude backup --info backup.tar.gz   # バックアップ情報を表示
  SuperClaude backup --cleanup --force      # 古いバックアップをクリーンアップ（強制）
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parents
    )
    
    # バックアップ操作（相互に排他的）
    operation_group = parser.add_mutually_exclusive_group(required=True)
    
    operation_group.add_argument(
        "--create",
        action="store_true",
        help="新しいバックアップを作成します"
    )
    
    operation_group.add_argument(
        "--list",
        action="store_true",
        help="利用可能なバックアップを一覧表示します"
    )
    
    operation_group.add_argument(
        "--restore",
        nargs="?",
        const="interactive",
        help="バックアップから復元します（オプションでバックアップファイルを指定）"
    )
    
    operation_group.add_argument(
        "--info",
        type=str,
        help="特定のバックアップファイルに関する情報を表示します"
    )
    
    operation_group.add_argument(
        "--cleanup",
        action="store_true",
        help="古いバックアップファイルをクリーンアップします"
    )
    
    # バックアップオプション
    parser.add_argument(
        "--backup-dir",
        type=Path,
        help="バックアップディレクトリ（デフォルト: <install-dir>/backups）"
    )
    
    parser.add_argument(
        "--name",
        type=str,
        help="カスタムバックアップ名（--create用）"
    )
    
    parser.add_argument(
        "--compress",
        choices=["none", "gzip", "bzip2"],
        default="gzip",
        help="圧縮方法（デフォルト: gzip）"
    )
    
    # 復元オプション
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="復元中に既存のファイルを上書きします"
    )
    
    # クリーンアップオプション
    parser.add_argument(
        "--keep",
        type=int,
        default=5,
        help="クリーンアップ中に保持するバックアップの数（デフォルト: 5）"
    )
    
    parser.add_argument(
        "--older-than",
        type=int,
        help="N日より古いバックアップを削除します"
    )
    
    return parser


def get_backup_directory(args: argparse.Namespace) -> Path:
    """バックアップディレクトリのパスを取得"""
    if args.backup_dir:
        return args.backup_dir
    else:
        return args.install_dir / "backups"


def check_installation_exists(install_dir: Path) -> bool:
    """SuperClaudeのインストール（v2含む）が存在するか確認"""
    settings_manager = SettingsService(install_dir)

    return settings_manager.check_installation_exists() or settings_manager.check_v2_installation_exists()


def get_backup_info(backup_path: Path) -> Dict[str, Any]:
    """バックアップファイルに関する情報を取得"""
    info = {
        "path": backup_path,
        "exists": backup_path.exists(),
        "size": 0,
        "created": None,
        "metadata": {}
    }
    
    if not backup_path.exists():
        return info
    
    try:
        # ファイル統計を取得
        stats = backup_path.stat()
        info["size"] = stats.st_size
        info["created"] = datetime.fromtimestamp(stats.st_mtime)
        
        # バックアップからメタデータを読み込もうと試みる
        if backup_path.suffix == ".gz":
            mode = "r:gz"
        elif backup_path.suffix == ".bz2":
            mode = "r:bz2"
        else:
            mode = "r"
        
        with tarfile.open(backup_path, mode) as tar:
            # メタデータファイルを探す
            try:
                metadata_member = tar.getmember("backup_metadata.json")
                metadata_file = tar.extractfile(metadata_member)
                if metadata_file:
                    info["metadata"] = json.loads(metadata_file.read().decode())
            except KeyError:
                pass  # メタデータファイルなし
            
            # バックアップ内のファイルリストを取得
            info["files"] = len(tar.getnames())
            
    except Exception as e:
        info["error"] = str(e)
    
    return info


def list_backups(backup_dir: Path) -> List[Dict[str, Any]]:
    """利用可能なすべてのバックアップを一覧表示"""
    backups = []
    
    if not backup_dir.exists():
        return backups
    
    # すべてのバックアップファイルを検索
    for backup_file in backup_dir.glob("*.tar*"):
        if backup_file.is_file():
            info = get_backup_info(backup_file)
            backups.append(info)
    
    # 作成日でソート（新しい順）
    backups.sort(key=lambda x: x.get("created", datetime.min), reverse=True)
    
    return backups


def display_backup_list(backups: List[Dict[str, Any]]) -> None:
    """利用可能なバックアップのリストを表示"""
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}利用可能なバックアップ{Colors.RESET}")
    print("=" * 70)
    
    if not backups:
        print(f"{Colors.YELLOW}バックアップが見つかりません{Colors.RESET}")
        return
    
    print(f"{'名前':<30} {'サイズ':<10} {'作成日時':<20} {'ファイル数':<8}")
    print("-" * 70)
    
    for backup in backups:
        name = backup["path"].name
        size = format_size(backup["size"]) if backup["size"] > 0 else "不明"
        created = backup["created"].strftime("%Y-%m-%d %H:%M") if backup["created"] else "不明"
        files = str(backup.get("files", "不明"))
        
        print(f"{name:<30} {size:<10} {created:<20} {files:<8}")
    
    print()


def create_backup_metadata(install_dir: Path) -> Dict[str, Any]:
    """バックアップ用のメタデータを作成"""
    metadata = {
        "backup_version": __version__,
        "created": datetime.now().isoformat(),
        "install_dir": str(install_dir),
        "components": {},
        "framework_version": "unknown"
    }
    
    try:
        # メタデータからインストール済みコンポーネントを取得
        settings_manager = SettingsService(install_dir)
        framework_config = settings_manager.get_metadata_setting("framework")
        
        if framework_config:
            metadata["framework_version"] = framework_config.get("version", "unknown")
            
            if "components" in framework_config:
                for component_name in framework_config["components"]:
                    version = settings_manager.get_component_version(component_name)
                    if version:
                        metadata["components"][component_name] = version
    except Exception:
        pass  # メタデータなしで続行
    
    return metadata


def create_backup(args: argparse.Namespace) -> bool:
    """新しいバックアップを作成"""
    logger = get_logger()
    
    try:
        # インストールが存在するか確認
        if not check_installation_exists(args.install_dir):
            logger.error(f"{args.install_dir}にSuperClaudeのインストールが見つかりません")
            return False
        
        # バックアップディレクトリを設定
        backup_dir = get_backup_directory(args)
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # バックアップファイル名を生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if args.name:
            backup_name = f"{args.name}_{timestamp}"
        else:
            backup_name = f"superclaude_backup_{timestamp}"
        
        # 圧縮を決定
        if args.compress == "gzip":
            backup_file = backup_dir / f"{backup_name}.tar.gz"
            mode = "w:gz"
        elif args.compress == "bzip2":
            backup_file = backup_dir / f"{backup_name}.tar.bz2"
            mode = "w:bz2"
        else:
            backup_file = backup_dir / f"{backup_name}.tar"
            mode = "w"
        
        logger.info(f"バックアップを作成中: {backup_file}")
        
        # メタデータを作成
        metadata = create_backup_metadata(args.install_dir)
        
        # バックアップを作成
        start_time = time.time()
        
        with tarfile.open(backup_file, mode) as tar:
            # メタデータファイルを追加
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(metadata, temp_file, indent=2)
                temp_file.flush()
                tar.add(temp_file.name, arcname="backup_metadata.json")
                Path(temp_file.name).unlink()  # 一時ファイルをクリーンアップ
            
            # インストールディレクトリの内容を追加（バックアップとローカルディレクトリを除く）
            files_added = 0
            for item in args.install_dir.rglob("*"):
                if item.is_file() and item != backup_file:
                    try:
                        # アーカイブ用の相対パスを作成
                        rel_path = item.relative_to(args.install_dir)
                        
                        # 除外されたディレクトリ内のファイルをスキップ
                        if rel_path.parts and rel_path.parts[0] in ["backups", "local"]:
                            continue
                            
                        tar.add(item, arcname=str(rel_path))
                        files_added += 1
                        
                        if files_added % 10 == 0:
                            logger.debug(f"{files_added}個のファイルをバックアップに追加しました")
                            
                    except Exception as e:
                        logger.warning(f"{item}をバックアップに追加できませんでした: {e}")
        
        duration = time.time() - start_time
        file_size = backup_file.stat().st_size
        
        logger.success(f"バックアップは{duration:.1f}秒で正常に作成されました")
        logger.info(f"バックアップファイル: {backup_file}")
        logger.info(f"アーカイブされたファイル数: {files_added}")
        logger.info(f"バックアップサイズ: {format_size(file_size)}")
        
        return True
        
    except Exception as e:
        logger.exception(f"バックアップの作成に失敗しました: {e}")
        return False


def restore_backup(backup_path: Path, args: argparse.Namespace) -> bool:
    """バックアップファイルから復元"""
    logger = get_logger()
    
    try:
        if not backup_path.exists():
            logger.error(f"バックアップファイルが見つかりません: {backup_path}")
            return False
        
        # バックアップファイルを確認
        info = get_backup_info(backup_path)
        if "error" in info:
            logger.error(f"無効なバックアップファイルです: {info['error']}")
            return False
        
        logger.info(f"バックアップから復元中: {backup_path}")
        
        # 圧縮を決定
        if backup_path.suffix == ".gz":
            mode = "r:gz"
        elif backup_path.suffix == ".bz2":
            mode = "r:bz2"
        else:
            mode = "r"
        
        # 現在のインストールが存在する場合、バックアップを作成
        if check_installation_exists(args.install_dir) and not args.dry_run:
            logger.info("復元前に現在のインストールのバックアップを作成中")
            # これは内部的にcreate_backupを呼び出す
        
        # バックアップを展開
        start_time = time.time()
        files_restored = 0
        
        with tarfile.open(backup_path, mode) as tar:
            # メタデータを除くすべてのファイルを展開
            for member in tar.getmembers():
                if member.name == "backup_metadata.json":
                    continue
                
                try:
                    target_path = args.install_dir / member.name
                    
                    # ファイルが存在し、上書きフラグが立っているか確認
                    if target_path.exists() and not args.overwrite:
                        logger.warning(f"既存のファイルをスキップ: {target_path}")
                        continue
                    
                    # ファイルを展開
                    tar.extract(member, args.install_dir)
                    files_restored += 1
                    
                    if files_restored % 10 == 0:
                        logger.debug(f"{files_restored}個のファイルを復元しました")
                        
                except Exception as e:
                    logger.warning(f"{member.name}を復元できませんでした: {e}")
        
        duration = time.time() - start_time
        
        logger.success(f"復元は{duration:.1f}秒で正常に完了しました")
        logger.info(f"復元されたファイル数: {files_restored}")
        
        return True
        
    except Exception as e:
        logger.exception(f"バックアップの復元に失敗しました: {e}")
        return False


def interactive_restore_selection(backups: List[Dict[str, Any]]) -> Optional[Path]:
    """復元のための対話型バックアップ選択"""
    if not backups:
        print(f"{Colors.YELLOW}復元可能なバックアップがありません{Colors.RESET}")
        return None
    
    print(f"\n{Colors.CYAN}復元するバックアップを選択:{Colors.RESET}")
    
    # メニューオプションを作成
    backup_options = []
    for backup in backups:
        name = backup["path"].name
        size = format_size(backup["size"]) if backup["size"] > 0 else "不明"
        created = backup["created"].strftime("%Y-%m-%d %H:%M") if backup["created"] else "不明"
        backup_options.append(f"{name} ({size}, {created})")
    
    menu = Menu("バックアップを選択:", backup_options)
    choice = menu.display()
    
    if choice == -1 or choice >= len(backups):
        return None
    
    return backups[choice]["path"]


def cleanup_old_backups(backup_dir: Path, args: argparse.Namespace) -> bool:
    """古いバックアップファイルをクリーンアップ"""
    logger = get_logger()
    
    try:
        backups = list_backups(backup_dir)
        if not backups:
            logger.info("クリーンアップするバックアップが見つかりません")
            return True
        
        to_remove = []
        
        # 古いものを削除
        if args.older_than:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=args.older_than)
            for backup in backups:
                if backup["created"] and backup["created"] < cutoff_date:
                    to_remove.append(backup)
        
        # 最新N個のみ保持
        if args.keep and len(backups) > args.keep:
            # 日付でソートし、最も古いものを削除対象にする
            backups.sort(key=lambda x: x.get("created", datetime.min), reverse=True)
            to_remove.extend(backups[args.keep:])
        
        # 重複を削除
        to_remove = list({backup["path"]: backup for backup in to_remove}.values())
        
        if not to_remove:
            logger.info("クリーンアップが必要なバックアップはありません")
            return True
        
        logger.info(f"{len(to_remove)}個の古いバックアップをクリーンアップ中")
        
        for backup in to_remove:
            try:
                backup["path"].unlink()
                logger.info(f"削除されたバックアップ: {backup['path'].name}")
            except Exception as e:
                logger.warning(f"{backup['path'].name}を削除できませんでした: {e}")
        
        return True
        
    except Exception as e:
        logger.exception(f"バックアップのクリーンアップに失敗しました: {e}")
        return False


def run(args: argparse.Namespace) -> int:
    """解析された引数でバックアップ操作を実行"""
    operation = BackupOperation()
    operation.setup_operation_logging(args)
    logger = get_logger()
    # ✅ 挿入された検証コード
    expected_home = Path.home().resolve()
    actual_dir = args.install_dir.resolve()

    if not str(actual_dir).startswith(str(expected_home)):
        print(f"\n[✗] インストールはユーザープロファイルディレクトリ内で行う必要があります。")
        print(f"    期待されるプレフィックス: {expected_home}")
        print(f"    指定されたパス:   {actual_dir}")
        sys.exit(1)
    
    try:
        # グローバル引数を検証
        success, errors = operation.validate_global_args(args)
        if not success:
            for error in errors:
                logger.error(error)
            return 1
        
        # ヘッダーを表示
        if not args.quiet:
            from setup.cli.base import __version__
            display_header(
                f"SuperClaude バックアップ v{__version__}",
                "SuperClaudeのインストールをバックアップおよび復元"
            )
        
        backup_dir = get_backup_directory(args)
        
        # さまざまなバックアップ操作を処理
        if args.create:
            success = create_backup(args)
            
        elif args.list:
            backups = list_backups(backup_dir)
            display_backup_list(backups)
            success = True
            
        elif args.restore:
            if args.restore == "interactive":
                # 対話的な復元
                backups = list_backups(backup_dir)
                backup_path = interactive_restore_selection(backups)
                if not backup_path:
                    logger.info("ユーザーによって復元がキャンセルされました")
                    return 0
            else:
                # 特定のバックアップファイル
                backup_path = Path(args.restore)
                if not backup_path.is_absolute():
                    backup_path = backup_dir / backup_path
            
            success = restore_backup(backup_path, args)
            
        elif args.info:
            backup_path = Path(args.info)
            if not backup_path.is_absolute():
                backup_path = backup_dir / backup_path
            
            info = get_backup_info(backup_path)
            if info["exists"]:
                print(f"\n{Colors.CYAN}バックアップ情報:{Colors.RESET}")
                print(f"ファイル: {info['path']}")
                print(f"サイズ: {format_size(info['size'])}")
                print(f"作成日時: {info['created']}")
                print(f"ファイル数: {info.get('files', '不明')}")
                
                if info["metadata"]:
                    metadata = info["metadata"]
                    print(f"フレームワークバージョン: {metadata.get('framework_version', '不明')}")
                    if metadata.get("components"):
                        print("コンポーネント:")
                        for comp, ver in metadata["components"].items():
                            print(f"  {comp}: v{ver}")
            else:
                logger.error(f"バックアップファイルが見つかりません: {backup_path}")
                success = False
            success = True
            
        elif args.cleanup:
            success = cleanup_old_backups(backup_dir, args)
        
        else:
            logger.error("バックアップ操作が指定されていません")
            success = False
        
        if success:
            if not args.quiet and args.create:
                display_success("バックアップ操作が正常に完了しました！")
            elif not args.quiet and args.restore:
                display_success("復元操作が正常に完了しました！")
            return 0
        else:
            display_error("バックアップ操作に失敗しました。詳細はログを確認してください。")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}ユーザーによってバックアップ操作がキャンセルされました{Colors.RESET}")
        return 130
    except Exception as e:
        return operation.handle_operation_error("backup", e)
