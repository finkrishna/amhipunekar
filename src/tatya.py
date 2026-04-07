"""
AmhiPunekar — Tatya API Server
A simple Flask wrapper that serves Tatya's voice via HTTP.

Usage:
    python src/tatya.py

Then:
    curl -X POST http://localhost:5000/chat \
      -H "Content-Type: application/json" \
      -d '{"message": "Should I buy Nifty now or wait?"}'
"""

import os
import uuid
import json
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import anthropic

from persona import build_system_prompt
from retrieval import load_databank, retrieve, format_for_prompt

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Load DataBank once at startup
try:
    DATABANK = load_databank()
    print(f"✓ DataBank loaded: {len(DATABANK)} entries")
except FileNotFoundError:
    print("⚠ DataBank not found — running without cultural context")
    DATABANK = []

# In-memory conversation store
# Replace with Redis or a database for production
conversations = {}

# In-memory ratings store
ratings_store = []


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "project": "AmhiPunekar",
        "persona": "Tatya — Tapri Philosopher, Narayan Peth, Pune",
        "version": "0.2",
        "databank_entries": len(DATABANK),
        "endpoints": {
            "POST /chat": "Send a message to Tatya",
            "POST /rate": "Rate a response for Puneri authenticity",
            "GET /databank/stats": "DataBank statistics",
            "GET /health": "Health check"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "theek aahe", "databank": len(DATABANK)})


@app.route("/chat", methods=["POST"])
def chat():
    """
    Send a message to Tatya.
    
    Request body:
        message (str): Required. The user's message.
        conversation_id (str): Optional. Pass to maintain conversation history.
        snark_level (str): Optional. "high" (default), "medium", "low"
        
    Returns:
        response (str): Tatya's response
        conversation_id (str): For maintaining conversation continuity
        databank_entries_used (list): Which entries were retrieved
        message_id (str): For rating this specific response
    """
    data = request.get_json()
    
    if not data or "message" not in data:
        return jsonify({"error": "Field 'message' is required"}), 400
    
    message = data["message"].strip()
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Get or create conversation
    conversation_id = data.get("conversation_id") or str(uuid.uuid4())
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    history = conversations[conversation_id]

    # Retrieve relevant DataBank context
    context_entries = retrieve(message, DATABANK, top_k=3)
    context_str = format_for_prompt(context_entries)

    # Build system prompt
    system_prompt = build_system_prompt(context_str)

    # Add user message to history
    history.append({"role": "user", "content": message})

    # Keep last 10 messages to prevent token bloat
    recent_history = history[-10:]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=720,
            system=system_prompt,
            messages=recent_history
        )
        
        reply = response.content[0].text
        
        # Add assistant response to history
        history.append({"role": "assistant", "content": reply})
        conversations[conversation_id] = history

        message_id = str(uuid.uuid4())

        return jsonify({
            "response": reply,
            "conversation_id": conversation_id,
            "message_id": message_id,
            "databank_entries_used": [e["id"] for e in context_entries],
            "tokens_used": {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens
            }
        })

    except anthropic.APIError as e:
        return jsonify({"error": f"API error: {str(e)}"}), 500


@app.route("/rate", methods=["POST"])
def rate():
    """
    Submit a Puneri authenticity rating for a response.
    
    Rating scale:
        0  = Mumbai nonsense
        5  = Theek aahe, could be sharper
        10 = Exactly what a real Punekar would say
    
    Request body:
        conversation_id (str): Required
        message_id (str): Required
        score (int): Required. 0-10.
        feedback (str): Optional. "How would Tatya actually say this?"
    """
    data = request.get_json()
    
    required = ["conversation_id", "message_id", "score"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Field '{field}' is required"}), 400

    score = data["score"]
    if not isinstance(score, int) or score < 0 or score > 10:
        return jsonify({"error": "Score must be an integer 0-10"}), 400

    rating = {
        "conversation_id": data["conversation_id"],
        "message_id": data["message_id"],
        "score": score,
        "feedback": data.get("feedback", ""),
        "timestamp": datetime.utcnow().isoformat()
    }
    ratings_store.append(rating)

    # Verdict
    if score >= 8:
        verdict = "Nakki Puneri. DataBank material."
    elif score >= 5:
        verdict = "Theek aahe. Usable."
    else:
        verdict = "Mumbai nonsense. Needs work."

    return jsonify({
        "received": True,
        "verdict": verdict,
        "score": score
    })


@app.route("/databank/stats", methods=["GET"])
def databank_stats():
    """Return DataBank statistics."""
    if not DATABANK:
        return jsonify({"error": "DataBank not loaded"}), 500

    by_type = {}
    by_score = {"10": 0, "9": 0, "8": 0, "7": 0, "below_7": 0}

    for entry in DATABANK:
        t = entry.get("type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1

        s = entry.get("score", 0)
        if s == 10:
            by_score["10"] += 1
        elif s == 9:
            by_score["9"] += 1
        elif s == 8:
            by_score["8"] += 1
        elif s == 7:
            by_score["7"] += 1
        else:
            by_score["below_7"] += 1

    return jsonify({
        "total_entries": len(DATABANK),
        "high_signal_9_plus": by_score["9"] + by_score["10"],
        "perfect_10s": by_score["10"],
        "by_type": by_type,
        "by_score": by_score,
        "ratings_collected": len(ratings_store)
    })


if __name__ == "__main__":
    print("\n🟠 AmhiPunekar — Tatya is waking up...")
    print(f"   DataBank: {len(DATABANK)} entries loaded")
    print(f"   Model: claude-sonnet-4-20250514")
    print(f"   Running on: http://localhost:5000")
    print("\n   Tatya is ready. Try not to embarrass yourself.\n")
    app.run(debug=True, port=5000)
