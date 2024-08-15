#!/bin/bash
# Define the base directory to store the data
BASE_DIR="COCO"
mkdir -p ${BASE_DIR}
cd ${BASE_DIR}

# URLs for the COCO dataset (2017 training images and annotations)
TRAIN_IMAGES_URL="http://images.cocodataset.org/zips/train2017.zip"
VALIDATION_IMAGES_URL="http://images.cocodataset.org/zips/val2017.zip"
ANNOTATIONS_URL="http://images.cocodataset.org/annotations/annotations_trainval2017.zip"
TEST_IMAGES_URL="http://images.cocodataset.org/zips/test2017.zip"
TEST_ANNOTATIONS_URL="http://images.cocodataset.org/annotations/image_info_test2017.zip"

# Function to download and unzip files if not already present
download_unzip() {
    local url=$1
    local file=$2
    echo "Downloading $file..."
    if [ -f "$file" ]; then
        echo "$file already downloaded."
    else
        wget -c $url -O $file
    fi

    echo "Unzipping $file..."
    #unzip -q $file
}

# Download datasets
download_unzip $TRAIN_IMAGES_URL "train2017.zip"
download_unzip $VALIDATION_IMAGES_URL "val2017.zip"
download_unzip $ANNOTATIONS_URL "annotations_trainval2017.zip"
download_unzip $TEST_IMAGES_URL "test2017.zip"
download_unzip $TEST_ANNOTATIONS_URL "image_info_test2017.zip"

# Prepare data directories
echo "Moving the images to the correct directory..."
cd ..
mkdir -p YOLO/images YOLO/labels

# Efficiently move all jpg files using find and xargs
find COCO/train2017 COCO/val2017 -name "*.jpg" -print0 | xargs -0 -I {} cp {} YOLO/images/

echo "creating YOLO type labels for the images..."
python3 coco_labels.py

# Create csv files for the annotations
echo "Creating csv files "
python3 coco_csv.py

# Optional: Cleanup zip files
# echo "Cleaning up zip files..."
# rm *.zip

echo "COCO dataset downloaded and unpacked."
