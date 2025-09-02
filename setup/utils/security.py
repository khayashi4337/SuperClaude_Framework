"""
SuperClaudeインストールシステム用のセキュリティユーティリティ
パスの検証と入力のサニタイズ

このモジュールは、SuperClaudeのインストール中にファイルパスとユーザー入力の包括的なセキュリティ検証を提供します。
これには、以下の保護が含まれます:
- ディレクトリトラバーサル攻撃
- システムディレクトリへのインストール
- パスインジェクション攻撃
- クロスプラットフォームのセキュリティ問題

主な機能:
- プラットフォーム固有の検証（Windows対Unix）
- 実行可能な提案を含むユーザーフレンドリーなエラーメッセージ
- 包括的なパスの正規化
- 既存の検証ロジックとの下位互換性

修正された問題:
- GitHub Issue #129: "dev"、"tmp"、"bin"などを含む正当なパスへのインストールを妨げていた過度に広範な正規表現パターンを修正
- クロスプラットフォーム互換性の強化
- エラーメッセージの明確さの向上

アーキテクチャ:
- 保守性を向上させるためにパターンカテゴリを分離
- プラットフォームを意識した検証ロジック
- 包括的なテストカバレッジ
"""

import re
import os
from pathlib import Path
from typing import List, Optional, Tuple, Set
import urllib.parse


