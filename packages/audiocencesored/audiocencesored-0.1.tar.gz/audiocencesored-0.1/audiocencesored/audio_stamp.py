import whisper
import json

def transcribe_timestamps(audio_file, output_file):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file, word_timestamps=True)
    
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
    
    print(result["text"])