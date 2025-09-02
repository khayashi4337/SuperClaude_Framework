"""
Modes component for SuperClaude behavioral modes
"""

from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

from ..core.base import Component
from setup import __version__
from ..services.claude_md import CLAUDEMdService


class ModesComponent(Component):
    """SuperClaude behavioral modes component"""
    
    def __init__(self, install_dir: Optional[Path] = None):
        """Initialize modes component"""
        super().__init__(install_dir, "modes")
    
    def get_metadata(self) -> Dict[str, str]:
        """Get component metadata"""
        return {
            "name": "modes",
            "version": __version__,
            "description": "SuperClaudeの振る舞いモード (ブレインストーミング, 内省, タスク管理, トークン効率)",
            "category": "modes"
        }
    
    def _install(self, config: Dict[str, Any]) -> bool:
        """Install modes component"""
        self.logger.info("SuperClaudeの振る舞いモードをインストール中...")

        # Validate installation
        success, errors = self.validate_prerequisites()
        if not success:
            for error in errors:
                self.logger.error(error)
            return False

        # Get files to install
        files_to_install = self.get_files_to_install()

        if not files_to_install:
            self.logger.warning("インストールするモードファイルが見つかりません")
            return False

        # Copy mode files
        success_count = 0
        for source, target in files_to_install:
            self.logger.debug(f"{source.name} を {target} にコピー中")
            
            if self.file_manager.copy_file(source, target):
                success_count += 1
                self.logger.debug(f"{source.name}のコピーに成功しました")
            else:
                self.logger.error(f"{source.name}のコピーに失敗しました")

        if success_count != len(files_to_install):
            self.logger.error(f"{len(files_to_install)}個のモードファイルのうち{success_count}個のみ正常にコピーされました")
            return False

        self.logger.success(f"モードコンポーネントが正常にインストールされました（{success_count}個のモードファイル）")

        return self._post_install()

    def _post_install(self) -> bool:
        """Post-installation tasks"""
        try:
            # Update metadata
            metadata_mods = {
                "components": {
                    "modes": {
                        "version": __version__,
                        "installed": True,
                        "files_count": len(self.component_files)
                    }
                }
            }
            self.settings_manager.update_metadata(metadata_mods)
            self.logger.info("メタデータをモードコンポーネントの登録で更新しました")
            
            # Update CLAUDE.md with mode imports
            try:
                manager = CLAUDEMdService(self.install_dir)
                manager.add_imports(self.component_files, category="Behavioral Modes")
                self.logger.info("CLAUDE.mdをモードのインポートで更新しました")
            except Exception as e:
                self.logger.warning(f"CLAUDE.mdをモードのインポートで更新できませんでした: {e}")
                # Don't fail the whole installation for this
            
            return True
        except Exception as e:
            self.logger.error(f"メタデータの更新に失敗しました: {e}")
            return False
    
    def uninstall(self) -> bool:
        """Uninstall modes component"""
        try:
            self.logger.info("SuperClaudeモードコンポーネントをアンインストール中...")
            
            # Remove mode files
            removed_count = 0
            for _, target in self.get_files_to_install():
                if self.file_manager.remove_file(target):
                    removed_count += 1
                    self.logger.debug(f"削除しました {target.name}")
            
            # Remove modes directory if empty
            try:
                if self.install_component_subdir.exists():
                    remaining_files = list(self.install_component_subdir.iterdir())
                    if not remaining_files:
                        self.install_component_subdir.rmdir()
                        self.logger.debug("空のmodesディレクトリを削除しました")
            except Exception as e:
                self.logger.warning(f"modesディレクトリを削除できませんでした: {e}")
            
            # Update settings.json
            try:
                if self.settings_manager.is_component_installed("modes"):
                    self.settings_manager.remove_component_registration("modes")
                    self.logger.info("settings.jsonからモードコンポーネントを削除しました")
            except Exception as e:
                self.logger.warning(f"settings.jsonを更新できませんでした: {e}")
            
            self.logger.success(f"モードコンポーネントがアンインストールされました（{removed_count}個のファイルを削除）")
            return True
            
        except Exception as e:
            self.logger.exception(f"モードのアンインストール中に予期しないエラーが発生しました: {e}")
            return False
    
    def get_dependencies(self) -> List[str]:
        """Get dependencies"""
        return ["core"]
    
    def _get_source_dir(self) -> Optional[Path]:
        """Get source directory for mode files"""
        # Assume we're in SuperClaude/setup/components/modes.py
        # and mode files are in SuperClaude/SuperClaude/Modes/
        project_root = Path(__file__).parent.parent.parent
        modes_dir = project_root / "SuperClaude" / "Modes"
        
        # Return None if directory doesn't exist to prevent warning
        if not modes_dir.exists():
            return None
        
        return modes_dir
    
    def get_size_estimate(self) -> int:
        """Get estimated installation size"""
        source_dir = self._get_source_dir()
        total_size = 0
        
        if source_dir and source_dir.exists():
            for filename in self.component_files:
                file_path = source_dir / filename
                if file_path.exists():
                    total_size += file_path.stat().st_size
        
        # Minimum size estimate
        total_size = max(total_size, 20480)  # At least 20KB
        
        return total_size