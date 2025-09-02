"""
Settings management for SuperClaude installation system
Handles settings.json migration to the new SuperClaude metadata json file
Allows for manipulation of these json files with deep merge and backup
"""

import json
import shutil
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import copy


class SettingsService:
    """Manages settings.json file operations"""
    
    def __init__(self, install_dir: Path):
        """
        Initialize settings manager
        
        Args:
            install_dir: Installation directory containing settings.json
        """
        self.install_dir = install_dir
        self.settings_file = install_dir / "settings.json"
        self.metadata_file = install_dir / ".superclaude-metadata.json"
        self.backup_dir = install_dir / "backups" / "settings"
        
    def load_settings(self) -> Dict[str, Any]:
        """
        Load settings from settings.json
        
        Returns:
            Settings dict (empty if file doesn't exist)
        """
        if not self.settings_file.exists():
            return {}
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"設定を読み込めませんでした: {self.settings_file}: {e}")
    
    def save_settings(self, settings: Dict[str, Any], create_backup: bool = True) -> None:
        """
        Save settings to settings.json with optional backup
        
        Args:
            settings: Settings dict to save
            create_backup: Whether to create backup before saving
        """
        # Create backup if requested and file exists
        if create_backup and self.settings_file.exists():
            self._create_settings_backup()
        
        # Ensure directory exists
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save with pretty formatting
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False, sort_keys=True)
        except IOError as e:
            raise ValueError(f"設定を保存できませんでした: {self.settings_file}: {e}")
    
    def load_metadata(self) -> Dict[str, Any]:
        """
        Load SuperClaude metadata from .superclaude-metadata.json
        
        Returns:
            Metadata dict (empty if file doesn't exist)
        """
        if not self.metadata_file.exists():
            return {}
        
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"メタデータを読み込めませんでした: {self.metadata_file}: {e}")
    
    def save_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        Save SuperClaude metadata to .superclaude-metadata.json
        
        Args:
            metadata: Metadata dict to save
        """
        # Ensure directory exists
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save with pretty formatting
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False, sort_keys=True)
        except IOError as e:
            raise ValueError(f"メタデータを保存できませんでした: {self.metadata_file}: {e}")

    def merge_metadata(self, modifications: Dict[str, Any]) -> Dict[str, Any]:
        """
        既存の設定に変更をディープマージします

        Args:
            modifications: マージする設定変更

        Returns:
            マージされた設定辞書
        """
        existing = self.load_metadata()
        return self._deep_merge(existing, modifications)

    def update_metadata(self, modifications: Dict[str, Any]) -> None:
        """
        変更を加えて設定を更新します

        Args:
            modifications: 適用する設定変更
            create_backup: 更新前にバックアップを作成するかどうか
        """
        merged = self.merge_metadata(modifications)
        self.save_metadata(merged)

    def migrate_superclaude_data(self) -> bool:
        """
        Migrate SuperClaude-specific data from settings.json to metadata file
        
        Returns:
            True if migration occurred, False if no data to migrate
        """
        settings = self.load_settings()
        
        # SuperClaude-specific fields to migrate
        superclaude_fields = ["components", "framework", "superclaude", "mcp"]
        data_to_migrate = {}
        fields_found = False
        
        # Extract SuperClaude data
        for field in superclaude_fields:
            if field in settings:
                data_to_migrate[field] = settings[field]
                fields_found = True
        
        if not fields_found:
            return False
        
        # Load existing metadata (if any) and merge
        existing_metadata = self.load_metadata()
        merged_metadata = self._deep_merge(existing_metadata, data_to_migrate)
        
        # Save to metadata file
        self.save_metadata(merged_metadata)
        
        # Remove SuperClaude fields from settings
        clean_settings = {k: v for k, v in settings.items() if k not in superclaude_fields}
        
        # Save cleaned settings
        self.save_settings(clean_settings, create_backup=True)
        
        return True
    
    def merge_settings(self, modifications: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge modifications into existing settings
        
        Args:
            modifications: Settings modifications to merge
            
        Returns:
            Merged settings dict
        """
        existing = self.load_settings()
        return self._deep_merge(existing, modifications)
    
    def update_settings(self, modifications: Dict[str, Any], create_backup: bool = True) -> None:
        """
        Update settings with modifications
        
        Args:
            modifications: Settings modifications to apply
            create_backup: Whether to create backup before updating
        """
        merged = self.merge_settings(modifications)
        self.save_settings(merged, create_backup)
    
    def get_setting(self, key_path: str, default: Any = None) -> Any:
        """
        ドット表記のパスを使用して設定値を取得します
        
        Args:
            key_path: ドットで区切られたパス (例: "hooks.enabled")
            default: キーが見つからない場合のデフォルト値
            
        Returns:
            設定値またはデフォルト値
        """
        settings = self.load_settings()
        
        try:
            value = settings
            for key in key_path.split('.'):
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_setting(self, key_path: str, value: Any, create_backup: bool = True) -> None:
        """
        ドット表記のパスを使用して設定値を設定します
        
        Args:
            key_path: ドットで区切られたパス (例: "hooks.enabled")
            value: 設定する値
            create_backup: 更新前にバックアップを作成するかどうか
        """
        # Build nested dict structure
        keys = key_path.split('.')
        modification = {}
        current = modification
        
        for key in keys[:-1]:
            current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        
        self.update_settings(modification, create_backup)
    
    def remove_setting(self, key_path: str, create_backup: bool = True) -> bool:
        """
        ドット表記のパスを使用して設定を削除します
        
        Args:
            key_path: 削除するドットで区切られたパス
            create_backup: 更新前にバックアップを作成するかどうか
            
        Returns:
            設定が削除された場合はTrue、見つからない場合はFalse
        """
        settings = self.load_settings()
        keys = key_path.split('.')
        
        # Navigate to parent of target key
        current = settings
        try:
            for key in keys[:-1]:
                current = current[key]
            
            # Remove the target key
            if keys[-1] in current:
                del current[keys[-1]]
                self.save_settings(settings, create_backup)
                return True
            else:
                return False
                
        except (KeyError, TypeError):
            return False
    
    def add_component_registration(self, component_name: str, component_info: Dict[str, Any]) -> None:
        """
        メタデータのレジストリにコンポーネントを追加します
        
        Args:
            component_name: コンポーネント名
            component_info: コンポーネントメタデータ辞書
        """
        metadata = self.load_metadata()
        if "components" not in metadata:
            metadata["components"] = {}
        
        metadata["components"][component_name] = {
            **component_info,
            "installed_at": datetime.now().isoformat()
        }
        
        self.save_metadata(metadata)
    
    def remove_component_registration(self, component_name: str) -> bool:
        """
        メタデータのレジストリからコンポーネントを削除します
        
        Args:
            component_name: 削除するコンポーネント名
            
        Returns:
            コンポーネントが削除された場合はTrue、見つからない場合はFalse
        """
        metadata = self.load_metadata()
        if "components" in metadata and component_name in metadata["components"]:
            del metadata["components"][component_name]
            self.save_metadata(metadata)
            return True
        return False
    
    def get_installed_components(self) -> Dict[str, Dict[str, Any]]:
        """
        レジストリからインストールされているすべてのコンポーネントを取得します
        
        Returns:
            component_name -> component_info の辞書
        """
        metadata = self.load_metadata()
        return metadata.get("components", {})
    
    def is_component_installed(self, component_name: str) -> bool:
        """
        コンポーネントがインストール済みとして登録されているか確認します
        
        Args:
            component_name: 確認するコンポーネント名
            
        Returns:
            コンポーネントがインストールされている場合はTrue、それ以外はFalse
        """
        components = self.get_installed_components()
        return component_name in components
    
    def get_component_version(self, component_name: str) -> Optional[str]:
        """
        インストールされているコンポーネントのバージョンを取得します
        
        Args:
            component_name: コンポーネント名
            
        Returns:
            インストールされている場合はバージョン文字列、それ以外はNone
        """
        components = self.get_installed_components()
        component_info = components.get(component_name, {})
        return component_info.get("version")
    
    def update_framework_version(self, version: str) -> None:
        """
        メタデータ内のSuperClaudeフレームワークのバージョンを更新します
        
        Args:
            version: フレームワークのバージョン文字列
        """
        metadata = self.load_metadata()
        if "framework" not in metadata:
            metadata["framework"] = {}
        
        metadata["framework"]["version"] = version
        metadata["framework"]["updated_at"] = datetime.now().isoformat()
        
        self.save_metadata(metadata)
    
    def check_installation_exists(self) -> bool:
        """
        Get SuperClaude framework version from metadata
        
        Returns:
            Version string or None if not set
        """
        return self.metadata_file.exists()

    def check_v2_installation_exists(self) -> bool:
        """
        メタデータからSuperClaudeフレームワークのバージョンを取得します

        Returns:
            バージョン文字列、設定されていない場合はNone
        """
        return self.settings_file.exists()
    
    def get_metadata_setting(self, key_path: str, default: Any = None) -> Any:
        """
        ドット表記のパスを使用してメタデータ値を取得します
        
        Args:
            key_path: ドットで区切られたパス (例: "framework.version")
            default: キーが見つからない場合のデフォルト値
            
        Returns:
            メタデータ値またはデフォルト値
        """
        metadata = self.load_metadata()
        
        try:
            value = metadata
            for key in key_path.split('.'):
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def _deep_merge(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        """
        2つの辞書をディープマージします
        
        Args:
            base: 基本となる辞書
            overlay: 上にマージする辞書
            
        Returns:
            マージされた辞書
        """
        result = copy.deepcopy(base)
        
        for key, value in overlay.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = copy.deepcopy(value)
        
        return result
    
    def _create_settings_backup(self) -> Path:
        """
        Create timestamped backup of settings.json
        
        Returns:
            Path to backup file
        """
        if not self.settings_file.exists():
            raise ValueError("存在しない設定ファイルはバックアップできません")
        
        # Create backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Create timestamped backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"settings_{timestamp}.json"
        
        shutil.copy2(self.settings_file, backup_file)
        
        # Keep only last 10 backups
        self._cleanup_old_backups()
        
        return backup_file
    
    def _cleanup_old_backups(self, keep_count: int = 10) -> None:
        """
        古いバックアップファイルを削除し、最新のもののみを保持します
        
        Args:
            keep_count: 保持するバックアップの数
        """
        if not self.backup_dir.exists():
            return
        
        # Get all backup files sorted by modification time
        backup_files = []
        for file in self.backup_dir.glob("settings_*.json"):
            backup_files.append((file.stat().st_mtime, file))
        
        backup_files.sort(reverse=True)  # Most recent first
        
        # Remove old backups
        for _, file in backup_files[keep_count:]:
            try:
                file.unlink()
            except OSError:
                pass  # Ignore errors when cleaning up
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """
        利用可能な設定のバックアップを一覧表示します
        
        Returns:
            名前、パス、タイムスタンプを含むバックアップ情報辞書のリスト
        """
        if not self.backup_dir.exists():
            return []
        
        backups = []
        for file in self.backup_dir.glob("settings_*.json"):
            try:
                stat = file.stat()
                backups.append({
                    "name": file.name,
                    "path": str(file),
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            except OSError:
                continue
        
        # Sort by creation time, most recent first
        backups.sort(key=lambda x: x["created"], reverse=True)
        return backups
    
    def restore_backup(self, backup_name: str) -> bool:
        """
        バックアップから設定を復元します
        
        Args:
            backup_name: 復元するバックアップファイルの名前
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        backup_file = self.backup_dir / backup_name
        
        if not backup_file.exists():
            return False
        
        try:
            # Validate backup file first
            with open(backup_file, 'r', encoding='utf-8') as f:
                json.load(f)  # Will raise exception if invalid
            
            # Create backup of current settings
            if self.settings_file.exists():
                self._create_settings_backup()
            
            # Restore backup
            shutil.copy2(backup_file, self.settings_file)
            return True
            
        except (json.JSONDecodeError, IOError):
            return False
