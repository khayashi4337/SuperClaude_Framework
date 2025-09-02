"""
SuperClaudeフレームワークの自動更新チェッカー
PyPIで新しいバージョンをチェックし、自動更新を提供します
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Optional, Tuple
from packaging import version
import urllib.request
import urllib.error
from datetime import datetime, timedelta

from .ui import display_info, display_warning, display_success, Colors
from .logger import get_logger


class UpdateChecker:
    """SuperClaudeの自動更新チェックを処理します"""
    
    PYPI_URL = "https://pypi.org/pypi/SuperClaude/json"
    CACHE_FILE = Path.home() / ".claude" / ".update_check"
    CHECK_INTERVAL = 86400  # 24 hours in seconds
    TIMEOUT = 2  # seconds
    
    def __init__(self, current_version: str):
        """
        更新チェッカーを初期化します
        
        Args:
            current_version: 現在インストールされているバージョン
        """
        self.current_version = current_version
        self.logger = get_logger()
        
    def should_check_update(self, force: bool = False) -> bool:
        """
        最終チェック時間に基づいて更新を確認すべきかどうかを判断します
        
        Args:
            force: 最終チェック時間に関係なくチェックを強制
            
        Returns:
            更新チェックを実行すべき場合はTrue
        """
        if force:
            return True
            
        if not self.CACHE_FILE.exists():
            return True
            
        try:
            with open(self.CACHE_FILE, 'r') as f:
                data = json.load(f)
                last_check = data.get('last_check', 0)
                
            # Check if 24 hours have passed
            if time.time() - last_check > self.CHECK_INTERVAL:
                return True
                
        except (json.JSONDecodeError, KeyError):
            return True
            
        return False
        
    def save_check_timestamp(self):
        """現在のタイムスタンプを最終チェック時間として保存"""
        self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        data = {}
        if self.CACHE_FILE.exists():
            try:
                with open(self.CACHE_FILE, 'r') as f:
                    data = json.load(f)
            except:
                pass
                
        data['last_check'] = time.time()
        
        with open(self.CACHE_FILE, 'w') as f:
            json.dump(data, f)
            
    def get_latest_version(self) -> Optional[str]:
        """
        PyPIにSuperClaudeの最新バージョンを問い合わせます
        
        Returns:
            最新のバージョン文字列、またはチェックが失敗した場合はNone
        """
        try:
            # Create request with timeout
            req = urllib.request.Request(
                self.PYPI_URL,
                headers={'User-Agent': 'SuperClaude-Updater'}
            )
            
            # Set timeout for the request
            with urllib.request.urlopen(req, timeout=self.TIMEOUT) as response:
                data = json.loads(response.read().decode())
                latest = data.get('info', {}).get('version')
                
            if self.logger:
                self.logger.debug(f"最新のPyPIバージョン: {latest}")
                
            return latest
            
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            if self.logger:
                self.logger.debug(f"PyPIのチェックに失敗しました: {e}")
            return None
        except Exception as e:
            if self.logger:
                self.logger.debug(f"更新の確認中に予期しないエラーが発生しました: {e}")
            return None
            
    def compare_versions(self, latest: str) -> bool:
        """
        現在のバージョンと最新バージョンを比較します
        
        Args:
            latest: 最新のバージョン文字列
            
        Returns:
            更新が利用可能な場合はTrue
        """
        try:
            return version.parse(latest) > version.parse(self.current_version)
        except Exception:
            return False
            
    def detect_installation_method(self) -> str:
        """
        SuperClaudeがどのようにインストールされたか（pip, pipxなど）を検出します
        
        Returns:
            インストール方法の文字列
        """
        # Check pipx first
        try:
            result = subprocess.run(
                ['pipx', 'list'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if 'SuperClaude' in result.stdout or 'superclaude' in result.stdout:
                return 'pipx'
        except:
            pass
            
        # Check if pip installation exists
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'show', 'SuperClaude'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                # Check if it's a user installation
                if '--user' in result.stdout or Path.home() in Path(result.stdout):
                    return 'pip-user'
                return 'pip'
        except:
            pass
            
        return 'unknown'
        
    def get_update_command(self) -> str:
        """
        インストール方法に基づいて適切な更新コマンドを取得します
        
        Returns:
            更新コマンド文字列
        """
        method = self.detect_installation_method()
        
        commands = {
            'pipx': 'pipx upgrade SuperClaude',
            'pip-user': 'pip install --upgrade --user SuperClaude',
            'pip': 'pip install --upgrade SuperClaude',
            'unknown': 'pip install --upgrade SuperClaude'
        }
        
        return commands.get(method, commands['unknown'])
        
    def show_update_banner(self, latest: str, auto_update: bool = False) -> bool:
        """
        利用可能な更新のバナーを表示します
        
        Args:
            latest: 利用可能な最新バージョン
            auto_update: プロンプトなしで自動更新するかどうか
            
        Returns:
            ユーザーが更新を希望する場合はTrue
        """
        update_cmd = self.get_update_command()
        
        # Display banner
        print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.YELLOW}  🚀 更新が利用可能です: {self.current_version} → {latest}        {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.GREEN}  実行: {update_cmd:<30} {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        if auto_update:
            return True
            
        # Check if running in non-interactive mode
        if not sys.stdin.isatty():
            return False
            
        # Prompt user
        try:
            response = input(f"{Colors.YELLOW}Would you like to update now? (y/N): {Colors.RESET}").strip().lower()
            return response in ['y', 'yes']
        except (EOFError, KeyboardInterrupt):
            return False
            
    def perform_update(self) -> bool:
        """
        更新コマンドを実行します
        
        Returns:
            更新が成功した場合はTrue
        """
        update_cmd = self.get_update_command()
        
        print(f"{Colors.CYAN}🔄 SuperClaudeを更新中...{Colors.RESET}")
        
        try:
            result = subprocess.run(
                update_cmd.split(),
                capture_output=False,
                text=True
            )
            
            if result.returncode == 0:
                display_success("更新が正常に完了しました！")
                print(f"{Colors.YELLOW}新しいバージョンを使用するには、SuperClaudeを再起動してください。{Colors.RESET}")
                return True
            else:
                display_warning("更新に失敗しました。手動で実行してください:")
                print(f"  {update_cmd}")
                return False
                
        except Exception as e:
            display_warning(f"自動更新できませんでした: {e}")
            print(f"手動で実行してください: {update_cmd}")
            return False
            
    def check_and_notify(self, force: bool = False, auto_update: bool = False) -> bool:
        """
        更新を確認してユーザーに通知するメインメソッド
        
        Args:
            force: 最終チェック時間に関係なくチェックを強制
            auto_update: 利用可能な場合は自動的に更新
            
        Returns:
            更新が実行された場合はTrue
        """
        # Check if we should skip based on environment variable
        if os.getenv('SUPERCLAUDE_NO_UPDATE_CHECK', '').lower() in ['true', '1', 'yes']:
            return False
            
        # Check if auto-update is enabled via environment
        if os.getenv('SUPERCLAUDE_AUTO_UPDATE', '').lower() in ['true', '1', 'yes']:
            auto_update = True
            
        # Check if enough time has passed
        if not self.should_check_update(force):
            return False
            
        # Get latest version
        latest = self.get_latest_version()
        if not latest:
            return False
            
        # Save timestamp
        self.save_check_timestamp()
        
        # Compare versions
        if not self.compare_versions(latest):
            return False
            
        # Show banner and potentially update
        if self.show_update_banner(latest, auto_update):
            return self.perform_update()
            
        return False


def check_for_updates(current_version: str = None, **kwargs) -> bool:
    """
    更新を確認するための便利な関数
    
    Args:
        current_version: 現在インストールされているバージョン（デフォルトはsetupから読み取り）
        **kwargs: check_and_notifyに渡される追加の引数
        
    Returns:
            更新が実行された場合はTrue
    """
    if current_version is None:
        from setup import __version__
        current_version = __version__
    checker = UpdateChecker(current_version)
    return checker.check_and_notify(**kwargs)