from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

def test_job():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "I am just here to say hello."},
            {"role": "user", "content": "Say Hello back"}

        ]
    )
    print(completion.choices[0].message)

# ZUERST NOCH MIT DEN FRUITS TESTEN
def upload_batch(file_name, description):

    # Uploading the Batch to the API Server
    batch_input_file = client.files.create(
      file=open(f"{file_name}", "rb"),
      purpose="batch"
    )

    batch_input_file_id = batch_input_file.id
    print(f"Batch input file ID: {batch_input_file_id}")
    with open("resources/batch_file_id.txt", "w") as batch_file_id:
        batch_file_id.write(batch_input_file_id)
        batch_file_id.close()

    # Creating the final batch job
    batch_job = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
          "description": f"{description}"
        }
    )

    batch_job_id = batch_job.id
    print(f"Batch job ID: {batch_job_id}")

    with open("resources/batch_job_id.txt", "w") as batch_id_file:
        batch_id_file.write(batch_job_id)
        batch_id_file.close()

def retrieve_status(id):
    print(f'Retrieving Status of Batch-job with the ID: {id}')
    batch_status = client.batches.retrieve(id)
    print(batch_status)
    return batch_status

def request_status(batch_job_id):
    # Retrieve the batch job status
    batch_status = retrieve_status(batch_job_id)
    print(batch_status.output_file_id)
    with open("resources/batch_output_file_id.txt", "w") as results_id_file:
        if batch_status.output_file_id == None:
            results_id_file.write("None")
        else:
            results_id_file.write(batch_status.output_file_id)
    with open("resources/batch_error_file_id.txt", "w") as error_file_id:
        if batch_status.error_file_id == None:
            error_file_id.write("None")
        else:
            error_file_id.write(batch_status.error_file_id)

def request_results(file_id):
    # Extract the result file ID from the batch status
    print(f"Result file ID: {file_id}")

    # Retrieve and print the results from the result file
    file_response = client.files.content(file_id)
    with open("API_Results/results.jsonl", "w") as results_doc:
        results_doc.write(file_response.text)
        print(file_response.text)

def request_errors(error_id):
    print(f"Error file ID: {error_id}")
    error_response = client.files.content(error_id)
    with open("API_Results/errors.jsonl", "w") as errors_doc:
        errors_doc.write(error_response.text)
        print(error_response.text)

def cancel_batch(batch_id):
    client.batches.cancel(batch_id)

def get_all_batches():
    batches = client.batches.list(limit=10)
    print(batches)

def kill_all_batches():
    batches = get_all_batches()
    # print(type(batc))
# ----------------------

# ---------------------------------
# Uncomment this to send a Test API Call like Hello Worlds
# test_job()

# Ucomment this to upload your batch file to the server an start the batch job
description_defend = "Classifying Playbooks"
path_to_tasks = "output_prompts/tasks.jsonl"
path_to_test_tasks = "playbooks_test.jsonl"
path_to_fruits = "api_test_prompt.jsonl"


# !!! HERE STARTS THE PAYED JOB !!!!!!!!!!
# upload_batch(path_to_tasks, description_defend)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Use this to rquest the current status of the batch job
with open("resources/batch_job_id.txt", "r") as batch_id_file:
    batch_job_id = batch_id_file.read().strip()

request_status(batch_job_id)


# -----------------------------
# 1. Read the current file output id
with open("resources/batch_output_file_id.txt", "r") as output_id_txt:
    final_results_id = output_id_txt.read().strip()

with open("resources/batch_error_file_id.txt", "r") as error_id_txt:
    error_results_id = error_id_txt.read().strip()

# 2. Uncomment to pull the results from the Server
if final_results_id != "None":
    # request_results(final_results_id)
    print("Pulled Batch Results. Look into results.jsonl")

if error_results_id != "None":
    #request_errors(error_results_id)
    print("Sadly there were errors")

# -------------------------------------
# Additional API Operations
# Get all the batches
# get_all_batches()

# Manually kill the batch you want:
kill_id = "batch_m10MGXxWSTrZSwWtvtGZHNpS"
# cancel_batch(kill_id)
# kill_all_batches()