"""
SuperClaudeインストールシステム用のクロスプラットフォームファイル管理
"""

import shutil
import stat
from typing import List, Optional, Callable, Dict, Any
from pathlib import Path
import fnmatch
import hashlib


class FileService:
    """クロスプラットフォームファイル操作マネージャー"""
    
    def __init__(self, dry_run: bool = False):
        """
        ファイルマネージャーを初期化します
        
        Args:
            dry_run: Trueの場合、ファイル操作をシミュレートするだけです
        """
        self.dry_run = dry_run
        self.copied_files: List[Path] = []
        self.created_dirs: List[Path] = []
        
    def copy_file(self, source: Path, target: Path, preserve_permissions: bool = True) -> bool:
        """
        権限を保持して単一ファイルをコピーします
        
        Args:
            source: ソースファイルパス
            target: ターゲットファイルパス
            preserve_permissions: ファイル権限を保持するかどうか
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        if not source.exists():
            raise FileNotFoundError(f"ソースファイルが見つかりません: {source}")
        
        if not source.is_file():
            raise ValueError(f"ソースはファイルではありません: {source}")
        
        if self.dry_run:
            print(f"[ドライラン] コピーします {source} -> {target}")
            return True
        
        try:
            # Ensure target ディレクトリ exists
            target.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            if preserve_permissions:
                shutil.copy2(source, target)
            else:
                shutil.copy(source, target)
            
            self.copied_files.append(target)
            return True
            
        except Exception as e:
            print(f"Error copying {source} to {target}: {e}")
            return False
    
    def copy_directory(self, source: Path, target: Path, ignore_patterns: Optional[List[str]] = None) -> bool:
        """
        gitignore形式のパターンでディレクトリを再帰的にコピーします
        
        Args:
            source: ソースディレクトリパス
            target: ターゲットディレクトリパス
            ignore_patterns: 無視するパターンのリスト（gitignore形式）
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        if not source.exists():
            raise FileNotFoundError(f"ソースディレクトリが見つかりません: {source}")
        
        if not source.is_dir():
            raise ValueError(f"ソースはディレクトリではありません: {source}")
        
        ignore_patterns = ignore_patterns or []
        default_ignores = ['.git', '.gitignore', '__pycache__', '*.pyc', '.DS_Store']
        all_ignores = ignore_patterns + default_ignores
        
        if self.dry_run:
            print(f"[ドライラン] ディレクトリをコピーします {source} -> {target}")
            return True
        
        try:
            # Create ignore function
            def ignore_func(directory: str, contents: List[str]) -> List[str]:
                ignored = []
                for item in contents:
                    item_path = Path(directory) / item
                    rel_path = item_path.relative_to(source)
                    
                    # Check against ignore patterns
                    for pattern in all_ignores:
                        if fnmatch.fnmatch(item, pattern) or fnmatch.fnmatch(str(rel_path), pattern):
                            ignored.append(item)
                            break
                
                return ignored
            
            # Copy tree
            shutil.copytree(source, target, ignore=ignore_func, dirs_exist_ok=True)
            
            # Track created directories and files
            for item in target.rglob('*'):
                if item.is_dir():
                    self.created_dirs.append(item)
                else:
                    self.copied_files.append(item)
            
            return True
            
        except Exception as e:
            print(f"ディレクトリのコピーエラー {source} to {target}: {e}")
            return False
    
    def ensure_directory(self, directory: Path, mode: int = 0o755) -> bool:
        """
        ディレクトリとその親が存在しない場合に作成します
        
        Args:
            directory: 作成するディレクトリパス
            mode: ディレクトリ権限（Unixのみ）
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        if self.dry_run:
            print(f"[ドライラン] ディレクトリを作成します {directory}")
            return True
        
        try:
            directory.mkdir(parents=True, exist_ok=True, mode=mode)
            
            if directory not in self.created_dirs:
                self.created_dirs.append(directory)
            
            return True
            
        except Exception as e:
            print(f"ディレクトリの作成エラー {directory}: {e}")
            return False
    
    def remove_file(self, file_path: Path) -> bool:
        """
        単一ファイルを削除します
        
        Args:
            file_path: 削除するファイルへのパス
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        if not file_path.exists():
            return True  # Already gone
        
        if self.dry_run:
            print(f"[ドライラン] ファイルを削除します {file_path}")
            return True
        
        try:
            if file_path.is_file():
                file_path.unlink()
            else:
                print(f"警告: {file_path} はファイルではないため、スキップします")
                return False
            
            # Remove from tracking
            if file_path in self.copied_files:
                self.copied_files.remove(file_path)
            
            return True
            
        except Exception as e:
            print(f"ファイルの削除エラー {file_path}: {e}")
            return False
    
    def remove_directory(self, directory: Path, recursive: bool = False) -> bool:
        """
        ディレクトリを削除します
        
        Args:
            directory: 削除するディレクトリパス
            recursive: 再帰的に削除するかどうか
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        if not directory.exists():
            return True  # Already gone
        
        if self.dry_run:
            action = "再帰的に削除" if recursive else "remove"
            print(f"[DRY RUN] Would {action} ディレクトリ {directory}")
            return True
        
        try:
            if recursive:
                shutil.rmtree(directory)
            else:
                directory.rmdir()  # Only works if empty
            
            # Remove from tracking
            if directory in self.created_dirs:
                self.created_dirs.remove(directory)
            
            return True
            
        except Exception as e:
            print(f"ディレクトリの削除エラー {directory}: {e}")
            return False
    
    def resolve_home_path(self, path: str) -> Path:
        """
        ~ を含むパスを任意のOSで実際のホームパスに変換します
        
        Args:
            path: ~ を含む可能性のあるパス文字列
            
        Returns:
            解決されたPathオブジェクト
        """
        return Path(path).expanduser().resolve()
    
    def make_executable(self, file_path: Path) -> bool:
        """
        Make file executable (Unix/Linux/macOS)
        
        Args:
            file_path: Path to file to make executable
            
        Returns:
            True if successful, False otherwise
        """
        if not file_path.exists():
            return False
        
        if self.dry_run:
            print(f"[ドライラン] 作成します {file_path} executable")
            return True
        
        try:
            # Get current permissions
            current_mode = file_path.stat().st_mode
            
            # Add execute permissions for owner, group, and others
            new_mode = current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            
            file_path.chmod(new_mode)
            return True
            
        except Exception as e:
            print(f"Error making {file_path} 実行可能: {e}")
            return False
    
    def get_file_hash(self, file_path: Path, algorithm: str = 'sha256') -> Optional[str]:
        """
        ファイルハッシュを計算します
        
        Args:
            file_path: ファイルへのパス
            algorithm: ハッシュアルゴリズム (md5, sha1, sha256, etc.)
            
        Returns:
            16進数のハッシュ文字列、またはエラーの場合はNone
        """
        if not file_path.exists() or not file_path.is_file():
            return None
        
        try:
            hasher = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                # Read in chunks for large files
                for chunk in iter(lambda: f.read(8192), b""):
                    hasher.update(chunk)
            
            return hasher.hexdigest()
            
        except Exception:
            return None
    
    def verify_file_integrity(self, file_path: Path, expected_hash: str, algorithm: str = 'sha256') -> bool:
        """
        ハッシュを使用してファイルの整合性を検証します
        
        Args:
            file_path: 検証するファイルへのパス
            expected_hash: 期待されるハッシュ値
            algorithm: 使用されるハッシュアルゴリズム
            
        Returns:
            ファイルが期待されるハッシュと一致する場合はTrue、それ以外はFalse
        """
        actual_hash = self.get_file_hash(file_path, algorithm)
        return actual_hash is not None and actual_hash.lower() == expected_hash.lower()
    
    def get_directory_size(self, directory: Path) -> int:
        """
        ディレクトリの合計サイズをバイト単位で計算します
        
        Args:
            directory: ディレクトリパス
            
        Returns:
            合計サイズ（バイト）
        """
        if not directory.exists() or not directory.is_dir():
            return 0
        
        total_size = 0
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception:
            pass  # Skip files we can't access
        
        return total_size
    
    def find_files(self, directory: Path, pattern: str = '*', recursive: bool = True) -> List[Path]:
        """
        パターンに一致するファイルを検索します
        
        Args:
            directory: 検索するディレクトリ
            pattern: 一致させるglobパターン
            recursive: 再帰的に検索するかどうか
            
        Returns:
            一致するファイルパスのリスト
        """
        if not directory.exists() or not directory.is_dir():
            return []
        
        try:
            if recursive:
                return list(directory.rglob(pattern))
            else:
                return list(directory.glob(pattern))
        except Exception:
            return []
    
    def backup_file(self, file_path: Path, backup_suffix: str = '.backup') -> Optional[Path]:
        """
        ファイルのバックアップコピーを作成します
        
        Args:
            file_path: バックアップするファイルへのパス
            backup_suffix: バックアップファイルに追加する接尾辞
            
        Returns:
            バックアップファイルへのパス、または失敗した場合はNone
        """
        if not file_path.exists() or not file_path.is_file():
            return None
        
        backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
        
        if self.copy_file(file_path, backup_path):
            return backup_path
        return None
    
    def get_free_space(self, path: Path) -> int:
        """
        パスの空きディスク容量をバイト単位で取得します
        
        Args:
            path: 確認するパス（ファイルまたはディレクトリ）
            
        Returns:
            空き容量（バイト）
        """
        try:
            if path.is_file():
                path = path.parent
            
            stat_result = shutil.disk_usage(path)
            return stat_result.free
        except Exception:
            return 0
    
    def cleanup_tracked_files(self) -> None:
        """このセッション中に作成されたすべてのファイルとディレクトリを削除"""
        if self.dry_run:
            print("[ドライラン] 追跡されたファイルをクリーンアップします")
            return
        
        # Remove files first
        for file_path in reversed(self.copied_files):
            try:
                if file_path.exists():
                    file_path.unlink()
            except Exception:
                pass
        
        # Remove directories (in reverse order of creation)
        for directory in reversed(self.created_dirs):
            try:
                if directory.exists() and not any(directory.iterdir()):
                    directory.rmdir()
            except Exception:
                pass
        
        self.copied_files.clear()
        self.created_dirs.clear()
    
    def get_operation_summary(self) -> Dict[str, Any]:
        """
        実行されたファイル操作の概要を取得します
        
        Returns:
            操作統計を含む辞書
        """
        return {
            'files_copied': len(self.copied_files),
            'directories_created': len(self.created_dirs),
            'dry_run': self.dry_run,
            'copied_files': [str(f) for f in self.copied_files],
            'created_directories': [str(d) for d in self.created_dirs]
        }