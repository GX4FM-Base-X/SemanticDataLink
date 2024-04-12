import yaml
import json

# Load YAML safely
with open('linkml/yaml/personinfo_complex.yaml', 'r') as yaml_file:
    yaml_content = yaml.safe_load(yaml_file)

# Convert the loaded YAML to JSON and save it
with open('/Users/maximilianstaebler/Downloads/personinfo_complex_converted.json', 'w') as json_file:
    json.dump(yaml_content, json_file, indent=4)


# # Load the JSON file
# with open('linkml/yaml/personinfo_complex_converted.json', 'r') as json_file:
#     json_content = json.load(json_file)

# # Convert the loaded JSON to YAML and save it
# with open('linkml/yaml/personinfo_complex_converted_back.yaml', 'w') as yaml_file:
#     yaml.safe_dump(json_content, yaml_file, allow_unicode=True,
#                    default_flow_style=False)
