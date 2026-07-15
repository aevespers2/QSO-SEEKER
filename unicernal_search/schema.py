from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

MAX_CONTENT_CHARS = 200_000

class RawSearchRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    repository: str = Field(min_length=1, max_length=200)
    path: str = Field(min_length=1, max_length=512)
    url: HttpUrl
    content: str = Field(max_length=MAX_CONTENT_CHARS)
    source_kind: str = Field(default="file", pattern="^(description|topic|readme|file|issue|pull_request|comment|commit|release|workflow_log)$")

    @field_validator("repository")
    @classmethod
    def repository_shape(cls, value: str) -> str:
        if value.count("/") != 1:
            raise ValueError("repository must be owner/name")
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.")
        if any(ch not in allowed for ch in value.replace("/", "")):
            raise ValueError("repository contains invalid characters")
        return value

    @field_validator("path")
    @classmethod
    def safe_path(cls, value: str) -> str:
        normalized = value.replace("\\", "/")
        if normalized.startswith("/") or ".." in normalized.split("/"):
            raise ValueError("absolute paths and traversal are forbidden")
        return normalized

class SanitizedRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    repository: str
    path: str
    source_kind: str
    source_url: str
    content: str
    content_sha256: str
    flags: list[str]
    transformations: list[str]
