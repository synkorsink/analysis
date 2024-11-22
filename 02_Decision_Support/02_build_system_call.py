# Combine the Information gathere by 01_load_Defend_JSON.py and the Playbook Parser, into Prompts
# The prmots must be in the OPENAPI Batch Format

import pandas as pd
import os
import glob


directory_path = 'output_defend/'
prompt_system_1 = '''
After this prompt you will be presented with 90 different cyber security instructions called playbooks with their Name and Description.
Your job is to name the four best fitting cyber security defensive techniques, provided by the following list (The format of the list is [Name of the technique]:[Description]).
Base the categorization on the Name and the Description and only return the three techniques for each of the 90 provided playbooks as a json object. If a categorization is not possible return the playbook id with empty Categories.
Choose the most fitting four techniques in the following format, replacing the content of the bracket with the found categorization and within the asterisk with the playbook id:
    {*Playbook id*: [{1:(Choice Number 1)}, {2:(Choice Number 2)}, {3:(Choice Number 3)}, {4:(Choice Number 4)}]}
Choose ONLY from the provided list and the returned json object should return a value for EACH of the 90 playbooks:'''

# - AccessModeling: Access modeling identifies and records the access permissions granted to administrators, users, groups, and systems.
system_only_count = len(prompt_system_1)
system_count = 0
count_batch = 0
count_only_batch = 0
playbook_chars = 0
count_single_system_plus_pb = 0
def transform_defend_to_jsonline():
    defend_files = glob.glob(os.path.join(directory_path, '*.txt'))

    with open('output_prompts/system_call.txt', 'w') as empty:
        empty.write(prompt_system_1)
        empty.close()

    for technique in defend_files:
        file_name = os.path.basename(technique)[0:-4]
        print(file_name)
        with open(technique, 'r') as f:
            content = f.read()
            with open('output_prompts/system_call.txt', 'a') as sc:
                sc.write('\n')
                sc.write(f'- {file_name}: {content}')
                sc.close()
            f.close()

    with open('output_prompts/system_call.txt', 'r') as count:
        global system_count
        global count_only_batch
        global count_single_system_plus_pb
        content = count.read()
        print(len(content))
        system_count += len(content)
        final_system_count = 5* system_count
        print(f'Ein einzelner System Call: {system_count}')
        count_only_batch += final_system_count
        print(f'5x der System count: {final_system_count}')


def calculate_pricing(count_pb):
    global count_only_batch
    global count_single_system_plus_pb
    count_only_batch += count_pb
    count_single_system_plus_pb += count_pb
# -----------------------------------------

def create_playbook_json():

    df = pd.read_csv('input/playbooks.csv')

   # print(df.head())

# if you want the index use iterrows

# if you want a fast iteration use itertuples)

    for playbook in df.itertuples(index=False, name="Playbook"):
        print(f'Index: {playbook.id}; Name: {playbook.playbook_name}; {playbook.playbook_description}')
        user_string = f'Name: {playbook.playbook_name}; Description: {playbook.playbook_description}'
        calculate_pricing(len(user_string))
# -----------------------------------------

transform_defend_to_jsonline()
create_playbook_json()

print(f'Der finale Char count: {count_only_batch}')
print(f'Ein einzelner System count: {system_count}')
einzelner = system_count + (count_single_system_plus_pb/5)
print(f'Char count wenn einmalig: {einzelner} ')