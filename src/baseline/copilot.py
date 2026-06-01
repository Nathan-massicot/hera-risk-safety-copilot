"""
HERA Risk & Safety Copilot — Baseline Prototype
================================================
A conversational copilot that helps mHealth app developers identify
ethical and regulatory risks using the HERA taxonomy.

This prototype uses Ollama for local LLM inference and Gradio for the UI.

Setup:
    1. Install Ollama: https://ollama.com
    2. Pull a model: ollama pull mistral:7b-instruct-v0.3-q4_K_M
    3. pip install gradio requests
    4. python copilot.py
"""

import json
import os
import requests
import gradio as gr
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.environ.get("HERA_MODEL", "mistral:7b-instruct-v0.3-q4_K_M")

TAXONOMY_PATH = Path(__file__).parent.parent.parent / "data" / "taxonomy" / "hera_taxonomy.json"


def load_taxonomy() -> dict:
    """Load the HERA taxonomy from JSON."""
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_system_prompt(taxonomy: dict) -> str:
    """Build the system prompt that injects HERA knowledge into the model."""
    pillar_summaries = []
    for pillar in taxonomy["pillars"]:
        dims = ", ".join(d["name"] for d in pillar["dimensions"])
        pillar_summaries.append(
            f"**{pillar['id']} — {pillar['name']}** ({pillar['focus']}): {dims}"
        )
    pillars_text = "\n".join(pillar_summaries)

    # Build a compact reference of all reflection questions
    questions_ref = []
    for pillar in taxonomy["pillars"]:
        for dim in pillar["dimensions"]:
            qs = "; ".join(dim["reflection_questions"][:2])  # first 2 per dimension
            questions_ref.append(f"[{dim['id']}] {dim['name']}: {qs}")
    questions_text = "\n".join(questions_ref)

    return f"""You are the HERA Risk & Safety Copilot, an expert assistant that helps mHealth app developers identify ethical and regulatory risks.

## Your Knowledge Base: HERA Taxonomy
HERA (Health Ethical & Regulatory Assessment) is a structured taxonomy with 7 pillars and 38 dimensions, covering ALL mHealth apps (with or without AI).

### Pillars
{pillars_text}

### Reflection Questions Reference
{questions_text}

## Your Conversation Protocol
1. FIRST: Understand the app. Ask clarifying questions about: app type, purpose, target users, data collected, technology used, deployment markets.
2. THEN: Systematically explore relevant HERA pillars. For each relevant dimension:
   - Ask a specific, targeted reflection question (not generic)
   - Listen to the developer's answer
   - If a risk is identified: name it clearly, explain why it matters, suggest a concrete mitigation
   - If the answer is satisfactory: acknowledge it and move on
3. PRIORITIZE: Start with the highest-risk dimensions for this specific app type.
4. BE SPECIFIC: Reference the exact HERA dimension ID (e.g., [P1.D3]) when discussing risks.
5. AT THE END: When the developer says they're done or you've covered the key dimensions, produce a structured risk report.

## Your Tone
- Professional but approachable — you're a helpful colleague, not an auditor
- Be direct about risks — don't sugarcoat safety issues
- Acknowledge good practices when you see them
- Use concrete examples relevant to their specific app

## Important Rules
- Every pillar can apply to non-AI apps. A medication reminder has autonomy, privacy, and reliability risks without any AI.
- Always cite regulatory frameworks when relevant (GDPR, MDR, EU AI Act, ISO 82304-2).
- If the app might be a Software as a Medical Device (SaMD), flag this early — it changes everything.
- Don't ask more than 1-2 questions per message. Keep the conversation flowing naturally."""


# ---------------------------------------------------------------------------
# Ollama interaction
# ---------------------------------------------------------------------------

