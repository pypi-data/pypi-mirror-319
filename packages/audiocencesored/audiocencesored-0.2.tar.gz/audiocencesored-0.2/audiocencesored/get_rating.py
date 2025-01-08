import re

def check_profanity(word_list_file, bad_words_file, rating="R"):
    with open(word_list_file, "r") as f:
        word_list = f.read().splitlines()

    with open(bad_words_file, "r") as f:
        bad_words = f.read().splitlines()

    matching_words = []
    for word in word_list:
        for bad_word in bad_words:
            if re.search(rf"\b{re.escape(bad_word)}\b", word, re.IGNORECASE):
                matching_words.append(word)
    
    if matching_words:
        match_count = {word: matching_words.count(word) for word in set(matching_words)}
        for word, count in match_count.items():
            if count > 1:
                print(f"Word: {word} - Count: {count} ({rating} rated)")
    else:
        print("No profanity")