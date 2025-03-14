import xml.etree.ElementTree as ET
import pandas as pd

def convert_cvat_xml_to_csv(xml_path, csv_path):
    # Parse XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 1. Collect the full set of possible categories (labels) from the meta section
    #    This ensures we include categories that might appear zero times in the images.
    labels_root = root.find("./meta/project/labels")
    all_categories = []
    if labels_root is not None:
        for label_node in labels_root.findall("label"):
            name_node = label_node.find("name")
            if name_node is not None:
                all_categories.append(name_node.text)

    # Make sure categories are unique and sorted
    all_categories = sorted(set(all_categories))

    # 2. For each <image>, collect its associated categories from <tag label="...">
    images_data = {}
    for image_node in root.findall("image"):
        image_name = image_node.get("name")
        # If any <tag> is present, read its label attribute
        category_set_for_this_image = set()
        for tag_node in image_node.findall("tag"):
            label = tag_node.get("label")
            category_set_for_this_image.add(label)

        images_data[image_name] = category_set_for_this_image

    # 3. Build a table (list of rows) where each row corresponds to an image
    #    and each column is a category with 1/0 indicating presence/absence.
    rows = []
    for image_name, label_set in images_data.items():
        row = [image_name] + [1 if category in label_set else 0 for category in all_categories]
        rows.append(row)

    # Create a DataFrame: columns are "image" + each category as a column
    df = pd.DataFrame(rows, columns=["image"] + all_categories)

    # 4. Save to CSV
    df.to_csv(csv_path, index=False)
    print(f"CSV file saved at: {csv_path}")

if __name__ == '__main__':
    xml_file_path = "annotations.xml"  # Replace with your annotations file path
    csv_file_path = "output.csv"       # Replace with desired output CSV path
    convert_cvat_xml_to_csv(xml_file_path, csv_file_path)
