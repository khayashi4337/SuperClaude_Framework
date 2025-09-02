"""
MCP component for MCP server configuration via .claude.json
"""

import json
import shutil
import time
import sys
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

# Platform-specific file locking imports
try:
    if sys.platform == "win32":
        import msvcrt
        LOCKING_AVAILABLE = "windows"
    else:
        import fcntl
        LOCKING_AVAILABLE = "unix"
except ImportError:
    LOCKING_AVAILABLE = None

from ..core.base import Component
from setup import __version__
from ..utils.ui import display_info, display_warning


class MCPComponent(Component):
    """MCPサーバー設定コンポーネント"""
    
    def __init__(self, install_dir: Optional[Path] = None):
        """MCPコンポーネントを初期化"""
        super().__init__(install_dir)
        
        # Define MCP servers available for configuration
        self.mcp_servers = {
            "context7": {
                "name": "context7",
                "description": "公式ライブラリのドキュメントとコード例",
                "config_file": "context7.json",
                "requires_api_key": False
            },
            "sequential": {
                "name": "sequential-thinking", 
                "description": "多段階の問題解決と体系的な分析",
                "config_file": "sequential.json",
                "requires_api_key": False
            },
            "magic": {
                "name": "magic",
                "description": "最新のUIコンポーネント生成とデザインシステム",
                "config_file": "magic.json",
                "requires_api_key": True,
                "api_key_env": "TWENTYFIRST_API_KEY"
            },
            "playwright": {
                "name": "playwright",
                "description": "クロスブラウザE2Eテストと自動化",
                "config_file": "playwright.json", 
                "requires_api_key": False
            },
            "serena": {
                "name": "serena",
                "description": "セマンティックなコード分析とインテリジェントな編集",
                "config_file": "serena.json",
                "requires_api_key": False
            },
            "morphllm": {
                "name": "morphllm-fast-apply",
                "description": "コンテキストに応じたコード修正のための高速適用機能",
                "config_file": "morphllm.json",
                "requires_api_key": True,
                "api_key_env": "MORPH_API_KEY"
            }
        }
        
        # This will be set during installation - initialize as empty list
        self.selected_servers: List[str] = []
        
        # Store collected API keys for configuration
        self.collected_api_keys: Dict[str, str] = {}
    
    def _lock_file(self, file_handle, exclusive: bool = False):
        """クロスプラットフォームのファイルロック"""
        if LOCKING_AVAILABLE == "unix":
            lock_type = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
            fcntl.flock(file_handle.fileno(), lock_type)
        elif LOCKING_AVAILABLE == "windows":
            # Windows locking using msvcrt
            if exclusive:
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_LOCK, 1)
        # If no locking available, continue without locking
    
    def _unlock_file(self, file_handle):
        """クロスプラットフォームのファイルロック解除"""
        if LOCKING_AVAILABLE == "unix":
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)
        elif LOCKING_AVAILABLE == "windows":
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
        # If no locking available, continue without unlocking
    
    def get_metadata(self) -> Dict[str, str]:
        """コンポーネントのメタデータを取得"""
        return {
            "name": "mcp",
            "version": __version__,
            "description": ".claude.jsonを介したMCPサーバー設定管理",
            "category": "integration"
        }
    
    def set_selected_servers(self, selected_servers: List[str]) -> None:
        """設定用に選択されたMCPサーバーを設定"""
        self.selected_servers = selected_servers
        self.logger.debug(f"設定するMCPサーバー: {selected_servers}")
    
    def validate_prerequisites(self, installSubPath: Optional[Path] = None) -> Tuple[bool, List[str]]:
        """
        MCPコンポーネントの前提条件を確認します
        """
        errors = []
        
        # Check if config source directory exists
        source_dir = self._get_config_source_dir()
        if not source_dir or not source_dir.exists():
            errors.append(f"MCP設定のソースディレクトリが見つかりません: {source_dir}")
            return False, errors
        
        # Check if user's Claude config exists
        claude_config = Path.home() / ".claude.json"
        if not claude_config.exists():
            errors.append(f"Claude設定ファイルが見つかりません: {claude_config}")
            errors.append("設定ファイルを作成するために、少なくとも一度Claude Codeを実行してください")
        
        return len(errors) == 0, errors
    
    def get_files_to_install(self) -> List[Tuple[Path, Path]]:
        """MCP component doesn't install files - it modifies .claude.json"""
        return []
    
    def _get_config_source_dir(self) -> Optional[Path]:
        """MCP設定ファイルのソースディレクトリを取得"""
        project_root = Path(__file__).parent.parent.parent
        config_dir = project_root / "SuperClaude" / "MCP" / "configs"
        
        if not config_dir.exists():
            return None
        
        return config_dir
    
    def _get_source_dir(self) -> Optional[Path]:
        """親メソッドをオーバーライド - MCPコンポーネントは従来のファイルインストールを使用しません"""
        return self._get_config_source_dir()
    
    def _load_claude_config(self) -> Tuple[Optional[Dict], Path]:
        """ファイルロック付きでユーザーのClaude設定を読み込み"""
        claude_config_path = Path.home() / ".claude.json"
        
        try:
            with open(claude_config_path, 'r') as f:
                # Apply shared lock for reading
                self._lock_file(f, exclusive=False)
                try:
                    config = json.load(f)
                    return config, claude_config_path
                finally:
                    self._unlock_file(f)
        except Exception as e:
            self.logger.error(f"Claude設定の読み込みに失敗しました: {e}")
            return None, claude_config_path
    
    def _save_claude_config(self, config: Dict, config_path: Path) -> bool:
        """バックアップとファイルロック付きでユーザーのClaude設定を保存"""
        max_retries = 3
        retry_delay = 0.1
        
        for attempt in range(max_retries):
            try:
                # Create backup first
                if config_path.exists():
                    backup_path = config_path.with_suffix('.json.backup')
                    shutil.copy2(config_path, backup_path)
                    self.logger.debug(f"バックアップを作成しました: {backup_path}")
                
                # Save updated config with exclusive lock
                with open(config_path, 'w') as f:
                    # Apply exclusive lock for writing
                    self._lock_file(f, exclusive=True)
                    try:
                        json.dump(config, f, indent=2)
                        f.flush()  # Ensure data is written
                    finally:
                        self._unlock_file(f)
                
                self.logger.debug("Claude設定を更新しました")
                return True
                
            except (OSError, IOError) as e:
                if attempt < max_retries - 1:
                    self.logger.warning(f"ファイルロック試行 {attempt + 1} が失敗しました。再試行中: {e}")
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    self.logger.error(f"{max_retries}回の試行の後、Claude設定の保存に失敗しました: {e}")
                    return False
            except Exception as e:
                self.logger.error(f"Claude設定の保存に失敗しました: {e}")
                return False
        
        return False
    
    def _merge_mcp_server_config(self, existing_config: Dict, new_config: Dict, server_key: str) -> None:
        """ユーザーのカスタマイズを保持しつつ、MCPサーバー設定を正確にマージします
        
        Args:
            existing_config: ユーザーの現在のmcpServers設定
            new_config: マージする新しいMCPサーバー設定
            server_key: ロギング用のサーバーキー
        """
        for server_name, server_def in new_config.items():
            if server_name in existing_config:
                # Server already exists - preserve user customizations
                existing_server = existing_config[server_name]
                
                # Only add missing keys, never overwrite existing ones
                for key, value in server_def.items():
                    if key not in existing_server:
                        existing_server[key] = value
                        self.logger.debug(f"既存のサーバー'{server_name}'に不足しているキー'{key}'を追加しました")
                    else:
                        self.logger.debug(f"'{server_name}.{key}'のユーザーカスタマイズを保持しました")
                
                # NEW: Apply environment variable references for API keys
                if "env" in existing_server and self.collected_api_keys:
                    for env_key, env_value in existing_server["env"].items():
                        if env_key in self.collected_api_keys and env_value == "":
                            # Update to use environment variable reference
                            existing_server["env"][env_key] = f"${{{env_key}}}"
                            self.logger.info(f"{env_key}を環境変数を使用するように設定しました")
                
                self.logger.info(f"既存のMCPサーバー'{server_name}'を更新しました（ユーザーカスタマイズを保持）")
            else:
                # New server - add complete configuration
                # Apply environment variable references if we have collected keys
                if "env" in server_def and self.collected_api_keys:
                    for env_key in server_def["env"]:
                        if env_key in self.collected_api_keys and server_def["env"][env_key] == "":
                            server_def["env"][env_key] = f"${{{env_key}}}"
                
                existing_config[server_name] = server_def
                self.logger.info(f"{server_key}から新しいMCPサーバー'{server_name}'を追加しました")
    
    def _load_mcp_server_config(self, server_key: str) -> Optional[Dict]:
        """MCPサーバー設定スニペットを読み込み"""
        if server_key not in self.mcp_servers:
            return None
        
        server_info = self.mcp_servers[server_key]
        config_file = server_info["config_file"]
        config_source_dir = self._get_config_source_dir()
        
        if not config_source_dir:
            return None
        
        config_path = config_source_dir / config_file
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"{server_key}のMCP設定の読み込みに失敗しました: {e}")
            return None
    
    def _install(self, config: Dict[str, Any]) -> bool:
        """Install MCP component by configuring .claude.json"""
        self.logger.info("ClaudeでMCPサーバーを設定中...")
        
        # Get selected servers from config
        selected_servers = config.get("selected_mcp_servers", [])
        if not selected_servers:
            self.logger.info("MCPサーバーが選択されていません - MCP設定をスキップします")
            return True
        
        self.set_selected_servers(selected_servers)
        
        # NEW: Log collected API keys information
        if hasattr(self, 'collected_api_keys') and self.collected_api_keys:
            self.logger.info(f"{len(self.collected_api_keys)}個の収集されたAPIキーを設定に使用中")
        
        # Validate prerequisites
        success, errors = self.validate_prerequisites()
        if not success:
            for error in errors:
                self.logger.error(error)
            return False
        
        # Load Claude configuration
        claude_config, config_path = self._load_claude_config()
        if claude_config is None:
            return False
        
        # Ensure mcpServers section exists
        if "mcpServers" not in claude_config:
            claude_config["mcpServers"] = {}
        
        # Configure each selected server
        configured_count = 0
        for server_key in selected_servers:
            if server_key not in self.mcp_servers:
                self.logger.warning(f"不明なMCPサーバー: {server_key}")
                continue
            
            server_info = self.mcp_servers[server_key]
            server_config = self._load_mcp_server_config(server_key)
            
            if server_config is None:
                self.logger.error(f"{server_key}の設定の読み込みに失敗しました")
                continue
            
            # Handle API key requirements
            if server_info.get("requires_api_key", False):
                api_key_env = server_info.get("api_key_env")
                if api_key_env:
                    display_info(f"サーバー'{server_key}'にはAPIキーが必要です: {api_key_env}")
                    display_info("この環境変数は後で設定できます")
            
            # Precisely merge server config, preserving user customizations
            self._merge_mcp_server_config(claude_config["mcpServers"], server_config, server_key)
            configured_count += 1
            
            self.logger.info(f"設定されたMCPサーバー: {server_info['name']}")
        
        if configured_count == 0:
            self.logger.error("正常に設定されたMCPサーバーはありませんでした")
            return False
        
        # Save updated configuration
        success = self._save_claude_config(claude_config, config_path)
        
        if success:
            self.logger.success(f"{configured_count}個のMCPサーバーが正常に設定されました")
            return self._post_install()
        else:
            return False
    
    def _post_install(self) -> bool:
        """インストール後のタスク"""
        try:
            # Update metadata
            metadata_mods = {
                "components": {
                    "mcp": {
                        "version": __version__,
                        "installed": True,
                        "servers_configured": len(self.selected_servers),
                        "configured_servers": self.selected_servers
                    }
                }
            }
            self.settings_manager.update_metadata(metadata_mods)
            self.logger.info("MCPコンポーネント登録でメタデータを更新しました")
            
            return True
        except Exception as e:
            self.logger.error(f"メタデータの更新に失敗しました: {e}")
            return False
    
    def uninstall(self) -> bool:
        """Uninstall MCP component by removing servers from .claude.json"""
        try:
            self.logger.info("MCPサーバー設定を削除中...")
            
            # Load Claude configuration
            claude_config, config_path = self._load_claude_config()
            if claude_config is None:
                self.logger.warning("クリーンアップのためにClaude設定を読み込めませんでした")
                return True  # Not a failure if config doesn't exist
            
            if "mcpServers" not in claude_config:
                self.logger.info("MCPサーバーが設定されていません")
                return True
            
            # Only remove servers that were installed by SuperClaude
            removed_count = 0
            installed_servers = self._get_installed_servers()
            
            for server_name in installed_servers:
                if server_name in claude_config["mcpServers"]:
                    # Check if this server was installed by SuperClaude by comparing with our configs
                    if self._is_superclaude_managed_server(claude_config["mcpServers"][server_name], server_name):
                        del claude_config["mcpServers"][server_name]
                        removed_count += 1
                        self.logger.debug(f"SuperClaude管理のMCPサーバーを削除しました: {server_name}")
                    else:
                        self.logger.info(f"ユーザーがカスタマイズしたMCPサーバーを保持しました: {server_name}")
            
            # Save updated configuration
            if removed_count > 0:
                success = self._save_claude_config(claude_config, config_path)
                if not success:
                    self.logger.warning("更新されたClaude設定の保存に失敗しました")
            
            # Update settings.json
            try:
                if self.settings_manager.is_component_installed("mcp"):
                    self.settings_manager.remove_component_registration("mcp")
                    self.logger.info("Removed MCP component from settings.json")
            except Exception as e:
                self.logger.warning(f"Could not update settings.json: {e}")
            
            if removed_count > 0:
                self.logger.success(f"MCP component uninstalled ({removed_count} 個のSuperClaude管理サーバーを削除しました)")
            else:
                self.logger.info("MCPコンポーネントがアンインストールされました (削除するSuperClaude管理サーバーなし)")
            return True
            
        except Exception as e:
            self.logger.exception(f"MCPアンインストール中に予期しないエラーが発生しました: {e}")
            return False
    
    def _get_installed_servers(self) -> List[str]:
        """SuperClaudeによってインストールされたサーバーのリストを取得"""
        try:
            metadata = self.settings_manager.get_metadata_setting("components")
            if metadata and "mcp" in metadata:
                return metadata["mcp"].get("configured_servers", [])
        except Exception:
            pass
        return []
    
    def _is_superclaude_managed_server(self, server_config: Dict, server_name: str) -> bool:
        """サーバー設定がSuperClaudeのテンプレートと一致するか確認します

        これにより、サーバーがSuperClaudeによってインストールされたか、ユーザーによって手動で設定されたかを判断でき、
        ユーザーのカスタマイズを保持することができます。
        """
        # Find the server key that maps to this server name
        server_key = None
        for key, info in self.mcp_servers.items():
            if info["name"] == server_name:
                server_key = key
                break
        
        if not server_key:
            return False  # Unknown server, don't remove
        
        # Load our template config for comparison
        template_config = self._load_mcp_server_config(server_key)
        if not template_config or server_name not in template_config:
            return False
        
        template_server = template_config[server_name]
        
        # Check if the current config has the same structure as our template
        # If user has customized it, the structure might be different
        required_keys = {"command", "args"}
        
        # Check if all required keys exist and match our template
        for key in required_keys:
            if key not in server_config or key not in template_server:
                return False
            # For command and basic structure, they should match our template
            if key == "command" and server_config[key] != template_server[key]:
                return False
        
        return True
    
    def get_dependencies(self) -> List[str]:
        """依存関係を取得"""
        return ["core"]
    
    def get_size_estimate(self) -> int:
        """推定サイズを取得 - 設定のみを変更するため最小限"""
        return 4096  # 4KB - just config modifications