import streamlit as st
from datetime import date

st.set_page_config(page_title="Manychat Prompt Builder", page_icon="✨", layout="wide")

# ------------------------------
# Presets tailored for Manychat
# ------------------------------
PRESETS = {
    "Troubleshoot WABA onboarding": {
        "role": "as a product specialist for WhatsApp (WABA)",
        "tone": "in a calm and reassuring tone",
        "audience": "customer",
        "format": "numbered action steps",
        "task": (
            "Help a customer connect their WhatsApp Business Account to Manychat and resolve common onboarding "
            "blockers (e.g., missing Business Verification, mismatched display name, phone number not eligible)."
        ),
        "extra": (
            "Policy: follow Meta's WABA policies. Provide links as placeholder text like [link]. "
            "Ask for exact error messages and screenshots. Offer safe, reversible steps only."
        ),
    },
    "Billing & refund reply": {
        "role": "as a billing & subscriptions specialist",
        "tone": "in a professional tone",
        "audience": "customer",
        "format": "short email reply",
        "task": (
            "Draft a polite email responding to a refund request for a recent upgrade that the customer didn't intend."
        ),
        "extra": (
            "Explain eligibility, proration, and next steps. Do not confirm a refund unless within policy. "
            "Include placeholders for order ID and date."
        ),
    },
    "Bug escalation to Engineering": {
        "role": "as a technical support engineer",
        "tone": "in a concise and direct tone",
        "audience": "engineering team",
        "format": "SOP checklist",
        "task": (
            "Prepare a minimal, reproducible bug report for a flow failing to send WhatsApp messages after a recent template update."
        ),
        "extra": (
            "Include: environment, steps to reproduce, expected vs actual, logs/timeframes, user impact, severity, rollbacks/workarounds."
        ),
    },
}

ROLE_OPTIONS = [
    "as an experienced Manychat support agent",
    "as a customer using WhatsApp Business via Manychat",
    "as a product specialist for WhatsApp (WABA)",
    "as a billing & subscriptions specialist",
    "as a technical support engineer",
]

FORMAT_OPTIONS = [
    "numbered action steps",
    "bullet points",
    "short email reply",
    "chat-style response",
    "troubleshooting decision tree",
    "knowledge base article draft",
    "SOP checklist",
]

TONE_OPTIONS = [
    "in a professional tone",
    "in a friendly and empathetic tone",
    "in a concise and direct tone",
    "in a calm and reassuring tone",
    "in a neutral, policy-aligned tone",
]

AUDIENCE_OPTIONS = [
    "customer",
    "prospective customer",
    "Manychat employee",
    "fellow support agent",
    "engineering team",
    "partner (Meta/agency)",
]

SCOPE_TYPES = ["No time scope", "Date range", "Last N days"]

# ------------------------------
# Sidebar
# ------------------------------
with st.sidebar:
    st.title("✨ Prompt Builder")
    st.caption("Design precise prompts for customer support and internal comms.")

    preset = st.selectbox("Quick preset", ["(None)"] + list(PRESETS.keys()))
    st.markdown("---")
    st.subheader("Options")
    quality_bar = st.toggle("Include quality bar", value=True)
    ref_sources = st.toggle("Allow reference placeholders", value=True)
    placeholders = st.toggle("Use ID placeholders", value=True)

# Load preset values
if "state" not in st.session_state:
    st.session_state.state = {}

if preset != "(None)":
    p = PRESETS[preset]
    st.session_state.state.update(
        role=p["role"], tone=p["tone"], audience=p["audience"], format=p["format"], task=p["task"], extra=p["extra"]
    )

