import os
import random
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from PIL import Image  # pip install pillow

def random_color():
    return '#' + ''.join(random.choices('0123456789ABCDEF', k=6))

# Parameters
csv_file_path = "annotation.csv"               # CSV file with annotations
output_xml_file = "annotation.xml"   # Output XML file
images_folder = "images"                     # Folder containing the images

# Task & meta configuration (update values as needed)
task_id = ""
task_name = ""
job_url = ""
owner_username = ""
owner_email = ""

# Default image dimensions if an image cannot be read
default_width, default_height = 450, 300

# Load CSV data
df = pd.read_csv(csv_file_path)

# Sort the dataframe by the original image name (alphabetically)
df = df.sort_values(by="Image_Name").reset_index(drop=True)
row_count = len(df)

# Use the headers after the first two ("Image_Name", "category") as annotation columns/labels
annotation_columns = df.columns[2:]
label_names = list(annotation_columns)

# Create labels configuration with random colors
labels_config = []
for name in label_names:
    labels_config.append({
        "name": name,
        "color": random_color(),
        "type": "any",
        "attributes": " "
    })

# Create the root element
root = ET.Element("annotations")
ET.SubElement(root, "version").text = "1.1"

# Create meta element
meta = ET.SubElement(root, "meta")
task = ET.SubElement(meta, "task")
ET.SubElement(task, "id").text = task_id
ET.SubElement(task, "name").text = task_name
ET.SubElement(task, "size").text = str(row_count)
ET.SubElement(task, "mode").text = "annotation"
ET.SubElement(task, "overlap").text = "0"
ET.SubElement(task, "bugtracker")  # empty tag

# Current timestamp with timezone offset
current_time = datetime.now().isoformat() + "+00:00"
ET.SubElement(task, "created").text = current_time
ET.SubElement(task, "updated").text = current_time
ET.SubElement(task, "subset").text = "default"
ET.SubElement(task, "start_frame").text = "0"
ET.SubElement(task, "stop_frame").text = str(row_count - 1)
ET.SubElement(task, "frame_filter")  # empty tag

# Create segments element with one segment
segments = ET.SubElement(task, "segments")
segment = ET.SubElement(segments, "segment")
ET.SubElement(segment, "id").text = task_id
ET.SubElement(segment, "start").text = "0"
ET.SubElement(segment, "stop").text = str(row_count - 1)
ET.SubElement(segment, "url").text = job_url

# Owner information
owner = ET.SubElement(task, "owner")
ET.SubElement(owner, "username").text = owner_username
ET.SubElement(owner, "email").text = owner_email
ET.SubElement(task, "assignee")  # empty tag

# Add labels
labels_elem = ET.SubElement(task, "labels")
for lab in labels_config:
    label_elem = ET.SubElement(labels_elem, "label")
    ET.SubElement(label_elem, "name").text = lab["name"]
    ET.SubElement(label_elem, "color").text = lab["color"]
    ET.SubElement(label_elem, "type").text = lab["type"]
    ET.SubElement(label_elem, "attributes").text = lab["attributes"]

# Dumped timestamp
ET.SubElement(meta, "dumped").text = datetime.now().isoformat() + "+00:00"

# Process each row to create image elements (sorted), keep the original image name unchanged.
for idx, row in df.iterrows():
    image_name = row["Image_Name"]
    img_path = os.path.join(images_folder, image_name)
    try:
        with Image.open(img_path) as img:
            width, height = img.size
    except Exception as e:
        print(f"Warning: Could not open {img_path}. Using default dimensions. Error: {e}")
        width, height = default_width, default_height

    # Create image element with the sorted sequential id and the original image name.
    image_elem = ET.SubElement(root, "image", id=str(idx), name=image_name,
                               width=str(width), height=str(height))
    # For each annotation column, if the value is 1 then add a tag element.
    for col in annotation_columns:
        try:
            if int(row[col]) == 1:
                ET.SubElement(image_elem, "tag", label=col, source="manual").text = " "
        except Exception:
            continue

# Write the XML tree to the output file
tree = ET.ElementTree(root)
tree.write(output_xml_file, encoding="utf-8", xml_declaration=True)
print(f"XML file generated successfully: {output_xml_file}")