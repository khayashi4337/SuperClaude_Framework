"""
SuperClaudeの環境変数管理
永続的な環境変数を設定するためのクロスプラットフォームユーティリティ
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from .ui import display_info, display_success, display_warning, Colors
from .logger import get_logger


def _get_env_tracking_file() -> Path:
    """環境変数追跡ファイルへのパスを取得"""
    from .. import DEFAULT_INSTALL_DIR
    install_dir = Path.home() / ".claude"
    install_dir.mkdir(exist_ok=True)
    return install_dir / "superclaude_env_vars.json"


def _load_env_tracking() -> Dict[str, Dict[str, str]]:
    """環境変数追跡データを読み込み"""
    tracking_file = _get_env_tracking_file()
    
    try:
        if tracking_file.exists():
            with open(tracking_file, 'r') as f:
                return json.load(f)
    except Exception as e:
        get_logger().warning(f"環境追跡を読み込めませんでした: {e}")
    
    return {}


def _save_env_tracking(tracking_data: Dict[str, Dict[str, str]]) -> bool:
    """環境変数追跡データを保存"""
    tracking_file = _get_env_tracking_file()
    
    try:
        with open(tracking_file, 'w') as f:
            json.dump(tracking_data, f, indent=2)
        return True
    except Exception as e:
        get_logger().error(f"環境追跡を保存できませんでした: {e}")
        return False


def _add_env_tracking(env_vars: Dict[str, str]) -> None:
    """環境変数を追跡に追加"""
    if not env_vars:
        return
    
    tracking_data = _load_env_tracking()
    timestamp = datetime.now().isoformat()
    
    for env_var, value in env_vars.items():
        tracking_data[env_var] = {
            "set_by": "superclaude",
            "timestamp": timestamp,
            "value_hash": str(hash(value))  # Store hash, not actual value for security
        }
    
    _save_env_tracking(tracking_data)
    get_logger().info(f"追加済み {len(env_vars)} 環境変数を追跡へ")


def _remove_env_tracking(env_vars: list) -> None:
    """環境変数を追跡から削除"""
    if not env_vars:
        return
    
    tracking_data = _load_env_tracking()
    
    for env_var in env_vars:
        if env_var in tracking_data:
            del tracking_data[env_var]
    
    _save_env_tracking(tracking_data)
    get_logger().info(f"削除済み {len(env_vars)} 環境変数を追跡から")


def detect_shell_config() -> Optional[Path]:
    """
    ユーザーのシェル設定ファイルを検出します
    
    Returns:
        シェル設定ファイルへのパス、見つからない場合はNone
    """
    home = Path.home()
    
    # Check in order of preference
    configs = [
        home / ".zshrc",        # Zsh (Mac default)
        home / ".bashrc",       # Bash
        home / ".profile",      # Generic shell profile
        home / ".bash_profile"  # Mac Bash profile
    ]
    
    for config in configs:
        if config.exists():
            return config
    
    # Default to .bashrc if none exist (will be created)
    return home / ".bashrc"


def setup_environment_variables(api_keys: Dict[str, str]) -> bool:
    """
    プラットフォーム間で環境変数を設定します
    
    Args:
        api_keys: 環境変数名と値の辞書
        
    Returns:
        すべての変数が正常に設定された場合はTrue、それ以外はFalse
    """
    logger = get_logger()
    success = True
    
    if not api_keys:
        return True
    
    print(f"\n{Colors.BLUE}[情報] 環境変数を設定中...{Colors.RESET}")
    
    for env_var, value in api_keys.items():
        try:
            # Set for current session
            os.environ[env_var] = value
            
            if os.name == 'nt':  # Windows
                # Use setx for persistent user variable
                result = subprocess.run(
                    ['setx', env_var, value],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    display_warning(f"設定できませんでした {env_var} を永続的に: {result.stderr.strip()}")
                    success = False
                else:
                    logger.info(f"Windows環境変数 {env_var} を永続的に設定")
            else:  # Unix-like systems
                shell_config = detect_shell_config()
                
                # Check if the export already exists
                export_line = f'export {env_var}="{value}"'
                
                try:
                    with open(shell_config, 'r') as f:
                        content = f.read()
                    
                    # Check if this environment variable is already set
                    if f'export {env_var}=' in content:
                        # Variable exists - don't duplicate
                        logger.info(f"Environment variable {env_var} は既に存在します {shell_config.name}")
                    else:
                        # Append export to shell config
                        with open(shell_config, 'a') as f:
                            f.write(f'\n# SuperClaude API Key\n{export_line}\n')
                        
                        display_info(f"追加済み {env_var} to {shell_config.name}")
                        logger.info(f"追加済み {env_var} to {shell_config}")
                        
                except Exception as e:
                    display_warning(f"更新できませんでした {shell_config.name}: {e}")
                    success = False
            
            logger.info(f"Environment variable {env_var} が現在のセッション用に設定されました")
            
        except Exception as e:
            logger.error(f"設定に失敗しました {env_var}: {e}")
            display_warning(f"設定に失敗しました {env_var}: {e}")
            success = False
    
    if success:
        # Add to tracking
        _add_env_tracking(api_keys)
        
        display_success("環境変数が正常に設定されました")
        if os.name != 'nt':
            display_info("Restart your terminal or run 'source ~/.bashrc' to apply changes")
        else:
            display_info("新しい環境変数は新しいターミナルセッションで利用可能になります")
    else:
        display_warning("一部の環境変数を永続的に設定できませんでした")
        display_info("手動で設定するか、詳細についてログを確認できます")
    
    return success


def validate_environment_setup(env_vars: Dict[str, str]) -> bool:
    """
    環境変数が正しく設定されていることを検証します
    
    Args:
        env_vars: 環境変数名と期待値の辞書
        
    Returns:
        すべての変数が正しく設定されている場合はTrue、それ以外はFalse
    """
    logger = get_logger()
    all_valid = True
    
    for env_var, expected_value in env_vars.items():
        current_value = os.environ.get(env_var)
        
        if current_value is None:
            logger.warning(f"Environment variable {env_var} が設定されていません")
            all_valid = False
        elif current_value != expected_value:
            logger.warning(f"Environment variable {env_var} に予期しない値があります")
            all_valid = False
        else:
            logger.info(f"Environment variable {env_var} は正しく設定されています")
    
    return all_valid


def get_shell_name() -> str:
    """
    現在のシェルの名前を取得します
    
    Returns:
        シェルの名前 (例: 'bash', 'zsh', 'fish')
    """
    shell_path = os.environ.get('SHELL', '')
    if shell_path:
        return Path(shell_path).name
    return 'unknown'


def get_superclaude_environment_variables() -> Dict[str, str]:
    """
    SuperClaudeによって設定された環境変数を取得します
    
    Returns:
        環境変数名とその現在の値の辞書
    """
    # Load tracking data to get SuperClaude-managed variables
    tracking_data = _load_env_tracking()
    
    found_vars = {}
    for env_var, metadata in tracking_data.items():
        if metadata.get("set_by") == "superclaude":
            value = os.environ.get(env_var)
            if value:
                found_vars[env_var] = value
    
    # Fallback: check known SuperClaude API key environment variables
    # (for backwards compatibility with existing installations)
    known_superclaude_env_vars = [
        "TWENTYFIRST_API_KEY",  # Magic server
        "MORPH_API_KEY"         # Morphllm server
    ]
    
    for env_var in known_superclaude_env_vars:
        if env_var not in found_vars:
            value = os.environ.get(env_var)
            if value:
                found_vars[env_var] = value
    
    return found_vars


def cleanup_environment_variables(env_vars_to_remove: Dict[str, str], create_restore_script: bool = True) -> bool:
    """
    バックアップと復元オプションを使用して環境変数を安全に削除します
    
    Args:
        env_vars_to_remove: 削除する環境変数名の辞書
        create_restore_script: 変数を復元するスクリプトを作成するかどうか
        
    Returns:
        クリーンアップが成功した場合はTrue、それ以外はFalse
    """
    logger = get_logger()
    success = True
    
    if not env_vars_to_remove:
        return True
    
    # Create restore script if requested
    if create_restore_script:
        restore_script_path = _create_restore_script(env_vars_to_remove)
        if restore_script_path:
            display_info(f"復元スクリプトを作成しました: {restore_script_path}")
        else:
            display_warning("復元スクリプトを作成できませんでした")
    
    print(f"\n{Colors.BLUE}[情報] 環境変数を削除中...{Colors.RESET}")
    
    for env_var, value in env_vars_to_remove.items():
        try:
            # Remove を現在のセッションから
            if env_var in os.environ:
                del os.environ[env_var]
                logger.info(f"削除済み {env_var} を現在のセッションから")
            
            if os.name == 'nt':  # Windows
                # Remove persistent user variable using reg command
                result = subprocess.run(
                    ['reg', 'delete', 'HKCU\\Environment', '/v', env_var, '/f'],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    # Variable might not exist in registry, which is fine
                    logger.debug(f"レジストリ削除: {env_var}: {result.stderr.strip()}")
                else:
                    logger.info(f"削除済み {env_var} をWindowsレジストリから")
            else:  # Unix-like systems
                shell_config = detect_shell_config()
                if shell_config and shell_config.exists():
                    _remove_env_var_from_shell_config(shell_config, env_var)
                    
        except Exception as e:
            logger.error(f"削除に失敗しました {env_var}: {e}")
            display_warning(f"削除できませんでした {env_var}: {e}")
            success = False
    
    if success:
        # Remove から tracking
        _remove_env_tracking(list(env_vars_to_remove.keys()))
        
        display_success("環境変数が正常に削除されました")
        if os.name != 'nt':
            display_info("変更を適用するには、ターミナルを再起動するか、シェル設定を再読み込みしてください")
        else:
            display_info("変更は新しいターミナルセッションで有効になります")
    else:
        display_warning("一部の環境変数を削除できませんでした")
    
    return success


def _create_restore_script(env_vars: Dict[str, str]) -> Optional[Path]:
    """環境変数を復元するスクリプトを作成"""
    try:
        home = Path.home()
        if os.name == 'nt':  # Windows
            script_path = home / "restore_superclaude_env.bat"
            with open(script_path, 'w') as f:
                f.write("@echo off\n")
                f.write("REM SuperClaude Environment Variable Restore Script\n")
                f.write("REM Generated during uninstall\n\n")
                for env_var, value in env_vars.items():
                    f.write(f'setx {env_var} "{value}"\n')
                f.write("\necho Environment variables restored\n")
                f.write("pause\n")
        else:  # Unix-like
            script_path = home / "restore_superclaude_env.sh"
            with open(script_path, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write("# SuperClaude Environment Variable Restore Script\n")
                f.write("# Generated during uninstall\n\n")
                shell_config = detect_shell_config()
                for env_var, value in env_vars.items():
                    f.write(f'export {env_var}="{value}"\n')
                    if shell_config:
                        f.write(f'echo \'export {env_var}="{value}"\' >> {shell_config}\n')
                f.write("\necho 'Environment variables restored'\n")
            
            # Make script executable
            script_path.chmod(0o755)
        
        return script_path
        
    except Exception as e:
        get_logger().error(f"復元スクリプトの作成に失敗しました: {e}")
        return None


def _remove_env_var_from_shell_config(shell_config: Path, env_var: str) -> bool:
    """シェル設定ファイルから環境変数エクスポートを削除"""
    try:
        # Read current content
        with open(shell_config, 'r') as f:
            lines = f.readlines()
        
        # Filter out lines that export this variable
        filtered_lines = []
        skip_next_blank = False
        
        for line in lines:
            # Check if this line exports our variable
            if f'export {env_var}=' in line or line.strip() == f'# SuperClaude APIキー':
                skip_next_blank = True
                continue
            
            # Skip blank line after removed export
            if skip_next_blank and line.strip() == '':
                skip_next_blank = False
                continue
            
            skip_next_blank = False
            filtered_lines.append(line)
        
        # Write back the filtered content
        with open(shell_config, 'w') as f:
            f.writelines(filtered_lines)
        
        get_logger().info(f"削除済み {env_var} のエクスポート元 {shell_config.name}")
        return True
        
    except Exception as e:
        get_logger().error(f"削除に失敗しました {env_var} から {shell_config}: {e}")
        return False


def create_env_file(api_keys: Dict[str, str], env_file_path: Optional[Path] = None) -> bool:
    """
    APIキーを含む.envファイルを作成します（シェル設定の代替）
    
    Args:
        api_keys: 環境変数名と値の辞書
        env_file_path: .envファイルへのパス（デフォルトはホームディレクトリ）
        
    Returns:
        .envファイルが正常に作成された場合はTrue、それ以外はFalse
    """
    if env_file_path is None:
        env_file_path = Path.home() / ".env"
    
    logger = get_logger()
    
    try:
        # Read existing .env file if it exists
        existing_content = ""
        if env_file_path.exists():
            with open(env_file_path, 'r') as f:
                existing_content = f.read()
        
        # Prepare new content
        new_lines = []
        for env_var, value in api_keys.items():
            line = f'{env_var}="{value}"'
            
            # Check if this variable already exists
            if f'{env_var}=' in existing_content:
                logger.info(f"Variable {env_var} は既に.envファイルに存在します")
            else:
                new_lines.append(line)
        
        # Append new lines if any
        if new_lines:
            with open(env_file_path, 'a') as f:
                if existing_content and not existing_content.endswith('\n'):
                    f.write('\n')
                f.write('# SuperClaude API Keys\n')
                for line in new_lines:
                    f.write(line + '\n')
            
            # Set file permissions (readable only by owner)
            env_file_path.chmod(0o600)
            
            display_success(f".envファイルを次の場所に作成しました {env_file_path}")
            logger.info(f".envファイルを...で作成しました {len(new_lines)} 個の新しい変数")
        
        return True
        
    except Exception as e:
        logger.error(f".envファイルの作成に失敗しました: {e}")
        display_warning(f".envファイルを作成できませんでした: {e}")
        return False