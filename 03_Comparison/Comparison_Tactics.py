import pandas as pd
import ast
import Comparison_Helper as helper
import requests
import json
import Graphics as graphics


df_coverage = pd.read_csv("Files/results_complete_v17.csv")
list_ATTACK_tactics = ["reconnaissance", "resource-development", "initial-access", "execution", "persistence", "privilege-escalation", "defense-evasion", "credential-access", "discovery", "lateral-movement", "collection", "command-and-control", "exfiltration", "impact"]
list_ATTACK_tactics_upper_case = ["Reconnaissance", "Resource Development", "Initial Access", "Execution", "Persistence", "Privilege Escalation", "Defense Evasion", "Credential Access", "Discovery", "Lateral Movement", "Collection", "Command And Control", "Exfiltration", "Impact"]
list_D3fend_tactics = ["Model", "Harden", "Detect", "Isolate", "Deceive", "Evict", "Restore"]
list_d3fend_to_attack_mapping = []
list_current_d3fend_percentages = []
list_current_attack_percentages = []
list_target_d3fend_percentages = []
list_target_attack_percentages = []

dict_d3fend_target = {
    "Model": 0,
    "Harden": 0,
    "Detect": 0,
    "Isolate": 0,
    "Deceive": 0,
    "Evict": 0,
    "Restore": 0
}


dict_attack_current = {
    "reconnaissance": 0,
    "resource-development": 0,
    "initial-access": 0,
    "execution": 0,
    "persistence": 0,
    "privilege-escalation": 0,
    "defense-evasion": 0,
    "credential-access": 0,
    "discovery": 0,
    "lateral-movement": 0,
    "collection": 0,
    "command-and-control": 0,
    "exfiltration": 0,
    "impact": 0,
}


dict_d3fend_current = {
        "Model": 0,
        "Harden": 0,
        "Detect": 0,
        "Isolate": 0,
        "Deceive": 0,
        "Evict": 0,
        "Restore": 0
}

dict_attack_target = {
        "Reconnaissance": 0,
        "Resource Development": 0,
        "Initial Access": 0,
        "Execution": 0,
        "Persistence": 0,
        "Privilege Escalation": 0,
        "Defense Evasion": 0,
        "Credential Access": 0,
        "Discovery": 0,
        "Lateral Movement": 0,
        "Collection": 0,
        "Command And Control": 0,
        "Exfiltration": 0,
        "Impact": 0,
}


def getD3FENDTacticsForAttackTech(attack_tech):
    attack_tech_row = df_coverage.loc[df_coverage["Attack_id"] == attack_tech]

    list_no_nan = attack_tech_row.dropna(axis=1).columns.tolist()

    list_needed_D3fend_tactics = list(set(list_no_nan) & set(list_D3fend_tactics))

    return list_needed_D3fend_tactics


def add_cve_side(set_d3fend_tactics, set_attack_tactics):
    for tactic in set_d3fend_tactics:
        dict_d3fend_target[tactic] += 1

    for tactic in set_attack_tactics:
        dict_attack_current[tactic] += 1


def calculate_cve_side():
    df_cve = helper.get_CVE_data()

    counter_techs = 0
    current_cve_id = ''
    set_d3fend_tactics = set()
    set_attack_tactics = set()
    for row in df_cve.itertuples(index=False):

        if current_cve_id != row.cve_id:
            add_cve_side(set_d3fend_tactics, set_attack_tactics)
            set_d3fend_tactics.clear()
            set_attack_tactics.clear()
            current_cve_id = row.cve_id

        list_needed_D3fend_tactics = getD3FENDTacticsForAttackTech(row.attack_technique)
        set_d3fend_tactics.update(list_needed_D3fend_tactics)

        str_used_Attack_tactics = row.attack_tactic
        list_used_Attack_tactics = ast.literal_eval(str_used_Attack_tactics)
        set_attack_tactics.update(list_used_Attack_tactics)

        counter_techs += 1
        print(f"Tech: {counter_techs}")

    total_sum_target_d3fend = sum(dict_d3fend_target.values())
    total_sum_current_attack = sum(dict_attack_current.values())

    print("Target D3fend: ")
    for key, value in dict_d3fend_target.items():
        percentage_d3fend = value / total_sum_target_d3fend
        print(f"{key}: {percentage_d3fend}")
        percentage_d3fend = round(percentage_d3fend * 100, 2)
        list_target_d3fend_percentages.append(percentage_d3fend)

    print("----------------------------------------------")

    print("Current Attack: ")
    for key, value in dict_attack_current.items():
        percentage_attack = value / total_sum_current_attack
        print(f"{key}: {percentage_attack}")
        percentage_attack = round(percentage_attack * 100, 2)
        list_current_attack_percentages.append(percentage_attack)


def get_d3fend_tactics(d3fend_tech):
    found_dict = search_for_tech(d3fend_tech)
    if not found_dict:
        read_d3fend_api_technique(d3fend_tech)
        found_dict = search_for_tech(d3fend_tech)
    return found_dict["d3fend_tactic"]


