# 🧼 Code Quality & Refactor Assistant (Streamlit + LLM)

This is a developer-oriented Streamlit app that uses **local or cloud LLMs** to:
- Score your Python code
- Suggest improvements
- Refactor the code
- Detect code smells
- Estimate complexity
- Save/load full sessions

---

## 🎯 What You Can Do

1. Paste or upload a Python function or script
2. Select a model:
   - 🧠 **GPT-4** (via OpenAI API)
   - ⚙️ **Local models with Ollama** (`codellama`, `deepseek-coder`, etc.)
3. Click **Analyze**
4. See:
   - A **code quality score**
   - **LLM feedback** for improvements
   - A **refactored version** of your code
   - **Code smells**
   - **Complexity estimate** (like cyclomatic complexity)
5. Copy or export refactored code
6. Save/load sessions!

---

## 📦 Dependencies

```bash
pip install streamlit openai pyperclip
```

Also install:
- [Ollama](https://ollama.com) if using local models
- Add your OpenAI key via environment variable:
```bash
export OPENAI_API_KEY=sk-xxxx
```

---

## 🧠 How It Works

### 🔁 Model Selection
```python
model_mode = st.selectbox("Choose model backend:", ["Ollama (local)", "OpenAI GPT-4"])
```

### 🧠 LLM Prompts (Chain)
- **Score**:
  > “Rate the following code from 1–10…”
- **Feedback**:
  > “Give a detailed list of improvements…”
- **Refactor**:
  > “Refactor the code for clarity, simplicity…”
- **Code smells**:
  > “Detect anti-patterns or smells…”
- **Complexity**:
  > “Estimate the cyclomatic complexity…”

---

## 💾 Session Management

Each session saves:
```json
{
  "code_input": "...",
  "score": "8",
  "feedback": "Use better naming...",
  "refactored_code": "...",
  "code_smells": "...",
  "complexity": "Low"
}
```

Stored inside:
```
quality_sessions/
├── session_20250330_151200.json
```

---

## 🖼 App UI Overview

```text
[ CODE INPUT ]
+-----------------------------+
|  Paste Python code here    |
+-----------------------------+

[ MODEL & TEMP ]
Choose GPT-4 or Ollama model

[ ANALYZE ]

→ Score (1–10)
→ Feedback
→ Code smells
→ Complexity
→ Refactored Code (copy/export)
→ Save Session

[ LOAD SESSION ]
Dropdown to reload previous analysis
```

---

## 🛠️ Extend Ideas

- Add token cost estimator
- Export full report as PDF
- Add multi-language support (JS, Java)
- GitHub action integration for PR review

---

Built for dev productivity 🧠💻