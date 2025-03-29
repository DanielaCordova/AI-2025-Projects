# 🧠 Mini Copilot – Streamlit AI Assistant (v2)

This is a fully interactive, developer-oriented assistant for **code completion**, **chat-based help**, **unit testing**, **Git integration**, and **session management** using local (`Ollama`) or cloud (`OpenAI GPT-4`) models.

---

## ✨ Features

| Feature                          | Description |
|----------------------------------|-------------|
| ✍️ Code Completion UI           | Write a function and let the LLM complete it |
| 💬 Chat Assistant Mode           | Ask programming questions with multi-turn memory |
| 🧠 Supports Ollama + OpenAI      | Choose local or GPT-4 models |
| 💾 Save sessions to JSON         | Keeps code, completions, language, model |
| 📂 Load previous sessions        | Restore any saved state |
| 📋 Copy completions to clipboard | One-click copy to clipboard |
| 📁 Export completions            | Save to `.py` or `.md` files |
| 🧪 Unit test generator           | Auto-generate test cases from your code |
| 🧱 Style checker                 | Simple suggestions for cleaner code |
| 🔁 Git integration               | Auto-commit changes to a local repo |

---

## 🧠 Modes

### 1. Code Completion Tab
Write code, press `Autocomplete`, and get a response from:
- `OpenAI GPT-4` (via API)
- `Ollama` local models like `codellama`, `deepseek-coder`

### 2. Chat Assistant Tab
Ask anything like:
> “How do I create a decorator in Python?”

It keeps the full **chat history**, useful for incremental code help or learning.

---

## 🧰 Developer Utilities

### Save Session
```json
{
  "user_code": "def add(a, b):",
  "completion": "...",
  "language": "python",
  "model_mode": "Ollama (local)",
  "ollama_model": "codellama"
}
```

### Git Auto-Commit
- Detects if your folder is a Git repo
- Adds & commits changes with default message:
  > `Auto-commit from Mini Copilot`

---

## 🧪 Example Flow

1. Start typing:
```python
def factorial(n):
```

2. Click Autocomplete → get full function body
3. Save, commit, or chat about test cases

---

## 🧱 Project Layout

```
📦 project/
├── copilot_app.py
├── saved_sessions/
│   └── session_20250330_140301.json
├── README_mini_copilot.md
```

---

## ⚙️ Requirements

```bash
pip install streamlit openai pyperclip gitpython
```

You’ll also need [Ollama](https://ollama.com/) installed for local models.

---

## 🏁 How to Launch

```bash
streamlit run copilot_app.py
```

---

## 🔮 Future Ideas

- Token usage + pricing estimation
- Branching for multi-version session tracking
- VS Code extension
- Org-wide config & analytics

---

Built for devs, by devs 💻✨