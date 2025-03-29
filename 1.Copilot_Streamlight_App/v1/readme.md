# 🧠 Mini Copilot Streamlit App – Full Documentation & Explanation

Welcome to your **AI Code Copilot** – a Streamlit app that helps developers autocomplete code, generate unit tests, check coding style, and manage session history using both **local models (Ollama)** and **cloud models (OpenAI GPT-4)**.

This guide will walk you through each component like you're attending a class 👨‍🏫.

---

## 🎯 Goal of the App

This app is designed to simulate a **code assistant** like GitHub Copilot, but with:
- Full control over the backend model (local or cloud)
- Enhanced explainability (you can inspect everything)
- Extendability for teams or internal developer platforms

---

## 🧱 App Architecture (Big Picture)

```
Streamlit Frontend
├── Code input area
├── Model and language selection
├── Buttons for actions (Autocomplete, Save, etc.)
├── Output display
└── Session manager (load/save)

Python Backend
├── Model access functions (Ollama, OpenAI)
├── Unit test generator
├── Code style checker
└── Session state management
```

---

## 🧑‍💻 Step-by-Step Explanation of Each Feature

### 1. 📝 Code Editor

```python
user_code = st.text_area("✍️ Start writing your code:", ...)
```
A large input box where the user starts writing a code snippet (e.g., a function, a class). This is the core input for everything else.

---

### 2. 🤖 Model Selection

```python
model_mode = st.selectbox("Choose model backend:", [...])
```
Lets you choose between:
- **Ollama (local)**: Fully offline inference using models like `codellama`
- **OpenAI GPT-4**: Cloud-based inference with higher quality and reliability

If you choose Ollama, another dropdown appears to let you pick the exact local model.

---

### 3. 🧠 Code Autocompletion

```python
if st.button("🚀 Autocomplete Code"):
```

When you click this:
- The app wraps your code into a **prompt** that says:
  ```
  Complete the following <language> code:

  <your_code>

  ### Completion:
  ```
- Then it sends the prompt to the selected model and displays the response.
- Results are cached in `st.session_state["completion"]` so the UI persists.

---

### 4. 📋 Copy to Clipboard

```python
pyperclip.copy(response)
```

Copies the completion output to the system clipboard using `pyperclip`. This allows quick reuse.

---

### 5. 💾 Export to File

You can export the completion to a `.py` or `.md` file. A timestamped filename is generated automatically and the file is saved locally.

---

### 6. 📥 Save Full Session

This saves:
- The user’s code
- The AI-generated completion
- The selected model and language

Saved as a JSON file inside a `/saved_sessions` folder:
```json
{
  "user_code": "...",
  "completion": "...",
  "language": "python",
  "model_mode": "Ollama (local)",
  "ollama_model": "codellama"
}
```

---

### 7. 📂 Load Session

From the sidebar, you can select and load a previously saved session. The UI updates with all saved settings and responses.

---

### 8. 🧪 Unit Test Generator

```python
Write unit tests for the following <language> function:
<your code>
```

This prompt is sent to the LLM to generate matching unit tests. You can use this to:
- Check if your function behaves as expected
- Speed up TDD (Test-Driven Development)

---

### 9. 🧱 Code Style Checker

Uses simple logic to detect common issues, like:
- Semicolons in Python
- Too many lines in one function

> This can be extended with `flake8`, `pylint`, or any custom logic.

---

### 10. 🧠 Session State & Persistence

We use `st.session_state` to remember:
- The last completion
- Code language
- Model settings

This makes the app feel “stateful” — buttons work without wiping data.

---

## 📦 Dependencies

```bash
pip install streamlit openai pyperclip
```

Also install and configure [Ollama](https://ollama.com) for local LLMs.

---

## 🏁 How to Run It

```bash
streamlit run copilot_app.py
```

---

## 🏢 Why This Is Valuable for Companies

- ✅ Works offline (great for internal tools)
- ✅ Tracks developer input/output for auditing or retraining
- ✅ Extendable with linters, Docker file generation, docstring helpers
- ✅ Shows how to orchestrate multiple LLMs in a single app
- ✅ Encourages explainability and testing from day 1

---

## 🔮 Ideas to Extend

- Track token usage and OpenAI cost
- Version control integration (auto-commit to Git)
- Syntax-aware suggestions with tree-sitter or ast
- Autocomplete chat mode (conversational)

---

Made by devs, for devs 💻✨