import os

from OCR import *
from template_match import *
import re
import pyautogui


def exit_to_origin(app_name, template_dict, GUI_state, save_data=False, task_folder=None, file_name=None):
    ################################################################
    # 在软件自动化操作过程中，可能由于大模型的误操作使得界面停在异常的位置
    # 该函数将UI界面退回到软件主界面
    # 用模板匹配确认页面是否存在异常界面，并将其关闭
    ################################################################
    if save_data:
        assert task_folder is not None and file_name is not None,  '    缺少保存文件的路径或文件保存名称'

    if app_name == 'Notepad':
        err_list = ['Exit find', 'Exit replace', 'Exit search', 'Line error OK', 'Goto cancel',
                    'Overwrite cancel', 'Save file cancel', 'blank']  # 为了图像数据集能够正常保存最终状态

        for button in err_list:
            if template_matching(GUI_state, button, template_dict):  # 如果当前界面中包含未退回到原始界面的按钮
                action_2_operation(f'click({button})', template_dict, save_data, task_folder)
                GUI_state = screen_capture(save_data, task_folder, str(file_name))  # 获取屏幕截图
                file_name += 1
                time.sleep(0.5)

    if app_name == 'Wordpad':
        err_list = ["overwrite confirm no", "overwrite confirm yes", "cancel save"]  # 为了图像数据集能够正常保存最终状态

        for button in err_list:
            if template_matching(GUI_state, button, template_dict):  # 如果当前界面中包含未退回到原始界面的按钮
                action_2_operation(f'click({button})', template_dict, save_data, task_folder)
                GUI_state = screen_capture(save_data, task_folder, str(file_name))  # 获取屏幕截图
                file_name += 1
                time.sleep(0.5)


# def create_task_folder(base_dir, task_name):
#     ##################################################
#     # 按照任务名称+序号的规则创建任务文件夹
#     ##################################################
#     # 获取所有子文件夹的列表
#     existing_folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
#
#     # 筛选出与任务名称匹配的文件夹
#     pattern = re.compile(rf'^{re.escape(task_name)}\+\d+$')
#     matching_folders = [f for f in existing_folders if pattern.match(f)]
#
#     if matching_folders:
#         # 提取已有文件夹的最大序号
#         max_index = max([int(f.split('+')[-1]) for f in matching_folders])
#         new_folder_name = f"{task_name}+{max_index + 1}"
#     else:
#         # 如果没有匹配的文件夹，创建第一个任务文件夹
#         new_folder_name = f"{task_name}+1"
#
#     # 创建新文件夹
#     new_folder_path = os.path.join(base_dir, new_folder_name)
#     os.makedirs(new_folder_path)
#     return new_folder_path


def create_next_folder(base_path):
    ##################################################
    # 在base-path下创建新文件夹，文件夹以数字命名，依次递增
    ##################################################
    # 确认 base_path 是否存在
    if not os.path.exists(base_path):
        print(f"路径 {base_path} 不存在")
        return

    # 获取 base_path 下的所有文件夹
    folders = [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]

    # 过滤出数字命名的文件夹并找到最大编号
    numbers = []
    for folder in folders:
        if folder.isdigit():
            numbers.append(int(folder))

    # 如果没有数字命名的文件夹，默认从 0 开始
    if numbers:
        next_number = max(numbers) + 1
    else:
        next_number = 0

    # 创建新文件夹路径
    new_folder_name = str(next_number)
    new_folder_path = os.path.join(base_path, new_folder_name)

    # 创建文件夹
    os.mkdir(new_folder_path)
    print(f"已创建文件夹：{new_folder_path}")

    return new_folder_path, next_number


def app_full_screen(templates_dict, app_name):
    ##################################################
    # 最小化pycharm，最大化目标APP
    ##################################################
    screen_image = screen_capture()

    # 将python程序运行软件最小化
    click_position = template_matching(screen_image, "Python min", templates_dict)
    pyautogui.moveTo(click_position[0], click_position[1])
    # 模拟点击鼠标左键
    pyautogui.click()
    time.sleep(0.5)

    try:
        click_position = template_matching(screen_image, app_name + " full screen", templates_dict)
        pyautogui.moveTo(click_position[0], click_position[1])
        # 模拟点击鼠标左键
        pyautogui.click()
        time.sleep(0.5)
    except:
        pass


