import json
import ast
import csv

csv_data = [['Name', 'Techniques']]
with open('Final_mappings/Categories_output_final_it1.txt', 'r') as file:
    input_list = file.readlines()
    for i in input_list:
        line = []
        name = i.split(" ")[0]
        line.append(name)
        techniques = i.split("['")[1]
        techniques = '[\'' + techniques
        list_techniques = ast.literal_eval(techniques)
        line.append(list_techniques)
       #
        csv_data.append(line)
        #for j in list_techniques:
            # print(j)

print(csv_data)
with open("Final_mappings/pb_mapping_iteration1.csv", mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for row in csv_data:
        writer.writerow(row)