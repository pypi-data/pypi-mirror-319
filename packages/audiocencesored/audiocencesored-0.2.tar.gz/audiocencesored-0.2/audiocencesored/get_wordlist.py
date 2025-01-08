import json

def extract_words(json_file, output_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    word_list = []
    for segment in data["segments"]:
        for word_info in segment["words"]:
            word_list.append(word_info["word"])

    with open(output_file, "w") as f:
        f.write("\n".join(word_list))