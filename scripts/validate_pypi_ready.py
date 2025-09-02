#!/usr/bin/env python3
"""
PyPI準備完了検証スクリプト
SuperClaudeプロジェクトがPyPI公開の準備ができているか確認します
"""

import sys
import toml
from pathlib import Path
from typing import List, Tuple

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

def check_file_exists(file_path: Path, description: str) -> bool:
    """必要なファイルが存在するか確認"""
    if file_path.exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ 不足: {description}: {file_path}")
        return False

def check_version_consistency() -> bool:
    """ファイル間でバージョンが一貫しているか確認"""
    print("\n🔍 Checking version consistency...")
    
    versions = {}
    
    # Check pyproject.toml
    try:
        pyproject_path = PROJECT_ROOT / "pyproject.toml"
        with open(pyproject_path, 'r') as f:
            pyproject = toml.load(f)
        versions['pyproject.toml'] = pyproject['project']['version']
        print(f"📋 pyproject.tomlバージョン: {versions['pyproject.toml']}")
    except Exception as e:
        print(f"❌ pyproject.tomlの読み取りエラー: {e}")
        return False
    
    # Check SuperClaude/__init__.py
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from SuperClaude import __version__
        versions['SuperClaude/__init__.py'] = __version__
        print(f"📦 パッケージバージョン: {versions['SuperClaude/__init__.py']}")
    except Exception as e:
        print(f"❌ SuperClaudeバージョンのインポートエラー: {e}")
        return False
    
    # Check setup/__init__.py
    try:
        from setup import __version__ as setup_version
        versions['setup/__init__.py'] = setup_version
        print(f"🔧 セットアップバージョン: {versions['setup/__init__.py']}")
    except Exception as e:
        print(f"❌ セットアップバージョンのインポートエラー: {e}")
        return False
    
    # Check consistency
    all_versions = list(versions.values())
    if len(set(all_versions)) == 1:
        print(f"✅ すべてのバージョンが一貫しています: {all_versions[0]}")
        return True
    else:
        print(f"❌ バージョンの不一致: {versions}")
        return False

def check_package_structure() -> bool:
    """パッケージ構造が正しいか確認"""
    print("\n🏗️ Checking package structure...")
    
    required_structure = [
        ("SuperClaude/__init__.py", "Main package __init__.py"),
        ("SuperClaude/__main__.py", "メインエントリポイント"),
        ("SuperClaude/Core/__init__.py", "Core module __init__.py"),
        ("SuperClaude/Commands/__init__.py", "Commands module __init__.py"),
        ("SuperClaude/Agents/__init__.py", "Agents module __init__.py"),
        ("SuperClaude/Modes/__init__.py", "Modes module __init__.py"),
        ("SuperClaude/MCP/__init__.py", "MCP module __init__.py"),
        ("setup/__init__.py", "Setup package __init__.py"),
    ]
    
    all_good = True
    for file_path, description in required_structure:
        full_path = PROJECT_ROOT / file_path
        if not check_file_exists(full_path, description):
            all_good = False
    
    return all_good

def check_required_files() -> bool:
    """すべての必要なファイルが存在するか確認"""
    print("\n📄 Checking required files...")
    
    required_files = [
        ("pyproject.toml", "パッケージ設定"),
        ("README.md", "プロジェクトREADME"),
        ("LICENSE", "ライセンスファイル"),
        ("MANIFEST.in", "パッケージマニフェスト"),
        ("setup.py", "セットアップスクリプト"),
    ]
    
    all_good = True
    for file_path, description in required_files:
        full_path = PROJECT_ROOT / file_path
        if not check_file_exists(full_path, description):
            all_good = False
    
    return all_good

def check_pyproject_config() -> bool:
    """pyproject.tomlの設定を確認"""
    print("\n⚙️ Checking pyproject.toml configuration...")
    
    try:
        pyproject_path = PROJECT_ROOT / "pyproject.toml"
        with open(pyproject_path, 'r') as f:
            pyproject = toml.load(f)
        
        project = pyproject.get('project', {})
        
        # Required fields
        required_fields = ['name', 'version', 'description', 'authors']
        for field in required_fields:
            if field in project:
                print(f"✅ {field}: {project[field]}")
            else:
                print(f"❌ 必要なフィールドがありません: {field}")
                return False
        
        # Check entry points
        scripts = project.get('scripts', {})
        if 'SuperClaude' in scripts:
            print(f"✅ CLIエントリポイント: {scripts['SuperClaude']}")
        else:
            print("❌ CLIエントリポイントがありません")
            return False
        
        # Check classifiers
        classifiers = project.get('classifiers', [])
        if len(classifiers) > 0:
            print(f"✅ {len(classifiers)} 個のPyPI分類子が定義されています")
        else:
            print("⚠️ PyPI分類子が定義されていません")
        
        return True
        
    except Exception as e:
        print(f"❌ pyproject.tomlの読み取りエラー: {e}")
        return False

def check_import_test() -> bool:
    """パッケージがインポートできるかテスト"""
    print("\n🧪 Testing package import...")
    
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        import SuperClaude
        print(f"✅ SuperClaudeのインポートに成功しました")
        print(f"📦 バージョン: {SuperClaude.__version__}")
        print(f"👤 作成者: {SuperClaude.__author__}")
        return True
    except Exception as e:
        print(f"❌ インポートに失敗しました: {e}")
        return False

def main():
    """メイン検証関数"""
    print("🔍 SuperClaude PyPI準備完了検証")
    print(f"📁 プロジェクトルート: {PROJECT_ROOT}")
    print("=" * 50)
    
    checks = [
        ("必要なファイル", check_required_files),
        ("パッケージ構造", check_package_structure),
        ("バージョンの一貫性", check_version_consistency),
        ("PyProject設定", check_pyproject_config),
        ("インポートテスト", check_import_test),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} のチェックが例外で失敗しました: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{total} 個のチェックに合格しました")
    
    if passed == total:
        print("🎉 プロジェクトはPyPI公開の準備ができました！")
        print("\nNext steps:")
        print("1. ./scripts/publish.sh test    # Test on TestPyPI")
        print("2. ./scripts/publish.sh prod    # Publish to PyPI")
        return True
    else:
        print("❌ プロジェクトはPyPI公開前に修正が必要です")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)