import os
import time

from openai import OpenAI

from basic_function import *
from template_match import *
import re
import pyautogui
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

test_app = "notepad"
save_data = False

# 如果要保存数据的话，那么创建APP对应的数据集文件夹
basic_path = f"./dataset/{test_app}"
if save_data and not os.path.exists(basic_path):
    os.makedirs(basic_path)

if __name__ == "__main__":
    #######################################
    # 初始化部分，获取ChatGPT的API连接0g
    #######################################
    # 首先获取ChatGPT的API
    LLM = OpenAI(
        api_key='Your Key Here',  # this is also the default, it can be omitted
        base_url='Base URL Here'
    )

    # 打开记事本文件（里面记录了大模型系统部分的prompt），使用 UTF-8 编码方式
    with open(f'./prompt/{test_app}/prompt-{test_app}-executor.txt', 'r', encoding='utf-8') as file:
        # 读取全部内容
        system_content = file.read()

    messages = [
        {"role": "system", "content": system_content},
    ]

    # # 加载图像模板
    templates_dict = load_template(f'template/{test_app}')

    #######################################
    # 初始化结束，金进入主循环
    #######################################

    while True:
        user_input = input('User:')
        # user_input = "zoom in"
        # app_full_screen(templates_dict, test_app)  # 将python应用最小化，将目标APP全屏

        # 如果保存文件的话，创建相应的文件夹
        folder_created = True  # 标志位，记录文件夹有没有被成功创建
        if save_data:
            try:
                task_folder = create_next_folder(basic_path)
                with open(task_folder + r"\action.txt", "a") as f:
                    f.write(f"task description:{user_input}\n")
            except:
                folder_created = False
                print(user_input, "文件夹创建失败，请根据需要手动决定是否停止程序")
        else:
            task_folder = None

        messages.append({"role": "user", "content": user_input})
        response = LLM.chat.completions.create(model="gpt-4o", messages=messages, stream=False)
        answer = ''
        # for res in response:
        #     content = res.choices[0].delta.content
        #     if content:
        #         answer += content

        content = response.choices[0].message.content
        if content:
            answer += content
        messages.pop(-1)
        print(answer)
        print()

        ################################################
        # 执行相应的键鼠操作
        ################################################
        time.sleep(3)

        task_folder = None
        actions_list = answer.split('->')

        step = 0
        GUI_state = screen_capture(save_fig=save_data, task_folder=task_folder, image_name=str(step))

        task = user_input
        for action in actions_list:
            try:
                step += 1
                action_2_operation(action, templates_dict, save_data=save_data, target_folder=task_folder)
                GUI_state = screen_capture(save_fig=save_data, task_folder=task_folder, image_name=str(step))

            except:
                print(action + " error")
                pass

        # 如果界面未退回到初始状态，下面的函数会发生作用
        step += 1
        exit_to_origin(test_app, templates_dict, GUI_state, save_data=save_data, task_folder=task_folder, file_name=step)

