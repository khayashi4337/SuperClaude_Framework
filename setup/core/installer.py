"""
SuperClaudeインストールシステムの基本インストーラーロジック いくつかの問題を修正
"""

from typing import List, Dict, Optional, Set, Tuple, Any
from pathlib import Path
import shutil
import tempfile
from datetime import datetime
from .base import Component
from ..utils.logger import get_logger


class Installer:
    """メインインストーラーオーケストレーター"""

    def __init__(self,
                 install_dir: Optional[Path] = None,
                 dry_run: bool = False):
        """
        インストーラーを初期化します
        
        Args:
            install_dir: ターゲットインストールディレクトリ
            dry_run: Trueの場合、インストールをシミュレートするだけです
        """
        from .. import DEFAULT_INSTALL_DIR
        self.install_dir = install_dir or DEFAULT_INSTALL_DIR
        self.dry_run = dry_run
        self.components: Dict[str, Component] = {}
        self.installed_components: Set[str] = set()
        self.updated_components: Set[str] = set()

        self.failed_components: Set[str] = set()
        self.skipped_components: Set[str] = set()
        self.backup_path: Optional[Path] = None
        self.logger = get_logger()

    def register_component(self, component: Component) -> None:
        """
        インストール用のコンポーネントを登録します
        
        Args:
            component: 登録するコンポーネントインスタンス
        """
        metadata = component.get_metadata()
        self.components[metadata['name']] = component

    def register_components(self, components: List[Component]) -> None:
        """
        複数のコンポーネントを登録します
        
        Args:
            components: コンポーネントインスタンスのリスト
        """
        for component in components:
            self.register_component(component)

    def resolve_dependencies(self, component_names: List[str]) -> List[str]:
        """
        正しいインストール順序でコンポーネントの依存関係を解決します
        
        Args:
            component_names: インストールするコンポーネント名のリスト
            
        Returns:
            依存関係を含む、順序付けされたコンポーネント名のリスト
            
        Raises:
            ValueError: 循環依存が検出されたか、不明なコンポーネントがある場合
        """
        resolved = []
        resolving = set()

        def resolve(name: str) -> None:
            if name in resolved:
                return

            if name in resolving:
                raise ValueError(
                    f"循環依存が検出されました: {name}")

            if name not in self.components:
                raise ValueError(f"不明なコンポーネント: {name}")

            resolving.add(name)

            # Resolve dependencies first
            for dep in self.components[name].get_dependencies():
                resolve(dep)

            resolving.remove(name)
            resolved.append(name)

        # Resolve each requested component
        for name in component_names:
            resolve(name)

        return resolved

    def validate_system_requirements(self) -> Tuple[bool, List[str]]:
        """
        登録されているすべてのコンポーネントのシステム要件を検証します
        
        Returns:
            (成功: bool, エラーメッセージ: List[str])のタプル
        """
        errors = []

        # Check disk space (500MB minimum)
        try:
            stat = shutil.disk_usage(self.install_dir.parent)
            free_mb = stat.free / (1024 * 1024)
            if free_mb < 500:
                errors.append(
                    f"ディスク容量が不足しています: 空き容量 {free_mb:.1f}MB (500MB が必要です)"
                )
        except Exception as e:
            errors.append(f"ディスク容量を確認できませんでした: {e}")

        # Check write permissions
        test_file = self.install_dir / ".write_test"
        try:
            self.install_dir.mkdir(parents=True, exist_ok=True)
            test_file.touch()
            test_file.unlink()
        except Exception as e:
            errors.append(f"{self.install_dir}への書き込み権限がありません: {e}")

        return len(errors) == 0, errors

    def create_backup(self) -> Optional[Path]:
        """
        既存のインストールのバックアップを作成します
        
        Returns:
            バックアップアーカイブへのパス、または既存のインストールがない場合はNone
        """
        if not self.install_dir.exists():
            return None

        if self.dry_run:
            return self.install_dir / "backup_dryrun.tar.gz"

        # Create backup directory
        backup_dir = self.install_dir / "backups"
        backup_dir.mkdir(exist_ok=True)

        # Create timestamped backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"superclaude_backup_{timestamp}"
        backup_path = backup_dir / f"{backup_name}.tar.gz"

        # Create temporary directory for backup
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_backup = Path(temp_dir) / backup_name

            # Ensure temp backup directory exists
            temp_backup.mkdir(parents=True, exist_ok=True)

            # Copy all files except backups and local directories
            for item in self.install_dir.iterdir():
                if item.name not in ["backups", "local"]:
                    try:
                        if item.is_file():
                            shutil.copy2(item, temp_backup / item.name)
                        elif item.is_dir():
                            shutil.copytree(item, temp_backup / item.name)
                    except Exception as e:
                        # Log warning but continue backup process
                        self.logger.warning(f"{item.name}をバックアップできませんでした: {e}")

            # Create archive only if there are files to backup
            if any(temp_backup.iterdir()):
                # shutil.make_archive adds .tar.gz automatically, so use base name without extensions
                base_path = backup_dir / backup_name
                shutil.make_archive(str(base_path), 'gztar', temp_backup)
            else:
                # Create empty backup file to indicate backup was attempted
                backup_path.touch()
                self.logger.warning(
                    f"バックアップするファイルがありません。空のバックアップマーカーを作成しました: {backup_path.name}"
                )

        self.backup_path = backup_path
        return backup_path

    def install_component(self, component_name: str,
                          config: Dict[str, Any]) -> bool:
        """
        単一のコンポーネントをインストールします
        
        Args:
            component_name: インストールするコンポーネントの名前
            config: インストール設定
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        if component_name not in self.components:
            raise ValueError(f"Unknown component: {component_name}")

        component = self.components[component_name]

        # Skip if already installed
        if component_name in self.installed_components:
            return True

        # Check prerequisites
        success, errors = component.validate_prerequisites()
        if not success:
            self.logger.error(f"{component_name}の前提条件が失敗しました:")
            for error in errors:
                self.logger.error(f"  - {error}")
            self.failed_components.add(component_name)
            return False

        # Perform installation
        try:
            if self.dry_run:
                self.logger.info(f"[ドライラン] {component_name}をインストールします")
                success = True
            else:
                success = component.install(config)

            if success:
                self.installed_components.add(component_name)
                self.updated_components.add(component_name)
            else:
                self.failed_components.add(component_name)

            return success

        except Exception as e:
            self.logger.error(f"{component_name}のインストール中にエラーが発生しました: {e}")
            self.failed_components.add(component_name)
            return False

    def install_components(self,
                           component_names: List[str],
                           config: Optional[Dict[str, Any]] = None) -> bool:
        """
        依存関係の順序で複数のコンポーネントをインストールします
        
        Args:
            component_names: インストールするコンポーネント名のリスト
            config: インストール設定
            
        Returns:
            すべて成功した場合はTrue、いずれかが失敗した場合はFalse
        """
        config = config or {}

        # Resolve dependencies
        try:
            ordered_names = self.resolve_dependencies(component_names)
        except ValueError as e:
            self.logger.error(f"依存関係の解決エラー: {e}")
            return False

        # Validate system requirements
        success, errors = self.validate_system_requirements()
        if not success:
            self.logger.error("システム要件が満たされていません:")
            for error in errors:
                self.logger.error(f"  - {error}")
            return False

        # Create backup if updating
        if self.install_dir.exists() and not self.dry_run:
            self.logger.info("既存のインストールのバックアップを作成中...")
            try:
                self.create_backup()
            except Exception as e:
                self.logger.error(f"バックアップの作成に失敗しました: {e}")
                return False

        # Install each component
        all_success = True
        for name in ordered_names:
            self.logger.info(f"{name}をインストール中...")
            if not self.install_component(name, config):
                all_success = False
                # Continue installing other components even if one fails

        if not self.dry_run:
            self._run_post_install_validation()

        return all_success

    def _run_post_install_validation(self) -> None:
        """インストールされたすべてのコンポーネントに対してインストール後の検証を実行"""
        self.logger.info("インストール後の検証を実行中...")

        all_valid = True
        for name in self.installed_components:
            component = self.components[name]
            success, errors = component.validate_installation()

            if success:
                self.logger.info(f"  ✓ {name}: 有効")
            else:
                self.logger.error(f"  ✗ {name}: 無効")
                for error in errors:
                    self.logger.error(f"    - {error}")
                all_valid = False

        if all_valid:
            self.logger.info("すべてのコンポーネントが正常に検証されました！")
        else:
            self.logger.error("一部のコンポーネントの検証に失敗しました。上記のエラーを確認してください。")
    def update_components(self, component_names: List[str], config: Dict[str, Any]) -> bool:
        """更新操作のエイリアス（インストールロジックを使用）"""
        return self.install_components(component_names, config)


    def get_installation_summary(self) -> Dict[str, Any]:
        """
        インストール結果の概要を取得します

        Returns:
            インストールの統計と結果を含む辞書
        """
        return {
            'installed': list(self.installed_components),
            'failed': list(self.failed_components),
            'skipped': list(self.skipped_components),
            'backup_path': str(self.backup_path) if self.backup_path else None,
            'install_dir': str(self.install_dir),
            'dry_run': self.dry_run
        }

    def get_update_summary(self) -> Dict[str, Any]:
        return {
            'updated': list(self.updated_components),
            'failed': list(self.failed_components),
            'backup_path': str(self.backup_path) if self.backup_path else None
        }
