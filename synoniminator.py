import requests
import re
import tkinter as tk
from tkinter import messagebox, scrolledtext

def fetch_words(word, is_synonym=True):
    url = f"https://www.thesaurus.com/browse/{word}"
    response = requests.get(url)    
    words = []
    if response.status_code == 200:
        page_content = response.text
        key = "synonyms" if is_synonym else "antonyms"
        words_text = re.search(rf'"{key}":\[(.*?)\]', page_content).group(1)
        words = [w.strip('"\t ') for w in re.findall(r'"term":"(.*?)"', words_text) if not any(flag in w for flag in ["target", "similarity", "isinformal", "isvulgar"])]
    
    return words

def display_words(words, word, is_synonym=True):
    words_output.config(state=tk.NORMAL)
    words_output.delete("1.0", tk.END)
    
    if words:
        key = "Synonyms" if is_synonym else "Antonyms"
        words_output.insert(tk.END, f"{key} for '{word}':\n")
        for idx, w in enumerate(words, start=1):
            words_output.insert(tk.END, f"{idx}. {w}\n")
    else:
        key = "Synonyms" if is_synonym else "Antonyms"
        words_output.insert(tk.END, f"No {key.lower()} found for '{word}'.\n")
    
    words_output.config(state=tk.DISABLED)

def find_words(is_synonym=True):
    word = entry_word.get()
    words = fetch_words(word, is_synonym)
    display_words(words, word, is_synonym)
app = tk.Tk()
app.title("Sheep Synonyminator")
label_word = tk.Label(app, text="Enter a word:")
entry_word = tk.Entry(app)
button_find_synonyms = tk.Button(app, text="Find Synonyms", command=lambda: find_words(is_synonym=True))
button_find_antonyms = tk.Button(app, text="Find Antonyms", command=lambda: find_words(is_synonym=False))
words_output = scrolledtext.ScrolledText(app, state=tk.DISABLED, wrap=tk.WORD)
label_word.pack(pady=5)
entry_word.pack(pady=5)
button_find_synonyms.pack(pady=5)
button_find_antonyms.pack(pady=5)
words_output.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
app.mainloop()
