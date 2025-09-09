# Generative AI Prompt Template Tool

A simple Streamlit app that helps customer support agents compose **clear, safe, and effective prompts** for AI chat tools.

## Features
- Role (fixed: **Customer support agent**)
- Free‑text **Task** field
- **Output format** dropdown: Email, Slack message, Slack post, Knowledge base article draft
- **Tone** dropdown
- **Audience** dropdown
- Optional **Advanced** controls (language, max length, review checklist, safety reminders)
- Built‑in **Tips for best results**
- One‑click **download** of the generated prompt

## Quickstart

### 1) Clone and install
```bash
git clone https://github.com/your-org/prompt-template-tool.git
cd prompt-template-tool
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run
```bash
streamlit run app.py
```

The app will open in your browser (usually http://localhost:8501).

## Deploy on Streamlit Community Cloud
1. Push this folder to a public GitHub repository.
2. Go to Streamlit Community Cloud and choose **Deploy an app**.
3. Point it at your repo and set the **main file** to `app.py`.
4. Click **Deploy**.

## Tips for best results
1. **Keep customer‑safe language**; avoid internal jargon or sensitive information. Use **placeholders** instead of private data (e.g., `<customer_name>`, `<account_id>`).
2. **Ensure all important information is in the _Task_ field** (context, issue description, error codes, relevant public links). Do **not** include sensitive data.
3. **Make your goal clear** (e.g., “draft a reply that apologizes, summarizes the issue, and proposes next steps”).

## License
MIT
