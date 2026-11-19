from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# --- Users ---
class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    display_name: str = Field(min_length=1, max_length=255)
    role: Literal["operator", "admin"] = "operator"


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: Optional[EmailStr] = None
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    role: Optional[Literal["operator", "admin"]] = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    display_name: str
    role: str
    created_at: datetime


# --- Projects ---
class ProjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    created_at: datetime


# --- Labels ---
class LabelCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=64)
    color: str = Field(default="#6b7280", pattern=r"^#[0-9a-fA-F]{6}$")


class LabelUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=64)
    color: Optional[str] = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")


class LabelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    color: str


# --- Tasks ---
class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_id: int
    assignee_id: Optional[int] = None
    label_id: Optional[int] = None
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    status: Literal["open", "in_progress", "done"] = "open"
    priority: Literal["low", "medium", "high"] = "medium"


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    label_id: Optional[int] = None
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[Literal["open", "in_progress", "done"]] = None
    priority: Optional[Literal["low", "medium", "high"]] = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    assignee_id: Optional[int]
    label_id: Optional[int]
    title: str
    description: Optional[str]
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime


# --- Comments ---
class CommentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: int
    author_id: int
    body: str = Field(min_length=1)

    @field_validator("body")
    @classmethod
    def body_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Comment body cannot be empty")
        return v


class CommentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    body: Optional[str] = Field(default=None, min_length=1)

    @field_validator("body")
    @classmethod
    def body_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Comment body cannot be empty")
        return v


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    author_id: int
    body: str
    created_at: datetime
