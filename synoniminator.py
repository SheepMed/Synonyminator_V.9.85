import requests
import re

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
        print(f"Synonyms for '{word}':")
        for idx, synonym in enumerate(synonyms, start=1):
            print(f"{idx}. {synonym}")
    else:
        print(f"No synonyms found for '{word}'.")

def main():
    word = input("Enter a word: ")
    synonyms = fetch_synonyms(word)
    display_synonyms(synonyms, word)

if __name__ == "__main__":
    main()
