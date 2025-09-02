"""
SuperClaude CLI ベースモジュール

すべてのCLI操作に共通機能を提供する基底クラス
"""

from pathlib import Path

# Read version from VERSION file
try:
    __version__ = (Path(__file__).parent.parent.parent / "VERSION").read_text().strip()
except Exception:
    __version__ = "4.0.8"  # Fallback


def get_command_info():
    """利用可能なコマンドに関する情報を取得します"""
    return {
        "install": {
            "name": "install",
            "description": "SuperClaudeフレームワークコンポーネントをインストールします",
            "module": "setup.cli.commands.install"
        },
        "update": {
            "name": "update", 
            "description": "既存のSuperClaudeインストールを更新します",
            "module": "setup.cli.commands.update"
        },
        "uninstall": {
            "name": "uninstall",
            "description": "SuperClaudeフレームワークのインストールを削除します",
            "module": "setup.cli.commands.uninstall"
        },
        "backup": {
            "name": "backup",
            "description": "SuperClaudeのインストールをバックアップおよび復元します",
            "module": "setup.cli.commands.backup"
        }
    }


class OperationBase:
    """すべての操作に共通機能を提供する基底クラス"""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.logger = None
    
    def setup_operation_logging(self, args):
        """操作固有のロギングを設定します"""
        from ..utils.logger import get_logger
        self.logger = get_logger()
        self.logger.info(f"開始中 {self.operation_name} operation")
    
    def validate_global_args(self, args):
        """すべての操作に共通のグローバル引数を検証します"""
        errors = []
        
        # Validate install directory
        if hasattr(args, 'install_dir') and args.install_dir:
            from ..utils.security import SecurityValidator
            is_safe, validation_errors = SecurityValidator.validate_installation_target(args.install_dir)
            if not is_safe:
                errors.extend(validation_errors)
        
        # Check for conflicting flags
        if hasattr(args, 'verbose') and hasattr(args, 'quiet'):
            if args.verbose and args.quiet:
                errors.append("--verboseと--quietは同時に指定できません")
        
        return len(errors) == 0, errors
    
    def handle_operation_error(self, 操作: str, error: Exception):
        """操作の標準エラー処理"""
        if self.logger:
            self.logger.exception(f"エラー: {operation} 操作: {error}")
        else:
            print(f"エラー: {operation} 操作: {error}")
        return 1