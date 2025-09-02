"""
自動検出と依存関係解決のためのコンポーネントレジストリ
"""

import importlib
import inspect
from typing import Dict, List, Set, Optional, Type
from pathlib import Path
from .base import Component
from ..utils.logger import get_logger


class ComponentRegistry:
    """インストール可能なコンポーネントの自動検出と管理"""
    
    def __init__(self, components_dir: Path):
        """
        コンポーネントレジストリを初期化します
        
        Args:
            components_dir: コンポーネントモジュールを含むディレクトリ
        """
        self.components_dir = components_dir
        self.component_classes: Dict[str, Type[Component]] = {}
        self.component_instances: Dict[str, Component] = {}
        self.dependency_graph: Dict[str, Set[str]] = {}
        self._discovered = False
        self.logger = get_logger()
    
    def discover_components(self, force_reload: bool = False) -> None:
        """
        componentsディレクトリ内のすべてのコンポーネントクラスを自動検出します
        
        Args:
            force_reload: 既に実行済みでも再検出を強制します
        """
        if self._discovered and not force_reload:
            return
        
        self.component_classes.clear()
        self.component_instances.clear()
        self.dependency_graph.clear()
        
        if not self.components_dir.exists():
            return
        
        # Add components directory to Python path temporarily
        import sys
        original_path = sys.path.copy()
        
        try:
            # Add parent directory to path so we can import setup.components
            setup_dir = self.components_dir.parent
            if str(setup_dir) not in sys.path:
                sys.path.insert(0, str(setup_dir))
            
            # Discover all Python files in components directory
            for py_file in self.components_dir.glob("*.py"):
                if py_file.name.startswith("__"):
                    continue
                
                module_name = py_file.stem
                self._load_component_module(module_name)
        
        finally:
            # Restore original Python path
            sys.path = original_path
        
        # Build dependency graph
        self._build_dependency_graph()
        self._discovered = True
    
    def _load_component_module(self, module_name: str) -> None:
        """
        モジュールからコンポーネントクラスを読み込みます
        
        Args:
            module_name: 読み込むモジュールの名前
        """
        try:
            # Import the module
            full_module_name = f"setup.components.{module_name}"
            module = importlib.import_module(full_module_name)
            
            # Find all コンポーネント subclasses in the module
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, Component) and 
                    obj is not Component):
                    
                    # Create instance to get metadata
                    try:
                        instance = obj()
                        metadata = instance.get_metadata()
                        component_name = metadata["name"]
                        
                        self.component_classes[component_name] = obj
                        self.component_instances[component_name] = instance
                        
                    except Exception as e:
                        self.logger.warning(f"コンポーネントをインスタンス化できませんでした {name}: {e}")
        
        except Exception as e:
            self.logger.warning(f"コンポーネントモジュールを読み込めませんでした {module_name}: {e}")
    
    def _build_dependency_graph(self) -> None:
        """検出されたすべてのコンポーネントの依存関係グラフを構築"""
        for name, instance in self.component_instances.items():
            try:
                dependencies = instance.get_dependencies()
                self.dependency_graph[name] = set(dependencies)
            except Exception as e:
                self.logger.warning(f"依存関係を取得できませんでした: {name}: {e}")
                self.dependency_graph[name] = set()
    
    def get_component_class(self, component_name: str) -> Optional[Type[Component]]:
        """
        名前でコンポーネントクラスを取得します
        
        Args:
            component_name: コンポーネント名
            
        Returns:
            コンポーネントクラス、見つからない場合はNone
        """
        self.discover_components()
        return self.component_classes.get(component_name)
    
    def get_component_instance(self, component_name: str, install_dir: Optional[Path] = None) -> Optional[Component]:
        """
        名前でコンポーネントインスタンスを取得します
        
        Args:
            component_name: コンポーネント名
            install_dir: インストールディレクトリ（このディレクトリで新しいインスタンスを作成）
            
        Returns:
            コンポーネントインスタンス、見つからない場合はNone
        """
        self.discover_components()
        
        if install_dir is not None:
            # Create new instance with specified install directory
            component_class = self.component_classes.get(component_name)
            if component_class:
                try:
                    return component_class(install_dir)
                except Exception as e:
                    self.logger.error(f"コンポーネントインスタンスの作成エラー {component_name}: {e}")
                    return None
        
        return self.component_instances.get(component_name)
    
    def list_components(self) -> List[str]:
        """
        検出されたすべてのコンポーネント名のリストを取得します
        
        Returns:
            コンポーネント名のリスト
        """
        self.discover_components()
        return list(self.component_classes.keys())
    
    def get_component_metadata(self, component_name: str) -> Optional[Dict[str, str]]:
        """
        コンポーネントのメタデータを取得します
        
        Args:
            component_name: コンポーネント名
            
        Returns:
            コンポーネントのメタデータ辞書、見つからない場合はNone
        """
        self.discover_components()
        instance = self.component_instances.get(component_name)
        if instance:
            try:
                return instance.get_metadata()
            except Exception:
                return None
        return None
    
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
        self.discover_components()
        
        resolved = []
        resolving = set()
        
        def resolve(name: str):
            if name in resolved:
                return
                
            if name in resolving:
                raise ValueError(f"循環依存が検出されました: {name}")
                
            if name not in self.dependency_graph:
                raise ValueError(f"不明なコンポーネント: {name}")
                
            resolving.add(name)
            
            # Resolve dependencies first
            for dep in self.dependency_graph[name]:
                resolve(dep)
                
            resolving.remove(name)
            resolved.append(name)
        
        # Resolve each requested component
        for name in component_names:
            resolve(name)
            
        return resolved
    
    def get_dependencies(self, component_name: str) -> Set[str]:
        """
        コンポーネントの直接の依存関係を取得します
        
        Args:
            component_name: コンポーネント名
            
        Returns:
            依存コンポーネント名のセット
        """
        self.discover_components()
        return self.dependency_graph.get(component_name, set())
    
    def get_dependents(self, component_name: str) -> Set[str]:
        """
        指定されたコンポーネントに依存するコンポーネントを取得します
        
        Args:
            component_name: コンポーネント名
            
        Returns:
            このコンポーネントに依存するコンポーネント名のセット
        """
        self.discover_components()
        dependents = set()
        
        for name, deps in self.dependency_graph.items():
            if component_name in deps:
                dependents.add(name)
                
        return dependents
    
    def validate_dependency_graph(self) -> List[str]:
        """
        依存関係グラフの循環と欠落している依存関係を検証します
        
        Returns:
            検証エラーのリスト（有効な場合は空）
        """
        self.discover_components()
        errors = []
        
        # Check for missing dependencies
        all_components = set(self.dependency_graph.keys())
        for name, deps in self.dependency_graph.items():
            missing_deps = deps - all_components
            if missing_deps:
                errors.append(f"コンポーネント {name} には不足している依存関係があります: {missing_deps}")
        
        # Check for circular dependencies
        for name in all_components:
            try:
                self.resolve_dependencies([name])
            except ValueError as e:
                errors.append(str(e))
        
        return errors
    
    def get_components_by_category(self, category: str) -> List[str]:
        """
        カテゴリでフィルタリングされたコンポーネントを取得します
        
        Args:
            category: フィルタリングするコンポーネントカテゴリ
            
        Returns:
            カテゴリ内のコンポーネント名のリスト
        """
        self.discover_components()
        components = []
        
        for name, instance in self.component_instances.items():
            try:
                metadata = instance.get_metadata()
                if metadata.get("category") == category:
                    components.append(name)
            except Exception:
                continue
        
        return components
    
    def get_installation_order(self, component_names: List[str]) -> List[List[str]]:
        """
        依存関係レベルでグループ化されたインストール順序を取得します
        
        Args:
            component_names: インストールするコンポーネント名のリスト
            
        Returns:
            リストのリスト。各内部リストには、その依存関係レベルで並行してインストールできるコンポーネントが含まれます
        """
        self.discover_components()
        
        # Get all components including dependencies
        all_components = set(self.resolve_dependencies(component_names))
        
        # Group by dependency level
        levels = []
        remaining = all_components.copy()
        
        while remaining:
            # Find components with no unresolved dependencies
            current_level = []
            for name in list(remaining):
                deps = self.dependency_graph.get(name, set())
                unresolved_deps = deps & remaining
                
                if not unresolved_deps:
                    current_level.append(name)
            
            if not current_level:
                # This shouldn't happen if dependency graph is valid
                raise ValueError("インストール順序の計算で循環依存が検出されました")
            
            levels.append(current_level)
            remaining -= set(current_level)
        
        return levels
    
    def create_component_instances(self, component_names: List[str], install_dir: Optional[Path] = None) -> Dict[str, Component]:
        """
        複数のコンポーネントのインスタンスを作成します
        
        Args:
            component_names: コンポーネント名のリスト
            install_dir: インスタンスのインストールディレクトリ
            
        Returns:
            コンポーネント名とインスタンスをマッピングする辞書
        """
        self.discover_components()
        instances = {}
        
        for name in component_names:
            instance = self.get_component_instance(name, install_dir)
            if instance:
                instances[name] = instance
            else:
                self.logger.warning(f"コンポーネントのインスタンスを作成できませんでした {name}")
        
        return instances
    
    def get_registry_info(self) -> Dict[str, any]:
        """
        包括的なレジストリ情報を取得します
        
        Returns:
            レジストリの統計とコンポーネント情報を含む辞書
        """
        self.discover_components()
        
        # Group components by category
        categories = {}
        for name, instance in self.component_instances.items():
            try:
                metadata = instance.get_metadata()
                category = metadata.get("category", "unknown")
                if category not in categories:
                    categories[category] = []
                categories[category].append(name)
            except Exception:
                if "unknown" not in categories:
                    categories["unknown"] = []
                categories["unknown"].append(name)
        
        return {
            "total_components": len(self.component_classes),
            "categories": categories,
            "dependency_graph": {name: list(deps) for name, deps in self.dependency_graph.items()},
            "validation_errors": self.validate_dependency_graph()
        }