def do_basic_operation(action, parameter=None, templates_dict=None, save_data=False, target_folder=None):
    ##################################################
    # 将动作转换为实际的键鼠操作
    # 包含最基本的键鼠操作，包括点击按钮、双击按钮、字符输入、热键等
    # action：具体的工作，click doubleclick left_mouse_up等
    # parameter：按钮名称、像素位置、组合按键等
    # templates_dict: 一个字典存储着所有按钮的模板，当执行鼠标点击功能时会使用
    ##################################################

    ##################################
    # 首先是鼠标操作
    ##################################
    if action.startswith("click"):
        # button = re.search(r'\((.*?)\)', action).group(1)
        if isinstance(parameter, str):  # 如果参数是字符串，则按照模板匹配进行点击
            button = parameter  # click的参数规定为按钮名称
            screen_image = screen_capture()
            click_position = template_matching(screen_image, button, templates_dict)

        elif isinstance(parameter, list):
            click_position = parameter

        # 移动鼠标到屏幕的坐标 (x, y) 处 并点击
        pyautogui.moveTo(click_position[0], click_position[1])
        pyautogui.click()

        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                if isinstance(parameter, str):
                    f.write(f"  {action}({button})   [{click_position[0]}, {click_position[1]}] \n")
                else:
                    f.write(f"  {action}   [{click_position[0]}, {click_position[1]}] \n")

    elif action.startswith("press"):
        button = parameter
        pyautogui.press(button)

        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action}({button}) \n")

    elif action.startswith("doubleclick"):
        # button = re.search(r'\((.*?)\)', action).group(1)
        button = parameter # doubleclick的参数规定为按钮名称
        screen_image = screen_capture()
        click_position = template_matching(screen_image, button, templates_dict)

        # 移动鼠标到屏幕的坐标 (x, y) 处
        pyautogui.moveTo(click_position[0], click_position[1])
        pyautogui.doubleClick()

        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action}({button})  [{click_position[0]}, {click_position[1]}] \n")

    elif action.startswith("left_mouse_down"):
        # 按住左键不松开
        # 按住鼠标左键的参数为像素位置 放在列表或元组中
        mouse_position = parameter
        pyautogui.mouseDown(x=mouse_position[0], y=mouse_position[1], button='left')
        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action} [{mouse_position[0]}, {mouse_position[1]}] \n")

    elif action.startswith("right_mouse_down"):
        # 按住右键不松开
        # 按住鼠标右键的参数为像素位置 放在列表或元组中
        mouse_position = parameter
        pyautogui.mouseDown(x=mouse_position[0], y=mouse_position[1], button='right')
        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action} [{mouse_position[0]}, {mouse_position[1]}] \n")

    elif action.startswith("middle_mouse_down"):
        # 按住中键不松开
        # 按住鼠标中键的参数为像素位置 放在列表或元组中
        mouse_position = parameter
        pyautogui.mouseDown(x=mouse_position[0], y=mouse_position[1], button='middle')
        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action} [{mouse_position[0]}, {mouse_position[1]}] \n")

    elif action.startswith("left_mouse_up"):
        # 松开左键
        pyautogui.mouseUp(button='left')
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action}\n")

    elif action.startswith("right_mouse_up"):
        # 松开右键
        pyautogui.mouseUp(button='right')
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action}\n")

    elif action.startswith("middle_mouse_up"):
        # 松开中键
        pyautogui.mouseUp(button='middle')
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action}\n")

    elif action.startswith("moveto"):
        # 将鼠标移动至指定位置
        # 参数为像素位置 放在列表或元组中
        mouse_position = parameter
        pyautogui.moveTo(x=mouse_position[0], y=mouse_position[1], duration=0)
        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action} [{mouse_position[0]}, {mouse_position[1]}] \n")

    elif action.startswith("left_dragto"):
        # 将鼠标拖拽至指定位置
        # 参数为像素位置 放在列表或元组中
        mouse_position = parameter
        pyautogui.dragTo(x=mouse_position[0], y=mouse_position[1], duration=1, button='left')
        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action} [{mouse_position[0]}, {mouse_position[1]}] \n")

    elif action.startswith("right_dragto"):
        # 将鼠标拖拽至指定位置
        # 参数为像素位置 放在列表或元组中
        mouse_position = parameter
        pyautogui.dragTo(x=mouse_position[0], y=mouse_position[1], duration=0.1, button='right')
        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action} [{mouse_position[0]}, {mouse_position[1]}] \n")

    elif action.startswith("middle_dragto"):
        # 将鼠标拖拽至指定位置
        # 参数为像素位置 放在列表或元组中
        mouse_position = parameter
        pyautogui.dragTo(x=mouse_position[0], y=mouse_position[1], duration=0.1, button='middle')
        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action} [{mouse_position[0]}, {mouse_position[1]}] \n")

    ##################################
    # 加下来是键盘操作
    ##################################
    elif action.startswith("input"):
        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action}({parameter})\n")

        # text = re.search(r'\((.*?)\)', action).group(1)
        pyautogui.write(parameter, interval=0.001)
        # print("input", text)

    elif action.startswith("hotkey"):
        # 去除字符串开头的"hotkey("和结尾的")"，并分割剩余的字符串
        # keys = action[len("hotkey("):-1].split('+')
        keys = parameter.split('+')
        pyautogui.hotkey(*keys)
        # print("hotkey", *keys)

        # 保存txt格式数据集
        if save_data:
            with open(target_folder + r"\action.txt", "a") as f:
                # 写入新的内容
                f.write(f"  {action}({parameter})\n")

    else:
        print("指令格式错误")


