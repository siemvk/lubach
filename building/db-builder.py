import webvtt
import os
import json

VEEL_LOGGING = False

def log(message) -> None:
    if VEEL_LOGGING:
        print(message)

output = []

files = os.listdir("lubach")
log(files)
print("We have " + str(len(files)) + " files to process.")

for file in files:
    if file.endswith(".vtt"):
        print("We lubaching: " + file)
        for caption in webvtt.read('lubach/' + file):
            log(f"From: {caption.start} To: {caption.end}")
            log(f"Text: {caption.text}")
            log(f"Video: {file.split('.')[0]}")
            output.append({
                "start": caption.start,
                "end": caption.end,
                "text": caption.text,
                "video": file.split(".")[0],
            })

with open("output.json", "w") as f:
    json.dump(output, f, indent=4)