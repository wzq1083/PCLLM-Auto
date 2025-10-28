# PCLLM-Auto
# Quick Start
PCLLM is a solution that leverages large language model technology to automate PC tasks. Refer to the content below to complete the quick setup.

# Prerequisites

- **Operating System**: Windows (Recommended for optimal compatibility)
- **Python**: 3.8 or higher

# Installation
1.Clone the repository
```bash
https://github.com/wzq1083/PCLLM-Auto.git
```
2.Configure environment
```bash
conda create -n PCLLM python=3.8
conda activate PCLLM
pip install -r requirements.txt
```
# Preparation

Before running PCLLM, you need to prepare the template and prompt files for your target application.

1.  **Create Template Folder & Screenshots**
    Navigate to the `template` directory and create a new subfolder for your target application. Take screenshots of the buttons or UI elements you need to click within the app. Save these images as templates with specific, meaningful names inside this subfolder.

2.  **Create Prompt Folder & File**
    Inside the `prompt` directory, create a subfolder with the **exact same name** you used in the previous step. Then, create a text file inside this prompt subfolder named in the following format: `prompt-{app_name}-executor.txt`.

3.  **Write the Prompt**
    Edit the newly created `.txt` file and write the software operation prompts. 
    **Important:** You must explicitly instruct the large language model to output commands in the exact format: `Action 1 -> Action 2 -> ...`. Otherwise, the project will be unable to parse the instructions.(an example can be seen at the bottom of the page)

## Run the Program

1.  **Configure Parameters**
    Open `main.py` and modify the variable values on lines 13 and 14.

    ```python
    test_app = "notepad"  # Replace "notepad" with your target application name
    save_data = False     # Set this to True to enable automatic logging
    ```

    - **`test_app`**: Set this to the name of your target application (this should match the folder names you created in the `template` and `prompt` directories).
    - **`save_data`**: When set to `True`, the program will automatically record the execution process of the large language model. The results will be saved in the `dataset` folder.

2.  **Execute the Script**
    Run the `main.py` file to start the automation process.
    
4.  **Interact with the Model**
    - Ensure the target application (e.g., Notepad) is open and visible on your desktop.
    - Once the script is running, you can enter your commands in the terminal.
    - The large language model will automatically output responsive actions (e.g., `Click -> Type -> Save`) to operate the application based on your input.

# Prompt Example

Below is a complete example of a prompt file for Notepad (`prompt-notepad-executor.txt`):

```bash
A dictionary stores the hierarchical relationship of software buttons. For example, {"1": {"2": {"5": {}}, "3": {"6": {}}, "4": {}}} means that when button 1 is clicked, a new screen reveals buttons 2, 3, and 4. Clicking button 2 reveals button 5, and clicking button 3 reveals button 6. Buttons 4, 5, and 6 do not reveal any new buttons.

The button hierarchy dictionary for Notepad is:
notebook_dict = {
    "File": {
        "New tab": {}, "New window": {}, "Open": {}, "Save all": {}, "Page setup": {},
        "Print": {}, "Close tab": {}, "Close window": {}, "Exit": {},
        "Save": {
            "Save path": {},
            "Save file name": {},
            "Save file confirm": {"Overwrite confirm": {}, "Overwrite cancel": {}},
            "Save file cancel": {}
        },
        "Save as": {
            "Save path": {},
            "Save file name": {},
            "Save file confirm": {"Overwrite confirm": {}, "Overwrite cancel": {}},
            "Save file cancel": {}
        }
    },
    "Edit": {
        "Undo": {}, "Cut": {}, "Copy": {}, "Paste": {}, "Delete": {},
        "Find": {
            "Find box": {}, "Search up": {}, "Search down": {}, "Find box clear": {}, "Exit find": {}
        },
        "Replace": {
            "Find box": {}, "Search up": {}, "Search down": {}, "Replace box": {}, "Replace one": {},
            "Replace all": {}, "Exit replace": {}, "Find box clear": {}, "Replace box clear": {}
        },
        "Goto": {
            "Goto linenum clear": {},
            "Goto linenum input": {},
            "Goto confirm": {"Line error OK": {}},
            "Goto cancel": {}
        },
        "TimeDate": {}
    },
    "View": {
        "Zoom": {
            "Zoom in": {},
            "Zoom out": {},
            "Restore default zoom": {}
        }
    }
}

Specific buttons have corresponding keyboard shortcuts:
- Cut: ctrl+x
- Copy: ctrl+c
- Paste: ctrl+v
- Find: ctrl+f
- Replace: ctrl+h
- New tab: ctrl+n
- New Window: ctrl+shift+n
- Open: ctrl+o
- Save: ctrl+s
- Save as: ctrl+shift+s
- Save all: ctrl+alt+s
- Print: ctrl+p
- Close tab: ctrl+w
- Close window: ctrl+shift+w
- Undo: ctrl+z
- Find next: f3
- Find previous: shift+f3
- Goto: ctrl+g
- Select all: ctrl+a
- TimeDate: f5
- Zoom in: ctrl+add
- Zoom out: ctrl+-
- Restore default zoom: ctrl+0
Using the corresponding hotkey is equivalent to directly clicking the button.

Available operations and their formats:
- Click button: click(button_name)
- Double-click: doubleclick(button_name)
- Press key: press(key_name)
- Input text: input(text_content)
- Hotkey combination: hotkey(key_combination)
- Select paragraph: select_para(start_para,end_para) - Use two-digit numbers with leading zeros

Special operation sequences:

Find text "111":
hotkey(ctrl+f)->click(Find box clear)->click(Find box)->input(111)->click(Search down)->click(Exit find)

Replace "111" with "222":
hotkey(ctrl+h)->click(Find box clear)->click(Find box)->input(111)->click(Replace box clear)->click(Replace box)->input(222)->click(Replace all)->click(Exit replace)

Go to line 5:
hotkey(ctrl+g)->click(Goto linenum clear)->click(Goto linenum input)->input(5)->click(Goto confirm)->click(Goto cancel)

Save file as "111.txt":
hotkey(ctrl+shift+s)->click(Save path)->click(Save file name)->hotkey(ctrl+a)->input(111.txt)->press(enter)->click(Overwrite confirm)

IMPORTANT NOTES:
- Top-level menu items (File, Edit, View) require double-click to access their sub-buttons
- Example: to click Exit: click(File)->doubleclick(Exit)
- ALWAYS use hotkeys when available
- Output ONLY the formatted operation sequence like: hotkey(ctrl+c)->click(button1)->click(button2)->input(text)
- No additional explanations or outputs

You are an operator familiar with Notepad operations. Based on user requests, output only the corresponding mouse/keyboard operations in the specified format.
