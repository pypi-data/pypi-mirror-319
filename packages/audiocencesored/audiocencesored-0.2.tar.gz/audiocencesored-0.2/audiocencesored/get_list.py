import requests

def download_list(output_file="bad_words.txt"):
    url = "https://raw.githubusercontent.com/sleepingcat4/audio-profanity/refs/heads/master/bad_words.txt"
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, "w") as f:
            f.write(response.text)
        print(f"File downloaded successfully: {output_file}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
