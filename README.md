A Python desktop application designed to help users quickly understand online articles by generating concise summaries, analysing sentiment, optionally translating content into French, and supporting lightweight fact-checking.

Built as a final-year Computer Science project, the focus is on thoughtful integration of NLP libraries and critical evaluation of their real-world behaviour, rather than treating them as black-box solutions.

What the App Does

Paste a news article URL

Generate a concise summary

Adjust summary length (10%–100%)

View overall sentiment (Positive / Neutral / Negative)

Translate the summary into French (optional)

Open fact-check links for key claims

Maintain a session history of analysed articles

All functionality is delivered through a simple desktop interface, with no terminal knowledge required.

How It Works (Overview)
Article Parsing & Summarisation

Uses Newspaper3k to extract and clean article text

Applies extractive summarisation by selecting key sentences

Summary length is controlled through sentence-level trimming using NLTK

Sentiment Analysis

Uses TextBlob to calculate sentiment polarity

Outputs sentiment as Positive, Neutral, or Negative, along with a polarity score

Translation (Optional)

Uses deep-translator to translate only the generated summary into French

Limiting translation to the summary keeps the system fast and lightweight

Fact-Check Mode (Assistive)

Converts the most important summary sentences into Bing search queries

Opens browser tabs such as:
https://www.bing.com/search?q=<sentence+keywords>

This feature is designed to support human verification, not to make automated truth claims.

Project Intent

This project is not about building AI models from scratch, nor about blindly relying on third-party libraries.

Instead, it:

Combines multiple NLP tools intentionally

Evaluates how they perform in real-world scenarios

Highlights limitations, trade-offs, and design decisions

Prioritises usability, speed, and interpretability

The goal is to demonstrate an engineering and research-oriented mindset, rather than simple feature accumulation.

Tech Stack

Python

Tkinter (GUI)

Newspaper3k (article parsing & summarisation)

NLTK (sentence tokenisation)

TextBlob (sentiment analysis)

deep-translator (translation)

How to Run
pip install -r requirements.txt
python main.py


The required NLTK tokenizer (punkt) is downloaded automatically on first run.

Demo Login

Username: demo

Password: demo

(Demo credentials are included for testing and review.)

Known Limitations

Extractive summarisation only (no transformer-based models)

Desktop-only application

English to French translation only

Lexicon-based sentiment analysis

Fact-checking is assistive, not automated

These limitations are intentional design choices, aligned with performance, clarity, and transparency.
