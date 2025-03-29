import streamlit as st
import subprocess
import openai
import os
import pyperclip
from datetime import datetime
import json

# === PAGE CONFIG ===
st.set_page_config(page_title="🧼 Code Quality Assistant", layout="centered")
st.title("🧪 Code Quality & Refactor Assistant")

# === SESSION PATH ===
session_dir = "quality_sessions"
os.makedirs(session_dir, exist_ok=True)

# === MODEL SETTINGS ===
model_mode = st.selectbox("Choose model backend:", ["Ollama (local)", "OpenAI GPT-4"])
ollama_model = None
if model_mode == "Ollama (local)":
    ollama_model = st.selectbox("Select Ollama model:", ["codellama", "deepseek-coder", "codegemma"])

openai.api_key = os.getenv("OPENAI_API_KEY")
temperature = st.slider("Creativity (temperature):", 0.0, 1.0, 0.3, 0.1)

# === LOAD SESSION ===
load_file = st.selectbox("📂 Load a previous session:", ["None"] + os.listdir(session_dir))
if load_file != "None":
    with open(os.path.join(session_dir, load_file), "r", encoding="utf-8") as f:
        saved = json.load(f)
        code_input = saved.get("code_input", "")
        st.session_state["last_refactored"] = saved.get("refactored_code", "")
        st.session_state["last_feedback"] = saved.get("feedback", "")
        st.session_state["last_score"] = saved.get("score", "")
        st.session_state["last_smells"] = saved.get("code_smells", "")
        st.session_state["last_complexity"] = saved.get("complexity", "")
else:
    code_input = ""

# === CODE INPUT ===
code_input = st.text_area("Paste your Python code:", value=code_input, height=300, placeholder="def calculate_tax(income):\n    ...")

# === HELPERS ===
def run_ollama(prompt, model):
    try:
        result = subprocess.run(["ollama", "run", model], input=prompt.encode(), capture_output=True, timeout=180)
        return result.stdout.decode().strip() or result.stderr.decode().strip()
    except Exception as e:
        return f"[Ollama error: {e}]"

def run_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior Python engineer helping improve code."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[OpenAI error: {e}]"

def ask_llm(prompt):
    if model_mode == "OpenAI GPT-4":
        return run_openai(prompt)
    elif model_mode == "Ollama (local)":
        return run_ollama(prompt, model=ollama_model)

# === ANALYZE BUTTON ===
if st.button("🧠 Analyze & Refactor") and code_input.strip():
    with st.spinner("Scoring and reviewing code..."):
        score_prompt = f"Rate the following Python code from 1–10 based on readability, structure, and best practices. Return just a number.\n\n{code_input}"
        score = ask_llm(score_prompt)

        feedback_prompt = f"Give a detailed list of improvements for the following Python code.\n\n{code_input}"
        feedback = ask_llm(feedback_prompt)

        refactor_prompt = f"Refactor the following Python code for clarity, simplicity, and Python best practices:\n\n{code_input}"
        refactored_code = ask_llm(refactor_prompt)

        smells_prompt = f"Detect any code smells or anti-patterns in this code and explain.\n\n{code_input}"
        code_smells = ask_llm(smells_prompt)

        complexity_prompt = f"Estimate the cyclomatic complexity of this Python code and explain.\n\n{code_input}"
        complexity = ask_llm(complexity_prompt)

        st.session_state["last_score"] = score
        st.session_state["last_feedback"] = feedback
        st.session_state["last_refactored"] = refactored_code
        st.session_state["last_smells"] = code_smells
        st.session_state["last_complexity"] = complexity

# === DISPLAY RESULTS IF AVAILABLE ===
if "last_score" in st.session_state:
    st.subheader("📊 Code Quality Score")
    st.markdown(f"**{st.session_state['last_score']}/10**")

    st.subheader("🧠 LLM Feedback")
    st.markdown(st.session_state["last_feedback"])

    st.subheader("🧱 Code Smells")
    st.markdown(st.session_state["last_smells"])

    st.subheader("🧮 Complexity Estimate")
    st.markdown(st.session_state["last_complexity"])

    st.subheader("🧼 Refactored Code")
    st.code(st.session_state["last_refactored"], language="python")

    if st.button("📋 Copy Refactored Code"):
        try:
            pyperclip.copy(st.session_state["last_refactored"])
            st.success("Copied to clipboard!")
        except:
            st.warning("Clipboard copy failed.")

    if st.button("💾 Save Refactored Code"):
        filename = f"refactored_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(st.session_state["last_refactored"])
        st.success(f"Saved to {filename}")

    if st.button("🗂 Save Session"):
        session_data = {
            "code_input": code_input,
            "score": st.session_state["last_score"],
            "feedback": st.session_state["last_feedback"],
            "refactored_code": st.session_state["last_refactored"],
            "code_smells": st.session_state["last_smells"],
            "complexity": st.session_state["last_complexity"]
        }
        session_file = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(os.path.join(session_dir, session_file), "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2)
        st.success(f"Session saved: {session_file}")
