# 📊 WhatsApp Chat Analyzer

A **Python-based WhatsApp Chat Analyzer** built using **Streamlit** that helps extract meaningful insights from exported WhatsApp chat files.  
The application analyzes chat data and visualizes statistics such as message counts, user activity, timelines, and word usage.

---

## 🚀 Features

- 📁 Upload WhatsApp `.txt` chat export
- 👤 User-wise message statistics
- 📈 Daily and monthly activity timelines
- 💬 Most active users
- 📝 Word frequency analysis
- 🔗 Count of links shared
- 🖼 Media messages count
- 😀 Emoji usage analysis
- 📊 Interactive visualizations using Streamlit

---

## 🛠 Tech Stack

- **Python 3**
- **Streamlit** – Web UI
- **Pandas** – Data processing
- **Matplotlib & Seaborn** – Visualization
- **NumPy** – Numerical operations

---

## 📁 Project Structure

```text
whatspp-chat-analyzer/
│
├── app.py                     # Main Streamlit application
├── preprocessor.py            # Chat parsing & preprocessing logic
├── helper.py                  # Analysis & visualization functions
├── extracted_stopwords.txt    # Stopwords for text analysis
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── .gitignore                 # Ignored files/folders
