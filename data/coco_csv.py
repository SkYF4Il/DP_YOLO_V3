import os
import csv


def generate_csv_files(data_dir, output_dir, dataset_types):
    """Generates CSV files listing images and corresponding label files for each dataset type."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for dataset_type in dataset_types:
        image_dir = os.path.join(data_dir, dataset_type)
        output_csv_path = os.path.join(output_dir, f'{dataset_type}.csv')
        prefix = f"{data_dir}_{dataset_type}_"

        with open(output_csv_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for img in os.listdir(image_dir):
                if img.endswith('.jpg'):
                    img_id = img.split('.')[0]
                    formatted_img_id = f"{prefix}{img_id}"
                    label_file = f"{formatted_img_id}.txt"
                    writer.writerow([f"{img_id}.jpg", label_file])


data_dir = 'COCO'
output_dir = 'YOLO'
dataset_types = ['train2017', 'val2017', 'test2017']

generate_csv_files(data_dir, output_dir, dataset_types)
