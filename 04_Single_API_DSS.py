from openai import OpenAI
from dotenv import load_dotenv
import os
import glob
import json
import time

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Define the path to JSON files and load the system prompt
path_jsons = "output_prompts/single_call/"
api_calls = glob.glob(os.path.join(path_jsons, '*.json'))

ongoing_system_prompt = "Use the list provided before and categorize the provided playbook within that list"
with open("output_prompts/system_call.txt", "r") as file:
    categorize_system_prompt = file.read()

file_index = 1
print(api_calls)
# Process each API call
for call in api_calls:
    if file_index >= 6:
        file_index += 1
        continue
    else:
        print(f"Starting API Call #{file_index}:")
        with open(call, "r") as j:
            content = j.read()
            json_data = json.loads(content)
            user_prompts = json_data["body"]["messages"][1:]
            message_ongoing = [
                {
                    "role": "system",
                    "content": categorize_system_prompt
                }
            ]
            print(f"Appending {len(user_prompts)}")
            for prompt in user_prompts:
                message_ongoing.append(prompt)

           # print(message_ongoing)
            # Uncomment the following lines to make the API call
            completion = client.chat.completions.create(
                 model="gpt-4o",
                 response_format={"type": "json_object"},
                 messages=message_ongoing,
                 temperature=0.1,
             )

            with open(f"API_Results/{file_index}_answer.json", "w") as answer:
                print(f"Writing #{file_index} to the json file")
                # Uncomment the following line to write the API response to the file
                answer.write(str(completion.choices[0].message.content))
            print(f"Pausing after API Call #{file_index}")

            time.sleep(70)
            print(f"Resuming action with #{file_index}")
            file_index += 1