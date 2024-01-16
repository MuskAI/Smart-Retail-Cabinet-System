import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

class ImageDisplayApp:
    def __init__(self, root):
        self.root = root
        self.result = []
        self.k = 0
        self.current_index = 0

        self.preview_label = tk.Label(self.root)
        self.preview_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # self.select_button = tk.Button(self.root, text="选择图片", command=self.retrieve_image)
        # self.select_button.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # self.retrieval_button = tk.Button(self.root, text="开始检索", command=self.start_retrieval)
        # self.retrieval_button.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        self.image_labels = []
        self.cls_labels = []
        self.dis_labels = []

        for i in range(8):

            img_label = tk.Label(self.root)
            img_label.grid(row=i // 4 + 3, column=i % 4, padx=15, pady=15)
            self.image_labels.append(img_label)

            cls_label = tk.Label(self.root, font=("Arial", 12))
            cls_label.grid(row=i // 4 + 4, column=i % 4, sticky='w')
            self.cls_labels.append(cls_label)

            dis_label = tk.Label(self.root, font=("Arial", 12))
            dis_label.grid(row=i // 4 + 5, column=i % 4, sticky='w')
            self.dis_labels.append(dis_label)
    #
    def select_image(self):
        file_path = filedialog.askopenfilename(title="选择图片")
        if file_path:
            img = Image.open(file_path)
            img = img.resize((200, 200))
            img = ImageTk.PhotoImage(img)
            self.preview_label.config(image=img)
            self.preview_label.image = img  # 保存图片的引用
        return file_path


    def show_result(self, result):
        # 模拟检索算法返回的result
        # 请用实际的检索算法替换这部分内容

        self.result = result
        self.k = min(3, len(self.result))  # 设置要显示的图片数量
        self.show_images()
    def show_images(self):
        for i in range(self.k):
            img_path = self.result[i]['img']
            img = Image.open(img_path)
            img = img.resize((200, 200))
            photo = ImageTk.PhotoImage(img)

            self.image_labels[i].config(image=photo)
            self.image_labels[i].image = photo
            self.image_labels[i].update()

            cls = self.result[i]['cls']
            dis = "{:.5f}".format(self.result[i]['dis'])  # 保留小数点后5位

            self.cls_labels[i].config(text="类别: " + cls)
            self.dis_labels[i].config(text="特征距离: " + dis)
            self.cls_labels[i].update()
            self.dis_labels[i].update()

if __name__ == "__main__":
    root = tk.Tk('SRCS')
    app = ImageDisplayApp(root)
    root.mainloop()
