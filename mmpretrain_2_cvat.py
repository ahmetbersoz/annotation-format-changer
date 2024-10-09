import json
import xml.etree.ElementTree as ET
from datetime import datetime
import random
import os
from PIL import Image

# Function to generate random colors for the labels
def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Input and Output file paths
input_json_file = "deq/annotation_all.json"  # Path to the input JSON file
output_xml_file = "deq/output_annotations.xml"  # Path to the output XML file
images_folder = "deq/JPEGImages"  # Folder where images are stored

# Read JSON data from a file
with open(input_json_file, "r") as file:
    data = json.load(file)

# Create the root element of the XML
root = ET.Element("annotations")

# Add version element
ET.SubElement(root, "version").text = "1.1"

# Create meta information
meta = ET.SubElement(root, "meta")
task = ET.SubElement(meta, "task")
ET.SubElement(task, "id").text = "945292"
ET.SubElement(task, "name").text = "DEQ"
ET.SubElement(task, "size").text = str(len(data['data_list']))
ET.SubElement(task, "mode").text = "annotation"
ET.SubElement(task, "overlap").text = "0"
ET.SubElement(task, "bugtracker")

# Add timestamp information
created = ET.SubElement(task, "created")
created.text = str(datetime.now())
updated = ET.SubElement(task, "updated")
updated.text = str(datetime.now())

# Additional meta details
ET.SubElement(task, "subset").text = "default"
ET.SubElement(task, "start_frame").text = "0"
ET.SubElement(task, "stop_frame").text = str(len(data['data_list']) - 1)
ET.SubElement(task, "frame_filter")

# No segments section as per the updated requirement

# Add owner information
owner = ET.SubElement(task, "owner")
ET.SubElement(owner, "username").text = "abersoz"
ET.SubElement(owner, "email").text = "abersoz@gmail.com"

# Add labels
labels = ET.SubElement(task, "labels")
for class_name in data['metainfo']['classes']:
    label = ET.SubElement(labels, "label")
    ET.SubElement(label, "name").text = class_name
    ET.SubElement(label, "color").text = generate_random_color()  # Generate a random color for each label
    ET.SubElement(label, "type").text = "any"
    ET.SubElement(label, "attributes").text = " "

# Add dumped timestamp
ET.SubElement(meta, "dumped").text = str(datetime.now())

# Add images and tags from data_list
for idx, item in enumerate(data['data_list']):
    img_path = os.path.join(images_folder, item["img_path"])
    
    try:
        # Open the image to get width and height
        with Image.open(img_path) as img:
            width, height = img.size
    except FileNotFoundError:
        print(f"Warning: Image {img_path} not found. Using default dimensions (450x300).")
        width, height = 450, 300  # Default dimensions if image is not found

    image = ET.SubElement(root, "image", id=str(idx), name=item["img_path"], width=str(width), height=str(height))
    
    for label_idx in item["gt_label"]:
        class_name = data['metainfo']['classes'][label_idx]
        tag = ET.SubElement(image, "tag", label=class_name, source="manual")
        tag.text = " "

# Convert the tree to a string
xml_data = ET.tostring(root, encoding='utf8', method='xml').decode()

# Write the XML data to a file
with open(output_xml_file, "w") as xml_file:
    xml_file.write(xml_data)

print(f"XML file generated successfully! Output file: {output_xml_file}")
