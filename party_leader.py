"""Helpers for identifying a party leader from party-member data.

This module deliberately contains no game or network integration: callers pass
party data obtained from their own trusted source, and receive a validated
leader record (or an explicit error).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True, slots=True)
class PartyMember:
    """Normalized party-member information needed by a follower."""

    name: str
    is_leader: bool = False
    area: str | None = None


class PartyDataError(ValueError):
    """Raised when party data is missing, malformed, or ambiguous."""


def _clean_name(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def normalize_party_member(raw: Mapping[str, Any]) -> PartyMember:
    """Convert one mapping from a party API into a validated member record."""
    if not isinstance(raw, Mapping):
        raise PartyDataError("Each party member must be a mapping")

    name = _clean_name(raw.get("ign", raw.get("name")))
    if not name:
        raise PartyDataError("Party member is missing a non-empty name")

    leader_value = raw.get("is_leader", False)
    if not isinstance(leader_value, bool):
        raise PartyDataError(f"is_leader for {name!r} must be a boolean")

    area_value = raw.get("area_raw_name", raw.get("area"))
    area = _clean_name(area_value) or None
    return PartyMember(name=name, is_leader=leader_value, area=area)


def find_party_leader(
    members: Iterable[Mapping[str, Any]], *, preferred_name: str | None = None
) -> PartyMember:
    """Find the leader, or a requested member, without relying on screen text.

    If ``preferred_name`` is supplied, that member is selected case-insensitively
    (useful when the caller intentionally follows a specific party member).
    Otherwise exactly one member must have ``is_leader=True``.
    """
    try:
        normalized = [normalize_party_member(member) for member in members]
    except TypeError as exc:
        raise PartyDataError("Party members must be an iterable of mappings") from exc

    if not normalized:
        raise PartyDataError("Party data is empty; check that the party panel/data is available")

    if preferred_name is not None:
        requested = _clean_name(preferred_name)
        if not requested:
            raise PartyDataError("preferred_name cannot be empty")
        matches = [member for member in normalized if member.name.casefold() == requested.casefold()]
        if len(matches) != 1:
            raise PartyDataError(f"Expected one party member named {requested!r}, found {len(matches)}")
        return matches[0]

    leaders = [member for member in normalized if member.is_leader]
    if len(leaders) != 1:
        raise PartyDataError(f"Expected exactly one party leader, found {len(leaders)}")
    return leaders[0]
