import glob
import os

path_api_results = "API_Results/"

api_calls = glob.glob(os.path.join(path_api_results, '*.json'))

with open('output/merged_results.json', 'w') as sc:
    sc.close()

for call in api_calls:
    file_name = os.path.basename(call)[0:-5]
    print(file_name)
    with open(call, 'r') as f:
        content = f.read()
        with open('output/merged_results.json', 'a') as sc:
            sc.write('\n')
            sc.write(content)
            sc.close()
        f.close()