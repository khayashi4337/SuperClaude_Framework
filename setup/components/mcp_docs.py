"""
MCP Documentation component for SuperClaude MCP server documentation
"""

from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

from ..core.base import Component
from setup import __version__
from ..services.claude_md import CLAUDEMdService


class MCPDocsComponent(Component):
    """MCP documentation component - installs docs for selected MCP servers"""
    
    def __init__(self, install_dir: Optional[Path] = None):
        """Initialize MCP docs component"""
        # Initialize attributes before calling parent constructor
        # because parent calls _discover_component_files() which needs these
        self.selected_servers: List[str] = []
        
        # Map server names to documentation files
        self.server_docs_map = {
            "context7": "MCP_Context7.md",
            "sequential": "MCP_Sequential.md", 
            "magic": "MCP_Magic.md",
            "playwright": "MCP_Playwright.md",
            "serena": "MCP_Serena.md",
            "morphllm": "MCP_Morphllm.md"
        }
        
        super().__init__(install_dir, Path(""))
    
    def get_metadata(self) -> Dict[str, str]:
        """Get component metadata"""
        return {
            "name": "mcp_docs",
            "version": __version__,
            "description": "MCPサーバードキュメントと使用ガイド",
            "category": "documentation"
        }
    
    def set_selected_servers(self, selected_servers: List[str]) -> None:
        """Set which MCP servers were selected for documentation installation"""
        self.selected_servers = selected_servers
        self.logger.debug(f"MCPドキュメントは次のサーバー用にインストールされます: {selected_servers}")
    
    def get_files_to_install(self) -> List[Tuple[Path, Path]]:
        """
        Return list of files to install based on selected MCP servers
        
        Returns:
            List of tuples (source_path, target_path)
        """
        source_dir = self._get_source_dir()
        files = []

        if source_dir and self.selected_servers:
            for server_name in self.selected_servers:
                if server_name in self.server_docs_map:
                    doc_file = self.server_docs_map[server_name]
                    source = source_dir / doc_file
                    target = self.install_dir / doc_file
                    if source.exists():
                        files.append((source, target))
                        self.logger.debug(f"{server_name}のドキュメントをインストールします: {doc_file}")
                    else:
                        self.logger.warning(f"{server_name}のドキュメントファイルが見つかりません: {doc_file}")

        return files
    
    def _discover_component_files(self) -> List[str]:
        """
        Override parent method to dynamically discover files based on selected servers
        """
        files = []
        # Check if selected_servers is not empty
        if self.selected_servers:
            for server_name in self.selected_servers:
                if server_name in self.server_docs_map:
                    files.append(self.server_docs_map[server_name])
        return files
    
    def _install(self, config: Dict[str, Any]) -> bool:
        """Install MCP documentation component"""
        self.logger.info("MCPサーバードキュメントをインストール中...")
        
        # Get selected servers from config
        selected_servers = config.get("selected_mcp_servers", [])
        if not selected_servers:
            self.logger.info("MCPサーバーが選択されていません - ドキュメントのインストールをスキップします")
            return True
        
        self.set_selected_servers(selected_servers)
        
        # Update component files based on selection
        self.component_files = self._discover_component_files()

        # Validate installation
        success, errors = self.validate_prerequisites()
        if not success:
            for error in errors:
                self.logger.error(error)
            return False

        # Get files to install
        files_to_install = self.get_files_to_install()

        if not files_to_install:
            self.logger.warning("インストールするMCPドキュメントファイルが見つかりません")
            return True  # Not an error - just no docs to install

        # Copy documentation files
        success_count = 0
        for source, target in files_to_install:
            self.logger.debug(f"{source.name} を {target} にコピー中")
            
            if self.file_manager.copy_file(source, target):
                success_count += 1
                self.logger.debug(f"{source.name}のコピーに成功しました")
            else:
                self.logger.error(f"{source.name}のコピーに失敗しました")

        if success_count != len(files_to_install):
            self.logger.error(f"{len(files_to_install)}個のドキュメントファイルのうち{success_count}個のみ正常にコピーされました")
            return False

        self.logger.success(f"MCPドキュメントが正常にインストールされました（{len(selected_servers)}個のサーバー用に{success_count}個のファイル）")

        return self._post_install()

    def _post_install(self) -> bool:
        """Post-installation tasks"""
        try:
            # Update metadata
            metadata_mods = {
                "components": {
                    "mcp_docs": {
                        "version": __version__,
                        "installed": True,
                        "files_count": len(self.component_files),
                        "servers_documented": self.selected_servers
                    }
                }
            }
            self.settings_manager.update_metadata(metadata_mods)
            self.logger.info("メタデータをMCPドキュメントコンポーネントの登録で更新しました")
            
            # Update CLAUDE.md with MCP documentation imports
            try:
                manager = CLAUDEMdService(self.install_dir)
                manager.add_imports(self.component_files, category="MCP Documentation")
                self.logger.info("CLAUDE.mdをMCPドキュメントのインポートで更新しました")
            except Exception as e:
                self.logger.warning(f"CLAUDE.mdをMCPドキュメントのインポートで更新できませんでした: {e}")
                # Don't fail the whole installation for this
            
            return True
        except Exception as e:
            self.logger.error(f"メタデータの更新に失敗しました: {e}")
            return False
    
    def uninstall(self) -> bool:
        """Uninstall MCP documentation component"""
        try:
            self.logger.info("MCPドキュメントコンポーネントをアンインストール中...")
            
            # Remove all MCP documentation files
            removed_count = 0
            source_dir = self._get_source_dir()
            
            if source_dir and source_dir.exists():
                # Remove all possible MCP doc files
                for doc_file in self.server_docs_map.values():
                    file_path = self.install_component_subdir / doc_file
                    if self.file_manager.remove_file(file_path):
                        removed_count += 1
                        self.logger.debug(f"削除しました {doc_file}")
            
            # Remove mcp directory if empty
            try:
                if self.install_component_subdir.exists():
                    remaining_files = list(self.install_component_subdir.iterdir())
                    if not remaining_files:
                        self.install_component_subdir.rmdir()
                        self.logger.debug("空のmcpディレクトリを削除しました")
            except Exception as e:
                self.logger.warning(f"mcpディレクトリを削除できませんでした: {e}")
            
            # Update settings.json
            try:
                if self.settings_manager.is_component_installed("mcp_docs"):
                    self.settings_manager.remove_component_registration("mcp_docs")
                    self.logger.info("settings.jsonからMCPドキュメントコンポーネントを削除しました")
            except Exception as e:
                self.logger.warning(f"settings.jsonを更新できませんでした: {e}")
            
            self.logger.success(f"MCPドキュメントがアンインストールされました（{removed_count}個のファイルを削除）")
            return True
            
        except Exception as e:
            self.logger.exception(f"MCPドキュメントのアンインストール中に予期しないエラーが発生しました: {e}")
            return False
    
    def get_dependencies(self) -> List[str]:
        """Get dependencies"""
        return ["core"]
    
    def _get_source_dir(self) -> Optional[Path]:
        """Get source directory for MCP documentation files"""
        # Assume we're in SuperClaude/setup/components/mcp_docs.py
        # and MCP docs are in SuperClaude/SuperClaude/MCP/
        project_root = Path(__file__).parent.parent.parent
        mcp_dir = project_root / "SuperClaude" / "MCP"
        
        # Return None if directory doesn't exist to prevent warning
        if not mcp_dir.exists():
            return None
        
        return mcp_dir
    
    def get_size_estimate(self) -> int:
        """Get estimated installation size"""
        source_dir = self._get_source_dir()
        total_size = 0
        
        if source_dir and source_dir.exists() and self.selected_servers:
            for server_name in self.selected_servers:
                if server_name in self.server_docs_map:
                    doc_file = self.server_docs_map[server_name]
                    file_path = source_dir / doc_file
                    if file_path.exists():
                        total_size += file_path.stat().st_size
        
        # Minimum size estimate
        total_size = max(total_size, 10240)  # At least 10KB
        
        return total_size