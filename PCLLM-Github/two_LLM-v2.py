"""
    v1版本两个大模型互动
    questioner将随机抽取的问题进行提问，并换一种问法
    executor负责与PC互动执行
"""
from openai import OpenAI
import random

from basic_function import *
import pyautogui
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

test_app = "wordpad"
save_data = True
model_s = ["gemini-1.5-pro-latest", "gemini-2.0-flash-exp"]

# 如果要保存数据的话，那么创建APP对应的数据集文件夹
basic_path = f"./dataset/{test_app}"
if save_data and not os.path.exists(basic_path):
    os.makedirs(basic_path)

task_type_list = ["basic_task", "intermediate_task", "advanced_task"]
# task_type_list = ["basic_task"]

# task_dict = {
#     "basic_task":
#         [
#             "Save the current document as '{}' in notepad.",
#             "Find the text '{}' in the document.",
#             "Go to line number {} in notepad.",
#             "Insert the current date and time at the cursor position in notepad.",
#             "Zoom in on the document by {}% in notepad.",
#             "Zoom out on the document by {}% in notepad.",
#             "Create a new tab.",
#             "Save the current file as {}.",
#             "Save all open files.",
#             "Undo the last operation.",
#             "Paste the content from the clipboard to the current location.",
#             "Replace {} with {}.",
#             "Restore to the default zoom level."
#         ],
#
#     "intermediate_task":
#         [
#             "Go to line number {} in notepad and insert the current date and time.",
#             "Find all occurrences of '{}' in the document and replace them with '{}', then save the document as '{}' in notepad.",
#             "Replace the text '{}' with '{}' in the document.",
#             "Go to line number {} in notepad and then save the document as '{}'.",
#             "Undo the last change in notepad, then save the document as '{}'."
#         ],
#
#     "advanced_task":
#         [
#             "Create a new tab, insert the current time, navigate to line {}, and save as {}.",
#             "Find {}, search downward, replace with {}, navigate to line {}, and save all files.",
#             "Open a new window, insert the current date and time, restore default zoom, and save as {}.",
#             "Navigate to line{}, find {}, delete the content in the line, and save all files.",
#             "Replace {} with {}, insert the current time, navigate to line{}, and save as {}.",
#             "Create a new tab, find {}, replace with {}, insert the current time, and save as {}.",
#             "Open a new window, zoom out, navigate to line {}, insert the current time, and save as {}.",
#             "Find {}, delete all matches, restore default zoom, and save as {}.",
#             "Navigate to a line, insert the date and time, zoom in, and save the current file.",
#             "Find {}, search upward, navigate to line {}, insert the current time, and save all files.",
#             "Create a new tab, insert the date and time, delete some content, and save as {}.",
#             "Find {}, replace with {}, navigate to line {}, and save as {}.",
#             "Restore default zoom, navigate to line {}, insert the date and time, and save the current file.",
#             "Create a new window, find {}, replace with {}, insert the date and time, and save as {}.",
#             "Navigate to a line, find {}, delete the matched line, and save as {}.",
#             "Find {}, replace all matches with {}, navigate to line {}, and save all files.",
#             "Create a new tab, zoom out, insert the current date and time, and save as {}.",
#             "Navigate to a line, delete some content, restore default zoom, and save all files.",
#             "Find {}, replace with {}, insert the current date and time, and save as {}.",
#             "Create a new window, find {}, navigate to line {}, delete content, and save as {}."
#         ]
# }

