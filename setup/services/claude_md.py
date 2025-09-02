"""
フレームワークのインポートを管理しながらユーザーのカスタマイズを保持するためのCLAUDE.mdマネージャー
"""

import re
from pathlib import Path
from typing import List, Set, Dict, Optional
from ..utils.logger import get_logger


class CLAUDEMdService:
    """ユーザーのカスタマイズを保持しながらCLAUDE.mdファイルの更新を管理します"""
    
    def __init__(self, install_dir: Path):
        """
        Initialize CLAUDEMdService
        
        Args:
            install_dir: Installation directory (typically ~/.claude)
        """
        self.install_dir = install_dir
        self.claude_md_path = install_dir / "CLAUDE.md"
        self.logger = get_logger()
    
    def read_existing_imports(self) -> Set[str]:
        """
        既存の@import文をCLAUDE.mdから解析します
        
        Returns:
            既にインポートされているファイル名のセット（@なし）
        """
        existing_imports = set()
        
        if not self.claude_md_path.exists():
            return existing_imports
        
        try:
            with open(self.claude_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all @import statements using regex
            import_pattern = r'^@([^\s\n]+\.md)\s*$'
            matches = re.findall(import_pattern, content, re.MULTILINE)
            existing_imports.update(matches)
            
            self.logger.debug(f"既存のインポートが見つかりました: {existing_imports}")
            
        except Exception as e:
            self.logger.warning(f"既存のCLAUDE.mdのインポートを読み込めませんでした: {e}")
        
        return existing_imports
    
    def read_existing_content(self) -> str:
        """
        既存のCLAUDE.mdのコンテンツを読み込みます
        
        Returns:
            既存のコンテンツ、またはファイルが存在しない場合は空文字列
        """
        if not self.claude_md_path.exists():
            return ""
        
        try:
            with open(self.claude_md_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.warning(f"既存のCLAUDE.mdを読み込めませんでした: {e}")
            return ""
    
    def extract_user_content(self, content: str) -> str:
        """
        ユーザーコンテンツ（フレームワークのインポートセクションより前のすべて）を抽出します
        
        Args:
            content: 完全なCLAUDE.mdのコンテンツ
            
        Returns:
            フレームワークのインポートを含まないユーザーコンテンツ
        """
        # Look for framework imports section marker
        framework_marker = "# ═══════════════════════════════════════════════════\n# SuperClaude Framework Components"
        
        if framework_marker in content:
            user_content = content.split(framework_marker)[0].rstrip()
        else:
            # If no framework section exists, preserve all content
            user_content = content.rstrip()
        
        return user_content
    
    def organize_imports_by_category(self, files_by_category: Dict[str, List[str]]) -> str:
        """
        インポートをカテゴリ別のセクションに整理します
        
        Args:
            files_by_category: カテゴリ名とファイルリストをマッピングする辞書
            
        Returns:
            フォーマットされたインポートセクション
        """
        if not files_by_category:
            return ""
        
        sections = []
        
        # Framework imports section header
        sections.append("# ═══════════════════════════════════════════════════")
        sections.append("# SuperClaude フレームワークコンポーネント")
        sections.append("# ═══════════════════════════════════════════════════")
        sections.append("")
        
        # Add each category
        for category, files in files_by_category.items():
            if files:
                sections.append(f"# {category}")
                for file in sorted(files):
                    sections.append(f"@{file}")
                sections.append("")
        
        return "\n".join(sections)
    
    def add_imports(self, files: List[str], category: str = "Framework") -> bool:
        """
        重複チェックとユーザーコンテンツの保持を行いながら新しいインポートを追加します
        
        Args:
            files: インポートするファイル名のリスト
            category: インポートを整理するためのカテゴリ名
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        try:
            # Ensure CLAUDE.md exists
            self.ensure_claude_md_exists()
            
            # Read existing content and imports
            existing_content = self.read_existing_content()
            existing_imports = self.read_existing_imports()
            
            # Filter out files already imported
            new_files = [f for f in files if f not in existing_imports]
            
            if not new_files:
                self.logger.info("すべてのファイルは既にインポートされているため、変更は不要です")
                return True
            
            self.logger.info(f"追加中 {len(new_files)} 個の新しいインポートをカテゴリ '{category}': {new_files}")
            
            # Extract user content (preserve everything before framework section)
            user_content = self.extract_user_content(existing_content)
            
            # Parse existing framework imports by category
            existing_framework_imports = self._parse_existing_framework_imports(existing_content)
            
            # Add new files to the specified category
            if category not in existing_framework_imports:
                existing_framework_imports[category] = []
            existing_framework_imports[category].extend(new_files)
            
            # Build new content
            new_content_parts = []
            
            # Add user content
            if user_content.strip():
                new_content_parts.append(user_content)
                new_content_parts.append("")  # Add blank line before framework section
            
            # Add organized framework imports
            framework_section = self.organize_imports_by_category(existing_framework_imports)
            if framework_section:
                new_content_parts.append(framework_section)
            
            # Write updated content
            new_content = "\n".join(new_content_parts)
            
            with open(self.claude_md_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.success(f"CLAUDE.mdを更新しました: {len(new_files)} new imports")
            return True
            
        except Exception as e:
            self.logger.error(f"CLAUDE.mdの更新に失敗しました: {e}")
            return False
    
    def _parse_existing_framework_imports(self, content: str) -> Dict[str, List[str]]:
        """
        カテゴリ別に整理された既存のフレームワークインポートを解析します
        
        Args:
            content: 完全なCLAUDE.mdのコンテンツ
            
        Returns:
            カテゴリ名とインポートされたファイルリストをマッピングする辞書
        """
        imports_by_category = {}
        
        # Look for framework imports section
        framework_marker = "# ═══════════════════════════════════════════════════\n# SuperClaude Framework Components"
        
        if framework_marker not in content:
            return imports_by_category
        
        # Extract framework section
        framework_section = content.split(framework_marker)[1] if framework_marker in content else ""
        
        # Parse categories and imports
        lines = framework_section.split('\n')
        current_category = None
        
        for line in lines:
            line = line.strip()
            
            # Skip section header lines and empty lines
            if line.startswith('# ═══') or not line:
                continue
            
            # Category header (starts with # but not the section divider)
            if line.startswith('# ') and not line.startswith('# ═══'):
                current_category = line[2:].strip()  # Remove "# "
                if current_category not in imports_by_category:
                    imports_by_category[current_category] = []
            
            # Import line (starts with @)
            elif line.startswith('@') and current_category:
                import_file = line[1:].strip()  # Remove "@"
                if import_file not in imports_by_category[current_category]:
                    imports_by_category[current_category].append(import_file)
        
        return imports_by_category
    
    def ensure_claude_md_exists(self) -> None:
        """
        CLAUDE.mdが存在しない場合、デフォルトのコンテンツで作成します
        """
        if self.claude_md_path.exists():
            return
        
        try:
            # Create directory if it doesn't exist
            self.claude_md_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Default CLAUDE.md content
            default_content = """# SuperClaude エントリポイント

このファイルはSuperClaudeフレームワークのエントリポイントとして機能します。
ここに独自のカスタム指示や設定を追加できます。

SuperClaudeフレームワークコンポーネントは以下に自動的にインポートされます。
"""
            
            with open(self.claude_md_path, 'w', encoding='utf-8') as f:
                f.write(default_content)
            
            self.logger.info("デフォルトのコンテンツでCLAUDE.mdを作成しました")
            
        except Exception as e:
            self.logger.error(f"CLAUDE.mdの作成に失敗しました: {e}")
            raise
    
    def remove_imports(self, files: List[str]) -> bool:
        """
        CLAUDE.mdから特定のインポートを削除します
        
        Args:
            files: インポートから削除するファイル名のリスト
            
        Returns:
            成功した場合はTrue、それ以外はFalse
        """
        try:
            if not self.claude_md_path.exists():
                return True  # Nothing to remove
            
            existing_content = self.read_existing_content()
            user_content = self.extract_user_content(existing_content)
            existing_framework_imports = self._parse_existing_framework_imports(existing_content)
            
            # Remove files from all categories
            removed_any = False
            for category, category_files in existing_framework_imports.items():
                for file in files:
                    if file in category_files:
                        category_files.remove(file)
                        removed_any = True
            
            # Remove empty categories
            existing_framework_imports = {k: v for k, v in existing_framework_imports.items() if v}
            
            if not removed_any:
                return True  # Nothing was removed
            
            # Rebuild content
            new_content_parts = []
            
            if user_content.strip():
                new_content_parts.append(user_content)
                new_content_parts.append("")
            
            framework_section = self.organize_imports_by_category(existing_framework_imports)
            if framework_section:
                new_content_parts.append(framework_section)
            
            # Write updated content
            new_content = "\n".join(new_content_parts)
            
            with open(self.claude_md_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"削除済み {len(files)} 個のインポートをCLAUDE.mdから")
            return True
            
        except Exception as e:
            self.logger.error(f"CLAUDE.mdからのインポートの削除に失敗しました: {e}")
            return False