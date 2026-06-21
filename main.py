import random
import json
import os
import time
import datetime
import argparse


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
# start settings

have_list = []
game_over = False
light = False
hp = 5
l = 'a lamp, '
k = 'a key, '
n = 'a note, '
s = 'a high altar, '
f = 'some food, '
w = ' and a bottle of water '
p = 'a pick-axe'
sc = 'a scroll, '
secret_unlocked = False
map_unlocked = False
amulet = False
turn_count = 0
chain1 = False
chain2 = False
diary_read = False
legacy_unlocked = False
new_game_plus = False
ng_amulet = False
ng_compass = False
ng_diary = False
current_room = "road"
torch = False
no_light_run = False
all_collected = False
force_in_cave = False
rune1 = False
rune2 = False
rune3 = False
faith = 0
sky = False
moon = False
trap_protect = False
rune = 'a rune'
grandmother = False
gate_unlock = False
old_diary_readed = False
grave_diary_read = False
force_over = False
game_back = False
play_count = 1
tomb_unlocked = False
old_note_readed = False
swamp_visited = False
swamp_quest = False
lily_count = 0
festival_mode = False
festival_steps = 0
map_unlocked = False
cleared_ending = False
merchant_story_stage = 0
tower_ghost_story = 0
swamp_spirit_story = 0
hut_ghost_story = 0
death_count = 0
misty_end = False


# Military Fort NPC Progress
fort_unlocked = False
soldier_task_done = False
lieutenant_task_done = False
colonel_diary_collected = 0
military_password = ""
has_military_key = False

# Orc Tribe
orc_friend = False
orc_totem_found = False

# Elf Grove
elf_rune_puzzle_solved = False
elf_blessing = False

# Hobbit Camp
hobbit_trap_learned = False

# Giant Cliffside
giant_path_opened = False

# Titan Easter Egg (3rd Playthrough Only)
titan_meet = False

# Special Item Flags
has_elf_amulet = False
has_trap_tool = False
# Weather
current_weather = "Clear"
weather_duration = random.randint(4, 7)
visibility = 100
move_penalty = 0
weather_damage = 0

# Day & Night System
time_period = "day"
step_count = 0

# Morality System
good = 0
evil = 0

# Death remember
death_location = ""
death_corpse_item = ""
has_death_corpse = False

one_hole_in = False
two_hole_in = False
three_hole_in = False
four_hole_in = False
gnome_hole_in = False
child_hole_in = False

MSG_FILE = "message_wall.json"

DEFAULT_MESSAGES = [
    {"name": "Wanderer", "msg": "I shouldn't have come here.", "time": "2026-05-30"},
    {"name": "Victim", "msg": "The dev is so evil.", "time": "2026-05-30"},
    {"name": "Regret", "msg": "3 runs is pure pain.", "time": "2026-05-30"},
    {"name": "TiredGamer", "msg": "I will never play again.", "time": "2026-05-30"}
]

parser = argparse.ArgumentParser(description="Death Adventure")
parser.add_argument("-g",'-G',"-godmode",'-GODMODE',dest="godmode", action="store_true", help="Enable invincibility and trap protection")
parser.add_argument("-c",'-C', "-cheat",'-CHEAT',dest="cheat", action="store_true", help="Unlock all key items and max stats")
args = parser.parse_args()

def load_messages():
    if not os.path.exists(MSG_FILE):
        with open(MSG_FILE, "w") as f:
            json.dump(DEFAULT_MESSAGES, f, indent=2)
    with open(MSG_FILE, "r") as f:
        return json.load(f)

