"""
Core component for SuperClaude framework files installation
"""

from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import shutil

from ..core.base import Component
from ..services.claude_md import CLAUDEMdService
from setup import __version__

class CoreComponent(Component):
    """Core SuperClaude framework files component"""
    
    def __init__(self, install_dir: Optional[Path] = None):
        """Initialize core component"""
        super().__init__(install_dir)
    
    def get_metadata(self) -> Dict[str, str]:
        """Get component metadata"""
        return {
            "name": "core",
            "version": __version__,
            "description": "SuperClaudeフレームワークのドキュメントとコアファイル",
            "category": "core"
        }
    
    def get_metadata_modifications(self) -> Dict[str, Any]:
        """Get metadata modifications for SuperClaude"""
        return {
            "framework": {
                "version": __version__,
                "name": "SuperClaude",
                "description": "Claude CodeのためのAI強化開発フレームワーク",
                "installation_type": "global",
                "components": ["core"]
            },
            "superclaude": {
                "enabled": True,
                "version": __version__,
                "profile": "default",
                "auto_update": False
            }
        }
    
    def _install(self, config: Dict[str, Any]) -> bool:
        """Install core component"""
        self.logger.info("SuperClaudeコアフレームワークファイルをインストール中...")

        return super()._install(config);

    def _post_install(self) -> bool:
        # Create or update metadata
        try:
            metadata_mods = self.get_metadata_modifications()
            self.settings_manager.update_metadata(metadata_mods)
            self.logger.info("メタデータをフレームワーク設定で更新しました")
            
            # Add component registration to metadata
            self.settings_manager.add_component_registration("core", {
                "version": __version__,
                "category": "core",
                "files_count": len(self.component_files)
            })

            self.logger.info("メタデータをコアコンポーネントの登録で更新しました")
            
            # Migrate any existing SuperClaude data from settings.json
            if self.settings_manager.migrate_superclaude_data():
                self.logger.info("既存のSuperClaudeデータをsettings.jsonから移行しました")
        except Exception as e:
            self.logger.error(f"メタデータの更新に失敗しました: {e}")
            return False

        # Create additional directories for other components
        additional_dirs = ["commands", "backups", "logs"]
        for dirname in additional_dirs:
            dir_path = self.install_dir / dirname
            if not self.file_manager.ensure_directory(dir_path):
                self.logger.warning(f"ディレクトリを作成できませんでした: {dir_path}")
        
        # Update CLAUDE.md with core framework imports
        try:
            manager = CLAUDEMdService(self.install_dir)
            manager.add_imports(self.component_files, category="Core Framework")
            self.logger.info("CLAUDE.mdをコアフレームワークのインポートで更新しました")
        except Exception as e:
            self.logger.warning(f"CLAUDE.mdをコアフレームワークのインポートで更新できませんでした: {e}")
            # Don't fail the whole installation for this

        return True

    
    def uninstall(self) -> bool:
        """Uninstall core component"""
        try:
            self.logger.info("SuperClaudeコアコンポーネントをアンインストール中...")
            
            # Remove framework files
            removed_count = 0
            for filename in self.component_files:
                file_path = self.install_dir / filename
                if self.file_manager.remove_file(file_path):
                    removed_count += 1
                    self.logger.debug(f"削除しました {filename}")
                else:
                    self.logger.warning(f"{filename}を削除できませんでした")
            
            # Update metadata to remove core component
            try:
                if self.settings_manager.is_component_installed("core"):
                    self.settings_manager.remove_component_registration("core")
                    metadata_mods = self.get_metadata_modifications()
                    metadata = self.settings_manager.load_metadata()
                    for key in metadata_mods.keys():
                        if key in metadata:
                            del metadata[key]

                    self.settings_manager.save_metadata(metadata)
                    self.logger.info("メタデータからコアコンポーネントを削除しました")
            except Exception as e:
                self.logger.warning(f"メタデータを更新できませんでした: {e}")
            
            self.logger.success(f"コアコンポーネントがアンインストールされました（{removed_count}個のファイルを削除）")
            return True
            
        except Exception as e:
            self.logger.exception(f"コアのアンインストール中に予期しないエラーが発生しました: {e}")
            return False
    
    def get_dependencies(self) -> List[str]:
        """Get component dependencies (core has none)"""
        return []
    
    def update(self, config: Dict[str, Any]) -> bool:
        """Update core component"""
        try:
            self.logger.info("SuperClaudeコアコンポーネントを更新中...")
            
            # Check current version
            current_version = self.settings_manager.get_component_version("core")
            target_version = self.get_metadata()["version"]
            
            if current_version == target_version:
                self.logger.info(f"コアコンポーネントは既にバージョン{target_version}です")
                return True
            
            self.logger.info(f"コアコンポーネントを{current_version}から{target_version}に更新中")
            
            # Create backup of existing files
            backup_files = []
            for filename in self.component_files:
                file_path = self.install_dir / filename
                if file_path.exists():
                    backup_path = self.file_manager.backup_file(file_path)
                    if backup_path:
                        backup_files.append(backup_path)
                        self.logger.debug(f"バックアップしました {filename}")
            
            # Perform installation (overwrites existing files)
            success = self.install(config)
            
            if success:
                # Remove backup files on successful update
                for backup_path in backup_files:
                    try:
                        backup_path.unlink()
                    except Exception:
                        pass  # Ignore cleanup errors
                
                self.logger.success(f"コアコンポーネントがバージョン{target_version}に更新されました")
            else:
                # Restore from backup on failure
                self.logger.warning("更新に失敗しました。バックアップから復元しています...")
                for backup_path in backup_files:
                    try:
                        original_path = backup_path.with_suffix('')
                        shutil.move(str(backup_path), str(original_path))
                        self.logger.debug(f"復元しました {original_path.name}")
                    except Exception as e:
                        self.logger.error(f"{backup_path}を復元できませんでした: {e}")
            
            return success
            
        except Exception as e:
            self.logger.exception(f"コアの更新中に予期しないエラーが発生しました: {e}")
            return False
    
    def validate_installation(self) -> Tuple[bool, List[str]]:
        """Validate core component installation"""
        errors = []
        
        # Check if all framework files exist
        for filename in self.component_files:
            file_path = self.install_dir / filename
            if not file_path.exists():
                errors.append(f"フレームワークファイルが見つかりません: {filename}")
            elif not file_path.is_file():
                errors.append(f"フレームワークファイルは通常のファイルではありません: {filename}")
        
        # Check metadata registration
        if not self.settings_manager.is_component_installed("core"):
            errors.append("コアコンポーネントがメタデータに登録されていません")
        else:
            # Check version matches
            installed_version = self.settings_manager.get_component_version("core")
            expected_version = self.get_metadata()["version"]
            if installed_version != expected_version:
                errors.append(f"バージョンの不一致: インストール済み {installed_version}, 期待値 {expected_version}")
        
        # Check metadata structure
        try:
            framework_config = self.settings_manager.get_metadata_setting("framework")
            if not framework_config:
                errors.append("メタデータにフレームワーク設定がありません")
            else:
                required_keys = ["version", "name", "description"]
                for key in required_keys:
                    if key not in framework_config:
                        errors.append(f"メタデータにframework.{key}がありません")
        except Exception as e:
            errors.append(f"メタデータを検証できませんでした: {e}")
        
        return len(errors) == 0, errors
    
    def _get_source_dir(self):
        """Get source directory for framework files"""
        # Assume we're in SuperClaude/setup/components/core.py
        # and framework files are in SuperClaude/SuperClaude/Core/
        project_root = Path(__file__).parent.parent.parent
        return project_root / "SuperClaude" / "Core"
    
    def get_size_estimate(self) -> int:
        """Get estimated installation size"""
        total_size = 0
        source_dir = self._get_source_dir()
        
        for filename in self.component_files:
            file_path = source_dir / filename
            if file_path.exists():
                total_size += file_path.stat().st_size
        
        # Add overhead for settings.json and directories
        total_size += 10240  # ~10KB overhead
        
        return total_size
    
    def get_installation_summary(self) -> Dict[str, Any]:
        """Get installation summary"""
        return {
            "component": self.get_metadata()["name"],
            "version": self.get_metadata()["version"],
            "files_installed": len(self.component_files),
            "framework_files": self.component_files,
            "estimated_size": self.get_size_estimate(),
            "install_directory": str(self.install_dir),
            "dependencies": self.get_dependencies()
        }
