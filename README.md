# AI Chatbot 

A simple, NLP-based customer support chatbot built with Python, Scikit-learn, and Streamlit. The chatbot identifies user intent by comparing user queries with predefined patterns using TF-IDF vectorization and cosine similarity, then returns an appropriate response.

## Features

- **Intent Recognition:** Matches user queries with predefined intent patterns.
- **TF-IDF Vectorization:** Converts text into numerical feature vectors.
- **Cosine Similarity:** Identifies the most similar stored pattern.
- **Fallback Handling:** Responds appropriately when a query cannot be matched confidently.
- **Interactive Chat Interface:** Provides a clean, professional interface using Streamlit.
- **Multiple Intents:** Supports greetings, services, pricing, working hours, contact information, refunds, technical support, and more.
- **Modular Structure:** Separates chatbot logic, query preprocessing, intent data, and UI.

## Tech Stack

- Python
- Scikit-learn
- NLTK (if preprocessing is implemented)
- Streamlit
- JSON

##  Project Structure

```text
ChatBot/
├── app.py           # Streamlit web interface
├── chatbot.py       # Intent matching and response logic
├── preprocess.py    # Query preprocessing (if implemented)
├── intents.json     # Intent patterns and responses
└── README.md        # Project documentation
```

## ⚙️ How It Works

1. The user enters a query through the Streamlit interface.
2. The query is optionally cleaned and normalized using the preprocessing module.
3. TF-IDF converts the query and predefined patterns into numerical vectors.
4. Cosine similarity measures the similarity between the query and stored patterns.
5. The chatbot selects the best-matching intent.
6. A predefined response is returned, or a fallback message is shown if the similarity score is below the configured threshold.

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_NAME
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2. Create and activate a virtual environment (optional)

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install streamlit scikit-learn nltk
```

Install NLTK only if the preprocessing module requires it.

### 4. Run the chatbot

```bash
streamlit run app.py
```

The application will open in your browser.

##  Example Queries

| User Query | Expected Intent |
|---|---|
| Hi | Greeting |
| What services do you offer? | Services |
| How much does it cost? | Pricing |
| Where are you located? | Location |
| Thank you | Thanks |
| I need technical assistance | Technical Support |

Actual predictions depend on the patterns defined in `intents.json` and the similarity threshold.

##  Future Improvements

- Improve query normalization and linguistic preprocessing.
- Add context-aware multi-turn conversations.
- Expand the intent dataset and test additional user queries.
- Evaluate intent-matching accuracy on a dedicated test set.
- Add conversation export functionality.
- Deploy the application for public access.

##  Project Objective

This project demonstrates how traditional NLP techniques can be used to build a lightweight intent-based chatbot without relying on external LLM APIs.

##  Author

**Syed Kaysan Ul Islam**


---

*Built as a Python NLP project to explore text vectorization, similarity-based intent recognition, and interactive chatbot development.*
