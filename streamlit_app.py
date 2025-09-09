# app.py
import streamlit as st
from datetime import datetime
from textwrap import dedent

APP_NAME = "Generative AI Prompt Template Tool"
st.set_page_config(page_title=APP_NAME, page_icon="🤖", layout="wide")

st.title("🤖 Generative AI Prompt Template Tool")
st.caption("Build clear, safe, and effective prompts for support scenarios — ready to paste into your AI chat tool.")

with st.expander("Tips for best results", expanded=True):
    st.markdown(
        """
1. **Keep customer‑safe language**; avoid internal jargon or sensitive information. Use **placeholders** instead of private data (e.g., `<customer_name>`, `<account_id>`).
2. **Put all important information in the _Task_ field** — context, problem/issue description, relevant steps tried, timestamps, error codes, links to public docs. **Do not include sensitive data.**
3. **Make the goal explicit** — what you want the AI to do (e.g., draft reply, summarize issue, propose next steps, create KB draft).
        """
    )

st.divider()

# -------------------------
# Inputs
# -------------------------
col1, col2 = st.columns([1,1])

with col1:
    role = st.selectbox("Role", ["Customer support agent"], index=0,
                        help="The perspective the AI should take.")
    task = st.text_area(
        "Task (free text)",
        placeholder="Describe the situation, context, goal, and any relevant facts.\n"
                    "Avoid sensitive data. Include public links or placeholders.",
        height=200,
    )

with col2:
    output_format = st.selectbox(
        "Output format",
        ["Email", "Slack message", "Slack post", "Knowledge base article draft"],
        help="How you want the AI to structure the response."
    )

    tone = st.selectbox(
        "Tone",
        [
            "Professional and polite",
            "Polite and casual, colleague‑oriented",
            "Professional, friendly, and empathetic",
        ],
        help="Choose the voice appropriate for the audience and situation."
    )

    audience = st.selectbox(
        "Audience",
        ["Customer", "Other Manychat employee"],
        help="Who will receive the final content."
    )

st.divider()

# -------------------------
# Advanced options
# -------------------------
with st.expander("Advanced options (optional)"):
    lang = st.text_input("Preferred language (e.g., 'English', 'Turkish')", value="English")
    max_length = st.slider("Max length (approx. words)", 80, 800, 250, step=10)
    include_checklist = st.checkbox("Append review checklist for the agent", value=True)
    include_placeholders_block = st.checkbox("Include common placeholders block at top", value=True)
    include_safety = st.checkbox("Include safety & privacy reminders to the model", value=True)

# -------------------------
# Prompt builder
# -------------------------
def build_prompt(role, task, output_format, tone, audience, lang, max_length,
                 include_checklist, include_placeholders_block, include_safety):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    placeholders = dedent("""\
        <placeholders>
        - <customer_name>
        - <account_id>
        - <subscription_plan>
        - <ticket_id>
        - <order_id>
        - <error_code>
        - <public_doc_link>
        </placeholders>
    """)

    safety = dedent("""\
        Safety & Privacy:
        - Do not invent or expose internal data, pricing, roadmaps, or credentials.
        - If information is missing or sensitive, explicitly ask for a safe placeholder.
        - Follow customer‑safe language; avoid internal jargon.
    """)

    review = dedent("""\
        Review checklist (for the human agent before sending):
        - ✅ Accurate and consistent with known facts
        - ✅ No sensitive/internal information; placeholders used where needed
        - ✅ Tone matches audience and situation
        - ✅ Clear next steps or resolution path
        - ✅ Links are public and correct
    """)

    header_blocks = []
    if include_placeholders_block:
        header_blocks.append(placeholders)
    if include_safety:
        header_blocks.append(safety)

    header = "\n".join(header_blocks).strip()

    # Map output format to brief guidance
    fmt_guidance = {
        "Email": "Structure with greeting, brief context, solution/next steps, and closing signature.",
        "Slack message": "Keep it concise with bullet points and action items.",
        "Slack post": "Use a clear headline, summary, bullets, and action items for visibility.",
        "Knowledge base article draft": "Include title, summary, prerequisites, step‑by‑step instructions, and troubleshooting."
    }

    prompt_template = dedent(f"""
        You are acting as a **{role}**.
        Write in **{lang}** for the **{audience}**.
        Use a **{tone}** tone.
        Produce a **{output_format}**. Target length: ~{max_length} words.

        {f"{header}\n" if header else ""}
        Objective:
        - Based on the Task below, produce a clear, accurate, and helpful {output_format.lower()}.
        - {fmt_guidance[output_format]}

        Task (source information; may include placeholders; do not expose sensitive data):
        ---
        {task.strip() if task else "[Task not provided]"}
        ---

        Requirements:
        - Be self‑contained and easy to understand for the {audience.lower()}.
        - If data is missing, note assumptions and suggest what to request next.
        - Use customer‑safe language and avoid internal jargon.
        - Include step‑by‑step guidance or next actions when relevant.
        - Keep the structure scannable (short paragraphs, bullets).
        - Do not fabricate details.

        Output:
        - Write only the final {output_format.lower()} with no extra preamble.
    """).strip()

    if include_checklist:
        prompt_template += "\n\n" + review

    return prompt_template

prompt_text = build_prompt(role, task, output_format, tone, audience, lang, max_length,
                           include_checklist, include_placeholders_block, include_safety)

st.subheader("Generated prompt")
st.caption("Copy this prompt and paste it into your AI chat tool.")
st.code(prompt_text, language="markdown")

st.download_button(
    "Download prompt as .txt",
    data=prompt_text.encode("utf-8"),
    file_name="generated_prompt.txt",
    mime="text/plain"
)

st.divider()
st.markdown("Made with ❤️ using Streamlit.")
