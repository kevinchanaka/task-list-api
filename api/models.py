from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Task:
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[str] = None
    completed: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Token:
    token: str
    expiry: int


@dataclass
class User:
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    password_hash: Optional[str] = None


@dataclass
class Label:
    id: Optional[str] = None
    name: Optional[str] = None
    colour: Optional[str] = None
    user_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
