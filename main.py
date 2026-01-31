import tkinter as tk
from tkinter import messagebox, ttk
import nltk
from textblob import TextBlob
from newspaper import Article
from nltk.tokenize import sent_tokenize
from deep_translator import GoogleTranslator
from datetime import datetime
import webbrowser
import os 
import subprocess  # To open URLs reliably on Windows

# Download the Punkt tokenizer for sentence splitting
nltk.download('punkt', quiet=True)

# Store the history of summarized URLs and their timestamps
history = []

#  Fact-check helper function ---
def fact_check_summary(summary_text):
    sentences = sent_tokenize(summary_text)
    top_sentences = sentences[:3]  # Take up to 3 claims
    for sent in top_sentences:
        try:
            query = sent.strip().replace(" ", "+")
            url = f"https://www.bing.com/search?q={query}"
            webbrowser.open_new_tab(url)
        except Exception as e:
            print("Fact-check error:", e)

#  handles the core summarization logic
def summarize():
    url = utext.get('1.0', "end").strip()
    if not url:
        print("No URL provided")
        return

    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
    except Exception as e:
        print("Error processing article:", e)
        return

    # Trim summary based on slider percentage
    summary_length_percentage = int(length_slider.get())
    sentences = sent_tokenize(article.summary)
    num_sentences = max(1, int(len(sentences) * (summary_length_percentage / 100.0)))
    final_summary = '. '.join(sentences[:num_sentences])
    if final_summary and not final_summary.endswith('.'):
        final_summary += '.'

    # Optionally translate to French
    if translate_var.get() == 1:
        try:
            translated = GoogleTranslator(source='auto', target='fr').translate(final_summary)
            final_summary = translated
        except Exception as e:
            final_summary += "\nTranslation Error: " + str(e)

    # Perform sentiment analysis
    analysis = TextBlob(article.text)
    polarity = analysis.sentiment.polarity
    sentiment_result = (
        f"{ 'Positive 😊' if polarity > 0 else 'Negative 😞' if polarity < 0 else 'Neutral 😐' } ({polarity:.2f})"
    )

    # Insert data into text fields
    for widget in [title, author, publication, summary, sentiment]:
        widget.config(state='normal')
        widget.delete('1.0', tk.END)

    title.insert(tk.END, article.title)
    author.insert(tk.END, ", ".join(article.authors))
    publication.insert(tk.END, str(article.publish_date))
    summary.insert(tk.END, final_summary)
    if translate_var.get() == 1:
        messagebox.showinfo("Translation Successful", "The summary has been successfully translated to French.")
    sentiment.insert(tk.END, sentiment_result)

    for widget in [title, author, publication, summary, sentiment]:
        widget.config(state='disabled')

    # Run fact check if selected
    if fact_check_var.get() == 1:
        fact_check_summary(final_summary)
        messagebox.showinfo("Fact Check", "Opened browser tabs to help verify top claims in the summary.")

    # Store in history
    utext.config(state='normal')
    utext.delete('1.0', tk.END)
    utext.insert(tk.END, url)
    utext.config(state='normal')

    history.append((url, datetime.now().strftime("%Y-%m-%d %H:%M")))
    messagebox.showinfo("Success", "Article has been summarized successfully!")

# Show user's history in a new window
def show_history():
    history_win = tk.Toplevel(root)
    history_win.title("History")
    history_win.geometry("700x400")

    tree = ttk.Treeview(history_win, columns=("Link", "Date"), show="headings")
    tree.heading("Link", text="Link")
    tree.heading("Date", text="Date")
    tree.column("Link", width=500)
    tree.column("Date", width=150)
    tree.pack(expand=True, fill='both')

    for link, date in history:
        tree.insert('', 'end', values=(link, date))

    def open_link(event):
        item = tree.identify_row(event.y)
        col = tree.identify_column(event.x)
        if col == '#1' and item:
            values = tree.item(item)['values']
            if values:
                url = values[0]
                webbrowser.open(url)

    tree.bind('<Double-1>', open_link)

