import pandas as pd
import Comparison_Helper as comp_helper


def read_comparison_data(data):
    # Iterate "bindings" arrays
    bindings = data["off_to_def"]["results"]["bindings"]

    tac_tech_dict = {}
    artifact_tech_dict = {}

    for binding in bindings:
        tactic = read_def_tactic(binding, tac_tech_dict)
        artifact = read_artifact(binding, artifact_tech_dict)
        read_def_tech(binding, tac_tech_dict, tactic, artifact_tech_dict, artifact)

    for tactic, tech_set in tac_tech_dict.items():
        print(f"Tactic: {tactic}, Techniques: {tech_set}")

    for artifact, tech_set in artifact_tech_dict.items():
        print(f"Artifact: {artifact}, Techniques: {tech_set}")

    dict_total = {
        "dict_tac_tech": tac_tech_dict,
        "dict_artifact_tech": artifact_tech_dict
    }

    return dict_total


def read_def_tactic(binding, tac_tech_dict):
    if "def_tactic_label" in binding:
        tactic = binding["def_tactic_label"]["value"]
        tac_tech_dict.setdefault(tactic, set())

        return tactic


def read_artifact(binding, artifact_tech_dict):
    if "off_artifact_label" in binding:
        artifact = binding["off_artifact_label"]["value"]
        artifact_tech_dict.setdefault(artifact, set())

        return artifact


def read_def_tech(binding, tac_tech_dict, tactic, artifact_tech_dict, artifact):
    if "def_tech_parent_is_toplevel" in binding:
        is_midlevel_tech = binding["def_tech_parent_is_toplevel"]["value"].lower() == "true"

        if is_midlevel_tech and "def_tech_label" in binding:
            tech = binding["def_tech_label"]["value"]

        elif not is_midlevel_tech and "def_tech_parent_label" in binding:
            tech = binding["def_tech_parent_label"]["value"]

        tech = tech.replace(' ', '')

        if tech == "DefensiveTechnique":
            tech = binding["def_tech_label"]["value"]
            tac_tech_dict[tactic].update(dict_level2_techs[tech])
            artifact_tech_dict[artifact].update(dict_level2_techs[tech])
        else:
            tac_tech_dict[tactic].add(tech)
            artifact_tech_dict[artifact].add(tech)


def is_technique_covered_by_playbooks(technique):
    if technique not in defend_techs_covered:
        defend_techs_covered[technique] = df_playbooks['Techniques'].apply(lambda x: technique in x).any()
    return defend_techs_covered[technique]


list_attack_techs = comp_helper.get_mitre_attack_techs()

defend_techs_covered = {}
df_results = pd.DataFrame(columns=['Attack_id', 'Attack_tactics', 'Model', 'Harden', 'Detect', 'Isolate', 'Deceive', 'Evict', 'Restore', 'Total', 'Artifact', 'Model_missing', 'Harden_missing',
                                   'Detect_missing', 'Isolate_missing', 'Deceive_missing', 'Evict_missing', 'Restore_missing', 'Model_covered', 'Harden_covered', 'Detect_covered',
                                   'Isolate_covered', 'Deceive_covered', 'Evict_covered', 'Restore_covered', 'Artifact_missing'])


#list_level2_tech = ["DefensiveTechnique", "AssetInventory", "NetworkMapping", "OperationalActivityMapping", "SystemMapping", "ApplicationHardening", "CredentialHardening", "MessageHardening", "PlatformHardening", "FileAnalysis", "IdentifierAnalysis", "MessageAnalysis", "NetworkTrafficAnalysis", "PlatformMonitoring", "ProcessAnalysis", "UserBehaviorAnalysis", "ExecutionIsolation", "NetworkIsolation", "DecoyEnvironment", "DecoyObject", "CredentialEviction", "ObjectEviction", "ProcessEviction", "RestoreAccess", "RestoreObject"]
dict_level2_techs = {
    "Decoy Environment": ["ConnectedHoneynet", "IntegratedHoneynet", "StandaloneHoneynet"],
    "File Analysis": ["DynamicAnalysis", "EmulatedFileAnalysis", "FileContentAnalysis", "FileHashing"]
}

# Tech Lists for Top X:
list_top10 = ["T1203", "T1499", "T1190", "T1059", "T1498", "T1548", "T1068", "T1505", "T1027", "T1083"]
list_top15 = ["T1203", "T1499", "T1190", "T1059", "T1498", "T1548", "T1068", "T1505", "T1027", "T1083", "T1070", "T1204", "T1071", "T1105", "T1553"]
list_top20 = ["T1203", "T1499", "T1190", "T1059", "T1498", "T1548", "T1068", "T1505", "T1027", "T1083", "T1070", "T1204", "T1071", "T1105", "T1553", "T1556", "T1055", "T1562", "T1033", "T1550", "T1574"]

df_playbooks = comp_helper.read_playbooks()


for attack_tech in list_attack_techs:

    #if attack_tech["attack_id"] not in list_top20:
    #    continue

    #if attack_tech["attack_id"] != "T1553":
    #    continue

    api_url_attack = "https://d3fend.mitre.org/api/offensive-technique/attack/" + attack_tech["attack_id"] + ".json"
    api_data = comp_helper.call_api(api_url_attack)
    dict_defend = read_comparison_data(api_data)

    total_techs = 0
    total_techs_covered = 0

    next_index = len(df_results)
    df_results.at[next_index, "Attack_id"] = attack_tech["attack_id"]
    df_results.at[next_index, "Attack_tactics"] = attack_tech["tactics"]

    for tactic, set_techs in dict_defend["dict_tac_tech"].items():

        list_covered_techs = []
        for technique in set_techs:
            if is_technique_covered_by_playbooks(technique):
                list_covered_techs.append(technique)

        list_missing_techs = [technique for technique in set_techs if technique not in list_covered_techs]

        coverage_in_tactic = len(list_covered_techs) / len(set_techs)
        df_results.at[next_index, tactic] = coverage_in_tactic

        total_techs_covered += len(list_covered_techs)
        total_techs += len(set_techs)

        df_results.at[next_index, tactic + "_missing"] = list_missing_techs
        df_results.at[next_index, tactic + "_covered"] = list_covered_techs

    if total_techs != 0:
        total = total_techs_covered / total_techs
        df_results.at[next_index, 'Total'] = total

# ------------------------------------------------------------
# Artifacts Coverage

    list_missing_artifacts = []
    count_covered_artifacts = 0
    counter_irrelevant_artifacts = 0
    for artifact, set_techs in dict_defend["dict_artifact_tech"].items():

        is_increased = False
        for technique in set_techs:
            if is_technique_covered_by_playbooks(technique):
                count_covered_artifacts += 1
                is_increased = True
                break

        if not is_increased and len(set_techs) != 0:
            list_missing_artifacts.append(artifact)

        if len(set_techs) == 0:
            counter_irrelevant_artifacts += 1

    if len(dict_defend["dict_artifact_tech"]) != 0:
        count_relevant_artifacts = len(dict_defend["dict_artifact_tech"]) - counter_irrelevant_artifacts

        if count_relevant_artifacts > 0:
            coverage_in_artifacts = 1 - (len(list_missing_artifacts) / count_relevant_artifacts)
            df_results.at[next_index, "Artifact"] = coverage_in_artifacts
            df_results.at[next_index, "Artifact_missing"] = list_missing_artifacts


pd.set_option("display.max_columns", None)
print(df_results)

df_results.to_csv("Files/results_v17.csv", index=False)





















