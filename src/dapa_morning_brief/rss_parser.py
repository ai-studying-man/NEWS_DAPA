from __future__ import annotations

import email.utils
import re
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from datetime import UTC, datetime, timedelta

from dapa_morning_brief.models import Article, Section
from dapa_morning_brief.sources import RELEVANT_KEYWORDS


def parse_rss_items(
    xml_text: str,
    *,
    source_name: str,
    default_section: Section | None,
    days: int,
    now: datetime,
) -> list[Article]:
    """Parse RSS XML into article metadata."""
    root = ET.fromstring(xml_text)
    cutoff = now - timedelta(days=days)
    articles: list[Article] = []

    for item in root.findall(".//item"):
        title = _text(item, "title")
        link = _text(item, "link")
        published_at = _parse_date(_text(item, "pubDate"), now)
        if not title or not link or published_at < cutoff:
            continue
        if not is_relevant_title(title):
            continue
        if default_section is Section.GOVERNMENT and not _is_current_government_news(
            title.casefold(),
        ):
            continue
        section = default_section or classify_title(title)
        source = _source_from_item(item) or source_name
        articles.append(
            Article(
                title=_clean_title(title),
                url=link,
                published_at=published_at,
                source=source,
                section=section,
            ),
        )

    return articles


def classify_title(title: str) -> Section:
    """Classify an article title into the closest newsletter section."""
    text = title.casefold()
    if _is_current_government_news(text):
        return Section.GOVERNMENT
    if _contains_any(
        text,
        (
            "방산수출",
            "k방산",
            "방산기업",
            "방위산업",
            "방산계약",
            "절충교역",
            "한화에어로",
            "lig",
            "현대로템",
            "한국항공우주",
            "kai",
            "풍산",
        ),
    ):
        return Section.EXPORT_BUSINESS
    if _contains_any(
        text,
        (
            "무기",
            "전력화",
            "체계개발",
            "양산사업",
            "후속양산",
            "최초양산",
            "시험평가",
            "kf-21",
            "미사일",
            "전투기",
            "함정",
        ),
    ):
        return Section.WEAPON_SYSTEM
    return Section.POLICY


def is_relevant_title(title: str) -> bool:
    """Return whether a title is relevant enough for DAPA morning brief."""
    text = title.casefold()
    return _contains_any(text, RELEVANT_KEYWORDS)


def _is_current_government_news(text: str) -> bool:
    government_actor_terms = (
        "이재명 대통령",
        "이 대통령",
        "국방부 장관",
        "국방장관",
        "합참의장",
        "육군참모총장",
        "해군참모총장",
        "공군참모총장",
    )
    defense_terms = (
        "방위사업",
        "방산",
        "방위산업",
        "방산수출",
        "국방",
        "자주국방",
        "무기체계",
        "전력화",
        "k방산",
        "획득",
        "방위력개선",
        "국방예산",
        "핵잠수함",
        "무인기",
        "드론",
    )
    return _contains_any(text, government_actor_terms) and _contains_any(
        text,
        defense_terms,
    )


def _text(item: ET.Element, name: str) -> str:
    found = item.find(name)
    if found is None or found.text is None:
        return ""
    return found.text.strip()


def _source_from_item(item: ET.Element) -> str:
    for child in item:
        if child.tag.endswith("source") and child.text:
            return child.text.strip()
    return ""


def _parse_date(raw: str, fallback: datetime) -> datetime:
    if not raw:
        return fallback
    parsed = email.utils.parsedate_to_datetime(raw)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _clean_title(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip()


def _contains_any(text: str, needles: Iterable[str]) -> bool:
    return any(needle.casefold() in text for needle in needles)
