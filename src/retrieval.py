"""
AmhiPunekar — DataBank RAG Retrieval
Finds relevant cultural entries to inject into Tatya's context.
"""

import json
import os
from typing import List, Dict


def load_databank(path: str = None) -> List[Dict]:
    """Load the master DataBank from JSON."""
    if path is None:
        path = os.path.join(
            os.path.dirname(__file__), 
            "../databank/master_databank.json"
        )
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("entries", data) if isinstance(data, dict) else data


def retrieve(message: str, databank: List[Dict], top_k: int = 3) -> List[Dict]:
    """
    Simple keyword-based retrieval.
    Scores each entry by keyword overlap with user message.
    
    Args:
        message: User's input message
        databank: List of DataBank entries
        top_k: Number of entries to return
        
    Returns:
        Top k most relevant entries
    """
    msg_lower = message.lower()
    words = [w for w in msg_lower.split() if len(w) > 3]

    scored = []
    for entry in databank:
        score = 0
        
        # Build searchable text from entry
        searchable = " ".join([
            entry.get("text", ""),
            entry.get("text_translation", "") or "",
            entry.get("text_transliterated", "") or "",
            " ".join(entry.get("topics", [])),
            entry.get("signal", "") or "",
            entry.get("source", "") or "",
        ]).lower()

        # Score by keyword matches
        for word in words:
            if word in searchable:
                score += 2

        # Boost high-authenticity entries slightly
        score += (entry.get("score", 7) - 7) * 0.3

        if score > 0:
            scored.append((score, entry))

    # Sort by relevance, take top k
    scored.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in scored[:top_k]]


def format_for_prompt(entries: List[Dict]) -> str:
    """
    Format retrieved entries for injection into system prompt.
    
    Args:
        entries: List of DataBank entries
        
    Returns:
        Formatted string for system prompt injection
    """
    if not entries:
        return ""

    lines = ["Draw on these naturally if relevant — do not quote mechanically:\n"]
    for e in entries:
        entry_type = e.get("type", "entry").upper()
        text = e.get("text", "")
        translation = e.get("text_translation", "")
        source = e.get("source", "")
        signal = e.get("signal", "")

        line = f"[{entry_type}] \"{text}\""
        if translation:
            line += f"\n  → {translation}"
        if source:
            line += f"\n  — {source}"
        if signal:
            line += f"\n  Signal: {signal}"
        lines.append(line)

    return "\n\n".join(lines)


# ---- Quick test ----
if __name__ == "__main__":
    # Test without loading file — use inline sample
    sample = [
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
            "topics": ["cleverness", "overanalysis", "action"],
            "signal": "too clever — ox stands idle",
            "score": 9
        }
    ]
    
    results = retrieve("I keep analysing but never taking action", sample)
    print("Retrieved:", [e["id"] for e in results])
    print("\nFormatted context:")
    print(format_for_prompt(results))
