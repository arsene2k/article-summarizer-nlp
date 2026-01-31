A Python desktop application that helps users quickly understand online articles by generating summaries, analyzing sentiment, optionally translating content into French, and supporting lightweight fact-checking.

🎓 Built as a final year Computer Science project, with a strong focus on combining NLP libraries thoughtfully and evaluating their real-world limitations — not just using them blindly.

🚀 What This App Does

✅ Paste a news article URL
✅ Generate a concise summary
✅ Adjust summary length (10%–100%)
✅ See overall sentiment (😊 😐 😞)
✅ Translate the summary to French (optional)
✅ Open fact-check links for key claims
✅ Keep a session history of articles

All through a simple desktop interface — no terminal knowledge required.

🧠 How It Works (Quick Breakdown)
📰 Article Parsing & Summarization

Uses Newspaper3k to extract and clean article text

Applies extractive summarization to select key sentences

Summary length is controlled via sentence-level trimming (NLTK)

😊 Sentiment Analysis

Uses TextBlob to calculate sentiment polarity

Displays result as Positive / Neutral / Negative + score

🌍 Translation (Optional)

Uses deep-translator to translate the summary into French

Only the summary is translated to keep the system fast and lightweight

🔎 Fact-Check Mode (Assistive)

Top summary sentences are converted into Bing search links

Opens tabs like:

https://www.bing.com/search?q=<sentence+words>


Designed to support human verification, not automated truth claims

🎯 Project Intent (Important)

⚠️ This project is not about building AI from scratch
⚠️ And not about blindly relying on libraries

✔️ It intentionally combines multiple NLP tools
✔️ Evaluates how they behave in real-world scenarios
✔️ Highlights limitations, trade-offs, and design decisions
✔️ Prioritizes usability, speed, and interpretability

This reflects an engineering + research mindset, not just feature building.

🛠 Tech Stack

🧩 Python
🖥️ Tkinter (GUI)
📰 Newspaper3k (article parsing & summarization)
🧠 NLTK (sentence tokenization)
😊 TextBlob (sentiment analysis)
🌍 deep-translator (translation)

▶️ How to Run
pip install -r requirements.txt
python main.py


ℹ️ The required NLTK tokenizer (punkt) is downloaded automatically on first run.

🔐 Demo Login
Username: demo
Password: demo


(Demo credentials included for testing and review.)

⚠️ Known Limitations

Extractive summarization only (no transformer models)

Desktop-only application

English → French translation only

Sentiment analysis is lexicon-based

Fact-checking is assistive, not automated

These are intentional design choices, aligned with performance and clarity.