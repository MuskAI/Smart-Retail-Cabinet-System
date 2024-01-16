import os
import random
import shutil

def copy_random_images(src_root, dst_root, num_images):
    all_images = []
    for root, dirs, files in os.walk(src_root):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                all_images.append(os.path.join(root, file))

    print(f"Found {len(all_images)} image(s).")
    selected_images = random.sample(all_images, min(num_images, len(all_images)))
    print(f"Copying {len(selected_images)} image(s).")

    for image in selected_images:
        shutil.copy(image, dst_root)
        print(f"Copied {image} to {dst_root}")

    return selected_images

src_root = '/Volumes/HIKVISION/三批次数据整合-36'
dst_root = '/Volumes/HIKVISION/dst_root'  # 替换为您的目的地文件夹路径
num_images = 2000

copy_random_images(src_root, dst_root, num_images)
