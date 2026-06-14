from __future__ import annotations

from unittest import TestCase

from dapa_morning_brief.collector import classify_title, is_relevant_title
from dapa_morning_brief.models import Section


class CollectorTest(TestCase):
    def test_is_relevant_title_rejects_non_defense_false_positives(self) -> None:
        # Given
        non_defense_titles = [
            "작성권 유리관리소, 환경지킴 캠페인 작업방제 실시",
            "2026년 정보통신산업(ICT) 수출 동향",
        ]

        # When
        results = [is_relevant_title(title) for title in non_defense_titles]

        # Then
        self.assertEqual([False, False], results)

    def test_classify_title_detects_weapon_system_when_defense_terms_exist(self) -> None:
        # Given
        title = "KF-21 후속양산 계획 구체화"

        # When
        section = classify_title(title)

        # Then
        self.assertEqual(Section.WEAPON_SYSTEM, section)

    def test_classify_title_detects_current_government_news(self) -> None:
        # Given
        title = "이재명 대통령, 자주국방과 방산수출 확대 필요성 언급"

        # When
        section = classify_title(title)

        # Then
        self.assertEqual(Section.GOVERNMENT, section)

    def test_classify_title_excludes_former_president_news_from_government(self) -> None:
        # Given
        title = "윤 전 대통령 평양 무인기 침투 사건 관련 재판"

        # When
        section = classify_title(title)

        # Then
        self.assertNotEqual(Section.GOVERNMENT, section)
