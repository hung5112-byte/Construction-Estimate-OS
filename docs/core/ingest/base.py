"""Shared types for the ingestion converters (avoids converters↔cad cycle)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConversionResult:
    body: str
    converter: str
    tier: str
    confidence: str  # high | med | low
    notes: str = ""
