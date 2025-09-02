"""
SuperClaudeインストールシステムの設定管理
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path

# Handle jsonschema import - if not available, use basic validation
try:
    import jsonschema
    from jsonschema import validate, ValidationError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    
    class ValidationError(Exception):
        """jsonschemaが利用できない場合のシンプルな検証エラー"""
        def __init__(self, message):
            self.message = message
            super().__init__(message)
    
    def validate(instance, schema):
        """ダミーの検証関数"""
        # Basic type checking only
        if "type" in schema:
            expected_type = schema["type"]
            if expected_type == "object" and not isinstance(instance, dict):
                raise ValidationError(f"オブジェクトを期待していましたが、取得したのは {type(instance).__name__}")
            elif expected_type == "array" and not isinstance(instance, list):
                raise ValidationError(f"配列を期待していましたが、取得したのは {type(instance).__name__}")
            elif expected_type == "string" and not isinstance(instance, str):
                raise ValidationError(f"文字列を期待していましたが、取得したのは {type(instance).__name__}")
            elif expected_type == "integer" and not isinstance(instance, int):
                raise ValidationError(f"整数を期待していましたが、取得したのは {type(instance).__name__}")
        # Skip detailed validation if jsonschema not available


class ConfigService:
    """設定ファイルと検証を管理します"""
    
    def __init__(self, config_dir: Path):
        """
        設定マネージャーを初期化します
        
        Args:
            config_dir: 設定ファイルを含むディレクトリ
        """
        self.config_dir = config_dir
        self.features_file = config_dir / "features.json"
        self.requirements_file = config_dir / "requirements.json"
        self._features_cache = None
        self._requirements_cache = None
        
        # Schema for features.json
        self.features_schema = {
            "type": "object",
            "properties": {
                "components": {
                    "type": "object",
                    "patternProperties": {
                        "^[a-zA-Z_][a-zA-Z0-9_]*$": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "version": {"type": "string"},
                                "description": {"type": "string"},
                                "category": {"type": "string"},
                                "dependencies": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "enabled": {"type": "boolean"},
                                "required_tools": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["name", "version", "description", "category"],
                            "additionalProperties": False
                        }
                    }
                }
            },
            "required": ["components"],
            "additionalProperties": False
        }
        
        # Schema for requirements.json
        self.requirements_schema = {
            "type": "object",
            "properties": {
                "python": {
                    "type": "object",
                    "properties": {
                        "min_version": {"type": "string"},
                        "max_version": {"type": "string"}
                    },
                    "required": ["min_version"]
                },
                "node": {
                    "type": "object",
                    "properties": {
                        "min_version": {"type": "string"},
                        "max_version": {"type": "string"},
                        "required_for": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["min_version"]
                },
                "disk_space_mb": {"type": "integer"},
                "external_tools": {
                    "type": "object",
                    "patternProperties": {
                        "^[a-zA-Z_][a-zA-Z0-9_-]*$": {
                            "type": "object",
                            "properties": {
                                "command": {"type": "string"},
                                "min_version": {"type": "string"},
                                "required_for": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "optional": {"type": "boolean"}
                            },
                            "required": ["command"],
                            "additionalProperties": False
                        }
                    }
                },
                "installation_commands": {
                    "type": "object",
                    "patternProperties": {
                        "^[a-zA-Z_][a-zA-Z0-9_-]*$": {
                            "type": "object",
                            "properties": {
                                "linux": {"type": "string"},
                                "darwin": {"type": "string"},
                                "win32": {"type": "string"},
                                "all": {"type": "string"},
                                "description": {"type": "string"}
                            },
                            "additionalProperties": False
                        }
                    }
                }
            },
            "required": ["python", "disk_space_mb"],
            "additionalProperties": False
        }
    
    def load_features(self) -> Dict[str, Any]:
        """
        Load and validate features configuration
        
        Returns:
            Features configuration dict
            
        Raises:
            FileNotFoundError: If features.json not found
            ValidationError: If features.json is invalid
        """
        if self._features_cache is not None:
            return self._features_cache
            
        if not self.features_file.exists():
            raise FileNotFoundError(f"機能設定が見つかりません: {self.features_file}")
        
        try:
            with open(self.features_file, 'r') as f:
                features = json.load(f)
                
            # Validate schema
            validate(instance=features, schema=self.features_schema)
            
            self._features_cache = features
            return features
            
        except json.JSONDecodeError as e:
            raise ValidationError(f"無効なJSON: {self.features_file}: {e}")
        except ValidationError as e:
            raise ValidationError(f"無効な機能スキーマ: {str(e)}")
    
    def load_requirements(self) -> Dict[str, Any]:
        """
        Load and validate requirements configuration
        
        Returns:
            Requirements configuration dict
            
        Raises:
            FileNotFoundError: If requirements.json not found
            ValidationError: If requirements.json is invalid
        """
        if self._requirements_cache is not None:
            return self._requirements_cache
            
        if not self.requirements_file.exists():
            raise FileNotFoundError(f"要件設定が見つかりません: {self.requirements_file}")
        
        try:
            with open(self.requirements_file, 'r') as f:
                requirements = json.load(f)
                
            # Validate schema
            validate(instance=requirements, schema=self.requirements_schema)
            
            self._requirements_cache = requirements
            return requirements
            
        except json.JSONDecodeError as e:
            raise ValidationError(f"無効なJSON: {self.requirements_file}: {e}")
        except ValidationError as e:
            raise ValidationError(f"無効な要件スキーマ: {str(e)}")
    
    def get_component_info(self, component_name: str) -> Optional[Dict[str, Any]]:
        """
        特定のコンポーネントに関する情報を取得します
        
        Args:
            component_name: コンポーネント名
            
        Returns:
            コンポーネント情報辞書、見つからない場合はNone
        """
        features = self.load_features()
        return features.get("components", {}).get(component_name)
    
    def get_enabled_components(self) -> List[str]:
        """
        有効なコンポーネント名のリストを取得します
        
        Returns:
            有効なコンポーネント名のリスト
        """
        features = self.load_features()
        enabled = []
        
        for name, info in features.get("components", {}).items():
            if info.get("enabled", True):  # Default to enabled
                enabled.append(name)
                
        return enabled
    
    def get_components_by_category(self, category: str) -> List[str]:
        """
        カテゴリ別のコンポーネント名を取得します
        
        Args:
            category: コンポーネントカテゴリ
            
        Returns:
            カテゴリ内のコンポーネント名のリスト
        """
        features = self.load_features()
        components = []
        
        for name, info in features.get("components", {}).items():
            if info.get("category") == category:
                components.append(name)
                
        return components
    
    def get_component_dependencies(self, component_name: str) -> List[str]:
        """
        コンポーネントの依存関係を取得します
        
        Args:
            component_name: コンポーネント名
            
        Returns:
            依存コンポーネント名のリスト
        """
        component_info = self.get_component_info(component_name)
        if component_info:
            return component_info.get("dependencies", [])
        return []
    
    def get_system_requirements(self) -> Dict[str, Any]:
        """
        システム要件を取得します
        
        Returns:
            システム要件の辞書
        """
        return self.load_requirements()
    
    def get_requirements_for_components(self, component_names: List[str]) -> Dict[str, Any]:
        """
        特定のコンポーネントの統合された要件を取得します
        
        Args:
            component_names: コンポーネント名のリスト
            
        Returns:
            統合された要件の辞書
        """
        requirements = self.load_requirements()
        features = self.load_features()
        
        # Start with base requirements
        result = {
            "python": requirements["python"],
            "disk_space_mb": requirements["disk_space_mb"],
            "external_tools": {}
        }
        
        # Add Node.js requirements if needed
        node_required = False
        for component_name in component_names:
            component_info = features.get("components", {}).get(component_name, {})
            required_tools = component_info.get("required_tools", [])
            
            if "node" in required_tools:
                node_required = True
                break
        
        if node_required and "node" in requirements:
            result["node"] = requirements["node"]
        
        # Add external tool requirements
        for component_name in component_names:
            component_info = features.get("components", {}).get(component_name, {})
            required_tools = component_info.get("required_tools", [])
            
            for tool in required_tools:
                if tool in requirements.get("external_tools", {}):
                    result["external_tools"][tool] = requirements["external_tools"][tool]
        
        return result
    
    def validate_config_files(self) -> List[str]:
        """
        すべての設定ファイルを検証します
        
        Returns:
            検証エラーのリスト（すべて有効な場合は空）
        """
        errors = []
        
        try:
            self.load_features()
        except Exception as e:
            errors.append(f"機能設定エラー: {e}")
        
        try:
            self.load_requirements()
        except Exception as e:
            errors.append(f"要件設定エラー: {e}")
        
        return errors
    
    def clear_cache(self) -> None:
        """キャッシュされた設定データをクリア"""
        self._features_cache = None
        self._requirements_cache = None