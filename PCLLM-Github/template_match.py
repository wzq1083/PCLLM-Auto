import time

import os
import cv2
import numpy as np
from PIL import ImageGrab, Image


def load_template(template_folder=r'template\notepad'):
    # 加载图像模板， 存放在工程目录下template文件夹下
    # 每个模板图像命名为：   模板名称-template
    # 创建一个空字典用于存储模板图像
    templates = {}

    # 遍历模板文件夹下的所有文件
    for filename in os.listdir(template_folder):
        # 解析模板名称
        template_name, _ = os.path.splitext(filename)
        # template_name = template_name.split("-")[0]
        # 读取图像并存储至字典中
        template_path = os.path.join(template_folder, filename)
        template_image = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        templates[template_name] = template_image
    print("模板加载完成")
    return templates


def template_matching(source_image, target, templates_dict):
    """
    在 source_image 中找到 target 的像素位置并返回。
    如果找到匹配结果，返回点击位置，否则返回 None。
    :param source_image: 原始图像
    :param target: 要匹配的目标名称
    :param templates_dict: 包含模板图像的字典
    :return: 匹配的点击位置 (x, y) 或 None
    """
    if target in templates_dict.keys():
        template = templates_dict[target]
        # 使用模板匹配方法
        result = cv2.matchTemplate(source_image, template, cv2.TM_CCOEFF_NORMED)

        # 设定匹配阈值
        threshold = 0.95

        # 获取匹配位置
        button_left_up_locations = np.where(result >= threshold)
        # 检查是否有匹配结果
        if len(button_left_up_locations[0]) == 0:  # 如果没有匹配
            return None

        button_click_location = (button_left_up_locations[1][0] + int(template.shape[1] / 2),
                                 button_left_up_locations[0][0] + int(template.shape[0] / 2))

        return button_click_location
    else:
        return None


def screen_capture(save_fig=False, task_folder=None, image_name='0', error=None, gray=True):
    # 截取整个屏幕图像，将其转换为模板匹配算法需要的灰度图格式之后返回

    # 截取整个屏幕
    screenshot = ImageGrab.grab()
    # 将截图转换为NumPy数组
    screenshot_np = np.array(screenshot)

    # 转换为灰度图像
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    # 转换为pil图像
    screenshot_gray_pil = Image.fromarray(screenshot_gray)

    if save_fig:
        # 保存截图
        fig_path = os.path.join(task_folder, f"{image_name}.png")
        screenshot.save(fig_path)
    if gray:
        return screenshot_gray
    else:
        return screenshot_gray_pil


if __name__ == "__main__":
    templates_dict = load_template()
    time.sleep(2)
    image = screen_capture('0')
    click_position = template_matching(image, "File", templates_dict)
    # 在指定位置绘制一个小红点
    radius = 5
    color = (0, 0, 255)  # 红色
    thickness = -1  # 填充实心圆
    image_with_point = cv2.circle(image, (click_position[0], click_position[1]), radius, color, thickness)
    cv2.imshow('result', image_with_point)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
