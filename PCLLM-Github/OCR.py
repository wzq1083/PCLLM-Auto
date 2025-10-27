from template_match import *
import pytesseract
import pyautogui
pyautogui.FAILSAFE = False
# pyautogui.PAUSE = 0.2

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\20871\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def find_character_position(target_word):
    # 打开图像
    image = screen_capture(gray=False)
    # image = image.convert('L')  # 转为灰度
    # image = image.point(lambda x: 0 if x < 128 else 255, '1')  # 二值化

    # 获取图像的高度，用于坐标调整
    img_width, img_height = image.size  # 返回值是一个包含宽度和高度的元组

    # 配置Tesseract以返回位置信息
    custom_config = r'--psm 11 --oem 3'  # 单个统一块的OCR。可以根据需要调整此参数。
    boxes = pytesseract.image_to_boxes(image, config=custom_config)

    word_positions = []
    current_word = ""
    word_start_pos = None

    # 遍历Tesseract的识别结果，拼接成单词
    for box in boxes.splitlines():
        b = box.split(' ')
        char = b[0]
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])

        if not word_start_pos:
            word_start_pos = (x, img_height - y)

        current_word += char

        # 判断是否达到了目标单词
        if current_word == target_word:
            # 计算单词的位置
            word_positions.append({
                'word': current_word,
                'left': word_start_pos[0],
                'bottom': word_start_pos[1],
                'right': w,
                'top': img_height - h
            })
            current_word = ""
            word_start_pos = None
        elif len(current_word) >= len(target_word):
            # 如果当前字符不匹配目标单词，重置状态
            current_word = ""
            word_start_pos = None

    return word_positions if word_positions else None  # 返回找到的所有单词位置


if __name__ == "__main__":
    target_word = 'Edit'  # 替换为你要查找的字符

    position = find_character_position(target_word)
    if position:
        print(f"字符 '{target_word}' 的像素位置为: {position}")
    else:
        print(f"字符 '{target_word}' 未在图像中找到。")

    click_position = [position[0]["left"], position[0]["bottom"]]
    pyautogui.moveTo(click_position[0], click_position[1])
    # 模拟点击鼠标左键
    pyautogui.click()





