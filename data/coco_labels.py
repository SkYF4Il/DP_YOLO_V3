import os
import json
from pycocotools.coco import COCO
from os.path import join, exists
from os import makedirs, getcwd

# Define COCO classes
classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane',
           'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
           'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
           'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
           'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
           'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
           'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
           'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
           'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
           'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
           'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven',
           'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
           'teddy bear', 'hair drier', 'toothbrush']


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[2]) / 2.0 - 1
    y = (box[1] + box[3]) / 2.0 - 1
    w = box[2] - box[0]
    h = box[3] - box[1]
    return (x * dw, y * dh, w * dw, h * dh)


def convert_coco_annotation(coco, img_id, classes, output_dir, prefix):
    filename = f"{prefix}_{str(img_id).zfill(12)}.txt"
    filepath = join(output_dir, filename)

    if exists(filepath):
        print(f"Skipping {filename}, already processed.")
        return

    ann_ids = coco.getAnnIds(imgIds=[img_id], iscrowd=None)
    annotations = coco.loadAnns(ann_ids)
    image_info = coco.loadImgs(img_id)[0]

    with open(filepath, 'w') as file:
        for ann in annotations:
            if ann['category_id'] not in coco.getCatIds(catNms=classes):
                continue
            cls_id = classes.index(coco.loadCats(
                ann['category_id'])[0]['name'])
            b = ann['bbox']
            bb = convert((image_info['width'], image_info['height']), [
                         b[0], b[1], b[0]+b[2], b[1]+b[3]])
            file.write(str(cls_id) + " " + " ".join(map(str, bb)) + '\n')


if __name__ == "__main__":
    dataDir = 'COCO/'
    output_dir = 'YOLO/labels'

    if not exists(output_dir):
        makedirs(output_dir)

    dataTypes = ['train2017', 'val2017', 'test2017']
    for dataType in dataTypes:
        annFile = f'{dataDir}/annotations/instances_{dataType}.json'
        coco = COCO(annFile)
        images = coco.getImgIds()
        prefix = 'COCO_' + dataType

        for img_id in images:
            convert_coco_annotation(coco, img_id, classes, output_dir, prefix)
