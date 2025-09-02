"""
SuperClaude Installation Operation Module
Refactored from install.py for unified CLI hub
"""

import sys
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
import argparse

from ...core.installer import Installer
from ...core.registry import ComponentRegistry
from ...services.config import ConfigService
from ...core.validator import Validator
from ...utils.ui import (
    display_header, display_info, display_success, display_error, 
    display_warning, Menu, confirm, ProgressBar, Colors, format_size, prompt_api_key
)
from ...utils.environment import setup_environment_variables
from ...utils.logger import get_logger
from ... import DEFAULT_INSTALL_DIR, PROJECT_ROOT, DATA_DIR
from . import OperationBase


class InstallOperation(OperationBase):
    """インストール操作の実装"""
    
    def __init__(self):
        super().__init__("install")


def register_parser(subparsers, global_parser=None) -> argparse.ArgumentParser:
    """インストールCLI引数を登録します"""
    parents = [global_parser] if global_parser else []
    
    parser = subparsers.add_parser(
        "install",
        help="SuperClaudeフレームワークコンポーネントをインストールします",
        description="様々なオプションとプロファイルでSuperClaudeフレームワークをインストールします",
        epilog="""
例:
  SuperClaude install                          # 対話的なインストール
  SuperClaude install --dry-run                # ドライランモード
  SuperClaude install --components core mcp    # 特定のコンポーネント
  SuperClaude install --verbose --force        # 詳細モードと強制モード
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parents
    )
    
    # Installation mode options
    
    parser.add_argument(
        "--components",
        type=str,
        nargs="+",
        help="インストールする特定のコンポーネント"
    )
    
    # Installation options
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="バックアップの作成をスキップします"
    )
    
    parser.add_argument(
        "--list-components",
        action="store_true",
        help="利用可能なコンポーネントを一覧表示して終了します"
    )
    
    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="システム診断を実行し、インストールヘルプを表示します"
    )
    
    return parser


def validate_system_requirements(validator: Validator, component_names: List[str]) -> bool:
    """システム要件を検証します"""
    logger = get_logger()
    
    logger.info("システム要件を検証中...")
    
    try:
        # Load requirements configuration
        config_manager = ConfigService(DATA_DIR)
        requirements = config_manager.get_requirements_for_components(component_names)
        
        # Validate requirements
        success, errors = validator.validate_component_requirements(component_names, requirements)
        
        if success:
            logger.success("すべてのシステム要件が満たされています")
            return True
        else:
            logger.error("システム要件が満たされていません:")
            for error in errors:
                logger.error(f"  - {error}")
            
            # Provide additional guidance
            print(f"\n{Colors.CYAN}💡 インストールヘルプ:{Colors.RESET}")
            print("  詳細なシステム診断については 'SuperClaude install --diagnose' を実行してください")
            print("  そして、ステップバイステップのインストール手順を参照してください。")
            
            return False
            
    except Exception as e:
        logger.error(f"システム要件を検証できませんでした: {e}")
        return False


def get_components_to_install(args: argparse.Namespace, registry: ComponentRegistry, config_manager: ConfigService) -> Optional[List[str]]:
    """インストールするコンポーネントを決定します"""
    logger = get_logger()
    
    # Explicit components specified
    if args.components:
        if 'all' in args.components:
            return ["core", "commands", "agents", "modes", "mcp", "mcp_docs"]
        return args.components
    
    # Interactive two-stage selection
    return interactive_component_selection(registry, config_manager)


def collect_api_keys_for_servers(selected_servers: List[str], mcp_instance) -> Dict[str, str]:
    """
    サーバーが必要とするAPIキーを収集します
    
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
    print(f"{Colors.YELLOW}以下のサーバーは全機能を利用するためにAPIキーが必要です:{Colors.RESET}\n")
    
    collected_keys = {}
    for server_key, server_info in servers_needing_keys:
        api_key_env = server_info.get("api_key_env")
        service_name = server_info["name"]
        
        if api_key_env:
            key = prompt_api_key(service_name, api_key_env)
            if key:
                collected_keys[api_key_env] = key
    
    return collected_keys


def select_mcp_servers(registry: ComponentRegistry) -> List[str]:
    """ステージ1: MCPサーバーの選択とAPIキーの収集"""
    logger = get_logger()
    
    try:
        # Get MCP component to access server list
        mcp_instance = registry.get_component_instance("mcp", Path.home() / ".claude")
        if not mcp_instance or not hasattr(mcp_instance, 'mcp_servers'):
            logger.error("MCPサーバー情報にアクセスできませんでした")
            return []
        
        # Create MCP server menu
        mcp_servers = mcp_instance.mcp_servers
        server_options = []
        
        for server_key, server_info in mcp_servers.items():
            description = server_info["description"]
            api_key_note = " (APIキーが必要です)" if server_info.get("requires_api_key", False) else ""
            server_options.append(f"{server_key} - {description}{api_key_note}")
        
        print(f"\n{Colors.CYAN}{Colors.BRIGHT}═══════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BRIGHT}ステージ1: MCPサーバーの選択（任意）{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BRIGHT}═══════════════════════════════════════════════════{Colors.RESET}")
        print(f"\n{Colors.BLUE}MCPサーバーは、専門的な機能でClaude Codeを拡張します。{Colors.RESET}")
        print(f"{Colors.BLUE}設定するサーバーを選択してください（後でいつでも追加できます）:{Colors.RESET}")
        
        # Add option to skip MCP
        server_options.append("MCPサーバーのインストールをスキップ")
        
        menu = Menu("設定するMCPサーバーを選択してください:", server_options, multi_select=True)
        selections = menu.display()
        
        if not selections:
            logger.info("MCPサーバーが選択されていません")
            return []
        
        # Filter out the "skip" option and return server keys
        server_keys = list(mcp_servers.keys())
        selected_servers = []
        
        for i in selections:
            if i < len(server_keys):  # Not the "skip" option
                selected_servers.append(server_keys[i])
        
        if selected_servers:
            logger.info(f"選択されたMCPサーバー: {', '.join(selected_servers)}")
            
            # NEW: Collect API keys for selected servers
            collected_keys = collect_api_keys_for_servers(selected_servers, mcp_instance)
            
            # Set up environment variables
            if collected_keys:
                setup_environment_variables(collected_keys)
                
                # Store keys for MCP component to use during installation
                mcp_instance.collected_api_keys = collected_keys
        else:
            logger.info("MCPサーバーが選択されていません")
        
        return selected_servers
        
    except Exception as e:
        logger.error(f"MCPサーバーの選択中にエラーが発生しました: {e}")
        return []


def select_framework_components(registry: ComponentRegistry, config_manager: ConfigService, selected_mcp_servers: List[str]) -> List[str]:
    """ステージ2: フレームワークコンポーネントの選択"""
    logger = get_logger()
    
    try:
        # Framework components (excluding MCP-related ones)
        framework_components = ["core", "modes", "commands", "agents"]
        
        # Create component menu
        component_options = []
        component_info = {}
        
        for component_name in framework_components:
            metadata = registry.get_component_metadata(component_name)
            if metadata:
                description = metadata.get("description", "説明なし")
                component_options.append(f"{component_name} - {description}")
                component_info[component_name] = metadata
        
        # Add MCP documentation option
        if selected_mcp_servers:
            mcp_docs_desc = f"{', '.join(selected_mcp_servers)} のMCPドキュメント (自動選択)"
            component_options.append(f"mcp_docs - {mcp_docs_desc}")
            auto_selected_mcp_docs = True
        else:
            component_options.append("mcp_docs - MCPサーバードキュメント (選択されていません)")
            auto_selected_mcp_docs = False
        
        print(f"\n{Colors.CYAN}{Colors.BRIGHT}═══════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BRIGHT}ステージ2: フレームワークコンポーネントの選択{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BRIGHT}═══════════════════════════════════════════════════{Colors.RESET}")
        print(f"\n{Colors.BLUE}インストールするSuperClaudeフレームワークコンポーネントを選択してください:{Colors.RESET}")
        
        menu = Menu("コンポーネントを選択してください (Coreを推奨):", component_options, multi_select=True)
        selections = menu.display()
        
        if not selections:
            # Default to core if nothing selected
            logger.info("コンポーネントが選択されていないため、coreをデフォルトにします")
            selected_components = ["core"]
        else:
            selected_components = []
            all_components = framework_components + ["mcp_docs"]
            
            for i in selections:
                if i < len(all_components):
                    selected_components.append(all_components[i])
        
        # Auto-select MCP docs if not explicitly deselected and we have MCP servers
        if auto_selected_mcp_docs and "mcp_docs" not in selected_components:
            # Check if user explicitly deselected it
            mcp_docs_index = len(framework_components)  # Index of mcp_docs in the menu
            if mcp_docs_index not in selections:
                # User didn't select it, but we auto-select it
                selected_components.append("mcp_docs")
                logger.info("設定されたサーバーのMCPドキュメントが自動選択されました")
        
        # Always include MCP component if servers were selected
        if selected_mcp_servers and "mcp" not in selected_components:
            selected_components.append("mcp")
        
        logger.info(f"選択されたフレームワークコンポーネント: {', '.join(selected_components)}")
        return selected_components
        
    except Exception as e:
        logger.error(f"フレームワークコンポーネントの選択中にエラーが発生しました: {e}")
        return ["core"]  # Fallback to core


def interactive_component_selection(registry: ComponentRegistry, config_manager: ConfigService) -> Optional[List[str]]:
    """2段階の対話型コンポーネント選択"""
    logger = get_logger()
    
    try:
        print(f"\n{Colors.CYAN}SuperClaude 対話的インストール{Colors.RESET}")
        print(f"{Colors.BLUE}2段階のプロセスでインストールするコンポーネントを選択してください:{Colors.RESET}")
        
        # Stage 1: MCP Server Selection
        selected_mcp_servers = select_mcp_servers(registry)
        
        # Stage 2: Framework Component Selection
        selected_components = select_framework_components(registry, config_manager, selected_mcp_servers)
        
        # Store selected MCP servers for components to use
        if not hasattr(config_manager, '_installation_context'):
            config_manager._installation_context = {}
        config_manager._installation_context["selected_mcp_servers"] = selected_mcp_servers
        
        return selected_components
        
    except Exception as e:
        logger.error(f"コンポーネントの選択中にエラーが発生しました: {e}")
        return None


def display_installation_plan(components: List[str], registry: ComponentRegistry, install_dir: Path) -> None:
    """インストール計画を表示します"""
    logger = get_logger()
    
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}インストール計画{Colors.RESET}")
    print("=" * 50)
    
    # Resolve dependencies
    try:
        ordered_components = registry.resolve_dependencies(components)
        
        print(f"{Colors.BLUE}インストールディレクトリ:{Colors.RESET} {install_dir}")
        print(f"{Colors.BLUE}インストールするコンポーネント:{Colors.RESET}")
        
        total_size = 0
        for i, component_name in enumerate(ordered_components, 1):
            metadata = registry.get_component_metadata(component_name)
            if metadata:
                description = metadata.get("description", "説明がありません")
                print(f"  {i}. {component_name} - {description}")
                
                # Get size estimate if component supports it
                try:
                    instance = registry.get_component_instance(component_name, install_dir)
                    if instance and hasattr(instance, 'get_size_estimate'):
                        size = instance.get_size_estimate()
                        total_size += size
                except Exception:
                    pass
            else:
                print(f"  {i}. {component_name} - 不明なコンポーネント")
        
        if total_size > 0:
            print(f"\n{Colors.BLUE}推定サイズ:{Colors.RESET} {format_size(total_size)}")
        
        print()
        
    except Exception as e:
        logger.error(f"依存関係を解決できませんでした: {e}")
        raise


