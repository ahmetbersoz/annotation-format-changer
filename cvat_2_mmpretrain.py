import os
import xml.etree.ElementTree as ET
import json
import random

# Input and output file paths
xml_file_path = "annotations.xml"
output_dir = "output_files"
train_file_path = os.path.join(output_dir, "train.json")
test_file_path = os.path.join(output_dir, "test.json")
all_file_path = os.path.join(output_dir, "all.json")

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

# Parsing XML File
with open(xml_file_path, 'r') as file:
    tree = ET.parse(file)
    root = tree.getroot()

# Extracting classes from <labels> tags
classes = []
for label in root.findall(".//label"):
    class_name = label.find("name").text
    if class_name not in classes:
        classes.append(class_name)

class_to_index = {label: idx for idx, label in enumerate(classes)}

# Extracting relevant information into a list
data = []
for image in root.findall('image'):
    image_name = image.attrib['name']
    labels = [class_to_index[tag.attrib['label']] for tag in image.findall('tag')]
    
    data.append({
        "img_path": image_name,
        "gt_label": labels
    })

# Shuffle data for random split
random.shuffle(data)

# Split data into train and test sets (80% train, 20% test)
split_index = int(len(data) * 0.8)
train_data = data[:split_index]
test_data = data[split_index:]

# Write to output files
metainfo = {
    "metainfo": {
        "classes": classes
    }
}

with open(all_file_path, 'w') as all_file:
    json.dump({**metainfo, "data_list": data}, all_file, indent=4)

with open(train_file_path, 'w') as train_file:
    json.dump({**metainfo, "data_list": train_data}, train_file, indent=4)

with open(test_file_path, 'w') as test_file:
    json.dump({**metainfo, "data_list": test_data}, test_file, indent=4)

print("Conversion complete. JSON files created in", output_dir)