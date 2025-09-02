"""
SuperClaudeインストール要件のシステム検証
"""

import subprocess
import sys
import shutil
from typing import Tuple, List, Dict, Any, Optional
from pathlib import Path
import re

# Handle packaging import - if not available, use a simple version comparison
try:
    from packaging import version
    PACKAGING_AVAILABLE = True
except ImportError:
    PACKAGING_AVAILABLE = False
    
    class SimpleVersion:
        def __init__(self, version_str: str):
            self.version_str = version_str
            # Simple version parsing: split by dots and convert to integers
            try:
                self.parts = [int(x) for x in version_str.split('.')]
            except ValueError:
                self.parts = [0, 0, 0]
        
        def __lt__(self, other):
            if isinstance(other, str):
                other = SimpleVersion(other)
            # Pad with zeros to same length
            max_len = max(len(self.parts), len(other.parts))
            self_parts = self.parts + [0] * (max_len - len(self.parts))
            other_parts = other.parts + [0] * (max_len - len(other.parts))
            return self_parts < other_parts
        
        def __gt__(self, other):
            if isinstance(other, str):
                other = SimpleVersion(other)
            return not (self < other) and not (self == other)
        
        def __eq__(self, other):
            if isinstance(other, str):
                other = SimpleVersion(other)
            return self.parts == other.parts
    
    class version:
        @staticmethod
        def parse(version_str: str):
            return SimpleVersion(version_str)


