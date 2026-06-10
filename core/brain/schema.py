"""Pydantic schemas for the Brain layer (00-Brain/*.md)."""
from __future__ import annotations
from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, Field

BusinessStage = Literal["pre-seed", "seed", "growth", "mature", "pivot", "unknown"]


class Strategy(BaseModel):
    vision: str
    mission: Optional[str] = None
    icp: str = Field(description="Ideal Customer Profile")
    icp_details: Optional[str] = None
    yearly_goals: dict[str, str] = Field(default_factory=dict)
    positioning: Optional[str] = None


class Product(BaseModel):
    code: str
    name: str
    price_usd: int = Field(gt=0, description="Price in USD")
    margin_pct: float = Field(ge=0, le=100)
    status: str = "active"
    features: list[str] = Field(default_factory=list)


class BudgetLine(BaseModel):
    department: str
    allocated_usd: int = Field(ge=0)
    spent_usd: int = Field(ge=0, default=0)

    @property
    def remaining_usd(self) -> int:
        return self.allocated_usd - self.spent_usd


class Budget(BaseModel):
    total_year_usd: int
    spent_year_usd: int = 0
    by_department: list[BudgetLine] = Field(default_factory=list)
    mkt_quarter_remaining_usd: int = 0


class Headcount(BaseModel):
    active_departments: list[str] = Field(default_factory=list)
    active_agents: dict[str, list[str]] = Field(default_factory=dict)
    expertise_gaps: list[str] = Field(default_factory=list)


class LawReference(BaseModel):
    name: str
    code: Optional[str] = None
    scope: str = "general"  # general | industry | local
    note: Optional[str] = None


class DecisionEntry(BaseModel):
    date: date
    slug: str
    owner: str
    decision: str
    reason: str
    task_ref: Optional[str] = None


class BrainContext(BaseModel):
    """Assembled view of the entire 00-Brain/ — passed into every agent."""
    strategy: Strategy
    products: list[Product]
    budget: Budget
    headcount: Headcount
    laws: list[LawReference]
    decisions: list[DecisionEntry]
    state: BusinessStage
    glossary: dict[str, str]
