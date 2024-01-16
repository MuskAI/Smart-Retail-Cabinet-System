input_folder = "/Volumes/HIKVISION/fix_results/labels"
output_folder = "/Volumes/HIKVISION/fix_results/nms_labels"
threshold = 0.5  # 调整NMS的阈值
import numpy as np
import os
from tqdm import tqdm
def calculate_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection_area = max(0, x2 - x1) * max(0, y2 - y1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    iou = intersection_area / float(box1_area + box2_area - intersection_area)

    return iou

def non_maximum_suppression(boxes, scores, threshold):
    selected_indices = []
    trash_bboxes_idx = []
    for idx1, box1 in enumerate(boxes):
        if idx1 in trash_bboxes_idx:
            continue
        for idx2, box2 in enumerate(boxes):
            if idx1 != idx2 and idx2 not in trash_bboxes_idx:
                iou = calculate_iou(box1, box2)
                if iou >= threshold:
                    trash_bboxes_idx.append(idx2)

    for idx, box in enumerate(boxes):
        if idx not in trash_bboxes_idx:
            selected_indices.append(idx)
    return selected_indices


if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in tqdm(os.listdir(input_folder)):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, "r") as file:
            lines = file.readlines()

        boxes = []
        scores = []

        for line in lines:
            data = line.strip().split()
            class_id = int(data[0])
            x_center, y_center, width, height = map(float, data[1:])
            x1, y1 = x_center - width / 2, y_center - height / 2
            x2, y2 = x_center + width / 2, y_center + height / 2
            boxes.append([x1, y1, x2, y2])
            scores.append(1.0)  # 分数可以是任意值，因为我们将在NMS中根据IoU来选择

        selected_indices = non_maximum_suppression(boxes, scores, threshold)

        with open(output_path, "w") as file:
            for idx in selected_indices:
                file.write(lines[idx])
