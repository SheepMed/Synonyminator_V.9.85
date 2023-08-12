import requests
import re
import tkinter as tk
from tkinter import messagebox, scrolledtext

def fetch_synonyms(word):
    url = f"https://www.thesaurus.com/browse/{word}"
    response = requests.get(url)    
    synonyms = []
    if response.status_code == 200:
        page_content = response.text
        synonyms_text = re.search(r'"synonyms":\[(.*?)\]', page_content).group(1)
        synonyms = [syn.strip('"\t ') for syn in re.findall(r'"term":"(.*?)"', synonyms_text) if not any(flag in syn for flag in ["target", "similarity", "isinformal", "isvulgar"])]    
    return synonyms

def display_synonyms(synonyms, word):
    if synonyms:
        synonyms_output.config(state=tk.NORMAL)
        synonyms_output.delete("1.0", tk.END)
        synonyms_output.insert(tk.END, f"Synonyms for '{word}':\n")
        for idx, synonym in enumerate(synonyms, start=1):
            synonyms_output.insert(tk.END, f"{idx}. {synonym}\n")
        synonyms_output.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("No Synonyms", f"No synonyms found for '{word}'.")

def find_synonyms():
    word = entry_word.get()
    synonyms = fetch_synonyms(word)
    display_synonyms(synonyms, word)
app = tk.Tk()
app.title("Synonym Finder")
label_word = tk.Label(app, text="Enter a word:")
entry_word = tk.Entry(app)
button_find = tk.Button(app, text="Find Synonyms", command=find_synonyms)
synonyms_output = scrolledtext.ScrolledText(app, state=tk.DISABLED, wrap=tk.WORD)
label_word.pack(pady=5)
entry_word.pack(pady=5)
button_find.pack(pady=5)
synonyms_output.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
app.mainloop()