class SecurityValidator:
    """セキュリティ検証ユーティリティ"""
    
    # Directory traversal patterns (match anywhere in path - platform independent)
    # These patterns detect common directory traversal attack vectors
    TRAVERSAL_PATTERNS = [
        r'\.\./',           # Directory traversal using ../
        r'\.\.\.',          # Directory traversal using ...
        r'//+',             # Multiple consecutive slashes (path injection)
    ]
    
    # Unix system directories (match only at start of path)
    # These patterns identify Unix/Linux system directories that should not be writable
    # by regular users. Using ^ anchor to match only at path start prevents false positives
    # for user directories containing these names (e.g., /home/user/dev/ は許可されています)
    UNIX_SYSTEM_PATTERNS = [
        r'^/etc/',          # System configuration files
        r'^/bin/',          # Essential command binaries
        r'^/sbin/',         # System binaries
        r'^/usr/bin/',      # User command binaries
        r'^/usr/sbin/',     # Non-essential system binaries
        r'^/var/',          # Variable data files
        r'^/tmp/',          # Temporary files (system-wide)
        r'^/dev/',          # Device files - FIXED: was r'/dev/' (GitHub Issue #129)
        r'^/proc/',         # Process information pseudo-filesystem
        r'^/sys/',          # System information pseudo-filesystem
    ]
    
    # Windows system directories (match only at start of path)
    # These patterns identify Windows system directories using flexible separator matching
    # to handle both forward slashes and backslashes consistently
    WINDOWS_SYSTEM_PATTERNS = [
        r'^c:[/\\]windows[/\\]',        # Windows system directory
        r'^c:[/\\]program files[/\\]',  # Program Files directory
        # Note: Removed c:\\users\\ to allow installation in user directories
        # Claude Code installs to user home directory by default
    ]
    
    # Combined dangerous patterns for backward compatibility
    # This maintains compatibility with existing code while providing the new categorized approach
    DANGEROUS_PATTERNS = TRAVERSAL_PATTERNS + UNIX_SYSTEM_PATTERNS + WINDOWS_SYSTEM_PATTERNS
    
    # Dangerous filename patterns
    DANGEROUS_FILENAMES = [
        r'\.exe$',          # Executables
        r'\.bat$',
        r'\.cmd$',
        r'\.scr$',
        r'\.dll$',
        r'\.so$',
        r'\.dylib$',
        r'passwd',          # System files
        r'shadow',
        r'hosts',
        r'\.ssh/',
        r'\.aws/',
        r'\.env',           # Environment files
        r'\.secret',
    ]
    
    # Allowed file extensions for installation
    ALLOWED_EXTENSIONS = {
        '.md', '.json', '.py', '.js', '.ts', '.jsx', '.tsx',
        '.txt', '.yml', '.yaml', '.toml', '.cfg', '.conf',
        '.sh', '.ps1', '.html', '.css', '.svg', '.png', '.jpg', '.gif'
    }
    
    # Maximum path lengths
    MAX_PATH_LENGTH = 4096
    MAX_FILENAME_LENGTH = 255
    
    @classmethod
    def validate_path(cls, path: Path, base_dir: Optional[Path] = None) -> Tuple[bool, str]:
        """
        強化されたクロスプラットフォームサポートでパスのセキュリティ問題を検証します
        
        このメソッドは以下を含む包括的なセキュリティ検証を実行します:
        - ディレクトリトラバーサル攻撃の検出
        - システムディレクトリの保護（プラットフォーム固有）
        - パスの長さとファイル名の検証
        - クロスプラットフォームのパス正規化
        - ユーザーフレンドリーなエラーメッセージ
        
        アーキテクチャ:
        - 検証に元のパスと解決されたパスの両方を使用
        - システムディレクトリにプラットフォーム固有のパターンを適用
        - 正規化前に攻撃をキャッチするために元のパスに対してトラバーサルパターンをチェック
        - 実行可能な提案を含む詳細なエラーメッセージを提供
        
        Args:
            path: 検証するパス（相対または絶対パス）
            base_dir: パスが含まれるべき基本ディレクトリ（オプション）
            
        Returns:
            (安全: bool, エラーメッセージ: str)のタプル
            - is_safe: パスがすべてのセキュリティチェックに合格した場合はTrue
            - error_message: 検証が失敗した場合の提案付きの詳細なエラーメッセージ
        """
        try:
            # Convert to absolute path
            abs_path = path.resolve()
            
            # For system directory validation, use the original path structure
            # to avoid issues with symlinks and cross-platform path resolution
            original_path_str = cls._normalize_path_for_validation(path)
            resolved_path_str = cls._normalize_path_for_validation(abs_path)
            
            # Check path length
            if len(str(abs_path)) > cls.MAX_PATH_LENGTH:
                return False, f"Path too long: {len(str(abs_path))} > {cls.MAX_PATH_LENGTH}"
            
            # Check filename length
            if len(abs_path.name) > cls.MAX_FILENAME_LENGTH:
                return False, f"ファイル名が長すぎます: {len(abs_path.name)} > {cls.MAX_FILENAME_LENGTH}"
            
            # Check for dangerous patterns using platform-specific validation
            # Always check traversal patterns (platform independent) - use original path string
            # to detect patterns before normalization removes them
            original_str = str(path).lower()
            for pattern in cls.TRAVERSAL_PATTERNS:
                if re.search(pattern, original_str, re.IGNORECASE):
                    return False, cls._get_user_friendly_error_message("traversal", pattern, abs_path)
            
            # Check platform-specific system directory patterns - use original path first, then resolved
            # Always check both Windows and Unix patterns to handle cross-platform scenarios
            
            # Check Windows system directory patterns
            for pattern in cls.WINDOWS_SYSTEM_PATTERNS:
                if (re.search(pattern, original_path_str, re.IGNORECASE) or 
                    re.search(pattern, resolved_path_str, re.IGNORECASE)):
                    return False, cls._get_user_friendly_error_message("windows_system", pattern, abs_path)
            
            # Check Unix system directory patterns
            for pattern in cls.UNIX_SYSTEM_PATTERNS:
                if (re.search(pattern, original_path_str, re.IGNORECASE) or 
                    re.search(pattern, resolved_path_str, re.IGNORECASE)):
                    return False, cls._get_user_friendly_error_message("unix_system", pattern, abs_path)
            
            # Check for dangerous filenames
            for pattern in cls.DANGEROUS_FILENAMES:
                if re.search(pattern, abs_path.name, re.IGNORECASE):
                    return False, f"危険なファイル名パターンが検出されました: {pattern}"
            
            # Check if path is within base directory
            if base_dir:
                base_abs = base_dir.resolve()
                try:
                    abs_path.relative_to(base_abs)
                except ValueError:
                    return False, f"許可されたディレクトリ外のパス: {abs_path} がありません {base_abs}"
            
            # Check for null bytes
            if '\x00' in str(path):
                return False, "パスにヌルバイトが検出されました"
            
            # Check for Windows reserved names
            if os.name == 'nt':
                reserved_names = [
                    'CON', 'PRN', 'AUX', 'NUL',
                    'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                    'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
                ]
                
                name_without_ext = abs_path.stem.upper()
                if name_without_ext in reserved_names:
                    return False, f"予約済みのWindowsファイル名: {name_without_ext}"
            
            return True, "パスは安全です"
            
        except Exception as e:
            return False, f"パス検証エラー: {e}"
    
    @classmethod
    def validate_file_extension(cls, path: Path) -> Tuple[bool, str]:
        """
        ファイル拡張子が許可されているか検証します
        
        Args:
            path: 検証するパス
            
        Returns:
            (許可されている: bool, メッセージ: str)のタプル
        """
        extension = path.suffix.lower()
        
        if not extension:
            return True, "拡張子なし（許可）"
        
        if extension in cls.ALLOWED_EXTENSIONS:
            return True, f"拡張子 {extension} は許可されています"
        else:
            return False, f"拡張子 {extension} は許可されていません"
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """
        危険な文字を削除してファイル名をサニタイズします
        
        Args:
            filename: 元のファイル名
            
        Returns:
            サニタイズされたファイル名
        """
        # Remove null bytes
        filename = filename.replace('\x00', '')
        
        # Remove or replace dangerous characters
        dangerous_chars = r'[<>:"/\\|?*\x00-\x1f]'
        filename = re.sub(dangerous_chars, '_', filename)
        
        # Remove leading/trailing dots and spaces
        filename = filename.strip('. ')
        
        # Ensure not empty
        if not filename:
            filename = 'unnamed'
        
        # Truncate if too long
        if len(filename) > cls.MAX_FILENAME_LENGTH:
            name, ext = os.path.splitext(filename)
            max_name_len = cls.MAX_FILENAME_LENGTH - len(ext)
            filename = name[:max_name_len] + ext
        
        # Check for Windows reserved names
        if os.name == 'nt':
            name_without_ext = os.path.splitext(filename)[0].upper()
            reserved_names = [
                'CON', 'PRN', 'AUX', 'NUL',
                'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
            ]
            
            if name_without_ext in reserved_names:
                filename = f"safe_{filename}"
        
        return filename
    
    @classmethod
    def sanitize_input(cls, user_input: str, max_length: int = 1000) -> str:
        """
        ユーザー入力をサニタイズします
        
        Args:
            user_input: 生のユーザー入力
            max_length: 許可される最大長
            
        Returns:
            サニタイズされた入力
        """
        if not user_input:
            return ""
        
        # Remove null bytes and control characters
        sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', user_input)
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        # Truncate if too long
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @classmethod
    def validate_url(cls, url: str) -> Tuple[bool, str]:
        """
        URLのセキュリティ問題を検証します
        
        Args:
            url: 検証するURL
            
        Returns:
            (安全: bool, メッセージ: str)のタプル
        """
        try:
            parsed = urllib.parse.urlparse(url)
            
            # Check scheme
            if parsed.scheme not in ['http', 'https']:
                return False, f"無効なスキーム: {parsed.scheme}"
            
            # Check for localhost/private IPs (basic check)
            hostname = parsed.hostname
            if hostname:
                if hostname.lower() in ['localhost', '127.0.0.1', '::1']:
                    return False, "localhostのURLは許可されていません"
                
                # Basic private IP check
                if hostname.startswith('192.168.') or hostname.startswith('10.') or hostname.startswith('172.'):
                    return False, "プライベートIPアドレスは許可されていません"
            
            # Check URL length
            if len(url) > 2048:
                return False, "URLが長すぎます"
            
            return True, "URLは安全です"
            
        except Exception as e:
            return False, f"URL検証エラー: {e}"
    
    @classmethod
    def check_permissions(cls, path: Path, required_permissions: Set[str]) -> Tuple[bool, List[str]]:
        """
        Check file/directory permissions
        
        Args:
            path: Path to check
            required_permissions: Set of required permissions ('read', 'write', 'execute')
            
        Returns:
            Tuple of (has_permissions: bool, missing_permissions: List[str])
        """
        missing = []
        
        try:
            if not path.exists():
                # For non-existent paths, check parent directory
                parent = path.parent
                if not parent.exists():
                    missing.append("パスが存在しません")
                    return False, missing
                path = parent
            
            if 'read' in required_permissions:
                if not os.access(path, os.R_OK):
                    missing.append('read')
            
            if 'write' in required_permissions:
                if not os.access(path, os.W_OK):
                    missing.append('write')
            
            if 'execute' in required_permissions:
                if not os.access(path, os.X_OK):
                    missing.append('execute')
            
            return len(missing) == 0, missing
            
        except Exception as e:
            missing.append(f"権限チェックエラー: {e}")
            return False, missing
    
    @classmethod
    def validate_installation_target(cls, target_dir: Path) -> Tuple[bool, List[str]]:
        """
        強化されたWindows互換性でインストール先のディレクトリを検証します
        
        Args:
            target_dir: ターゲットインストールディレクトリ
            
        Returns:
            (安全: bool, エラーメッセージ: List[str])のタプル
        """
        errors = []
        
        # Enhanced path resolution with Windows normalization
        try:
            abs_target = target_dir.resolve()
        except Exception as e:
            errors.append(f"ターゲットパスを解決できません: {e}")
            return False, errors
            
        # Windows-specific path normalization
        if os.name == 'nt':
            # Normalize Windows paths for consistent comparison
            abs_target_str = str(abs_target).lower().replace('/', '\\')
        else:
            abs_target_str = str(abs_target).lower()
        
        # Special handling for Claude installation directory
        claude_patterns = ['.claude', '.claude' + os.sep, '.claude\\', '.claude/']
        is_claude_dir = any(abs_target_str.endswith(pattern) for pattern in claude_patterns)
        
        if is_claude_dir:
            try:
                home_path = Path.home()
            except (RuntimeError, OSError):
                # If we can't determine home directory, skip .claude special handling
                cls._log_security_decision("WARN", f".claudeの検証のためにホームディレクトリを特定できません: {abs_target}")
                # Fall through to regular validation
            else:
                try:
                    # Verify it's specifically the current user's home directory
                    abs_target.relative_to(home_path)
                    
                    # Enhanced Windows security checks for .claude directories
                    if os.name == 'nt':
                        # Check for junction points and symbolic links on Windows
                        if cls._is_windows_junction_or_symlink(abs_target):
                            errors.append("セキュリティ上の理由から、ジャンクションポイントまたはシンボリックリンクへのインストールは許可されていません")
                            return False, errors
                        
                        # Additional validation: verify it's in the current user's profile directory
                        # Use actual home directory comparison instead of username-based path construction
                        if ':' in abs_target_str and '\\users\\' in abs_target_str:
                            try:
                                # Check if target is within the user's actual home directory
                                home_path = Path.home()
                                abs_target.relative_to(home_path)
                                # Path is valid - within user's home directory
                            except ValueError:
                                # Path is outside user's home directory
                                current_user = os.environ.get('USERNAME', home_path.name)
                                errors.append(f"インストールは現在のユーザーのディレクトリ内で行う必要があります ({current_user})")
                                return False, errors
                    
                    # Check permissions
                    has_perms, missing = cls.check_permissions(target_dir, {'read', 'write'})
                    if not has_perms:
                        if os.name == 'nt':
                            errors.append(f"Windowsインストールのための権限が不十分です: {missing}. 管理者として実行するか、フォルダの権限を確認してみてください。")
                        else:
                            errors.append(f"権限が不十分です: 不足 {missing}")
                    
                    # Log successful validation for audit trail
                    cls._log_security_decision("ALLOW", f"Claudeディレクトリのインストールが検証されました: {abs_target}")
                    return len(errors) == 0, errors
                    
                except ValueError:
                    # Not under current user's home directory
                    if os.name == 'nt':
                        errors.append("Claude installation must be in your user directory (e.g., C:\\Users\\YourName\\.claude)")
                    else:
                        errors.append("Claude installation must be in your home directory (e.g., ~/.claude)")
                    cls._log_security_decision("DENY", f"ユーザーホーム外のClaudeディレクトリ: {abs_target}")
                    return False, errors
        
        # Validate path for non-.claude directories
        is_safe, msg = cls.validate_path(target_dir)
        if not is_safe:
            if os.name == 'nt':
                # Enhanced Windows error messages
                if "危険なパスパターン" in msg.lower():
                    errors.append(f"無効なWindowsパス: {msg}. パスに危険なパターンや予約されたディレクトリが含まれていないことを確認してください。")
                elif "パスが長すぎます" in msg.lower():
                    errors.append(f"Windowsパスが長すぎます: {msg}. Windowsでは、ほとんどのパスに260文字の制限があります。")
                elif "reserved" in msg.lower():
                    errors.append(f"Windows予約名: {msg}. CON, PRN, AUX, NUL, COM1-9, LPT1-9のような名前は避けてください。")
                else:
                    errors.append(f"無効なターゲットパス: {msg}")
            else:
                errors.append(f"無効なターゲットパス: {msg}")
        
        # Check permissions with platform-specific guidance
        has_perms, missing = cls.check_permissions(target_dir, {'read', 'write'})
        if not has_perms:
            if os.name == 'nt':
                errors.append(f"Windowsの権限が不十分です: {missing}. 管理者として実行するか、プロパティ > セキュリティでフォルダのセキュリティ設定を確認してみてください。")
            else:
                errors.append(f"Insufficient permissions: {missing}. 試してください: chmod 755 {target_dir}")
        
        # Check if it's a system directory with enhanced messages
        system_dirs = [
            Path('/etc'), Path('/bin'), Path('/sbin'), Path('/usr/bin'), Path('/usr/sbin'),
            Path('/var'), Path('/tmp'), Path('/dev'), Path('/proc'), Path('/sys')
        ]
        
        if os.name == 'nt':
            system_dirs.extend([
                Path('C:\\Windows'), Path('C:\\Program Files'), Path('C:\\Program Files (x86)')
            ])
        
        for sys_dir in system_dirs:
            try:
                if abs_target.is_relative_to(sys_dir):
                    if os.name == 'nt':
                        errors.append(f"Windowsシステムディレクトリにインストールできません: {sys_dir}. Use a location in your user profile instead (e.g., C:\\Users\\YourName\\).")
                    else:
                        errors.append(f"Cannot install to system directory: {sys_dir}. Use a location in your home directory instead (~/).")
                    cls._log_security_decision("DENY", f"システムディレクトリへのインストールが試みられました: {sys_dir}")
                    break
            except (ValueError, AttributeError):
                # is_relative_to not available in older Python versions
                try:
                    abs_target.relative_to(sys_dir)
                    errors.append(f"Cannot install to system directory: {sys_dir}")
                    break
                except ValueError:
                    continue
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_component_files(cls, file_list: List[Tuple[Path, Path]], base_source_dir: Path, base_target_dir: Path) -> Tuple[bool, List[str]]:
        """
        コンポーネントインストールのためのファイルリストを検証します
        
        Args:
            file_list: (ソース, ターゲット) パスタプルのリスト
            base_source_dir: 基本ソースディレクトリ
            base_target_dir: 基本ターゲットディレクトリ
            
        Returns:
            (すべて安全: bool, エラーメッセージ: List[str])のタプル
        """
        errors = []
        
        for source, target in file_list:
            # Validate source path
            is_safe, msg = cls.validate_path(source, base_source_dir)
            if not is_safe:
                errors.append(f"無効なソースパス {source}: {msg}")
            
            # Validate target path
            is_safe, msg = cls.validate_path(target, base_target_dir)
            if not is_safe:
                errors.append(f"無効なターゲットパス {target}: {msg}")
            
            # Validate file extension
            is_allowed, msg = cls.validate_file_extension(source)
            if not is_allowed:
                errors.append(f"ファイル {source}: {msg}")
        
        return len(errors) == 0, errors
    
    @classmethod
    def _normalize_path_for_validation(cls, path: Path) -> str:
        """
        プラットフォーム間で一貫した検証のためにパスを正規化します
        
        Args:
            path: 正規化するパス
            
        Returns:
            検証用の正規化されたパス文字列
        """
        path_str = str(path)
        
        # Convert to lowercase for case-insensitive comparison
        path_str = path_str.lower()
        
        # Normalize path separators for consistent pattern matching
        if os.name == 'nt':  # Windows
            # Convert forward slashes to backslashes for Windows
            path_str = path_str.replace('/', '\\')
            # Ensure consistent drive letter format
            if len(path_str) >= 2 and path_str[1] == ':':
                path_str = path_str[0] + ':\\' + path_str[3:].lstrip('\\')
        else:  # Unix-like systems
            # Convert backslashes to forward slashes for Unix
            path_str = path_str.replace('\\', '/')
            # Ensure single leading slash
            if path_str.startswith('//'):
                path_str = '/' + path_str.lstrip('/')
        
        return path_str
    
    @classmethod
    def _get_user_friendly_error_message(cls, error_type: str, pattern: str, path: Path) -> str:
        """
        実行可能な提案を含むユーザーフレンドリーなエラーメッセージを生成します
        
        Args:
            error_type: エラーの種類 (traversal, windows_system, unix_system)
            pattern: 一致した正規表現パターン
            path: エラーを引き起こしたパス
            
        Returns:
            提案付きのユーザーフレンドリーなエラーメッセージ
        """
        if error_type == "traversal":
            return (
                f"セキュリティ違反: パス 'でディレクトリトラバーサルパターンが検出されました{path}'. "
                f"Paths containing '..' or '//' are not allowed for security reasons. "
                f"Please use an absolute path without directory traversal characters."
            )
        elif error_type == "windows_system":
            if pattern == r'^c:\\windows\\':
                return (
                    f"Windowsシステムディレクトリにインストールできません '{path}'. "
                    f"Please choose a location in your user directory instead, "
                    f"such as C:\\Users\\{os.environ.get('USERNAME', 'YourName')}\\.claude\\"
                )
            elif pattern == r'^c:\\program files\\':
                return (
                    f"Program Filesディレクトリにインストールできません '{path}'. "
                    f"Please choose a location in your user directory instead, "
                    f"such as C:\\Users\\{os.environ.get('USERNAME', 'YourName')}\\.claude\\"
                )
            else:
                return (
                    f"Windowsシステムディレクトリにインストールできません '{path}'. "
                    f"Please choose a location in your user directory instead."
                )
        elif error_type == "unix_system":
            system_dirs = {
                r'^/dev/': "/dev (device files)",
                r'^/etc/': "/etc (system configuration)",
                r'^/bin/': "/bin (system binaries)",
                r'^/sbin/': "/sbin (system binaries)",
                r'^/usr/bin/': "/usr/bin (user binaries)",
                r'^/usr/sbin/': "/usr/sbin (user system binaries)",
                r'^/var/': "/var (variable data)",
                r'^/tmp/': "/tmp (temporary files)",
                r'^/proc/': "/proc (process information)",
                r'^/sys/': "/sys (system information)"
            }
            
            dir_desc = system_dirs.get(pattern, "システムディレクトリ")
            return (
                f"Cannot install to {dir_desc} '{path}'. "
                f"Please choose a location in your home directory instead, "
                f"such as ~/.claude/ or ~/SuperClaude/"
            )
        else:
            return f"パス 'のセキュリティ検証に失敗しました{path}'"
    
    @classmethod
    def _is_windows_junction_or_symlink(cls, path: Path) -> bool:
        """
        パスがWindowsのジャンクションポイントまたはシンボリックリンクであるかを確認します
        
        Args:
            path: 確認するパス
            
        Returns:
            パスがジャンクションポイントまたはシンボリックリンクの場合はTrue、それ以外はFalse
        """
        if os.name != 'nt':
            return False
            
        try:
            # Only check if path exists to avoid filesystem errors during testing
            if not path.exists():
                return False
                
            # Check if path is a symlink (covers most cases)
            if path.is_symlink():
                return True
                
            # Additional Windows-specific checks for junction points
            try:
                import stat
                st = path.stat()
                # Check for reparse point (junction points have this attribute)
                if hasattr(st, 'st_reparse_tag') and st.st_reparse_tag != 0:
                    return True
            except (OSError, AttributeError):
                pass
                    
            # Alternative method using os.path.islink
            try:
                if os.path.islink(str(path)):
                    return True
            except (OSError, AttributeError):
                pass
                
        except (OSError, AttributeError, NotImplementedError):
            # If we can't determine safely, default to False
            # This ensures the function doesn't break validation
            pass
            
        return False
    
    @classmethod
    def _log_security_decision(cls, action: str, message: str) -> None:
        """
        監査証跡のためにセキュリティ検証の決定をログに記録します
        
        Args:
            action: 実行されたセキュリティアクション (ALLOW, DENY, WARN)
            message: 決定の説明
        """
        try:
            import logging
            import datetime
            
            # Create security logger if it doesn't exist
            security_logger = logging.getLogger('superclaude.security')
            if not security_logger.handlers:
                # Set up basic logging if not already configured
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
                )
                handler.setFormatter(formatter)
                security_logger.addHandler(handler)
                security_logger.setLevel(logging.INFO)
            
            # Log the security decision
            timestamp = datetime.datetime.now().isoformat()
            log_message = f"[{action}] {message} (PID: {os.getpid()})"
            
            if action == "DENY":
                security_logger.warning(log_message)
            else:
                security_logger.info(log_message)
                
        except Exception:
            # Don't fail security validation if logging fails
            pass
    
    @classmethod
    def create_secure_temp_dir(cls, prefix: str = "superclaude_") -> Path:
        """
        安全な一時ディレクトリを作成します
        
        Args:
            prefix: 一時ディレクトリ名のプレフィックス
            
        Returns:
            安全な一時ディレクトリへのパス
        """
        import tempfile
        
        # Create with secure permissions (0o700)
        temp_dir = Path(tempfile.mkdtemp(prefix=prefix))
        temp_dir.chmod(0o700)
        
        return temp_dir
    
    @classmethod
    def secure_delete(cls, path: Path) -> bool:
        """
        ファイルまたはディレクトリを安全に削除します
        
        Args:
            path: 削除するパス
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        try:
            if not path.exists():
                return True
            
            if path.is_file():
                # Overwrite file with random data before deletion
                try:
                    import secrets
                    file_size = path.stat().st_size
                    
                    with open(path, 'r+b') as f:
                        # Overwrite with random data
                        f.write(secrets.token_bytes(file_size))
                        f.flush()
                        os.fsync(f.fileno())
                except Exception:
                    pass  # If overwrite fails, still try to delete
                
                path.unlink()
            
            elif path.is_dir():
                # Recursively delete directory contents
                import shutil
                shutil.rmtree(path)
            
            return True
            
        except Exception:
            return False