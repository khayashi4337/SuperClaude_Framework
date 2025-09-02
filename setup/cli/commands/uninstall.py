"""
SuperClaude Uninstall Operation Module
Refactored from uninstall.py for unified CLI hub
"""

import sys
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
import argparse

from ...core.registry import ComponentRegistry
from ...services.settings import SettingsService
from ...services.files import FileService
from ...utils.ui import (
    display_header, display_info, display_success, display_error, 
    display_warning, Menu, confirm, ProgressBar, Colors
)
from ...utils.environment import get_superclaude_environment_variables, cleanup_environment_variables
from ...utils.logger import get_logger
from ... import DEFAULT_INSTALL_DIR, PROJECT_ROOT
from . import OperationBase


def verify_superclaude_file(file_path: Path, component: str) -> bool:
    """
    削除前にこれがSuperClaudeのファイルであることを確認
    
    Args:
        file_path: Path to the file to verify
        component: Component name this file belongs to
        
    Returns:
        安全に削除できる場合はTrue、不確かな場合はFalse（デフォルトで保持）
    """
    try:
        # コンポーネント別の既知のSuperClaudeファイルパターン
        superclaude_patterns = {
            'core': [
                'CLAUDE.md', 'FLAGS.md', 'PRINCIPLES.md', 'RULES.md', 
                'ORCHESTRATOR.md', 'SESSION_LIFECYCLE.md'
            ],
            'commands': [
                # コマンドはsc/サブディレクトリにのみ存在
            ],
            'agents': [
                'backend-engineer.md', 'brainstorm-PRD.md', 'code-educator.md',
                'code-refactorer.md', 'devops-engineer.md', 'frontend-specialist.md',
                'performance-optimizer.md', 'python-ultimate-expert.md', 'qa-specialist.md',
                'root-cause-analyzer.md', 'security-auditor.md', 'system-architect.md',
                'technical-writer.md'
            ],
            'modes': [
                'MODE_Brainstorming.md', 'MODE_Introspection.md', 
                'MODE_Task_Management.md', 'MODE_Token_Efficiency.md'
            ],
            'mcp_docs': [
                'MCP_Context7.md', 'MCP_Sequential.md', 'MCP_Magic.md',
                'MCP_Playwright.md', 'MCP_Morphllm.md', 'MCP_Serena.md'
            ]
        }
        
        # commandsコンポーネントの場合、sc/サブディレクトリにあることを確認
        if component == 'commands':
            return 'commands/sc/' in str(file_path)
        
        # 他のコンポーネントの場合、既知のファイルリストと照合
        if component in superclaude_patterns:
            filename = file_path.name
            return filename in superclaude_patterns[component]
        
        # MCPコンポーネントはファイルを削除せず、.claude.jsonを変更
        if component == 'mcp':
            return True  # MCPコンポーネントには独自の安全ロジックがあります
        
        # 不確かな場合はデフォルトで保持
        return False
        
    except Exception:
        # 検証中にエラーが発生した場合は、ファイルを保持
        return False


def verify_directory_safety(directory: Path, component: str) -> bool:
    """
    ディレクトリを安全に削除できることを確認
    
    Args:
        directory: Directory path to verify
        component: Component name
        
    Returns:
        安全に削除できる場合はTrue（空またはSuperClaudeファイルのみを含む場合）
    """
    try:
        if not directory.exists():
            return True
        
        # ディレクトリが空かどうかを確認
        contents = list(directory.iterdir())
        if not contents:
            return True
        
        # すべてのコンテンツがこのコンポーネントのSuperClaudeファイルであることを確認
        for item in contents:
            if item.is_file():
                if not verify_superclaude_file(item, component):
                    return False
            elif item.is_dir():
                # SuperClaude以外のサブディレクトリを含むディレクトリは削除しない
                return False
        
        return True
        
    except Exception:
        # エラーが発生した場合は、ディレクトリを保持
        return False


class UninstallOperation(OperationBase):
    """アンインストール操作の実装"""
    
    def __init__(self):
        super().__init__("uninstall")


