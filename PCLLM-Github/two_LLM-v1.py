"""
    v1版本两个大模型互动
    questioner按照自己的意愿提问
    executor负责与PC互动执行
"""

from openai import OpenAI

from template_match import *
from basic_function import *
import pyautogui
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

test_app = "calculator"
save_data = False
model = "gpt-4o"

# 如果要保存数据的话，那么创建APP对应的数据集文件夹
basic_path = f"./dataset/{test_app}"
if save_data and not os.path.exists(basic_path):
    os.makedirs(basic_path)


if __name__ == "__main__":
    #######################################
    # 初始化部分
    #######################################
    # 首先获取ChatGPT的API
    LLM = OpenAI(api_key='Your Key Here',  # this is also the default, it can be omitted
        base_url='Base URL Here'
    )

    # 打开记事本文件（里面记录了大模型系统部分的prompt），使用 UTF-8 编码方式
    with open(f'./prompt/{test_app}/prompt-{test_app}-questioner.txt', 'r', encoding='utf-8') as file:
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

    for _ in range(10):
        #################################################
        # 通过questioner给出下一个任务指示
        #################################################
        questioner_input = "给出下一个任务"
        questioner_messages.append({"role": "user", "content": questioner_input})
        questioner_response = LLM.chat.completions.create(model=model, messages=questioner_messages, stream=True)
        questioner_answer = ''
        for res in questioner_response:
            content = res.choices[0].delta.content
            if content:
                questioner_answer += content

        print(questioner_answer)
        questioner_messages.append({"role": "assistant", "content": questioner_answer})
        print()

        #################################################
        # executor执行任务
        #################################################
        user_input = questioner_answer

        # 如果保存文件的话，创建相应的文件夹
        folder_created = True  # 标志位，记录文件夹有没有被成功创建
        if save_data:
            try:
                task_folder = create_next_folder(basic_path)
                with open(task_folder + r"\action.txt", "a") as f:
                    f.write(f"task description:{user_input}\n")
            except:
                folder_created = False
                print(questioner_answer, "文件夹创建失败，请根据需要手动决定是否停止程序")
        else:
            task_folder = None

        if folder_created:  # 如果任务文件夹被成功创建才执行动作
            executor_messages.append({"role": "user", "content": user_input})
            executor_response = LLM.chat.completions.create(model=model, messages=executor_messages, stream=True)
            executor_answer = ''
            for res in executor_response:
                content = res.choices[0].delta.content
                if content:
                    executor_answer += content

            print(executor_answer)
            executor_messages.append({"role": "assistant", "content": executor_answer})
            print()

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

                except:
                    print(action + " error")
                    pass

            # 如果界面未退回到初始状态，下面的函数会发生作用
            step += 1
            exit_to_origin(test_app, templates_dict, GUI_state, save_data=save_data, task_folder=task_folder, file_name=step)
