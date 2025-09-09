import textwrap
from datetime import datetime
import streamlit as st
from streamlit.components.v1 import html


st.set_page_config(
page_title="Generative AI Prompt Template Builder",
page_icon="🤖",
layout="centered",
)


# ---------- Helper: build the final prompt ----------


def build_prompt(task: str, output_format: str, tone: str, audience: str) -> str:
# Normalize blanks
task = (task or "").strip()


# Map human-readable format to an instruction
format_instructions = {
"email": "Write the response as a clear, well-structured email.",
"Slack message": "Write the response as a concise Slack message (1–5 short paragraphs, use bullets when helpful).",
"Slack post": "Write the response as a Slack post suitable for a channel announcement (title + short sections + bullet points).",
"knowledge base article draft": (
"Write the response as a knowledge base article draft (title, summary, prerequisites, step-by-step sections, and a short FAQ)."
),
}


tone_text = tone.strip() if tone else "in a professional and polite tone"


# Compose a structured, model-friendly prompt
prompt_sections = [
"ROLE:",
"You are a customer support agent.",
"",
"AUDIENCE:",
f"Write to the {audience.strip() if audience else 'customer'}.",
"",
"TASK:",
task if task else "<Describe the issue, error codes, context, history, previous attempts, and desired outcome>",
"",
"OUTPUT FORMAT:",
format_instructions.get(output_format, "Provide the response in a clear and readable format."),
"",
"TONE:",
f"Write {tone_text}.",
"",
"CONSTRAINTS & SAFETY:",
"- Use customer-safe language; avoid internal jargon or sensitive info.",
"- Replace private data with placeholders like <customer_name>, <ticket_id>, <order_number>.",
"- If critical details are missing, ask clarifying questions first in a short list.",
"- Be accurate, concise, and solution-oriented.",
"- Prefer plain language; avoid long, complex sentences.",
"",
"QUALITY CHECK BEFORE FINALIZING:",
"- Ensure the goal is explicit and the steps are actionable.",
"- Confirm the tone matches the audience and channel.",
"- Include next steps or links to relevant resources when appropriate.",
]


return "\n".join(prompt_sections).strip()




# ---------- UI ----------


st.title("Generative AI Prompt Template Builder")
st.caption("Create effective, safe prompts for support use-cases — fast.")


with st.expander("Tips for best results", expanded=True):
st.markdown(
"""
1. **Keep customer-safe language**; avoid internal jargon or sensitive information. Use placeholders instead of private data.
2. **Ensure all important info is in the _Task_ field** (context, issue description, error codes, account IDs, links, constraints, etc.).
3. **Make your goal explicit and specific** (what a great answer looks like, success criteria, and any limits like word count or format).
"""
)


st.subheader("Build your prompt")


# Fixed Role (shown for clarity)
st.text_input("Role", value="customer support agent", disabled=True, help="This tool is designed for support agents.")


# Task
_task = st.text_area(
"Task",
placeholder=(
"Describe the situation clearly: context, issue, error codes, impacted customer(s), prior steps taken, "
)