def run_system_diagnostics(validator: Validator) -> None:
    """包括的なシステム診断を実行します"""
    logger = get_logger()
    
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}SuperClaude システム診断{Colors.RESET}")
    print("=" * 50)
    
    # Run diagnostics
    diagnostics = validator.diagnose_system()
    
    # Display platform info
    print(f"{Colors.BLUE}プラットフォーム:{Colors.RESET} {diagnostics['platform']}")
    
    # Display check results
    print(f"\n{Colors.BLUE}システムチェック:{Colors.RESET}")
    all_passed = True
    
    for check_name, check_info in diagnostics['checks'].items():
        status = check_info['status']
        message = check_info['message']
        
        if status == 'pass':
            print(f"  ✅ {check_name}: {message}")
        else:
            print(f"  ❌ {check_name}: {message}")
            all_passed = False
    
    # Display issues and recommendations
    if diagnostics['issues']:
        print(f"\n{Colors.YELLOW}問題が見つかりました:{Colors.RESET}")
        for issue in diagnostics['issues']:
            print(f"  ⚠️  {issue}")
        
        print(f"\n{Colors.CYAN}推奨事項:{Colors.RESET}")
        for recommendation in diagnostics['recommendations']:
            print(recommendation)
    
    # Summary
    if all_passed:
        print(f"\n{Colors.GREEN}✅ すべてのシステムチェックに合格しました！お使いのシステムはSuperClaudeの準備ができています。{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}⚠️ いくつかの問題が見つかりました。上記の推奨事項に対処してください。{Colors.RESET}")
    
    print(f"\n{Colors.BLUE}次のステップ:{Colors.RESET}")
    if all_passed:
        print("  1. 'SuperClaude install' を実行してインストールを続行してください")
        print("  2. お好みのインストールモード（クイック、最小、またはカスタム）を選択してください")
    else:
        print("  1. 上記のコマンドを使用して、不足している依存関係をインストールしてください")
        print("  2. ツールをインストールした後、ターミナルを再起動してください")
        print("  3. 'SuperClaude install --diagnose' を再度実行して確認してください")


