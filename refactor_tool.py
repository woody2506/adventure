import re
import os

def update_main_py(input_file="script.py", output_py="main.py"):
    print(f"Reading '{input_file}' to generate '{output_py}'...")
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Could not find '{input_file}'. Make sure it's in the same folder.")
        return

    new_lines = []
    text_counter = 1

    # Regex to safely find pure string prints and inputs
    print_pattern = re.compile(r'^(\s*)print\s*\(\s*(["\'])(.*?)\2\s*\)\s*$')
    input_pattern = re.compile(r'^(\s*)(\w+\s*=\s*)input\s*\(\s*(["\'])(.*?)\3\s*\)\s*$')

    for line in lines:
        print_match = print_pattern.match(line)
        input_match = input_pattern.match(line)

        # Process print statements
        if print_match and "{" not in line and "+" not in line:
            indent, quote, content = print_match.groups()
            key = f"text_{text_counter:04d}"
            new_lines.append(f'{indent}print(get_text("{key}"))\n')
            text_counter += 1

        # Process input statements
        elif input_match and "{" not in line and "+" not in line:
            indent, assignment, quote, content = input_match.groups()
            key = f"input_{text_counter:04d}"
            new_lines.append(f'{indent}{assignment}input(get_text("{key}"))\n')
            text_counter += 1
            
        else:
            # Leave complex code, logic, and variables untouched
            new_lines.append(line)

    # ---------------------------------------------------------
    # Create the block of code to inject at the top of main.py
    # ---------------------------------------------------------
    header = """
# --- Language Selection Setup ---
import sys
import json
import builtins

LANG = "EN"  # Default language

# Safely extract language from arguments without breaking existing argparse
if "CN" in sys.argv:
    LANG = "CN"
    sys.argv.remove("CN")
elif "EN" in sys.argv:
    LANG = "EN"
    sys.argv.remove("EN")

# --- Load Bilingual JSON ---
def load_game_texts():
    try:
        with open("interaction.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: interaction.json not found! Please ensure it is in the same folder.")
        return {}

TEXTS = load_game_texts()

def get_text(key):
    # Try requested LANG, fallback to EN, fallback to error message
    return TEXTS.get(key, {}).get(LANG, TEXTS.get(key, {}).get("EN", f"[{key} missing]"))

# --- Input Interceptor for Chinese Commands ---
# This maps Chinese user inputs back to the English commands the game engine expects.
CMD_MAP = {
    "开始": "start", "退出": "quit", "任务": "task", "时间": "time", "天堂": "heaven",
    "菜单": "menu", "北": "north", "南": "south", "东": "east", "西": "west",
    "进": "in", "出": "out", "离开": "leave", "返回": "back",
    "看": "look", "背包": "bag", "包": "bag", "状态": "hp", "血量": "hp",
    "道德": "moral", "天气": "weather", "保存": "save", "加载": "load", "读取": "load",
    "日记": "journal", "下": "down", "下去": "go down", "上": "up", "爬": "climb",
    "跑": "run", "逃跑": "run", "攻击": "attack", "打": "strike", "防御": "defend",
    "吃": "eat", "喝": "drink", "地图": "map", "指南针": "compass",
    "祈祷": "pray", "继续": "forward", "神": "godmode", "作弊": "cheat",
    "帮助": "help", "读日记": "read diary", "看日记": "read diary",
    "拿灯": "take lamp", "拿钥匙": "take key", "拿食物": "take food"
}

original_input = builtins.input

def game_input(prompt=""):
    user_in = original_input(prompt).strip()
    if LANG == "CN":
        # If running in CN, translate the command to English for the logic
        return CMD_MAP.get(user_in, user_in)
    return user_in

# Override the default input function
builtins.input = game_input
# --------------------------------
"""
    
    # Insert the JSON loader right after the initial imports so it processes
    # sys.argv before the existing parser = argparse.ArgumentParser() runs.
    insert_idx = 0
    for i, l in enumerate(new_lines):
        if not l.startswith("import") and not l.startswith("from") and l.strip() != "":
            insert_idx = i
            break

    new_lines.insert(insert_idx, header)

    # Write the new main.py
    with open(output_py, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"\n✅ Success! Updated '{output_py}' with the Input Interceptor.")
    print("You can now type '开始', '北', '南', '看', etc., when running in CN mode!")

if __name__ == "__main__":
    update_main_py()