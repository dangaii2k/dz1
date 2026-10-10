from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskIn(BaseModel):
    title: str = Field(examples=["Сделать домашку"])
    priority: int = Field(default=5, ge=1, le=5, examples=[3])


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: int

    model_config = ConfigDict(from_attributes=True)
