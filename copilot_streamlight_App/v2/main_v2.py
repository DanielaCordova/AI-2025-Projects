import streamlit as st
import subprocess
import openai
import os
import pyperclip
from datetime import datetime
import re
import json
import git
from git import Repo, InvalidGitRepositoryError

# === FIX GIT ENV FOR WINDOWS ===
os.environ['GIT_PYTHON_REFRESH'] = 'quiet'
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = r'C:\Program Files\Git\bin\git.exe'

# === CONFIGURATION ===
st.set_page_config(page_title="🧠 Mini Copilot", layout="wide")

st.title("💻 Your Mini AI Code Copilot")

# --- Tabs ---
tabs = st.tabs(["✍️ Code Completion", "💬 Chat Assistant"])

# === SESSION MANAGEMENT ===
saved_sessions_path = "saved_sessions"
os.makedirs(saved_sessions_path, exist_ok=True)

# === GIT HELPER ===
def auto_commit_changes(commit_message="Auto-commit from Mini Copilot"):
    try:
        repo = Repo(".")
        if repo.is_dirty():
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            return True, "Changes committed successfully."
        else:
            return False, "No changes to commit."
    except InvalidGitRepositoryError:
        return False, "This folder is not a Git repository."
    except Exception as e:
        return False, f"Git error: {e}"

# === COMMON SETTINGS ===
model_mode = st.sidebar.selectbox("Choose model backend:", ["Ollama (local)", "OpenAI GPT-4"])
ollama_model = None
if model_mode == "Ollama (local)":
    ollama_model = st.sidebar.selectbox("Choose Ollama model:", ["codellama", "deepseek-coder", "codegemma"])

temperature = st.sidebar.slider("Creativity (temperature):", 0.0, 1.0, 0.3, 0.1)
language = st.sidebar.selectbox("Code language:", ["python", "javascript", "java", "sql"])

# === COMPLETION MODE ===
with tabs[0]:
    st.subheader("✍️ Code Completion Mode")

    load_session = st.selectbox("📂 Load previous session:", ["None"] + os.listdir(saved_sessions_path))
    if load_session != "None":
        with open(os.path.join(saved_sessions_path, load_session), "r", encoding="utf-8") as f:
            saved_data = json.load(f)
            st.session_state["completion"] = saved_data["completion"]
            user_code = saved_data["user_code"]
            language = saved_data.get("language", "python")
    else:
        user_code = ""

    user_code = st.text_area("✍️ Start writing your code:", value=user_code, height=300)

    def get_ollama_completion(prompt, model="codellama"):
        try:
            full_prompt = f"""Complete the following {language} code:\n\n{prompt}\n\n### Completion:\n"""
            result = subprocess.run([
                "ollama", "run", model
            ], input=full_prompt.encode(), capture_output=True, timeout=180)
            output = result.stdout.decode().strip()
            return output or result.stderr.decode().strip()
        except subprocess.TimeoutExpired:
            return "[Error: Model timed out]"
        except Exception as e:
            return f"[Error running model: {e}]"

    def get_openai_completion(prompt):
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant that completes {language} code."},
                    {"role": "user", "content": f"Complete this code:\n{prompt}"}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[OpenAI error: {e}]"

    if st.button("🚀 Autocomplete Code") and user_code.strip():
        with st.spinner("Thinking..."):
            if model_mode == "OpenAI GPT-4":
                st.session_state["completion"] = get_openai_completion(user_code)
            elif model_mode == "Ollama (local)":
                st.session_state["completion"] = get_ollama_completion(user_code, model=ollama_model)

    if "completion" in st.session_state:
        response = st.session_state["completion"]
        st.subheader("🤖 Suggested Completion:")
        st.code(response, language=language)

        if st.button("📋 Copy to clipboard"):
            try:
                pyperclip.copy(response)
                st.success("Copied!")
            except:
                st.warning("Clipboard not supported.")

        if st.button("💾 Save to .py"):
            fn = f"completion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            with open(fn, "w", encoding="utf-8") as f:
                f.write(response)
            st.success(f"Saved as {fn}")

        if st.button("📥 Save Full Session"):
            data = {
                "user_code": user_code,
                "completion": response,
                "language": language,
                "model_mode": model_mode,
                "ollama_model": ollama_model
            }
            name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(os.path.join(saved_sessions_path, name), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            st.success(f"Saved session: {name}")

        if st.button("🔁 Auto-commit to Git"):
            ok, msg = auto_commit_changes()
            st.success(msg) if ok else st.warning(msg)

# === CHAT MODE ===
with tabs[1]:
    st.subheader("💬 Chat-based Code Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask something about coding:", key="chat_input")

    if st.button("💬 Send") and user_input.strip():
        with st.spinner("Generating answer..."):
            messages = st.session_state.chat_history + [
                {"role": "user", "content": user_input}
            ]
            try:
                if model_mode == "OpenAI GPT-4":
                    openai.api_key = os.getenv("OPENAI_API_KEY")
                    reply = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=messages,
                        temperature=temperature
                    ).choices[0].message.content.strip()
                else:
                    chat_prompt = "\n".join([f"User: {m['content']}" if m['role'] == 'user' else f"AI: {m['content']}" for m in messages])
                    reply = get_ollama_completion(chat_prompt, model=ollama_model)
            except Exception as e:
                reply = f"[Error: {e}]"

            st.session_state.chat_history.extend([
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": reply}
            ])

    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"**👤 You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 AI:** {msg['content']}")
