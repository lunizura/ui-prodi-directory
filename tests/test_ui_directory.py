"""
Automated end-to-end validation test suite for Universitas Indonesia (UI) Study Programs Directory.
Verifies dataset consistency across JSON, JS, CSV, metadata, admission quotas, DOM contract elements,
and strict zero-emoji compliance.
"""

import os
import json
import csv
import re
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
INDEX_HTML = os.path.join(ROOT_DIR, "index.html")
README_MD = os.path.join(ROOT_DIR, "README.md")


class TestDatasetIntegrity(unittest.TestCase):
    """Verify integrity, counts, and parity across UI data files."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(DATA_DIR, "metadata.json"), "r", encoding="utf-8") as f:
            cls.metadata = json.load(f)

        with open(os.path.join(DATA_DIR, "ui_prodi.json"), "r", encoding="utf-8") as f:
            cls.prodi_json = json.load(f)

        with open(os.path.join(DATA_DIR, "ui_prodi.js"), "r", encoding="utf-8") as f:
            content = f.read()
            match_data = re.search(r"window\.UI_PRODI_DATA\s*=\s*(\[[\s\S]*?\]);", content)
            assert match_data is not None, "ui_prodi.js must define window.UI_PRODI_DATA"
            cls.prodi_js = json.loads(match_data.group(1))

            match_fac = re.search(r"window\.UI_FACULTIES\s*=\s*(\{[\s\S]*?\});", content)
            assert match_fac is not None, "ui_prodi.js must define window.UI_FACULTIES"
            cls.faculties_js = json.loads(match_fac.group(1))

        with open(os.path.join(DATA_DIR, "ui_prodi.csv"), "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cls.prodi_csv = list(reader)

    def test_total_counts(self):
        """Verify program counts across metadata, JSON, JS, and CSV."""
        self.assertEqual(self.metadata["total_prodi"], 85)
        self.assertEqual(len(self.prodi_json), 85)
        self.assertEqual(len(self.prodi_js), 85)
        self.assertEqual(len(self.prodi_csv), 85)
        self.assertEqual(self.metadata["total_fakultas"], 17)
        self.assertEqual(len(self.faculties_js), 17)
        self.assertEqual(self.metadata["total_s1"], 60)
        self.assertEqual(self.metadata["total_vokasi"], 12)
        self.assertEqual(self.metadata["total_pascasarjana"], 13)

    def test_faculty_coverage(self):
        """Ensure all 17 faculties and academic units are represented."""
        expected_faculties = {
            "FK", "FKG", "FF", "FKM", "FIK", "FMIPA", "FT", "FASILKOM",
            "FH", "FEB", "FPsi", "FISIP", "FIA", "FIB", "Vokasi", "SKSG", "SIL"
        }
        found_faculties = {p["fakultas_singkatan"] for p in self.prodi_json}
        self.assertEqual(found_faculties, expected_faculties)

    def test_campus_locations(self):
        """Ensure both Depok and Salemba campuses are present."""
        locations = {p["lokasi"] for p in self.prodi_json}
        has_depok = any("Depok" in loc for loc in locations)
        has_salemba = any("Salemba" in loc for loc in locations)
        self.assertTrue(has_depok, "Depok campus must be present")
        self.assertTrue(has_salemba, "Salemba campus must be present")

    def test_admission_quota_balance(self):
        """Verify that total quota equals the sum of SNBP, SNBT, and SIMAK UI."""
        for p in self.prodi_json:
            total = p["daya_tampung"]
            snbp = p["dt_snbp"]
            snbt = p["dt_snbt"]
            simak = p["dt_simak"]
            self.assertEqual(total, snbp + snbt + simak, f"Quota sum mismatch for {p['id']}")

    def test_qualitative_profiles(self):
        """Verify bilingual descriptions, curriculum focus, and career prospects."""
        for p in self.prodi_json:
            profil = p.get("profil", {})
            deskripsi = p.get("deskripsi", {})
            self.assertTrue(len(deskripsi.get("id", "")) > 10, f"{p['id']} missing Indonesian description")
            self.assertTrue(len(deskripsi.get("en", "")) > 10, f"{p['id']} missing English description")

            fokus = p.get("fokus", {})
            self.assertTrue(len(fokus.get("id", [])) >= 2, f"{p['id']} missing Indonesian curriculum focus")
            self.assertTrue(len(fokus.get("en", [])) >= 2, f"{p['id']} missing English curriculum focus")

            karir = p.get("karir", {})
            self.assertTrue(len(karir.get("id", [])) >= 2, f"{p['id']} missing Indonesian career prospects")
            self.assertTrue(len(karir.get("en", [])) >= 2, f"{p['id']} missing English career prospects")


class TestUIElements(unittest.TestCase):
    """Verify index.html DOM structure and interactive components."""

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            cls.html = f.read()

    def test_required_dom_ids(self):
        """Verify presence of all required DOM element IDs."""
        required_ids = [
            # Header & Navbar
            "announcement-text",
            "announcement-updated",
            "lang-toggle-btn",
            "nav-title",
            "nav-subtitle",
            # Hero stats
            "stat-prodi-val",
            "stat-s1-val",
            "stat-vokasi-val",
            "stat-fakultas-val",
            "stat-intl-val",
            # Filter controls
            "filter-search",
            "filter-jenjang",
            "filter-fakultas",
            "filter-rumpun",
            "filter-lokasi",
            "filter-intl",
            "view-grid-btn",
            "view-table-btn",
            "btn-reset-filters",
            # Containers
            "cards-grid-container",
            "table-view-container",
            "directory-table-body",
            # Modal Dialog
            "prodi-modal",
            "modal-close-btn",
            "modal-jenjang-badge",
            "modal-fakultas-badge",
            "modal-rumpun-badge",
            "modal-lokasi-badge",
            "modal-prodi-name",
            "modal-fakultas-full",
            "modal-dt-total",
            "modal-dt-snbp",
            "modal-dt-snbt",
            "modal-dt-simak",
            "modal-desc",
            "modal-focus-list",
            "modal-career-tags",
            "modal-ukt-info",
            "modal-btn-copy",
            "modal-link-simak",
            "modal-link-web",
            # Toast
            "toast",
            "toast-message"
        ]
        for elem_id in required_ids:
            self.assertIn(f'id="{elem_id}"', self.html, f"Missing DOM id: {elem_id}")

    def test_bilingual_translations(self):
        """Verify bilingual translation keys exist in script."""
        for key in ["announcement_text", "nav_title", "hero_title", "stat_prodi_lbl", "modal_sec_quota", "modal_lbl_copy"]:
            self.assertIn(f'{key}:', self.html, f"Missing translation key {key} in index.html")


class TestZeroEmojiCompliance(unittest.TestCase):
    """Strictly assert zero emoji characters across repository files."""

    def test_no_emojis(self):
        files_to_check = [
            INDEX_HTML,
            README_MD,
            os.path.join(ROOT_DIR, "LICENSE"),
            os.path.join(DATA_DIR, "metadata.json"),
            os.path.join(DATA_DIR, "ui_prodi.json"),
            os.path.join(DATA_DIR, "ui_prodi.js"),
            os.path.join(DATA_DIR, "ui_prodi.csv"),
            os.path.join(ROOT_DIR, "scripts", "build_ui_dataset.py")
        ]
        for file_path in files_to_check:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            emoji_chars = [c for c in content if ord(c) in range(0x1F300, 0x1FAFF) or ord(c) in range(0x2600, 0x27BF)]
            self.assertEqual(len(emoji_chars), 0, f"Found emojis in {file_path}: {emoji_chars}")


if __name__ == "__main__":
    unittest.main()