def perform_installation(components: List[str], args: argparse.Namespace, config_manager: ConfigService = None) -> bool:
    """実際のインストールを実行します"""
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
        
        # Register components with installer
        installer.register_components(list(component_instances.values()))
        
        # Resolve dependencies
        ordered_components = registry.resolve_dependencies(components)
        
        # Setup progress tracking
        progress = ProgressBar(
            total=len(ordered_components),
            prefix="インストール中: ",
            suffix=""
        )
        
        # Install components
        logger.info(f"{len(ordered_components)}個のコンポーネントをインストール中...")
        
        config = {
            "force": args.force,
            "backup": not args.no_backup,
            "dry_run": args.dry_run,
            "selected_mcp_servers": getattr(config_manager, '_installation_context', {}).get("selected_mcp_servers", [])
        }
        
        success = installer.install_components(ordered_components, config)
        
        # Update progress
        for i, component_name in enumerate(ordered_components):
            if component_name in installer.installed_components:
                progress.update(i + 1, f"インストール済み {component_name}")
            else:
                progress.update(i + 1, f"失敗 {component_name}")
            time.sleep(0.1)  # Brief pause for visual effect
        
        progress.finish("インストール完了")
        
        # Show results
        duration = time.time() - start_time
        
        if success:
            logger.success(f"インストールが{duration:.1f}秒で正常に完了しました")
            
            # Show summary
            summary = installer.get_installation_summary()
            if summary['installed']:
                logger.info(f"インストールされたコンポーネント: {', '.join(summary['installed'])}")
            
            if summary['backup_path']:
                logger.info(f"バックアップが作成されました: {summary['backup_path']}")
                
        else:
            logger.error(f"{duration:.1f}秒でエラーが発生してインストールが完了しました")
            
            summary = installer.get_installation_summary()
            if summary['failed']:
                logger.error(f"失敗したコンポーネント: {', '.join(summary['failed'])}")
        
        return success
        
    except Exception as e:
        logger.exception(f"インストール中に予期しないエラーが発生しました: {e}")
        return False