task_dict = {
    "basic_task": [
        "Set the unit to {} (inch, centimeter, pound)",
        "input {any ty} in the wordpad",
        "Set the font color to {} (text-red, text-blue, text-green, text-yellow, text-orange)",
        "Set the font size to {} (12, 14, 16, 18, 20)",
        "Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink)",
        "Save the document as {} (filename + rtf or xml or txt)",
        "Zoom in the view",
        "Zoom out the view",
        "Set the alignment to {} (left-aligned, right-aligned, middle-aligned , justified-aligned)",
        "Change the font to {} (Arial, Times New Roman, Courier New)}",
        "Increase the font size",
        "Decrease the font size",
        "Enable auto line break as {} (auto line break no auto line break, by window, by ruler)",
        "change the strikeout line mode on the text",
        "{} (close, open) the ruler in the wordpad",
    ],
    "intermediate_task": [
        "Set the unit to {} (inch, centimeter, pound) and Set the font size to {} (12, 14, 16, 18, 20)",
        "Zoom in the view and Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink)",
        "Change the font to {} (Arial, Times New Roman, Courier New) and Set the alignment to {} (left-aligned, right-aligned, middle-aligned, justified-aligned)",
        "Set the font color to {} (text-red, text-blue, text-green, text-yellow, text-orange) and Save the document as {} (filename + rtf or xml or txt)",
        "Enable auto line break as {} (auto line break no auto line break, by window, by ruler) and Set the unit to {} (inch, centimeter, pound)",
        "Increase the font size and Set the alignment to {} (left-aligned, right-aligned, middle-aligned, justified-aligned)",
        "Decrease the font size and Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink)",
        "Set the font size to {} (12, 14, 16, 18, 20) and Change the strikeout line mode on the text",
        "Zoom out the view and Input {} in the WordPad",
        "Set the unit to {} (inch, centimeter, pound) and Save the document as {} (filename + rtf or xml or txt)",
        "Set the font color to {} (text-red, text-blue, text-green, text-yellow, text-orange) and Enable auto line break as {} (no auto line break, by window, by ruler)",
        "Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink) and Zoom in the view",
        "Set the font to {} (Arial, Times New Roman, Courier New) and Change the strikeout line mode on the text",
        "Set the alignment to {} (left-aligned, right-aligned, middle-aligned, justified-aligned) and Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink)",
        "Zoom out the view and Set the alignment to {} (left-aligned, right-aligned, middle-aligned, justified-aligned)",
        "Save the document as {} (filename + rtf or xml or txt) and Set the font color to {} (text-red, text-blue, text-green, text-yellow, text-orange)",
        "Set the unit to {} (inch, centimeter, pound) and Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink)",
        "Change the font to {} (Arial, Times New Roman, Courier New) and Zoom in the view",
        "Enable auto line break as {} (no auto line break, by window, by ruler) and Input {} in the WordPad",
        "Set the font size to {} (12, 14, 16, 18, 20) and Set the alignment to {} (left-aligned, right-aligned, middle-aligned, justified-aligned)",
    ],

    "advanced_task": [
        "Set the unit to {} (inch, centimeter, pound), Set the font color to {} (text-red, text-blue, text-green, text-yellow, text-orange), and Set the alignment to {} (left-aligned, right-aligned, middle-aligned, justified-aligned)",
        "Save the document as {} (filename + rtf or xml or txt), Zoom in the view, and Change the strikeout line mode on the text",
        "Set the font size to {} (12, 14, 16, 18, 20), Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink), and Enable auto line break as {} (no auto line break, by window, by ruler)",
        "Zoom out the view, Set the alignment to {} (left-aligned, right-aligned, middle-aligned, justified-aligned), and Set the font to {} (Arial, Times New Roman, Courier New)",
        "Set the unit to {} (inch, centimeter, pound), Change the font to {} (Arial, Times New Roman, Courier New), and Input {} in the WordPad",
        "Increase the font size, Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink), and Enable auto line break as {} (by window, by ruler)",
        "Set the font color to {} (text-red, text-blue, text-green, text-yellow, text-orange), Save the document as {} (filename + rtf or xml or txt), and Zoom in the view",
        "Change the strikeout line mode on the text, Set the alignment to {} (left-aligned, right-aligned, middle-aligned, justified-aligned), and Enable auto line break as {} (no auto line break, by window)",
        "Set the unit to {} (inch, centimeter, pound), Set the font size to {} (12, 14, 16, 18, 20), and Zoom out the view",
        "Set the font size to {} (12, 14, 16, 18, 20), Zoom in the view, and Change the font to {} (Arial, Times New Roman, Courier New)",
        "Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink), Set the font color to {} (text-red, text-blue, text-green, text-yellow, text-orange), and Save the document as {} (filename + rtf or xml or txt)",
        "Increase the font size, Decrease the font size, and Set the font to {} (Arial, Times New Roman, Courier New)",
        "Zoom out the view, Set the font color to {} (text-red, text-blue, text-green, text-yellow, text-orange), and Set the unit to {} (inch, centimeter, pound)",
        "Enable auto line break as {} (by window, by ruler), Set the font size to {} (12, 14, 16, 18, 20), and Zoom in the view",
        "Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink), Set the font size to {} (12, 14, 16, 18, 20), and Set the unit to {} (inch, centimeter, pound)",
        "Set the alignment to {} (left-aligned, right-aligned, middle-aligned, justified-aligned), Change the font to {} (Arial, Times New Roman, Courier New), and Enable auto line break as {} (by window, by ruler)",
        "Set the unit to {} (inch, centimeter, pound), Zoom out the view, and Input {} in the WordPad",
        "Set the font color to {} (text-red, text-blue, text-green, text-yellow, text-orange), Zoom in the view, and Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink)",
        "Change the font to {} (Arial, Times New Roman, Courier New), Set the alignment to {} (left-aligned, right-aligned, middle-aligned, justified-aligned), and Zoom out the view",
        "Set the text background color to {} (background-red, background-blue, background-green, background-yellow, background-pink), Set the font size to {} (12, 14, 16, 18, 20), and Enable auto line break as {} (no auto line break, by window, by ruler)",
    ]

}