# Launch the summarizer GUI after successful login
def open_main_app():
    global root, utext, length_slider, translate_var, fact_check_var, title, author, publication, summary, sentiment
    login_window.destroy()

    root = tk.Tk()
    root.title("Article Summarizer")
    root.geometry("1000x700")
    root.resizable(True, True)
    root.config(bg='#e3f2fd')

    frame_title = tk.Frame(root, bg='#e3f2fd')
    frame_title.pack(pady=5)
    tk.Label(frame_title, text="Title 📖", font=("Helvetica", 14, 'bold'), bg='#e3f2fd').pack()
    title = tk.Text(frame_title, height=1, width=80, bg='#ffffff', font=("Arial", 12))
    title.config(state='disabled')
    title.pack()

    frame_author = tk.Frame(root, bg='#e3f2fd')
    frame_author.pack(pady=5)
    tk.Label(frame_author, text="Author 👨‍💻", font=("Helvetica", 14, 'bold'), bg='#e3f2fd').pack()
    author = tk.Text(frame_author, height=1, width=80, bg='#ffffff', font=("Arial", 12))
    author.config(state='disabled')
    author.pack()

    frame_publication = tk.Frame(root, bg='#e3f2fd')
    frame_publication.pack(pady=5)
    tk.Label(frame_publication, text="Publishing Date 📅", font=("Helvetica", 14, 'bold'), bg='#e3f2fd').pack()
    publication = tk.Text(frame_publication, height=1, width=80, bg='#ffffff', font=("Arial", 12))
    publication.config(state='disabled')
    publication.pack()

    frame_summary = tk.Frame(root, bg='#e3f2fd')
    frame_summary.pack(pady=5)
    tk.Label(frame_summary, text="Summary 📝", font=("Helvetica", 14, 'bold'), bg='#e3f2fd').pack()
    summary = tk.Text(frame_summary, height=8, width=80, bg='#ffffff', font=("Arial", 12))
    summary.config(state='disabled')
    scrollbar = tk.Scrollbar(frame_summary, command=summary.yview)
    summary.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    summary.pack()

    frame_sentiment = tk.Frame(root, bg='#e3f2fd')
    frame_sentiment.pack(pady=5)
    tk.Label(frame_sentiment, text="Sentiment Analysis 🙂", font=("Helvetica", 14, 'bold'), bg='#e3f2fd').pack()
    sentiment = tk.Text(frame_sentiment, height=1, width=80, bg='#ffffff', font=("Arial Unicode MS", 12))
    sentiment.config(state='disabled')
    sentiment.pack()

    frame_url = tk.Frame(root, bg='#e3f2fd')
    frame_url.pack(pady=5)
    tk.Label(frame_url, text="URL 🌐", font=("Helvetica", 14, 'bold'), bg='#e3f2fd').pack()
    utext = tk.Text(frame_url, height=1, width=80, bg='#ffffff', font=("Arial", 12))
    utext.pack()

    frame_options = tk.Frame(root, bg='#e3f2fd')
    frame_options.pack(pady=5)

    frame_slider = tk.Frame(frame_options, bg='#e3f2fd')
    frame_slider.pack(side=tk.LEFT, padx=10)
    tk.Label(frame_slider, text="Summary Length (%)", font=("Helvetica", 14), bg='#e3f2fd').pack()
    length_slider = tk.Scale(frame_slider, from_=10, to=100, orient="horizontal")
    length_slider.set(100)
    length_slider.pack()

    frame_translate_fact = tk.Frame(frame_options, bg='#e3f2fd')
    frame_translate_fact.pack(side=tk.LEFT, padx=10)

    translate_var = tk.IntVar()
    tk.Checkbutton(frame_translate_fact, text="Translate Summary to French", variable=translate_var, font=("Arial", 12)).pack(anchor='w')

    fact_check_var = tk.IntVar()
    tk.Checkbutton(frame_translate_fact, text="Enable Fact-Check Mode", variable=fact_check_var, font=("Arial", 12)).pack(anchor='w')

    frame_button = tk.Frame(root, bg='#e3f2fd')
    frame_button.pack(pady=10, anchor='center')
    tk.Button(frame_button, text="Summarize", command=summarize, font=("Arial", 14, 'bold'), bg='#4CAF50', fg='white', padx=20, pady=10).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_button, text="History", command=show_history, font=("Arial", 12), bg='#2196F3', fg='white', padx=10, pady=10).pack(side=tk.LEFT, padx=10)

    root.mainloop()

# Simple login screen for access control
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x200")
login_window.config(bg='#e3f2fd')

tk.Label(login_window, text="Username", font=("Arial", 12), bg='#e3f2fd').pack(pady=5)
username_entry = tk.Entry(login_window, font=("Arial", 12))
username_entry.pack(pady=5)

tk.Label(login_window, text="Password", font=("Arial", 12), bg='#e3f2fd').pack(pady=5)
password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
password_entry.pack(pady=5)

def validate_login():
    if username_entry.get() == "arsene" and password_entry.get() == "pass":
        open_main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

tk.Button(login_window, text="Login", command=validate_login, font=("Arial", 12), bg='#4CAF50', fg='white').pack(pady=10)

login_window.mainloop()
