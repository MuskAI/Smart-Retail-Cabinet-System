import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')

# 创建一个示例列表，包含一些非None和None的元素
my_list = [1, 2, None, 4, None, 6, 7, None, 9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,None,None,None,None,None,None,None,None,None,None,None]

# 创建时间轴
time_axis = np.arange(len(my_list))

# 创建一个颜色列表，用于表示非None元素和None元素
colors = ['blue' if item is not None else 'red' for item in my_list]

# 绘制时间轴
plt.figure(figsize=(10, 2))  # 设置图形大小
plt.bar(time_axis, [1] * len(my_list), color=colors, width=0.9)

# 可以添加一些额外的样式，如标题和坐标轴标签
plt.title('时间轴示例')
plt.xlabel('时间')
plt.ylabel('事件')

# 设置x轴标签为时间轴上的位置
plt.xticks(time_axis)

# 显示图形
plt.show()