def register_parser(subparsers, global_parser=None) -> argparse.ArgumentParser:
    """Register uninstall CLI arguments"""
    parents = [global_parser] if global_parser else []
    
    parser = subparsers.add_parser(
        "uninstall",
        help="SuperClaudeフレームワークのインストールを削除します",
        description="SuperClaudeフレームワークコンポーネントをアンインストールします",
        epilog="""
例:
  SuperClaude uninstall                    # 対話的なアンインストール
  SuperClaude uninstall --components core  # 特定のコンポーネントを削除
  SuperClaude uninstall --complete --force # 完全な削除（強制）
  SuperClaude uninstall --keep-backups     # バックアップファイルを保持
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parents
    )
    
    # Uninstall mode options
    parser.add_argument(
        "--components",
        type=str,
        nargs="+",
        help="アンインストールする特定のコンポーネント"
    )
    
    parser.add_argument(
        "--complete",
        action="store_true",
        help="完全なアンインストール（すべてのファイルとディレクトリを削除）"
    )
    
    # Data preservation options
    parser.add_argument(
        "--keep-backups",
        action="store_true",
        help="アンインストール中にバックアップファイルを保持します"
    )
    
    parser.add_argument(
        "--keep-logs",
        action="store_true",
        help="アンインストール中にログファイルを保持します"
    )
    
    parser.add_argument(
        "--keep-settings",
        action="store_true",
        help="アンインストール中にユーザー設定を保持します"
    )
    
    # Safety options
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="確認プロンプトをスキップします（注意して使用）"
    )
    
    # Environment cleanup options
    parser.add_argument(
        "--cleanup-env",
        action="store_true",
        help="SuperClaudeの環境変数を削除します"
    )
    
    parser.add_argument(
        "--no-restore-script",
        action="store_true",
        help="環境変数復元スクリプトの作成をスキップします"
    )
    
    return parser

def get_installed_components(install_dir: Path) -> Dict[str, Dict[str, Any]]:
    """現在インストールされているコンポーネントとそのバージョンを取得"""
    try:
        settings_manager = SettingsService(install_dir)
        return settings_manager.get_installed_components()
    except Exception:
        return {}


def get_installation_info(install_dir: Path) -> Dict[str, Any]:
    """詳細なインストール情報を取得"""
    info = {
        "install_dir": install_dir,
        "exists": False,
        "components": {},
        "directories": [],
        "files": [],
        "total_size": 0
    }
    
    if not install_dir.exists():
        return info
    
    info["exists"] = True
    info["components"] = get_installed_components(install_dir)
    
    # インストールディレクトリをスキャン
    try:
        for item in install_dir.rglob("*"):
            if item.is_file():
                info["files"].append(item)
                info["total_size"] += item.stat().st_size
            elif item.is_dir():
                info["directories"].append(item)
    except Exception:
        pass
    
    return info


def display_environment_info() -> Dict[str, str]:
    """SuperClaudeの環境変数を表示して返す"""
    env_vars = get_superclaude_environment_variables()
    
    if env_vars:
        print(f"\n{Colors.CYAN}{Colors.BRIGHT}環境変数{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.BLUE}SuperClaudeのAPIキー環境変数が見つかりました:{Colors.RESET}")
        for env_var, value in env_vars.items():
            # セキュリティのため、最初と最後の数文字のみ表示
            masked_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
            print(f"  {env_var}: {masked_value}")
        
        print(f"\n{Colors.YELLOW}注意: これらの環境変数は --cleanup-env を使用しない限り残ります{Colors.RESET}")
    else:
        print(f"\n{Colors.GREEN}SuperClaudeの環境変数が見つかりませんでした{Colors.RESET}")
    
    return env_vars


def display_uninstall_info(info: Dict[str, Any]) -> None:
    """アンインストール前にインストール情報を表示"""
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}現在のインストール{Colors.RESET}")
    print("=" * 50)
    
    if not info["exists"]:
        print(f"{Colors.YELLOW}SuperClaudeのインストールが見つかりません{Colors.RESET}")
        return
    
    print(f"{Colors.BLUE}インストールディレクトリ:{Colors.RESET} {info['install_dir']}")
    
    if info["components"]:
        print(f"{Colors.BLUE}インストール済みコンポーネント:{Colors.RESET}")
        for component, version in info["components"].items():
            print(f"  {component}: v{version}")
    
    print(f"{Colors.BLUE}ファイル数:{Colors.RESET} {len(info['files'])}")
    print(f"{Colors.BLUE}ディレクトリ数:{Colors.RESET} {len(info['directories'])}")
    
    if info["total_size"] > 0:
        from ...utils.ui import format_size
        print(f"{Colors.BLUE}合計サイズ:{Colors.RESET} {format_size(info['total_size'])}")
    
    print()


def get_components_to_uninstall(args: argparse.Namespace, installed_components: Dict[str, str]) -> Optional[List[str]]:
    """アンインストールするコンポーネントを決定"""
    logger = get_logger()
    
    # 完全なアンインストール
    if args.complete:
        return list(installed_components.keys())
    
    # 明示的に指定されたコンポーネント
    if args.components:
        # 指定されたコンポーネントがインストールされていることを検証
        invalid_components = [c for c in args.components if c not in installed_components]
        if invalid_components:
            logger.error(f"コンポーネントがインストールされていません: {invalid_components}")
            return None
        return args.components
    
    # 対話的な選択
    return interactive_uninstall_selection(installed_components)


def interactive_component_selection(installed_components: Dict[str, str], env_vars: Dict[str, str]) -> Optional[tuple]:
    """
    詳細なコンポーネントオプションを備えた強化された対話型選択
    
    Returns:
        (削除するコンポーネント, クリーンアップオプション)のタプル、またはキャンセルの場合はNone
    """
    if not installed_components:
        return []
    
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}SuperClaude アンインストールオプション{Colors.RESET}")
    print("=" * 60)
    
    # メインのアンインストールタイプの選択
    main_options = [
        "完全なアンインストール（すべてのSuperClaudeコンポーネントを削除）",
        "カスタムアンインストール（特定のコンポーネントを選択）",
        "アンインストールをキャンセル"
    ]
    
    print(f"\n{Colors.BLUE}アンインストールの種類を選択してください:{Colors.RESET}")
    main_menu = Menu("オプションを選択:", main_options)
    main_choice = main_menu.display()
    
    if main_choice == -1 or main_choice == 2:  # キャンセル
        return None
    elif main_choice == 0:  # 完全なアンインストール
        # 完全なアンインストール - すべてのコンポーネントとオプションのクリーンアップを含む
        cleanup_options = _ask_complete_uninstall_options(env_vars)
        return list(installed_components.keys()), cleanup_options
    elif main_choice == 1:  # カスタムアンインストール
        return _custom_component_selection(installed_components, env_vars)
    
    return None


def _ask_complete_uninstall_options(env_vars: Dict[str, str]) -> Dict[str, bool]:
    """完全なアンインストールオプションを尋ねる"""
    cleanup_options = {
        'remove_mcp_configs': True,
        'cleanup_env_vars': False,
        'create_restore_script': True
    }
    
    print(f"\n{Colors.YELLOW}{Colors.BRIGHT}完全なアンインストールオプション{Colors.RESET}")
    print("これにより、すべてのSuperClaudeコンポーネントが削除されます。")
    
    if env_vars:
        print(f"\n{Colors.BLUE}環境変数が見つかりました:{Colors.RESET}")
        for env_var, value in env_vars.items():
            masked_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
            print(f"  {env_var}: {masked_value}")
        
        cleanup_env = confirm("APIキーの環境変数も削除しますか？", default=False)
        cleanup_options['cleanup_env_vars'] = cleanup_env
        
        if cleanup_env:
            create_script = confirm("環境変数の復元スクリプトを作成しますか？", default=True)
            cleanup_options['create_restore_script'] = create_script
    
    return cleanup_options


def _custom_component_selection(installed_components: Dict[str, str], env_vars: Dict[str, str]) -> Optional[tuple]:
    """詳細オプション付きのカスタムコンポーネント選択を処理"""
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}カスタムアンインストール - コンポーネントの選択{Colors.RESET}")
    print("削除するSuperClaudeコンポーネントを選択してください:")
    
    # 説明付きのコンポーネントオプションを構築
    component_options = []
    component_keys = []
    
    component_descriptions = {
        'core': 'コアフレームワークファイル (CLAUDE.md, FLAGS.md, PRINCIPLES.md, など)',
        'commands': 'SuperClaudeコマンド (commands/sc/*.md)',
        'agents': '専門エージェント (agents/*.md)',
        'mcp': 'MCPサーバー設定',
        'mcp_docs': 'MCPドキュメント',
        'modes': 'SuperClaudeモード'
    }
    
    for component, version in installed_components.items():
        description = component_descriptions.get(component, f"{component} コンポーネント")
        component_options.append(f"{description}")
        component_keys.append(component)
    
    print(f"\n{Colors.BLUE}削除するコンポーネントを選択してください:{Colors.RESET}")
    component_menu = Menu("コンポーネント:", component_options, multi_select=True)
    selections = component_menu.display()
    
    if not selections:
        return None
    
    selected_components = [component_keys[i] for i in selections]
    
    # MCPコンポーネントが選択された場合、関連するクリーンアップオプションを尋ねる
    cleanup_options = {
        'remove_mcp_configs': 'mcp' in selected_components,
        'cleanup_env_vars': False,
        'create_restore_script': True
    }
    
    if 'mcp' in selected_components:
        cleanup_options.update(_ask_mcp_cleanup_options(env_vars))
    elif env_vars:
        # MCPが選択されていなくても、env varが存在する場合は尋ねる
        cleanup_env = confirm(f"{len(env_vars)}個のAPIキー環境変数を削除しますか？", default=False)
        cleanup_options['cleanup_env_vars'] = cleanup_env
        if cleanup_env:
            create_script = confirm("環境変数の復元スクリプトを作成しますか？", default=True)
            cleanup_options['create_restore_script'] = create_script
    
    return selected_components, cleanup_options


def _ask_mcp_cleanup_options(env_vars: Dict[str, str]) -> Dict[str, bool]:
    """MCP関連のクリーンアップオプションを尋ねる"""
    print(f"\n{Colors.YELLOW}{Colors.BRIGHT}MCPクリーンアップオプション{Colors.RESET}")
    print("MCPコンポーネントを削除するため:")
    
    cleanup_options = {}
    
    # MCPサーバー設定について尋ねる
    remove_configs = confirm(".claude.jsonからMCPサーバー設定を削除しますか？", default=True)
    cleanup_options['remove_mcp_configs'] = remove_configs
    
    # APIキー環境変数について尋ねる
    if env_vars:
        print(f"\n{Colors.BLUE}関連するAPIキー環境変数が見つかりました:{Colors.RESET}")
        for env_var, value in env_vars.items():
            masked_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
            print(f"  {env_var}: {masked_value}")
        
        cleanup_env = confirm(f"{len(env_vars)}個のAPIキー環境変数を削除しますか？", default=False)
        cleanup_options['cleanup_env_vars'] = cleanup_env
        
        if cleanup_env:
            create_script = confirm("環境変数の復元スクリプトを作成しますか？", default=True)
            cleanup_options['create_restore_script'] = create_script
        else:
            cleanup_options['create_restore_script'] = True
    else:
        cleanup_options['cleanup_env_vars'] = False
        cleanup_options['create_restore_script'] = True
    
    return cleanup_options


def interactive_uninstall_selection(installed_components: Dict[str, str]) -> Optional[List[str]]:
    """レガシー関数 - 強化された選択にリダイレクト"""
    env_vars = get_superclaude_environment_variables()
    result = interactive_component_selection(installed_components, env_vars)
    
    if result is None:
        return None
    
    # 下位互換性のため、コンポーネントリストのみを返す
    components, cleanup_options = result
    return components


def display_preservation_info() -> None:
    """削除されないもの（ユーザーのカスタムファイル）を表示"""
    print(f"\n{Colors.GREEN}{Colors.BRIGHT}保持されるファイル:{Colors.RESET}")
    print(f"{Colors.GREEN}✓ ユーザーのカスタムコマンド（commands/sc/にないもの）{Colors.RESET}")
    print(f"{Colors.GREEN}✓ ユーザーのカスタムエージェント（SuperClaudeエージェントではないもの）{Colors.RESET}")
    print(f"{Colors.GREEN}✓ ユーザーのカスタム.claude.json設定{Colors.RESET}")
    print(f"{Colors.GREEN}✓ 共有ディレクトリ内のユーザーのカスタムファイル{Colors.RESET}")
    print(f"{Colors.GREEN}✓ Claude Codeの設定および他のツールの設定{Colors.RESET}")


def display_component_details(component: str, info: Dict[str, Any]) -> Dict[str, Any]:
    """コンポーネントで削除されるものの詳細情報を取得"""
    details = {
        'files': [],
        'directories': [],
        'size': 0,
        'description': ''
    }
    
    install_dir = info['install_dir']
    
    component_paths = {
        'core': {
            'files': ['CLAUDE.md', 'FLAGS.md', 'PRINCIPLES.md', 'RULES.md', 'ORCHESTRATOR.md', 'SESSION_LIFECYCLE.md'],
            'description': '~/.claude/内のコアフレームワークファイル'
        },
        'commands': {
            'files': 'commands/sc/*.md',
            'description': '~/.claude/commands/sc/内のSuperClaudeコマンド'
        },
        'agents': {
            'files': 'agents/*.md',
            'description': '~/.claude/agents/内の専門AIエージェント'
        },
        'mcp': {
            'files': '.claude.json内のMCPサーバー設定',
            'description': 'MCPサーバー設定'
        },
        'mcp_docs': {
            'files': 'MCP/*.md',
            'description': 'MCPドキュメントファイル'
        },
        'modes': {
            'files': 'MODE_*.md',
            'description': 'SuperClaude運用モード'
        }
    }
    
    if component in component_paths:
        details['description'] = component_paths[component]['description']
        
        # 利用可能な場合はメタデータから実際のファイル数を取得
        component_metadata = info["components"].get(component, {})
        if isinstance(component_metadata, dict):
            if 'files_count' in component_metadata:
                details['file_count'] = component_metadata['files_count']
            elif 'agents_count' in component_metadata:
                details['file_count'] = component_metadata['agents_count']
            elif 'servers_configured' in component_metadata:
                details['file_count'] = component_metadata['servers_configured']
    
    return details


def display_uninstall_plan(components: List[str], args: argparse.Namespace, info: Dict[str, Any], env_vars: Dict[str, str]) -> None:
    """詳細なアンインストール計画を表示"""
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}アンインストール計画{Colors.RESET}")
    print("=" * 60)
    
    print(f"{Colors.BLUE}インストールディレクトリ:{Colors.RESET} {info['install_dir']}")
    
    if components:
        print(f"\n{Colors.BLUE}削除するコンポーネント:{Colors.RESET}")
        total_files = 0
        
        for i, component_name in enumerate(components, 1):
            details = display_component_details(component_name, info)
            version = info["components"].get(component_name, "unknown")
            
            if isinstance(version, dict):
                version_str = version.get('version', 'unknown')
                file_count = details.get('file_count', version.get('files_count', version.get('agents_count', version.get('servers_configured', '?'))))
            else:
                version_str = str(version)
                file_count = details.get('file_count', '?')
            
            print(f"  {i}. {component_name} (v{version_str}) - {file_count} ファイル")
            print(f"     {details['description']}")
            
            if isinstance(file_count, int):
                total_files += file_count
        
        print(f"\n{Colors.YELLOW}削除されるファイルの推定合計数: {total_files}{Colors.RESET}")
    
    # 詳細な保存情報を表示
    print(f"\n{Colors.GREEN}{Colors.BRIGHT}安全保証 - 保持されるもの:{Colors.RESET}")
    print(f"{Colors.GREEN}✓ ユーザーのカスタムコマンド（commands/sc/にないもの）{Colors.RESET}")
    print(f"{Colors.GREEN}✓ ユーザーのカスタムエージェント（SuperClaudeエージェントではないもの）{Colors.RESET}")
    print(f"{Colors.GREEN}✓ ユーザーの.claude.jsonのカスタマイズ{Colors.RESET}")
    print(f"{Colors.GREEN}✓ Claude Codeの設定および他のツールの設定{Colors.RESET}")
    
    # 追加の保存項目を表示
    preserved = []
    if args.keep_backups:
        preserved.append("バックアップファイル")
    if args.keep_logs:
        preserved.append("ログファイル")
    if args.keep_settings:
        preserved.append("ユーザー設定")
    
    if preserved:
        for item in preserved:
            print(f"{Colors.GREEN}✓ {item}{Colors.RESET}")
    
    if args.complete:
        print(f"\n{Colors.RED}⚠️  警告: 完全なアンインストールはすべてのSuperClaudeファイルを削除します{Colors.RESET}")
    
    # 環境変数のクリーンアップ情報を表示
    if env_vars:
        print(f"\n{Colors.BLUE}環境変数:{Colors.RESET}")
        if args.cleanup_env:
            print(f"{Colors.YELLOW}{len(env_vars)}個のAPIキー環境変数を削除します:{Colors.RESET}")
            for env_var in env_vars.keys():
                print(f"  - {env_var}")
            if not args.no_restore_script:
                print(f"{Colors.GREEN}  ✓ 復元スクリプトが作成されます{Colors.RESET}")
        else:
            print(f"{Colors.BLUE}{len(env_vars)}個のAPIキー環境変数を保持します:{Colors.RESET}")
            for env_var in env_vars.keys():
                print(f"  ✓ {env_var}")
    
    print()


def create_uninstall_backup(install_dir: Path, components: List[str]) -> Optional[Path]:
    """アンインストール前にバックアップを作成"""
    logger = get_logger()
    
    try:
        from datetime import datetime
        backup_dir = install_dir / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"pre_uninstall_{timestamp}.tar.gz"
        backup_path = backup_dir / backup_name
        
        import tarfile
        
        logger.info(f"アンインストールバックアップを作成中: {backup_path}")
        
        with tarfile.open(backup_path, "w:gz") as tar:
            for component in components:
                # バックアップにコンポーネントファイルを追加
                settings_manager = SettingsService(install_dir)
                # これにはコンポーネント固有のバックアップロジックが必要
                pass
        
        logger.success(f"バックアップが作成されました: {backup_path}")
        return backup_path
        
    except Exception as e:
        logger.warning(f"バックアップを作成できませんでした: {e}")
        return None


def perform_uninstall(components: List[str], args: argparse.Namespace, info: Dict[str, Any], env_vars: Dict[str, str]) -> bool:
    """実際のアンインストールを実行"""
    logger = get_logger()
    start_time = time.time()
    
    try:
        # コンポーネントレジストリを作成
        registry = ComponentRegistry(PROJECT_ROOT / "setup" / "components")
        registry.discover_components()
        
        # コンポーネントインスタンスを作成
        component_instances = registry.create_component_instances(components, args.install_dir)
        
        # 進捗追跡を設定
        progress = ProgressBar(
            total=len(components),
            prefix="アンインストール中: ",
            suffix=""
        )
        
        # コンポーネントをアンインストール
        logger.info(f"{len(components)}個のコンポーネントをアンインストール中...")
        
        uninstalled_components = []
        failed_components = []
        
        for i, component_name in enumerate(components):
            progress.update(i, f"アンインストール中 {component_name}")
            
            try:
                if component_name in component_instances:
                    instance = component_instances[component_name]
                    if instance.uninstall():
                        uninstalled_components.append(component_name)
                        logger.debug(f"{component_name}を正常にアンインストールしました")
                    else:
                        failed_components.append(component_name)
                        logger.error(f"{component_name}のアンインストールに失敗しました")
                else:
                    logger.warning(f"コンポーネント {component_name} が見つかりません。スキップします")
                    
            except Exception as e:
                logger.error(f"{component_name}のアンインストール中にエラーが発生しました: {e}")
                failed_components.append(component_name)
            
            progress.update(i + 1, f"処理済み {component_name}")
            time.sleep(0.1)  # 視覚効果のための短い一時停止
        
        progress.finish("アンインストール完了")
        
        # 完全なアンインストールのクリーンアップを処理
        if args.complete:
            cleanup_installation_directory(args.install_dir, args)
        
        # 環境変数のクリーンアップを処理
        env_cleanup_success = True
        if args.cleanup_env and env_vars:
            logger.info("環境変数をクリーンアップ中...")
            create_restore_script = not args.no_restore_script
            env_cleanup_success = cleanup_environment_variables(env_vars, create_restore_script)
            
            if env_cleanup_success:
                logger.success(f"{len(env_vars)}個の環境変数を削除しました")
            else:
                logger.warning("一部の環境変数を削除できませんでした")
        
        # 結果を表示
        duration = time.time() - start_time
        
        if failed_components:
            logger.warning(f"アンインストールは{duration:.1f}秒でいくつかの失敗とともに完了しました")
            logger.warning(f"失敗したコンポーネント: {', '.join(failed_components)}")
        else:
            logger.success(f"アンインストールが{duration:.1f}秒で正常に完了しました")
        
        if uninstalled_components:
            logger.info(f"アンインストールされたコンポーネント: {', '.join(uninstalled_components)}")
        
        return len(failed_components) == 0
        
    except Exception as e:
        logger.exception(f"アンインストール中に予期しないエラーが発生しました: {e}")
        return False


def cleanup_installation_directory(install_dir: Path, args: argparse.Namespace) -> None:
    """完全なアンインストールのためにインストールディレクトリをクリーンアップ"""
    logger = get_logger()
    file_manager = FileService()
    
    try:
        # 要求された場合、特定のディレクトリ/ファイルを保持
        preserve_patterns = []
        
        if args.keep_backups:
            preserve_patterns.append("backups/*")
        if args.keep_logs:
            preserve_patterns.append("logs/*")
        if args.keep_settings and not args.complete:
            preserve_patterns.append("settings.json")
        
        # インストールディレクトリの内容を削除
        if args.complete and not preserve_patterns:
            # 完全な削除
            if file_manager.remove_directory(install_dir):
                logger.info(f"インストールディレクトリを削除しました: {install_dir}")
            else:
                logger.warning(f"インストールディレクトリを削除できませんでした: {install_dir}")
        else:
            # 選択的な削除
            for item in install_dir.iterdir():
                should_preserve = False
                
                for pattern in preserve_patterns:
                    if item.match(pattern):
                        should_preserve = True
                        break
                
                if not should_preserve:
                    if item.is_file():
                        file_manager.remove_file(item)
                    elif item.is_dir():
                        file_manager.remove_directory(item)
                        
    except Exception as e:
        logger.error(f"クリーンアップ中にエラーが発生しました: {e}")


def run(args: argparse.Namespace) -> int:
    """解析された引数でアンインストール操作を実行"""
    operation = UninstallOperation()
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
                f"SuperClaude アンインストール v{__version__}",
                "SuperClaudeフレームワークコンポーネントを削除中"
            )
        
        # インストール情報を取得
        info = get_installation_info(args.install_dir)
        
        # 現在のインストールを表示
        if not args.quiet:
            display_uninstall_info(info)
        
        # 環境変数を確認
        env_vars = display_environment_info() if not args.quiet else get_superclaude_environment_variables()
        
        # SuperClaudeがインストールされているか確認
        if not info["exists"]:
            logger.warning(f"{args.install_dir}にSuperClaudeのインストールが見つかりません")
            return 0
        
        # 強化された選択を使用してアンインストールするコンポーネントを取得
        if args.components or args.complete:
            # 非対話モード - 既存のロジックを使用
            components = get_components_to_uninstall(args, info["components"])
            cleanup_options = {
                'remove_mcp_configs': 'mcp' in (components or []),
                'cleanup_env_vars': args.cleanup_env,
                'create_restore_script': not args.no_restore_script
            }
            if components is None:
                logger.info("ユーザーによってアンインストールがキャンセルされました")
                return 0
            elif not components:
                logger.info("アンインストールするコンポーネントが選択されていません")
                return 0
        else:
            # 対話モード - 強化された選択を使用
            result = interactive_component_selection(info["components"], env_vars)
            if result is None:
                logger.info("ユーザーによってアンインストールがキャンセルされました")
                return 0
            elif not result:
                logger.info("アンインストールするコンポーネントが選択されていません")
                return 0
            
            components, cleanup_options = result
            
            # 対話型の選択でコマンドライン引数を上書き
            args.cleanup_env = cleanup_options.get('cleanup_env_vars', False)
            args.no_restore_script = not cleanup_options.get('create_restore_script', True)
        
        # アンインストール計画を表示
        if not args.quiet:
            display_uninstall_plan(components, args, info, env_vars)
        
        # 確認
        if not args.no_confirm and not args.yes:
            if args.complete:
                warning_msg = "これによりSuperClaudeが完全に削除されます。続行しますか？"
            else:
                warning_msg = f"これにより{len(components)}個のコンポーネントが削除されます。続行しますか？"
            
            if not confirm(warning_msg, default=False):
                logger.info("ユーザーによってアンインストールがキャンセルされました")
                return 0
        
        # ドライランでなく、バックアップを保持しない場合はバックアップを作成
        if not args.dry_run and not args.keep_backups:
            create_uninstall_backup(args.install_dir, components)
        
        # アンインストールを実行
        success = perform_uninstall(components, args, info, env_vars)
        
        if success:
            if not args.quiet:
                display_success("SuperClaudeのアンインストールが正常に完了しました！")
                
                if not args.dry_run:
                    print(f"\n{Colors.CYAN}アンインストール完了:{Colors.RESET}")
                    print(f"SuperClaudeが{args.install_dir}から削除されました")
                    if not args.complete:
                        print(f"'SuperClaude install'を使用していつでも再インストールできます")
                    
            return 0
        else:
            display_error("アンインストールはいくつかの失敗で完了しました。詳細はログを確認してください。")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}ユーザーによってアンインストールがキャンセルされました{Colors.RESET}")
        return 130
    except Exception as e:
        return operation.handle_operation_error("uninstall", e)
