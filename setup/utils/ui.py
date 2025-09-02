"""
SuperClaudeインストールシステム用のユーザーインターフェースユーティリティ
色と進捗表示を備えたクロスプラットフォームのコンソールUI
"""

import sys
import time
import shutil
import getpass
from typing import List, Optional, Any, Dict, Union
from enum import Enum

# Try to import colorama for cross-platform color support
try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback color codes for Unix-like systems
    class MockFore:
        RED = '\033[91m' if sys.platform != 'win32' else ''
        GREEN = '\033[92m' if sys.platform != 'win32' else ''
        YELLOW = '\033[93m' if sys.platform != 'win32' else ''
        BLUE = '\033[94m' if sys.platform != 'win32' else ''
        MAGENTA = '\033[95m' if sys.platform != 'win32' else ''
        CYAN = '\033[96m' if sys.platform != 'win32' else ''
        WHITE = '\033[97m' if sys.platform != 'win32' else ''
    
    class MockStyle:
        RESET_ALL = '\033[0m' if sys.platform != 'win32' else ''
        BRIGHT = '\033[1m' if sys.platform != 'win32' else ''
    
    Fore = MockFore()
    Style = MockStyle()


class Colors:
    """コンソール出力用の色定数"""
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BRIGHT = Style.BRIGHT


