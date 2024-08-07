import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import visualize
from datetime import datetime
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_image(path):
    # 加载并返回图像对象
    image = Image.open(path).convert("RGB")
    image.thumbnail((800, 400))
    return image


def show_images(original, result):
    # 将图像转换为Tkinter可显示的格式
    original_tk = ImageTk.PhotoImage(original)
    result_tk = ImageTk.PhotoImage(result)

    # 创建标签以显示图像
    original_label.config(image=original_tk)
    original_label.image = original_tk  # 防止被垃圾回收

    result_label.config(image=result_tk)
    result_label.image = result_tk  # 同上


def select_image():
    # 打开文件选择对话框
    path = filedialog.askopenfilename()
    if path:
        try:
            original = load_image(path)
            result = visualize.visualize(original)
            result.thumbnail((800, 800))
            show_images(original, result)
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    if datetime.now().hour >= 5:
        root.title("黑塔的三棱镜")
    else:
        root.title("熬夜的小孩会被黑塔小姐做成人偶")
    root.iconbitmap(resource_path('my_icon.ico'))
    root.configure(bg='black')

    # 设置窗口大小和位置
    window_width = 810
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)  # 禁止调整窗口大小

    # 创建按钮用于选择图像
    select_button = tk.Button(root, text="选择图片", command=select_image)
    select_button.pack()

    # 创建标签以显示图像
    original_label = tk.Label(root, bg='black')
    original_label.pack()
    result_label = tk.Label(root, bg='black')
    result_label.pack(side=tk.BOTTOM)

    # 运行主循环
    root.mainloop()
