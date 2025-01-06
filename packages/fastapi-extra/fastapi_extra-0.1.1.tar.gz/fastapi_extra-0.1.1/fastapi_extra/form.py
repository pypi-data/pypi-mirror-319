__author__ = "ziyan.yin"
__date__ = "2024-12-24"


from typing import Generic, Literal

from pydantic import BaseModel, Field, model_validator

from fastapi_extra.types import C, S


class DataRange(BaseModel, Generic[C]):
    start: C | None = Field(default=None, title="起始")
    end: C | None = Field(default=None, title="终止")


class ColumnExpression(BaseModel, Generic[S]):
    column_name: str = Field(title="列名")
    option: Literal["eq", "ne", "gt", "lt", "ge", "le"] = Field(default="eq", title="逻辑值")
    value: S = Field(title="参考值")
    
    @model_validator(mode="after")
    def validate_value(self):
        if self.value is None and self.option not in ("eq", "ne"):
            raise ValueError("NoneType is not comparable")


class WhereClause(BaseModel):
    option: Literal["and", "or"] = Field(default="and", title="关系")
    column_clauses: list[ColumnExpression | "WhereClause"]
