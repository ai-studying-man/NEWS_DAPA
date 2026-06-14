from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import assert_never


class Section(StrEnum):
    """Newsletter section."""

    GOVERNMENT = "government"
    POLICY = "policy"
    WEAPON_SYSTEM = "weapon_system"
    EXPORT_BUSINESS = "export_business"

    @property
    def title(self) -> str:
        match self:
            case Section.GOVERNMENT:
                return "현 정부 주요 뉴스"
            case Section.POLICY:
                return "방위사업 관련 동향"
            case Section.WEAPON_SYSTEM:
                return "무기체계·전력화"
            case Section.EXPORT_BUSINESS:
                return "방산수출·기업동향"
            case unreachable:
                assert_never(unreachable)


@dataclass(frozen=True, slots=True)
class Article:
    """Collected news article metadata."""

    title: str
    url: str
    published_at: datetime
    source: str
    section: Section


@dataclass(frozen=True, slots=True)
class Briefing:
    """Selected newsletter articles grouped by section."""

    sections: dict[Section, tuple[Article, ...]]
