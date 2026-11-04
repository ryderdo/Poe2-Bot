"""Tests for the pure party leader lookup helper."""

import unittest

from party_leader import PartyDataError, find_party_leader


class FindPartyLeaderTests(unittest.TestCase):
    def setUp(self):
        self.members = [
            {"ign": "  Mira  ", "is_leader": False, "area_raw_name": "Hideout"},
            {"ign": "Aster", "is_leader": True, "area_raw_name": "MapBloomingField"},
        ]

    def test_finds_member_marked_as_leader(self):
        leader = find_party_leader(self.members)
        self.assertEqual(leader.name, "Aster")
        self.assertEqual(leader.area, "MapBloomingField")
        self.assertTrue(leader.is_leader)

    def test_selects_requested_member_case_insensitively(self):
        member = find_party_leader(self.members, preferred_name=" mira ")
        self.assertEqual(member.name, "Mira")
        self.assertFalse(member.is_leader)

    def test_empty_party_is_a_clear_error(self):
        with self.assertRaisesRegex(PartyDataError, "empty"):
            find_party_leader([])

    def test_missing_leader_is_a_clear_error(self):
        with self.assertRaisesRegex(PartyDataError, "exactly one"):
            find_party_leader([{"ign": "Mira", "is_leader": False}])

    def test_multiple_leaders_are_rejected(self):
        with self.assertRaisesRegex(PartyDataError, "exactly one"):
            find_party_leader([
                {"ign": "Mira", "is_leader": True},
                {"ign": "Aster", "is_leader": True},
            ])

    def test_duplicate_requested_name_is_rejected(self):
        with self.assertRaisesRegex(PartyDataError, "Expected one"):
            find_party_leader([
                {"ign": "Mira", "is_leader": False},
                {"ign": "mira", "is_leader": True},
            ], preferred_name="Mira")

    def test_blank_or_missing_name_is_rejected(self):
        with self.assertRaisesRegex(PartyDataError, "name"):
            find_party_leader([{"ign": "  ", "is_leader": True}])

    def test_invalid_leader_flag_is_rejected(self):
        with self.assertRaisesRegex(PartyDataError, "boolean"):
            find_party_leader([{"ign": "Mira", "is_leader": "yes"}])

    def test_name_alias_and_area_alias_are_supported(self):
        member = find_party_leader([{"name": "Aster", "is_leader": True, "area": "Map"}])
        self.assertEqual((member.name, member.area), ("Aster", "Map"))


if __name__ == "__main__":
    unittest.main()