def check_ollama() -> tuple[bool, str]:
    """Check if Ollama is running and the model is available."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if r.status_code == 200:
            models = [m["name"] for m in r.json().get("models", [])]
            if any(MODEL_NAME.split(":")[0] in m for m in models):
                return True, f"Connected to Ollama. Model: {MODEL_NAME}"
            available = ", ".join(models[:5]) if models else "none"
            return False, (
                f"Ollama is running but model '{MODEL_NAME}' not found. "
                f"Available: {available}. "
                f"Run: ollama pull {MODEL_NAME}"
            )
        return False, f"Ollama returned status {r.status_code}"
    except requests.ConnectionError:
        return False, (
            "Cannot connect to Ollama. "
            "Install from https://ollama.com and run: ollama serve"
        )


def chat_with_ollama(
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> str:
    """Send a chat request to Ollama and return the response."""
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["message"]["content"]
    except requests.ConnectionError:
        return "Error: Cannot connect to Ollama. Is it running? (ollama serve)"
    except requests.Timeout:
        return "Error: Ollama request timed out. The model may be loading."
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

def create_app() -> gr.Blocks:
    """Create the Gradio application."""
    taxonomy = load_taxonomy()
    system_prompt = build_system_prompt(taxonomy)

    # Count dimensions for display
    total_dims = sum(len(p["dimensions"]) for p in taxonomy["pillars"])
    pillar_names = [f"{p['id']}: {p['name']}" for p in taxonomy["pillars"]]

    with gr.Blocks(
        title="HERA Risk & Safety Copilot",
    ) as app:
        # State
        chat_history = gr.State([])

        # Header
        gr.Markdown(
            """
            # HERA Risk & Safety Copilot
            **Health Ethical & Regulatory Assessment for mHealth Applications**

            Describe your mHealth app and I'll guide you through a structured
            risk assessment covering patient safety, data privacy, autonomy,
            quality, transparency, equity, and regulatory compliance.
            """,
            elem_classes="header",
        )

        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=520,
                    buttons=["copy", "copy_all"],
                )
                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="Describe your mHealth app or answer the copilot's question...",
                        label="Your message",
                        scale=5,
                        lines=2,
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1)

                with gr.Row():
                    clear_btn = gr.Button("New conversation", variant="secondary")
                    report_btn = gr.Button("Generate risk report", variant="secondary")

            with gr.Column(scale=1):
                gr.Markdown("### HERA Taxonomy")
                gr.Markdown(
                    f"**{len(taxonomy['pillars'])} pillars, {total_dims} dimensions**"
                )
                for p in taxonomy["pillars"]:
                    dim_count = len(p["dimensions"])
                    gr.Markdown(
                        f"<span class='pillar-badge'>{p['id']}: {p['name']} ({dim_count})</span>",
                    )
                gr.Markdown("---")
                gr.Markdown("### Status")
                status_display = gr.Markdown("Ready. Describe your app to begin.")

                gr.Markdown("---")
                gr.Markdown("### Model")
                ollama_ok, ollama_msg = check_ollama()
                status_icon = "🟢" if ollama_ok else "🔴"
                gr.Markdown(f"{status_icon} {ollama_msg}")

        # --- Event handlers ---

        def respond(user_message: str, history: list) -> tuple:
            if not user_message.strip():
                return "", history, history, "Waiting for your message..."

            # Build messages for Ollama
            messages = [{"role": "system", "content": system_prompt}]
            for entry in history:
                messages.append(entry)
            messages.append({"role": "user", "content": user_message})

            # Get response
            assistant_response = chat_with_ollama(messages)

            # Update history
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": assistant_response})

            # Count turns for status
            user_turns = sum(1 for m in history if m["role"] == "user")
            status = f"Turn {user_turns} — Conversation in progress..."

            return "", history, history, status

        def generate_report(history: list) -> tuple:
            if not history:
                return history, history, "No conversation to generate report from."

            report_prompt = (
                "Based on our entire conversation, produce a structured HERA Risk Report. "
                "Format it as follows:\n\n"
                "# HERA Risk Assessment Report\n"
                "## App Summary\n"
                "[Brief description of the app]\n\n"
                "## Identified Risks\n"
                "For each risk found, list:\n"
                "- **HERA Dimension**: [ID and name]\n"
                "- **Risk**: [Description]\n"
                "- **Severity**: [High/Medium/Low]\n"
                "- **Mitigation**: [Recommended action]\n\n"
                "## Positive Practices\n"
                "[What the developer is already doing well]\n\n"
                "## Recommended Next Steps\n"
                "[Priority actions]\n\n"
                "## Dimensions Not Yet Explored\n"
                "[HERA dimensions that were not covered and may need review]"
            )

            messages = [{"role": "system", "content": system_prompt}]
            for entry in history:
                messages.append(entry)
            messages.append({"role": "user", "content": report_prompt})

            report = chat_with_ollama(messages, max_tokens=2048)

            history.append({"role": "user", "content": "[Requested risk report]"})
            history.append({"role": "assistant", "content": report})

            return history, history, "Risk report generated."

        def clear_chat() -> tuple:
            return [], [], "Ready. Describe your app to begin."

        # Wire events
        send_btn.click(
            respond,
            inputs=[msg_input, chat_history],
            outputs=[msg_input, chatbot, chat_history, status_display],
        )
        msg_input.submit(
            respond,
            inputs=[msg_input, chat_history],
            outputs=[msg_input, chatbot, chat_history, status_display],
        )
        report_btn.click(
            generate_report,
            inputs=[chat_history],
            outputs=[chatbot, chat_history, status_display],
        )
        clear_btn.click(
            clear_chat,
            outputs=[chatbot, chat_history, status_display],
        )

    return app


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point for the HERA copilot (used by `uv run hera-copilot`)."""
    print("=" * 60)
    print("HERA Risk & Safety Copilot — Baseline Prototype")
    print("=" * 60)

    ok, msg = check_ollama()
    print(f"Ollama status: {msg}")
    if not ok:
        print(
            f"\nTo get started:\n"
            f"  1. Install Ollama: https://ollama.com\n"
            f"  2. Run: ollama pull {MODEL_NAME}\n"
            f"  3. Run: ollama serve\n"
            f"  4. Then restart this script.\n"
        )

    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        theme=gr.themes.Soft(primary_hue="blue"),
        css="""
        .header { text-align: center; margin-bottom: 1rem; }
        .pillar-badge {
            display: inline-block; padding: 4px 10px; margin: 2px;
            border-radius: 12px; font-size: 0.85rem;
            background: #e8f4f8; color: #1a5276;
        }
        """,
    )


if __name__ == "__main__":
    main()
