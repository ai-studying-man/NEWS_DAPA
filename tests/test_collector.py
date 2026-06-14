from __future__ import annotations

from unittest import TestCase

from dapa_morning_brief.collector import classify_title, is_relevant_title
from dapa_morning_brief.models import Section


class CollectorTest(TestCase):
    def test_is_relevant_title_rejects_non_defense_false_positives(self) -> None:
        # Given
        non_defense_titles = [
            "양산국유림관리소, 농경지 돌발해충 협업방제 실시",
            "2026년 5월 정보통신산업(ICT) 수출입 동향",
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