def get_attack_tactics(d3fend_tech):
    found_dict = search_for_tech(d3fend_tech)
    if not found_dict:
        read_d3fend_api_technique(d3fend_tech)
        found_dict = search_for_tech(d3fend_tech)
    return found_dict["dict_d3fend_to_attack"]


def search_for_tech(d3fend_tech):
    found_dict = next((item for item in list_d3fend_to_attack_mapping if item["technique"] == d3fend_tech), None)
    return found_dict


def read_d3fend_api_technique(d3fend_tech):
    api_url = "https://d3fend.mitre.org/api/technique/d3f:" + d3fend_tech + ".json"
    try:
        data = helper.call_api(api_url)
    except requests.exceptions.JSONDecodeError:
        dict_d3fend_tech = {
            "technique": d3fend_tech,
            "dict_d3fend_to_attack": {},
            "d3fend_tactic": None
        }
        list_d3fend_to_attack_mapping.append(dict_d3fend_tech)
        return
    dict_d3fend_to_attack = {}
    matrix = data["related_offensive_matrix"]
    for tactic in list_ATTACK_tactics_upper_case:
        if tactic in matrix:
            tactic_field = matrix[tactic]

            list_techs = []
            for attack_tech in tactic_field:
                list_techs.append(attack_tech[0])

            dict_d3fend_to_attack[tactic] = list_techs

    d3fend_tactic = ''
    bindings = data["def_to_off"]["results"]["bindings"]
    for binding in bindings:
        if "def_tactic_label" in binding:
            d3fend_tactic = binding["def_tactic_label"]["value"]
            break

    dict_d3fend_tech = {
        "technique": d3fend_tech,
        "dict_d3fend_to_attack": dict_d3fend_to_attack,
        "d3fend_tactic": d3fend_tactic
    }

    list_d3fend_to_attack_mapping.append(dict_d3fend_tech)


def add_playbook_side(set_d3fend_tactics, set_attack_tactics):
    for tactic in set_d3fend_tactics:
        dict_d3fend_current[tactic] += 1

    for tactic in set_attack_tactics:
        dict_attack_target[tactic] += 1


def calculate_playbook_side():
    df_playbooks = helper.read_playbooks()

    counter = 0
    for playbook in df_playbooks.itertuples(index=False):
        print(playbook.Name)
        counter += 1
        print(counter)

        list_used_d3fend_techs = playbook.Techniques

        set_d3fend_tactics = set()
        set_attack_tactics = set()
        for d3fend_tech in list_used_d3fend_techs:

            d3fend_tactic = get_d3fend_tactics(d3fend_tech)
            if d3fend_tactic is not None and d3fend_tactic != '':
                set_d3fend_tactics.add(d3fend_tactic)

            dict_d3fend_to_attack = get_attack_tactics(d3fend_tech)
            for key, value in dict_d3fend_to_attack.items():
                set_attack_tactics.add(key)

        add_playbook_side(set_d3fend_tactics, set_attack_tactics)
        set_d3fend_tactics.clear()
        set_attack_tactics.clear()

    total_sum_current_d3fend = sum(dict_d3fend_current.values())
    total_sum_target_attack = sum(dict_attack_target.values())

    print("D3fend_current: ")
    for key, value in dict_d3fend_current.items():
        percentage_d3fend = value / total_sum_current_d3fend
        print(f"{key}: {percentage_d3fend}")
        percentage_d3fend = round(percentage_d3fend * 100, 2)
        list_current_d3fend_percentages.append(percentage_d3fend)

    print("----------------------------------------------")

    print("Attack_target")
    for key, value in dict_attack_target.items():
        percentage_attack = value / total_sum_target_attack
        print(f"{key}: {percentage_attack}")
        percentage_attack = round(percentage_attack * 100, 2)
        list_target_attack_percentages.append(percentage_attack)


with open("Files/d3fend_to_attack_v17.json", "r") as file:
    list_d3fend_to_attack_mapping = json.load(file)

calculate_playbook_side()

with open("Files/d3fend_to_attack_v17.json", "w") as file:
   json.dump(list_d3fend_to_attack_mapping, file)


calculate_cve_side()


#with open("Files/percentage_attack_current_v17.json", "r") as file:
#    list_current_attack_percentages = json.load(file)

#with open("Files/percentage_attack_target_v17.json", "r") as file:
#    list_target_attack_percentages = json.load(file)

#with open("Files/percentage_d3fend_current_v17.json", "r") as file:
#    list_current_d3fend_percentages = json.load(file)

#with open("Files/percentage_d3fend_target_v17.json", "r") as file:
#    list_target_d3fend_percentages = json.load(file)


graphics.genereateFigureAttackTactics(list_current_attack_percentages, list_target_attack_percentages)
graphics.genereateFigureD3fendTactics(list_current_d3fend_percentages, list_target_d3fend_percentages)


#with open("Files/percentage_attack_current_v17.json", "w") as file:
#    json.dump(list_current_attack, file)

#with open("Files/percentage_attack_target_v17.json", "w") as file:
#    json.dump(list_target_attack, file)

#with open("Files/percentage_d3fend_current_v17.json", "w") as file:
#    json.dump(list_current_d3fend, file)

#with open("Files/percentage_d3fend_target_v17.json", "w") as file:
#     json.dump(list_target_d3fend, file)












