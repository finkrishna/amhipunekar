# AmhiPunekar — Architecture

## The Core Idea

AmhiPunekar is a **persona layer**, not a model. It sits on top of any capable LLM and transforms its output into Tatya's voice.

```
User Input
    ↓
[DataBank RAG] — retrieve relevant cultural entries
    ↓
[Tatya System Prompt] — persona + retrieved context injected
    ↓
[LLM Call] — Claude processes with full persona context
    ↓
Tatya's Response
    ↓
[Rating System] — 0-10 authenticity score, feedback collected
    ↓
[DataBank Improvement] — high-rated feedback feeds back in
```

## Three Layers

### Layer 1 — The Brain (LLM)
Claude handles factual accuracy, reasoning, and knowledge. We don't touch this. It's already excellent.

The key insight: **intelligence and personality are separable.** Claude knows what to say. Tatya knows how to say it.

### Layer 2 — The Tatya Skin (System Prompt)
`src/persona.py` contains the complete persona definition:
- Identity and backstory
- Voice and language register  
- Response length rules
- Signature rhetorical moves
- Cultural anchors and vocabulary
- The standard: "Haan. Exactly."

### Layer 3 — The DataBank (Cultural Memory)
`databank/master_databank.json` — 71 verified entries of authentic Puneri cultural material:
- Puneri Patya (signboards)
- P.L. Deshpande verified quotes
- Marathi proverbs (Mhani)
- Tilak and Agarkar journalism
- Contemporary Pune voice
- Vocabulary bank

Retrieved via keyword scoring at query time and injected into the system prompt. Tatya doesn't just approximate a Punekar — he draws from actual Puneri cultural artefacts.

## RAG Retrieval

Current implementation: simple keyword scoring.

```python
def retrieve(message, databank, top_k=3):
    # Score each entry by keyword overlap
    # Boost high-authenticity entries
    # Return top k most relevant
```

Future: vector embeddings for semantic similarity. For now, keyword matching is sufficient and fast.

## Conversation Memory

Current: in-memory dictionary keyed by `conversation_id`.
- Keeps last 10 messages per conversation
- Resets on server restart

Future (Phase 4): persistent storage with Redis or PostgreSQL.

## The Rating Feedback Loop

```
Response rated 0-10
    ↓
Score < 5: flag for system prompt review
Score 5-7: acceptable, continue
Score 8-9: strong, note patterns
Score 10: DataBank candidate — add feedback as new entry
    ↓
DataBank improves
    ↓
Tatya improves
```

This is human feedback driving improvement at the prompt and data layer — not weights, but the same spirit as RLHF.

## Phase Roadmap

| Phase | Architecture |
|-------|-------------|
| 1 (done) | Claude Project — persona in project instructions |
| 2 (current) | Flask API wrapper — this repo |
| 3 (planned) | Web app — proper frontend, persistent ratings |
| 4 (planned) | Memory layer — user history across sessions |
| 5 (future) | Kakku — female Punekar persona, same architecture |

## Adding Other Personas

The architecture is deliberately modular. To add a new persona (e.g., Kakku):

1. Create `src/kakku_persona.py` with her system prompt
2. Create `databank/kakku_databank.json` with her cultural entries
3. Add a `/kakku/chat` endpoint to `tatya.py`
4. Same RAG retrieval, different persona layer

The LLM layer doesn't change. Only the skin changes.