if __name__ == "__main__":
    #######################################
    # 初始化部分
    #######################################
    # 首先获取ChatGPT的API
    LLM = OpenAI(
        api_key='Your Key Here',  # this is also the default, it can be omitted
        base_url='Base URL Here'
    )

    # 打开记事本文件（里面记录了大模型系统部分的prompt），使用 UTF-8 编码方式
    with open(f'./prompt/{test_app}/prompt-{test_app}-questioner-2.txt', 'r', encoding='utf-8') as file:
        # 读取全部内容
        questioner_system_content = file.read()

    questioner_messages = [
        {"role": "system", "content": questioner_system_content},
    ]

    # 打开记事本文件（里面记录了大模型系统部分的prompt），使用 UTF-8 编码方式
    with open(f'./prompt/{test_app}/prompt-{test_app}-executor.txt', 'r', encoding='utf-8') as file:
        # 读取全部内容
        executor_system_content = file.read()

    executor_messages = [
        {"role": "system", "content": executor_system_content},
    ]

    # 加载图像模板
    templates_dict = load_template(f'template/{test_app}')

    # python运行软件最小化，应用软件全屏
    # app_full_screen(templates_dict, test_app)
    time.sleep(2)

    for model in model_s:
        basic_path_model = basic_path + f"/{model}"
        if save_data and not os.path.exists(basic_path_model):
            os.makedirs(basic_path_model)
        for task_type in task_type_list:
            basic_path_task = basic_path_model + f"/{task_type}"
            if save_data and not os.path.exists(basic_path_task):
                os.makedirs(basic_path_task)
            for i in range(71):

                # #################################################
                # # 通过questioner给出下一个任务指示15873OR
                # #################################################
                questioner_input = random.choice(task_dict[task_type])
                questioner_messages.append({"role": "user", "content": questioner_input})
                questioner_response = LLM.chat.completions.create(model="gpt-4o", messages=questioner_messages, stream=False)
                questioner_answer = ''

                content = questioner_response.choices[0].message.content
                if content:
                    questioner_answer += content

                print(questioner_answer)
                questioner_messages.pop(-1)
                print()

                #################################################
                # executor执行任务
                #################################################
                user_input = questioner_answer
                # user_input = "Increase the zoom level."

                # # 如果保存文件的话，创建相应的文件夹
                folder_created = True  # 标志位，记录文件夹有没有被成功创建
                if save_data:
                    try:
                        task_folder, folder_number = create_next_folder(basic_path_task)
                        if folder_number >=71:
                            break
                        # with open(task_folder + r"\action.txt", "a") as f:
                        #     f.write(f"task description:{user_input}\n")
                    except:
                        folder_created = False
                        # print(questioner_answer, "文件夹创建失败，请根据需要手动决定是否停止程序")
                else:
                    task_folder = None


                if folder_created:  # 如果任务文件夹被成功创建才执行动作
                    pass
                    executor_messages.append({"role": "user", "content": user_input})
                    executor_response = LLM.chat.completions.create(model=model, messages=executor_messages, stream=False)
                    executor_answer = ''

                    content = executor_response.choices[0].message.content
                    if content:
                        executor_answer += content

                    print(executor_answer)
                    print()
                    executor_messages.pop(-1)
                    ################################################
                    # 执行相应的键鼠操作
                    ################################################
                    # user_input = "1"
                    # executor_answer = 'click(File)->click(Exit)'
                    actions_list = executor_answer.split('->')

                    step = 0
                    GUI_state = screen_capture(save_fig=save_data, task_folder=task_folder, image_name=str(step))

                    task = user_input
                    for action in actions_list:
                        try:
                            step += 1
                            action_2_operation(action, templates_dict, save_data=save_data, target_folder=task_folder)
                            GUI_state = screen_capture(save_fig=save_data, task_folder=task_folder, image_name=str(step))
                            time.sleep(0.3)

                        except:
                            print(action + " error")
                            if save_data:
                                with open(task_folder + r"\action.txt", "a") as f:
                                    f.write(f"  {action}   error \n")

                    # 如果界面未退回到初始状态，下面的函数会发生作用
                    step += 1
                    for _ in range(3):
                        try:
                            exit_to_origin(test_app, templates_dict, GUI_state, save_data=save_data, task_folder=task_folder, file_name=step)
                            time.sleep(1)
                        except:
                            pass
