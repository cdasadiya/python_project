# 🐍 Python Project

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**A comprehensive collection of Python utilities, algorithms, CLI tools, and web applications for strengthening core programming skills.**

[Features](#-features) • [Getting Started](#-getting-started) • [Project Structure](#-project-structure) • [Learning Path](#-recommended-learning-path)

</div>

---

## 📋 Overview

This repository is designed to strengthen **core Python programming skills** through practical, real-world implementations. It covers:

- ✨ **Reusable modules** and utilities
- 🎯 **Algorithm exercises** and data structure practice
- 🖥️ **CLI applications** for hands-on learning
- 🌐 **Web applications** using Streamlit
- 🧪 **Testing patterns** and best practices
- 📊 **NumPy foundations** and scientific computing
- ✅ **Pydantic validation** with nested models, validators, and serialization

---

## 👤 Author

<table>
<tr>
<td align="center">
<strong>Chaitanya Dasadiya</strong><br/>
<a href="https://github.com/cdasadiya">@cdasadiya</a><br/>
<a href="https://in.linkedin.com/in/chaitanya-dasadiya">LinkedIn</a><br/>
<sub>Python Developer | AI Engineering Enthusiast | Automation Specialist</sub>
</td>
</tr>
</table>

---

## ✨ Features

| Category | Features |
|----------|----------|
| **📈 Algorithms** | Anagram detection, Frequency analysis, Repetitive element finding, Counter & Dictionary usage |
| **🖥️ CLI Tools** | Dynamic calculator, Interactive to-do checklist, User input handling, Error management |
| **🌐 Web Apps** | Streamlit calculator, Interactive interfaces, Lightweight deployment |
| **🔧 Utilities** | String manipulation, Data structure practice, Reusable functions, NumPy scripts, Pydantic models |
| **🧪 Testing** | Unit testing foundations, Pytest integration, Test coverage |

---

## 📁 Project Structure

```
python_project/
├── 📄 README.md                          # Project documentation
├── 📊 numpy_learning.py                  # NumPy fundamentals & operations
├── ✅ pydantic_validation_demo.py        # Pydantic validation models & helpers
├── 🔤 anagram_check.py                   # Anagram detection algorithm
├── 🧮 dynamic_calculator.py              # Interactive CLI calculator
├── 🌐 streamlit_calculator.py            # Web-based calculator app
├── 📈 most_frequent_element.py           # Frequency analysis
├── 🔄 most_repetitive.py                 # Repetitive element detection
├── 🔄 most_repetitive_element.py         # Advanced repetition analysis
├── ✅ to_do_checklist_python_list.py    # Interactive to-do manager
├── requirements.txt                      # Project dependencies
└── 📂 tests/                             # Unit tests directory
    └── test_*.py                         # Test files
```

---

## 🎯 Project Highlights

### 📊 Algorithm Practice

Master fundamental algorithms and data structures:

```python
# Examples included in this repository:
- Anagram detection using dictionaries
- Frequency counting with Counter()
- Repetitive element analysis
- Optimization techniques for common problems
```

**Skills Reinforced:**
- 🔷 Data structures (lists, dicts, sets)
- 🔄 Loop optimization and iteration
- 📦 Python collections module
- 💡 Problem-solving approaches
- ⚙️ Algorithm complexity analysis

### 🖥️ CLI Utilities

Build interactive command-line applications:

**Dynamic Calculator**
```bash
python dynamic_calculator.py
```
- ➕ Arithmetic operations (add, subtract, multiply, divide)
- 🔢 Input validation and error handling
- 🔄 Continuous operation support
- 📝 Modular function architecture

**To-Do Checklist Manager**
```bash
python to_do_checklist_python_list.py
```
- ✅ Add, view, and remove tasks
- 💾 List manipulation patterns
- 🎯 Menu-driven interface
- 🏗️ Structured data management


**Pydantic Validation Demo**
```bash
python pydantic_validation_demo.py
```
- 🧱 Nested models for users, addresses, products, and orders
- ✅ Field constraints for emails, IDs, quantities, prices, and postal codes
- 🔄 Validators for tag normalization and cross-field shipping rules
- 🧮 Computed fields for line totals and order totals
- 📦 JSON parsing and serialization helpers

**Concepts Demonstrated:**
- ⌨️ User input handling (input(), sys)
- 🔀 Conditional logic (if/elif/else)
- 🔁 Loops and iteration patterns
- ❌ Error handling and validation
- 📦 Modular programming practices

### 🌐 Streamlit Web Application

Transform Python logic into interactive web interfaces instantly:

```bash
streamlit run streamlit_calculator.py
```

**Features:**
- 🎨 Interactive widgets and sliders
- 📊 Real-time computation feedback
- 🚀 Quick prototyping capability
- 💻 No frontend knowledge required
- 🌍 Easily deployable

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/cdasadiya/python_project.git
cd python_project
```

### Step 2: Create a Virtual Environment

**On macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Scripts

**Run any Python file directly:**
```bash
python filename.py
```

**Example - Run the dynamic calculator:**
```bash
python dynamic_calculator.py
```

**Example - Launch Streamlit app:**
```bash
streamlit run streamlit_calculator.py
```

---

## 🧪 Testing

This project includes unit tests to validate reusable modules.

**Run all tests:**
```bash
pytest
```

**Run specific test file:**
```bash
pytest tests/test_calculator.py
```

**Run with coverage:**
```bash
pytest --cov=.
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core programming language (3.8+) |
| **NumPy** | Numerical computing and arrays |
| **Pydantic** | Data validation, parsing, and serialization |
| **Streamlit** | Web application framework |
| **Pytest** | Testing framework |
| **Collections** | Advanced data structures |

---

## 📚 Skills Demonstrated

✅ Core Python programming fundamentals  
✅ Object-oriented and functional programming patterns  
✅ Modular code organization and best practices  
✅ CLI application development  
✅ Web application development (Streamlit)  
✅ Algorithm design and optimization  
✅ Data structure usage and manipulation  
✅ Unit testing and test-driven development  
✅ Pydantic data validation and serialization
✅ Error handling and validation  
✅ Python project structuring and configuration  

---

## 🎓 Recommended Learning Path

Follow this progression to maximize learning:

```
1. Start with Algorithm Scripts
   └─ Understand data structures and problem-solving

2. Explore Calculator Utilities
   └─ Learn modular function patterns

3. Review String & Frequency Analysis
   └─ Master Python collections

4. Run & Modify the Streamlit App
   └─ Explore web interface concepts

5. Examine & Write Tests
   └─ Practice test-driven development

6. Refactor Scripts Into Packages
   └─ Advanced project organization
```

---

## 🔮 Future Enhancements

This project roadmap includes:

- 🏗️ Object-oriented refactoring and design patterns
- 🎯 Advanced algorithm challenges (sorting, searching, dynamic programming)
- 🔌 REST API integrations and external services
- 🗄️ Database support (SQLite, PostgreSQL)
- 🐳 Docker containerization
- 🔄 CI/CD pipelines (GitHub Actions)
- 📝 Advanced logging and configuration management
- 📊 Data visualization (matplotlib, Plotly, Seaborn)
- ☁️ Cloud deployment (Heroku, AWS, Google Cloud)
- 🤖 Machine Learning integration

---

## 📖 Resources & References

- [Python Official Documentation](https://docs.python.org/3/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

---

## 📄 License

This project is licensed under the **MIT License** - a permissive open-source license.

See the [LICENSE](LICENSE) file for full details.

---

## 💬 Contributing

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

<div align="center">

**⭐ If you find this project helpful, please consider giving it a star!**

Made with ❤️ by [Chaitanya Dasadiya](https://github.com/cdasadiya) · [LinkedIn](https://in.linkedin.com/in/chaitanya-dasadiya)

</div>
