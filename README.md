# 🗎 AI-Powered JIRA Ticket Generator

An intelligent automation tool to generate **User Stories** and **Test Cases** from requirements and directly creates them in **Jira** with relational links. Ideal for agile teams seeking to streamline requirements engineering and QA workflows.

<img src="https://github.com/user-attachments/assets/d6313304-7432-49db-bdef-532898ea0b41" alt="Chatbot screenshot User Story" width="300"> <img src="https://github.com/user-attachments/assets/b5d3c978-e488-4f80-91ff-66726e34a56c" alt="Chatbot screenshot Test Cases" width="300">

## ✨ Features

- 🔍 Fetch Jira tickets with requirements
- ✍️ Generate structured User Stories with Acceptance Criteria
- ✅ Generate associated Test Cases based on User Stories
- 🔗 Create and link Jira issues (User Story / Test Case)


## 🤖 How It Works

1. **Fetch Requirements**: Pull existing ticket description from JIRA using the ticket number.
2. **Generate Content**: Generate user stories or test cases based on the ticket requirements.
3. **Create Ticket**: Create user stories or test cases in JIRA and link them to the reference ticket.

---

## 📑 Table of Contents
1. [Setup Instructions](#%EF%B8%8F-setup-instructions)
   - [Clone the Repository](#1%EF%B8%8F-clone-the-repository)
   - [Set Up a Virtual Environment](#2%EF%B8%8F-set-up-a-virtual-environment-optional-but-recommended)
   - [Install Dependencies](#3%EF%B8%8F-install-dependencies)
   - [Configure Environment Variables](#4%EF%B8%8F-configure-environment-variables)
   - [Run the Tool](#5%EF%B8%8F-run-the-application)
2. [License](#-license)

---

## 🛠️ Setup Instructions

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/deedmitrij/ai-testing-agent.git
cd ai-testing-agent
```

### **2️⃣ Set Up a Virtual Environment**
```sh
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate  # On Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Configure Environment Variables**
Create a `.env` file in the project root and add the following:

```ini
# ------------------------------------
# Jira API Configuration
# ------------------------------------
JIRA_API_KEY=your_jira_api_key
JIRA_USER_EMAIL=your_jira_user_email
JIRA_BASE_URL=your_jira_base_url

# ------------------------------------
# Google Gemini API Configuration
# ------------------------------------
GEMINI_API_KEY=your_gemini_api_key
```

📌 **Note:** Replace `your_jira_api_key` with your actual JIRA API key.  
📌 **Note:** Replace `your_jira_user_email` with your actual JIRA user e-mail.  
📌 **Note:** Replace `your_jira_base_url` with your actual JIRA base URL.  
📌 **Note:** Replace `your_gemini_api_key` with your actual Gemini API key.  

### **5️⃣ Run the Tool**
```sh
python -m backend.run
```

The chatbot will start and be accessible at **http://localhost:5000**.

---

## 🛡️ License

MIT License © 2025 QuantumAIMind
