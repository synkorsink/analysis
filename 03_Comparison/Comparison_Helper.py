import json
import requests
import pandas as pd
import ast
import os
import zipfile
import subprocess

playbook_file = 'Files/pb_mapping_iteration2 1.csv'
mitre_attack_file = 'Files/enterprise-attack-15.1.json'


def get_all_off_techs(data):
    off_techs_list = data["@graph"]

    set_off_techs = set()
    for off_tech in off_techs_list:
        set_off_techs.add(off_tech["d3f:attack-id"])

    return set_off_techs


def call_api(url):
    api_data = requests.get(url).json()
    api_data = json.dumps(api_data)

    # JSON-String to Python objekt
    data = json.loads(api_data)
    return data


def get_mitre_attack_techs():
    with open(mitre_attack_file, 'r', encoding='utf-8') as file_input:
        data = json.load(file_input)

        list_objects = data["objects"]
        list_techs = []

        for obj in list_objects:
            if obj["type"] == "attack-pattern" and not obj.get("x_mitre_deprecated", False) and not obj.get("revoked", False) and not obj["x_mitre_is_subtechnique"]:
                name = obj["name"]

                ext_refs = obj["external_references"]
                for ref in ext_refs:
                    if ref["source_name"] == "mitre-attack":
                        attack_id = ref["external_id"]
                        break

                list_tactics = set()
                kill_phases = obj["kill_chain_phases"]
                for phase in kill_phases:
                    if phase["kill_chain_name"] == "mitre-attack":
                        list_tactics.add(phase["phase_name"])

                technique = {
                    "attack_id": attack_id,
                    "name": name,
                    "tactics": list_tactics
                }

                list_techs.append(technique)

        list_techs = sorted(list_techs, key=lambda x: x['attack_id'])

        df_techs = pd.DataFrame(list_techs)
        df_techs.to_csv('Files/mitre_attack.csv', index=False)

        return list_techs


def download_cve_kaggle_data():
    # Step 2: Define the dataset identifier
    dataset_identifier = 'synkorsink/cve-attack-ttp'  # Replace with your dataset identifier

    # Step 3: Create a directory to store the dataset
    os.makedirs('kaggle_dataset', exist_ok=True)

    # Step 4: Download the dataset
    try:
        subprocess.run(
            ['kaggle', 'datasets', 'download', '-d', dataset_identifier, '-p', 'kaggle_dataset', '--force'],
            check=True
        )
    except FileNotFoundError:
        raise RuntimeError(
            "Kaggle CLI not found. Please ensure you have the Kaggle CLI installed and properly configured.")

    # Step 5: List all downloaded files
    downloaded_files = os.listdir('kaggle_dataset')

    # Step 6: Extract all zip files in the directory
    for file_name in downloaded_files:
        if file_name.endswith('.zip'):
            with zipfile.ZipFile(os.path.join('kaggle_dataset', file_name), 'r') as zip_ref:
                zip_ref.extractall('kaggle_dataset')

    attack_df = pd.read_csv('kaggle_dataset/cve_attack_mapping.csv')
    # Save the DataFrame to a CSV file
    attack_df.to_csv('cve_attack_mapping.csv', index=False)

    attack_df.head(10)
    return attack_df

def get_CVE_data():
    #cve_file = 'Files/kaggle_dataset/results.csv'
    #df = pd.read_csv(cve_file)

    df = download_cve_kaggle_data()

    df_filtered = df[df['confidence'] > 0.175]

    # Filter descriptions starting with 'Rejected'
    df_filtered = df_filtered[~df_filtered['description'].str.startswith('Rejected')]

    cve_count = df_filtered['cve_id'].nunique()
    #print(f"Anzahl CVEs: {cve_count}")

    attack_technique_count = len(df_filtered)
    #print(f"Count Attack Techniques: {attack_technique_count}")

    df_sorted = df_filtered.sort_values(by='cve_id')

    return df_sorted


def read_playbooks():
    df_playbooks = pd.read_csv(playbook_file)

    # First split the column into two
    df_playbooks[['Name', 'Techniques']] = df_playbooks['Playbook'].str.split('; ', expand=True)

    # The 'Techniques' column contains strings that look like lists, so we convert them into real lists
    df_playbooks['Techniques'] = df_playbooks['Techniques'].apply(ast.literal_eval)

    return df_playbooks