class ProgressBar:
    """カスタマイズ可能な表示を備えたクロスプラットフォームのプログレスバー"""
    
    def __init__(self, total: int, width: int = 50, prefix: str = '', suffix: str = ''):
        """
        プログレスバーを初期化します
        
        Args:
            total: 処理するアイテムの総数
            width: プログレスバーの幅（文字数）
            prefix: プログレスバーの前に表示するテキスト
            suffix: プログレスバーの後に表示するテキスト
        """
        self.total = total
        self.width = width
        self.prefix = prefix
        self.suffix = suffix
        self.current = 0
        self.start_time = time.time()
        
        # Get terminal width for responsive display
        try:
            self.terminal_width = shutil.get_terminal_size().columns
        except OSError:
            self.terminal_width = 80
    
    def update(self, current: int, message: str = '') -> None:
        """
        プログレスバーを更新します
        
        Args:
            current: 現在の進行状況の値
            message: 表示するオプションのメッセージ
        """
        self.current = current
        percent = min(100, (current / self.total) * 100) if self.total > 0 else 100
        
        # Calculate filled and empty portions
        filled_width = int(self.width * current / self.total) if self.total > 0 else self.width
        filled = '█' * filled_width
        empty = '░' * (self.width - filled_width)
        
        # Calculate elapsed time and ETA
        elapsed = time.time() - self.start_time
        if current > 0:
            eta = (elapsed / current) * (self.total - current)
            eta_str = f" ETA: {self._format_time(eta)}"
        else:
            eta_str = ""
        
        # Format progress line
        if message:
            status = f" {message}"
        else:
            status = ""
        
        progress_line = (
            f"\r{self.prefix}[{Colors.GREEN}{filled}{Colors.WHITE}{empty}{Colors.RESET}] "
            f"{percent:5.1f}%{status}{eta_str}"
        )
        
        # Truncate if too long for terminal
        max_length = self.terminal_width - 5
        if len(progress_line) > max_length:
            # Remove color codes for length calculation
            plain_line = progress_line.replace(Colors.GREEN, '').replace(Colors.WHITE, '').replace(Colors.RESET, '')
            if len(plain_line) > max_length:
                progress_line = progress_line[:max_length] + "..."
        
        print(progress_line, end='', flush=True)
    
    def increment(self, message: str = '') -> None:
        """
        進行状況を1つインクリメントします
        
        Args:
            message: 表示するオプションのメッセージ
        """
        self.update(self.current + 1, message)
    
    def finish(self, message: str = 'Complete') -> None:
        """
        プログレスバーを完了します
        
        Args:
            message: 完了メッセージ
        """
        self.update(self.total, message)
        print()  # New line after completion
    
    def _format_time(self, seconds: float) -> str:
        """時間の長さを人間が読める文字列としてフォーマット"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            return f"{seconds/60:.0f}m {seconds%60:.0f}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours:.0f}h {minutes:.0f}m"


class Menu:
    """キーボードナビゲーション付きの対話型メニューシステム"""
    
    def __init__(self, title: str, options: List[str], multi_select: bool = False):
        """
        メニューを初期化します
        
        Args:
            title: メニューのタイトル
            options: メニューオプションのリスト
            multi_select: 複数選択を許可
        """
        self.title = title
        self.options = options
        self.multi_select = multi_select
        self.selected = set() if multi_select else None
        
    def display(self) -> Union[int, List[int]]:
        """
        メニューを表示してユーザーの選択を取得します
        
        Returns:
            選択されたオプションのインデックス（単一）またはインデックスのリスト（複数選択）
        """
        print(f"\n{Colors.CYAN}{Colors.BRIGHT}{self.title}{Colors.RESET}")
        print("=" * len(self.title))
        
        for i, option in enumerate(self.options, 1):
            if self.multi_select:
                marker = "[x]" if i-1 in (self.selected or set()) else "[ ]"
                print(f"{Colors.YELLOW}{i:2d}.{Colors.RESET} {marker} {option}")
            else:
                print(f"{Colors.YELLOW}{i:2d}.{Colors.RESET} {option}")
        
        if self.multi_select:
            print(f"\n{Colors.BLUE}カンマで区切られた数字（例: 1,3,5）またはすべてのオプションに対して'all'を入力してください:{Colors.RESET}")
        else:
            print(f"\n{Colors.BLUE}選択を入力してください (1-{len(self.options)}):{Colors.RESET}")
        
        while True:
            try:
                user_input = input("> ").strip().lower()
                
                if self.multi_select:
                    if user_input == 'all':
                        return list(range(len(self.options)))
                    elif user_input == '':
                        return []
                    else:
                        # Parse comma-separated numbers
                        selections = []
                        for part in user_input.split(','):
                            part = part.strip()
                            if part.isdigit():
                                idx = int(part) - 1
                                if 0 <= idx < len(self.options):
                                    selections.append(idx)
                                else:
                                    raise ValueError(f"無効なオプション: {part}")
                            else:
                                raise ValueError(f"無効な入力: {part}")
                        return list(set(selections))  # Remove duplicates
                else:
                    if user_input.isdigit():
                        choice = int(user_input) - 1
                        if 0 <= choice < len(self.options):
                            return choice
                        else:
                            print(f"{Colors.RED}無効な選択です。1から...の間の数字を入力してください {len(self.options)}.{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}有効な数値を入力してください。{Colors.RESET}")
                        
            except (ValueError, KeyboardInterrupt) as e:
                if isinstance(e, KeyboardInterrupt):
                    print(f"\n{Colors.YELLOW}操作がキャンセルされました。{Colors.RESET}")
                    return [] if self.multi_select else -1
                else:
                    print(f"{Colors.RED}無効な入力: {e}{Colors.RESET}")


def confirm(message: str, default: bool = True) -> bool:
    """
    ユーザーに確認を求めます
    
    Args:
        message: 確認メッセージ
        default: ユーザーがEnterキーのみを押した場合のデフォルトの応答
        
    Returns:
        確認された場合はTrue、それ以外はFalse
    """
    suffix = "[Y/n]" if default else "[y/N]"
    print(f"{Colors.BLUE}{message} {suffix}{Colors.RESET}")
    
    while True:
        try:
            response = input("> ").strip().lower()
            
            if response == '':
                return default
            elif response in ['y', 'yes', 'true', '1']:
                return True
            elif response in ['n', 'no', 'false', '0']:
                return False
            else:
                print(f"{Colors.RED}'y'または'n'を入力してください（またはデフォルトの場合はEnterキーを押してください）。{Colors.RESET}")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}操作がキャンセルされました。{Colors.RESET}")
            return False


def display_header(title: str, subtitle: str = '') -> None:
    """
    フォーマットされたヘッダーを表示します
    
    Args:
            title: メインタイトル
            subtitle: オプションのサブタイトル
    """
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BRIGHT}{title:^60}{Colors.RESET}")
    if subtitle:
        print(f"{Colors.WHITE}{subtitle:^60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BRIGHT}{'='*60}{Colors.RESET}\n")


def display_info(message: str) -> None:
    """情報メッセージを表示"""
    print(f"{Colors.BLUE}[INFO] {message}{Colors.RESET}")


def display_success(message: str) -> None:
    """成功メッセージを表示"""
    print(f"{Colors.GREEN}[✓] {message}{Colors.RESET}")


def display_warning(message: str) -> None:
    """警告メッセージを表示"""
    print(f"{Colors.YELLOW}[!] {message}{Colors.RESET}")


def display_error(message: str) -> None:
    """エラーメッセージを表示"""
    print(f"{Colors.RED}[✗] {message}{Colors.RESET}")


def display_step(step: int, total: int, message: str) -> None:
    """ステップの進捗を表示"""
    print(f"{Colors.CYAN}[{step}/{total}] {message}{Colors.RESET}")


def display_table(headers: List[str], rows: List[List[str]], title: str = '') -> None:
    """
    データをテーブル形式で表示します
    
    Args:
        headers: 列ヘッダー
        rows: データ行
        title: オプションのテーブルタイトル
    """
    if not rows:
        return
    
    # Calculate column widths
    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Display title
    if title:
        print(f"\n{Colors.CYAN}{Colors.BRIGHT}{title}{Colors.RESET}")
        print()
    
    # Display headers
    header_line = " | ".join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))
    print(f"{Colors.YELLOW}{header_line}{Colors.RESET}")
    print("-" * len(header_line))
    
    # Display rows
    for row in rows:
        row_line = " | ".join(f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row))
        print(row_line)
    
    print()


def prompt_api_key(service_name: str, env_var_name: str) -> Optional[str]:
    """
    セキュリティとUXのベストプラクティスを用いてAPIキーの入力を促します
    
    Args:
        service_name: 人間が読めるサービス名 (例: "Magic", "Morphllm")
        env_var_name: 環境変数名 (例: "TWENTYFIRST_API_KEY")
        
    Returns:
        提供された場合はAPIキー文字列、スキップされた場合はNone
    """
    print(f"{Colors.BLUE}[API KEY] {service_name} が必要です: {Colors.BRIGHT}{env_var_name}{Colors.RESET}")
    print(f"{Colors.WHITE}APIキーを取得するには、サービスのドキュメントにアクセスしてください{Colors.RESET}")
    print(f"{Colors.YELLOW}スキップするにはEnterキーを押してください（後で手動で設定できます）{Colors.RESET}")
    
    try:
        # Use getpass for hidden input
        api_key = getpass.getpass(f"入力 {env_var_name}: ").strip()
        
        if not api_key:
            print(f"{Colors.YELLOW}[SKIPPED] {env_var_name} - 後で手動で設定{Colors.RESET}")
            return None
        
        # Basic validation (non-empty, reasonable length)
        if len(api_key) < 10:
            print(f"{Colors.RED}[WARNING] API key seems too short. Continue anyway? (y/N){Colors.RESET}")
            if not confirm("", default=False):
                return None
        
        print(f"{Colors.GREEN}[✓] {env_var_name} 設定済み{Colors.RESET}")
        return api_key
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[SKIPPED] {env_var_name}{Colors.RESET}")
        return None


def wait_for_key(message: str = "続行するにはEnterキーを押してください...") -> None:
    """ユーザーがキーを押すのを待つ"""
    try:
        input(f"{Colors.BLUE}{message}{Colors.RESET}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}操作がキャンセルされました。{Colors.RESET}")


def clear_screen() -> None:
    """ターミナル画面をクリア"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


