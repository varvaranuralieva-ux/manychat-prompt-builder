import textwrap
placeholder=(
"Describe the situation clearly: context, issue, error codes, impacted customer(s), prior steps taken, "
"what you need the AI to produce, and any constraints (word count, brand name, links)."
),
(height=180,
)


# Format
_format = st.selectbox(
"Format",
["email", "Slack message", "Slack post", "knowledge base article draft"],
help="Choose how the AI should deliver the response.",
)


# Tone
_tone = st.selectbox(
"Tone",
[
"in a professional and polite tone",
"in a polite and casual colleague‑oriented tone",
"in a professional, friendly, and empathetic tone",
],
help="Select how the response should sound.",
)


# Audience
_audience = st.selectbox(
"Audience",
["customer", "other Manychat employee"],
help="Who will read the response?",
)


# Generate
st.divider()
if st.button("Generate Prompt", type="primary", use_container_width=True):
final_prompt = build_prompt(_task, _format, _tone, _audience)
st.session_state["final_prompt"] = final_prompt


# Preview & actions
final_prompt = st.session_state.get("final_prompt")
if final_prompt:
st.subheader("Your prompt")
st.text_area("", value=final_prompt, height=420, label_visibility="collapsed")


# Copy to clipboard
html(
f"""
<button id=\"copyBtn\" style=\"margin-top:10px;padding:8px 12px;border-radius:8px;border:1px solid #ddd;\">Copy to clipboard</button>
<script>
const btn = document.getElementById('copyBtn');
btn.addEventListener('click', async () => {{
const txt = `{final_prompt.replace('`', '\\`')}`;
try {{ await navigator.clipboard.writeText(txt); btn.textContent = 'Copied!'; }}
catch(e) {{ btn.textContent = 'Copy failed'; }}
}});
</script>
""",
height=60,
)


# Download as .txt
st.download_button(
"Download as .txt",
data=final_prompt,
file_name=f"generated_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
mime="text/plain",
use_container_width=True,
)


# Footer
st.markdown("\n")
st.caption("Built with Streamlit. Always review and edit the generated prompt to match the specific case and customer.")