def save_message(name, msg):
    messages = load_messages()
    name = name[:12].strip()
    msg = msg[:60].strip()
    if not name:
        name = "Anonymous"
    if not msg:
        msg = "..."
    new_msg = {
        "name": name,
        "msg": msg,
        "time": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    messages.append(new_msg)
    if len(messages) > 50:
        messages = messages[-50:]
    with open(MSG_FILE, "w") as f:
        json.dump(messages, f, indent=2)

def show_message_wall():
    messages = load_messages()
    print("\n" + "="*60)
    print(get_text("text_0001"))
    print("="*60)
    for idx, m in enumerate(messages[-20:], 1):
        print(f"{idx:2d}. [{m['name']}] {m['msg']} ({m['time']})")
    print("="*60)

# Save / Load System
def save_game():
    global have_list, hp, light, torch, amulet, diary_read, legacy_unlocked
    global rune1, rune2, rune3, faith, new_game_plus, current_room
    global play_count, game_back, grandmother, old_diary_readed, grave_diary_read
    global trap_protect, secret_unlocked, map_unlocked, chain1, chain2, tomb_unlocked
    global cleared_ending,achievements

    data = {
        "have_list": have_list,
        "hp": hp,
        "light": light,
        "torch": torch,
        "amulet": amulet,
        "diary_read": diary_read,
        "legacy_unlocked": legacy_unlocked,
        "rune1": rune1,
        "rune2": rune2,
        "rune3": rune3,
        "faith": faith,
        "new_game_plus": new_game_plus,
        "current_room": current_room,
        "play_count": play_count,
        "game_back": game_back,
        "grandmother": grandmother,
        "old_diary_readed": old_diary_readed,
        "grave_diary_read": grave_diary_read,
        "trap_protect": trap_protect,
        "secret_unlocked": secret_unlocked,
        "map_unlocked": map_unlocked,
        "chain1": chain1,
        "chain2": chain2,
        "tomb_unlocked": tomb_unlocked,
        "cleared_ending": cleared_ending,
        "achievements": achievements
    }
    with open("save.json", "w") as f:
        json.dump(data, f)
    print(get_text("text_0002"))

# Load game
def load_game():
    global have_list, hp, light, torch, amulet, diary_read, legacy_unlocked
    global rune1, rune2, rune3, faith, new_game_plus, current_room
    global play_count, game_back, grandmother, old_diary_readed, grave_diary_read
    global trap_protect, secret_unlocked, map_unlocked, cleared_ending
    global achievements

    try:
        with open("save.json", "r") as f:
            data = json.load(f)
        have_list = data["have_list"]
        hp = data["hp"]
        light = data["light"]
        torch = data["torch"]
        amulet = data["amulet"]
        diary_read = data["diary_read"]
        legacy_unlocked = data["legacy_unlocked"]
        rune1 = data["rune1"]
        rune2 = data["rune2"]
        rune3 = data["rune3"]
        faith = data["faith"]
        new_game_plus = data["new_game_plus"]
        current_room = data["current_room"]
        play_count = data["play_count"]
        game_back = data["game_back"]
        achievements = data['achievements']
        grandmother = data.get("grandmother", False)
        old_diary_readed = data.get("old_diary_readed", False)
        grave_diary_read = data.get("grave_diary_read", False)
        trap_protect = data.get("trap_protect", False)
        secret_unlocked = data.get("secret_unlocked", False)
        map_unlocked = data.get("map_unlocked", False)
        cleared_ending = data.get("cleared_ending", False)
        print(get_text("text_0003"))
        print(f"HP: {hp}")
    except:
        print(get_text("text_0004"))

achievements = {
    "First Blood": False,
    "Reach Floor 2": False,
    "Collect 5 Items": False,
    "Defeat 3 Ghosts": False,
    "Break Curse": False,
    "Full Moon Clear": False,
    "Swamp Spirit Peace": False,
    "True Ending": False,
    "Dark Path Survivor": False,
    "Joke Master": False,
    "Death Collector": False
}
tasks = {
    "Find 3 runes": False,
    "Open the cave grate": False,
    "Reach the altar": False,
    "Read explorer diary": False,
    "Enter the tomb": False,
    "Help the swamp spirit": False,
    "Climb the watchtower": False,
    "Unlock the family truth": False
}

def unlock_achievement(name):
    if name in achievements and not achievements[name]:
        achievements[name] = True
        print(f"\n[ACHIEVEMENT UNLOCKED] {name}\n")

def update_task(name):
    if name in tasks and not tasks[name]:
        tasks[name] = True
        print(f"\n[TASK COMPLETED] {name}\n")

def refresh_panels(aw, tw):
    aw.clear()
    aw.box()
    aw.addstr(1, 2, "ACHIEVEMENTS")
    for i in range(len(achievements)):
        n, d = achievements[i]
        m = "[✓]" if d else "[ ]"
        aw.addstr(2 + i, 2, f"{m} {n[:16]}")
    aw.refresh()

    tw.clear()
    tw.box()
    tw.addstr(1, 2, "TASK LOG")
    for i in range(len(tasks)):
        n, d = tasks[i]
        m = "[✓]" if d else "[ ]"
        tw.addstr(2 + i, 2, f"{m} {n[:18]}")
    tw.refresh()

def show_journal():
    print("\n" + "="*60)
    print(get_text("text_0005"))
    print("="*60)
    print(f"Play Count: {play_count}")
    print(f"HP: {hp}")
    print(f"Good: {good} | Evil: {evil}")
    print(get_text("text_0006"))
    print(f"Rune 1: {rune1} | Rune 2: {rune2} | Rune 3: {rune3}")
    print(get_text("text_0007"))
    print(f"Read Explorer Diary: {diary_read}")
    print(f"Read Wizard Diary: {old_diary_readed}")
    print(f"Read Grave Diary: {grave_diary_read}")
    print(get_text("text_0008"))
    for task_name, done in tasks.items():
        mark = "[✓]" if done else "[ ]"
        print(f"{mark} {task_name}")
    print("="*60)

def get_last_player_name():
    try:
        messages = load_messages()
        if messages:
            return messages[-1]["name"]
    except:
        pass
    return ""

# weather
def update_weather():
    global current_weather, weather_duration, visibility, move_penalty, weather_damage
    weathers = ["clear", "light_rain", "heavy_rain", "fog", "windy", "thunderstorm", "snow"]
    current_weather = random.choice(weathers)
    weather_duration = random.randint(4, 7)
    visibility = 100
    move_penalty = 0
    weather_damage = 0

    if current_weather == "fog":
        visibility = 35
    elif current_weather == "light_rain":
        visibility = 75
    elif current_weather == "heavy_rain":
        visibility = 45
        move_penalty = 1
        weather_damage = 1
    elif current_weather == "thunderstorm":
        visibility = 25
        move_penalty = 2
        weather_damage = 2
    elif current_weather == "snow":
        visibility = 40
        move_penalty = 1
        weather_damage = 1
    elif current_weather == "windy":
        visibility = 65

def print_weather():
    print(f"\nWeather: {current_weather} | Visibility: {visibility}%")
    if weather_damage > 0:
        print(get_text("text_0009"))

def military_fort():
    global hp, good, evil, soldier_task_done, lieutenant_task_done, colonel_diary_collected
    global fort_unlocked, military_password, has_military_key, trap_protect, have_list
    print(get_text("text_0010"))
    print(get_text("text_0011"))
    print(get_text("text_0012"))

    while True:
        cmd = input(get_text("input_0013"))
        if cmd == "back":
            print(get_text("text_0014"))
            break
        elif cmd == "east_sentry":
            if not soldier_task_done:
                print(get_text("text_0015"))
                print(get_text("text_0016"))
                sub_cmd = input(get_text("input_0017"))
                if sub_cmd == "help":
                    if "some food" in have_list:
                        have_list.remove("some food")
                        soldier_task_done = True
                        good += 8
                        has_military_key = True
                        print(get_text("text_0018"))
                        print(get_text("text_0019"))
                    else:
                        print(get_text("text_0020"))
                elif sub_cmd == "loot":
                    evil += 12
                    hp -= 3
                    print(get_text("text_0021"))
                elif sub_cmd == "leave":
                    continue
            else:
                print(get_text("text_0022"))
        elif cmd == "swamp_command":
            if not lieutenant_task_done:
                print(get_text("text_0023"))
                print(get_text("text_0024"))
                print(get_text("text_0025"))
                ans = input(get_text("input_0026"))
                if ans == "R1R2R3":
                    lieutenant_task_done = True
                    military_password = "FORT739"
                    good += 10
                    trap_protect = True
                    print(get_text("text_0027"))
                else:
                    hp -= 5
                    print(get_text("text_0028"))
            else:
                print(get_text("text_0029"))
        elif cmd == "top_headquarters":
            if colonel_diary_collected < 3:
                print(get_text("text_0030"))
                print(get_text("text_0031"))
            else:
                print(get_text("text_0032"))
                good += 15
                have_list.append("military archive document")
                print(get_text("text_0033"))
        else:
            print(get_text("text_0034"))
        
def orc_tribe_dungeon():
    global hp, good, evil, orc_friend, orc_totem_found, have_list
    print(get_text("text_0035"))
    print(get_text("text_0036"))
    while True:
        cmd = input(get_text("input_0037"))
        if cmd == "back":
            print(get_text("text_0038"))
            break
        elif cmd == "search_totem":
            if not orc_totem_found:
                print(get_text("text_0039"))
                orc_totem_found = True
                have_list.append("orc tribal totem")
            else:
                print(get_text("text_0040"))
        elif cmd == "negotiate":
            if orc_totem_found:
                orc_friend = True
                good += 18
                have_list.append("orc mining pickaxe")
                print(get_text("text_0041"))
            else:
                print(get_text("text_0042"))
        elif cmd == "raid":
            evil += 30
            hp -= 8
            print(get_text("text_0043"))
        else:
            print(get_text("text_0044"))

def titan_guardian_easter():
    global titan_meet, good, evil, hp
    print(get_text("text_0045"))
    print(get_text("text_0046"))
    if not titan_meet:
        titan_meet = True
        choice = input(get_text("input_0047"))
        if choice == "offer_prayer":
            good += 30
            hp = 99
            print(get_text("text_0048"))
        elif choice == "confess_sins":
            evil = 0
            print(get_text("text_0049"))
        elif choice == "depart":
            print(get_text("text_0050"))
    else:
        print(get_text("text_0051"))

# Mistery
def forgotten_archive():
    global hp, have_list, good, evil, faith, game_over, game_back
    global has_death_corpse, death_location, death_corpse_item,current_room,one_hole_in,light,torch,trap_protect,gnome_hole_in

    current_room = 'forgotten_achive'
    print(get_text("text_0052"))
    print(get_text("text_0053"))
    print(get_text("text_0054"))
    print(get_text("text_0055"))
    print(get_text("text_0056"))

    current_room = "rune_hall"
    mistake_streak = 0
    mirror_angles = [0, 0, 0]
    correct_rune_order = ["sun", "moon", "star", "void"]
    rune_step = 0
    balance_target = 7
    final_code = "327"

    item_weights = {
        "a key": 1,
        "a lamp": 2,
        "rope": 3,
        "flint": 1,
        "a pick-axe": 5,
        "gold coins": 4
    }

    while True:
        if has_death_corpse and death_location == current_room:
            print(get_text("text_0057"))
        cmd = input("archive> ").strip().lower()

        if cmd == "leave" or cmd == "back" or cmd == 'walk back':
            print(get_text("text_0058"))
            gamestart()
            return

        elif cmd == "bag":
            for item in have_list:
                print(item)
            continue

        elif cmd == "hp":
            print(f"HP: {hp}")
            continue
        elif cmd == "examine corpse" or cmd == 'corpse' or cmd == 'search corpse' or cmd == 'find corpse':
            if has_death_corpse and death_location == current_room:
                print(get_text("text_0059"))
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print(get_text("text_0060"))
                has_death_corpse = False
            else:
                print(get_text("text_0061"))

        elif current_room == "rune_hall":
            if cmd == "look":
                print(get_text("text_0062"))
                print(get_text("text_0063"))
                print(get_text("text_0064"))
                print(get_text("text_0065"))
                print(get_text("text_0066"))
                print(get_text("text_0067"))
                print(get_text("text_0068"))

            elif cmd.startswith(""):
                rune_name = cmd.split()[1] if len(cmd.split()) > 1 else ""
                if rune_name not in ["sun", "moon", "star", "void"]:
                    print(get_text("text_0069"))
                    continue

                if rune_name == correct_rune_order[rune_step]:
                    rune_step += 1
                    print(f"Pedestal {rune_name} glows faintly.")
                    mistake_streak = 0
                    if rune_step == 4:
                        print(get_text("text_0070"))
                        current_room = "mirror_hall"
                        rune_step = 0
                else:
                    mistake_streak += 1
                    damage = 1 if mistake_streak < 3 else 3
                    hp -= damage
                    print(f"Wrong order. Arcane energy shocks you. HP -{damage}")
                    jump_scare_face()
                    rune_step = 0
                    if hp <= 0:
                        print(get_text("text_0071"))
                        game_over = True
                        game_back = True
                        break

            else:
                print(get_text("text_0072"))

        elif current_room == "balance_hall_clear":
            if cmd == "forward":
                current_room = "core_room"
            elif cmd == "workshop":
                print(get_text("text_0073"))
                current_room = "gnome_workshop"
            elif cmd == "back":
                current_room = "balance_hall"
            else:
                print(get_text("text_0074"))
        elif current_room == "gnome_workshop":
            if cmd == "look":
                print(get_text("text_0075"))
                print(get_text("text_0076"))
                print(get_text("text_0077"))
                print(get_text("text_0078"))

            elif cmd == "talk to gnome" or cmd == "talk bryn" or cmd == "talk":
                if not hasattr(forgotten_archive, 'gnome_met'):
                    print(get_text("text_0079"))
                    print(get_text("text_0080"))
                    print(get_text("text_0081"))
                    hp -= 1
                    if hp <= 0:
                        print(get_text("text_0082"))
                        game_back = True
                        game_over = True
                        break
                    forgotten_archive.gnome_met = 1
                elif forgotten_archive.gnome_met == 1:
                    print(get_text("text_0083"))
                    print(get_text("text_0084"))
                    print(get_text("text_0085"))
                    print(get_text("text_0086"))
                    print(get_text("text_0087"))
                    forgotten_archive.gnome_met = 2
                    faith += 5
                else:
                    print(get_text("text_0088"))
                    print(get_text("text_0089"))

            elif cmd == "ask wizard" and forgotten_archive.gnome_met >= 2:
                print(get_text("text_0090"))
                print(get_text("text_0091"))
                print(get_text("text_0092"))
                print(get_text("text_0093"))

            elif cmd == "ask curse" and forgotten_archive.gnome_met >= 2:
                print(get_text("text_0094"))
                print(get_text("text_0095"))
                print(get_text("text_0096"))
                print(get_text("text_0097"))

            elif cmd == "ask himself" and forgotten_archive.gnome_met >= 2:
                print(get_text("text_0098"))
                print(get_text("text_0099"))
                print(get_text("text_0100"))
                print(get_text("text_0101"))

            elif cmd == "ask dwarf" and forgotten_archive.gnome_met >= 2:
                print(get_text("text_0102"))
                print(get_text("text_0103"))
                print(get_text("text_0104"))
                print(get_text("text_0105"))
                print(get_text("text_0106"))
                print(get_text("text_0107"))

            elif cmd == "ask hint" or cmd == "hints" and forgotten_archive.gnome_met >= 2:
                print(get_text("text_0108"))
                print(get_text("text_0109"))

            elif cmd == "hint runes" and forgotten_archive.gnome_met >= 2:
                if faith >= 2:
                    faith -= 2
                    print(get_text("text_0110"))
                    print(get_text("text_0111"))
                else:
                    print(get_text("text_0112"))

            elif cmd == "upgrade lantern" and forgotten_archive.gnome_met >= 2:
                if "a lamp" in have_list and good >= 10:
                    have_list.remove("a lamp")
                    have_list.append("eternal rune lantern")
                    light = True
                    torch = True
                    print(get_text("text_0113"))
                    print(get_text("text_0114"))
                    print(get_text("text_0115"))
                else:
                    print(get_text("text_0116"))

            elif cmd == "free gnome" or cmd == "help him leave":
                if good >= 15 and forgotten_archive.gnome_met >= 2:
                    print(get_text("text_0117"))
                    print(get_text("text_0118"))
                    print(get_text("text_0119"))
                    print(get_text("text_0120"))
                    print(get_text("text_0121"))
                    print(get_text("text_0122"))
                    print(get_text("text_0123"))
                    good += 15
                    faith += 10
                    trap_protect = True
                    gnome_hole_in = True
                    have_list.append('gnome master toolkit')
                    forgotten_archive.gnome_met = 3
                else:
                    print(get_text("text_0124"))

            elif cmd == "steal from him" or cmd == "take tools":
                if forgotten_archive.gnome_met >= 2:
                    print(get_text("text_0125"))
                    print(get_text("text_0126"))
                    print(get_text("text_0127"))
                    print(get_text("text_0128"))
                    print(get_text("text_0129"))
                    have_list.append("gnome toolkit")
                    evil += 20
                    forgotten_archive.gnome_met = 0
                    gnome_hole_in = True
                    current_room = "balance_hall_clear"
                else:
                    print(get_text("text_0130"))

            elif cmd == "attack gnome" or cmd == "kill bryn":
                print(get_text("text_0131"))
                evil += 5
            elif cmd == "joke" and forgotten_archive.gnome_met >= 2:
                print(get_text("text_0132"))
                print(get_text("text_0133"))
                print(get_text("text_0134"))
                print(get_text("text_0135"))

            elif cmd == "give food" and forgotten_archive.gnome_met >= 2:
                if "some food" in have_list:
                    have_list.remove("some food")
                    print(get_text("text_0136"))
                    print(get_text("text_0137"))
                    print(get_text("text_0138"))
                    print(get_text("text_0139"))
                    forgotten_archive.free_hint = True
                else:
                    print(get_text("text_0140"))

            elif cmd == "leave" or cmd == "back":
                print(get_text("text_0141"))
                current_room = "balance_hall_clear"

            else:
                print(get_text("text_0142"))
        elif current_room == "mirror_hall":
            if cmd == "look":
                print(get_text("text_0143"))
                print(get_text("text_0144"))
                print(f"Mirror angles (0 = forward, 1 = right, -1 = left): {mirror_angles}")
                print(get_text("text_0145"))
                print(get_text("text_0146"))

            elif cmd.startswith("turn mirror"):
                parts = cmd.split()
                if len(parts) < 3:
                    print(get_text("text_0147"))
                    continue
                try:
                    mirror_idx = int(parts[1][-1]) - 1
                    direction = parts[2]
                    if mirror_idx < 0 or mirror_idx > 2:
                        print(get_text("text_0148"))
                        continue
                    if direction == "left":
                        mirror_angles[mirror_idx] -= 1
                    elif direction == "right":
                        mirror_angles[mirror_idx] += 1
                    else:
                        print(get_text("text_0149"))
                        continue
                    print(f"Mirror {mirror_idx+1} rotated.")
                except:
                    print(get_text("text_0150"))

            elif cmd == "beam":
                correct = [1, -1, 1]
                if mirror_angles == correct:
                    print(get_text("text_0151"))
                    print(get_text("text_0152"))
                    current_room = "balance_hall"
                else:
                    mistake_streak += 1
                    damage = 1 if mistake_streak < 3 else 2
                    hp -= damage
                    jump_scare_face('flash')
                    print(f"Beam hits a wall and bounces back, burning you. HP -{damage}")
                    if hp <= 0:
                        print(get_text("text_0153"))
                        game_over = True
                        game_back = True
                        break

            else:
                print(get_text("text_0154"))

        elif current_room == "balance_hall":
            if cmd == "look":
                print(get_text("text_0155"))
                print(get_text("text_0156"))
                print(get_text("text_0157"))
                print(get_text("text_0158"))
                print(get_text("text_0159"))

            elif cmd == "clear":
                print(get_text("text_0160"))
                if not hasattr(forgotten_archive, 'plate_items'):
                    forgotten_archive.plate_items = []
                forgotten_archive.plate_items.clear()
            elif cmd == 'bag':
                for i in range(len(have_list)):
                    print(have_list[i])
            elif cmd.startswith("place "):
                item_name = cmd[6:].strip()
                if item_name not in have_list:
                    print(get_text("text_0161"))
                    continue
                if not hasattr(forgotten_archive, 'plate_items'):
                    forgotten_archive.plate_items = []
                if item_name in forgotten_archive.plate_items:
                    print(get_text("text_0162"))
                    continue
                forgotten_archive.plate_items.append(item_name)
                print(f"You place {item_name} on the plate.")

            elif cmd == "weigh":
                if not hasattr(forgotten_archive, 'plate_items'):
                    forgotten_archive.plate_items = []
                total = 0
                for item in forgotten_archive.plate_items:
                    total += item_weights.get(item, 0)
                if total == balance_target:
                    print(get_text("text_0163"))
                    print(get_text("text_0164"))
                    print(get_text("text_0165"))
                    current_room = "balance_hall_clear"
                else:
                    mistake_streak += 1
                    print(f"Right side weighs {total}. Not balanced.")
                    if mistake_streak >= 3:
                        hp -= 2
                        print(get_text("text_0166"))
                        if hp <= 0:
                            print(get_text("text_0167"))
                            game_over = True
                            game_back = True
                            break

            else:
                print(get_text("text_0168"))
        elif current_room == "balance_hall_clear":
            if cmd == "forward":
                current_room = "core_room"
            elif cmd == "workshop":
                if gnome_hole_in == False:
                    print(get_text("text_0169"))
                    current_room = "gnome_workshop"
                else:
                    print(get_text("text_0170"))
            elif cmd == "back":
                current_room = "balance_hall"
            else:
                print(get_text("text_0171"))
        elif current_room == "core_room":
            if cmd == "look":
                print(get_text("text_0172"))
                print(get_text("text_0173"))
                print(get_text("text_0174"))
                print(get_text("text_0175"))
                print(get_text("text_0176"))

            elif cmd == "pray":
                faith_cost = 5
                if faith >= faith_cost:
                    faith -= faith_cost
                    print(get_text("text_0177"))
                    print(get_text("text_0178"))
                else:
                    print(get_text("text_0179"))

            elif cmd.startswith("enter "):
                code = cmd.split()[1] if len(cmd.split()) > 1 else ""
                if code == final_code:
                    print(get_text("text_0180"))
                    print(get_text("text_0181"))
                    print('Hp +99!!!')
                    hp += 99
                    one_hole_in = True
                    gamestart()
                    return
                else:
                    mistake_streak += 1
                    damage = 2 if mistake_streak < 3 else 4
                    hp -= damage
                    print(f"Wrong code. Poison gas fills the room. HP -{damage}")
                    jump_scare_face('flash')
                    if hp <= 0:
                        print(get_text("text_0182"))
                        game_over = True
                        game_back = True
                        break

            else:
                print(get_text("text_0183"))

    if game_over:
        print(get_text("text_0184"))
        print(get_text("text_0185"))
        while True:
            c = input()
            if c == "menu":
                main()
                return

def child_tomb():
    global hp, have_list, good, evil, faith, game_over, game_back, current_room
    global has_death_corpse, death_location, death_corpse_item,child_hole_in
    current_room = "child_tomb"

    print(get_text("text_0186"))
    print(get_text("text_0187"))
    print(get_text("text_0188"))
    print(get_text("text_0189"))
    print(get_text("text_0190"))

    toys_placed = []
    correct_order = ["crayon", "horse", "doll", "coffin"]
    question_stage = 0
    wrong_count = 0

    while True:
        if has_death_corpse and death_location == current_room:
            print(get_text("text_0191"))
        cmd = input("child> ").strip().lower()

        if handle_terminal_cmd(cmd):
            continue

        if cmd == "leave" or cmd == "back":
            print(get_text("text_0192"))
            pendulum_mortuary()
            return

        if cmd == "bag":
            for item in have_list:
                print(item)
            continue
        if cmd == "hp":
            print(f"HP: {hp}")
            continue

        if cmd == "look":
            print(get_text("text_0193"))
            print(get_text("text_0194"))
            print(get_text("text_0195"))
            print(get_text("text_0196"))

        elif cmd.startswith("place "):
            toy = cmd[6:].strip()
            if toy not in ["crayon", "horse", "doll", "coffin"]:
                print(get_text("text_0197"))
                continue
            if toy in toys_placed:
                print(get_text("text_0198"))
                continue
            if toy == correct_order[len(toys_placed)]:
                toys_placed.append(toy)
                print(f"You place the {toy} on the altar. It glows faintly.")
                if len(toys_placed) == 4:
                    print(get_text("text_0199"))
                    print(get_text("text_0200"))
                    question_stage = 1
            else:
                wrong_count += 1
                dmg = 1 if wrong_count < 3 else 3
                hp -= dmg
                print(f"The toy turns cold and burns your hand. HP -{dmg}")
                toys_placed.clear()
                print(get_text("text_0201"))
                if hp <= 0:
                    print(get_text("text_0202"))
                    game_over = True
                    game_back = True
                    break

        elif cmd == "reset":
            toys_placed.clear()
            print(get_text("text_0203"))

        elif question_stage == 1:
            if cmd == "yes":
                print(get_text("text_0204"))
                question_stage = 2
            elif cmd == "no":
                print(get_text("text_0205"))
                print(get_text("text_0206"))
                hp -= 3
                print(get_text("text_0207"))
                if hp <= 0:
                    print(get_text("text_0208"))
                    game_over = True
                    game_back = True
                    break
            else:
                print(get_text("text_0209"))

        elif question_stage == 2:
            if cmd == "stay" or cmd == "yes":
                print(get_text("text_0210"))
                print(get_text("text_0211"))
                print(get_text("text_0212"))
                print(get_text("text_0213"))
                game_over = True
                game_back = True
                break
            elif cmd == "no" or cmd == "i cant":
                print(get_text("text_0214"))
                print(get_text("text_0215"))
                question_stage = 3
            else:
                print(get_text("text_0216"))

        elif question_stage == 3:
            if cmd == "wizard" or cmd == "the wizard" or cmd == "your father":
                print(get_text("text_0217"))
                print(get_text("text_0218"))
                print(get_text("text_0219"))
                print(get_text("text_0220"))
                print(get_text("text_0221"))
                have_list.append("child rune shard")
                faith += 15
                good += 20
                hp += 10
                print("You got CHILD RUNE SHARD. Faith +15, Good +20, HP +10")
                print(get_text("text_0222"))
                question_stage = 4
            else:
                print(get_text("text_0223"))
                hp -= 1
                print(get_text("text_0224"))

        elif question_stage == 4 and cmd == "leave":
            print(get_text("text_0225"))
            child_hole_in = True
            pendulum_mortuary()
            return

        elif cmd == "attack boy" or cmd == "kill boy":
            print(get_text("text_0226"))
            print(get_text("text_0227"))
            hp -= 10
            evil += 30
            print("HP -10 | Evil +30")
            if hp <= 0:
                print(get_text("text_0228"))
                game_over = True
                game_back = True
                break
            print(get_text("text_0229"))
            child_hole_in = True
            pendulum_mortuary()
            return

        elif cmd == "corpse" or cmd == "search corpse":
            if has_death_corpse and death_location == current_room:
                print(get_text("text_0230"))
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print(get_text("text_0231"))
                has_death_corpse = False
            else:
                print(get_text("text_0232"))

        else:
            print(get_text("text_0233"))

    if game_over:
        print(get_text("text_0234"))
        print(get_text("text_0235"))
        while True:
            c = input()
            if c == "menu":
                main()
                return

def handle_terminal_cmd(cmd):
    global game_back,game_over,hp
    
    cmd = cmd.strip().lower()
    if cmd in ["ls", "dir"]:
        print(get_text("text_0236"))
        print(get_text("text_0237"))
        print(get_text("text_0238"))
        print(get_text("text_0239"))
        print(get_text("text_0240"))
        return True
    elif cmd == "ls -la" or cmd == "dir /a":
        print(get_text("text_0241"))
        print(get_text("text_0242"))
        print(get_text("text_0243"))
        print(get_text("text_0244"))
        return True
    elif cmd.startswith("cd "):
        path = cmd[3:].strip()
        if path == "..":
            print(get_text("text_0245"))
        elif path == "/":
            print(get_text("text_0246"))
        elif path == "~":
            print(get_text("text_0247"))
        else:
            print(f"No such directory: {path}")
        return True
    elif cmd == "pwd":
        print(get_text("text_0248"))
        return True
    elif cmd.startswith("mkdir "):
        name = cmd[6:].strip()
        print(f"Directory '{name}' created. Filled with dust instantly.")
        return True
    elif cmd == "rm -rf /" or cmd == "rm -rf /*":
        print(get_text("text_0249"))
        for _ in range(30):
            print(get_text("text_0250"))
            time.sleep(0.01)
        print(get_text("text_0251"))
        time.sleep(1.5)
        print(get_text("text_0252"))
        time.sleep(2)
        hp -= 3
        if hp == 0:
            print(get_text("text_0253"))
            game_over = True
            game_back = True
        else:
            print(get_text("text_0254"))
            print(get_text("text_0255"))
        return True
    elif cmd.startswith("rm "):
        print(get_text("text_0256"))
        return True
    elif cmd.startswith("sudo "):
        print(get_text("text_0257"))
        return True
    elif cmd == "sudo su" or cmd == "su":
        print(get_text("text_0258"))
        return True
    elif cmd.startswith("cat "):
        file = cmd[4:].strip()
        if file == "diary":
            print(get_text("text_0259"))
        elif file == "wall":
            print(get_text("text_0260"))
        else:
            print(f"No such file: {file}")
        return True
    elif cmd.startswith("echo "):
        text = cmd[5:].strip()
        print(f"A whisper echoes back: {text}")
        return True
    elif cmd in ["clear", "cls"]:
        print("\n" * 50)
        print(get_text("text_0261"))
        return True
    elif cmd in ["exit", "quit"]:
        print(get_text("text_0262"))
        return True
    elif cmd == "whoami":
        print(get_text("text_0263"))
        return True
    elif cmd.startswith("touch "):
        name = cmd[6:].strip()
        print(f"You touched {name}. It is cold and dusty.")
        return True
    elif cmd.startswith("chmod "):
        print(get_text("text_0264"))
        return True
    elif cmd.startswith("ping "):
        target = cmd[5:].strip()
        print(f"Pinging {target}...")
        print(get_text("text_0265"))
        print(get_text("text_0266"))
        return True
    elif cmd in ["reboot", "shutdown -r now"]:
        print(get_text("text_0267"))
        return True
    elif cmd in ["shutdown", "shutdown now", "halt"]:
        print(get_text("text_0268"))
        return True
    elif cmd == "ps" or cmd == "ps aux":
        print(get_text("text_0269"))
        print(get_text("text_0270"))
        print(get_text("text_0271"))
        print(get_text("text_0272"))
        return True
    elif cmd.startswith("kill "):
        print(get_text("text_0273"))
        return True
    elif cmd == "kill -9 1":
        print(get_text("text_0274"))
        return True
    elif cmd == "top":
        print(get_text("text_0275"))
        print(get_text("text_0276"))
        return True
    elif cmd.startswith("man "):
        topic = cmd[4:].strip()
        print(f"No manual for {topic}. Figure it out yourself.")
        return True
    elif cmd == "help":
        print(get_text("text_0277"))
        return True
    elif cmd in ["vim", "vi", "nano", "emacs"]:
        print(get_text("text_0278"))
        return True
    elif cmd == "python" or cmd == "python3":
        print(get_text("text_0279"))
        print(get_text("text_0280"))
        print(get_text("text_0281"))
        return True
    elif cmd.startswith("pip "):
        print(get_text("text_0282"))
        return True
    elif cmd in ["ifconfig", "ipconfig"]:
        print(get_text("text_0283"))
        print(get_text("text_0284"))
        return True
    elif cmd == "ipconfig /flushdns":
        print(get_text("text_0285"))
        return True
    elif cmd.startswith("curl ") or cmd.startswith("wget "):
        print(get_text("text_0286"))
        return True
    elif cmd == "date":
        print(get_text("text_0287"))
        return True
    elif cmd == "cal":
        print(get_text("text_0288"))
        return True
    elif cmd == "df -h":
        print(get_text("text_0289"))
        print(get_text("text_0290"))
        print(get_text("text_0291"))
        return True
    elif cmd == "find .":
        print(get_text("text_0292"))
        print(get_text("text_0293"))
        print(get_text("text_0294"))
        return True
    elif cmd == "grep":
        print(get_text("text_0295"))
        return True
    elif cmd == "tar":
        print(get_text("text_0296"))
        return True
    elif cmd in ["tree", "tree /f"]:
        print(get_text("text_0297"))
        print(get_text("text_0298"))
        print(get_text("text_0299"))
        print(get_text("text_0300"))
        return True
    elif cmd == "tasklist":
        print(get_text("text_0301"))
        print(get_text("text_0302"))
        print(get_text("text_0303"))
        print(get_text("text_0304"))
        return True
    elif cmd.startswith("taskkill"):
        print(get_text("text_0305"))
        return True
    elif cmd == "tracert":
        print(get_text("text_0306"))
        print(get_text("text_0307"))
        print(get_text("text_0308"))
        print(get_text("text_0309"))
        return True
    else:
        return False
    
def full_moon_maze():
    global hp, have_list, good, evil, faith, game_over, game_back, festival_mode
    global two_hole_in
    global current_room,has_death_corpse,death_corpse_item,death_location

    current_room = 'maze'
    if not festival_mode:
        print(get_text("text_0310"))
        return

    print(get_text("text_0311"))
    print(get_text("text_0312"))
    print(get_text("text_0313"))
    print(get_text("text_0314"))

    room = "shadow_hall"
    mistake = 0
    phase_progress = 0
    correct_phases = ["new", "waxing", "full", "waning", "crescent"]
    moon_code = "532"

    if has_death_corpse and death_location == current_room:
        print(get_text("text_0315"))
    while True:
        cmd = input("moon> ").strip().lower()

        if cmd == "leave" or cmd == "back":
            print(get_text("text_0316"))
            gamestart()
            return

        elif cmd == "bag":
            for item in have_list:
                print(item)
            continue
        elif cmd == "hp":
            print(f"HP: {hp}")
            continue
        if has_death_corpse and death_location == current_room:
            print(get_text("text_0317"))
        elif room == "shadow_hall":
            if cmd == "look":
                print(get_text("text_0318"))
                print(get_text("text_0319"))
                print(get_text("text_0320"))
                print(get_text("text_0321"))
                print(get_text("text_0322"))

            elif cmd.startswith("step "):
                target = cmd.split()[1] if len(cmd.split()) > 1 else ""
                order = ["wolf", "maiden", "tree"]
                if target == order[phase_progress]:
                    phase_progress += 1
                    print(f"Shadow of {target} glows softly.")
                    mistake = 0
                    if phase_progress == 3:
                        print(get_text("text_0323"))
                        room = "phase_chamber"
                        phase_progress = 0
                else:
                    mistake += 1
                    dmg = 1 if mistake < 3 else 3
                    hp -= dmg
                    print(f"Wrong shadow. Moonlight burns you. HP -{dmg}")
                    phase_progress = 0
                    if hp <= 0:
                        print(get_text("text_0324"))
                        game_over = True
                        game_back = True
                        break
            else:
                print(get_text("text_0325"))

        elif room == "phase_chamber":
            if cmd == "look":
                print(get_text("text_0326"))
                print(get_text("text_0327"))
                print(get_text("text_0328"))

            elif cmd.startswith("press "):
                phase = cmd.split()[1] if len(cmd.split()) > 1 else ""
                if phase == correct_phases[phase_progress]:
                    phase_progress += 1
                    print(f"{phase} plate lights up.")
                    mistake = 0
                    if phase_progress == 5:
                        print(get_text("text_0329"))
                        room = "moon_core"
                        phase_progress = 0
                else:
                    mistake += 1
                    dmg = 1 if mistake < 3 else 2
                    hp -= dmg
                    print(f"Wrong phase. Energy shocks you. HP -{dmg}")
                    phase_progress = 0
                    if hp <= 0:
                        print(get_text("text_0330"))
                        game_over = True
                        game_back = True
                        break
            else:
                print(get_text("text_0331"))

        elif room == "moon_core":
            if cmd == "look":
                print(get_text("text_0332"))
                print(get_text("text_0333"))
                print(get_text("text_0334"))
                print(get_text("text_0335"))

            elif cmd == "pray":
                if faith >= 3:
                    faith -= 3
                    print(get_text("text_0336"))
                else:
                    print(get_text("text_0337"))

            elif cmd.startswith("enter "):
                code = cmd.split()[1] if len(cmd.split()) > 1 else ""
                if code == moon_code:
                    print(get_text("text_0338"))
                    print(get_text("text_0339"))
                    print(get_text("text_0340"))
                    good += 10
                    evil -= 5
                    hp += 20
                    two_hole_in = True
                    gamestart()  
                    return
                else:
                    mistake += 1
                    dmg = 2 if mistake < 3 else 4
                    hp -= dmg
                    print(f"Wrong code. Cold frost spreads. HP -{dmg}")
                    jump_scare_face('flash')
                    if hp <= 0:
                        print(get_text("text_0341"))
                        game_over = True
                        game_back = True
                        break
            else:
                print(get_text("text_0342"))

    if game_over:
        print(get_text("text_0343"))
        print(get_text("text_0344"))
        while True:
            c = input()
            if c == "menu":
                main()
                return

def wax_chamber():
    global hp, have_list, good, evil, faith, game_over, game_back,three_hole_in
    global current_room,has_death_corpse,death_corpse_item,death_location

    jump_scare_face('flash')
    current_room = 'chamber'
    print(get_text("text_0345"))
    print(get_text("text_0346"))
    print(get_text("text_0347"))
    print(get_text("text_0348"))
    print(get_text("text_0349"))
    print(get_text("text_0350"))

    correct = 4
    tried = 0
    details = {
        1: "Clean hands, no wound. Robe has no rune mark. Feet are intact.",
        2: "Chest has a stab wound. No ring on finger. Rune mark on left arm.",
        3: "Wax drips from the chin. Clearly fake. Eyes are glass.",
        4: "Bronze ring on right hand. Rune scar on chest. Left ankle broken.",
        5: "Modern clothes. Definitely not ancient. Smells like dust.",
        6: "Perfect face, no flaw. Too smooth to be real human.",
        7: "Hands folded. No ring. Rune mark is carved, not scarred."
    }
    if has_death_corpse and death_location == current_room:
        print(get_text("text_0351"))
    while True:
        cmd = input("wax> ").strip().lower()

        if cmd == "leave" or cmd == "back":
            print(get_text("text_0352"))
            tomb()
            return

        elif cmd == "bag":
            for item in have_list:
                print(item)
            continue
        elif cmd == "hp":
            print(f"HP: {hp}")
            continue

        elif cmd.startswith("examine "):
            try:
                num = int(cmd.split()[1])
                if 1 <= num <= 7:
                    print(f"Figure {num}: {details[num]}")
                else:
                    print(get_text("text_0353"))
            except:
                print(get_text("text_0354"))
        elif cmd == "examine corpse" or cmd == 'corpse' or cmd == 'search corpse' or cmd == 'find corpse':
            if has_death_corpse and death_location == current_room:
                print(get_text("text_0355"))
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print(get_text("text_0356"))
                has_death_corpse = False
            else:
                print(get_text("text_0357"))
        elif cmd.startswith("choose "):
            try:
                num = int(cmd.split()[1])
                if num == correct:
                    print(get_text("text_0358"))
                    print(get_text("text_0359"))
                    print(get_text("text_0360"))
                    print(get_text("text_0361"))
                    print(get_text("text_0362"))
                    hp += 10
                    faith = 100
                    good += 10
                    evil = 0
                    three_hole_in = True
                    tomb()
                    return
                else:
                    tried += 1
                    dmg = 2 if tried < 3 else 10
                    hp -= dmg
                    print(f"The wax figure lurches at you! HP -{dmg}")
                    print(get_text("text_0363"))
                    jump_scare_face()
                    if hp <= 0:
                        print(get_text("text_0364"))
                        print(get_text("text_0365"))
                        print(get_text("text_0366"))
                        print(get_text("text_0367"))
                        print(get_text("text_0368"))
                        print(get_text("text_0369"))
                        print(get_text("text_0370"))
                        exit()
            except:
                print(get_text("text_0371"))
        else:
            print(get_text("text_0372"))


def pendulum_mortuary():
    global hp, have_list, good, evil, faith, game_over, game_back,four_hole_in
    global current_room,has_death_corpse,death_corpse_item,death_location


    jump_scare_face('flash')
    current_room = 'mortuary'
    if has_death_corpse and death_location == current_room:
        print(get_text("text_0373"))
    print(get_text("text_0374"))
    print(get_text("text_0375"))
    print(get_text("text_0376"))
    print(get_text("text_0377"))
    print(get_text("text_0378"))
    print(get_text("text_0379"))
    print(get_text("text_0380"))
    print(get_text("text_0381"))
    correct = 4
    tried = 0
    swing_count = 0
    coffin_details = {
        1: "Rotted cloth. Sword wound on chest. Death in battle.",
        2: "Smooth wood. No wound. Hands folded in peace.",
        3: "Iron nails on lid. Scratches from inside.",
        4: "Bronze ring carved on lid. Rune marks around edges.",
        5: "Broken lid. Bones scattered by animals.",
        6: "Child-sized. Small handprint on the side."
    }

    while True:
        cmd = input("mortuary> ").strip().lower()
        if cmd == "leave" or cmd == "back":
            print(get_text("text_0382"))
            misty_swamp()
            return

        elif cmd == "bag":
            for item in have_list:
                print(item)
            continue
        elif cmd == "hp":
            print(f"HP: {hp}")
            continue

        elif cmd == "listen pendulum" or cmd == "pendulum":
            swing_count += 1
            print(get_text("text_0383"))
            print(f"You count {swing_count} swings so far.")
            if swing_count >= 3:
                print(get_text("text_0384"))
        elif cmd == "open" or cmd == "child coffin" or cmd == 'down':
            if child_hole_in == False:
                print(get_text("text_0385"))
                child_tomb()
                return
            else:
                print(get_text("text_0386"))
        elif cmd.startswith("examine "):
            try:
                num = int(cmd.split()[1])
                if 1 <= num <= 6:
                    print(f"Coffin {num}: {coffin_details[num]}")
                    if num == correct and tried >= 2:
                        print(get_text("text_0387"))
                    else:
                        print(get_text("text_0388"))
                else:
                    print(get_text("text_0389"))
            except:
                print(get_text("text_0390"))

        elif cmd == "pray":
            if faith >= 5:
                faith -= 5
                print(get_text("text_0391"))
            else:
                print(get_text("text_0392"))
        elif cmd == "examine corpse" or cmd == 'corpse' or cmd == 'search corpse' or cmd == 'find corpse':
            if has_death_corpse and death_location == current_room:
                print(get_text("text_0393"))
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print(get_text("text_0394"))
                has_death_corpse = False
            else:
                print(get_text("text_0395"))
        elif cmd.startswith("open "):
            try:
                num = int(cmd.split()[1])
                if num == correct:
                    jump_scare_face('flash')
                    print(get_text("text_0396"))
                    print(get_text("text_0397"))
                    print(get_text("text_0398"))
                    print(get_text("text_0399"))
                    print(get_text("text_0400"))
                    print(get_text("text_0401"))
                    hp += 10
                    faith += 10
                    good += 10
                    current_room = "dwarf_chamber"
                    continue
                        
                else:
                    tried += 1
                    dmg = 2 if tried < 3 else 8
                    hp -= dmg
                    print(f"Dead hands reach out and scratch you! HP -{dmg}")
                    print(get_text("text_0402"))
                    jump_scare_face()
                    if hp <= 0:
                        print(get_text("text_0403"))
                        print(get_text("text_0404"))
                        print(get_text("text_0405"))
                        print(get_text("text_0406"))
                        print(get_text("text_0407"))
                        print(get_text("text_0408"))
                        print(get_text("text_0409"))
                        exit()
            except:
                print(get_text("text_0410"))
        elif current_room == "dwarf_chamber":
            if cmd == "look":
                print(get_text("text_0411"))
                print(get_text("text_0412"))
                print(get_text("text_0413"))
                print(get_text("text_0414"))
            elif cmd == "talk to dwarf" or cmd == "speak gimble" or cmd == 'talk':
                if not hasattr(pendulum_mortuary, 'dwarf_talked'):
                    print(get_text("text_0415"))
                    print(get_text("text_0416"))
                    print(get_text("text_0417"))
                    print(get_text("text_0418"))
                    pendulum_mortuary.dwarf_talked = True
                else:
                    print(get_text("text_0419"))

            elif cmd == "show toolkit" or cmd == "give toolkit":
                if "gnome master toolkit" in have_list and hasattr(pendulum_mortuary, 'dwarf_talked') and pendulum_mortuary.dwarf_talked:
                    print(get_text("text_0420"))
                    print(get_text("text_0421"))
                    print(get_text("text_0422"))
                    print(get_text("text_0423"))
                    print(get_text("text_0424"))
                    print(get_text("text_0425"))
                    current_room = "dwarf_chamber_clear"
                else:
                    print(get_text("text_0426"))

            elif cmd == "purify dwarf" or cmd == "use holy amulet":
                if "holy amulet" in have_list and good >= 30 and hasattr(pendulum_mortuary, 'dwarf_talked') and pendulum_mortuary.dwarf_talked:
                    print(get_text("text_0427"))
                    print(get_text("text_0428"))
                    print(get_text("text_0429"))
                    print(get_text("text_0430"))
                    print(get_text("text_0431"))
                    print(get_text("text_0432"))
                    print(get_text("text_0433"))
                    have_list.append("rune-forged hammer")
                    if evil >= 10:
                        evil = 0
                    else:
                        good += 25
                    faith += 20
                    four_hole_in = True
                    current_room = "dwarf_chamber_clear"
                    misty_swamp()
                    return
                else:
                    print(get_text("text_0434"))

            elif cmd == "attack dwarf" or cmd == "fight gimble":
                print(get_text("text_0435"))
                dwarf_hp = 8
                while dwarf_hp > 0 and hp > 0:
                    print(f"\nDwarf HP: {dwarf_hp} | Your HP: {hp}")
                    action = input("strike / defend / run: ").strip().lower()
                    if action == "strike":
                        if "ghost sword" in have_list or "rune-forged hammer" in have_list:
                            dwarf_hp -= 2
                            print(get_text("text_0436"))
                        else:
                            dwarf_hp -= 1
                            print(get_text("text_0437"))
                        if dwarf_hp > 0:
                            hp -= 2
                            print(get_text("text_0438"))
                    elif action == "defend":
                        hp -= 1
                        print(get_text("text_0439"))
                    elif action == "run":
                        print(get_text("text_0440"))
                        current_room = "mortuary"
                        break
                    else:
                        print(get_text("text_0441"))
                if dwarf_hp <= 0:
                    print(get_text("text_0442"))
                    print(get_text("text_0443"))
                    print(get_text("text_0444"))
                    have_list.append("corrupted warhammer")
                    evil += 30
                    four_hole_in = True
                    misty_swamp()
                    return
                elif hp <= 0:
                    print(get_text("text_0445"))
                    game_over = True
                    game_back = True
            else:
                print(get_text("text_0446"))
        else:
            print(get_text("text_0447"))

    if game_over:
        print(get_text("text_0448"))
        print(get_text("text_0449"))
        while True:
            c = input()
            if c == "menu":
                main()
                return

# tomb
def tomb():
    global game_over, hp, have_list, play_count, tomb_unlocked, game_back,cleared_ending
    global one_hole_in,two_hole_in,three_hole_in
    jump_scare_face('flash')
    print("\n=== FORGOTTEN TOMB (NG+ ONLY) ===")
    print(get_text("text_0450"))
    print(get_text("text_0451"))
    print(get_text("text_0452"))
    print(get_text("text_0453"))
    print(get_text("text_0454"))
    print(get_text("text_0455"))
    if play_count == 2:
        print(get_text("text_0456"))
    tomb_unlocked = True

    while True:
        cmd = input(get_text("input_0457"))
        if handle_terminal_cmd(cmd):
            continue
        if cmd == "look" or cmd == 'look around':
            print(get_text("text_0458"))
            print(get_text("text_0459"))
            print(get_text("text_0460"))
            print(get_text("text_0461"))
            print(get_text("text_0462"))
            print(get_text("text_0463"))
        elif cmd == 'read diary' or cmd == 'diary' or cmd == 'take diary':
            print(get_text("text_0464"))
            print(get_text("text_0465"))
            print(get_text("text_0466"))
            print(get_text("text_0467"))
            print(get_text("text_0468"))
            print(get_text("text_0469"))
        elif cmd == 'down' or cmd == 'go down':
            if three_hole_in == False:
                wax_chamber()
            else:
                print(get_text("text_0470"))
        elif cmd == "challenge guardian":
            if play_count == 2:
                print(get_text("text_0471"))
                guard_hp = 5
                while guard_hp > 0 and hp > 0:
                    print(f"Guardian HP: {guard_hp} | Your HP: {hp}")
                    fight = input(get_text("input_0472"))
                    if fight == "strike":
                        guard_hp -= 1
                        print(get_text("text_0473"))
                        if guard_hp > 0:
                            hp -= 1
                            print(get_text("text_0474"))
                    elif fight == "defend":
                        print(get_text("text_0475"))
                if guard_hp <= 0:
                    print(get_text("text_0476"))
                    have_list.append("guardian shield")
                else:
                    print(get_text("text_0477"))
                    hp = 5
            else:
                print(get_text("text_0478"))
        elif cmd == "trial":
            if play_count == 2:
                print(get_text("text_0479"))
                print(get_text("text_0480"))
                print(get_text("text_0481"))
                trial_choice = input()
                if trial_choice == "choose inherit":
                    print(get_text("text_0482"))
                    print(get_text("text_0483"))
                    hp = 90
                    print(get_text("text_0484"))
                elif trial_choice == "choose refuse":
                    print(get_text("text_0485"))
                    print(get_text("text_0486"))
                    print(get_text("text_0487"))
                elif trial_choice == "choose listen":
                    print(get_text("text_0488"))
                    print(get_text("text_0489"))
                    print(get_text("text_0490"))
                else:
                    print(get_text("text_0491"))
            else:
                print(get_text("text_0492"))
        elif cmd == "sing":
            print(get_text("text_0493"))
            print(get_text("text_0494"))
            hp += 1
        elif cmd == "eat candy":
            if "silly candy" in have_list:
                print(get_text("text_0495"))
            else:
                print(get_text("text_0496"))
        elif cmd == "pretend ghost":
            print(get_text("text_0497"))
        elif cmd == "tickling guardian":
            print(get_text("text_0498"))
        elif cmd == "offer snack":
            print(get_text("text_0499"))
        elif cmd == "ask ghost why here":
            print(get_text("text_0500"))
            print(get_text("text_0501"))
        elif cmd == "ghost wifi":
            print(get_text("text_0502"))
            print(get_text("text_0503"))
        elif cmd == "ghost joke":
            print(get_text("text_0504"))
            print(get_text("text_0505"))
        elif cmd == "ghost favorite dessert":
            print(get_text("text_0506"))
            print(get_text("text_0507"))
        elif cmd == "ghost elevator":
            print(get_text("text_0508"))
            print(get_text("text_0509"))
        elif cmd == "ghost social media":
            print(get_text("text_0510"))
            print(get_text("text_0511"))
        elif cmd == "ghost party":
            print(get_text("text_0512"))
            print(get_text("text_0513"))
        elif cmd == "ghost math":
            print(get_text("text_0514"))
            print(get_text("text_0515"))
        elif cmd == "ghost love":
            print(get_text("text_0516"))
            print(get_text("text_0517"))
        elif cmd == "ghost homework":
            print(get_text("text_0518"))
            print(get_text("text_0519"))
        elif cmd == "guardian joke":
            print(get_text("text_0520"))
            print(get_text("text_0521"))
        elif cmd == "do robot" or cmd == 'robot':
            print(get_text("text_0522"))
        elif cmd == "race ghost" or cmd == 'race':
            print(get_text("text_0523"))
        elif cmd == "beg":
            print(get_text("text_0524"))
        elif cmd == "greet":
            print(get_text("text_0525"))
        elif cmd == "tease guardian":
            print(get_text("text_0526"))
        elif cmd == "play hide and seek":
            print(get_text("text_0527"))
        elif cmd == "march":
            print(get_text("text_0528"))
        elif cmd == "blow whistle" or cmd == 'whistle':
            print(get_text("text_0529"))
        elif cmd == "bow":
            print(get_text("text_0530"))
        elif cmd == "yawn":
            print(get_text("text_0531"))
        elif cmd == 'kiss':
            print(get_text("text_0532"))
        elif cmd == "whistle":
            print(get_text("text_0533"))
        elif cmd == "wave":
            print(get_text("text_0534"))
        elif cmd == "dance":
            print(get_text("text_0535"))
            have_list.append("silly candy")
            print(get_text("text_0536"))
        elif cmd == "make noise":
            print(get_text("text_0537"))
        elif cmd == "altar":
            print(get_text("text_0538"))
            print(get_text("text_0539"))
            if "family locket" not in have_list:
                print(get_text("text_0540"))
                have_list.append("family locket")
            if "final diary" not in have_list:
                print(get_text("text_0541"))
                print(get_text("text_0542"))
                print(get_text("text_0543"))
                print(get_text("text_0544"))
                have_list.append("final diary")
        elif cmd == "pray":
            print(get_text("text_0545"))
            print(get_text("text_0546"))
            print(get_text("text_0547"))
            hp += 5
            print("HP +5!")
            print(get_text("text_0548"))
        elif cmd == "open coffin":
            print(get_text("text_0549"))
            print(get_text("text_0550"))
            if "broken amulet" not in have_list:
                have_list.append("broken amulet")
                print(get_text("text_0551"))
            if 'a magic key' not in have_list:
                have_list.append('a magic key')
                print(get_text("text_0552"))
        elif cmd == "leave" or cmd == "back":
            print(get_text("text_0553"))
            gamestart()
        elif cmd == "bag":
            for item in have_list:
                print(item)
        elif cmd == "burp":
            print(get_text("text_0554"))
        elif cmd == "sing baby shark":
            print(get_text("text_0555"))
        elif cmd == "hide":
            print(get_text("text_0556"))
        elif cmd == "blow kiss":
            print(get_text("text_0557"))
        elif cmd == "nap":
            print(get_text("text_0558"))
        elif cmd == "truth":
            print(get_text("text_0559"))
            print(get_text("text_0560"))
            print(get_text("text_0561"))
            print(get_text("text_0562"))
            game_over = True
            game_back = True
            break
        elif cmd == "tiktok":
            print(get_text("text_0563"))
            print(get_text("text_0564"))
        elif cmd == "snore":
            print(get_text("text_0565"))
            print(get_text("text_0566"))
        else:
            print(get_text("text_0567"))

    if game_over:
        print(get_text("text_0568"))
        print(get_text("text_0569"))
        while True:
            c = input()
            if c == "menu":
                menu()
                return

# misty swamp
def misty_swamp():
    global game_over, hp, have_list, time_period, good, evil, rune2, game_back, swamp_quest, swamp_visited, lily_count,cleared_ending,swamp_spirit_story,misty_end,has_death_corpse,death_corpse_item,death_location,four_hole_in

    print(get_text("text_0570"))
    print(get_text("text_0571"))
    print(get_text("text_0572"))
    if time_period == "night":
        print(get_text("text_0573"))

    if "a swamp herb" not in have_list:
        print(get_text("text_0574"))
        print(get_text("text_0575"))
        print(get_text("text_0576"))
        have_list.append("a swamp herb")

    swamp_visited = True
    swamp_quest = False
    lily_count = 0

    while True:
        print(get_text("text_0577"))
        if has_death_corpse and death_location == current_room:
            print(get_text("text_0578"))
        scmd = input(get_text("input_0579"))
        if handle_terminal_cmd(scmd):
            continue
        if scmd == "west" or scmd == "back" or scmd == "leave":
            print(get_text("text_0580"))
            return
        elif scmd == 'down':
            if four_hole_in == False:
                pendulum_mortuary()
            else:
                print(get_text("text_0581"))
        elif scmd == "look":
            print(get_text("text_0582"))
        elif scmd == "hp":
            print(f"HP: {hp}")
        elif scmd == "bag":
            for item in have_list:
                print(item)
        elif scmd == "moral":
            print(f"Good: {good} | Evil: {evil}")
        elif scmd == "quest":
            swamp_quest = True
            print(get_text("text_0583"))
            print(get_text("text_0584"))
            print(get_text("text_0585"))
            print(get_text("text_0586"))
        elif scmd == "find lily" and swamp_quest:
            rnd = random.randint(1,6)
            if rnd <= 3:
                lily_count += 1
                print(get_text("text_0587"))
            elif rnd == 4:
                lily_count += 1
                have_list.append("dewdrop")
                print(get_text("text_0588"))
                print(get_text("text_0589"))
                print(get_text("text_0590"))
            elif rnd == 5:
                lily_count += 1
                good += 5
                print(get_text("text_0591"))
            else:
                print(get_text("text_0592"))
        elif scmd == "use dewdrop" and "dewdrop" in have_list:
            hp += 8
            good += 6
            have_list.remove("dewdrop")
            print(get_text("text_0593"))
        elif scmd == "turn in" and swamp_quest and lily_count >= 3:
            have_list.append("swamp pendant")
            good += 15
            print(get_text("text_0594"))
            print(get_text("text_0595"))
            print(get_text("text_0596"))
            print(get_text("text_0597"))
            lily_count = 0
            swamp_quest = False
        elif scmd == "progress" and swamp_quest:
            print(f"Lily collected: {lily_count} / 3. Keep going!")
        elif scmd == "tips":
            print(get_text("text_0598"))

        elif scmd == "swamp ending" and "swamp pendant" in have_list and good >= 20:
            print(get_text("text_0599"))
            print(get_text("text_0600"))
            print(get_text("text_0601"))
            print(get_text("text_0602"))
            have_list.append('a magic key')
            hp += 20
            print('HP +20')
            if play_count == 2:
                print(get_text("text_0603"))
            misty_end = True
            gamestart()
            return

        elif scmd == "peace leave" and "swamp pendant" in have_list:
            print(get_text("text_0604"))
            print(get_text("text_0605"))
            print('HP +5')
            hp += 5
            good += 5
            misty_end = True
            gamestart()
        elif scmd == "examine corpse" or scmd == 'corpse' or scmd == 'search corpse' or scmd == 'find corpse':
            if has_death_corpse and death_location == current_room:
                print(get_text("text_0606"))
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print(get_text("text_0607"))
                has_death_corpse = False
            else:
                print(get_text("text_0608"))
        elif scmd == "drain spirit" and swamp_quest:
            print(get_text("text_0609"))
            print(get_text("text_0610"))
            evil += 25
            hp += 5
            print(get_text("text_0611"))
            misty_end = True
            gamestart

        elif scmd == "search":
            find = random.randint(1, 3)
            if find == 1 or find == 2:
                print(get_text("text_0612"))
                have_list.append("a swamp herb")
            else:
                print(get_text("text_0613"))
        elif scmd == "help soul":
            print(get_text("text_0614"))
            good += 15
            have_list.append("healing potion")
        elif scmd == "steal soul":
            print(get_text("text_0615"))
            evil += 20
            hp += 3
        elif scmd == "use herb" or scmd == "eat herb":
            if "a swamp herb" in have_list:
                hp += 3
                have_list.remove("a swamp herb")
                print("The herb heals your wounds. HP +3")
        elif scmd == "use potion" or scmd == "drink potion":
            if "healing potion" in have_list:
                hp += 5
                have_list.remove("healing potion")
                good += 5
                print("You drink the potion. HP +5")
        elif scmd == "talk" and swamp_quest:
            print(get_text("text_0616"))
            print(get_text("text_0617"))
            print(get_text("text_0618"))
            print(get_text("text_0619"))
            print(get_text("text_0620"))
            good += 10
            hp += 4
            print("Your kindness soothes the spirit. Good +10, HP +4")
            if festival_mode:
                print(get_text("text_0621"))
                print("The spirit shares a wisp of moonlight with you. HP +3")
                hp += 3
        elif scmd == "ask past" and swamp_quest:
            print(get_text("text_0622"))
            print(get_text("text_0623"))
            print(get_text("text_0624"))
            faith += 5
        elif scmd == "ask" and swamp_quest:
            if swamp_spirit_story == 0:
                print(get_text("text_0625"))
                print(get_text("text_0626"))
                print(get_text("text_0627"))
                swamp_spirit_story = 1
            elif swamp_spirit_story == 1:
                print(get_text("text_0628"))
                print(get_text("text_0629"))
                swamp_spirit_story = 2
            elif swamp_spirit_story == 2:
                print(get_text("text_0630"))
                print(get_text("text_0631"))
                good += 10
                faith += 10
                swamp_spirit_story = 3
            else:
                print(get_text("text_0632"))
        else:
            print(get_text("text_0633"))

        toxin = 1
        if time_period == "night":
            toxin = 2
        hp -= toxin
        print(f"Swamp toxins burn you! HP -{toxin}")

        if hp <= 0:
            print(get_text("text_0634"))
            print(get_text("text_0635"))
            jump_scare_face('flash')
            game_over = True
            game_back = True
            break

def developer_room():
    global hp, have_list, good, evil, rune1, rune2, rune3, trap_protect, festival_mode

    print("\n" + "="*60)
    print(get_text("text_0636"))
    print("="*60)
    print(get_text("text_0637"))
    print(get_text("text_0638"))
    print("="*60)

    while True:
        cmd = input(get_text("input_0639"))
        if cmd == "heal":
            hp = 20
            print(get_text("text_0640"))
        elif cmd == "max":
            hp = 999
            good = 999
            evil = 0
            print(get_text("text_0641"))
        elif cmd == "runes":
            rune1 = rune2 = rune3 = True
            have_list.append("rune stone 1")
            have_list.append("rune stone 2")
            have_list.append("rune stone 3")
            print(get_text("text_0642"))
        elif cmd == "godmode":
            trap_protect = True
            festival_mode = True
            hp = 999
            have_list.append("dev amulet")
            have_list.append("infinite torch")
            print(get_text("text_0643"))
        elif cmd == "leave" or cmd == "back":
            print(get_text("text_0644"))
            print(get_text("text_0645"))
            print(get_text("text_0646"))
            gamestart()
            return
        elif cmd == "bag":
            for item in have_list:
                print(item)
        else:
            print(get_text("text_0647"))

# watchtower
def watchtower():
    global hp, have_list, good, evil, game_over, game_back,map_unlocked,cleared_ending

    print(get_text("text_0648"))
    print(get_text("text_0649"))
    print(get_text("text_0650"))
    print(get_text("text_0651"))

    floor = 1
    while True:
        cmd = input(get_text("input_0652"))

        if cmd == "climb" or cmd == "up":
            if floor == 1:
                print(get_text("text_0653"))
                floor = 2
            elif floor == 2:
                print(get_text("text_0654"))
                floor = 3
            elif floor == 3:
                print(get_text("text_0655"))
                print(get_text("text_0656"))
                floor = 4
            elif floor == 4:
                print(get_text("text_0657"))
                floor = 5
            elif floor == 5:
                print(get_text("text_0658"))

        elif cmd == "down":
            if floor > 1:
                floor -= 1
                print(f"You go down to FLOOR {floor}.")
            else:
                print(get_text("text_0659"))

        elif cmd == "look":
            if floor == 1:
                print(get_text("text_0660"))
            elif floor == 2:
                print(get_text("text_0661"))
            elif floor == 3:
                print(get_text("text_0662"))
            elif floor == 4:
                print(get_text("text_0663"))
            elif floor == 5:
                print(get_text("text_0664"))
                print(get_text("text_0665"))
                print(get_text("text_0666"))
                print(get_text("text_0667"))
                print(get_text("text_0668"))
                print(get_text("text_0669"))
                print(get_text("text_0670"))
                print(get_text("text_0671"))
                print(get_text("text_0672"))
                map_unlocked = True
                if "a bird feather" not in have_list:
                    have_list.append("a bird feather")
                    print(get_text("text_0673"))

        elif cmd == "ask story" and floor == 4:
            if tower_ghost_story == 0:
                print(get_text("text_0674"))
                print(get_text("text_0675"))
                print(get_text("text_0676"))
                tower_ghost_story = 1
            elif tower_ghost_story == 1:
                print(get_text("text_0677"))
                print(get_text("text_0678"))
                tower_ghost_story = 2
            elif tower_ghost_story == 2:
                print(get_text("text_0679"))
                print(get_text("text_0680"))
                faith += 5
                good += 5
                tower_ghost_story = 3
            else:
                print(get_text("text_0681"))
        elif cmd == 'fight ghost' and floor == 4 or cmd == 'kill ghost' and floor == 4 or cmd == 'attack ghost' and floor == 4:
            print(get_text("text_0682"))
        elif cmd == "give feather":
            if "a bird feather" in have_list:
                print(get_text("text_0683"))
                have_list.remove("bird feather")
                good += 10
                hp += 3
                print("HP +3 | Good +10")
            else:
                print(get_text("text_0684"))

        elif cmd == "leave" or cmd == "back" or cmd == "exit":
            print(get_text("text_0685"))
            return

        elif cmd == "hp":
            print(f"HP: {hp}")
        elif cmd == "bag":
            for item in have_list:
                print(item)
        elif cmd == "moral":
            print(f"Good: {good} | Evil: {evil}")
        else:
            print(get_text("text_0686"))

# ===================== PRINT VERSION - CELESTIAL REALM =====================
def print_heaven():
    print("="*60)
    print(get_text("text_0687"))
    print("="*60)
    print(get_text("text_0688"))
    print(get_text("text_0689"))
    print(get_text("text_0690"))
    print(get_text("text_0691"))
    print(get_text("text_0692"))
    print(get_text("text_0693"))
    print(get_text("text_0694"))
    print("="*60)

    while True:
        print(get_text("text_0695"))
        print(get_text("text_0696"))
        print(get_text("text_0697"))
        print(get_text("text_0698"))
        print(get_text("text_0699"))
        print(get_text("text_0700"))

        opt = input(get_text("input_0701"))

        if opt == "1":
            print(get_text("text_0702"))
            print(get_text("text_0703"))
            print(get_text("text_0704"))
            print(get_text("text_0705"))
            print(get_text("text_0706"))
            choice = input()
            if choice == "ask for power":
                print(get_text("text_0707"))
                print("HP: 999 | Good: +50")
                print(get_text("text_0708"))
            elif choice == "ask for peace":
                print(get_text("text_0709"))
                print(get_text("text_0710"))
                print("Good: +100")
            elif choice == "ask for forgiveness":
                print(get_text("text_0711"))
                print("Evil: 0 | Good: +75")

        elif opt == "2":
            print(get_text("text_0712"))
            print(get_text("text_0713"))
            print(get_text("text_0714"))
            print(get_text("text_0715"))
            print(get_text("text_0716"))
            print(get_text("text_0717"))
            print("Faith: +20")
            print(get_text("text_0718"))
        elif opt == "3":
            print(get_text("text_0719"))
            print(get_text("text_0720"))
            print(get_text("text_0721"))
            print(get_text("text_0722"))
            print(get_text("text_0723"))
            choice = input()
            if choice == "become a god":
                print(get_text("text_0724"))
                print(get_text("text_0725"))
                print(get_text("text_0726"))
                show_message_wall()
                name = input(get_text("input_0727"))
                msg = input(get_text("input_0728"))
                save_message(name, msg)
                print(get_text("text_0729"))
                print(get_text("text_0730"))
                print(get_text("text_0731"))
                print(get_text("text_0732"))
                print(get_text("text_0733"))
                print(get_text("text_0734"))
                print(get_text("text_0735"))
                print(get_text("text_0736"))
                print(get_text("text_0737"))
                print(get_text("text_0738"))
                print(get_text("text_0739"))
                print(get_text("text_0740"))
                print(get_text("text_0741"))
                exit()
            elif choice == "return to earth":
                print(get_text("text_0742"))
                print(get_text("text_0743"))
                print(get_text("text_0744"))
                print(get_text("text_0745"))
                show_message_wall()
                name = input(get_text("input_0746"))
                msg = input(get_text("input_0747"))
                save_message(name, msg)
                print(get_text("text_0748"))
                print(get_text("text_0749"))
                print(get_text("text_0750"))
                print(get_text("text_0751"))
                print(get_text("text_0752"))
                print(get_text("text_0753"))
                print(get_text("text_0754"))
                print(get_text("text_0755"))
                print(get_text("text_0756"))
                print(get_text("text_0757"))
                print(get_text("text_0758"))
                print(get_text("text_0759"))
                print(get_text("text_0760"))
                exit()
            elif choice == "create a new world":
                print(get_text("text_0761"))
                print(get_text("text_0762"))
                print(get_text("text_0763"))
                show_message_wall()
                name = input(get_text("input_0764"))
                msg = input(get_text("input_0765"))
                save_message(name, msg)
                print(get_text("text_0766"))
                print(get_text("text_0767"))
                print(get_text("text_0768"))
                print(get_text("text_0769"))
                print(get_text("text_0770"))
                print(get_text("text_0771"))
                print(get_text("text_0772"))
                print(get_text("text_0773"))
                print(get_text("text_0774"))
                print(get_text("text_0775"))
                print(get_text("text_0776"))
                print(get_text("text_0777"))
                print(get_text("text_0778"))
                exit()

        elif opt == "4":
            print(get_text("text_0779"))
            main()
            return

        elif opt == "5":
            print(get_text("text_0780"))
            print(get_text("text_0781"))
            print(get_text("text_0782"))
            print(get_text("text_0783"))
            choice = input()
            if choice == "judge all":
                print(get_text("text_0784"))
                print(get_text("text_0785"))
                print(get_text("text_0786"))
                print(get_text("text_0787"))
            elif choice == "forgive all":
                print(get_text("text_0788"))
                print(get_text("text_0789"))
                print(get_text("text_0790"))
                print(get_text("text_0791"))
            elif choice == "let them choose":
                print(get_text("text_0792"))
                print(get_text("text_0793"))
                print(get_text("text_0794"))
                print(get_text("text_0795"))

            print(get_text("text_0796"))
            print(get_text("text_0797"))
            show_message_wall()
            name = input(get_text("input_0798"))
            msg = input(get_text("input_0799"))
            save_message(name, msg)
            print(get_text("text_0800"))
            print(get_text("text_0801"))
            print(get_text("text_0802"))
            print(get_text("text_0803"))
            print(get_text("text_0804"))
            print(get_text("text_0805"))
            print(get_text("text_0806"))
            print(get_text("text_0807"))
            print(get_text("text_0808"))
            print(get_text("text_0809"))
            print(get_text("text_0810"))
            print(get_text("text_0811"))
            print(get_text("text_0812"))
            exit()
        elif opt == "6":
            jump_scare_face('flash')
            print(get_text("text_0813"))
            print(get_text("text_0814"))
            titan_guardian_easter()
def time_travel_origin():
    global good, evil, hp, game_over, game_back, cleared_ending

    print("\n" + "="*60)
    print(get_text("text_0815"))
    print("="*60)
    print(get_text("text_0816"))
    print(get_text("text_0817"))
    print(get_text("text_0818"))
    print("="*60)

    past_phase = 1

    while True:
        print(f"\n--- PAST PHASE {past_phase} ---")
        cmd = input(get_text("input_0819"))

        if past_phase == 1:
            if cmd == "look":
                print(get_text("text_0820"))
            elif cmd == "talk":
                print(get_text("text_0821"))
                print(get_text("text_0822"))
                past_phase = 2
            elif cmd == "leave":
                print(get_text("text_0823"))
                gamestart()
                return
            else:
                print(get_text("text_0824"))

        elif past_phase == 2:
            if cmd == "look":
                print(get_text("text_0825"))
            elif cmd == "help":
                print(get_text("text_0826"))
                good += 99
                past_phase = 3
            elif cmd == "watch":
                print(get_text("text_0827"))
                evil += 50
                past_phase = 3
            else:
                print(get_text("text_0828"))

        elif past_phase == 3:
            if cmd == "look":
                print(get_text("text_0829"))
            elif cmd == "stop seal":
                print(get_text("text_0830"))
                print(get_text("text_0831"))
                print(get_text("text_0832"))
                cleared_ending = True
                main()
            elif cmd == "let seal":
                print(get_text("text_0833"))
                print(get_text("text_0834"))
                main()
                return
            elif cmd == "unite":
                print(get_text("text_0835"))
                print(get_text("text_0836"))
                print(get_text("text_0837"))
                cleared_ending = True
                main()
                return
            else:
                print(get_text("text_0838"))

        if game_over:
            print(get_text("text_0839"))
            print(get_text("text_0840"))
            while True:
                c = input()
                if c == "menu":
                    menu()
                    return

def jump_scare_face(mode="normal"):
    if mode == "flash":
        for i in range(30):
            print(get_text("text_0841"))
        print(get_text("text_0842"))
        print(get_text("text_0843"))
        print(get_text("text_0844"))
        print(get_text("text_0845"))
        print(get_text("text_0846"))
        print(get_text("text_0847"))
        print(get_text("text_0848"))
        print(get_text("text_0849"))
        print(get_text("text_0850"))
        print(get_text("text_0851"))
        for i in range(50):
            print(get_text("text_0852"))
            time.sleep(0.002)
        print(get_text("text_0853"))
    elif mode == "bloody":
        print(get_text("text_0854"))
        print(get_text("text_0855"))
        print(get_text("text_0856"))
        print(get_text("text_0857"))
        print(get_text("text_0858"))
        print(get_text("text_0859"))
        print(get_text("text_0860"))
        print(get_text("text_0861"))
        print(get_text("text_0862"))
        print(get_text("text_0863"))
        print(get_text("text_0864"))
        print(get_text("text_0865"))
        print(get_text("text_0866"))
    else:
        print(get_text("text_0867"))
        print(get_text("text_0868"))
        print(get_text("text_0869"))
        print(get_text("text_0870"))
        print(get_text("text_0871"))
        print(get_text("text_0872"))
        print(get_text("text_0873"))
        print(get_text("text_0874"))
        print(get_text("text_0875"))
        print(get_text("text_0876"))

def hill():
    global current_room,hp,evil,good,game_back,game_over,cleared_ending,map_unlocked
    high = 0

    current_room = 'hill'
    print(get_text("text_0877"))
    while True:
        cmd = input()
        if cmd == 'climb':
            if high == 0:
                high = 1
                print(get_text("text_0878"))
            elif high == 1:
                high = 2
                print(get_text("text_0879"))
                print(get_text("text_0880"))
                print(get_text("text_0881"))
                hp -= 5
                if hp <= 0:
                    print(get_text("text_0882"))
                    game_over = True
                    game_back = True
                    break
                if 'a book' not in have_list:
                    print(get_text("text_0883"))
                    have_list.append('a book')
                else:
                    print(get_text("text_0884"))
            elif high == 2:
                high == 3
                print(get_text("text_0885"))
                print(get_text("text_0886"))
                print(get_text("text_0887"))
                print(get_text("text_0888"))
                map_unlocked = True
        elif cmd == 'read book' and 'a book' in have_list or cmd == 'read' and 'a book' in have_list:
            print(get_text("text_0889"))
            print(get_text("text_0890"))
            print(get_text("text_0891"))
            print(get_text("text_0892"))
            print(get_text("text_0893"))
            print(get_text("text_0894"))
            print(get_text("text_0895"))
            print(get_text("text_0896"))
            print(get_text("text_0897"))
            print(get_text("text_0898"))
            print(get_text("text_0899"))
            print(get_text("text_0900"))
            print(get_text("text_0901"))
            print(get_text("text_0902"))
            print(get_text("text_0903"))
            print(get_text("text_0904"))
            print(get_text("text_0905"))
        elif cmd == 'look' and high == 0:
            print(get_text("text_0906"))
        elif cmd == 'look' and high == 1:
            print(get_text("text_0907"))
        elif cmd == 'look' and high == 2:
            print(get_text("text_0908"))
        elif cmd == 'look' and high == 3:
            print(get_text("text_0909"))
        elif cmd == 'touch statue':
            print(get_text("text_0910"))
        elif cmd == 'leave' or cmd == 'back' or cmd == 'down' and high == 0:
            print(get_text("text_0911"))
            gamestart()
            return
        elif cmd == 'leave' or cmd == 'back' or cmd == 'down' and high == 1:
            high = 0
            print(get_text("text_0912"))
        elif cmd == 'leave' or cmd == 'back' or cmd == 'down' and high == 2:
            high = 1
            print(get_text("text_0913"))
        else:
            print(get_text("text_0914"))
    if game_over == True:
        print(get_text("text_0915"))
        print(get_text("text_0916"))
        while True:
            c = input()
            if c == 'menu':
                menu()
                return
            else:
                print(get_text("text_0917"))
#cave
def cave():
    global game_over, hp, have_list, light, p, amulet, map_unlocked, secret_unlocked, diary_read, legacy_unlocked, current_room, torch,rune1,rune2,rune3,rune,grandmother,gate_unlock,old_diary_readed, game_back,play_count,old_note_readed,festival_mode,cleared_ending,force_in_cave,all_collected,amulet,ng_amulet,has_elf_amulet
    global has_death_corpse, death_location, death_corpse_item
    game_over = False
    jump_scare_face('flash')
    while True:
        if has_death_corpse and death_location == current_room:
            print(get_text("text_0918"))
        op = input()
        if handle_terminal_cmd(op):
            continue
        if op == 'unlock':
            if 'a key' in have_list:
                x = random.randint(1,5)
                if x == 1:
                    jump_scare_face('flash')
                    print(get_text("text_0919"))
                    print(get_text("text_0920"))
                    if 'super amulet' not in have_list:
                        print(get_text("text_0921"))
                        game_over = True
                        game_back = True
                        break
                    elif 'super amulet' in have_list:
                        print(get_text("text_0922"))
                        have_list.remove('super amulet')
                else:
                    fake_key = random.randint(1,10)
                    if fake_key == 1:
                        jump_scare_face('flash')
                        print(get_text("text_0923"))
                        print(get_text("text_0924"))
                        if festival_mode:
                            print(get_text("text_0925"))
                            hp += 2
                        else:
                            if 'super amulet' not in have_list:
                                print(get_text("text_0926"))
                                print(get_text("text_0927"))
                                game_over = True
                                game_back = True
                                break
                            elif 'super amulet' in have_list:
                                print(get_text("text_0928"))
                                have_list.remove('super amulet')
                    else:
                        jump_scare_face('flash')
                        print(get_text("text_0929"))
                        print(get_text("text_0930"))
                        while True:
                            if has_death_corpse and death_location == current_room:
                                print(get_text("text_0931"))
                            west = input()
                            if west == 'west':
                                print(get_text("text_0932"))
                                print(get_text("text_0933"))
                                while True:
                                    if has_death_corpse and death_location == current_room:
                                        print(get_text("text_0934"))
                                    gocave = input()
                                    if gocave == 'east':
                                        print(get_text("text_0935"))
                                    elif gocave == 'dig':
                                        if 'a pick-axe' in have_list:
                                            print(get_text("text_0936"))
                                            print(get_text("text_0937"))
                                            gamestart()
                                            return
                                        else:
                                            print(get_text("text_0938"))
                                    elif gocave == "examine corpse" or gocave == 'corpse' or gocave == 'search corpse' or gocave == 'find corpse':
                                        if has_death_corpse and death_location == current_room:
                                            print(get_text("text_0939"))
                                            if death_corpse_item:
                                                print(f"You retrieve {death_corpse_item} from its pocket.")
                                                have_list.append(death_corpse_item)
                                            else:
                                                print(get_text("text_0940"))
                                            has_death_corpse = False
                                        else:
                                            print(get_text("text_0941"))
                                    elif gocave == 'library':
                                        print(get_text("text_0942"))
                                        while True:
                                            lib = input(get_text("input_0943"))
                                            if lib == 'read':
                                                print(get_text("text_0944"))
                                                print(get_text("text_0945"))
                                                print(get_text("text_0946"))
                                                print(get_text("text_0947"))
                                            elif lib == 'read all':
                                                print(get_text("text_0948"))
                                                print(get_text("text_0949"))
                                                print(get_text("text_0950"))
                                                faith += 10
                                            elif lib == 'take book':
                                                have_list.append('memory book')
                                                print(get_text("text_0951"))
                                            elif lib == 'back':
                                                break
                                            else:
                                                print(get_text("text_0952"))
                                    elif gocave == 'sewer' or gocave == 'go into sewer' or gocave == 'go into the sewer' or gocave == 'go to sewer':
                                        print(get_text("text_0953"))
                                        print(get_text("text_0954"))
                                        print(get_text("text_0955"))
                                        while True:
                                            if has_death_corpse and death_location == current_room:
                                                print(get_text("text_0956"))
                                            sewer_cmd = input(get_text("input_0957"))
                                            if sewer_cmd == 'west' or sewer_cmd == 'back' or sewer_cmd == 'leave':
                                                print(get_text("text_0958"))
                                                break
                                            elif sewer_cmd == "examine corpse" or sewer_cmd == 'corpse' or sewer_cmd == 'search corpse' or sewer_cmd == 'find corpse':
                                                if has_death_corpse and death_location == current_room:
                                                    print(get_text("text_0959"))
                                                    if death_corpse_item:
                                                        print(f"You retrieve {death_corpse_item} from its pocket.")
                                                        have_list.append(death_corpse_item)
                                                    else:
                                                        print(get_text("text_0960"))
                                                    has_death_corpse = False
                                                else:
                                                    print(get_text("text_0961"))
                                            elif sewer_cmd == 'forward':
                                                jump_scare_face('flash')
                                                print(get_text("text_0962"))
                                                hp -= 2
                                                print(get_text("text_0963"))
                                                print(get_text("text_0964"))
                                                print(get_text("text_0965"))
                                                print(get_text("text_0966"))
                                                print(get_text("text_0967"))
                                                print(get_text("text_0968"))
                                                print(get_text("text_0969"))
                                                print(get_text("text_0970"))
                                                print(get_text("text_0971"))
                                                old_note_readed = True
                                                if old_diary_readed == True or grave_diary_read == True:
                                                    print(get_text("text_0972"))
                                                else:
                                                    print(get_text("text_0973"))
                                                if hp <= 0:
                                                    print(get_text("text_0974"))
                                                    game_over = True
                                                    game_back = True
                                                    break
                                            elif sewer_cmd == 'treasure':
                                                print(get_text("text_0975"))
                                                have_list.append('gold coins')
                                            elif sewer_cmd == "deep" or sewer_cmd == 'go deep':
                                                jump_scare_face('flash')
                                                print(get_text("text_0976"))
                                                print(get_text("text_0977"))
                                                while True:
                                                    deep_cmd = input(get_text("input_0978"))
                                                    if deep_cmd == "open door":
                                                        if "rune stone 1" in have_list:
                                                            print(get_text("text_0979"))
                                                            print(get_text("text_0980"))
                                                        else:
                                                            print(get_text("text_0981"))
                                                    elif deep_cmd == "read letter":
                                                        print(get_text("text_0982"))
                                                        print(get_text("text_0983"))
                                                        print(get_text("text_0984"))
                                                        old_note_readed = True
                                                    elif deep_cmd == "take staff":
                                                        print(get_text("text_0985"))
                                                        have_list.append("wizard staff")
                                                        print(get_text("text_0986"))
                                                    elif deep_cmd == "leave":
                                                        print(get_text("text_0987"))
                                                        break
                                                    else:
                                                        print(get_text("text_0988"))
                                            elif sewer_cmd == 'bag':
                                                for i in have_list:
                                                    print(i)
                                            else:
                                                print(get_text("text_0989"))
                                    elif gocave == 'west':
                                        print(get_text("text_0990"))
                                        print(get_text("text_0991"))
                                        while True:
                                            if has_death_corpse and death_location == current_room:
                                                print(get_text("text_0992"))
                                            pathwest = input()
                                            if pathwest == 'west':
                                                print(get_text("text_0993"))
                                                print(get_text("text_0994"))
                                                while True:
                                                    if has_death_corpse and death_location == current_room:
                                                        print(get_text("text_0995"))
                                                    west2 = input()
                                                    if west2 == 'west':
                                                        while True:
                                                            print(get_text("text_0996"))
                                                            print('You go west, you see here a human corpse, you are shocked! There is still path to west. You see here ' + p)
                                                            print(get_text("text_0997"))
                                                            west3 = input()
                                                            if west3 == 'west':
                                                                while True:
                                                                    print(get_text("text_0998"))
                                                                    print(get_text("text_0999"))
                                                                    choice = input(get_text("input_1000"))
                                                                    if choice == "go dark":
                                                                        print(get_text("text_1001"))
                                                                        if 'a pick-axe' in have_list and 'diamond vault' in have_list:
                                                                            print(get_text("text_1002"))
                                                                            if diary_read == True and legacy_unlocked == True:
                                                                                print(get_text("text_1003"))
                                                                                print(get_text("text_1004"))
                                                                            print(get_text("text_1005"))
                                                                            game_over = True
                                                                            game_back = True
                                                                            cleared_ending = True
                                                                            break
                                                                        elif "a pick-axe" in have_list:
                                                                            required_items = {"rope", "flint", "old compass", "an amulet", "diamond vault"}
                                                                            if required_items.issubset(set(have_list)):
                                                                                all_collected = True
                                                                            if all_collected:
                                                                                print(get_text("text_1006"))
                                                                                if diary_read == True and legacy_unlocked == True:
                                                                                    print(get_text("text_1007"))
                                                                                    print(get_text("text_1008"))
                                                                                print(get_text("text_1009"))
                                                                                game_over = True
                                                                                game_back = True
                                                                                cleared_ending = True
                                                                                break
                                                                            else:
                                                                                print(get_text("text_1010"))
                                                                                print(get_text("text_1011"))
                                                                                if diary_read == True and legacy_unlocked == True:
                                                                                    print(get_text("text_1012"))
                                                                                    print(get_text("text_1013"))
                                                                                print(get_text("text_1014"))
                                                                                game_over = True
                                                                                game_back = True
                                                                                cleared_ending = True
                                                                                break
                                                                        else:
                                                                            print(get_text("text_1015"))
                                                                            print(get_text("text_1016"))
                                                                            print(get_text("text_1017"))
                                                                            game_over = True
                                                                            game_back = True
                                                                            cleared_ending = True
                                                                            break
                                                                    elif choice == "go bright":
                                                                        print(get_text("text_1018"))
                                                                        print(get_text("text_1019"))
                                                                        print(get_text("text_1020"))
                                                                        game_over = True
                                                                        game_back = True
                                                                        break
                                                                    elif choice == 'east':
                                                                        print(get_text("text_1021"))
                                                                        break
                                                                    elif choice == 'bag':
                                                                        for i in range(len(have_list)):
                                                                            print(have_list[i])
                                                                    else:
                                                                        print(get_text("text_1022"))
                                                            elif west3 == "orc":
                                                                orc_tribe_dungeon()
                                                            elif west3 == "hug ghost":
                                                                print(get_text("text_1023"))
                                                                have_list.append("ghost hug")
                                                            elif west3 == "ask about dev":
                                                                print(get_text("text_1024"))
                                                                print(get_text("text_1025"))
                                                                print(get_text("text_1026"))
                                                            elif west3 == "find secret wall":
                                                                if "a pick-axe" in have_list:
                                                                    print(get_text("text_1027"))
                                                                    print(get_text("text_1028"))
                                                                    print(get_text("text_1029"))
                                                                    have_list.append("dev test note")
                                                                else:
                                                                    print(get_text("text_1030"))
                                                            elif west3 == "read dev test note":
                                                                if "dev test note" in have_list:
                                                                    print(get_text("text_1031"))
                                                                    print(get_text("text_1032"))
                                                                    print(get_text("text_1033"))
                                                                else:
                                                                    print(get_text("text_1034"))
                                                            elif west3 == "ghost job":
                                                                print(get_text("text_1035"))
                                                                print(get_text("text_1036"))
                                                            elif west3 == "ghost bored":
                                                                print(get_text("text_1037"))
                                                                print(get_text("text_1038"))
                                                            elif west3 == "ghost friend":
                                                                print(get_text("text_1039"))
                                                                print(get_text("text_1040"))
                                                            elif west3 == "ghost joke":
                                                                print(get_text("text_1041"))
                                                                print(get_text("text_1042"))
                                                            elif west3 == "ghost favorite food":
                                                                print(get_text("text_1043"))
                                                                print(get_text("text_1044"))
                                                            elif west3 == "ghost school":
                                                                print(get_text("text_1045"))
                                                                print(get_text("text_1046"))
                                                            elif west3 == "ghost rain":
                                                                print(get_text("text_1047"))
                                                                print(get_text("text_1048"))
                                                            elif west3 == "ghost phone":
                                                                print(get_text("text_1049"))
                                                                print(get_text("text_1050"))
                                                            elif west3 == "ghost band":
                                                                print(get_text("text_1051"))
                                                                print(get_text("text_1052"))
                                                            elif west3 == "ghost pet":
                                                                print(get_text("text_1053"))
                                                                print(get_text("text_1054"))
                                                            elif west3 == "ghost workout":
                                                                print(get_text("text_1055"))
                                                                print(get_text("text_1056"))
                                                            elif west3 == "ghost holiday":
                                                                print(get_text("text_1057"))
                                                                print(get_text("text_1058"))
                                                            elif festival_mode:
                                                                print(get_text("text_1059"))
                                                                hp += 2
                                                            elif west3 == "ghost fashion":
                                                                print(get_text("text_1060"))
                                                                print(get_text("text_1061"))
                                                            elif west3 == "ghost password":
                                                                print(get_text("text_1062"))
                                                                print(get_text("text_1063"))
                                                            elif west3 == "tell scary story":
                                                                print(get_text("text_1064"))
                                                            elif west3 == "wave flashlight":
                                                                print(get_text("text_1065"))
                                                            elif west3 == "ask age":
                                                                print(get_text("text_1066"))
                                                            elif west3 == "ask food":
                                                                print(get_text("text_1067"))
                                                            elif west3 == "scare ghost":
                                                                print(get_text("text_1068"))
                                                            elif west3 == "ask sleep":
                                                                print(get_text("text_1069"))
                                                            elif west3 == "borrow clothes":
                                                                print(get_text("text_1070"))
                                                            elif west3 == "ask travel":
                                                                print(get_text("text_1071"))
                                                            elif west3 == "sing off key":
                                                                print(get_text("text_1072"))
                                                            elif west3 == "play dead":
                                                                print(get_text("text_1073"))
                                                            elif west3 == "lift hand":
                                                                print(get_text("text_1074"))
                                                            elif west3 == "walk slow":
                                                                print(get_text("text_1075"))
                                                            elif west3 == "lean close":
                                                                print(get_text("text_1076"))
                                                            elif west3 == "race on foot" or west3 == 'race':
                                                                print(get_text("text_1077"))
                                                            elif west3 == "blow kiss to ghost":
                                                                print(get_text("text_1078"))
                                                            elif west3 == "play tag":
                                                                print(get_text("text_1079"))
                                                            elif west3 == "complain cold" or west3 == 'complain':
                                                                print(get_text("text_1080"))
                                                            elif west3 == "pat ghost":
                                                                print(get_text("text_1081"))
                                                            elif west3 == "wave finger":
                                                                print(get_text("text_1082"))
                                                            elif west3 == "call" or west3 == 'call ghost':
                                                                print(get_text("text_1083"))
                                                            elif west3 == "point around":
                                                                print(get_text("text_1084"))
                                                            elif west3 == "hum song":
                                                                print(get_text("text_1085"))
                                                            elif west3 == 'sing':
                                                                print(get_text("text_1086"))
                                                            elif west3 == "selfie":
                                                                print(get_text("text_1087"))
                                                                print(get_text("text_1088"))
                                                            elif west3 == "feed":
                                                                print(get_text("text_1089"))
                                                                print(get_text("text_1090"))
                                                            elif west3 == "tease ghost":
                                                                print(get_text("text_1091"))
                                                            elif west3 == "fight ghost":
                                                                if festival_mode:
                                                                    print(get_text("text_1092"))
                                                                    hp += 2
                                                                else:
                                                                    if play_count == 1:
                                                                        print(get_text("text_1093"))
                                                                        ghost_hp = 3
                                                                        while ghost_hp > 0 and hp > 0:
                                                                            print(f"Ghost HP: {ghost_hp} | Your HP: {hp}")
                                                                            fight = input(get_text("input_1094"))
                                                                            if fight == "attack":
                                                                                ghost_hp -= 1
                                                                                print(get_text("text_1095"))
                                                                                if ghost_hp > 0:
                                                                                    hp -= 2
                                                                                    print(get_text("text_1096"))
                                                                            elif fight == "run":
                                                                                print(get_text("text_1097"))
                                                                                break
                                                                        if ghost_hp <= 0:
                                                                            print(get_text("text_1098"))
                                                                            have_list.append("ghost sword")
                                                                        elif hp <= 0:
                                                                            print(get_text("text_1099"))
                                                                            game_over = True
                                                                            game_back = True
                                                                    else:
                                                                        print(get_text("text_1100"))
                                                            elif west3 == 'take pick-axe':
                                                                print(get_text("text_1101"))
                                                                print(get_text("text_1102"))
                                                                print(get_text("text_1103"))
                                                                print(get_text("text_1104"))
                                                                hp -= 3
                                                                if hp <= 0:
                                                                    print(get_text("text_1105"))
                                                                    print(get_text("text_1106"))
                                                                    game_over = True
                                                                    game_back = True
                                                                    break
                                                                print('left hp: ' + str(hp))
                                                                have_list.append(p)
                                                                p = 'nothing'
                                                                if play_count == 2:
                                                                    print(get_text("text_1107"))
                                                                    print(get_text("text_1108"))
                                                                    print(get_text("text_1109"))
                                                                elif play_count == 1:
                                                                    print(get_text("text_1110"))
                                                                    if festival_mode:
                                                                        print(get_text("text_1111"))
                                                                        hp += 2
                                                                    else:
                                                                        if amulet == True:
                                                                            print(get_text("text_1112"))
                                                                        else:
                                                                            print(get_text("text_1113"))
                                                                            game_over = True
                                                                            game_back = True
                                                                            break
                                                            elif west3 == 'east':
                                                                print(get_text("text_1114"))
                                                                break
                                                            elif west3 == 'touch corpse':
                                                                print(get_text("text_1115"))
                                                                amulet = True
                                                                have_list.append('an amulet')
                                                            elif west3 == 'room':
                                                                print(get_text("text_1116"))
                                                                trap = random.randint(1,4)
                                                                if trap != 1:
                                                                    print(get_text("text_1117"))
                                                                    print(get_text("text_1118"))
                                                                else:
                                                                    print(get_text("text_1119"))
                                                                    game_over = True
                                                                    game_back = True
                                                                    break
                                                            elif west3 == 'thank you':
                                                                if diary_read:
                                                                    print(get_text("text_1120"))
                                                                    have_list.append('diamonds')
                                                                else:
                                                                    print(get_text("text_1121"))
                                                            elif west3 == 'colin woody':
                                                                print(get_text("text_1122"))
                                                                print(get_text("text_1123"))
                                                                have_list.append('diamond vault')
                                                            elif west3 == 'bag':
                                                                for i in range(len(have_list)):
                                                                    print(have_list[i])
                                                            elif west3 == 'kill me':
                                                                print(get_text("text_1124"))
                                                                game_over = True
                                                                game_back = True
                                                                break
                                                            elif west3 == 'search corpse':
                                                                print(get_text("text_1125"))
                                                                print(get_text("text_1126"))
                                                                have_list.append('old compass')
                                                                legacy_unlocked = True
                                                            elif west3 == 'bury corpse':
                                                                if diary_read == True:
                                                                    print(get_text("text_1127"))
                                                                    print(get_text("text_1128"))
                                                                    print(get_text("text_1129"))
                                                                    amulet = True
                                                                else:
                                                                    print(get_text("text_1130"))
                                                            else:
                                                                print(get_text("text_1131"))
                                                           
                                                            if game_over == True:
                                                                print(get_text("text_1132"))
                                                                print(get_text("text_1133"))
                                                                while True:
                                                                    c = input()
                                                                    if c == 'menu':
                                                                        menu()
                                                                        return
                                                                    else:
                                                                        print(get_text("text_1134"))
                                                    elif west2 == 'take note':
                                                        print(get_text("text_1135"))
                                                        print(get_text("text_1136"))
                                                        hp -= 1
                                                        if hp <= 0:
                                                            print(get_text("text_1137"))
                                                            print(get_text("text_1138"))
                                                            game_over = True
                                                            game_back = True
                                                            break
                                                    elif west2 == 'read diary':
                                                        print(get_text("text_1139"))
                                                        print(get_text("text_1140"))
                                                        print(get_text("text_1141"))
                                                        print(get_text("text_1142"))
                                                        print(get_text("text_1143"))
                                                        print(get_text("text_1144"))
                                                        print(get_text("text_1145"))
                                                        print(get_text("text_1146"))
                                                        hp += 1
                                                        diary_read = True
                                                    elif west2 == 'east':
                                                        print(get_text("text_1147"))
                                                        break
                                                    elif west2 == 'bag':
                                                        for i in range(len(have_list)):
                                                            print(have_list[i])
                                                    else:
                                                        print(get_text("text_1148"))
                                                    if game_over == True:
                                                        print(get_text("text_1149"))
                                                        print(get_text("text_1150"))
                                                        while True:
                                                            c = input()
                                                            if c == 'menu':
                                                                menu()
                                                                return
                                                            else:
                                                                print(get_text("text_1151"))
                                            elif pathwest == 'east':
                                                print(get_text("text_1152"))
                                                break
                                            elif pathwest == "examine corpse" or pathwest == 'corpse' or pathwest == 'search corpse' or pathwest == 'find corpse':
                                                if has_death_corpse and death_location == current_room:
                                                    print(get_text("text_1153"))
                                                    if death_corpse_item:
                                                        print(f"You retrieve {death_corpse_item} from its pocket.")
                                                        have_list.append(death_corpse_item)
                                                    else:
                                                        print(get_text("text_1154"))
                                                    has_death_corpse = False
                                                else:
                                                    print(get_text("text_1155"))
                                            elif pathwest == 'bag':
                                                for i in range(len(have_list)):
                                                    print(have_list[i])

                                            else:
                                                print(get_text("text_1156"))
                                            if game_over == True:
                                                print(get_text("text_1157"))
                                                print(get_text("text_1158"))
                                                while True:
                                                    c = input()
                                                    if c == 'menu':
                                                        menu()
                                                        return
                                                    else:
                                                        print(get_text("text_1159"))
                                    elif gocave == 'bag':
                                        for i in range(len(have_list)):
                                            print(have_list[i])
                                    else:
                                        print(get_text("text_1160"))
                                    if game_over == True:
                                        print(get_text("text_1161"))
                                        print(get_text("text_1162"))
                                        while True:
                                            c = input()
                                            if c == 'menu':
                                                menu()
                                                return
                                            else:
                                                print(get_text("text_1163"))
                                if game_over == True:
                                    print(get_text("text_1164"))
                                    print(get_text("text_1165"))
                                    while True:
                                        c = input()
                                        if c == 'menu':
                                            menu()
                                            return
                                        else:
                                            print(get_text("text_1166"))
                            elif west == 'bag':
                                for i in range(len(have_list)):
                                    print(have_list[i])
                            if game_over == True:
                                print(get_text("text_1167"))
                                print(get_text("text_1168"))
                                while True:
                                    c = input()
                                    if c == 'menu':
                                        menu()
                                        return
                                    else:
                                        print(get_text("text_1169"))
                        
                            elif west == 'north':
                                print(get_text("text_1170"))
                            elif west == 'south':
                                print(get_text("text_1171"))
                            elif west == 'east':
                                print(get_text("text_1172"))
                            else:
                                print(get_text("text_1173"))
                        if game_over == True:
                            print(get_text("text_1174"))
                            print(get_text("text_1175"))
                            while True:
                                c = input()
                                if c == 'menu':
                                    main()
                                    return
                    if game_over == True:
                        print(get_text("text_1176"))
                        print(get_text("text_1177"))
                        while True:
                            c = input()
                            if c == 'menu':
                                main()
                                return
                if game_over == True:
                    print(get_text("text_1178"))
                    print(get_text("text_1179"))
                    while True:
                        c = input()
                        if c == 'menu':
                            main()
                            return
            if game_over == True:
                print(get_text("text_1180"))
                print(get_text("text_1181"))
                while True:
                    c = input()
                    if c == 'menu':
                        main()
                        return
                    
            else:
                if festival_mode:
                    print(get_text("text_1182"))
                    print(get_text("text_1183"))
                    hp += 2
                else:
                    if amulet == True or ng_amulet == True or has_elf_amulet == True:
                        print(get_text("text_1184"))
                    else:
                        print(get_text("text_1185"))
                        print(get_text("text_1186"))
                        game_over = True
                        game_back = True
            if game_over == True:
                print(get_text("text_1187"))
                print(get_text("text_1188"))
                while True:
                    c = input()
                    if c == 'menu':
                        main()
                        return
            print(get_text("text_1189"))
        elif op == 'south':
            print(get_text("text_1190"))
        elif op == 'east':
            print(get_text("text_1191"))
        elif op == 'compass':
            if 'old compass' in have_list:
                print(get_text("text_1192"))
            else:
                print(get_text("text_1193"))
            continue
        elif op == 'colin':
            print(get_text("text_1194"))
            gamestart()
            return
        elif op == "examine corpse" or op == 'corpse' or op == 'search corpse' or op == 'find corpse':
            if has_death_corpse and death_location == current_room:
                print(get_text("text_1195"))
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print(get_text("text_1196"))
                has_death_corpse = False
            else:
                print(get_text("text_1197"))
        else:
            print(get_text("text_1198"))
        if game_over == True:
            print(get_text("text_1199"))
            print(get_text("text_1200"))
            while True:
                c = input()
                if c == 'menu':
                    main()
                    return

#game
def gamestart():
    global have_list, game_over, light, hp, map_unlocked, secret_unlocked, amulet, take, chain1, chain2, current_room, torch,l,k,n,s,f,w,sc,rune1,rune2,rune3,rune,grandmother,diary_read,old_diary_readed,grave_diary_read, game_back,play_count,trap_protect,cleared_ending,force_in_cave
    global step_count
    global time_period
    global festival_mode, festival_steps
    global good, evil
    global weather_duration,weather_damage
    global merchant_story_stage,swamp_spirit_story,hut_ghost_story,tower_ghost_story
    global has_death_corpse, death_location, death_corpse_item
    global one_hole_in,two_hole_in,three_hole_in
    altar = False
    if game_back == True and cleared_ending == True:
        play_count = 2
        hp = 10
        torch = True
        light = True
        print("=== NEW GAME+ ===")
        print(get_text("text_1201"))
    else:
        play_count = 1
    cleared_ending = False
    print(get_text("text_1202"))
    print(get_text("text_1203"))
    print(get_text("text_1204"))
    print(get_text("text_1205"))
    print(get_text("text_1206"))
    if has_death_corpse and death_location == current_room:
        print(get_text("text_1207"))
    if map_unlocked == True:
            print(get_text("text_1208"))
    while True:
        if play_count >= 2 and death_count >= 1 and random.randint(1, 10) == 1:
            auto_cmd = random.choice(["go deeper", "do not leave", "stay here", "kill yourself"])
            print(auto_cmd)
            time.sleep(0.8)
            print(get_text("text_1209"))
            time.sleep(1)
            print(get_text("text_1210"))
            hp -= 2
            if auto_cmd == 'go deeper':
                if current_room != 'cave':
                    print(get_text("text_1211"))
                current_room = "cave"
                print(get_text("text_1212"))
                print(get_text("text_1213"))
                print(get_text("text_1214"))
                evil += 10
            elif auto_cmd == 'do not leave':
                print(get_text("text_1215"))
                time.sleep(1)
                print(get_text("text_1216"))
                print(get_text("text_1217"))
                hp -= 1
            elif auto_cmd == 'stay here':
                print(get_text("text_1218"))
            elif auto_cmd == 'kill yourself':
                for i in range(30):
                    print(get_text("text_1219"))
                    time.sleep(0.03)
                    print(get_text("text_1220"))
                    game_back = True
                    game_over = True
                    break
        if death_count >= 3 and random.randint(1, 10) == 1:
            player_name = get_last_player_name() or os.getlogin()
            print(get_text("text_1221"))
            print(f"'{player_name}... turn around...'")
            print(get_text("text_1222"))
            hp -= 1
        # Weather
        weather_duration -= 1
        if weather_duration <= 0:
            update_weather()
            print(get_text("text_1223"))
            print_weather()
        if weather_damage > 0:
            if amulet == False:
                hp -= weather_damage
                print(f"You take {weather_damage} damage from the weather.")
                if hp <= 0:
                    print(get_text("text_1224"))
                    game_over = True
                    game_back = True
                    if game_over == True:
                        print(get_text("text_1225"))
                        print(get_text("text_1226"))
                        while True:
                            c = input()
                            if c == 'menu':
                                main()
                                return
            else:
                print(get_text("text_1227"))
            print(get_text("text_1228"))
        # STRONGER DAY/NIGHT FEEL
        step_count += 1
        if step_count % 4 == 0:
            # FESTIVAL EGG — FULL MOON EVENT
            festival_steps += 1
            if festival_steps >= 7 and random.randint(1,3) == 1:
                festival_mode = True
                festival_steps = 0
                print(get_text("text_1229"))
                print(get_text("text_1230"))
                print(get_text("text_1231"))
                print(get_text("text_1232"))
                hp += 5
                good += 5
            elif festival_steps >= 25:
                festival_mode = False
                festival_steps = 0
                print(get_text("text_1233"))
                print(get_text("text_1234"))
                print(get_text("text_1235"))
            if time_period == "day":
                time_period = "dusk"
                print(get_text("text_1236"))
            elif time_period == "dusk":
                time_period = "night"
                print(get_text("text_1237"))
            elif time_period == "night":
                time_period = "day"
                print(get_text("text_1238"))

        # NIGHT DAMAGE (STRONGER)
        if time_period == "night" and not torch and not light:
            hp -= 1
            print(get_text("text_1239"))
            if hp <= 0:
                print(get_text("text_1240"))
                game_over = True
                game_back = True
                print(get_text("text_1241"))
                print(get_text("text_1242"))
                while True:
                    c = input()
                    if c == 'menu':
                        main()
                        return
        if festival_mode:
            print(get_text("text_1243"))
        go = input()
        if handle_terminal_cmd(go):
            continue
        if go == 'in':
            current_room = 'house'
            if play_count == 2:
                jump_scare_face('flash')
                print(get_text("text_1244"))
                print(get_text("text_1245"))
                print(get_text("text_1246"))
                print(get_text("text_1247"))
                print(get_text("text_1248"))
                print(get_text("text_1249"))
                print(get_text("text_1250"))
            elif play_count == 1:
                jump_scare_face('flash')
                print(get_text("text_1251"))
                print(get_text("text_1252"))
                print(get_text("text_1253"))
                print(get_text("text_1254"))
                print(get_text("text_1255"))
                print(get_text("text_1256"))
                print(get_text("text_1257"))
                print(get_text("text_1258"))
                print(get_text("text_1259"))
                print(get_text("text_1260"))
                print(get_text("text_1261"))
            while True:
                print('You are in the house, there is ' + l + k + n + s + sc +f + w + 'and a note your father left')
                print(get_text("text_1262"))
                print(get_text("text_1263"))
                if has_death_corpse and death_location == current_room:
                    print(get_text("text_1264"))
                take = input()
                if handle_terminal_cmd(take):
                    continue
                if take == 'take lamp':
                    print(get_text("text_1265"))
                    have_list.append('a lamp')
                    l = ''
                elif take == 'down' or take == 'go down' or take == 'climb down':
                    if one_hole_in == False:
                        forgotten_archive()
                    else:
                        print(get_text("text_1266"))
                elif take == 'take key':
                    if 'a key' not in have_list:
                        print(get_text("text_1267"))
                        have_list.append('a key')
                        k = ''
                    else:
                        print(get_text("text_1268"))
                elif take == 'pc' or take == 'take pc':
                    print(get_text("text_1269"))
                    print(get_text("text_1270"))
                    print(get_text("text_1271"))
                    print(get_text("text_1272"))
                elif take == "who made this" or take == 'Who made this' or take == 'who made this?' or take == 'Who made this?':
                    print(get_text("text_1273"))
                    print(get_text("text_1274"))
                elif take == "is this a game" or take == 'Is this a game' or take == 'is this a game?' or take == 'Is this a game?':
                    print(get_text("text_1275"))
                    print(get_text("text_1276"))
                    print(get_text("text_1277"))
                elif take == "spin":
                    print(get_text("text_1278"))
                elif take == "jump":
                    print(get_text("text_1279"))
                elif take == "flip table":
                    print(get_text("text_1280"))
                elif take == 'take food':
                    if 'some food' not in have_list:
                        print(get_text("text_1281"))
                        have_list.append('some food')
                        f = ''
                    else:
                        print(get_text("text_1282"))
                elif take == 'take water':
                    if 'a bottle' not in have_list:
                        print(get_text("text_1283"))
                        have_list.append('a bottle')
                        have_list.append('some water in the bottle')
                        w = ''
                    else:
                        print(get_text("text_1284"))
                elif take == 'take scroll':
                    if 'a scroll' not in have_list:
                        print(get_text("text_1285"))
                        have_list.append('a scroll')
                        sc = ''
                    else:
                        print(get_text("text_1286"))
                elif take == 'wall':
                    if rune1 == False:
                        print(get_text("text_1287"))
                        print(get_text("text_1288"))
                        rune1 = True
                        have_list.append('rune stone 1')
                    else:
                        print(get_text("text_1289"))
                elif take == "examine corpse" or take == 'corpse' or take == 'search corpse' or take == 'find corpse':
                    if has_death_corpse and death_location == current_room:
                        print(get_text("text_1290"))
                        if death_corpse_item:
                            print(f"You retrieve {death_corpse_item} from its pocket.")
                            have_list.append(death_corpse_item)
                        else:
                            print(get_text("text_1291"))
                        has_death_corpse = False
                    else:
                        print(get_text("text_1292"))
                elif take == 'light lamp':
                    if 'a lamp' in have_list:
                        print(get_text("text_1293"))
                        light = True
                    else:
                        print(get_text("text_1294"))
                elif take == 'hp':
                    print('HP:', hp)
                elif take == 'save':
                    save_game()
                elif take == 'load':
                    load_game()
                elif take == 'status' or take == 'statue':
                    print('HP:', hp)
                    print('Light:', light)
                    print('Torch:', torch)
                    print('Amulet:', amulet)
                elif take == 'read scroll':
                    if 'a scroll' in have_list:
                        print(get_text("text_1295"))
                        print(get_text("text_1296"))
                        print(get_text("text_1297"))
                        print(get_text("text_1298"))
                        print(get_text("text_1299"))
                        print(get_text("text_1300"))
                        print(get_text("text_1301"))
                        print(get_text("text_1302"))
                    else:
                        print(get_text("text_1303"))
                elif take == 'make torch':
                    if 'flint' in have_list and 'a lamp' in have_list:
                        print(get_text("text_1304"))
                        have_list.remove('flint')
                        have_list.remove('a lamp')
                        have_list.append('a torch')
                        torch = True
                        light = True
                    else:
                        print(get_text("text_1305"))
                elif take == 'Garry':
                    if play_count == 1:
                        print(get_text("text_1306"))
                        print(get_text("text_1307"))
                        game_over = True
                        game_back = True
                        cleared_ending = True
                        break
                    else:
                        print(get_text("text_1308"))
                elif take == 'take note':
                    print(get_text("text_1309"))
                elif take == 'out':
                    print(get_text("text_1310"))
                    break
                elif take == 'altar':
                    print(get_text("text_1311"))
                    altar = True
                    break
                elif take == "eat":
                    if "some food" in have_list:
                        have_list.remove("some food")
                        hp += 3
                        print("You eat food. HP +3")
                    else:
                        print(get_text("text_1312"))

                elif take == "drink":
                    if "some water in the bottle" in have_list:
                        have_list.remove("some water in the bottle")
                        hp += 2
                        print("You drink water. HP +2")
                    else:
                        print(get_text("text_1313"))
                elif take == 'bag':
                    for i in range(len(have_list)):
                        print(have_list[i])
                elif take == "stare":
                    print(get_text("text_1314"))
                elif take == "clap":
                    print(get_text("text_1315"))
                elif take == 'colin':
                    print(get_text("text_1316"))
                    chain1 = True
                elif take == 'woody' and chain1:
                    chain2 = True
                    print(get_text("text_1317"))
                
                elif take == 'garry' and chain2:
                    if play_count == 1:
                        print(get_text("text_1318"))
                        print(get_text("text_1319"))
                        print(get_text("text_1320"))
                        hp = 5
                        amulet = True
                        light = True
                        game_over = True
                        game_back = True
                        cleared_ending = True
                        break
                    else:
                        print(get_text("text_1321"))
                elif take == 'map':
                    print(get_text("text_1322"))
                    map_unlocked = True
                elif take == 'compass':
                    if 'old compass' in have_list:
                        if current_room == "house":
                            print(get_text("text_1323"))
                        elif current_room == "road":
                            print(get_text("text_1324"))
                        else:
                            print(get_text("text_1325"))
                    else:
                        print(get_text("text_1326"))
                elif take == 'read father note' or take == 'take father note' or take == 'father note':
                    print(get_text("text_1327"))
                    print(get_text("text_1328"))
                    print(get_text("text_1329"))
                    print(get_text("text_1330"))
                    print(get_text("text_1331"))
                    print(get_text("text_1332"))
                    print(get_text("text_1333"))
                    print(get_text("text_1334"))
                    print(get_text("text_1335"))
                    print(get_text("text_1336"))
                    print(get_text("text_1337"))
                    print(get_text("text_1338"))
                else:
                    print(get_text("text_1339"))
            if altar == True:
                if play_count == 2:
                    print(get_text("text_1340"))
                    print(get_text("text_1341"))
                    print(get_text("text_1342"))
                    print(get_text("text_1343"))
                elif play_count == 1:
                    print(get_text("text_1344"))
                print('You see here ' + rune)
                while True:
                    if rune1 and rune2 and rune3:
                        print(get_text("text_1345"))
                    tele = input()
                    if tele == 'light lamp':
                        if 'a lamp' in have_list:
                            print(get_text("text_1346"))
                            light =True
                        else:
                            print(get_text("text_1347"))
                    elif tele == 'take rune':
                        if play_count == 2:
                            if rune != 'nothing':
                                print(get_text("text_1348"))
                                print(get_text("text_1349"))
                                rune = 'nothing' 
                                rune3 = True
                            else:
                                print(get_text("text_1350"))
                        else:
                            print(get_text("text_1351"))
                            print(get_text("text_1352"))
                    elif tele == 'colin':
                        if light == False and not torch:
                            if hp > 10:
                                print(get_text("text_1353"))
                                hp -= 10
                                force_in_cave = True
                            else:
                                print(get_text("text_1354"))
                                print(get_text("text_1355"))
                                game_over = True
                                game_back = True
                                break
                        elif torch == True:
                            print(get_text("text_1356"))
                            print(get_text("text_1357"))
                            print(get_text("text_1358"))
                            current_room = "cave"
                            cave()
                            if game_over == True:
                                print(get_text("text_1359"))
                                print(get_text("text_1360"))
                                while True:
                                    c = input()
                                    if c == 'menu':
                                        main()
                                        return
                        elif light == True or force_in_cave:
                            print(get_text("text_1361"))
                            print(get_text("text_1362"))
                            current_room = "cave"
                            cave()
                            if game_over == True:
                                print(get_text("text_1363"))
                                print(get_text("text_1364"))
                                while True:
                                    c = input()
                                    if c == 'menu':
                                        main()
                                        return  
                    elif tele == 'down':
                        if 'rope' in have_list:
                            print(get_text("text_1365"))
                            break
                        else:
                            print(get_text("text_1366"))
                            print(get_text("text_1367"))
                            game_over = True
                            game_back = True
                            break
                    elif tele == 'place runes':
                        if rune1 and rune2 and rune3:
                            good = good - evil
                            print(get_text("text_1368"))
                            if play_count == 1:
                                print(get_text("text_1369"))
                            elif play_count == 2:
                                print(get_text("text_1370"))
                            while True:
                                c = input()
                                if c == 'seal':
                                    if good >= 10:
                                        print(get_text("text_1371"))
                                        print(get_text("text_1372"))
                                        if grave_diary_read == True:
                                            print(get_text("text_1373"))
                                            print(get_text("text_1374"))
                                            print(get_text("text_1375"))
                                        else:
                                            print(get_text("text_1376"))
                                            print(get_text("text_1377"))
                                        game_over = True
                                        game_back = True
                                        cleared_ending = True
                                        break
                                    else:
                                        print(get_text("text_1378"))
                                elif c == 'unleash':
                                    if play_count == 2:
                                        if good >= 20:
                                            print(get_text("text_1379"))
                                            print(get_text("text_1380"))
                                            print(get_text("text_1381"))
                                            game_over = True
                                            game_back = True
                                            cleared_ending = True
                                            break
                                        else:
                                            print(get_text("text_1382"))
                                    elif play_count == 1:
                                        print(get_text("text_1383"))
                                elif c == 'leave':
                                    if play_count == 2:
                                        print(get_text("text_1384"))
                                        print(get_text("text_1385"))
                                        game_over = True
                                        cleared_ending = True
                                        break
                                    elif play_count == 1:
                                        print(get_text("text_1386"))
                                        print(get_text("text_1387"))
                                        game_over = True
                                        game_back = True
                                        cleared_ending = True
                                        break
                                elif c == 'release':
                                    print(get_text("text_1388"))
                                    print(get_text("text_1389"))
                                    game_over = True
                                    game_back = True
                                    cleared_ending = True
                                    break
                                elif c == 'talk':
                                    if grave_diary_read == True and old_diary_readed == True and good >= 20:
                                        print(get_text("text_1390"))
                                        print(get_text("text_1391"))
                                        print(get_text("text_1392"))
                                        game_over = True
                                        game_back = True
                                        cleared_ending = True
                                        break
                                    else:
                                        print(get_text("text_1393"))
                                elif c == 'absorb':
                                    print(get_text("text_1394"))
                                    print(get_text("text_1395"))
                                    print(get_text("text_1396"))
                                    amulet = True
                                    hp = 99
                                    game_over = True
                                    game_back = True
                                    cleared_ending = True
                                    break
                                elif c == 'sacrifice':
                                    print(get_text("text_1397"))
                                    print(get_text("text_1398"))
                                    print(get_text("text_1399"))
                                    game_over = True
                                    game_back = True
                                    cleared_ending = True
                                    break
                                elif c == 'symbiosis':
                                    if good >= 5:
                                        print(get_text("text_1400"))
                                        print(get_text("text_1401"))
                                        print(get_text("text_1402"))
                                        game_over = True
                                        game_back = True
                                        cleared_ending = True
                                        break
                                    else:
                                        print(get_text("text_1403"))
                                elif c == 'truth':
                                    if play_count == 2:
                                        if 'a magic key' in have_list:
                                            print(get_text("text_1404"))
                                            print(get_text("text_1405"))
                                            print(get_text("text_1406"))
                                            print(get_text("text_1407"))
                                        else:
                                            print(get_text("text_1408"))
                                            print(get_text("text_1409"))
                                    elif play_count == 1:
                                        print(get_text("text_1410"))
                                    game_over = True
                                    game_back = True
                                    cleared_ending = True
                                    break
                                elif c == 'break curse':
                                    if 'a magic key' in have_list and play_count == 2:
                                        if good >= 25:
                                            print(get_text("text_1411"))
                                            print(get_text("text_1412"))
                                            print(get_text("text_1413"))
                                            print(get_text("text_1414"))
                                            game_over = True
                                            game_back = True
                                            cleared_ending = True
                                            break
                                        else:
                                            print(get_text("text_1415"))
                                    else:
                                        print(get_text("text_1416"))
                                else:
                                    print(get_text("text_1417"))
                                if force_over == True:
                                    break
                            if game_over:
                                print(get_text("text_1418"))
                                print(get_text("text_1419"))
                                while True:
                                    c = input()
                                    if c == 'menu':
                                        main()
                                        return
                        else:
                            print(get_text("text_1420"))
                        if force_over == True:
                            break
                    elif tele == 'woody':
                        if light == True:
                            print(get_text("text_1421"))
                            secret_unlocked = True
                        else:
                            print(get_text("text_1422"))
                    elif tele == 'bag':
                        for i in range(len(have_list)):
                            print(have_list[i])
                    else:
                        print(get_text("text_1423"))
                    if force_over == True:
                        break
                if force_over == True:
                    break
            if force_over == True:
                break
        elif go == "help":
            print(get_text("text_1424"))
            print(get_text("text_1425"))
            print(get_text("text_1426"))
            print(get_text("text_1427"))
            print(get_text("text_1428"))
            print(get_text("text_1429"))
            print("tomb - Enter tomb (New Game+ only)")
            print(get_text("text_1430"))
            print(get_text("text_1431"))
            print(get_text("text_1432"))
            print(get_text("text_1433"))
            print(get_text("text_1434"))
        elif go == 'down' or go == 'go down':
            if festival_mode:
                if three_hole_in == False:
                    full_moon_maze()
                else:
                    print(get_text("text_1435"))
            else:
                print(get_text("text_1436"))
        elif go == 'load':
            load_game()
        elif go == 'save':
            save_game()
        elif go == "journal":
            show_journal()
        elif go == 'dev':
            if play_count == 1:
                developer_room()
            else:
                print(get_text("text_1437"))
        desktop_path = os.path.expanduser("~/Desktop")
        try:
            real_files = os.listdir(desktop_path)
            real_item = random.choice(real_files) if real_files else "unknown_file.txt"
        except:
            real_item = "a file from your desktop"

        if go == "bag" and death_count >= 2 and random.randint(1, 2) == 1:
            for item in have_list:
                print(item)
            print(real_item)
            time.sleep(1.5)
            jump_scare_face('flash')
            print(get_text("text_1438"))
        elif go == "examine corpse" or go == 'corpse' or go == 'search corpse' or go == 'find corpse':
            if has_death_corpse and death_location == current_room:
                print(get_text("text_1439"))
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print(get_text("text_1440"))
                has_death_corpse = False
            else:
                print(get_text("text_1441"))
        elif go == 'hp':
            print('HP:', hp)
        elif go == 'bag':
            for i in range(len(have_list)):
                print(have_list[i])
        elif go == 'map':
            print("""WORLD MAP
        ====================
        [Watchtower]   [Road * (You are here)]
                |
        [Merchant]      [House]
                |
        [Forest]  <-->  [Haunted Hut]
                |
        [Abandoned Camp]
                |
        [Grave]   [Tomb (NG+)]
                |
        [Misty Swamp]
                |
        [Cave -> Altar]
        ====================""")
        elif go == "moral":
            print(f"Good: {good} | Evil: {evil}")
            if good > evil:
                print(get_text("text_1442"))
            elif evil > good:
                print(get_text("text_1443"))
        elif go == "weather":
            print_weather()
        elif go == "eat":
            if "some food" in have_list:
                have_list.remove("some food")
                hp += 3
                print("You eat food. HP +3")
            else:
                print(get_text("text_1444"))

        elif go == "drink":
            if "some water in the bottle" in have_list:
                have_list.remove("some water in the bottle")
                hp += 2
                print("You drink water. HP +2")
            else:
                print(get_text("text_1445"))
        elif go == 'north':
            tower_check = input(get_text("input_1446"))
            if tower_check == "fort":
                military_fort()
                continue
            elif tower_check == "tower":
                watchtower()
                continue
            elif tower_check == 'merchant':
                print(get_text("text_1447"))
                print(get_text("text_1448"))
                print(get_text("text_1449"))
                if args.godmode:
                    print(get_text("text_1450"))
                while True:
                    m = input(get_text("input_1451"))
                    if m == 'trade food':
                        if 'some food' in have_list:
                            have_list.remove('some food')
                            have_list.append('super amulet')
                            amulet = True
                            print(get_text("text_1452"))
                    elif m == 'trade water':
                        if 'a bottle' in have_list:
                            have_list.remove('a bottle')
                            torch = True
                            light = True
                            print(get_text("text_1453"))
                    elif m == "stare":
                        print(get_text("text_1454"))
                    elif m == 'attack merchant' or m == 'kill merchant' or m == 'attack him' or m == 'kill him' or m == 'fight him' or m == 'fight merchant':
                        print(get_text("text_1455"))
                        evil += 5
                    elif m == "wave hand":
                        print(get_text("text_1456"))
                    elif m == "nod":
                        print(get_text("text_1457"))
                    elif m == "copy move":
                        print(get_text("text_1458"))
                    elif m == "pretend to cry":
                        print(get_text("text_1459"))
                    elif m == "dance together":
                        print(get_text("text_1460"))
                    elif m == "doze":
                        print(get_text("text_1461"))
                    elif m == "walk around":
                        print(get_text("text_1462"))
                    elif m == "complain":
                        print(get_text("text_1463"))
                    elif m == "merchant lazy":
                        print(get_text("text_1464"))
                        print(get_text("text_1465"))
                    elif m == "merchant ghost":
                        print(get_text("text_1466"))
                        print(get_text("text_1467"))
                    elif m == "merchant tired":
                        print(get_text("text_1468"))
                        print(get_text("text_1469"))
                    elif m == "arm wrestle":
                        print(get_text("text_1470"))
                    elif m == 'leave' or m == 'back' or m == 'south':
                        print(get_text("text_1471"))
                        break
                    elif m == "ask past":
                        print(get_text("text_1472"))
                        print(get_text("text_1473"))
                        print(get_text("text_1474"))
                    elif m == "talk more" or m == 'talk':
                        if merchant_story_stage == 0:
                            print(get_text("text_1475"))
                            print(get_text("text_1476"))
                            print(get_text("text_1477"))
                            good += 5
                            merchant_story_stage = 1
                        elif merchant_story_stage == 1:
                            print(get_text("text_1478"))
                            print(get_text("text_1479"))
                            merchant_story_stage = 2
                            good += 5
                        elif merchant_story_stage == 2:
                            print(get_text("text_1480"))
                            print(get_text("text_1481"))
                            good += 5
                            merchant_story_stage = 3
                        elif merchant_story_stage == 3:
                            print(get_text("text_1482"))
                            print(get_text("text_1483"))
                            if "rune1" not in have_list:
                                have_list.append("stone rune1")
                                rune1 = True
                                print(get_text("text_1484"))
                            if evil >= 0:
                                evil = 0
                            else:
                                good += 10
                            merchant_story_stage = 4
                        else:
                            print(get_text("text_1485"))
                    elif m == "ask fate":
                        print(get_text("text_1486"))
                        print(get_text("text_1487"))
                    elif m == "trade secret":
                        if play_count == 2 and grave_diary_read:
                            if "gold coins" in have_list:
                                have_list.remove("gold coins")
                                have_list.append("ancient scroll")
                                print(get_text("text_1488"))
                                print(get_text("text_1489"))
                            else:
                                print(get_text("text_1490"))
                        else:
                            print(get_text("text_1491"))
                    elif m == "trade coin" or m == 'trade coins' or m == 'trade gold coins':
                        if "gold coins" in have_list:
                            have_list.remove("gold coins")
                            hp += 10
                            print("You trade your gold coins, and your HP +10.")
                        else:
                            print(get_text("text_1492"))
                    elif m == "joke":
                        print(get_text("text_1493"))
                        print(get_text("text_1494"))
                    elif m == "pretend dead":
                        print(get_text("text_1495"))
                    elif m == "sing together":
                        print(get_text("text_1496"))
                    elif m == "point":
                        print(get_text("text_1497"))
                    elif m == "tickling":
                        print(get_text("text_1498"))
                    elif m == "dance":
                        print(get_text("text_1499"))
                        hp += 1
                    elif m == "act like ghost":
                        print(get_text("text_1500"))
                    elif m == "beg for gifts" or m == 'beg':
                        print(get_text("text_1501"))
                    elif m == "pretend sleep":
                        print(get_text("text_1502"))
                    elif m == "cheer":
                        print(get_text("text_1503"))
                    elif m == "walk side by side":
                        print(get_text("text_1504"))
                    else:
                        print(get_text("text_1505"))
            else:
                print(get_text("text_1506"))
        elif go == "statue":
            print(f"HP: {hp}")
            print(f"Time: {time_period}")
            print(f"Good: {good} | Evil: {evil}")
            print(f"New Game+: {play_count}")
        elif go == 'west':
            print(get_text("text_1507"))
            print(get_text("text_1508"))
            print(get_text("text_1509"))
            while True:
                h = input(get_text("input_1510"))
                if h == 'talk':
                    print(get_text("text_1511"))
                    print(get_text("text_1512"))
                    if grave_diary_read == True or old_diary_readed == True:
                        print(get_text("text_1513"))
                    else:
                        print(get_text("text_1514"))
                elif h == 'give diary':
                    if diary_read:
                        print('Ghost smiles! Max HP +5!')
                        hp += 5
                        good += 10
                        break
                    else:
                        print(get_text("text_1515"))
                elif festival_mode:
                    print(get_text("text_1516"))
                    hp += 2
                elif h == "ask wish":
                    print(get_text("text_1517"))
                    print(get_text("text_1518"))
                elif h == "comfort ghost":
                    if old_diary_readed and grave_diary_read:
                        print(get_text("text_1519"))
                        print(get_text("text_1520"))
                        hp += 4
                        print(get_text("text_1521"))
                    else:
                        print(get_text("text_1522"))
                elif h == "lead to cave":
                    if play_count == 2:
                        print(get_text("text_1523"))
                        print(get_text("text_1524"))
                        print(get_text("text_1525"))
                        print(get_text("text_1526"))
                        trap_protect = True
                    else:
                        print(get_text("text_1527"))
                elif h == 'leave' or h == 'east' or h == 'back':
                    print(get_text("text_1528"))
                    break
                elif h == "forgive":
                    if good >= 20:
                        print(get_text("text_1529"))
                        print(get_text("text_1530"))
                        good += 20
                elif h == 'west':
                    print(get_text("text_1531"))
                    print(get_text("text_1532"))
                    while True:
                        ch = input(get_text("input_1533"))
                        if ch == 'east' or ch == 'back' or ch == 'leave':
                            print(get_text("text_1534"))
                            break
                        elif ch == 'read stone':
                            print(get_text("text_1535"))
                            print(get_text("text_1536"))
                            print(get_text("text_1537"))
                            print(get_text("text_1538"))
                            print(get_text("text_1539"))
                            print(get_text("text_1540"))
                            print(get_text("text_1541"))
                            print(get_text("text_1542"))
                            print(get_text("text_1543"))
                            print(get_text("text_1544"))
                            grandmother = True
                            if grave_diary_read == True:
                                print(get_text("text_1545"))
                            else:
                                print(get_text("text_1546"))
                        elif ch == 'purify':
                            print(get_text("text_1547"))
                            have_list.append('holy amulet')
                            amulet = True
                        elif ch == "look bottom":
                            print(get_text("text_1548"))
                            print(get_text("text_1549"))
                            print(get_text("text_1550"))
                            if play_count == 2:
                                print(get_text("text_1551"))
                        elif ch == 'desecrate':
                            print(get_text("text_1552"))
                            have_list.append('demon claw')
                        elif ch == 'bag':
                            for i in have_list:
                                print(i)
                        else:
                            print(get_text("text_1553"))
                else:
                    print(get_text("text_1554"))
        elif go == 'east':
            print(get_text("text_1555"))
            print(get_text("text_1556"))
            while True:
                forest_take = input(get_text("input_1557"))
                if forest_take == 'read diary' or forest_take == 'take diary':
                    print(get_text("text_1558"))
                    print(get_text("text_1559"))
                    print(get_text("text_1560"))
                    print(get_text("text_1561"))
                    print(get_text("text_1562"))
                    print(get_text("text_1563"))
                    print(get_text("text_1564"))
                    print(get_text("text_1565"))
                    print(get_text("text_1566"))
                    print(get_text("text_1567"))
                    print(get_text("text_1568"))
                    print(get_text("text_1569"))
                    print(get_text("text_1570"))
                    print(get_text("text_1571"))
                    print(get_text("text_1572"))
                    print(get_text("text_1573"))
                    print(get_text("text_1574"))
                    old_diary_readed = True
                    if grave_diary_read:
                        print(get_text("text_1575"))
                        print(get_text("text_1576"))
                        print(get_text("text_1577"))
                        break
                    else:
                        print(get_text("text_1578"))
                        print(get_text("text_1579"))
                        break
                elif forest_take == 'east' or forest_take == 'go to swamp' or forest_take == 'go to misty swamp':
                    if misty_end == False:
                        misty_swamp()
                        if game_over:
                            print(get_text("text_1580"))
                            print(get_text("text_1581"))
                            while True:
                                c = input()
                                if c == 'menu':
                                    main()
                                    return
                    else:
                        print(get_text("text_1582"))
                    break
                elif forest_take == 'leave' or forest_take == 'back' or forest_take == 'west':
                    print(get_text("text_1583"))
                    break
                elif forest_take == 'climb tree':
                    x = random.randint(1,2)
                    if x == 1:
                        print(get_text("text_1584"))
                        print(get_text("text_1585"))
                        hp -= 1
                        if hp <= 0:
                            print(get_text("text_1586"))
                            game_back = True
                            game_over = True
                            break
                    else:
                        print('Luck for you, you find some delicious nut, Hp +1')
                        hp += 1
                elif forest_take == 'tree':
                    print(get_text("text_1587"))
                elif forest_take == 'cut tree':
                    cmd = input(get_text("input_1588"))
                    if cmd == 'Y' or cmd == 'y' or cmd == 'yes' or cmd == 'YES':
                        print(get_text("text_1589"))
                        print(get_text("text_1590"))
                        print(get_text("text_1591"))
                        hp -= 5
                        if hp <= 0:
                            print(get_text("text_1592"))
                            game_back = True
                            game_over = True
                            break
                        evil += 10
                    elif cmd == 'N' or cmd == 'n' or cmd == 'no' or cmd == 'NO':
                        print(get_text("text_1593"))
                    else:
                        print(get_text("text_1594"))
                elif forest_take == "talk to bird":
                    print(get_text("text_1595"))
                    if old_diary_readed:
                        print(get_text("text_1596"))
                    else:
                        print(get_text("text_1597"))
                elif forest_take == "feed bird":
                    if "some food" in have_list:
                        have_list.remove("some food")
                        print(get_text("text_1598"))
                        have_list.append("spirit feather")
                        print(get_text("text_1599"))
                elif forest_take == "wave to bird":
                    print(get_text("text_1600"))
                else:
                    print(get_text("text_1601"))
        elif go == 'south':
            print(get_text("text_1602"))
            print(get_text("text_1603"))
            print(get_text("text_1604"))
            while True:
                print(get_text("text_1605"))
                if play_count == 2:
                    print(get_text("text_1606"))
                print(get_text("text_1607"))
                if has_death_corpse and death_location == current_room:
                    print(get_text("text_1608"))
                camp_cmd = input(get_text("input_1609"))
                if camp_cmd == 'west':
                    print(get_text("text_1610"))
                    print(get_text("text_1611"))
                elif camp_cmd == "make funny face":
                    print(get_text("text_1612"))
                elif camp_cmd == 'go to hill' or camp_cmd == 'south' or camp_cmd == 'forward' or camp_cmd == 'go to south':
                    hill()
                    return
                elif camp_cmd == "count stars":
                    print(get_text("text_1613"))
                elif camp_cmd == "talk to fire":
                    print(get_text("text_1614"))
                elif camp_cmd == "jump":
                    print(get_text("text_1615"))
                elif camp_cmd == "examine corpse" or camp_cmd == 'corpse' or camp_cmd == 'search corpse' or camp_cmd == 'find corpse':
                    if has_death_corpse and death_location == current_room:
                        print(get_text("text_1616"))
                        if death_corpse_item:
                            print(f"You retrieve {death_corpse_item} from its pocket.")
                            have_list.append(death_corpse_item)
                        else:
                            print(get_text("text_1617"))
                        has_death_corpse = False
                    else:
                        print(get_text("text_1618"))
                elif camp_cmd == 'firepit':
                    if festival_mode:
                        print(get_text("text_1619"))
                        print(get_text("text_1620"))
                        hp += 2
                    if amulet == False or ng_amulet == False or has_elf_amulet == False:
                        print(get_text("text_1621"))
                        print(get_text("text_1622"))
                        game_over = True
                        game_back = True
                        break
                    elif args.godmode:
                        print(get_text("text_1623"))
                        print(get_text("text_1624"))
                        hp += 1
                    else:
                        print(get_text("text_1625"))
                elif camp_cmd == "play":
                    print(get_text("text_1626"))
                elif camp_cmd == "yell":
                    print(get_text("text_1627"))
                    print(get_text("text_1628"))
                elif camp_cmd == "tell joke":
                    print(get_text("text_1629"))
                    print(get_text("text_1630"))
                elif camp_cmd == 'search':
                    print(get_text("text_1631"))
                    have_list.append('rope')
                elif camp_cmd == 'chest':
                    print(get_text("text_1632"))
                    have_list.append('flint')
                elif camp_cmd == "tomb" or camp_cmd == 'go to tomb' or camp_cmd == 'go to the tomb':
                    if play_count == 2:
                        print("\n[NG+ ONLY] A hidden stone door slowly opens...")
                        tomb()
                    else:
                        print(get_text("text_1633"))
                elif camp_cmd == 'north':
                    print(get_text("text_1634"))
                    break
                elif camp_cmd == 'east':
                    print(get_text("text_1635"))
                    if festival_mode:
                        print(get_text("text_1636"))
                        hp += 2
                    else:
                        print(get_text("text_1637"))
                    print(get_text("text_1638"))
                    print(get_text("text_1639"))
                    have_list.append('super amulet')
                    amulet = True
                elif camp_cmd == 'back' or camp_cmd == 'leave':
                    print(get_text("text_1640"))
                    break
                elif camp_cmd == 'cliff':
                    print(get_text("text_1641"))
                elif camp_cmd == 'climb down':
                    if 'rope' in have_list:
                        print(get_text("text_1642"))
                        print(get_text("text_1643"))
                        current_room = "cave"
                        cave()
                        if game_over:
                            print(get_text("text_1644"))
                            print(get_text("text_1645"))
                            while True:
                                c = input()
                                if c == 'menu':
                                    main()
                                    return
                    else:
                        print(get_text("text_1646"))
                elif camp_cmd == 'bag':
                    for i in have_list:
                        print(i)
                elif camp_cmd == 'search grave':
                    if rune2 == False:
                        print(get_text("text_1647"))
                        print(get_text("text_1648"))
                        rune2 = True
                        have_list.append('rune stone 2')
                    else:
                        print(get_text("text_1649"))
                elif camp_cmd == 'dig grave':
                    print(get_text("text_1650"))
                    choice = input()
                    if choice == 'take':
                        print(get_text("text_1651"))
                        have_list.append('a diamond')
                        evil += 15
                        print(get_text("text_1652"))
                        print(get_text("text_1653"))
                        print(get_text("text_1654"))
                        print(get_text("text_1655"))
                        print(get_text("text_1656"))
                        print(get_text("text_1657"))
                        print(get_text("text_1658"))
                        print(get_text("text_1659"))
                        print(get_text("text_1660"))
                        print(get_text("text_1661"))
                        print(get_text("text_1662"))
                        print(get_text("text_1663"))
                        print(get_text("text_1664"))
                        print(get_text("text_1665"))
                        print(get_text("text_1666"))
                        print(get_text("text_1667"))
                        print(get_text("text_1668"))
                        grave_diary_read = True
                    elif choice == 'leave':
                        print(get_text("text_1669"))
                        good += 20
                        print(get_text("text_1670"))
                        print(get_text("text_1671"))
                        print(get_text("text_1672"))
                        print(get_text("text_1673"))
                        print(get_text("text_1674"))
                        print(get_text("text_1675"))
                        print(get_text("text_1676"))
                        print(get_text("text_1677"))
                        print(get_text("text_1678"))
                        print(get_text("text_1679"))
                        print(get_text("text_1680"))
                        print(get_text("text_1681"))
                        print(get_text("text_1682"))
                        print(get_text("text_1683"))
                        print(get_text("text_1684"))
                        print(get_text("text_1685"))
                        print(get_text("text_1686"))
                        grave_diary_read = True
                    else:
                        print(get_text("text_1687"))
                else:
                    print(get_text("text_1688"))
        else:
            print(get_text("text_1689"))
        if game_over == True:
            print(get_text("text_1690"))
            print(get_text("text_1691"))
            while True:
                c = input()
                if c == 'menu':
                    main()
                    return
        if force_over == True:
            break

def ng_three():
    global m1, m2, m3,cleared_ending
    m1 = False
    m2 = False
    m3 = False
    
    print(get_text("text_1692"))
    print(get_text("text_1693"))
    print(get_text("text_1694"))
    print(get_text("text_1695"))
    print(get_text("text_1696"))
    print(get_text("text_1697"))
    
    while True:
        print(get_text("text_1698"))
        print(get_text("text_1699"))
        print(get_text("text_1700"))
        if m1 and m2:
            print(get_text("text_1701"))
        if m3:
            print(get_text("text_1702"))
        print(get_text("text_1703"))
        
        opt = input(get_text("input_1704"))
        
        if opt == "1":
            print(get_text("text_1705"))
            print(get_text("text_1706"))
            print(get_text("text_1707"))
            print(get_text("text_1708"))
            print(get_text("text_1709"))
            print(get_text("text_1710"))
            print(get_text("text_1711"))
            print(get_text("text_1712"))
            print(get_text("text_1713"))
            print(get_text("text_1714"))
            print(get_text("text_1715"))
            m1 = True
        
        elif opt == "2":
            print(get_text("text_1716"))
            print(get_text("text_1717"))
            print(get_text("text_1718"))
            print(get_text("text_1719"))
            print(get_text("text_1720"))
            print(get_text("text_1721"))
            print(get_text("text_1722"))
            print(get_text("text_1723"))
            m2 = True
        
        elif opt == "3" and m1 and m2:
            print(get_text("text_1724"))
            print(get_text("text_1725"))
            print(get_text("text_1726"))
            print(get_text("text_1727"))
            print(get_text("text_1728"))
            print(get_text("text_1729"))
            m3 = True
        
        elif opt == "4" and m3:
            print(get_text("text_1730"))
            print(get_text("text_1731"))
            print(get_text("text_1732"))
            print(get_text("text_1733"))
            print(get_text("text_1734"))
            print(get_text("text_1735"))
            print(get_text("text_1736"))
            print(get_text("text_1737"))
            e = input(get_text("input_1738"))
            if e == "1":
                print(get_text("text_1739"))
                print(get_text("text_1740"))
                print(get_text("text_1741"))
                print(get_text("text_1742"))
                print(get_text("text_1743"))
                print(get_text("text_1744"))
                cleared_ending = True
                main()
                return
            elif e == "2":
                print(get_text("text_1745"))
                print(get_text("text_1746"))
                print(get_text("text_1747"))
                print(get_text("text_1748"))
                print(get_text("text_1749"))
                print(get_text("text_1750"))
                cleared_ending = True
                main()
                return
            elif e == "3":
                print(get_text("text_1751"))
                print(get_text("text_1752"))
                print(get_text("text_1753"))
                print(get_text("text_1754"))
                print(get_text("text_1755"))
                print(get_text("text_1756"))
                cleared_ending = True
                main()
                return
            elif e == "4":
                print(get_text("text_1757"))
                print(get_text("text_1758"))
                print(get_text("text_1759"))
                print(get_text("text_1760"))
                print(get_text("text_1761"))
                print(get_text("text_1762"))
                print(get_text("text_1763"))
                cleared_ending = True
                main()
                return
        elif opt == "5":
            print(get_text("text_1764"))
            break
# main menu
def menu():

    global force_over

    print(get_text("text_1765"))
    print(get_text("text_1766"))
    if play_count == 3:
        print(get_text("text_1767"))
    while True:
        print(get_text("text_1768"))
        if play_count == 3:
            start = input(get_text("input_1769"))
        elif play_count == 4:
            start = input(get_text("input_1770"))
        else:
            start = input(get_text("input_1771"))
        if play_count != 4:
            if start == 'start':
                print(get_text("text_1772"))
                if play_count <= 2:
                    print(get_text("text_1773"))
                    print(get_text("text_1774"))
                    gamestart()
                elif play_count == 3:
                    print(get_text("text_1775"))
                    print(get_text("text_1776"))
                    ng_three()
            elif start == 'quit':
                if play_count <= 4:
                    print(get_text("text_1777"))
                    print(get_text("text_1778"))
                    print(get_text("text_1779"))
                    print(get_text("text_1780"))
                    exit()
                else:
                    show_message_wall()
                    name = input(get_text("input_1781"))
                    msg = input(get_text("input_1782"))
                    save_message(name, msg)
                    print(get_text("text_1783"))
                    print(get_text("text_1784"))
                    print(get_text("text_1785"))
                    print(get_text("text_1786"))
                    print(get_text("text_1787"))
                    print(get_text("text_1788"))
                    print(get_text("text_1789"))
                    print(get_text("text_1790"))
                    print(get_text("text_1791"))
                    print(get_text("text_1792"))
                    print(get_text("text_1793"))
                    print(get_text("text_1794"))
                    print(get_text("text_1795"))
                    exit()   
            elif start == "time" or start == 'time travel':
                if play_count == 3:
                    time_travel_origin()
                else:
                    print(get_text("text_1796"))
            elif start == 'task':
                if play_count <= 2:
                    print(get_text("text_1797"))
                    print(get_text("text_1798"))
                    print(get_text("text_1799"))
                    print(get_text("text_1800"))
                    print(get_text("text_1801"))
                    print(get_text("text_1802"))
                else:
                    print(get_text("text_1803"))
        elif play_count == 4:
            if start == 'heaven':
                print_heaven()
            elif start == 'quit':
                print(get_text("text_1804"))
                print(get_text("text_1805"))
                print(get_text("text_1806"))
                print(get_text("text_1807"))
                exit()
            
        else:
            print(get_text("text_1808"))
# main
def main():
    global have_list, game_over, light, hp, l, k, n, s, f, w, p, sc, secret_unlocked, map_unlocked, amulet, turn_count, chain1, chain2, diary_read, legacy_unlocked, new_game_plus, ng_amulet, ng_compass, ng_diary, current_room, torch, no_light_run, all_collected, rune1, rune2, rune3, faith, sky, moon, trap_protect, rune, grandmother, gate_unlock, old_diary_readed, grave_diary_read, force_over, game_back, play_count, tomb_unlocked, old_note_readed,cleared_ending,time_period,step_count,death_count,good,evil,death_corpse_item,death_location,has_death_corpse,one_hole_in,two_hole_in,three_hole_in,four_hole_in
    today = datetime.date.today()
    m = today.month
    d = today.day

    if m == 1:
        if d == 1:
            print(get_text("text_1809"))
            print(get_text("text_1810"))
            print(get_text("text_1811"))
            print(get_text("text_1812"))
            hp = 8
            good += 8
        elif d == 14:
            print(get_text("text_1813"))
            print(get_text("text_1814"))
            print(get_text("text_1815"))
            print(get_text("text_1816"))
            diary_read = True
            have_list.append("ancient diary")
        elif d == 21:
            print(get_text("text_1817"))
            print(get_text("text_1818"))
            print(get_text("text_1819"))
            print(get_text("text_1820"))
            good += 12
            hp += 4
        elif d == 26:
            print(get_text("text_1821"))
            print(get_text("text_1822"))
            print(get_text("text_1823"))
            print(get_text("text_1824"))
            evil -= 5
            torch = True
        elif d == 31:
            print(get_text("text_1825"))
            print(get_text("text_1826"))
            print(get_text("text_1827"))
            print(get_text("text_1828"))
            have_list.append("shadow whisper")
            faith += 6

    elif m == 2:
        if d == 2:
            print(get_text("text_1829"))
            print(get_text("text_1830"))
            print(get_text("text_1831"))
            print(get_text("text_1832"))
            hp += 5
        elif d == 14:
            print(get_text("text_1833"))
            print(get_text("text_1834"))
            print(get_text("text_1835"))
            print(get_text("text_1836"))
            good += 10
        elif d == 17:
            print(get_text("text_1837"))
            print(get_text("text_1838"))
            print(get_text("text_1839"))
            print(get_text("text_1840"))
            have_list.append("lucky clover")
        elif d == 20:
            print(get_text("text_1841"))
            print(get_text("text_1842"))
            print(get_text("text_1843"))
            print(get_text("text_1844"))
            evil -= 8
            good += 5
        elif d == 28:
            print(get_text("text_1845"))
            print(get_text("text_1846"))
            print(get_text("text_1847"))
            print(get_text("text_1848"))
            light = True
            have_list.append("eternal flame")

    elif m == 3:
        if d == 4:
            print(get_text("text_1849"))
            print(get_text("text_1850"))
            print(get_text("text_1851"))
            print(get_text("text_1852"))
            faith += 7
        elif d == 14:
            print(get_text("text_1853"))
            print(get_text("text_1854"))
            print(get_text("text_1855"))
            print(get_text("text_1856"))
            good += 9
        elif d == 17:
            print(get_text("text_1857"))
            print(get_text("text_1858"))
            print(get_text("text_1859"))
            print(get_text("text_1860"))
            hp += 6
        elif d == 20:
            print(get_text("text_1861"))
            print(get_text("text_1862"))
            print(get_text("text_1863"))
            print(get_text("text_1864"))
            good += 7
            evil -= 7
        elif d == 31:
            print(get_text("text_1865"))
            print(get_text("text_1866"))
            print(get_text("text_1867"))
            print(get_text("text_1868"))
            have_list.append("ghost companion")

    elif m == 4:
        if d == 1:
            print(get_text("text_1869"))
            print(get_text("text_1870"))
            print(get_text("text_1871"))
            print(get_text("text_1872"))
            have_list.append("trickster mask")
        elif d == 14:
            print(get_text("text_1873"))
            print(get_text("text_1874"))
            print(get_text("text_1875"))
            print(get_text("text_1876"))
            evil += 5
        elif d == 15:
            print(get_text("text_1877"))
            print(get_text("text_1878"))
            print(get_text("text_1879"))
            print(get_text("text_1880"))
            evil -= 10
        elif d == 22:
            print(get_text("text_1881"))
            print(get_text("text_1882"))
            print(get_text("text_1883"))
            print(get_text("text_1884"))
            hp += 7
        elif d == 30:
            print(get_text("text_1885"))
            print(get_text("text_1886"))
            print(get_text("text_1887"))
            print(get_text("text_1888"))
            have_list.append("ghost essence")

    elif m == 5:
        if d == 5:
            print(get_text("text_1889"))
            print(get_text("text_1890"))
            print(get_text("text_1891"))
            print(get_text("text_1892"))
            good += 8
        elif d == 14:
            print(get_text("text_1893"))
            print(get_text("text_1894"))
            print(get_text("text_1895"))
            print(get_text("text_1896"))
            good += 10
        elif d == 20:
            print(get_text("text_1897"))
            print(get_text("text_1898"))
            print(get_text("text_1899"))
            print(get_text("text_1900"))
            have_list.append("thunder core")
        elif d == 25:
            print(get_text("text_1901"))
            print(get_text("text_1902"))
            print(get_text("text_1903"))
            print(get_text("text_1904"))
            faith += 8
        elif d == 31:
            print(get_text("text_1905"))
            print(get_text("text_1906"))
            print(get_text("text_1907"))
            print(get_text("text_1908"))
            have_list.append("spirit bond")

    elif m == 6:
        if d == 1:
            print(get_text("text_1909"))
            print(get_text("text_1910"))
            print(get_text("text_1911"))
            have_list.append('silly candy')
            print(get_text("text_1912"))
        if d == 6:
            print(get_text("text_1913"))
            print(get_text("text_1914"))
            print(get_text("text_1915"))
            print(get_text("text_1916"))
            evil -= 6
        elif d == 14:
            print(get_text("text_1917"))
            print(get_text("text_1918"))
            print(get_text("text_1919"))
            print(get_text("text_1920"))
            good += 7
        elif d == 21:
            print(get_text("text_1921"))
            print(get_text("text_1922"))
            print(get_text("text_1923"))
            print(get_text("text_1924"))
            hp += 8
        elif d == 24:
            print(get_text("text_1925"))
            print(get_text("text_1926"))
            print(get_text("text_1927"))
            print(get_text("text_1928"))
            torch = True
        elif d == 30:
            print(get_text("text_1929"))
            print(get_text("text_1930"))
            print(get_text("text_1931"))
            print(get_text("text_1932"))
            diary_read = True
            old_diary_readed = True
            old_note_readed = True

    elif m == 7:
        if d == 7:
            print(get_text("text_1933"))
            print(get_text("text_1934"))
            print(get_text("text_1935"))
            print(get_text("text_1936"))
            faith += 10
        elif d == 15:
            print(get_text("text_1937"))
            print(get_text("text_1938"))
            print(get_text("text_1939"))
            print(get_text("text_1940"))
            have_list.append("ancestor blessing")
            good += 12
        elif d == 20:
            print(get_text("text_1941"))
            print(get_text("text_1942"))
            print(get_text("text_1943"))
            print(get_text("text_1944"))
            evil -= 10
        elif d == 25:
            print(get_text("text_1945"))
            print(get_text("text_1946"))
            print(get_text("text_1947"))
            print(get_text("text_1948"))
            have_list.append("crystal light")
        elif d == 31:
            print(get_text("text_1949"))
            print(get_text("text_1950"))
            print(get_text("text_1951"))
            print(get_text("text_1952"))
            have_list.append("shadow story")

    elif m == 8:
        if d == 8:
            print(get_text("text_1953"))
            print(get_text("text_1954"))
            print(get_text("text_1955"))
            print(get_text("text_1956"))
            good += 8
        elif d == 15:
            print(get_text("text_1957"))
            print(get_text("text_1958"))
            print(get_text("text_1959"))
            print(get_text("text_1960"))
            hp += 4
            amulet = True
        elif d == 20:
            print(get_text("text_1961"))
            print(get_text("text_1962"))
            print(get_text("text_1963"))
            print(get_text("text_1964"))
            have_list.append("harvest fruit")
        elif d == 25:
            print(get_text("text_1965"))
            print(get_text("text_1966"))
            print(get_text("text_1967"))
            print(get_text("text_1968"))
            faith += 7
        elif d == 31:
            print(get_text("text_1969"))
            print(get_text("text_1970"))
            print(get_text("text_1971"))
            print(get_text("text_1972"))
            good += 6

    elif m == 9:
        if d == 9:
            print(get_text("text_1973"))
            print(get_text("text_1974"))
            print(get_text("text_1975"))
            print(get_text("text_1976"))
            have_list.append("ancient scroll")
        elif d == 14:
            print(get_text("text_1977"))
            print(get_text("text_1978"))
            print(get_text("text_1979"))
            print(get_text("text_1980"))
            good += 8
        elif d == 22:
            print(get_text("text_1981"))
            print(get_text("text_1982"))
            print(get_text("text_1983"))
            print(get_text("text_1984"))
            good += 7
            evil -= 7
        elif d == 27:
            print(get_text("text_1985"))
            print(get_text("text_1986"))
            print(get_text("text_1987"))
            print(get_text("text_1988"))
            amulet = True
        elif d == 30:
            print(get_text("text_1989"))
            print(get_text("text_1990"))
            print(get_text("text_1991"))
            print(get_text("text_1992"))
            faith += 8

    elif m == 10:
        if d == 1:
            print(get_text("text_1993"))
            print(get_text("text_1994"))
            print(get_text("text_1995"))
            print(get_text("text_1996"))
            hp += 5
        elif d == 15:
            print(get_text("text_1997"))
            print(get_text("text_1998"))
            print(get_text("text_1999"))
            print(get_text("text_2000"))
            have_list.append("shadow dance")
        elif d == 20:
            print(get_text("text_2001"))
            print(get_text("text_2002"))
            print(get_text("text_2003"))
            print(get_text("text_2004"))
            diary_read = True
            old_note_readed = True
            old_diary_readed = True
        elif d == 25:
            print(get_text("text_2005"))
            print(get_text("text_2006"))
            print(get_text("text_2007"))
            print(get_text("text_2008"))
            light = True
        elif d == 31:
            print(get_text("text_2009"))
            print(get_text("text_2010"))
            print(get_text("text_2011"))
            print(get_text("text_2012"))
            hp += 3
            good += 5
            evil -= 3
    elif m == 11:
        if d == 1:
            print(get_text("text_2013"))
            print(get_text("text_2014"))
            print(get_text("text_2015"))
            print(get_text("text_2016"))
            good += 10
        elif d == 2:
            print(get_text("text_2017"))
            print(get_text("text_2018"))
            print(get_text("text_2019"))
            print(get_text("text_2020"))
            faith += 10
        elif d == 11:
            print(get_text("text_2021"))
            print(get_text("text_2022"))
            print(get_text("text_2023"))
            print(get_text("text_2024"))
            hp += 7
        elif d == 20:
            print(get_text("text_2025"))
            print(get_text("text_2026"))
            print(get_text("text_2027"))
            print(get_text("text_2028"))
            have_list.append("misty veil")
        elif d == 30:
            print(get_text("text_2029"))
            print(get_text("text_2030"))
            print(get_text("text_2031"))
            print(get_text("text_2032"))
            good += 8

    elif m == 12:
        if d == 5:
            print(get_text("text_2033"))
            print(get_text("text_2034"))
            print(get_text("text_2035"))
            print(get_text("text_2036"))
            hp += 4
        elif d == 15:
            print(get_text("text_2037"))
            print(get_text("text_2038"))
            print(get_text("text_2039"))
            print(get_text("text_2040"))
            faith += 10
        elif d == 22:
            print(get_text("text_2041"))
            print(get_text("text_2042"))
            print(get_text("text_2043"))
            print(get_text("text_2044"))
            hp += 6
        elif d == 25:
            print(get_text("text_2045"))
            print(get_text("text_2046"))
            print(get_text("text_2047"))
            print(get_text("text_2048"))
            hp += 5
            have_list.append("christmas candy")
        elif d == 31:
            print(get_text("text_2049"))
            print(get_text("text_2050"))
            print(get_text("text_2051"))
            print(get_text("text_2052"))
            hp = 15
            good += 10
            evil -= 5
            diary_read = True
            old_diary_readed = True
            old_note_readed = True
    game_over = False
    force_over = False
    if play_count == 3:
        play_count = 4
    if play_count == 2 and cleared_ending == True:
        play_count = 3
    if play_count == 4:
        print(get_text("text_2053"))
        print(get_text("text_2054"))
    if game_back == False:
        if not args.godmode:
            print(get_text("text_2055"))
            print(get_text("text_2056"))
            print(get_text("text_2057"))
        else:
            print(get_text("text_2058"))
            print(get_text("text_2059"))
            print(get_text("text_2060"))
            print(get_text("text_2061"))
            print(get_text("text_2062"))
        if args.godmode:
            hp = 999
            trap_protect = True
            rune1 = True
            rune2 = True
            rune3 = True
            diary_read = True
            old_diary_readed = True
            old_note_readed = True
            light = True
            grave_diary_read = True
            have_list.append('rope')
            have_list.append('ghost sword')
            have_list.append('gold coins')
            have_list.append('a pick-axe')
            have_list.append('super amulet')
            have_list.append('holy amulet')
            amulet = True
            map_unlocked = True
            print(get_text("text_2063"))
            menu()
        if args.cheat:
            have_list.extend(["a lamp", "a key", "a pick-axe", "super amulet", "ghost sword", "gold coins"])
            hp = 999
            map_unlocked = True
            secret_unlocked = True
            rune1 = rune2 = rune3 = True
            trap_protect = True
            torch = True
            print(get_text("text_2064"))
            menu()
        menu()
    elif game_back == True:
        if cleared_ending == True:
            if play_count == 2:
                if args.godmode:
                    pass
                else:
                    have_list = []
                light = False
                hp = 5
                l = 'a lamp, '
                k = 'a key, '
                n = 'a note, '
                s = 'a high altar, '
                f = 'some food, '
                w = ' and a bottle of water '
                p = 'a pick-axe'
                sc = 'a scroll, '
                secret_unlocked = False
                map_unlocked = False
                amulet = False
                turn_count = 0
                chain1 = False
                chain2 = False
                diary_read = False
                legacy_unlocked = False
                new_game_plus = False
                ng_amulet = False
                ng_compass = False
                ng_diary = False
                current_room = "road"
                torch = False
                no_light_run = False
                all_collected = False
                rune1 = False
                rune2 = False
                rune3 = False
                faith = 0
                sky = False
                moon = False
                trap_protect = False
                rune = 'a rune'
                grandmother = False
                gate_unlock = False
                old_diary_readed = False
                grave_diary_read = False
                tomb_unlocked = False
                old_note_readed = False
                print(get_text("text_2065"))
                print(get_text("text_2066"))
                print(get_text("text_2067"))
                print(get_text("text_2068"))
                print(get_text("text_2069"))
                print(get_text("text_2070"))
                print(get_text("text_2071"))
                print(get_text("text_2072"))
                print(get_text("text_2073"))
                print(get_text("text_2074"))
                print(get_text("text_2075"))
                print(get_text("text_2076"))
                menu()
            elif play_count == 3:
                print(get_text("text_2077"))
                print(get_text("text_2078"))
                print(get_text("text_2079"))
        else:
            print(get_text("text_2080"))
            print(get_text("text_2081"))
            if len(have_list) > 0:
                death_corpse_item = random.choice(have_list)
            else:
                death_corpse_item = ""
            one_hole_in = False
            two_hole_in = False
            three_hole_in = False
            four_hole_in = False
            death_location = current_room
            has_death_corpse = True
            have_list = []
            game_over = False
            light = False
            hp = 5
            l = 'a lamp, '
            k = 'a key, '
            n = 'a note, '
            s = 'a high altar, '
            f = 'some food, '
            w = ' and a bottle of water'
            p = 'a pick-axe'
            sc = 'a scroll, '
            secret_unlocked = False
            map_unlocked = False
            amulet = False
            turn_count = 0
            chain1 = False
            chain2 = False
            diary_read = False
            legacy_unlocked = False
            new_game_plus = False
            ng_amulet = False
            ng_compass = False
            ng_diary = False
            current_room = "road"
            torch = False
            no_light_run = False
            all_collected = False
            rune1 = False
            rune2 = False
            rune3 = False
            faith = 0
            sky = False
            moon = False
            trap_protect = False
            rune = 'a rune'
            grandmother = False
            gate_unlock = False
            old_diary_readed = False
            grave_diary_read = False
            force_over = False
            game_back = False
            tomb_unlocked = False
            old_note_readed = False
            map_unlocked = False
            cleared_ending = False
            play_count = 1
            time_period = "day"
            step_count = 0

            # Morality System
            good = 0
            evil = 0
            death_count += 1
            if death_count == 3:
                print(get_text("text_2082"))
                print(get_text("text_2083"))
            if death_count == 5:
                print(get_text("text_2084"))
                print('Hp +5 in case of you die again.')
                hp += 5
            if death_count >= 8 and death_count < 10:
                 print(get_text("text_2085"))
                 print('Hp +10 and you can trap protect in case you finally become part of ghost.')
                 hp += 10
                 trap_protect = True
            if death_count >= 10:
                print(get_text("text_2086"))
                print(get_text("text_2087"))
                print(get_text("text_2088"))
                print(get_text("text_2089"))
                print(get_text("text_2090"))
                exit()
            menu()
    if force_over == True:
        return

if __name__ == '__main__':
    main()