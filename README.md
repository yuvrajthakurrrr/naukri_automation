**Naukri Profile Auto-Updater using AI-Powered Resume Parsing**

Automatically update your Naukri.com profile with optimized sections extracted from your LaTeX resume using NVIDIA’s DeepSeek model and Selenium automation. This tool generates a headline, key skills, and a summary tailored for Data and AI Engineering roles, respecting character limits and keyword‑rich formatting.

---

## 🚀 Features

- **AI‑Powered Resume Parsing**: Uses LangChain + NVIDIA DeepSeek‑v3.1 to extract relevant information from a LaTeX resume.
- **Keyword Optimization**: Generates concise, recruiter‑friendly sections for Naukri.com.
- **Automated Profile Update**: Selenium automates the update of:
  - Resume headline (max 250 characters)
  - Key skills (max 19 skills, comma‑separated)
  - Profile summary (max 1000 characters)
- **Error Handling**: Waits for dynamic elements, clears existing skills, and handles suggestion dropdowns.
- **Customizable**: Easily adapt the prompt to your industry or add more sections.

---

## 📋 Prerequisites

- Python 3.8+
- A [NVIDIA API key](https://build.nvidia.com/explore) (for the DeepSeek model)
- Google Chrome browser installed
- ChromeDriver compatible with your Chrome version (automatically handled if using `webdriver_manager`, but here we assume manual installation or PATH inclusion)
- Your resume in LaTeX format (e.g., `yuvraj_resume.tex`)

---

## 🔧 Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/naukri-profile-updater.git
   cd naukri-profile-updater

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for improvements, bug fixes, or additional features (e.g., updating employment details, education, etc.).

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

## 🔗 Keywords
naukri.com resume parser AI resume updater LangChain NVIDIA AI Selenium automation LaTeX resume job search automation Python profile optimizer
