from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from dapa_morning_brief.models import Section

USER_AGENT: Final[str] = (
    "DAPA-Morning-Brief/0.1 "
    "(public RSS newsletter automation; contact: repository owner)"
)

SECTION_QUERIES: Final[dict[Section, str]] = {
    Section.GOVERNMENT: (
        "이재명 대통령 방산 OR 이 대통령 방산 OR 대통령 방위사업 OR 대통령 방위산업 "
        "OR 대통령 국방획득 OR 대통령 국방예산 OR 대통령 자주국방 "
        "OR 국방부 장관 방위사업 OR 국방부 장관 방산 OR 국방부 장관 무기체계 "
        "OR 합참의장 방위사업 OR 합참의장 방산 "
        "OR 육군참모총장 방산 OR 해군참모총장 방산 OR 공군참모총장 방산"
    ),
    Section.POLICY: (
        "방위사업청 OR 방위사업 OR 방위력개선 OR 국방획득 OR 국방조달 "
        "OR 방위사업법 OR 국방예산 OR 국방정책"
    ),
    Section.WEAPON_SYSTEM: (
        "무기체계 OR 전력화 OR 체계개발 OR 양산사업 OR 후속양산 "
        "OR 최초양산 OR 시험평가 OR 야전운용시험 OR ROC OR CDR OR PDR"
    ),
    Section.EXPORT_BUSINESS: (
        "방산수출 OR K방산 OR 방산기업 OR 방위산업 OR 방산계약 "
        "OR 절충교역 OR 한화에어로스페이스 OR LIG넥스원 OR 현대로템 "
        "OR 한국항공우주 OR KAI OR 풍산"
    ),
}

BROAD_FALLBACK_QUERY: Final[str] = "방위사업 OR 무기체계 OR 방산수출 OR K방산"
SINGLE_FALLBACK_KEYWORDS: Final[tuple[str, ...]] = (
    "방위사업청",
    "방위사업",
    "무기체계",
    "전력화",
    "시험평가",
    "방산수출",
    "K방산",
)

RELEVANT_KEYWORDS: Final[tuple[str, ...]] = (
    "방위사업청",
    "방위사업",
    "방위력개선",
    "국방획득",
    "국방조달",
    "방위사업법",
    "국방예산",
    "국방정책",
    "국방부 장관",
    "국방장관",
    "합참의장",
    "참모총장",
    "자주국방",
    "핵잠수함",
    "방산",
    "방위산업",
    "무기체계",
    "전력화",
    "체계개발",
    "시험평가",
    "야전운용시험",
    "국방과학연구소",
    "ADD",
    "KF-21",
    "K2 전차",
    "K9",
    "L-SAM",
    "M-SAM",
    "천궁",
    "미사일",
    "전투기",
    "전차",
    "함정",
    "드론",
    "무인기",
    "한화에어로",
    "LIG넥스원",
    "현대로템",
    "한국항공우주",
    "KAI",
    "풍산",
)


@dataclass(frozen=True, slots=True)
class RssSource:
    """RSS source metadata."""

    name: str
    url: str
    default_section: Section | None


RSS_SOURCES: Final[tuple[RssSource, ...]] = (
    RssSource(
        name="정책브리핑 방위사업청",
        url="https://www.korea.kr/rss/dept_dapa.xml",
        default_section=Section.POLICY,
    ),
    RssSource(
        name="정책브리핑 국방부",
        url="https://www.korea.kr/rss/dept_mnd.xml",
        default_section=Section.POLICY,
    ),
    RssSource(
        name="정책브리핑 보도자료",
        url="https://www.korea.kr/rss/pressrelease.xml",
        default_section=None,
    ),
    RssSource(
        name="국방일보 방위사업",
        url="http://kookbang.dema.mil.kr/dema_xml/dema0010020000.xml",
        default_section=None,
    ),
)
