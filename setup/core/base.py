"""
インストール可能なコンポーネントの抽象基底クラス
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path
import json
from ..services.files import FileService
from ..services.settings import SettingsService
from ..utils.logger import get_logger
from ..utils.security import SecurityValidator


class Component(ABC):
    """すべてのインストール可能なコンポーネントの基底クラス"""
    
    def __init__(self, install_dir: Optional[Path] = None, component_subdir: Path = Path('')):
        """
        Initialize component with installation directory
        
        Args:
            install_dir: Target installation directory (defaults to ~/.claude)
        """
        from .. import DEFAULT_INSTALL_DIR
        # Initialize logger first
        self.logger = get_logger()
        # Resolve path safely
        self.install_dir = self._resolve_path_safely(install_dir or DEFAULT_INSTALL_DIR)
        self.settings_manager = SettingsService(self.install_dir)
        self.component_files = self._discover_component_files()
        self.file_manager = FileService()
        self.install_component_subdir = self.install_dir / component_subdir
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, str]:
        """
        コンポーネントのメタデータを返します
        
        Returns:
            以下を含む辞書:
                - name: コンポーネント名
                - version: コンポーネントバージョン
                - description: コンポーネントの説明
                - category: コンポーネントカテゴリ (core, command, integration, etc.)
        """
        pass
    
    def validate_prerequisites(self, installSubPath: Optional[Path] = None) -> Tuple[bool, List[str]]:
        """
        このコンポーネントの前提条件を確認します
        
        Returns:
            (成功: bool, エラーメッセージ: List[str])のタプル
        """
        errors = []

        # Check if we have read access to source files
        source_dir = self._get_source_dir()
        if not source_dir or (source_dir and not source_dir.exists()):
            errors.append(f"ソースディレクトリが見つかりません: {source_dir}")
            return False, errors

        # Check if all required framework files exist
        missing_files = []
        for filename in self.component_files:
            source_file = source_dir / filename
            if not source_file.exists():
                missing_files.append(filename)

        if missing_files:
            errors.append(f"コンポーネントファイルが見つかりません: {missing_files}")

        # Check write permissions to install directory
        has_perms, missing = SecurityValidator.check_permissions(
            self.install_dir, {'write'}
        )
        if not has_perms:
            errors.append(f"{self.install_dir}への書き込み権限がありません: {missing}")

        # Validate installation target
        is_safe, validation_errors = SecurityValidator.validate_installation_target(self.install_component_subdir)
        if not is_safe:
            errors.extend(validation_errors)

        # Get files to install
        files_to_install = self.get_files_to_install()

        # Validate all files for security
        is_safe, security_errors = SecurityValidator.validate_component_files(
            files_to_install, source_dir, self.install_component_subdir
        )
        if not is_safe:
            errors.extend(security_errors)

        if not self.file_manager.ensure_directory(self.install_component_subdir):
            errors.append(f"インストールディレクトリを作成できませんでした: {self.install_component_subdir}")

        return len(errors) == 0, errors
    
    def get_files_to_install(self) -> List[Tuple[Path, Path]]:
        """
        インストールするファイルのリストを返します
        
        Returns:
            (ソースパス, ターゲットパス)のタプルのリスト
        """
        source_dir = self._get_source_dir()
        files = []

        if source_dir:
            for filename in self.component_files:
                source = source_dir / filename
                target = self.install_component_subdir / filename
                files.append((source, target))

        return files
    
    def get_settings_modifications(self) -> Dict[str, Any]:
        """
        Return settings.json modifications to apply
        (now only Claude Code compatible settings)

        Returns:
            Dict of settings to merge into settings.json
        """
        # Return empty dict as we don't modify Claude Code settings
        return {}
    
    def install(self, config: Dict[str, Any]) -> bool:
        try:
            return self._install(config)
        except Exception as e:
            self.logger.exception(f"{repr(self)}のインストール中に予期しないエラーが発生しました: {e}")
            return False

    @abstractmethod
    def _install(self, config: Dict[str, Any]) -> bool:
        """
        コンポーネント固有のインストールロジックを実行します
        
        Args:
            config: インストール設定
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        # Validate installation
        success, errors = self.validate_prerequisites()
        if not success:
            for error in errors:
                self.logger.error(error)
            return False

        # Get files to install
        files_to_install = self.get_files_to_install()

        # Copy framework files
        success_count = 0
        for source, target in files_to_install:
            self.logger.debug(f"{source.name} を {target} にコピー中")

            if self.file_manager.copy_file(source, target):
                success_count += 1
                self.logger.debug(f"{source.name}のコピーに成功しました")
            else:
                self.logger.error(f"{source.name}のコピーに失敗しました")

        if success_count != len(files_to_install):
            self.logger.error(f"{len(files_to_install)}個のファイルのうち{success_count}個のみ正常にコピーされました")
            return False

        self.logger.success(f"{repr(self)}コンポーネントが正常にインストールされました（{success_count}個のファイル）")

        return self._post_install()

    
    @abstractmethod
    def _post_install(self) -> bool:
        pass


    @abstractmethod
    def uninstall(self) -> bool:
        """
        コンポーネントを削除します
        
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        pass
    
    @abstractmethod
    def get_dependencies(self) -> List[str]:
        """
        コンポーネントの依存関係リストを返します
        
        Returns:
            このコンポーネントが依存するコンポーネント名のリスト
        """
        pass

    @abstractmethod
    def _get_source_dir(self) -> Optional[Path]:
        """コンポーネントファイルのソースディレクトリを取得"""
        pass
    
    def update(self, config: Dict[str, Any]) -> bool:
        """
        コンポーネントを更新します (デフォルト: アンインストールしてからインストール)
        
        Args:
            config: インストール設定
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        # Default implementation: uninstall and reinstall
        if self.uninstall():
            return self.install(config)
        return False
    
    def get_installed_version(self) -> Optional[str]:
        """
        現在インストールされているコンポーネントのバージョンを取得します
        
        Returns:
            インストールされている場合はバージョン文字列、それ以外はNone
        """
        self.logger.debug("インストール済みバージョンの確認")
        metadata_file = self.install_dir / ".superclaude-metadata.json"
        if metadata_file.exists():
            self.logger.debug("メタデータファイルが存在するため、バージョンを読み取り中")
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                component_name = self.get_metadata()['name']
                version = metadata.get('components', {}).get(component_name, {}).get('version')
                self.logger.debug(f"バージョンが見つかりました: {version}")
                return version
            except Exception as e:
                self.logger.warning(f"メタデータからバージョンを読み取れませんでした: {e}")
        else:
            self.logger.debug("メタデータファイルが存在しません")
        return None
    
    def is_installed(self) -> bool:
        """
        コンポーネントがインストールされているか確認します
        
        Returns:
            インストールされている場合はTrue、それ以外はFalse
        """
        return self.get_installed_version() is not None
    
    def validate_installation(self) -> Tuple[bool, List[str]]:
        """
        コンポーネントが正しくインストールされていることを検証します
        
        Returns:
            (成功: bool, エラーメッセージ: List[str])のタプル
        """
        errors = []
        
        # Check if all files exist
        for _, target in self.get_files_to_install():
            if not target.exists():
                errors.append(f"ファイルが見つかりません: {target}")
        
        # Check version in metadata
        if not self.get_installed_version():
            errors.append("コンポーネントが.superclaude-metadata.jsonに登録されていません")
        
        return len(errors) == 0, errors
    
    def get_size_estimate(self) -> int:
        """
        インストールサイズをバイト単位で推定します
        
        Returns:
            推定サイズ（バイト）
        """
        total_size = 0
        for source, _ in self.get_files_to_install():
            if source.exists():
                if source.is_file():
                    total_size += source.stat().st_size
                elif source.is_dir():
                    total_size += sum(f.stat().st_size for f in source.rglob('*') if f.is_file())
        return total_size

    def _discover_component_files(self) -> List[str]:
        """
        Coreディレクトリ内のフレームワーク.mdファイルを動的に検出します

        Returns:
            フレームワークファイル名のリスト (例: ['CLAUDE.md', 'COMMANDS.md', ...])
        """
        source_dir = self._get_source_dir()

        if not source_dir:
            return []

        return self._discover_files_in_directory(
            source_dir,
            extension='.md',
            exclude_patterns=['README.md', 'CHANGELOG.md', 'LICENSE.md']
        )

    def _discover_files_in_directory(self, directory: Path, extension: str = '.md',
                                   exclude_patterns: Optional[List[str]] = None) -> List[str]:
        """
        ディレクトリ内のファイルを検出するための共有ユーティリティ

        Args:
            directory: スキャンするディレクトリ
            extension: 検索するファイル拡張子 (デフォルト: '.md')
            exclude_patterns: 除外するファイル名パターンのリスト

        Returns:
            ディレクトリ内で見つかったファイル名のリスト
        """
        if exclude_patterns is None:
            exclude_patterns = []

        try:
            if not directory.exists():
                self.logger.warning(f"ソースディレクトリが見つかりません: {directory}")
                return []

            if not directory.is_dir():
                self.logger.warning(f"ソースパスはディレクトリではありません: {directory}")
                return []

            # Discover files with the specified extension
            files = []
            for file_path in directory.iterdir():
                if (file_path.is_file() and
                    file_path.suffix.lower() == extension.lower() and
                    file_path.name not in exclude_patterns):
                    files.append(file_path.name)

            # Sort for consistent ordering
            files.sort()

            self.logger.debug(f"{directory}で{len(files)}個の{extension}ファイルを発見しました")
            if files:
                self.logger.debug(f"見つかったファイル: {files}")

            return files

        except PermissionError:
            self.logger.error(f"ディレクトリへのアクセスが拒否されました: {directory}")
            return []
        except Exception as e:
            self.logger.error(f"{directory}でのファイル発見中にエラーが発生しました: {e}")
            return []
    
    def __str__(self) -> str:
        """コンポーネントの文字列表現"""
        metadata = self.get_metadata()
        return f"{metadata['name']} v{metadata['version']}"
    
    def __repr__(self) -> str:
        """コンポーネントの開発者向け表現"""
        return f"<{self.__class__.__name__}({self.get_metadata()['name']})>"
    
    def _resolve_path_safely(self, path: Path) -> Path:
        """
        適切なエラー処理とセキュリティ検証で安全にパスを解決します
        
        Args:
            path: 解決するパス
            
        Returns:
            解決されたパス
            
        Raises:
            ValueError: パスの解決に失敗した場合、またはパスが安全でない場合
        """
        try:
            # Expand user directory (~) and resolve path
            resolved_path = path.expanduser().resolve()
            
            # Basic security validation - only enforce for production directories
            path_str = str(resolved_path).lower()
            
            # Check for most dangerous system patterns (but allow /tmp for testing)
            dangerous_patterns = [
                '/etc/', '/bin/', '/sbin/', '/usr/bin/', '/usr/sbin/',
                '/var/log/', '/var/lib/', '/dev/', '/proc/', '/sys/',
                'c:\\windows\\', 'c:\\program files\\'
            ]
            
            # Allow temporary directories for testing
            if path_str.startswith('/tmp/') or 'temp' in path_str:
                self.logger.debug(f"一時ディレクトリを許可しています: {resolved_path}")
                return resolved_path
            
            for pattern in dangerous_patterns:
                if path_str.startswith(pattern):
                    raise ValueError(f"システムディレクトリは使用できません: {resolved_path}")
            
            return resolved_path
            
        except Exception as e:
            self.logger.error(f"パスの解決に失敗しました {path}: {e}")
            raise ValueError(f"無効なパスです: {path}")
    
    def _resolve_source_path_safely(self, path: Path) -> Optional[Path]:
        """
        存在チェック付きで安全にソースパスを解決します
        
        Args:
            path: 解決するソースパス
            
        Returns:
            有効で存在する場合は解決されたパス、それ以外はNone
        """
        try:
            resolved_path = self._resolve_path_safely(path)
            return resolved_path if resolved_path.exists() else None
        except ValueError:
            return None
