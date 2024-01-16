if __name__ == '__main__':
    ''' 
        拼接多个coco格式的json(单个coco json中可包含多个图片与标注)
        仅支持单个category
        会自动将image id 与 bbox id 顺序排列
    '''
import json
from pathlib import Path

if __name__ == '__main__':
    json_root = Path('../coco_json')
    output_file = 'train.json'

    categories = [
        {
            "supercategory": "wildfire",
            "id": 1,
            "name": "smoke"
        }
    ]
    total_data = {"images": [], "categories": categories, "annotations": []}
    img_id_count, bbox_id_count = 0, 0
    file_list = [str(i) for i in json_root.iterdir() if i.suffix == '.json']
    print(file_list)
    for js_file in file_list:
        print(js_file)
        with open(js_file, 'r') as f:
            js_data = json.load(f)
            images = js_data['images']
            annotations = js_data['annotations']
        # Dont change origin data
        for img_idx, image in enumerate(images):
            print(img_id_count, bbox_id_count)
            image_new = image.copy()
            origin_img_id = image['id']
            image_new['id'] = img_id_count
            total_data['images'].append(image_new)
            for idx, anno in enumerate(annotations):
                if anno['image_id'] == origin_img_id:
                    anno_new = anno.copy()
                    anno_new['id'] = bbox_id_count
                    anno_new['image_id'] = img_id_count
                    total_data['annotations'].append(anno_new)
                    bbox_id_count += 1
            img_id_count += 1

    with open(output_file, 'w') as f:
        json.dump(total_data, f)

