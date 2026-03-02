import json

# Load the JSON array from the file
with open("test.py") as f:
    data = json.load(f)

# Extract messages
messages = [item["message"] for item in data if "message" in item]

# Overwrite the file with just messages, one per line
with open("test.py", "w") as f:
    f.write("\n".join(messages))