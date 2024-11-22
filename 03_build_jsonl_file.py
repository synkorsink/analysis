from openai import OpenAI
import pandas as pd
import json
# client = OpenAI()

dataset_path = "input/playbooks.csv"

df = pd.read_csv(dataset_path)
df.head()
print(df)

with open("output_prompts/system_call.txt", "r") as file:
  categorize_system_prompt = file.read()

ongoing_system_prompt = "Use the list provided before and categorize the provided playbook within that list"

tasks_global = []
def create_context_task(id, user_prompt):
  task = {
    "custom_id": f"task-{id}",
    "method": "POST",
    "url": "/v1/chat/completions",
    "body": {
      # This is what you would have in your Chat Completions API call
      "model": "gpt-4o",
      "temperature": 0.1,
      "response_format": {
        "type": "json_object"
      },
      "messages": [
        {
          "role": "system",
          "content": categorize_system_prompt
        },
        {
          "role": "user",
          "content": user_prompt
        }
      ],
    }
  }
  print(task)
  return task

def create_task_list_ongoing():
  tasks = []

  for index, row in df.iterrows():
    description = row['playbook_description']
    id = row['id']
    name = row['playbook_name']
    print(id)
    playbook_prompt = f'Name: {name}; Description: {description}'

    task = {
      "custom_id": f"task-{id}",
      "method": "POST",
      "url": "/v1/chat/completions",
      "body": {
        # This is what you would have in your Chat Completions API call
        "model": "gpt-4o",
        "temperature": 0.1,
        "response_format": {
          "type": "json_object"
        },
        "messages": [
          {
            "role": "system",
            "content": categorize_system_prompt
          },
          {
            "role": "user",
            "content": playbook_prompt
          }
        ],
      }
    }
    #print(task)
    tasks.append(task)
  return tasks
# This approach can be used for generating 5 different chat tasks, each providing the necessary context:
def create_task_list_x5():
  tasks = []
  starting_index = 0
  ending_index = 90
  for i in range(14):
    print(f"Iteration {i + 1}")
    task = {
      "custom_id": f"task-{i+1}",
      "method": "POST",
      "url": "/v1/chat/completions",
      "body": {
        # This is what you would have in your Chat Completions API call
        "model": "gpt-4o",
        "temperature": 0.1,
        "response_format": {
          "type": "json_object"
        },
        "messages": [
          {
            "role": "system",
            "content": categorize_system_prompt
          },
        ],
      }
    }
    df_sliced = df.iloc[starting_index:ending_index]
   # print(df_sliced.head())
    for index, row in df_sliced.iterrows():

      description = row['playbook_description']
      id = row['id']
      name = row['playbook_name']
      print(id)
      playbook_prompt = f'ID: {id}; Name: {name}; Description: {description}'

      additional_message = {
        "role": "user",
        "content": f"{playbook_prompt}"
      }

      task["body"]["messages"].append(additional_message)
    starting_index += 90
    ending_index += 90
    tasks.append(task)
  return tasks


#tasks_final = create_task_list_ongoing()
tasks_x5 = create_task_list_x5()
index_tasks = 0
print(type(tasks_x5[2]))


for i in range(14):
  with open(f"output_prompts/single_call/tasks_{i+1}.json", "w") as j:
    task_json = json.dumps(tasks_x5[index_tasks])
    j.write(task_json)
    j.close()
    index_tasks += 1
