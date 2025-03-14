# Annotation Format Changer

This repository provides Python scripts to convert between various annotation formats commonly used in machine learning projects, specifically between CSV, CVAT, and MMPretrain formats.

## Supported Conversions

- CSV to MMPretrain
- CVAT to CSV
- CVAT to MMPretrain
- MMPretrain to CVAT

## Files

- `csv_2_mmpretrain.py`: Convert CSV annotations to MMPretrain format.
- `cvat_2_csv.py`: Convert CVAT XML annotations to CSV format.
- `cvat_2_mmpretrain.py`: Convert CVAT annotations (XML) to MMPretrain format.
- `mmpretrain_2_cvat.py`: Convert MMPretrain annotations to CVAT format.

## Requirements

- Python 3.6 or later
- pandas
- scikit-learn
- Pillow (for image processing in MMPretrain to CVAT conversion)