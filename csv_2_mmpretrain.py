import pandas as pd
import json
from sklearn.model_selection import train_test_split

# Define file paths
csv_file_path = 'annotations.csv'  # Replace with actual path to the .csv file
train_output_path = 'deq/annotation_train.json'
test_output_path = 'deq/annotation_test.json'
all_output_path = 'deq/annotation_all.json'

# Load CSV data
data = pd.read_csv(csv_file_path)

# Shuffle the data and split it into train and test sets (80% train, 20% test)
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42, shuffle=True)

# Extract unique categories and assign an index to each
categories = list(sorted(set([cat.strip() for sublist in data['category'].str.split(',') for cat in sublist])))
category_to_idx = {category: idx for idx, category in enumerate(categories)}

# Function to generate the annotation structure with exploded multiple labels
def create_annotation_with_multilabels(data_split, categories):
    annotation = {
        "metainfo": {
            "classes": categories
        },
        "data_list": []
    }
    
    for _, row in data_split.iterrows():
        # Explode the categories by comma and map them to their indices
        labels = row['category'].split(',')
        gt_labels = [category_to_idx[label.strip()] for label in labels]
        
        annotation["data_list"].append({
            "img_path": row['filename'],
            'gt_label': gt_labels
        })
    
    return annotation

# Create annotations for train, test, and all data sets with multi-label support
annotation_train = create_annotation_with_multilabels(train_data, categories)
annotation_test = create_annotation_with_multilabels(test_data, categories)
annotation_all = create_annotation_with_multilabels(data, categories)

# Save the annotations as JSON files
with open(train_output_path, 'w') as train_file:
    json.dump(annotation_train, train_file, indent=4)

with open(test_output_path, 'w') as test_file:
    json.dump(annotation_test, test_file, indent=4)

with open(all_output_path, 'w') as all_file:
    json.dump(annotation_all, all_file, indent=4)

# Return the structure of the generated annotations for train, test, and all
annotation_train, annotation_test, annotation_all
