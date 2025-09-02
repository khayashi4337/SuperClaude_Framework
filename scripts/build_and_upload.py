#!/usr/bin/env python3
"""
SuperClaudeフレームワーク用のPyPIビルドおよびアップロードスクリプト
適切なエラー処理でビルド、検証、PyPIへのアップロードを処理します
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path
from typing import Tuple, List, Optional

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"

def run_command(cmd: List[str], description: str) -> Tuple[bool, str]:
    """コマンドを実行し、成功ステータスと出力を返す"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=PROJECT_ROOT,
            check=True
        )
        print(f"✅ {description} が正常に完了しました")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} が失敗しました:")
        print(f"   終了コード: {e.returncode}")
        print(f"   エラー: {e.stderr}")
        return False, e.stderr
    except Exception as e:
        print(f"❌ {description} は例外で失敗しました: {e}")
        return False, str(e)

def clean_build_artifacts():
    """以前のビルドアーティファクトをクリーンアップ"""
    artifacts = [DIST_DIR, BUILD_DIR, PROJECT_ROOT / "SuperClaude.egg-info"]
    
    for artifact in artifacts:
        if artifact.exists():
            print(f"🧹 削除中 {artifact}")
            if artifact.is_dir():
                shutil.rmtree(artifact)
            else:
                artifact.unlink()

def install_build_tools() -> bool:
    """必要なビルドツールをインストール"""
    tools = ["build", "twine"]
    
    for tool in tools:
        success, _ = run_command(
            [sys.executable, "-m", "pip", "install", "--upgrade", tool],
            f"インストール中 {tool}"
        )
        if not success:
            return False
    
    return True

def validate_project_structure() -> bool:
    """ビルド前にプロジェクト構造を検証"""
    required_files = [
        "pyproject.toml",
        "README.md", 
        "LICENSE",
        "SuperClaude/__init__.py",
        "SuperClaude/__main__.py",
        "setup/__init__.py"
    ]
    
    print("🔍 プロジェクト構造を検証中...")
    
    for file_path in required_files:
        full_path = PROJECT_ROOT / file_path
        if not full_path.exists():
            print(f"❌ 必要なファイルがありません: {file_path}")
            return False
    
    # Check if version is consistent
    try:
        from SuperClaude import __version__
        print(f"📦 パッケージバージョン: {__version__}")
    except ImportError as e:
        print(f"❌ SuperClaudeからバージョンをインポートできませんでした: {e}")
        return False
    
    print("✅ プロジェクト構造の検証に合格しました")
    return True

def build_package() -> bool:
    """パッケージをビルド"""
    return run_command(
        [sys.executable, "-m", "build"],
        "パッケージ配布物をビルド中"
    )[0]

def validate_distribution() -> bool:
    """ビルドされた配布物を検証"""
    if not DIST_DIR.exists():
        print("❌ 配布ディレクトリが存在しません")
        return False
    
    dist_files = list(DIST_DIR.glob("*"))
    if not dist_files:
        print("❌ 配布ファイルが見つかりません")
        return False
    
    print(f"📦 配布ファイルが見つかりました:")
    for file in dist_files:
        print(f"   - {file.name}")
    
    # Check with twine
    return run_command(
        [sys.executable, "-m", "twine", "check"] + [str(f) for f in dist_files],
        "twineで配布物を検証中"
    )[0]

def upload_to_testpypi() -> bool:
    """テストのためにTestPyPIにアップロード"""
    dist_files = list(DIST_DIR.glob("*"))
    return run_command(
        [sys.executable, "-m", "twine", "upload", "--repository", "testpypi"] + [str(f) for f in dist_files],
        "TestPyPIにアップロード中"
    )[0]

def upload_to_pypi() -> bool:
    """本番PyPIにアップロード"""
    dist_files = list(DIST_DIR.glob("*"))
    
    # Check if we have API token in environment
    if os.getenv('PYPI_API_TOKEN'):
        cmd = [
            sys.executable, "-m", "twine", "upload",
            "--username", "__token__",
            "--password", os.getenv('PYPI_API_TOKEN')
        ] + [str(f) for f in dist_files]
    else:
        # Fall back to .pypirc configuration
        cmd = [sys.executable, "-m", "twine", "upload"] + [str(f) for f in dist_files]
    
    return run_command(cmd, "PyPIにアップロード中")[0]

def test_installation_from_testpypi() -> bool:
    """TestPyPIからのインストールをテスト"""
    print("🧪 TestPyPIからのインストールをテスト中...")
    print("   注: これは別のプロセスでインストールされます")
    
    success, output = run_command([
        sys.executable, "-m", "pip", "install", 
        "--index-url", "https://test.pypi.org/simple/",
        "--extra-index-url", "https://pypi.org/simple/",
        "SuperClaude", "--force-reinstall", "--no-deps"
    ], "TestPyPIからインストール中")
    
    if success:
        print("✅ テストインストールに成功しました")
        # Try to import the package
        try:
            import SuperClaude
            print(f"✅ パッケージのインポートに成功しました、バージョン: {SuperClaude.__version__}")
            return True
        except ImportError as e:
            print(f"❌ パッケージのインポートに失敗しました: {e}")
            return False
    
    return False

def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description="SuperClaudeをビルドしてPyPIにアップロード")
    parser.add_argument("--testpypi", action="store_true", help="PyPIの代わりにTestPyPIにアップロード")
    parser.add_argument("--test-install", action="store_true", help="TestPyPIからのインストールをテスト")
    parser.add_argument("--skip-build", action="store_true", help="ビルドステップをスキップ（既存のdistを使用）")
    parser.add_argument("--skip-validation", action="store_true", help="検証ステップをスキップ")
    parser.add_argument("--clean", action="store_true", help="ビルドアーティファクトのみをクリーンアップ")
    
    args = parser.parse_args()
    
    # Change to project root
    os.chdir(PROJECT_ROOT)
    
    if args.clean:
        clean_build_artifacts()
        return
    
    print("🚀 SuperClaude PyPI ビルドおよびアップロードスクリプト")
    print(f"📁 作業ディレクトリ: {PROJECT_ROOT}")
    
    # Step 1: Clean previous builds
    clean_build_artifacts()
    
    # Step 2: Install build tools
    if not install_build_tools():
        print("❌ ビルドツールのインストールに失敗しました")
        sys.exit(1)
    
    # Step 3: Validate project structure
    if not args.skip_validation and not validate_project_structure():
        print("❌ プロジェクト構造の検証に失敗しました")
        sys.exit(1)
    
    # Step 4: Build package
    if not args.skip_build:
        if not build_package():
            print("❌ パッケージのビルドに失敗しました")
            sys.exit(1)
    
    # Step 5: Validate distribution
    if not args.skip_validation and not validate_distribution():
        print("❌ 配布物の検証に失敗しました")
        sys.exit(1)
    
    # Step 6: Upload
    if args.testpypi:
        if not upload_to_testpypi():
            print("❌ TestPyPIへのアップロードに失敗しました")
            sys.exit(1)
        
        # Test installation if requested
        if args.test_install:
            if not test_installation_from_testpypi():
                print("❌ テストインストールに失敗しました")
                sys.exit(1)
    else:
        # Confirm production upload
        response = input("🚨 Upload to production PyPI? This cannot be undone! (yes/no): ")
        if response.lower() != "yes":
            print("❌ アップロードがキャンセルされました")
            sys.exit(1)
        
        if not upload_to_pypi():
            print("❌ PyPIへのアップロードに失敗しました")
            sys.exit(1)
    
    print("✅ すべての操作が正常に完了しました！")

if __name__ == "__main__":
    main()