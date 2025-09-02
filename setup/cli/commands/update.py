"""
SuperClaude Update Operation Module
Refactored from update.py for unified CLI hub
"""

import sys
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
import argparse

from ...core.installer import Installer
from ...core.registry import ComponentRegistry
from ...services.settings import SettingsService
from ...core.validator import Validator
from ...utils.ui import (
    display_header, display_info, display_success, display_error, 
    display_warning, Menu, confirm, ProgressBar, Colors, format_size, prompt_api_key
)
from ...utils.environment import setup_environment_variables
from ...utils.logger import get_logger
from ... import DEFAULT_INSTALL_DIR, PROJECT_ROOT
from . import OperationBase


class UpdateOperation(OperationBase):
    """更新操作の実装"""
    
    def __init__(self):
        super().__init__("update")


def register_parser(subparsers, global_parser=None) -> argparse.ArgumentParser:
    """更新CLI引数を登録"""
    parents = [global_parser] if global_parser else []
    
    parser = subparsers.add_parser(
        "update",
        help="既存のSuperClaudeインストールを更新",
        description="SuperClaudeフレームワークコンポーネントを最新バージョンに更新",
        epilog="""
例:
  SuperClaude update                       # 対話的な更新
  SuperClaude update --check --verbose     # 更新を確認 (詳細)
  SuperClaude update --components core mcp # 特定のコンポーネントを更新
  SuperClaude update --backup --force      # 更新前にバックアップを作成 (強制)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parents
    )
    
    # Update mode options
    parser.add_argument(
        "--check",
        action="store_true",
        help="インストールせずに利用可能な更新を確認"
    )
    
    parser.add_argument(
        "--components",
        type=str,
        nargs="+",
        help="更新する特定のコンポーネント"
    )
    
    # Backup options
    parser.add_argument(
        "--backup",
        action="store_true",
        help="更新前にバックアップを作成"
    )
    
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="バックアップ作成をスキップ"
    )
    
    # Update options
    parser.add_argument(
        "--reinstall",
        action="store_true",
        help="バージョンが一致してもコンポーネントを再インストール"
    )
    
    return parser

def check_installation_exists(install_dir: Path) -> bool:
    """SuperClaudeのインストールが存在するか確認"""
    settings_manager = SettingsService(install_dir)

    return settings_manager.check_installation_exists()

def get_installed_components(install_dir: Path) -> Dict[str, Dict[str, Any]]:
    """現在インストールされているコンポーネントとそのバージョンを取得"""
    try:
        settings_manager = SettingsService(install_dir)
        return settings_manager.get_installed_components()
    except Exception:
        return {}


def get_available_updates(installed_components: Dict[str, str], registry: ComponentRegistry) -> Dict[str, Dict[str, str]]:
    """利用可能な更新を確認"""
    updates = {}
    
    for component_name, current_version in installed_components.items():
        try:
            metadata = registry.get_component_metadata(component_name)
            if metadata:
                available_version = metadata.get("version", "unknown")
                if available_version != current_version:
                    updates[component_name] = {
                        "current": current_version,
                        "available": available_version,
                        "description": metadata.get("description", "説明なし")
                    }
        except Exception:
            continue
    
    return updates


def display_update_check(installed_components: Dict[str, str], available_updates: Dict[str, Dict[str, str]]) -> None:
    """更新チェック結果を表示"""
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}Update Check Results{Colors.RESET}")
    print("=" * 50)
    
    if not installed_components:
        print(f"{Colors.YELLOW}SuperClaudeのインストールが見つかりません{Colors.RESET}")
        return
    
    print(f"{Colors.BLUE}現在インストールされているコンポーネント:{Colors.RESET}")
    for component, version in installed_components.items():
        print(f"  {component}: v{version}")
    
    if available_updates:
        print(f"\n{Colors.GREEN}Available updates:{Colors.RESET}")
        for component, info in available_updates.items():
            print(f"  {component}: v{info['current']} → v{info['available']}")
            print(f"    {info['description']}")
    else:
        print(f"\n{Colors.GREEN}すべてのコンポーネントは最新です{Colors.RESET}")
    
    print()


def get_components_to_update(args: argparse.Namespace, installed_components: Dict[str, str], 
                           available_updates: Dict[str, Dict[str, str]]) -> Optional[List[str]]:
    """更新するコンポーネントを決定"""
    logger = get_logger()
    
    # Explicit components specified
    if args.components:
        # Validate that specified components are installed
        invalid_components = [c for c in args.components if c not in installed_components]
        if invalid_components:
            logger.error(f"インストールされていないコンポーネント: {invalid_components}")
            return None
        return args.components
    
    # If no updates available and not forcing reinstall
    if not available_updates and not args.reinstall:
        logger.info("利用可能な更新はありません")
        return []
    
    # Interactive selection
    if available_updates:
        return interactive_update_selection(available_updates, installed_components)
    elif args.reinstall:
        # Reinstall all components
        return list(installed_components.keys())
    
    return []


def collect_api_keys_for_servers(selected_servers: List[str], mcp_instance) -> Dict[str, str]:
    """
    更新中にサーバーが必要とするAPIキーを収集します
    
    Args:
        selected_servers: 選択されたサーバーキーのリスト
        mcp_instance: MCPコンポーネントインスタンス
        
    Returns:
        環境変数名とAPIキー値の辞書
    """
    # Filter servers needing keys
    servers_needing_keys = [
        (server_key, mcp_instance.mcp_servers[server_key])
        for server_key in selected_servers
        if server_key in mcp_instance.mcp_servers and
           mcp_instance.mcp_servers[server_key].get("requires_api_key", False)
    ]
    
    if not servers_needing_keys:
        return {}
    
    # Display API key configuration header
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}═══ APIキー設定 ═══{Colors.RESET}")
    print(f"{Colors.YELLOW}新しいMCPサーバーは全機能を利用するためにAPIキーが必要です:{Colors.RESET}\n")
    
    collected_keys = {}
    for server_key, server_info in servers_needing_keys:
        api_key_env = server_info.get("api_key_env")
        service_name = server_info["name"]
        
        if api_key_env:
            key = prompt_api_key(service_name, api_key_env)
            if key:
                collected_keys[api_key_env] = key
    
    return collected_keys


def interactive_update_selection(available_updates: Dict[str, Dict[str, str]], 
                                installed_components: Dict[str, str]) -> Optional[List[str]]:
    """対話的な更新の選択"""
    if not available_updates:
        return []
    
    print(f"\n{Colors.CYAN}利用可能な更新:{Colors.RESET}")
    
    # Create menu options
    update_options = []
    component_names = []
    
    for component, info in available_updates.items():
        update_options.append(f"{component}: v{info['current']} → v{info['available']}")
        component_names.append(component)
    
    # Add bulk options
    preset_options = [
        "すべてのコンポーネントを更新",
        "個別のコンポーネントを選択",
        "更新をキャンセル"
    ]
    
    menu = Menu("更新オプションを選択:", preset_options)
    choice = menu.display()
    
    if choice == -1 or choice == 2:  # Cancelled
        return None
    elif choice == 0:  # Update all
        return component_names
    elif choice == 1:  # Select individual
        component_menu = Menu("更新するコンポーネントを選択:", update_options, multi_select=True)
        selections = component_menu.display()
        
        if not selections:
            return None
        
        return [component_names[i] for i in selections]
    
    return None


def display_update_plan(components: List[str], available_updates: Dict[str, Dict[str, str]], 
                       installed_components: Dict[str, str], install_dir: Path) -> None:
    """更新計画を表示"""
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}Update Plan{Colors.RESET}")
    print("=" * 50)
    
    print(f"{Colors.BLUE}インストールディレクトリ:{Colors.RESET} {install_dir}")
    print(f"{Colors.BLUE}更新するコンポーネント:{Colors.RESET}")
    
    for i, component_name in enumerate(components, 1):
        if component_name in available_updates:
            info = available_updates[component_name]
            print(f"  {i}. {component_name}: v{info['current']} → v{info['available']}")
        else:
            current_version = installed_components.get(component_name, "unknown")
            print(f"  {i}. {component_name}: v{current_version} (再インストール)")
    
    print()


def perform_update(components: List[str], args: argparse.Namespace) -> bool:
    """実際の更新を実行"""
    logger = get_logger()
    start_time = time.time()
    
    try:
        # Create installer
        installer = Installer(args.install_dir, dry_run=args.dry_run)
        
        # Create component registry
        registry = ComponentRegistry(PROJECT_ROOT / "setup" / "components")
        registry.discover_components()
        
        # Create component instances
        component_instances = registry.create_component_instances(components, args.install_dir)
        
        if not component_instances:
            logger.error("有効なコンポーネントインスタンスが作成されませんでした")
            return False
        
        # Handle MCP component specially - collect API keys for new servers
        collected_api_keys = {}
        if "mcp" in components and "mcp" in component_instances:
            mcp_instance = component_instances["mcp"]
            if hasattr(mcp_instance, 'mcp_servers'):
                # Get all available MCP servers
                all_server_keys = list(mcp_instance.mcp_servers.keys())
                
                # Collect API keys for any servers that require them
                collected_api_keys = collect_api_keys_for_servers(all_server_keys, mcp_instance)
                
                # Set up environment variables if any keys were collected
                if collected_api_keys:
                    setup_environment_variables(collected_api_keys)
                    
                    # Store keys for MCP component to use during update
                    mcp_instance.collected_api_keys = collected_api_keys
                    
                    logger.info(f"収集済み {len(collected_api_keys)} MCPサーバー更新用のAPIキー")
        
        # Register components with installer
        installer.register_components(list(component_instances.values()))
        
        # Setup progress tracking
        progress = ProgressBar(
            total=len(components),
            prefix="更新中: ",
            suffix=""
        )
        
        # Update components
        logger.info(f"更新中 {len(components)} コンポーネント...")
        
        # Determine backup strategy
        backup = args.backup or (not args.no_backup and not args.dry_run)
        
        config = {
            "force": args.force,
            "backup": backup,
            "dry_run": args.dry_run,
            "update_mode": True,
            "selected_mcp_servers": list(mcp_instance.mcp_servers.keys()) if "mcp" in component_instances else []
        }
        
        success = installer.update_components(components, config)
        
        # Update progress
        for i, component_name in enumerate(components):
            if component_name in installer.updated_components:
                progress.update(i + 1, f"更新済み {component_name}")
            else:
                progress.update(i + 1, f"失敗 {component_name}")
            time.sleep(0.1)  # Brief pause for visual effect
        
        progress.finish("更新完了")
        
        # Show results
        duration = time.time() - start_time
        
        if success:
            logger.success(f"更新は正常に完了しました: {duration:.1f} 秒")
            
            # Show summary
            summary = installer.get_update_summary()
            if summary.get('updated'):
                logger.info(f"更新されたコンポーネント: {', '.join(summary['updated'])}")
            
            if summary.get('backup_path'):
                logger.info(f"バックアップ作成済み: {summary['backup_path']}")
                
        else:
            logger.error(f"更新はエラーで完了しました: {duration:.1f} 秒")
            
            summary = installer.get_update_summary()
            if summary.get('failed'):
                logger.error(f"失敗したコンポーネント: {', '.join(summary['failed'])}")
        
        return success
        
    except Exception as e:
        logger.exception(f"更新中に予期しないエラーが発生しました: {e}")
        return False


def run(args: argparse.Namespace) -> int:
    """解析された引数で更新操作を実行"""
    operation = UpdateOperation()
    operation.setup_operation_logging(args)
    logger = get_logger()
    # ✅ Inserted validation code
    expected_home = Path.home().resolve()
    actual_dir = args.install_dir.resolve()

    if not str(actual_dir).startswith(str(expected_home)):
        print(f"\n[✗] Installation must be inside your user profile directory.")
        print(f"    期待されるプレフィックス: {expected_home}")
        print(f"    指定されたパス:   {actual_dir}")
        sys.exit(1)
    
    try:
        # Validate global arguments
        success, errors = operation.validate_global_args(args)
        if not success:
            for error in errors:
                logger.error(error)
            return 1
        
        # Display header
        if not args.quiet:
            display_header(
                f"SuperClaude 更新 v{__version__}",
                "SuperClaudeフレームワークコンポーネントを更新中"
            )
        
        # Check if SuperClaude is installed
        if not check_installation_exists(args.install_dir):
            logger.error(f"SuperClaudeのインストールが次の場所に見つかりません: {args.install_dir}")
            logger.info("最初に 'SuperClaude install' を使用してSuperClaudeをインストールしてください")
            return 1
        
        # Create component registry
        logger.info("利用可能な更新を確認中...")
        
        registry = ComponentRegistry(PROJECT_ROOT / "setup" / "components")
        registry.discover_components()
        
        # Get installed components
        installed_components = get_installed_components(args.install_dir)
        if not installed_components:
            logger.error("インストールされているコンポーネントを特定できませんでした")
            return 1
        
        # Check for available updates
        available_updates = get_available_updates(installed_components, registry)
        
        # Display update check results
        if not args.quiet:
            display_update_check(installed_components, available_updates)
        
        # If only checking for updates, exit here
        if args.check:
            return 0
        
        # Get components to update
        components = get_components_to_update(args, installed_components, available_updates)
        if components is None:
            logger.info("ユーザーによって更新がキャンセルされました")
            return 0
        elif not components:
            logger.info("更新対象のコンポーネントが選択されていません")
            return 0
        
        # Display update plan
        if not args.quiet:
            display_update_plan(components, available_updates, installed_components, args.install_dir)
            
            if not args.dry_run:
                if not args.yes and not confirm("更新を続行しますか？", default=True):
                    logger.info("ユーザーによって更新がキャンセルされました")
                    return 0
        
        # Perform update
        success = perform_update(components, args)
        
        if success:
            if not args.quiet:
                display_success("SuperClaudeの更新が正常に完了しました！")
                
                if not args.dry_run:
                    print(f"\n{Colors.CYAN}次のステップ:{Colors.RESET}")
                    print(f"1. Claude Codeセッションを再起動してください")
                    print(f"2. 更新されたコンポーネントが利用可能です")
                    print(f"3. ドキュメントで破壊的変更がないか確認してください")
                    
            return 0
        else:
            display_error("更新に失敗しました。詳細はログを確認してください。")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Update cancelled by user{Colors.RESET}")
        return 130
    except Exception as e:
        return operation.handle_operation_error("update", e)
