# 🐍 Core Python Lab

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active%202026-brightgreen?style=for-the-badge)
![Repo Size](https://img.shields.io/github/repo-size/cdasadiya/core-python-lab?style=for-the-badge)

**A comprehensive, production-ready collection of Python utilities, algorithms, CLI tools, and web applications for mastering core programming skills.**

[📖 Features](#-features) • [🚀 Quick Start](#-getting-started) • [📁 Structure](#-project-structure) • [🎓 Learning Path](#-recommended-learning-path) • [👤 Author](#-author)

</div>

---

## 📋 Overview

This repository is a hands-on learning lab designed to strengthen **core Python programming skills** through practical, production-grade implementations. Whether you're mastering data structures, building CLI applications, or learning advanced concepts like multithreading and OOP, this repository provides well-documented, tested examples.

### What's Inside?

- ✨ **Algorithm Practice** - Data structures, frequency analysis, anagram detection
- 🎯 **CLI Applications** - Interactive calculators, to-do managers, validators
- 🖥️ **Web Frameworks** - Streamlit-based interactive dashboards
- 🔧 **Utility Modules** - Reusable functions and helper patterns
- 📊 **Data Science** - NumPy, Pandas, and scientific computing fundamentals
- 🧪 **Advanced Concepts** - OOP systems, multithreading, web scraping, async operations
- ✅ **Testing** - Unit test patterns and validation examples
- 📦 **Data Validation** - Pydantic models with nested structures and custom validators

---

## 👤 Author

<table>
<tr>
<td align="center" width="300px">
<a href="https://github.com/cdasadiya">
<img src="https://avatars.githubusercontent.com/u/7426056?v=4" width="100px;" alt="Chaitanya Dasadiya"/>
</a>
<br/>
<strong>Chaitanya Dasadiya</strong>
<br/>
<a href="https://github.com/cdasadiya">GitHub: @cdasadiya</a>
<br/>
<a href="https://in.linkedin.com/in/chaitanya-dasadiya">LinkedIn Profile</a>
<br/>
<sub>Python Developer • AI Engineering Enthusiast • Automation Specialist</sub>
<br/>
<sub>Last Updated: June 2026</sub>
</td>
</tr>
</table>

---

## ✨ Features

| Category | Highlights |
|----------|------------|
| **🧮 Algorithm Mastery** | Anagram detection, frequency counting, element analysis, pattern matching |
| **📈 Data Structures** | Lists, dictionaries, Counter, sets - practical patterns and optimizations |
| **🖥️ CLI Tools** | Interactive calculator, to-do manager, datetime utilities, custom validators |
| **🌐 Web Applications** | Streamlit-based UI, interactive dashboards, no backend coding required |
| **🔌 Advanced Python** | Multithreading, OOP patterns, web scraping, async operations, decorators |
| **📊 Data Science Stack** | NumPy arrays, Pandas DataFrames, Pydantic validation, data transformations |
| **✅ Best Practices** | Type hints, error handling, docstrings, test patterns, code organization |
| **🧪 Validation & Testing** | Unit tests, custom validators, Pydantic constraints, pytest integration |

---

## 📁 Project Structure

```
core-python-lab/
├── 📄 README.md                           # Project documentation (you are here)
├── 📋 requirements.txt                    # Python dependencies with versions
├── 📜 LICENSE                             # MIT License
│
├── 🧮 Algorithm & Data Structure Fundamentals
│   ├── anagram_check.py                   # Detect anagrams using dictionaries
│   ├── most_frequent_element.py           # Find most common element in lists
│   ├── most_repetitive.py                 # Efficient frequency analysis
│   └── most_repetitive_element.py         # Advanced repetition detection with error handling
│
├── 🖥️ Interactive CLI Applications
│   ├── dynamic_calculator.py              # Calculator with arithmetic operations
│   ├── to_do_checklist_python_list.py     # Interactive to-do list manager
│   ├── datetime_master_utility.py         # Comprehensive datetime operations
│   └── streamlit_calculator.py            # Web-based calculator interface
│
├── 📊 Data Science & Analysis
│   ├── numpy_learning.py                  # NumPy fundamentals and operations
│   └── pandas_methods_demo.py             # Pandas DataFrame manipulation
│
├── 📦 Advanced Concepts & Patterns
│   ├── pydantic_validation_demo.py        # Data validation with nested models
│   ├── oop_learning_hospital_system.py    # Full OOP system with design patterns
│   ├── multithreading_mini_project.py     # Threading primitives and coordination
│   └── webscraping_learning_framework.py  # Web scraping with BeautifulSoup & Selenium
│
├── 🧪 Testing & Execution
│   ├── test_execution.py                  # Test runner for all modules
│   └── 📂 tests/                          # Unit test directory (ready for pytest)
│
└── 🔧 Configuration
    └── .github/                           # GitHub workflows and templates
```

---

## 🎯 Core Features Deep Dive

### 1. 🧮 Algorithm & Data Structure Practice

Master fundamental algorithms with clear, documented code:

```python
# Examples in this repo:
- Anagram detection using dictionaries
- Frequency counting with Counter()
- Efficient list operations and transformations
- Problem-solving patterns and optimization techniques
```

**Learn:** Data structures (lists, dicts, sets) → Collections module → Algorithm complexity

### 2. 🖥️ Interactive CLI Applications

Build feature-rich command-line tools:

**Dynamic Calculator**
```bash
python dynamic_calculator.py
```
- ➕ Full arithmetic operations with error handling
- 🔢 Input validation and user-friendly prompts
- 🔄 Continuous operation mode
- 📝 Modular function design

**To-Do Checklist Manager**
```bash
python to_do_checklist_python_list.py
```
- ✅ Add, complete, and remove tasks
- 📋 Advanced list operations (sort, reverse, insert)
- 🎯 Menu-driven interface patterns
- 📊 Task tracking and summaries

### 3. 📊 Data Validation & Pydantic

**Pydantic Validation Demo**
```bash
python pydantic_validation_demo.py
```
- 🧱 Nested model structures (User → Address, Product, Order)
- ✅ Field constraints (emails, numeric ranges, postal codes)
- 🔄 Custom validators and normalization
- 🧮 Computed fields (line totals, order totals)
- 📦 JSON serialization and deserialization

### 4. 🌐 Web Applications with Streamlit

```bash
streamlit run streamlit_calculator.py
```

- 🎨 Interactive widgets with real-time feedback
- 📊 Visual interface without frontend coding
- 🚀 One-command deployment
- 💻 Responsive design

### 5. 🧵 Advanced Concurrency with Multithreading

**Comprehensive Threading Demo**
```bash
python multithreading_mini_project.py
```

Covers:
- 🔄 Thread creation and management
- 🔒 Lock and RLock for data protection
- 📊 Semaphore for resource limiting
- 🚩 Event and Condition for coordination
- 🏁 Barrier for synchronization
- 📬 Queue for safe inter-thread communication
- 🏊 ThreadPoolExecutor for worker pools
- 👻 Daemon threads for background tasks

### 6. 🏥 OOP Design Patterns

**Hospital Management System**
```bash
python oop_learning_hospital_system.py
```

Demonstrates:
- 🏗️ Class hierarchies and inheritance
- 🛡️ Role-Based Access Control (RBAC)
- 📊 Data encapsulation and properties
- 🎯 Decorators for cross-cutting concerns
- 🧪 Model validation and error handling

### 7. 🌐 Web Scraping Framework

**Comprehensive Web Scraping**
```bash
python webscraping_learning_framework.py
```

Features:
- 📄 HTML parsing with BeautifulSoup
- 🤖 Browser automation with Selenium
- 🔄 Async operations with aiohttp
- 🛡️ User-agent rotation
- 📊 Data extraction patterns

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (3.10+ recommended)
- **pip** (Python package manager)
- **Git** (for cloning)
- **Virtual environment** (optional but recommended)

### Step 1️⃣: Clone the Repository

```bash
git clone https://github.com/cdasadiya/core-python-lab.git
cd core-python-lab
```

### Step 2️⃣: Create Virtual Environment

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3️⃣: Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Step 4️⃣: Run Examples

**Run any script directly:**
```bash
python script_name.py
```

**Run the test suite:**
```bash
python test_execution.py
```

**Launch Streamlit app:**
```bash
streamlit run streamlit_calculator.py
```

---

## 📚 Detailed File Guide

### Algorithm & Data Structures

| File | Purpose | Difficulty | Duration |
|------|---------|-----------|----------|
| `anagram_check.py` | Compare strings for anagrams | Beginner | 5 min |
| `most_frequent_element.py` | Find most common element | Beginner | 5 min |
| `most_repetitive.py` | Frequency analysis with Counter | Beginner | 5 min |
| `most_repetitive_element.py` | Advanced frequency with error handling | Intermediate | 10 min |

### CLI Applications

| File | Purpose | Difficulty | Duration |
|------|---------|-----------|----------|
| `dynamic_calculator.py` | Interactive arithmetic calculator | Beginner | 10 min |
| `to_do_checklist_python_list.py` | Full-featured to-do manager | Beginner | 15 min |
| `datetime_master_utility.py` | Comprehensive datetime utilities | Intermediate | 20 min |
| `streamlit_calculator.py` | Web-based calculator UI | Beginner | 5 min |

### Data Science

| File | Purpose | Difficulty | Duration |
|------|---------|-----------|----------|
| `numpy_learning.py` | NumPy fundamentals | Intermediate | 15 min |
| `pandas_methods_demo.py` | DataFrame operations | Intermediate | 15 min |

### Advanced Topics

| File | Purpose | Difficulty | Duration |
|------|---------|-----------|----------|
| `pydantic_validation_demo.py` | Data validation & serialization | Advanced | 20 min |
| `oop_learning_hospital_system.py` | Full OOP system | Advanced | 30 min |
| `multithreading_mini_project.py` | Threading & concurrency | Advanced | 30 min |
| `webscraping_learning_framework.py` | Web scraping patterns | Advanced | 30 min |

---

## 🛠️ Tech Stack

| Component | Purpose | Version |
|-----------|---------|----------|
| **Python** | Core language | 3.8+ |
| **NumPy** | Numerical computing | ≥1.24 |
| **Pandas** | Data manipulation | ≥1.5 |
| **Pydantic** | Data validation | ≥2.7 |
| **Streamlit** | Web framework | ≥1.30 |
| **Requests** | HTTP client | ≥2.31 |
| **BeautifulSoup4** | HTML parsing | ≥4.12 |
| **Selenium** | Browser automation | ≥4.13 |
| **Pytest** | Testing framework | ≥7.0 |

---

## 🧪 Testing

This project includes comprehensive test patterns:

**Run all files with test_execution.py:**
```bash
python test_execution.py
```

This generates a detailed report showing:
- ✅ Successful executions
- ❌ Failures with error messages
- ⏱️ Timeouts
- ⊘ Skipped files

**Run pytest for formal unit tests:**
```bash
pytest                                      # Run all tests
pytest tests/                              # Run tests directory
pytest -v                                  # Verbose output
pytest --cov                               # With coverage report
```

---

## 📚 Skills Demonstrated

### Core Python
✅ Variables, data types, and operations  
✅ Control flow (if/elif/else, loops)  
✅ Functions with type hints and docstrings  
✅ List comprehensions and generator expressions  
✅ Error handling and custom exceptions  
✅ File I/O and string operations  

### Intermediate
✅ Decorators and closures  
✅ Object-oriented programming (classes, inheritance)  
✅ Magic methods and properties  
✅ Context managers and with statements  
✅ Regular expressions  
✅ Collections module (Counter, defaultdict, etc.)  

### Advanced
✅ Multithreading and concurrency primitives  
✅ Async/await and asynchronous programming  
✅ Web scraping and HTTP requests  
✅ Data validation with Pydantic  
✅ Design patterns (Decorator, Observer, Strategy)  
✅ Testing and test-driven development  
✅ Web frameworks (Streamlit)  

---

## 🎓 Recommended Learning Path

### Week 1: Foundations
1. `anagram_check.py` - Understand dictionaries
2. `most_frequent_element.py` - Master list operations
3. `dynamic_calculator.py` - Learn functions and input handling

### Week 2: Data Structures & Collections
1. `most_repetitive_element.py` - Collections.Counter
2. `to_do_checklist_python_list.py` - Advanced list operations
3. `numpy_learning.py` - Introduction to NumPy

### Week 3: Data Science & Validation
1. `pandas_methods_demo.py` - DataFrame fundamentals
2. `pydantic_validation_demo.py` - Data validation
3. `streamlit_calculator.py` - Web interfaces

### Week 4: Advanced Concepts
1. `oop_learning_hospital_system.py` - OOP design patterns
2. `multithreading_mini_project.py` - Concurrency
3. `webscraping_learning_framework.py` - Web scraping

### Week 5: Master Project
1. Study all implementations
2. Modify and extend examples
3. Combine concepts for custom projects

---

## 🔮 Future Enhancements

Planned additions to the repository:

- 🐳 Docker containerization for easy deployment
- 🔄 CI/CD pipelines with GitHub Actions
- 📝 Advanced logging and configuration management
- 📊 Data visualization (matplotlib, Plotly, Seaborn)
- ☁️ Cloud deployment examples (Heroku, AWS, Google Cloud)
- 🤖 Machine Learning integration (scikit-learn, TensorFlow)
- 🏗️ Microservices architecture examples
- 🔐 Security best practices (authentication, encryption)
- 📚 Interactive Jupyter notebooks

---

## 📖 Resources & References

### Official Documentation
- [Python 3 Official Docs](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints Guide](https://docs.python.org/3/library/typing.html)

### Libraries Used
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium Documentation](https://selenium.dev/documentation/)

### Learning Resources
- [Real Python Tutorials](https://realpython.com/)
- [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/)
- [Python Design Patterns](https://refactoring.guru/design-patterns/python)
- [Async IO in Python](https://docs.python.org/3/library/asyncio.html)

---

## 📄 License

This project is licensed under the **MIT License** - a permissive, permissive open-source license that allows free use, modification, and distribution.

**License Details:**
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ⚠️ Must include license and copyright notice

See the [LICENSE](LICENSE) file for the complete license text.

---

## 🤝 Contributing

Contributions are welcome! Help improve this learning resource:

### How to Contribute

1. **Fork the repository**
   ```bash
   git clone https://github.com/cdasadiya/core-python-lab.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-improvement
   ```

3. **Make your changes**
   - Add comments and docstrings
   - Follow PEP 8 style guide
   - Test your code

4. **Commit changes**
   ```bash
   git commit -m "feature: Add improvement description"
   ```

5. **Push to branch**
   ```bash
   git push origin feature/your-improvement
   ```

6. **Open a Pull Request**
   - Describe your changes
   - Reference any related issues

### Contribution Guidelines
- Add comprehensive docstrings
- Include author/reference information
- Follow existing code patterns
- Update README if needed
- Add tests for new features

---

## 🌟 Acknowledgments

This project is maintained with ❤️ as an educational resource for Python learners worldwide.

**Special Thanks To:**
- Python community for excellent libraries
- Contributors who improve this project
- Learners who use this as a reference

---

## 📞 Support & Contact

### Get in Touch
- 🐙 **GitHub:** [@cdasadiya](https://github.com/cdasadiya)
- 💼 **LinkedIn:** [Chaitanya Dasadiya](https://in.linkedin.com/in/chaitanya-dasadiya)
- 🌐 **GitHub Issues:** [Report bugs or suggest features](https://github.com/cdasadiya/core-python-lab/issues)

### Questions or Issues?
Open an issue on GitHub or reach out via LinkedIn!

---

<div align="center">

### ⭐ If you find this project helpful, please give it a star!

**Made with ❤️ by [Chaitanya Dasadiya](https://github.com/cdasadiya)**

[GitHub](https://github.com/cdasadiya) • [LinkedIn](https://in.linkedin.com/in/chaitanya-dasadiya) • [Portfolio](https://github.com/cdasadiya)

Last Updated: **June 2026**

Happy Learning! 🎓

</div>