class Validator:
    """システム要件バリデーター"""
    
    def __init__(self):
        """バリデーターを初期化"""
        self.validation_cache: Dict[str, Any] = {}
    
    def check_python(self, min_version: str = "3.8", max_version: Optional[str] = None) -> Tuple[bool, str]:
        """
        Pythonのバージョン要件を確認します
        
        Args:
            min_version: 必須の最小Pythonバージョン
            max_version: サポートされる最大Pythonバージョン（オプション）
            
        Returns:
            (成功: bool, メッセージ: str)のタプル
        """
        cache_key = f"python_{min_version}_{max_version}"
        if cache_key in self.validation_cache:
            return self.validation_cache[cache_key]
        
        try:
            # Get current Python version
            current_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            
            # Check minimum version
            if version.parse(current_version) < version.parse(min_version):
                help_msg = self.get_installation_help("python")
                result = (False, f"Python {min_version}+ が必要、見つかったのは {current_version}{help_msg}")
                self.validation_cache[cache_key] = result
                return result
            
            # Check maximum version if specified
            if max_version and version.parse(current_version) > version.parse(max_version):
                result = (False, f"Pythonバージョン {current_version} はサポートされている最大値を超えています {max_version}")
                self.validation_cache[cache_key] = result
                return result
            
            result = (True, f"Python {current_version} は要件を満たしています")
            self.validation_cache[cache_key] = result
            return result
            
        except Exception as e:
            result = (False, f"Pythonのバージョンを確認できませんでした: {e}")
            self.validation_cache[cache_key] = result
            return result
    
    def check_node(self, min_version: str = "16.0", max_version: Optional[str] = None) -> Tuple[bool, str]:
        """
        Check Node.js version requirements
        
        Args:
            min_version: Minimum required Node.js version
            max_version: Maximum supported Node.js version (optional)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        cache_key = f"node_{min_version}_{max_version}"
        if cache_key in self.validation_cache:
            return self.validation_cache[cache_key]
        
        try:
            # Check if node is installed - use shell=True on Windows for better PATH resolution
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True,
                text=True,
                timeout=10,
                shell=(sys.platform == "win32")
            )
            
            if result.returncode != 0:
                help_msg = self.get_installation_help("node")
                result_tuple = (False, f"Node.js がPATHに見つかりません{help_msg}")
                self.validation_cache[cache_key] = result_tuple
                return result_tuple
            
            # Parse version (format: v18.17.0)
            version_output = result.stdout.strip()
            if version_output.startswith('v'):
                current_version = version_output[1:]
            else:
                current_version = version_output
            
            # Check minimum version
            if version.parse(current_version) < version.parse(min_version):
                help_msg = self.get_installation_help("node")
                result_tuple = (False, f"Node.js {min_version}+ が必要、見つかったのは {current_version}{help_msg}")
                self.validation_cache[cache_key] = result_tuple
                return result_tuple
            
            # Check maximum version if specified
            if max_version and version.parse(current_version) > version.parse(max_version):
                result_tuple = (False, f"Node.js version {current_version} はサポートされている最大値を超えています {max_version}")
                self.validation_cache[cache_key] = result_tuple
                return result_tuple
            
            result_tuple = (True, f"Node.js {current_version} は要件を満たしています")
            self.validation_cache[cache_key] = result_tuple
            return result_tuple
            
        except subprocess.TimeoutExpired:
            result_tuple = (False, "Node.js version のチェックがタイムアウトしました")
            self.validation_cache[cache_key] = result_tuple
            return result_tuple
        except FileNotFoundError:
            help_msg = self.get_installation_help("node")
            result_tuple = (False, f"Node.js がPATHに見つかりません{help_msg}")
            self.validation_cache[cache_key] = result_tuple
            return result_tuple
        except Exception as e:
            result_tuple = (False, f"確認できませんでした Node.js version: {e}")
            self.validation_cache[cache_key] = result_tuple
            return result_tuple
    
    def check_claude_cli(self, min_version: Optional[str] = None) -> Tuple[bool, str]:
        """
        Claude CLIのインストールとバージョンを確認します
        
        Args:
            min_version: 必須の最小Claude CLIバージョン（オプション）
            
        Returns:
            (成功: bool, メッセージ: str)のタプル
        """
        cache_key = f"claude_cli_{min_version}"
        if cache_key in self.validation_cache:
            return self.validation_cache[cache_key]
        
        try:
            # Check if claude is installed - use shell=True on Windows for better PATH resolution
            result = subprocess.run(
                ['claude', '--version'],
                capture_output=True,
                text=True,
                timeout=10,
                shell=(sys.platform == "win32")
            )
            
            if result.returncode != 0:
                help_msg = self.get_installation_help("claude_cli")
                result_tuple = (False, f"Claude CLIがPATHに見つかりません{help_msg}")
                self.validation_cache[cache_key] = result_tuple
                return result_tuple
            
            # Parse version from output
            version_output = result.stdout.strip()
            version_match = re.search(r'(\d+\.\d+\.\d+)', version_output)
            
            if not version_match:
                result_tuple = (True, "Claude CLIが見つかりました (バージョン形式不明)")
                self.validation_cache[cache_key] = result_tuple
                return result_tuple
            
            current_version = version_match.group(1)
            
            # Check minimum version if specified
            if min_version and version.parse(current_version) < version.parse(min_version):
                result_tuple = (False, f"Claude CLI {min_version}+ が必要、見つかったのは {current_version}")
                self.validation_cache[cache_key] = result_tuple
                return result_tuple
            
            result_tuple = (True, f"Claude CLI {current_version} found")
            self.validation_cache[cache_key] = result_tuple
            return result_tuple
            
        except subprocess.TimeoutExpired:
            result_tuple = (False, "Claude CLIのバージョンチェックがタイムアウトしました")
            self.validation_cache[cache_key] = result_tuple
            return result_tuple
        except FileNotFoundError:
            help_msg = self.get_installation_help("claude_cli")
            result_tuple = (False, f"Claude CLIがPATHに見つかりません{help_msg}")
            self.validation_cache[cache_key] = result_tuple
            return result_tuple
        except Exception as e:
            result_tuple = (False, f"Claude CLIを確認できませんでした: {e}")
            self.validation_cache[cache_key] = result_tuple
            return result_tuple
    
    def check_external_tool(self, tool_name: str, command: str, min_version: Optional[str] = None) -> Tuple[bool, str]:
        """
        外部ツールの利用可能性とバージョンを確認します
        
        Args:
            tool_name: ツールの表示名
            command: バージョンを確認するコマンド
            min_version: 必須の最小バージョン（オプション）
            
        Returns:
            (成功: bool, メッセージ: str)のタプル
        """
        cache_key = f"tool_{tool_name}_{command}_{min_version}"
        if cache_key in self.validation_cache:
            return self.validation_cache[cache_key]
        
        try:
            # Split command into parts
            cmd_parts = command.split()
            
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=10,
                shell=(sys.platform == "win32")
            )
            
            if result.returncode != 0:
                result_tuple = (False, f"{tool_name} が見つからないか、コマンドが失敗しました")
                self.validation_cache[cache_key] = result_tuple
                return result_tuple
            
            # Extract version if min_version specified
            if min_version:
                version_output = result.stdout + result.stderr
                version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', version_output)
                
                if version_match:
                    current_version = version_match.group(1)
                    
                    if version.parse(current_version) < version.parse(min_version):
                        result_tuple = (False, f"{tool_name} {min_version}+ が必要、見つかったのは {current_version}")
                        self.validation_cache[cache_key] = result_tuple
                        return result_tuple
                    
                    result_tuple = (True, f"{tool_name} {current_version} found")
                    self.validation_cache[cache_key] = result_tuple
                    return result_tuple
                else:
                    result_tuple = (True, f"{tool_name} が見つかりました (バージョン不明)")
                    self.validation_cache[cache_key] = result_tuple
                    return result_tuple
            else:
                result_tuple = (True, f"{tool_name} found")
                self.validation_cache[cache_key] = result_tuple
                return result_tuple
                
        except subprocess.TimeoutExpired:
            result_tuple = (False, f"{tool_name} のチェックがタイムアウトしました")
            self.validation_cache[cache_key] = result_tuple
            return result_tuple
        except FileNotFoundError:
            result_tuple = (False, f"{tool_name} がPATHに見つかりません")
            self.validation_cache[cache_key] = result_tuple
            return result_tuple
        except Exception as e:
            result_tuple = (False, f"確認できませんでした {tool_name}: {e}")
            self.validation_cache[cache_key] = result_tuple
            return result_tuple
    
    def check_disk_space(self, path: Path, required_mb: int = 500) -> Tuple[bool, str]:
        """
        利用可能なディスク容量を確認します
        
        Args:
            path: 確認するパス（ファイルまたはディレクトリ）
            required_mb: 必要な空き容量（MB）
            
        Returns:
            (成功: bool, メッセージ: str)のタプル
        """
        cache_key = f"disk_{path}_{required_mb}"
        if cache_key in self.validation_cache:
            return self.validation_cache[cache_key]
        
        try:
            # Get parent directory if path is a file
            check_path = path.parent if path.is_file() else path
            
            # Get disk usage
            stat_result = shutil.disk_usage(check_path)
            free_mb = stat_result.free / (1024 * 1024)
            
            if free_mb < required_mb:
                result = (False, f"ディスク容量が不足しています: {free_mb:.1f}MBの空き, {required_mb}MBが必要")
            else:
                result = (True, f"十分なディスク容量: {free_mb:.1f}MB free")
            
            self.validation_cache[cache_key] = result
            return result
            
        except Exception as e:
            result = (False, f"ディスク容量を確認できませんでした: {e}")
            self.validation_cache[cache_key] = result
            return result
    
    def check_write_permissions(self, path: Path) -> Tuple[bool, str]:
        """
        パスの書き込み権限を確認します
        
        Args:
            path: 確認するパス
            
        Returns:
            (成功: bool, メッセージ: str)のタプル
        """
        cache_key = f"write_{path}"
        if cache_key in self.validation_cache:
            return self.validation_cache[cache_key]
        
        try:
            # Create parent directories if needed
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
            
            # Test write access
            test_file = path / ".write_test"
            test_file.touch()
            test_file.unlink()
            
            result = (True, f"書き込みアクセス権が確認されました: {path}")
            self.validation_cache[cache_key] = result
            return result
            
        except Exception as e:
            result = (False, f"書き込みアクセス権がありません: {path}: {e}")
            self.validation_cache[cache_key] = result
            return result
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        すべてのシステム要件を検証します
        
        Args:
            requirements: 要件設定の辞書
            
        Returns:
            (すべて合格: bool, エラーメッセージ: List[str])のタプル
        """
        errors = []
        
        # Check Python requirements
        if "python" in requirements:
            python_req = requirements["python"]
            success, message = self.check_python(
                python_req["min_version"],
                python_req.get("max_version")
            )
            if not success:
                errors.append(f"Python: {message}")
        
        # Check Node.js requirements
        if "node" in requirements:
            node_req = requirements["node"]
            success, message = self.check_node(
                node_req["min_version"],
                node_req.get("max_version")
            )
            if not success:
                errors.append(f"Node.js: {message}")
        
        # Check disk space
        if "disk_space_mb" in requirements:
            success, message = self.check_disk_space(
                Path.home(),
                requirements["disk_space_mb"]
            )
            if not success:
                errors.append(f"Disk space: {message}")
        
        # Check external tools
        if "external_tools" in requirements:
            for tool_name, tool_req in requirements["external_tools"].items():
                # Skip optional tools that fail
                is_optional = tool_req.get("optional", False)
                
                success, message = self.check_external_tool(
                    tool_name,
                    tool_req["command"],
                    tool_req.get("min_version")
                )
                
                if not success and not is_optional:
                    errors.append(f"{tool_name}: {message}")
        
        return len(errors) == 0, errors
    
    def validate_component_requirements(self, component_names: List[str], all_requirements: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        特定のコンポーネントの要件を検証します
        
        Args:
            component_names: 検証するコンポーネント名のリスト
            all_requirements: 完全な要件設定
            
        Returns:
            (すべて合格: bool, エラーメッセージ: List[str])のタプル
        """
        errors = []
        
        # Start with base requirements
        base_requirements = {
            "python": all_requirements.get("python", {}),
            "disk_space_mb": all_requirements.get("disk_space_mb", 500)
        }
        
        # Add conditional requirements based on components
        external_tools = {}
        
        # Check if any component needs Node.js
        node_components = []
        for component in component_names:
            # This would be enhanced with actual component metadata
            if component in ["mcp"]:  # MCP component needs Node.js
                node_components.append(component)
        
        if node_components and "node" in all_requirements:
            base_requirements["node"] = all_requirements["node"]
        
        # Add external tools needed by components
        if "external_tools" in all_requirements:
            for tool_name, tool_req in all_requirements["external_tools"].items():
                required_for = tool_req.get("required_for", [])
                
                # Check if any of our components need this tool
                if any(comp in required_for for comp in component_names):
                    external_tools[tool_name] = tool_req
        
        if external_tools:
            base_requirements["external_tools"] = external_tools
        
        # Validate consolidated requirements
        return self.validate_requirements(base_requirements)
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        包括的なシステム情報を取得します
        
        Returns:
            システム情報を含む辞書
        """
        info = {
            "platform": sys.platform,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "python_executable": sys.executable
        }
        
        # Add Node.js info if available
        node_success, node_msg = self.check_node()
        info["node_available"] = node_success
        if node_success:
            info["node_message"] = node_msg
        
        # Add Claude CLI info if available
        claude_success, claude_msg = self.check_claude_cli()
        info["claude_cli_available"] = claude_success
        if claude_success:
            info["claude_cli_message"] = claude_msg
        
        # Add disk space info
        try:
            home_path = Path.home()
            stat_result = shutil.disk_usage(home_path)
            info["disk_space"] = {
                "total_gb": stat_result.total / (1024**3),
                "free_gb": stat_result.free / (1024**3),
                "used_gb": (stat_result.total - stat_result.free) / (1024**3)
            }
        except Exception:
            info["disk_space"] = {"error": "ディスク容量を特定できませんでした"}
        
        return info
    
    def get_platform(self) -> str:
        """
        インストールコマンド用の現在のプラットフォームを取得します
        
        Returns:
            プラットフォーム文字列 (linux, darwin, win32)
        """
        return sys.platform
    
    def load_installation_commands(self) -> Dict[str, Any]:
        """
        要件設定からインストールコマンドを読み込みます
        
        Returns:
            インストールコマンドの辞書
        """
        try:
            from ..services.config import ConfigService
            from .. import DATA_DIR
            
            config_manager = ConfigService(DATA_DIR)
            requirements = config_manager.load_requirements()
            return requirements.get("installation_commands", {})
        except Exception:
            return {}
    
    def get_installation_help(self, tool_name: str, platform: Optional[str] = None) -> str:
        """
        特定のツールのインストールヘルプを取得します
        
        Args:
            tool_name: ヘルプを取得するツールの名前
            platform: ターゲットプラットフォーム（Noneの場合は自動検出）
            
        Returns:
            インストールヘルプ文字列
        """
        if platform is None:
            platform = self.get_platform()
        
        commands = self.load_installation_commands()
        tool_commands = commands.get(tool_name, {})
        
        if not tool_commands:
            return f"利用可能なインストール手順はありません: {tool_name}"
        
        # Get platform-specific command or fallback to 'all'
        install_cmd = tool_commands.get(platform, tool_commands.get("all", ""))
        description = tool_commands.get("description", "")
        
        if install_cmd:
            help_text = f"\n💡 Installation Help for {tool_name}:\n"
            if description:
                help_text += f"   {description}\n"
            help_text += f"   コマンド: {install_cmd}\n"
            return help_text
        
        return f"利用可能なインストール手順はありません: {tool_name} on {platform}"
    
    def diagnose_system(self) -> Dict[str, Any]:
        """
        包括的なシステム診断を実行します
        
        Returns:
            診断情報の辞書
        """
        diagnostics = {
            "platform": self.get_platform(),
            "checks": {},
            "issues": [],
            "recommendations": []
        }
        
        # Check Python
        python_success, python_msg = self.check_python()
        diagnostics["checks"]["python"] = {
            "status": "pass" if python_success else "fail",
            "message": python_msg
        }
        if not python_success:
            diagnostics["issues"].append("Pythonバージョンの問題")
            diagnostics["recommendations"].append(self.get_installation_help("python"))
        
        # Check Node.js
        node_success, node_msg = self.check_node()
        diagnostics["checks"]["node"] = {
            "status": "pass" if node_success else "fail", 
            "message": node_msg
        }
        if not node_success:
            diagnostics["issues"].append("Node.js not found or version issue")
            diagnostics["recommendations"].append(self.get_installation_help("node"))
        
        # Check Claude CLI
        claude_success, claude_msg = self.check_claude_cli()
        diagnostics["checks"]["claude_cli"] = {
            "status": "pass" if claude_success else "fail",
            "message": claude_msg
        }
        if not claude_success:
            diagnostics["issues"].append("Claude CLIが見つかりません")
            diagnostics["recommendations"].append(self.get_installation_help("claude_cli"))
        
        # Check disk space
        disk_success, disk_msg = self.check_disk_space(Path.home())
        diagnostics["checks"]["disk_space"] = {
            "status": "pass" if disk_success else "fail",
            "message": disk_msg
        }
        if not disk_success:
            diagnostics["issues"].append("ディスク容量が不足しています")
        
        # Check common PATH issues
        self._diagnose_path_issues(diagnostics)
        
        return diagnostics
    
    def _diagnose_path_issues(self, diagnostics: Dict[str, Any]) -> None:
        """PATH関連の診断を追加"""
        path_issues = []
        
        # Check if tools are in PATH, with alternatives for some tools
        tool_checks = [
            # For Python, check if either python3 OR python is available
            (["python3", "python"], "Python (python3 または python)"),
            (["node"], "Node.js"),
            (["npm"], "npm"),
            (["claude"], "Claude CLI")
        ]
        
        for tool_alternatives, display_name in tool_checks:
            tool_found = False
            for tool in tool_alternatives:
                try:
                    result = subprocess.run(
                        ["which" if sys.platform != "win32" else "where", tool],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        shell=(sys.platform == "win32")
                    )
                    if result.returncode == 0:
                        tool_found = True
                        break
                except Exception:
                    continue
            
            if not tool_found:
                # Only report as missing if none of the alternatives were found
                if len(tool_alternatives) > 1:
                    path_issues.append(f"{display_name} がPATHに見つかりません")
                else:
                    path_issues.append(f"{tool_alternatives[0]} がPATHに見つかりません")
        
        if path_issues:
            diagnostics["issues"].extend(path_issues)
            diagnostics["recommendations"].append(
                "\n💡 PATH Issue Help:\n"
                "   Some tools may not be in your PATH. Try:\n"
                "   - Restart your terminal after installation\n"
                "   - Check your shell configuration (.bashrc, .zshrc)\n"
                "   - Use full paths to tools if needed\n"
            )
    
    def clear_cache(self) -> None:
        """検証キャッシュをクリア"""
        self.validation_cache.clear()
