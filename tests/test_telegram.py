from __future__ import annotations

from unittest import TestCase

from dapa_morning_brief.telegram import parse_chat_ids


class TelegramTest(TestCase):
    def test_parse_chat_ids_accepts_multiple_comma_separated_targets(self) -> None:
        # Given
        raw_chat_ids = "6015255978, -1004402722342"

        # When
        chat_ids = parse_chat_ids(raw_chat_ids)

        # Then
        self.assertEqual(("6015255978", "-1004402722342"), chat_ids)

    def test_parse_chat_ids_ignores_empty_parts(self) -> None:
        # Given
        raw_chat_ids = " 6015255978, , -1004402722342, "

        # When
        chat_ids = parse_chat_ids(raw_chat_ids)

        # Then
        self.assertEqual(("6015255978", "-1004402722342"), chat_ids)