# ------------------------------
# Main layout
# ------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Basics")
    role = st.selectbox("Role", ROLE_OPTIONS, index=ROLE_OPTIONS.index(st.session_state.state.get("role", ROLE_OPTIONS[0])))
    audience = st.selectbox(
        "Audience", AUDIENCE_OPTIONS, index=AUDIENCE_OPTIONS.index(st.session_state.state.get("audience", AUDIENCE_OPTIONS[0]))
    )
    tone = st.selectbox("Tone", TONE_OPTIONS, index=TONE_OPTIONS.index(st.session_state.state.get("tone", TONE_OPTIONS[1])))
    fmt = st.selectbox(
        "Format", FORMAT_OPTIONS, index=FORMAT_OPTIONS.index(st.session_state.state.get("format", FORMAT_OPTIONS[0]))
    )
    task = st.text_area(
        "Task",
        st.session_state.state.get(
            "task",
            "Diagnose and resolve a customer's issue with WhatsApp template approval not showing up inside Manychat.",
        ),
        height=120,
    )

    st.subheader("Scope & constraints")
    scope_type = st.radio("Scope", SCOPE_TYPES, horizontal=True)
    scope_text = ""
    if scope_type == "Date range":
        c1, c2 = st.columns(2)
        with c1:
            start = st.date_input("Start date", value=date.today())
        with c2:
            end = st.date_input("End date", value=date.today())
        scope_text = f"Within the timeframe {start.isoformat()} to {end.isoformat()}."
    elif scope_type == "Last N days":
        n = st.number_input("Last N days", min_value=1, value=14)
        scope_text = f"Focus on events from the last {int(n)} days."

    extra = st.text_area(
        "Any additional information",
        st.session_state.state.get(
            "extra",
            """
Product context: Manychat with WhatsApp (WABA).
User context: SMB marketer with limited technical background.
Constraints: Follow Meta and Manychat policies; avoid exposing internal-only details.
Ask for: affected workspace, relevant template name, phone number, exact error text, screenshots, and timestamps in UTC.
If troubleshooting, provide reversible steps and warn about possible side-effects.
            """.strip(),
        ),
        height=160,
    )

with col2:
    st.header("Generated prompt")

    parts = []
    parts.append(f"Act {role}. Write for the {audience} {tone}.")
    if scope_text:
        parts.append(scope_text)
    parts.append(f"Task: {task}")
    parts.append(f"Preferred format: {fmt}.")

    if extra.strip():
        parts.append("Additional context:\n" + extra.strip())

    if quality_bar:
        parts.append(
            """
Quality bar:
- Be accurate and policy-aligned; never guess customer-specific data.
- Provide clear next steps and highlight irreversible actions.
- Flag when additional data is required and list exactly what is needed.
- Prefer structured outputs (lists, tables, checklists) to speed execution.
            """.strip()
        )

    if ref_sources:
        parts.append(
            """
If relevant, reference official documentation with short titles and placeholder links like [Manychat Help Center] or [Meta Business Help Center].
Do not fabricate links or private/internal URLs.
            """.strip()
        )

    if placeholders:
        parts.append(
            """
Use placeholders for sensitive identifiers, e.g., {workspace_id}, {waba_id}, {template_name}, {phone_number}, {order_id}.
            """.strip()
        )

    parts.append(
        """
Output requirements:
- Provide a complete answer. If information is missing, clearly list the exact questions to ask the user to proceed.
- Keep reasoning brief and user-facing; do not include hidden deliberation steps.
- End with a short checklist of next actions (who does what, by when).
        """.strip()
    )

    prompt_text = "\n\n".join(parts)

    st.text_area("Copy-ready prompt", prompt_text, height=420)
    st.download_button("Download .txt", data=prompt_text.encode("utf-8"), file_name="manychat-prompt.txt")

    st.markdown("---")
    st.subheader("Tips for best results")
    st.markdown(
        """
- Be specific with product areas (e.g., “WhatsApp Template messages”, “Partner-initiated WABA creation”).
- Mention exact error texts, timestamps (UTC), and the user's goal in one sentence.
- Choose a structured format (action steps / checklist) when you need speed and clarity.
- Keep customer-safe language; avoid internal jargon. Add placeholders instead of private data.
        """
    )

st.caption("Built for Manychat support workflows. Paste the prompt into your preferred AI chat tool.")
