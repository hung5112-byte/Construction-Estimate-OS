"""Signals layer (Layer 0) — inbound event ingestion in front of ENTRY.

Watchers (email/chat) yield Events → deterministic prefilter → LLM triage
→ deterministic trigger policy → dispatcher (bd_run + bd_meeting, stops at
Stop 1). Auto-triggered flows NEVER approve or execute — that stays human.
"""