class StatusSpinner:
    """長時間の操作用のシンプルなステータスピナー"""
    
    def __init__(self, message: str = "Working..."):
        """
        スピナーを初期化します
        
        Args:
            message: スピナーと共に表示するメッセージ
        """
        self.message = message
        self.spinning = False
        self.chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        self.current = 0
    
    def start(self) -> None:
        """バックグラウンドスレッドでスピナーを開始"""
        import threading
        
        def spin():
            while self.spinning:
                char = self.chars[self.current % len(self.chars)]
                print(f"\r{Colors.BLUE}{char} {self.message}{Colors.RESET}", end='', flush=True)
                self.current += 1
                time.sleep(0.1)
        
        self.spinning = True
        self.thread = threading.Thread(target=spin, daemon=True)
        self.thread.start()
    
    def stop(self, final_message: str = '') -> None:
        """
        スピナーを停止します
        
        Args:
            final_message: 最後に表示するメッセージ
        """
        self.spinning = False
        if hasattr(self, 'thread'):
            self.thread.join(timeout=0.2)
        
        # Clear spinner line
        print(f"\r{' ' * (len(self.message) + 5)}\r", end='')
        
        if final_message:
            print(final_message)


def format_size(size_bytes: int) -> str:
    """ファイルサイズを人間が読める形式にフォーマット"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_duration(seconds: float) -> str:
    """期間を人間が読める形式にフォーマット"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:.0f}m {secs:.0f}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:.0f}h {minutes:.0f}m"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """オプションの接尾辞付きでテキストを最大長に切り詰める"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
