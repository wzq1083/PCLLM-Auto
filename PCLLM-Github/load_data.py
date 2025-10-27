import os
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image

print(torch.__version__)

# 自定义 collate_fn 支持批量加载
def custom_collate_fn(batch):
    """
    自定义的 collate 函数，用于批量处理数据。
    :param batch: 一个批量数据的列表，每个元素是一个字典
    :return: 合并后的批量数据
    """
    tasks = [item["task"] for item in batch]
    all_images = [item["images"] for item in batch]
    actions = [item["actions"] for item in batch]

    # 将图片数据堆叠成批次
    max_image_len = max([len(images) for images in all_images])  # 找出最大图片序列长度
    length = [len(images) for images in all_images]
    padded_images = []
    for images in all_images:
        # 填充到统一长度
        padding = torch.zeros_like(images[0]).unsqueeze(0).repeat(max_image_len - len(images), 1, 1, 1)
        padded_images.append(torch.cat([images, padding], dim=0))
    images_batch = torch.stack(padded_images)

    return {
        "length": length,
        "tasks": tasks,  # 保留任务描述列表
        "images": images_batch,  # 填充后的图片批量数据
        "actions": actions  # 保留动作列表
    }


class IntelligentAssistantDataset(Dataset):
    def __init__(self, root_dir, software_filter=None, transform=None):
        """
        初始化数据集
        :param root_dir: 数据集的根目录
        :param software_filter: 软件名称的过滤列表（可选）
        :param transform: 图像的变换操作
        """
        self.root_dir = root_dir
        self.transform = transform
        self.software_filter = software_filter  # 软件名称过滤列表

        # 获取所有子文件夹
        all_software_folders = [os.path.join(root_dir, d) for d in os.listdir(root_dir) if
                                os.path.isdir(os.path.join(root_dir, d))]

        # 过滤指定的软件名称（如果提供了）
        if software_filter:
            self.task_folders = []
            for software_folder in all_software_folders:
                if os.path.basename(software_folder) in software_filter:
                    # 添加该软件下的所有任务文件夹
                    self.task_folders.extend(
                        [os.path.join(software_folder, task_folder)
                         for task_folder in os.listdir(software_folder)
                         if os.path.isdir(os.path.join(software_folder, task_folder))]
                    )
        else:
            # 如果未指定软件，加载所有任务
            self.task_folders = [
                os.path.join(software_folder, task_folder)
                for software_folder in all_software_folders
                for task_folder in os.listdir(software_folder)
                if os.path.isdir(os.path.join(software_folder, task_folder))
            ]

        pass

    def __len__(self):
        return len(self.task_folders)

    def __getitem__(self, idx):
        task_folder = self.task_folders[idx]
        txt_file = os.path.join(task_folder, "action.txt")

        # 读取txt文件
        with open(txt_file, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines()

        # 提取任务描述和动作
        task_description = []
        actions = []
        action_section = False
        for line in lines:
            line = line.strip()
            if line.startswith("task description:"):
                task_description.append(line.replace("task description:", "").strip())
            elif line.startswith("actions:"):
                action_section = True
            elif action_section:
                actions.append(line.strip())
            else:
                task_description.append(line)

        # 将任务描述合并成字符串
        task_description = "\n".join(task_description)

        # 获取图片列表
        image_files = sorted(
            [f for f in os.listdir(task_folder) if f.endswith(".png")],
            key=lambda x: int(os.path.splitext(x)[0])
        )
        images = []
        for img_file in image_files:
            img_path = os.path.join(task_folder, img_file)
            image = Image.open(img_path).convert("RGB")
            if self.transform:
                image = self.transform(image)
            images.append(image)

        return {
            "task": task_description,
            "images": torch.stack(images),
            "actions": actions
        }


import numpy as np


def construct_prompts(task, actions):
    """    构造新的提示词。
    Args:
        task (list of str): 每个任务的描述列表。
        actions (list of list of str): 每个任务对应的动作列表。

    Returns:
        list of str: 生成的新提示词列表。
    """
    prompts = []
    for i, (task_desc, action_list) in enumerate(zip(task, actions)):
        # 开始构造提示词
        prompt = f"###Human:{task_desc}<Img><ImageHere></Img>"
        for action in action_list:
            prompt += f"###Assistant:{action}###<Img><ImageHere></Img>"
        prompt += "###<Img><ImageHere></Img>"
        prompts.append(prompt)
    return prompts


# 使用示例
if __name__ == "__main__":
    from torchvision import transforms

    # 图像变换（可以根据需要调整）
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # 调整为统一尺寸
        transforms.ToTensor()           # 转换为Tensor
    ])

    dataset = IntelligentAssistantDataset(
        root_dir="dataset",  # 替换为数据集路径
        # software_filter=["Notepad", "Calculator"],
        software_filter=None,
        transform=transform
    )
    # DataLoader 支持批量处理
    dataloader = DataLoader(dataset, batch_size=2, shuffle=False, collate_fn=custom_collate_fn)

    for batch in dataloader:
        tasks = batch["tasks"]
        images = batch["images"]
        actions = batch["actions"]
        new_prompt = construct_prompts(tasks, actions)
        print(new_prompt)
