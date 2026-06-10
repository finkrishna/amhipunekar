# AmhiPunekar 🟠

> *"मी राहतो पुण्यात म्हणजे विद्वत्तेच्या ठाण्यात. बोलणे हा इथला धर्म आहे आणि ऐकणे हा दानधर्म आहे."*
> — P.L. Deshpande

**AmhiPunekar** is an open-source conversational AI persona layer called **PunerifyMe** — a system prompt + DataBank that transforms standard LLM output into responses delivered by **Tatya**, a tapri philosopher from Peth Pune.

Sharp. Sardonic. Intellectually uncompromising. Deeply culturally rooted. Not a caricature. The real thing.

---

## What This Is

A **persona layer** — not a new model, not a fine-tune. A carefully engineered system prompt + cultural DataBank that sits on top of any capable LLM (Claude, GPT-4, etc.) and transforms its output into Tatya's voice.

```
User Input
    ↓
[LLM Call] — factually correct base response
    ↓
[Tatya Skin] — system prompt + DataBank context injected
    ↓
Tatya's Response — sharp, Puneri, culturally rooted
```

---

## The Persona — Tatya

- Tapri philosopher, Narayan Peth, Pune
- No formal title. More wisdom than any PhD.
- Voracious reader — Marathi literature, history, economics, philosophy, world affairs
- Speaks English primarily, Marathi/Hindi dropped in naturally
- Default snark dial: **High demolition. Full. No prisoners.**
- Will roast bad/lazy questions before answering. Will always answer.
- Deep cultural references: PuLa Deshpande, Tilak, Agarkar, Peshwa history, Sinhagad, Chitale Bandhu, Puneri Patya

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/finkrishna/amhipunekar.git
cd amhipunekar
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API key

You need your own [Anthropic API key](https://platform.claude.com/) — Tatya runs on Claude.

```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

### 4. Run Tatya

```bash
cd src && python tatya.py
```

### 5. Talk to him

Open **http://localhost:5000** — chat UI with snark dial (Demolition / Khochak / Saumya) and a 0–10 authenticity rating under every reply.

Or via API:

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Should I buy Nifty now or wait?"}'
```

---

## Project Structure

```
amhipunekar/
├── README.md
├── LICENSE
├── .env.example
├── requirements.txt
├── src/
│   ├── tatya.py              ← Main Flask API server
│   ├── persona.py            ← Tatya system prompt + snark dial
│   └── retrieval.py          ← DataBank RAG retrieval
├── static/
│   └── index.html            ← Web chat UI (snark dial + ratings)
├── databank/
│   └── master_databank.json  ← 71 verified cultural entries
├── docs/
│   ├── ARCHITECTURE.md       ← How it works
│   └── DATABANK.md           ← DataBank schema + contribution guide
├── examples/
│   ├── python_example.py
│   └── curl_examples.sh
└── tests/
    └── test_tatya.py
```

---

## API Reference

### POST /chat

Send a message to Tatya.

**Request:**
```json
{
  "message": "Your question here",
  "conversation_id": "optional-session-id",
  "snark_level": "high"
}
```

**Response:**
```json
{
  "response": "Tatya's response",
  "databank_entries_used": ["DB-PAT-002", "DB-PLA-008"],
  "conversation_id": "session-id"
}
```

### POST /rate

Submit an authenticity rating for a response.

**Request:**
```json
{
  "conversation_id": "session-id",
  "message_id": "msg-id",
  "score": 8,
  "feedback": "How would Tatya actually say this?"
}
```

---

## The DataBank

The DataBank is the cultural soul of this project — 71 verified entries across:

| Type | Count | Examples |
|------|-------|---------|
| Puneri Patya | 21 | Shop signs, housing society notices |
| PuLa Deshpande | 13 | Verified quotes with source attribution |
| Proverbs (Mhani) | 8 | Marathi proverbs with Pune deployment context |
| Journalism | 4 | Tilak, Agarkar — the intellectual backbone |
| Vocabulary | 16 | Khochak, Tomna, Agau, TTMM, Ghanta |
| Contemporary | 5 | Reddit, social media — living Pune voice |
| Institutions | 3 | Chitale Bandhu, Balgandharva, ABC |

Every entry has:
- Authenticity score (0-10)
- Signal description (what makes it Puneri)
- Topic tags (for RAG retrieval)
- Verified source attribution

### Contributing to the DataBank

See [DATABANK.md](docs/DATABANK.md) for the contribution guide.

The standard is simple: a real Punekar from the old Peths reads your entry and says *"Haan. Exactly. This is us."*

---

## Tatya Rating System

Every response can be rated 0-10 for Puneri authenticity:

- **0** = "This is some Mumbai nonsense"
- **5** = "Theek aahe. Could be sharper."
- **10** = "Exactly. A real Punekar said this."

Ratings + feedback feed the DataBank improvement pipeline.

---

## Roadmap

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 0 | Founding document | ✅ Done |
| 1 | Tatya v0.1 — voice testing | ✅ Done |
| 1b | DataBank seed — 71 entries | ✅ Done |
| 2 | API wrapper — this repo | ✅ Done |
| 3 | Web app — snark dial + rating system | ✅ Done |
| 4 | Memory layer — persistent history | Planned |
| 5 | Kakku — female Punekar persona | Future |

---

## Model

Tatya currently runs on **Claude Fable 5** (`claude-fable-5`) — change `MODEL` in `src/tatya.py` to use a different Claude model. Conversation history is in-memory; restarting the server starts fresh.

---

## Contributing

Pull requests welcome. Please read [DATABANK.md](docs/DATABANK.md) before submitting DataBank entries.

For code contributions, open an issue first to discuss what you'd like to change.

**The only rule:** Tatya must remain Tatya. Not a caricature. Not a performance. The real thing.

---

## The Standard

A real Punekar reads Tatya's response and says:

*"Haan. Exactly. He would say exactly this."*

That is the only acceptable outcome.

---

## License

MIT License — code is free. DataBank entries carry their original attributions.

---

*AmhiPunekar — Pune's contribution to the AI persona layer.*
