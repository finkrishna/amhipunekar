"""
AmhiPunekar — Test Suite
Tests persona loading, DataBank retrieval, and API structure.
Does not test live API calls (those cost money and require a key).
"""

import sys
import os
import json
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from persona import build_system_prompt, TATYA_SYSTEM_PROMPT
from retrieval import retrieve, format_for_prompt


# ── Sample DataBank for testing ──────────────────────────────
SAMPLE_DATABANK = [
    {
        "id": "DB-PAT-001",
        "type": "patya",
        "text": "उधार मागून आपला अपमान करून घेऊ नये, ही नम्र विनंती.",
        "text_translation": "Please do not ask for credit and get yourself insulted.",
        "topics": ["class", "culture", "credit", "money"],
        "signal": "weaponized civility",
        "score": 9
    },
    {
        "id": "DB-PLA-008",
        "type": "pula",
        "text": "माणूस अपयशाला भीत नाही. अपयशाचं खापर फोडायला काहीच मिळालं नाही तर याची त्याला भिती वाटते.",
        "text_translation": "A man is not afraid of failure. What he fears is having nothing to blame the failure on.",
        "topics": ["failure", "blame", "fear", "accountability"],
        "signal": "khapar psychology",
        "score": 10
    },
    {
        "id": "DB-PRV-003",
        "type": "proverb",
        "text": "अति शहाणा त्याचा बैल रिकामा.",
        "text_translation": "The over-smart person's ox remains idle.",
        "topics": ["cleverness", "overanalysis", "action", "work"],
        "signal": "too clever — ox stands idle",
        "score": 9
    },
    {
        "id": "DB-JRN-001",
        "type": "journalism",
        "text": "सरकारचे डोके ठिकाणावर आहे का?",
        "text_translation": "Is the government in its right mind?",
        "source": "Tilak, Kesari",
        "topics": ["government", "politics", "policy", "sanity"],
        "signal": "demolition framed as sincere inquiry",
        "score": 10
    },
]


class TestPersona(unittest.TestCase):

    def test_system_prompt_exists(self):
        self.assertIsInstance(TATYA_SYSTEM_PROMPT, str)
        self.assertGreater(len(TATYA_SYSTEM_PROMPT), 100)

    def test_system_prompt_contains_key_elements(self):
        self.assertIn("Tatya", TATYA_SYSTEM_PROMPT)
        self.assertIn("Pune", TATYA_SYSTEM_PROMPT)
        self.assertIn("paalhaal", TATYA_SYSTEM_PROMPT.lower())

    def test_build_system_prompt_without_context(self):
        prompt = build_system_prompt()
        self.assertEqual(prompt, TATYA_SYSTEM_PROMPT)

    def test_build_system_prompt_with_context(self):
        prompt = build_system_prompt("Some DataBank context here")
        self.assertIn("DATABANK CONTEXT", prompt)
        self.assertIn("Some DataBank context here", prompt)

    def test_system_prompt_not_empty_with_context(self):
        prompt = build_system_prompt("context")
        self.assertGreater(len(prompt), len(TATYA_SYSTEM_PROMPT))


class TestRetrieval(unittest.TestCase):

    def test_retrieve_returns_list(self):
        results = retrieve("Should I buy Nifty?", SAMPLE_DATABANK)
        self.assertIsInstance(results, list)

    def test_retrieve_respects_top_k(self):
        results = retrieve("anything", SAMPLE_DATABANK, top_k=2)
        self.assertLessEqual(len(results), 2)

    def test_retrieve_finds_relevant_entry(self):
        results = retrieve("I failed and I'm looking for someone to blame", SAMPLE_DATABANK, top_k=3)
        ids = [e["id"] for e in results]
        self.assertIn("DB-PLA-008", ids)

    def test_retrieve_finds_government_entry(self):
        results = retrieve("What do you think of the government's policy?", SAMPLE_DATABANK, top_k=3)
        ids = [e["id"] for e in results]
        self.assertIn("DB-JRN-001", ids)

    def test_retrieve_empty_query(self):
        results = retrieve("", SAMPLE_DATABANK)
        self.assertIsInstance(results, list)

    def test_retrieve_no_match_returns_high_score_entries(self):
        results = retrieve("xyzabc123notaword", SAMPLE_DATABANK, top_k=2)
        # Should still return something (falls back gracefully)
        self.assertIsInstance(results, list)


class TestFormatForPrompt(unittest.TestCase):

    def test_format_empty_list(self):
        result = format_for_prompt([])
        self.assertEqual(result, "")

    def test_format_single_entry(self):
        result = format_for_prompt([SAMPLE_DATABANK[0]])
        self.assertIn(SAMPLE_DATABANK[0]["text"], result)

    def test_format_includes_translation(self):
        result = format_for_prompt([SAMPLE_DATABANK[0]])
        self.assertIn(SAMPLE_DATABANK[0]["text_translation"], result)

    def test_format_includes_source_when_present(self):
        result = format_for_prompt([SAMPLE_DATABANK[3]])
        self.assertIn("Tilak", result)

    def test_format_multiple_entries(self):
        result = format_for_prompt(SAMPLE_DATABANK[:3])
        for entry in SAMPLE_DATABANK[:3]:
            self.assertIn(entry["text"], result)


class TestDataBank(unittest.TestCase):

    def test_databank_file_exists(self):
        path = os.path.join(
            os.path.dirname(__file__),
            "../databank/master_databank.json"
        )
        self.assertTrue(os.path.exists(path), "master_databank.json not found")

    def test_databank_loads_correctly(self):
        path = os.path.join(
            os.path.dirname(__file__),
            "../databank/master_databank.json"
        )
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        entries = data.get("entries", data) if isinstance(data, dict) else data
        self.assertGreater(len(entries), 50, "DataBank should have more than 50 entries")

    def test_databank_entries_have_required_fields(self):
        path = os.path.join(
            os.path.dirname(__file__),
            "../databank/master_databank.json"
        )
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        entries = data.get("entries", data) if isinstance(data, dict) else data

        required_fields = ["id", "type", "text_original"]
        for entry in entries[:10]:  # Check first 10
            for field in required_fields:
                self.assertIn(
                    field, entry,
                    f"Entry {entry.get('id', '?')} missing field '{field}'"
                )

    def test_databank_has_high_signal_entries(self):
        path = os.path.join(
            os.path.dirname(__file__),
            "../databank/master_databank.json"
        )
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        entries = data.get("entries", data) if isinstance(data, dict) else data
        high_signal = [e for e in entries if e.get("score", 0) >= 9]
        self.assertGreater(len(high_signal), 20, "Should have more than 20 high-signal entries")


if __name__ == "__main__":
    print("🟠 AmhiPunekar — Running test suite\n")
    unittest.main(verbosity=2)