def action_2_operation(action, templates_dict, save_data=False, target_folder=None):
    ##################################################
    # 将命令字符串转换为具体的键鼠操作
    # 与PC_basic_operation函数联合使用
    ##################################################
    screen_width, screen_height = pyautogui.size()  # 获取屏幕的宽度和高度
    print(action)  # action字符串操作名称和参数两个数据 如click(File)代表点击File按钮

    # 列表中包含最基本的PC键鼠操作
    basic_operation_list = ['moveto', 'click', 'doubleclick', 'left_mouse_down', 'right_mouse_down',
                            'middle_mouse_down', 'left_mouse_up', 'right_mouse_up', 'middle_mouse_up',
                            'left_dragto', 'right_dragto', 'middle_dragto', 'input', 'hotkey', 'press']

    operation_name = action.split("(")[0]  # 操作的名称
    parameter = re.search(r'\((.*?)\)', action).group(1)  # 操作的参数
    if parameter.count(',') == 1 and all(i.isdigit() for i in parameter.split(',')):
        parameter = [int(i) for i in parameter.split(',')]
    if operation_name in basic_operation_list:
        if parameter == 'Replace all':
            pass
        # 如果只是最基本的操作
        do_basic_operation(operation_name, parameter, templates_dict, save_data, target_folder)
    #########################################################
    # 接下来是一些复杂操作，针对不同的软件需要自定义多种复杂操作
    #########################################################
    # 关于文本编辑的软件，可以提供以下功能
    elif action.startswith("select_para"):
        # 用鼠标拖动方式选中某一段的内容
        # 此功能需要之前的动作已经将页面调整到指定段落开始的位置

        # 抽取出开始和结尾的段落字符串
        start_paragraph, end_paragraph = (str(int(num)).zfill(2) for num in parameter.split(','))

        first_para_identified = False  # 一个flag记录起始段的标识是否被识别到
        last_para_identified = False  # 一个flag记录起始段的标识是否被识别到
        # 首先基于OCR定位出段落指示开始的位置
        for i in range(10):
            paragraph_position = find_character_position(start_paragraph)
            if paragraph_position:
                first_paragraph_pixel_position = [paragraph_position[0]['right'] + 10, paragraph_position[0]['top']]  # 起始段的像素位置
                first_para_identified = True
                print("查找到开始段落位置")
                break

        if first_para_identified:  # 如果识别到第一段的位置，则尝试识别最后一段的位置
            # 尝试识别最终段落的位置
            for i in range(10):
                paragraph_position = find_character_position(end_paragraph)
                if paragraph_position:
                    last_paragraph_pixel_position = [screen_width, paragraph_position[0]['top']-30]  # 起始段的像素位置
                    last_para_identified = True
                    print("查找到终止段落位置")
                    break

        if first_para_identified and last_para_identified:  # 如果两个标识均被识别到
            # do_basic_operation('moveto', last_paragraph_pixel_position)  # 将鼠标移动到段落开始位置
            do_basic_operation('left_mouse_down', first_paragraph_pixel_position)
            do_basic_operation('moveto', last_paragraph_pixel_position)
            time.sleep(0.1)
            do_basic_operation('left_mouse_up', last_paragraph_pixel_position)  # 拖拽至最后一段


if __name__ == "__main__":
    # operation = 'select_para(1, 2)'
    # templates_dict = load_template()
    # # app_full_screen(templates_dict, app_name='Notepad')
    # time.sleep(0.5)
    # action_2_operation(operation, None)
    # # exit_to_origin('Notepad', templates_dict)

    create_next_folder(r"C:\postgraduater\AI PLC\LLM-project-V2\dataset\Notepad")


