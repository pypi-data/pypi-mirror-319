from enum import Enum
from typing import Optional, Dict, Union, List, Literal, Any
from pydantic import BaseModel, Field, HttpUrl
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
import re
import typing


class ChartType(str, Enum):
    """Types of supported charts"""
    BAR = "bar"
    LINE = "line"
    MAP = "map"
    COUNTER = "counter"
    SCATTER = "scatter"
    TABLE = "table"

class Color(str):
    """Validates hex colors with optional alpha"""
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: typing.Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("string required")
        
        if not re.match(r'^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$', v):
            raise ValueError("invalid hex color format - must be #RRGGBB or #RRGGBBAA")
            
        return v

class ChartTags(Dict[str, Union[str, List[str]]]):
    """Tags for charts with validation rules"""
    
    def __init__(self, tags: Dict[str, Union[str, List[str]]]):
        self.validate_tags(tags)
        super().__init__(tags)
    
    @classmethod
    def validate_tags(cls, tags: Dict[str, Any]) -> None:
        if len(tags) > 10:
            raise ValueError("Maximum of 10 tags allowed")

        key_pattern = re.compile(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$')
        
        for key, value in tags.items():
            # Key validation
            if not 1 <= len(key) <= 32:
                raise ValueError(f"Tag key '{key}' must be between 1 and 32 characters")
            
            if not key_pattern.match(key):
                raise ValueError(f"Tag key '{key}' must be lowercase alphanumeric with hyphens, cannot start/end with hyphen")

            # Value validation
            values = [value] if isinstance(value, str) else value
            
            if not isinstance(values, (str, list)):
                raise ValueError(f"Tag value must be string or list of strings")

            for val in values:
                if not isinstance(val, str):
                    raise ValueError(f"Tag value must be string, got {type(val)}")
                
                if not 1 <= len(val) <= 64:
                    raise ValueError(f"Tag value '{val}' must be between 1 and 64 characters")
                
                if not all(c.isprintable() for c in val):
                    raise ValueError(f"Tag value '{val}' contains invalid characters")
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.dict_schema(
                keys_schema=core_schema.str_schema(),
                values_schema=core_schema.union_schema([
                    core_schema.str_schema(),
                    core_schema.list_schema(core_schema.str_schema())
                ])
            ),
            python_schema=core_schema.union_schema(
                choices=[
                    core_schema.is_instance_schema(cls),
                    core_schema.dict_schema(
                        keys_schema=core_schema.str_schema(),
                        values_schema=core_schema.union_schema([
                            core_schema.str_schema(),
                            core_schema.list_schema(core_schema.str_schema())
                        ])
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                function=lambda x: dict(x),
                return_schema=core_schema.dict_schema(
                    keys_schema=core_schema.str_schema(),
                    values_schema=core_schema.union_schema([
                        core_schema.str_schema(),
                        core_schema.list_schema(core_schema.str_schema())
                    ])
                ),
                when_used='json'
            )
        )
    
    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: CoreSchema,
        _handler: GetCoreSchemaHandler,
    ) -> JsonSchemaValue:
        return {
            "type": "object",
            "maxProperties": 10,
            "propertyNames": {
                "type": "string",
                "pattern": "^[a-z0-9][a-z0-9-]*[a-z0-9]$",
                "minLength": 3,
                "maxLength": 32
            },
            "additionalProperties": {
                "oneOf": [
                    {"type": "string", "maxLength": 64},
                    {
                        "type": "array",
                        "items": {"type": "string", "maxLength": 64},
                        "uniqueItems": True
                    }
                ]
            }
        }

class BaseMetadata(BaseModel):
    """Base metadata shared by all chart types"""
    type: ChartType
    title: str = Field(..., min_length=8, max_length=140)
    subtitle: Optional[str] = Field(None, min_length=3, max_length=140)
    description: Optional[str] = Field(None, min_length=8, max_length=2000)
    icon: Optional[HttpUrl] = None
    background_color: Color = Field(default="#FFFFFF")
    show_legend: bool = Field(default=True)
    
    model_config = {
        'extra': 'forbid'
    }


class AxisConfig(BaseModel):
    """Base configuration for chart axes"""
    label: Optional[str] = Field(..., min_length=1, max_length=100)
    show_grid: bool = Field(default=True)
    show_line: bool = Field(default=True)

class NumericAxisConfig(AxisConfig):
    """Configuration for numeric axes with scale options"""
    min: Optional[float] = None
    max: Optional[float] = None  
    log_scale: bool = Field(default=False)

class BaseChartProperties(BaseModel):
    """Base properties shared by all charts"""
    metadata: BaseMetadata
    data: Any 
    is_draft: bool = Field(default=False)
    tags: Optional[ChartTags] = None
    
    model_config = {
        'extra': 'forbid'
    }
