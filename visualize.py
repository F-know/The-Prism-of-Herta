import numpy as np
from PIL import Image
from math import sqrt, floor, log2
import colorsys

H, S, V = 12, 64, 64


def hsv_to_hex(h, s, v):
    # 将 HSV 转换为 RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    # 将 RGB 分量从浮点数转换为整数（0-255）
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    # 将整数 RGB 值转换为十六进制字符串
    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)

    return hex_color


def trans_sv(s, v):
    s = 1 - (1 - s) * v
    s, v = (s + v - 1) * sqrt(3), v - s + 1
    return s, v


def get_image_info(image):
    width, height = image.size
    image_info = np.zeros((H, S, V))
    for x in range(width):
        for y in range(height):
            r, g, b = [x / 255.0 for x in image.getpixel((x, y))]
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            s, v = trans_sv(s, v)
            image_info[min(floor(h * H), H - 1)][min(floor(s / sqrt(3) * S), S - 1)][min(floor(v / 2 * V), V - 1)] += 1
    for h in range(H):
        for s in range(S):
            for v in range(V):
                image_info[h][s][v] = log2(image_info[h][s][v]) if image_info[h][s][v] > 0 else 0
    return image_info


def generate_picture(image_info):
    max_val = np.max(image_info)
    edge_width = 1.1
    res_pic = Image.new('RGB', (floor(S * sqrt(3) * edge_width * H / 2), floor(V * 2 * edge_width * 2)))
    for h in range(H):
        pic = Image.new('RGB', (V, S))
        for s in range(S):
            for v in range(V):
                val = floor(image_info[h][s][v] / max_val * 255)
                pic.putpixel((v, s), (val, val, val))
        pic = pic.resize((floor(V * 2), floor(S * sqrt(3))))
        color = hsv_to_hex((h + 0.5) / H, 1, 1)
        new_pic = Image.new('RGB', (pic.size[0], pic.size[1]), color=color)
        for s in range(new_pic.size[1]):
            for v in range(new_pic.size[0]):
                if s > min(sqrt(3) * v, -sqrt(3) * (v - new_pic.size[0])):
                    new_pic.putpixel((v, s), (0, 0, 0))
        new_pic2 = new_pic.resize((floor(new_pic.size[0] * edge_width), floor(new_pic.size[1] * edge_width)))
        for s in range(new_pic2.size[1]):
            _s = s - 3
            if 0 <= _s < new_pic.size[1]:
                for v in range(new_pic2.size[0]):
                    _v = v - (new_pic2.size[0] - new_pic.size[0]) // 2
                    if 0 <= _v < new_pic.size[0]:
                        if new_pic.getpixel((_v, _s)) != (0, 0, 0):
                            new_pic2.putpixel((v, s), pic.getpixel((_v, _s)))
        new_pic3 = Image.new('RGB', (new_pic2.size[1], new_pic2.size[0]))
        for s in range(new_pic2.size[1]):
            for v in range(new_pic2.size[0]):
                new_pic3.putpixel((s, new_pic2.size[0] - v - 1), new_pic2.getpixel((v, s)))
        if h < H // 2:
            res_pic.paste(new_pic3, (new_pic3.size[0] * h, 0))
        else:
            res_pic.paste(new_pic3, (new_pic3.size[0] * (h - H // 2), new_pic3.size[1]))
    res_pic = res_pic.resize((floor(res_pic.size[0] * 1.5), floor(res_pic.size[1] * 1.5)))
    return res_pic


def visualize(image):
    image_info = get_image_info(image)
    return generate_picture(image_info)
