from openai import OpenAI
import os
import base64
from dotenv import load_dotenv

# Load API Key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Convert JPG frames to base64
def convert_frames_to_base64(frames_dir):
    base64_frames = []
    for filename in sorted(os.listdir(frames_dir)):
        if filename.endswith(".jpg"):
            with open(os.path.join(frames_dir, filename), "rb") as image_file:
                base64_frames.append(base64.b64encode(image_file.read()).decode("utf-8"))
    return base64_frames

frames_dir = "frames"
base64_frames = convert_frames_to_base64(frames_dir)
print(f"Converted {len(base64_frames)} frames to base64.")

# Load and prompt model
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

prompt_messages = [
    {
        "role": "user",
        "content": [
            "These are frames from a security camera footage of a robbery. You are a security officer tasked with filling out a theft incident report form. Identify and describe the following for each suspect: race, gender, whether or not the suspect was armed (you must be extremely sensitive to possible arms), the attire each suspect was wearing and the color of the attire, and whether or not the frame is a good still shot photo of the suspect. Also, determine the duration of the incident, the start time of the incident, and the date of the incident. Please also provide a detailed general summary of the incident.",
            *map(lambda x: {"image": x, "resize": 768}, base64_frames),
        ],
    },
]

params = {
    "model": "gpt-4o",
    "messages": prompt_messages,
    "max_tokens": 500,
}

result = client.chat.completions.create(**params)

response_content = result.choices[0].message.content
print(response_content)

response_file = "response_content.txt"
with open(response_file, mode="w") as file:
    file.write(response_content)

print(f"Response content saved to {response_file}")