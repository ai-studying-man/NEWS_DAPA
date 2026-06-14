from __future__ import annotations

from datetime import datetime, timezone
from unittest import TestCase

from dapa_morning_brief.briefing import build_briefing, format_telegram_message
from dapa_morning_brief.models import Article, Section


class BriefingTest(TestCase):
    def test_build_briefing_deduplicates_titles_and_limits_each_section(self) -> None:
        # Given
        published = datetime(2026, 6, 14, 6, 0, tzinfo=timezone.utc)
        articles = [
            Article(
                title="방위사업청, 획득제도 개선안 발표",
                url="https://example.com/a",
                published_at=published,
                source="정책브리핑",
                section=Section.POLICY,
            ),
            Article(
                title="방위사업청, 획득제도 개선안 발표",
                url="https://example.com/b",
                published_at=published,
                source="Google News",
                section=Section.POLICY,
            ),
        ]
        articles.extend(
            Article(
                title=f"정책 기사 {index}",
                url=f"https://example.com/policy-{index}",
                published_at=published,
                source="뉴스",
                section=Section.POLICY,
            )
            for index in range(1, 5)
        )

        # When
        briefing = build_briefing(articles, max_per_section=3)

        # Then
        policy_articles = briefing.sections[Section.POLICY]
        self.assertEqual(3, len(policy_articles))
        self.assertEqual("방위사업청, 획득제도 개선안 발표", policy_articles[0].title)
        self.assertEqual(
            len({article.title for article in policy_articles}),
            len(policy_articles),
        )

    def test_format_telegram_message_contains_sections_summary_and_links(self) -> None:
        # Given
        published = datetime(2026, 6, 14, 6, 0, tzinfo=timezone.utc)
        briefing = build_briefing(
            [
                Article(
                    title="KF-21 후속 양산 계획 구체화",
                    url="https://example.com/kf21",
                    published_at=published,
                    source="국방일보",
                    section=Section.WEAPON_SYSTEM,
                ),
            ],
            max_per_section=3,
        )

        # When
        message = format_telegram_message(
            briefing,
            today=datetime(2026, 6, 14, tzinfo=timezone.utc).date(),
        )

        # Then
        self.assertIn("방산출근길 - 2026.06.14", message)
        self.assertIn("무기체계·전력화", message)
        self.assertIn("→ KF-21 후속 양산 계획 구체화", message)
        self.assertIn("📌 실무 참고:", message)
        self.assertIn("🔗 https://example.com/kf21", message)