def run(args: argparse.Namespace) -> int:
    """解析された引数でインストール操作を実行します"""
    operation = InstallOperation()
    operation.setup_operation_logging(args)
    logger = get_logger()
    # ✅ Enhanced security validation with symlink protection
    expected_home = Path.home().resolve()
    install_dir_original = args.install_dir
    install_dir_resolved = args.install_dir.resolve()

    # Check for symlink attacks - compare original vs resolved paths
    try:
        # Verify the resolved path is still within user home
        install_dir_resolved.relative_to(expected_home)
        
        # Additional check: if there's a symlink in the path, verify it doesn't escape user home
        if install_dir_original != install_dir_resolved:
            # Path contains symlinks - verify each component stays within user home
            current_path = expected_home
            parts = install_dir_original.parts
            home_parts = expected_home.parts
            
            # Skip home directory parts
            if len(parts) >= len(home_parts) and parts[:len(home_parts)] == home_parts:
                relative_parts = parts[len(home_parts):]
                
                for part in relative_parts:
                    current_path = current_path / part
                    if current_path.is_symlink():
                        symlink_target = current_path.resolve()
                        # Ensure symlink target is also within user home
                        symlink_target.relative_to(expected_home)
    except ValueError:
        print(f"\n[✗] インストールはユーザープロファイルディレクトリ内で行う必要があります。")
        print(f"    期待されるプレフィックス: {expected_home}")
        print(f"    指定されたパス:   {install_dir_resolved}")
        print(f"    セキュリティ: ユーザーディレクトリ外へのシンボリックリンクは許可されていません。")
        sys.exit(1)
    except Exception as e:
        print(f"\n[✗] セキュリティ検証に失敗しました: {e}")
        print(f"    ユーザープロファイル内の標準的なディレクトリパスを使用してください。")
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
            from setup.cli.base import __version__
            display_header(
                f"SuperClaude インストール v{__version__}",
                "SuperClaudeフレームワークコンポーネントをインストール中"
            )
        
        # Handle special modes
        if args.list_components:
            registry = ComponentRegistry(PROJECT_ROOT / "setup" / "components")
            registry.discover_components()
            
            components = registry.list_components()
            if components:
                print(f"\n{Colors.CYAN}利用可能なコンポーネント:{Colors.RESET}")
                for component_name in components:
                    metadata = registry.get_component_metadata(component_name)
                    if metadata:
                        desc = metadata.get("description", "説明がありません")
                        category = metadata.get("category", "不明")
                        print(f"  {component_name} ({category}) - {desc}")
                    else:
                        print(f"  {component_name} - 不明なコンポーネント")
            else:
                print("コンポーネントが見つかりません")
            return 0
        
        # Handle diagnostic mode
        if args.diagnose:
            validator = Validator()
            run_system_diagnostics(validator)
            return 0
        
        # Create component registry and load configuration
        logger.info("インストールシステムを初期化中...")
        
        registry = ComponentRegistry(PROJECT_ROOT / "setup" / "components")
        registry.discover_components()
        
        config_manager = ConfigService(DATA_DIR)
        validator = Validator()
        
        # Validate configuration
        config_errors = config_manager.validate_config_files()
        if config_errors:
            logger.error("設定の検証に失敗しました:")
            for error in config_errors:
                logger.error(f"  - {error}")
            return 1
        
        # Get components to install
        components = get_components_to_install(args, registry, config_manager)
        if not components:
            logger.error("インストールするコンポーネントが選択されていません")
            return 1
        
        # Validate system requirements
        if not validate_system_requirements(validator, components):
            if not args.force:
                logger.error("システム要件が満たされていません。--forceを使用して上書きしてください。")
                return 1
            else:
                logger.warning("システム要件が満たされていませんが、--forceフラグのため続行します")
        
        # Check for existing installation
        if args.install_dir.exists() and not args.force:
            if not args.dry_run:
                logger.warning(f"インストールディレクトリは既に存在します: {args.install_dir}")
                if not args.yes and not confirm("既存のインストールを続行して更新しますか？", default=False):
                    logger.info("ユーザーによってインストールがキャンセルされました")
                    return 0
        
        # Display installation plan
        if not args.quiet:
            display_installation_plan(components, registry, args.install_dir)
            
            if not args.dry_run:
                if not args.yes and not confirm("インストールを続行しますか？", default=True):
                    logger.info("ユーザーによってインストールがキャンセルされました")
                    return 0
        
        # Perform installation
        success = perform_installation(components, args, config_manager)
        
        if success:
            if not args.quiet:
                display_success("SuperClaudeのインストールが正常に完了しました！")
                
                if not args.dry_run:
                    print(f"\n{Colors.CYAN}次のステップ:{Colors.RESET}")
                    print(f"1. Claude Codeセッションを再起動してください")
                    print(f"2. フレームワークファイルが{args.install_dir}で利用可能になりました")
                    print(f"3. Claude CodeでSuperClaudeのコマンドと機能を使用してください")
                    
            return 0
        else:
            display_error("インストールに失敗しました。詳細はログを確認してください。")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}ユーザーによってインストールがキャンセルされました{Colors.RESET}")
        return 130
    except Exception as e:
        return operation.handle_operation_error("install", e)
