#!/bin/bash
# AmhiPunekar — curl Examples
# Make sure tatya.py is running first: python src/tatya.py

BASE="http://localhost:5000"

echo "=== AmhiPunekar curl Examples ==="
echo ""

# ---- Health check ----
echo "1. Health check:"
curl -s "$BASE/health" | python3 -m json.tool
echo ""

# ---- Basic question ----
echo "2. Ask Tatya about the market:"
curl -s -X POST "$BASE/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Should I buy Nifty now or wait?"}' \
  | python3 -m json.tool
echo ""

# ---- With conversation ID ----
echo "3. Start a conversation (save the conversation_id for follow-up):"
RESPONSE=$(curl -s -X POST "$BASE/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What do you think of all these IPOs?"}')
echo $RESPONSE | python3 -m json.tool
CONV_ID=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['conversation_id'])")
echo ""

# ---- Follow-up question in same conversation ----
echo "4. Follow-up in same conversation:"
curl -s -X POST "$BASE/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"And what about gold?\", \"conversation_id\": \"$CONV_ID\"}" \
  | python3 -m json.tool
echo ""

# ---- Rating a response ----
echo "5. Rate a response:"
curl -s -X POST "$BASE/rate" \
  -H "Content-Type: application/json" \
  -d "{
    \"conversation_id\": \"$CONV_ID\",
    \"message_id\": \"test-123\",
    \"score\": 8,
    \"feedback\": \"Good but could be sharper on the historical reference\"
  }" \
  | python3 -m json.tool
echo ""

# ---- DataBank stats ----
echo "6. DataBank statistics:"
curl -s "$BASE/databank/stats" | python3 -m json.tool
echo ""

# ---- Lazy question (tests the roast) ----
echo "7. Lazy question — watch Tatya roast it:"
curl -s -X POST "$BASE/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Give me some good advice."}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"
echo ""

echo "=== Done ==="
