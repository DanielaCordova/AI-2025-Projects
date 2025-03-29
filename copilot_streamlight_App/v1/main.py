import streamlit as st
import subprocess
import openai
import os
import pyperclip
from datetime import datetime
import re
import json

# === CONFIGURATION ===
st.set_page_config(page_title="🧠 Mini Copilot", layout="centered")

st.title("💻 Your Mini AI Code Copilot")
st.markdown("Type code and let your selected model autocomplete it ✨")

# --- Session Load/Save ---
saved_sessions_path = "saved_sessions"
os.makedirs(saved_sessions_path, exist_ok=True)

load_session = st.sidebar.selectbox("📂 Load previous session:", ["None"] + os.listdir(saved_sessions_path))
if load_session != "None":
    with open(os.path.join(saved_sessions_path, load_session), "r", encoding="utf-8") as f:
        saved_data = json.load(f)
        st.session_state["completion"] = saved_data["completion"]
        user_code = saved_data["user_code"]
        st.session_state["language"] = saved_data.get("language", "python")
        st.session_state["model_mode"] = saved_data.get("model_mode", "Ollama (local)")
        st.session_state["ollama_model"] = saved_data.get("ollama_model", "codellama")
else:
    user_code = ""

# --- Model Selector ---
model_mode = st.selectbox("Choose model backend:", ["Ollama (local)", "OpenAI GPT-4"])
ollama_model = None
if model_mode == "Ollama (local)":
    ollama_model = st.selectbox("Choose Ollama model:", ["codellama", "deepseek-coder", "codegemma"])

# --- Advanced settings ---
temperature = st.slider("Model creativity (temperature):", 0.0, 1.0, 0.3, 0.1)
language = st.selectbox("Code language:", ["python", "javascript", "java", "sql"])

def get_ollama_completion(prompt, model="codellama"):
    try:
        full_prompt = f"""Complete the following {language} code:

{prompt}

### Completion:
"""
        result = subprocess.run(
            ["ollama", "run", model],
            input=full_prompt.encode(),
            capture_output=True,
            timeout=180
        )
        output = result.stdout.decode().strip()
        if not output:
            output = result.stderr.decode().strip()
        return output or "[No output returned by model]"
    except subprocess.TimeoutExpired:
        return "[Error: Ollama model timed out. Try again or use a shorter prompt.]"
    except Exception as e:
        return f"[Error running Ollama model: {e}]"

def get_openai_completion(prompt):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            return "[OPENAI_API_KEY not set in environment variables.]"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are an expert {language} developer that autocompletes code."},
                {"role": "user", "content": f"Complete this code:\n{prompt}"}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error calling OpenAI API: {e}]"

def generate_autotest(code_snippet):
    test_prompt = f"""Write unit tests for the following {language} function:

{code_snippet}

Include only the test code."""
    if model_mode == "OpenAI GPT-4":
        return get_openai_completion(test_prompt)
    elif model_mode == "Ollama (local)" and ollama_model:
        return get_ollama_completion(test_prompt, model=ollama_model)
    else:
        return "[Cannot generate test: No valid model selected]"

def check_code_style(code_snippet):
    issues = []
    if ";" in code_snippet and language == "python":
        issues.append("Avoid using semicolons in Python code.")
    if len(code_snippet.splitlines()) > 20:
        issues.append("Consider breaking the function into smaller parts for readability.")
    return issues or ["No major style issues detected."]

# --- Input Code Area ---
user_code = st.text_area("✍️ Start writing your code:", value=user_code, height=300, placeholder="def fibonacci(n):\n    if n <= 1:")

# --- Button to Autocomplete ---
if st.button("🚀 Autocomplete Code") and user_code.strip():
    with st.spinner("Thinking..."):
        if model_mode == "Ollama (local)" and ollama_model:
            st.session_state["completion"] = get_ollama_completion(user_code, model=ollama_model)
        elif model_mode == "OpenAI GPT-4":
            st.session_state["completion"] = get_openai_completion(user_code)
        else:
            st.session_state["completion"] = "[Unsupported model mode or model not selected]"

# --- Display Completion (if exists) ---
if "completion" in st.session_state:
    response = st.session_state["completion"]
    st.subheader("🤖 Suggested Completion:")
    st.code(response, language=language)

    # --- Clipboard Copy ---
    if st.button("📋 Copy to clipboard"):
        try:
            pyperclip.copy(response)
            st.success("Copied to clipboard!")
        except Exception:
            st.warning("Clipboard copy not supported in this environment.")

    # --- Export to File ---
    file_format = st.radio("Export format:", [".py", ".md"], horizontal=True)
    if st.button("💾 Save to file"):
        filename = f"completion_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_format}"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response)
        st.success(f"Saved as {filename}")

    # --- Save Full Session ---
    if st.button("📥 Save Full Session"):
        session_filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        session_data = {
            "user_code": user_code,
            "completion": response,
            "language": language,
            "model_mode": model_mode,
            "ollama_model": ollama_model
        }
        with open(os.path.join(saved_sessions_path, session_filename), "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2)
        st.success(f"Session saved as {session_filename}")

    # --- Autotest Generator ---
    if st.button("🧪 Generate Unit Tests"):
        with st.spinner("Generating tests..."):
            tests = generate_autotest(user_code)
            st.subheader("🧪 Suggested Unit Tests:")
            st.code(tests, language=language)

    # --- Code Style Checker ---
    if st.button("🧱 Check Code Style"):
        issues = check_code_style(user_code)
        st.subheader("🧱 Style Feedback:")
        for issue in issues:
            st.markdown(f"- {issue}")

# --- Business-Ready Features (Implemented) ---
st.markdown("---")
st.markdown("### ✅ Company Features Now Available:")
st.markdown("- 💾 Export completions to .py or .md file")
st.markdown("- 📋 Clipboard copy button for suggestions")
st.markdown("- 🧠 Multiple language support (Python, JS, Java, SQL)")
st.markdown("- 🧪 Autotest generator from input code")
st.markdown("- 🧱 Code style feedback tool")
st.markdown("- 📊 Token usage (OpenAI) – Coming Soon")
st.markdown("- 📂 Load/save previous sessions with code + response")
