"""
AmhiPunekar — Python Example
Direct Python usage without the Flask server.
"""

import os
import anthropic
from dotenv import load_dotenv
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from persona import build_system_prompt
from retrieval import load_databank, retrieve, format_for_prompt

load_dotenv()


def ask_tatya(message: str, history: list = None) -> str:
    """
    Ask Tatya a question directly.
    
    Args:
        message: Your question
        history: Optional conversation history
        
    Returns:
        Tatya's response
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    databank = load_databank()
    
    # Retrieve relevant context
    context_entries = retrieve(message, databank)
    context_str = format_for_prompt(context_entries)
    system_prompt = build_system_prompt(context_str)
    
    # Build messages
    messages = history or []
    messages = messages + [{"role": "user", "content": message}]
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=720,
        system=system_prompt,
        messages=messages
    )
    
    return response.content[0].text


def chat_session():
    """Interactive chat session with Tatya."""
    print("\n🟠 AmhiPunekar — Tatya")
    print("   Tapri Philosopher, Narayan Peth, Pune")
    print("   Type 'quit' to exit\n")
    print("-" * 50)
    print("Tatya: Arre, kay? Ask.")
    print("-" * 50 + "\n")
    
    history = []
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ("quit", "exit", "bye"):
            print("\nTatya: Theek aahe. Go.")
            break
            
        if not user_input:
            continue
        
        print("\nTatya: ", end="", flush=True)
        reply = ask_tatya(user_input, history)
        print(reply)
        print()
        
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": reply})
        
        # Keep history manageable
        if len(history) > 10:
            history = history[-10:]


if __name__ == "__main__":
    chat_session()
