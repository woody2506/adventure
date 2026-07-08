import random
import json
import os
import time
import datetime
import argparse
import getpass
import subprocess
import tempfile


permanent_points = 0
perm_hp_bonus = 0
perm_sanity_bonus = 0
perm_start_light = False
perm_start_rope = False
perm_start_amulet = False

fort_gears_solved = False
fort_captain_saved = False
fort_logs_found = 0

werewolf_cleansed = False
werewolf_pelt_obtained = False

swamp_witch_defeated = False
swamp_witch_helped = False

ultimate_ending_unlocked = False

achievement_list = {
    "first_death": "First Blood",
    "clear_ng1": "First Cycle",
    "clear_ng2": "Curse Breaker",
    "all_runes": "Seal Scholar",
    "full_good": "Pure Heart",
    "full_evil": "Dark Lord",
    "no_death_run": "Unscathed",
    "kill_werewolf": "Moon Slayer",
    "all_endings": "Master of Fates",
    "meta_ending": "Beyond the Code"
}
achievements = {}

daily_challenge_today = ""
daily_challenge_active = False
daily_modifier = {}

mod_enabled = False
mod_items = {}
mod_events = {}
skill_uses_remaining = 2
defeated_werewolf = False
session_start_time = time.time()
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
hill_diary_read = False
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
x2 = None
sanity = 100
bw = False

# Torch Durability
torch_durability = 20
TORCH_MAX = 20

# Weapon Durability (10 attacks before breaking)
weapon_durability = 10
weapon_broken = False

# Amulet Durability System
current_amulet = "none"
amulet_durability = 0
AMULET_BASIC_MAX = 5
AMULET_HIGH_MAX = 20

player_class = "wanderer"
base_attack_bonus = 0
base_defense_bonus = 0
escape_bonus = 0
player_weapon_damage = 2
player_armor_reduction = 0

defeated_enemies = set()
npc_reputation = {
    "merchant": 0,
    "hut_ghost": 0,
    "tower_guard": 0,
    "fort_lieutenant": 0
}

ng_plus_level = 1
difficulty_scalar = 1.0

# Score System
player_total_score = 0
SCORE_SAVE_FILE = "adventure_score_save.txt"
no_death_run = True

# Military Fort - Random Password System
military_password = ""
password_attempts = 0
fort_password_locked = False
diary_fragment_1 = False
diary_fragment_2 = False
diary_fragment_3 = False
colonel_diary_collected = 0
soldier_task_done = False
lieutenant_task_done = False
fort_unlocked = False
has_military_key = False
orc_in = False

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

blood_moon = False
blood_warrior_alive = False
blood_warrior_hp = 15
blood_dungeon_cleared = False
blood_rune_hatred = False
blood_rune_agony = False
blood_rune_despair = False
blood_lord_seal_obtained = False

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
grave_take = False
sewer_in = False
grave_looted = False
church_purified = False
church_desecrated = False
swamp_quest_done = False
sewer_treasure_taken = False
explorer_thank_reward = False
tomb_pray_used = False

hunger = 20
thirst = 15

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

meta_file_tier = 0
DESKTOP_PATH = os.path.expanduser("~/Desktop")
# Hidden files on macOS start with "." -- invisible by default
META_FILENAMES = [
    ".do_not_open.txt",
    ".they_are_watching.txt",
    ".stop_playing.txt",
    ".i_know_you.txt",
    ".it_is_too_late.txt"
]

def adjust_sanity(value):
    global sanity
    sanity = max(0, min(100, sanity + value))

def get_real_username():
    try:
        return getpass.getuser()
    except:
        return "player"

class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    DARK_GRAY = '\033[90m'
    BOLD = '\033[1m'
    BLINK = '\033[5m'
    BG_RED = '\033[41m'
    BG_BLACK = '\033[40m'

def print_colored(text, color=Colors.WHITE, end='\n'):
    print(f"{color}{text}{Colors.RESET}", end=end)

def print_glitch(text, duration=0.5):
    glitch_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'
    for _ in range(3):
        garbled = ''.join(random.choice(glitch_chars) for _ in range(len(text)))
        print(garbled, end='\r')
        time.sleep(duration / 3)
    print(text)

def mac_horror_whisper(text, tier="normal"):
    voice_configs = {
        "normal":   {"voice": "Bad News",  "rate": 90,  "volume": 0.6},
        "close":    {"voice": "Whisper",   "rate": 70,  "volume": 0.8},
        "deranged": {"voice": "Deranged",  "rate": 110, "volume": 0.5},
        "demon":    {"voice": "Zarvox",    "rate": 60,  "volume": 0.9},
        "chant":    {"voice": "Cellos",    "rate": 50,  "volume": 0.7}
    }
    cfg = voice_configs.get(tier, voice_configs["normal"])
    try:
        full_text = f'[[volm {cfg["volume"]}]]{text}'
        cmd = [
            "say",
            "-v", cfg["voice"],
            "-r", str(cfg["rate"]),
            full_text
        ]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

def mac_demon_whisper(text):
    try:
        with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as f_raw:
            tmp_raw = f_raw.name
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f_final:
            tmp_final = f_final.name

        subprocess.run(
            ["say", "-v", "Zarvox", "-r", "55", "-o", tmp_raw, text],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )

        subprocess.run(
            ["sox", tmp_raw, tmp_final,
             "reverse",
             "speed", "0.7",
             "bass", "+8", "120", "0.5",
             "flanger", "0.9", "0.7", "20", "0.5", "2", "sine"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )

        subprocess.Popen(
            ["afplay", tmp_final],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        os.unlink(tmp_raw)
    except:
        mac_horror_whisper(text, "demon")

def apply_permanent_bonuses():
    global hp, sanity, light, have_list, amulet
    hp += perm_hp_bonus
    sanity += perm_sanity_bonus
    if perm_start_light:
        light = True
    if perm_start_rope:
        if "rope" not in have_list:
            have_list.append("rope")
    if perm_start_amulet:
        amulet = True
        if "super amulet" not in have_list:
            have_list.append("super amulet")

def perm_upgrade_menu():
    global permanent_points, perm_hp_bonus, perm_sanity_bonus, perm_start_light, perm_start_rope, perm_start_amulet
    if permanent_points >= 1:
        print('You feel more experienced, choose what way you want to be improved.')
        print("\n=== PERMANENT UPGRADES ===")
        print(f"Available points: {permanent_points}")
        print("1. +10 Max HP (1 point)")
        print("2. +20 Starting Sanity (1 point)")
        print("3. Start with light source (2 points)")
        print("4. Start with rope (2 points)")
        print("5. Start with super amulet (3 points)")
        print("6. Back")
        while True:
            c = input("Upgrade: ").strip().lower()
            if c == "1" and permanent_points >= 1:
                permanent_points -= 1
                perm_hp_bonus += 10
                print("Permanent HP +10 unlocked.")
            elif c == "2" and permanent_points >= 1:
                permanent_points -= 1
                perm_sanity_bonus += 20
                print("Permanent sanity +20 unlocked.")
            elif c == "3" and permanent_points >= 2:
                permanent_points -= 2
                perm_start_light = True
                print("Starting light unlocked.")
            elif c == "4" and permanent_points >= 2:
                permanent_points -= 2
                perm_start_rope = True
                print("Starting rope unlocked.")
            elif c == "5" and permanent_points >= 3:
                permanent_points -= 3
                perm_start_amulet = True
                print("Starting amulet unlocked.")
            elif c == "6" or c == "back":
                print('You go back.')
                return
            else:
                print("Invalid choice or not enough points. Maybe go back?")

def werewolf_encounter():
    global hp, game_over, game_back, player_total_score, have_list, good, evil, defeated_werewolf,player_class,skill_uses_remaining

    print("\n--- FULL MOON EVENT ---")
    print("A deep, guttural howl tears through the night.")
    print("A massive werewolf blocks the path, eyes glowing red.")
    print("It tilts its head back and howls again, calling for its pack.")
    mac_horror_whisper("Awooooooo...", "demon")
    print("\nFight or run? (1.fight / 2.run)")

    while True:
        choice = input("> ").strip().lower()
        if choice == "run" or choice == '2':
            print("You turn and flee. The werewolf does not chase.")
            hp -= 3
            print("HP -3 from exhaustion.")
            return
        elif choice == "fight" or choice == '1':
            break
        else:
            print("Invalid choice.")

    print("\nThe werewolf snarls and summons its pack!")
    print("Three feral wolves leap from the shadows.")

    for wolf_num in range(1, 4):
        if game_over:
            break
        print(f"\n--- WOLF {wolf_num} / 3 ---")
        wolf_hp = 5
        wolf_dmg = 2
        while wolf_hp > 0 and hp > 0:
            print(f"Wolf HP: {wolf_hp} | Your HP: {hp}")
            print("Actions: 1.attack / 2.defend / 3.use item")
            act = input("> ").strip().lower()

            if act == "attack" or act == '1':
                dmg = random.randint(3, 6)
                wolf_hp -= dmg
                print(f"You strike the wolf for {dmg} damage.")
                if wolf_hp > 0:
                    e_dmg = random.randint(1, wolf_dmg)
                    hp -= e_dmg
                    print(f"The wolf bites you for {e_dmg} damage.")
            elif act == "defend" or act == '2':
                e_dmg = max(0, random.randint(1, wolf_dmg) - 2)
                hp -= e_dmg
                print(f"You block. Take {e_dmg} reduced damage.")
            elif act == "use item" or act == '3':
                if "some food" in have_list:
                    have_list.remove("some food")
                    hp += 3
                    print("You eat food. HP +3")
                else:
                    print("No usable items.")
            else:
                print("Unknown action.")

            if hp <= 0:
                game_over = True
                game_back = True
                print("You are torn apart by the wolf pack.")
                mac_demon_whisper("Torn apart...")
                return

        print(f"Wolf {wolf_num} slain!")

    print("\nAll pack wolves dead. The werewolf steps forward.")
    print("=== PHASE 1: BEAST FORM ===")
    mac_demon_whisper("You will join my pack.")
    boss_hp = 40
    boss_dmg = 5
    phase_two_triggered = False

    while boss_hp > 0 and hp > 0:
        if boss_hp <= 22 and not phase_two_triggered:
            phase_two_triggered = True
            print("\n=== PHASE 2: HUMANOID FORM ===")
            print("The beast stands upright, bones cracking and shifting.")
            print("It takes human shape, claws still sharp, eyes burning with rage.")
            print("It moves faster, hits harder, and knows how you fight.")
            mac_horror_whisper("Now you die.", "deranged")
            boss_dmg = 8
        
        print(f"Werewolf HP: {boss_hp} | Your HP: {hp}")
        print("Actions: 1.attack / 2.defend / 3.skill / 4.use item")
        act = input("> ").strip().lower()

        if act == "attack" or act == '1':
            dmg = random.randint(4, 7)
            boss_hp -= dmg
            print(f"You deal {dmg} damage.")
        elif act == "defend" or act == '2':
            e_dmg = max(0, random.randint(2, boss_dmg) - 3)
            hp -= e_dmg
            print(f"You block the strike. Take {e_dmg} damage.")
            continue
        elif act == "skill" or act == '3':
            if skill_uses_remaining > 0:
                skill_uses_remaining -= 1
                if player_class == "warrior":
                    print("Shield Bash stuns the werewolf!")
                    print("It misses its next attack.")
                    boss_hp -= 5
                    continue
                elif player_class == "rogue":
                    crit_dmg = random.randint(10, 16)
                    boss_hp -= crit_dmg
                    print(f"Shadow Strike lands! {crit_dmg} damage!")
                elif player_class == "mage":
                    sanity -= 15
                    magic_dmg = random.randint(12, 18)
                    boss_hp -= magic_dmg
                    print(f"Mind Burst hits for {magic_dmg} damage.")
                elif player_class == "cleric":
                    hp += 6
                    print("Holy Light heals you for 6 HP.")
                    boss_hp -= 4
                    continue
            else:
                print('You do not have enough to use your skill.')
        elif act == "use item" or act == '4':
            if "some food" in have_list:
                have_list.remove("some food")
                hp += 3
                print("You eat food. HP +3")
            else:
                print("No usable items.")
            continue
        else:
            print("Unknown action.")
            continue

        if boss_hp > 0:
            if boss_hp >= 20:
                atk_roll == random.randint(1,4)
            else:
                atk_roll == random.radint(1.5)
            atk_roll = random.randint(1, 5)
            if atk_roll == 1 and not phase_two_triggered:
                print("The werewolf lunges and bites deep!")
                hp -= boss_dmg + 1
            elif atk_roll == 2 and phase_two_triggered:
                print("Its claws rake across your chest.")
                hp -= boss_dmg
                evil += 3
            elif atk_roll == 5:
                print('The werewolf summons for help!')
                print('Four wolves then run forward the werewolf.')
                for wolf_num in range(1, 4):
                    if game_over:
                        break
                    print(f"\n--- WOLF {wolf_num} / 3 ---")
                    wolf_hp = 5
                    wolf_dmg = 2
                    while wolf_hp > 0 and hp > 0:
                        print(f"Wolf HP: {wolf_hp} | Your HP: {hp}")
                        print("Actions: 1.attack / 2.defend / 3.use item")
                        act = input("> ").strip().lower()

                        if act == "attack" or act == '1':
                            dmg = random.randint(3, 6)
                            wolf_hp -= dmg
                            print(f"You strike the wolf for {dmg} damage.")
                            if wolf_hp > 0:
                                e_dmg = random.randint(1, wolf_dmg)
                                hp -= e_dmg
                                print(f"The wolf bites you for {e_dmg} damage.")
                        elif act == "defend" or act == '2':
                            e_dmg = max(0, random.randint(1, wolf_dmg) - 2)
                            hp -= e_dmg
                            print(f"You block. Take {e_dmg} reduced damage.")
                        elif act == "use item" or act == '3':
                            if "some food" in have_list:
                                have_list.remove("some food")
                                hp += 3
                                print("You eat food. HP +3")
                            else:
                                print("No usable items.")
                        else:
                            print("Unknown action.")

                        if hp <= 0:
                            game_over = True
                            game_back = True
                            print("You are torn apart by the wolf pack.")
                            mac_demon_whisper("Torn apart...")
                            return

                    print(f"Wolf {wolf_num} slain!")

                print("\nAll wolves dead. The werewolf steps forward.")
                print('It has eat something, it look like better than before.')
                boss_hp += 10
            else:
                print("It swipes at you.")
                hp -= boss_dmg

        if hp <= 0:
            game_over = True
            game_back = True
            print("The werewolf tears you apart under the full moon.")
            break
    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return
    print("\nThe werewolf collapses, fading back to human form.")
    print("In its hand, you find a moon-forged blade and a pouch of gold.")
    print('Its corpse then rots away.')
    have_list.append("moonfang blade")
    have_list.append("some gold coins")
    player_total_score += 50
    good += 5
    defeated_werewolf = True
    print("Obtained Moonfang Blade and gold coins.")
    print("-------------------------\n")

def boss_fight(boss_name, max_hp, base_attack, phases, loot_item, boss_id):
    global hp, defeated_enemies, player_total_score, amulet,game_back,game_over,good,evil,weapon_broken,player_armor_reduction,player_weapon_damage,player_class,weapon_durability,weather_duration,weather_damage

    if boss_id in defeated_enemies:
        print(f"The {boss_name} has already been defeated.")
        return True

    boss_hp = max_hp
    phase_index = 0
    turn = 0
    mac_demon_whisper(boss_name)
    print_colored(f"\n=== BOSS ENCOUNTER: {boss_name.upper()} ===", Colors.RED + Colors.BOLD)
    print_colored("A terrifying presence fills the room...", Colors.RED)
    time.sleep(1.2)

    while boss_hp > 0 and hp > 0:
        turn += 1
        print(f"\n--- Turn {turn} ---")
        print(f"Your HP: {hp}  |  Boss HP: {boss_hp}/{max_hp}")

        # Phase transition check
        while phase_index < len(phases) - 1 and boss_hp <= phases[phase_index + 1]["hp_threshold"]:
            phase_index += 1
            phase = phases[phase_index]
            print_colored(f"\n{phase['dialogue']}", Colors.PURPLE + Colors.BOLD)
            if phase.get("enrage"):
                print_colored("The boss enters berserk rage!", Colors.RED + Colors.BLINK)
            time.sleep(1.2)

        current_phase = phases[phase_index]
        dmg_multiplier = 1.5 if current_phase.get("enrage") else 1.0

        # Player action
        action = input("Action: 1.attack / 2.defend / 3.use item: ").strip().lower()

        if action == "attack" or action == '1':
            base_dmg = random.randint(3, 6)
            # Weapon bonuses
            if "ghost sword" in have_list:
                base_dmg += 4
            elif "iron sword" in have_list:
                base_dmg += 2
            # Critical hit
            is_crit = random.randint(1, 10) == 1
            if is_crit:
                base_dmg *= 2
                print_colored("CRITICAL HIT!", Colors.YELLOW + Colors.BOLD)
            if not weapon_broken and player_weapon_damage > 1:
                weapon_durability -= 1
                if weapon_durability <= 0:
                    weapon_broken = True
                    player_weapon_damage = 1
                    for w in ["iron sword", "cursed greatsword", "captain longsword",'ghost sword']:
                        if w in have_list:
                            have_list.remove(w)
                    print_colored("Your weapon shatters! You fight with bare fists from now on.",Colors.YELLOW)
                    player_total_score -= 15
            
            boss_hp -= base_dmg
            print(f"You deal {base_dmg} damage to the {boss_name}.")

        elif action == "defend" or action == '2':
            print("You raise your guard. Damage reduced by 50%.")
            dmg_multiplier *= 0.5
            print('You then raise your weapon, you deal 2 damage.')
            boss_hp -= 2

        elif action == "use item" or action == '3':
            if "some food" in have_list:
                have_list.remove("some food")
                hp += 3
                print("You eat food. HP +3")
            elif "some water in the bottle" in have_list:
                have_list.remove("some water in the bottle")
                hp += 2
                print("You drink water. HP +2")
            else:
                print("No usable items left!")
            continue
        else:
            print("Invalid action. You lose your turn.")

        # Boss attacks if still alive
        if boss_hp > 0:
            skill = random.choice(current_phase["attacks"])
            damage = int(random.randint(base_attack - 1, base_attack + 2) * dmg_multiplier)
            
            # Amulet damage reduction
            if amulet:
                damage = max(1, damage - 2)

            print_colored(f"{boss_name} uses {skill['name']}!", Colors.RED)
            if skill.get("description"):
                print(skill["description"])
            
            hp -= damage
            print(f"You take {damage} damage.")

            # Special skill effects
            if skill.get("lifesteal"):
                heal = damage // 2
                boss_hp = min(max_hp, boss_hp + heal)
                print(f"The boss drains your life and heals for {heal}.")
            if skill.get("curse"):
                evil += 3
                print("Dark curse corrupts you. Evil +3")

        time.sleep(0.6)

    # Battle conclusion
    if hp <= 0:
        print_colored("\nYou have been slain by the boss...", Colors.RED)
        game_over = True
        game_back = True
    else:
        print_colored(f"\nVICTORY! You defeated the {boss_name}!", Colors.GREEN + Colors.BOLD)
        print(f"You obtained: {loot_item}")
        have_list.append(loot_item)
        player_total_score += current_phase.get("score_reward", 30)
        defeated_enemies.add(boss_id)
        adjust_sanity(-10)
        return True
    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return

def write_creepy_desktop_file(tier: int):
    global meta_file_tier, death_count, session_start_time

    if tier <= meta_file_tier:
        return
    meta_file_tier = tier
    username = get_real_username()
    play_minutes = int((time.time() - session_start_time) // 60)

    try:
        file_path = os.path.join(DESKTOP_PATH, META_FILENAMES[tier - 1])
        with open(file_path, "w", encoding="utf-8") as f:
            if tier == 1:
                f.write("I can see you through the screen.\n")
                f.write(f"Hello, {username}.\n")
                f.write("Don't look behind you.\n")
            elif tier == 2:
                f.write(f"You have died {death_count} times now.\n")
                f.write(f"You've been playing for {play_minutes} minutes.\n")
                f.write("You think this is just a game.\n")
                f.write("It's not.\n")
                f.write("The cave is real.\n")
            elif tier == 3:
                f.write("You found the developer room.\n")
                f.write("He didn't make this place.\n")
                f.write("He just wrote down what he saw.\n")
                f.write(f"{username}, you should stop while you can.\n")
                f.write("Close the window. Run.\n")
            elif tier == 4:
                f.write("The blood moon is real too.\n")
                f.write("It's not code.\n")
                f.write("It's looking through your window right now.\n")
                f.write("Don't turn around.\n")
                f.write("I'm not in the game.\n")
                f.write("I'm behind you.\n")
            elif tier == 5:
                f.write("You reached the end.\n")
                f.write("But you can't leave.\n")
                f.write("Every time you restart, you go deeper into the cave.\n")
                f.write("Soon you won't be able to come back.\n")
                f.write(f"Goodbye, {username}.\n")
                f.write("Enjoy your stay.\n")
    except:
        pass

def init_military_password():
    global military_password
    d1 = str(random.randint(0, 9))
    d2 = str(random.randint(0, 9))
    d3 = str(random.randint(0, 9))
    military_password = d1 + d2 + d3

init_military_password()

def consume_step_durability():
    global light, torch_durability,sanity,game_back,game_over,hp,evil

    if not args.godmode:
        if not light and not torch and time_period == 'night' or  not light and not torch and time_period == 'dusk':
            sanity -= 3
        if time_period == "night" and random.randint(1, 3) == 1:
            sanity -= 2
        if sanity <= 0:
            if hp > 15:
                mac_demon_whisper("Go die, Thou!")
                print('You mind shtters.')
                print('However, you rarely survive.')
                print('Hp -15')
                hp -= 15
                sanity = 30
            else:
                mac_demon_whisper("Break. Break forever.")
                print("Your mind shatters into endless madness.")
                game_over = True
                game_back = True

        if sanity <= 20:
            if random.randint(1, 3) == 1:
                print("Hallucinations warp everything you see.")
                hp -= 3
                evil += 5
        elif sanity <= 40:
            if random.randint(1, 2) == 1:
                print("Cold dread crawls down your spine.")
                hp -= 1
    
    if light and torch_durability <= 0:
        torch_durability -= 1
        if torch_durability <= 0:
            light = False
            print("Your light burns out completely. Darkness closes in.")
            print('You shound go back to the black house to light it again.')
    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return

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
    print("           MESSAGE WALL")
    print("="*60)
    for idx, m in enumerate(messages[-20:], 1):
        print(f"{idx:2d}. [{m['name']}] {m['msg']} ({m['time']})")
    print("="*60)

def survival_tick():
    global hunger, thirst, hp,game_back,game_over

    hunger -= 1
    thirst -= 1
    if hunger <= 0:
        print('You feel very hungry, Hp -1')
        hp -= 1
    if thirst <= 0:
        print('You feel thirsty, Hp -1')
        hp -= 1
    if hp <= 0:
        print('You are too hungry and thirsty, so you died.')
        game_over = True
        game_back = True
    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return
        
def end_score_rating():
    global no_death_run,SCORE_SAVE_FILE,player_total_score,sanity

    if sanity <= 20:
        total = player_total_score + 50
    else:
        total = player_total_score
    if no_death_run:
        total += 100
    if total >= 1000:
        rank = '? RANK, Wow, you are wonderful!'
    elif total >= 600:
        rank = "S RANK, you are so cool~~~"
    elif total >= 500:
        rank = "A+ RANK, nice!"
    elif total >= 450:
        rank = "A RANK, very good!"
    elif total >= 300:
        rank = "B RANK, OK."
    elif total >= 150:
        rank = "C RANK, a little bad."
    elif total >= 50:
        rank = "D RANK, so bad!"
    else:
        rank = 'E RANK, are you a donkey?'

    print("\n==================== FINAL RESULT ====================")
    print(f"Total Score: {total}")
    print(f"Final Rating: {rank}")
    if sanity <= 20:
        print('See how crazy you are, you pass this game with less then 20 sanity, crazy!')
    print("======================================================\n")

    ranking = []
    try:
        with open(SCORE_SAVE_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line.isdigit():
                    ranking.append(int(line))
    except FileNotFoundError:
        ranking = []

    ranking.append(total)
    ranking = sorted(list(set(ranking)), reverse=True)
    ranking = ranking[:5]

    with open(SCORE_SAVE_FILE, "w") as f:
        for i in range(len(ranking)):
            f.write(f"{ranking[i]}\n")

    print("==== TOP 5 RANKING BOARD ====")
    for i in range(len(ranking)):
        print(f"{i+1}. {ranking[i]} Points")
    print("============================\n")

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
    print("Game saved!")

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
        print("Game loaded!")
        print(f"HP: {hp}")
    except:
        print("No save found!")

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

def character_creation():
    global hp, base_attack_bonus, base_defense_bonus, escape_bonus
    global have_list, player_class, player_weapon_damage, light

    print("\n=== CHOOSE YOUR ORIGIN ===")
    print("Select your background:")
    print("1. Warrior  | High HP, strong melee attacks")
    print("2. Rogue    | High escape, trap resistance")
    print("3. Mage     | Innate light, basic magic damage")

    while True:
        choice = input("origin> ").strip().lower()
        if choice == "1" or choice == "warrior":
            player_class = "warrior"
            hp = 35
            base_attack_bonus = 2
            base_defense_bonus = 1
            have_list.append("iron sword")
            player_weapon_damage = 3
            print("You choose the path of the Warrior.")
            print("HP: 35 | ATK Bonus: +2 | DEF Bonus: +1")
            print("Starting item: Iron Sword")
            break
        elif choice == "2" or choice == "rogue":
            player_class = "rogue"
            hp = 30
            base_attack_bonus = 1
            escape_bonus = 2
            have_list.append("lockpick")
            have_list.append("rope")
            player_weapon_damage = 2
            print("You choose the path of the Rogue.")
            print("HP: 30 | ATK Bonus: +1 | Escape Bonus: +2")
            print("Starting items: Lockpick, Rope")
            break
        elif choice == "3" or choice == "mage":
            player_class = "mage"
            hp = 27
            base_attack_bonus = 3
            light = True
            have_list.append("magic staff")
            player_weapon_damage = 4
            print("You choose the path of the Mage.")
            print("HP: 27 | ATK Bonus: +3 | Permanent inner light")
            print("Starting item: Magic Staff")
            break
        else:
            print("Invalid choice. Type 1, 2, 3 or class name.")

def can_enter_altar():
    global soldier_task_done,lieutenant_task_done,old_diary_readed,grave_diary_read,have_list,x2

    if soldier_task_done and lieutenant_task_done and old_diary_readed and grave_diary_read and len(have_list) >= 6:
        x2 = True
    else:
        x2 = False

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
    print("               PLAYER JOURNAL")
    print("="*60)
    print(f"Play Count: {play_count}")
    print(f"HP: {hp}")
    print(f"Good: {good} | Evil: {evil}")
    print("\n--- Runes Collected ---")
    print(f"Rune 1: {rune1} | Rune 2: {rune2} | Rune 3: {rune3}")
    print("\n--- Story Progress ---")
    print(f"Read Explorer Diary: {diary_read}")
    print(f"Read Wizard Diary: {old_diary_readed}")
    print(f"Read Grave Diary: {grave_diary_read}")
    print("\n--- Task List ---")
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
    elif current_weather == "heavy_snow":
        visibility = 40
        move_penalty = 1
        weather_damage = 1
    elif current_weather == "windy":
        visibility = 65

def print_weather():
    print(f"\nWeather: {current_weather} | Visibility: {visibility}%")
    if weather_damage > 0 and amulet == False:
        print("The harsh weather hurts you.")

def military_fort():
    global hp, good, evil, soldier_task_done, lieutenant_task_done
    global colonel_diary_collected, fort_unlocked, military_password
    global has_military_key, trap_protect, have_list
    global password_attempts, fort_password_locked
    global player_total_score
    global diary_fragment_1, diary_fragment_2, diary_fragment_3
    print("\n==================== ABANDONED MILITARY FORT ====================")
    print("Decades-old outpost built to seal the cursed cave. Rusty weapons and scattered journals lie everywhere.")
    print("Available locations: 1.east_sentry | 2.swamp_command | 3.top_headquarters | 4.barracks| 5.armory | 6.back")

    while True:
        advance_time()
        consume_step_durability()
        cmd = input("fort> ").strip().lower()
        if cmd == "back" or cmd == '6':
            print("You leave the military fort and return to the northern road.")
            break

        elif cmd == "east_sentry" or cmd == '1':
            if not soldier_task_done:
                print("\n[Soldier (Ghost)]")
                print("I lost my ration pack in the woods. I cannot hold this post without supplies.")
                sub_cmd = input("choice: 1.help | 2.loot | 3.search_note | 4.leave\n").strip().lower()
                if sub_cmd == "help" or sub_cmd == '1':
                    if "some food" in have_list:
                        have_list.remove("some food")
                        soldier_task_done = True
                        good += 8
                        has_military_key = True
                        print("You hand over food. The soldier gives you a bronze key for the armory.")
                        print("Head to the swamp command post and find the lieutenant for the march password.")
                        print('He also says: First digit of the march code is ' + military_password[0])
                        player_total_score += 10
                    else:
                        print("You carry no food to offer.")
                elif sub_cmd == "loot" or sub_cmd == '2':
                    evil += 12
                    hp -= 3
                    print("You steal supplies and trigger an old trap. The soldier becomes hostile.")
                elif sub_cmd == "search_note" or sub_cmd == '3':
                    if not diary_fragment_1:
                        diary_fragment_1 = True
                        print("You find a torn journal page: First digit of the march code is " + military_password[0])
                        player_total_score += 5
                    else:
                        print("You already searched this area.")
                elif sub_cmd == "leave" or sub_cmd == '4':
                    continue
            else:
                print("The soldier stands guard quietly.")

        elif cmd == "barracks" or cmd == '4':
            if not diary_fragment_2:
                diary_fragment_2 = True
                print("You rummage through old bunks and find a crumpled note: Second digit of the march code is " + military_password[1])
                player_total_score += 5
            else:
                print("Empty barracks. Nothing left to find.")

        elif cmd == "armory" or cmd == '5':
            if not diary_fragment_3:
                diary_fragment_3 = True
                print("Beneath a rusted rifle you find a log slip: Third digit of the march code is " + military_password[2])
                player_total_score += 5
            else:
                print("The armory has been picked clean.")

        elif cmd == "swamp_command" or cmd == '2':
            if fort_password_locked:
                print("The command post is permanently sealed. You failed too many times.")
                continue
            if not lieutenant_task_done:
                print("\n[Lieutenant (Ghost)]")
                print("The march password is split across three journal fragments scattered around the fort.")
                print("Enter the full 3-digit code to unlock trap immunity and access to archives.")
                ans = input("input password: ").strip().lower()
                if ans == military_password:
                    lieutenant_task_done = True
                    good += 10
                    trap_protect = True
                    print("Password verified. You gain full swamp trap immunity.")
                    player_total_score += 20
                else:
                    password_attempts += 1
                    hp -= 4
                    evil += 2
                    if password_attempts >= 3:
                        fort_password_locked = True
                        print("WRONG. Three failed attempts. The system locks permanently.")
                        print("You will never access the military archives in this run.")
                        player_total_score -= 30
                    else:
                        print(f"Wrong code. Poison gas leaks. Attempts left: {3 - password_attempts}")
                        player_total_score -= 10
            else:
                print("Deliver all three garrison journals to the colonel at headquarters.")

        elif cmd == "top_headquarters" or cmd == '3':
            if good < 10:
                print("\n[Colonel (Ghost)]")
                print("Go away, evil man.")
            else:
                print("You submit all journals. The colonel recounts the full story of your family's cursed guardianship.")
                if 'military archive document' not in have_list:
                    have_list.append("military archive document")
                    good += 15
                    player_total_score += 10
                print("You obtain classified files that unlock the hidden military ending.")

        else:
            print("Unknown command.")
        
def orc_tribe_dungeon():
    global hp, good, evil, orc_friend, orc_totem_found, have_list,game_back,game_over
    global player_total_score,orc_in

    print("\n==================== ORC TRIBE UNDERGROUND DUNGEON ====================")
    print("A primitive orc settlement trapped inside the infinite cave cycle. You can choose to negotiate or raid this tribe.")
    while True:
        consume_step_durability()
        cmd = input("orc> negotiate | raid | search_totem | back: ").strip().lower()
        if cmd == "back":
            print("You leave the orc dungeon area.")
            return
        elif cmd == "search_totem":
            if not orc_totem_found:
                print("You discover the stolen tribal totem hidden behind loose stone blocks.")
                orc_totem_found = True
                have_list.append("orc tribal totem")
                player_total_score += 40
            else:
                print("The tribal totem has already been retrieved.")
        elif cmd == "negotiate":
            if orc_totem_found:
                orc_friend = True
                good += 18
                have_list.append("a pickaxe")
                print("You return the sacred totem. The chieftain gifts you a durable pickaxe and marks all cave traps on your map.")
                player_total_score += 20
                orc_in = True
                return
            else:
                print("The tribe refuses to communicate until their stolen totem is returned.")
        elif cmd == "raid":
            evil += 30
            hp -= 8
            print("You attack the tribe and seize gold treasures, but gain heavy evil karma.")
            print('Hp -8')
            player_total_score -= 80
            if hp <= 0:
                print('You was killed by the dark evil karma.')
                game_over = True
                game_back = True
            orc_in = True
            return
        else:
            print("Unknown command.")

def titan_guardian_easter():
    global titan_meet, good, evil, hp
    global player_total_score
    print("\n==================== TITAN ANCIENT GUARDIAN (3RD RUN SECRET) ====================")
    print("A primordial titan sleeps deep inside the illusion tunnel, witnessing the birth of the ancient sealing curse.")
    if not titan_meet:
        titan_meet = True
        choice = input("offer_prayer | confess_sins | depart: ").strip().lower()
        if choice == "offer_prayer":
            good += 30
            hp = 99
            print("The titan grants you full vitality and pure spiritual alignment.")
            player_total_score += 15
        elif choice == "confess_sins":
            evil = 0
            print("All your accumulated evil karma is completely cleansed by ancient holy light.")
            player_total_score += 10
        elif choice == "depart":
            print("You leave the titan's resting place without receiving any blessing.")
            player_total_score -= 30
    else:
        print("The titan remains in eternal slumber and refuses to interact again.")

# Mistery
def forgotten_archive():
    global hp, have_list, good, evil, faith, game_over, game_back
    global has_death_corpse, death_location, death_corpse_item,current_room,one_hole_in,light,torch,trap_protect,gnome_hole_in
    global player_total_score

    current_room = 'forgotten_achive'
    print("\n=== FORGOTTEN ARCHIVE ===")
    print("Dust dances in faint light. Rows of stone shelves hold ancient scrolls.")
    print("The wizard built this place to seal his most dangerous experiments.")
    print("Four chambers lie ahead. Only the wise may reach the core.")
    print('Try to type look in every hall.')

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
        "gold coins": 4,
        'a book': 7,
        'a bottle': 2,
        'some water in the bottle': 3,
        'some food': 5
    }

    while True:
        if has_death_corpse and death_location == current_room:
            print('You see here a corpse, type corpse to search it.\n')
        
        consume_step_durability()
        cmd = input("archive> ").strip().lower()

        if cmd == "leave" or cmd == "back" or cmd == 'walk back':
            print("You climb out of the archive to the road.\n")
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
                print("\nA corpse slumps against the dusty floor. It wears your exact clothes.")
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print("Nothing useful left on the body.")
                has_death_corpse = False
            else:
                print("There is not any corpse..")

        elif current_room == "rune_hall":
            if cmd == "look":
                print("Four rune pedestals stand before a stone door: moon, sun, void, star.")
                print("Faded verse on the wall reads:")
                print("  'First the one that wakes the field,")
                print("   Then the one that guards the shield,")
                print("   Third the one that leads the lost,")
                print("   Last the one that bears the cost.'")
                print("Type 'press [rune]' to activate a pedestal. Wrong order resets progress.")

            elif cmd.startswith(""):
                rune_name = cmd.split()[1] if len(cmd.split()) > 1 else ""
                if rune_name not in ["sun", "moon", "star", "void"]:
                    print("Unknown rune.")
                    continue

                if rune_name == correct_rune_order[rune_step]:
                    rune_step += 1
                    print(f"Pedestal {rune_name} glows faintly.")
                    mistake_streak = 0
                    if rune_step == 4:
                        print("The stone door rumbles open. You enter the mirror corridor.")
                        player_total_score += 10
                        current_room = "mirror_hall"
                        rune_step = 0
                else:
                    mistake_streak += 1
                    damage = 1 if mistake_streak < 3 else 3
                    hp -= damage
                    print(f"Wrong order. Arcane energy shocks you. HP -{damage}")
                    player_total_score -= 10
                    jump_scare_face()
                    rune_step = 0
                    if hp <= 0:
                        print("You collapse under the magic surge.")
                        game_over = True
                        game_back = True
                        break

            else:
                print("Unknown command. Try 'look' to examine the room.")

        elif current_room == "balance_hall_clear":
            if cmd == "forward":
                current_room = "core_room"
            elif cmd == "workshop":
                print("You squeeze through the narrow side door into a tiny workshop.")
                current_room = "gnome_workshop"
            elif cmd == "back":
                current_room = "balance_hall"
            else:
                print("Unknown command. Try 'forward' or 'workshop'.")
        elif current_room == "gnome_workshop":
            if cmd == "look":
                print("A tiny workshop hidden behind the bookshelf. Gears and runestones scatter everywhere.")
                print("A gnarled rock gnome hunches over the workbench, his beard braided with copper wire.")
                print("He freezes when he hears you, then slowly turns around.")
                print('Type talk to talk, you should talk for more times.')

            elif cmd == "talk to gnome" or cmd == "talk bryn" or cmd == "talk":
                if not hasattr(forgotten_archive, 'gnome_met'):
                    print("Bryn: Back off! This place belongs to the wizard. No trespassers allowed.")
                    print("He picks up a small wrench, looking both nervous and fierce.")
                    print('Hp -1')
                    hp -= 1
                    if hp <= 0:
                        print('What a joke! Kill by a tiny stone!')
                        game_back = True
                        game_over = True
                        break
                    forgotten_archive.gnome_met = 1
                elif forgotten_archive.gnome_met == 1:
                    print("You tell him you are the wizard's descendant, here to end the curse.")
                    print("Bryn stares at you for a long time. His hands start to shake.")
                    print("Bryn: ...You have his eyes. Really his blood.")
                    print("Bryn: Two hundred years. I waited two hundred years for someone to come.")
                    print("Bryn: Sit. I'll tell you everything he never wrote in the diaries.")
                    forgotten_archive.gnome_met = 2
                    faith += 5
                    player_total_score += 5
                else:
                    print("Bryn looks up from his work. What do you want to know?")
                    print("You can ask: wizard / curse / himself / outside / dwarf / hints / upgrade / help him leave / steal from him")

            elif cmd == "ask wizard" and forgotten_archive.gnome_met >= 2:
                print("Bryn: He was never a hero. He was just a man scared of losing his wife.")
                print("Bryn: Everyone said he sealed her to save the world. Lies.")
                print("Bryn: He sealed her because he couldn't bear to let her die, even as a monster.")
                print("Bryn: Foolish man. Spent his whole life building a cage for the person he loved.")

            elif cmd == "ask curse" and forgotten_archive.gnome_met >= 2:
                print("Bryn: The curse didn't start with her. It started with the dwarven relic he stole.")
                print("Bryn: Gimble thought he could use it to cure her. It only made things worse.")
                print("Bryn: That's why the dwarf is down there, guarding the tomb. He blames us all.")
                print("Bryn: ...To be honest, he's not entirely wrong.")

            elif cmd == "ask himself" and forgotten_archive.gnome_met >= 2:
                print("Bryn: I? I was his chief machinist. Built all the traps, all the seals, all the puzzles.")
                print("Bryn: He told me to guard the archive until the heir arrived. So I stayed.")
                print("Bryn: Didn't even need magic. Gnome lives are long enough to wait out a human curse.")
                print("He laughs bitterly, tapping his cane on the stone floor.")

            elif cmd == "ask dwarf" and forgotten_archive.gnome_met >= 2:
                print("Bryn: Gimble. Used to be my best friend. Best blacksmith under the mountain.")
                print("Bryn: He came here to help us. Then the relic corrupted him.")
                print("Bryn: Now he's just an angry thing guarding the tomb. Doesn't remember anyone.")
                print("Bryn: If you can ... don't kill him. He's suffered enough.")
                print('You: Where is the dwarf?')
                print('The gnome seems to be quiet, do not answer you, just looking at you.')

            elif cmd == "ask hint" or cmd == "hints" and forgotten_archive.gnome_met >= 2:
                print("Bryn: Hints cost faith energy. Which puzzle are you stuck on?")
                print("runes / mirrors / scale / final lock")

            elif cmd == "hint runes" and forgotten_archive.gnome_met >= 2:
                if faith >= 10:
                    faith -= 10
                    print("Bryn: Think about the sky. What comes first, what comes after?")
                    print("Bryn: Sun wakes the world, moon guards the night, star leads the lost, void ends all.")
                else:
                    print("Bryn: Not enough faith. Go pray at the altar first.")

            elif cmd == "upgrade lantern" and forgotten_archive.gnome_met >= 2:
                if "a lamp" in have_list and good >= 10:
                    have_list.remove("a lamp")
                    have_list.append("eternal rune lantern")
                    light = False
                    torch = True
                    print("Bryn takes your lamp, scribes tiny runes on the glass.")
                    print("Bryn: There. Won't run out of oil anymore. Don't break it.")
                    print("Bryn: And ... be careful down there. Darkness eats people like you.")
                else:
                    print("Bryn: You need a lamp and a steady heart. You're not ready yet.")

            elif cmd == "free gnome" or cmd == "help him leave":
                if good >= 15 and forgotten_archive.gnome_met >= 2:
                    print("You break the sealing rune on the workshop door.")
                    print("Bryn stares at the open passage for a long time. He doesn't move at first.")
                    print("Bryn: I ... I thought I'd die down here.")
                    print("He takes a small toolkit from his belt and hands it to you.")
                    print("Bryn: Take this. All my best work. It'll protect you from traps.")
                    print("Bryn: I'm going up. To see the sun again.")
                    print('He then go into a small tunnal.')
                    good += 15
                    faith += 10
                    trap_protect = True
                    gnome_hole_in = True
                    have_list.append('gnome master toolkit')
                    player_total_score += 20
                    forgotten_archive.gnome_met = 3
                else:
                    print("Bryn: The seal only responds to a pure heart. You still carry too much darkness.")

            elif cmd == "steal from him" or cmd == "take tools":
                if forgotten_archive.gnome_met >= 2:
                    print("You sneak toward his toolbox while he's not looking.")
                    print("He slams his hammer down right beside your hand.")
                    print("Bryn: I knew it. Just like him. Greedy. Always greedy.")
                    print("The wall behind you slides shut. He vanishes into a side tunnel.")
                    print("You hear his voice from the dark: 'Find your own way out.'")
                    have_list.append("gnome toolkit")
                    evil += 20
                    forgotten_archive.gnome_met = 0
                    gnome_hole_in = True
                    player_total_score += 10
                    current_room = "balance_hall_clear"
                else:
                    print("You don't see any tools to steal yet.")

            elif cmd == "attack gnome" or cmd == "kill bryn":
                print('Bryn: Really? Attack a poor old gnome? You are so evil!')
                player_total_score -= 5
                evil += 5
            elif cmd == "joke" and forgotten_archive.gnome_met >= 2:
                print("You tell him a silly joke about ghosts.")
                print("He snorts, then chuckles, then laughs out loud — a rough, rusty sound.")
                print("Bryn: Hundreds of years. First joke I've heard.")
                print("He tosses you a small healing crystal.")

            elif cmd == "give food" and forgotten_archive.gnome_met >= 2:
                if "some food" in have_list:
                    have_list.remove("some food")
                    print("You hand him your food. He stares at it like it's a treasure.")
                    print("Bryn: Fresh bread. I almost forgot what it tastes like.")
                    print("He eats slowly, very slowly. His eyes soften.")
                    print("Bryn: Alright. Ask me anything. I'll give you one free hint.")
                    forgotten_archive.free_hint = True
                    player_total_score += 10
                else:
                    print("You have no food to give him.")

            elif cmd == "leave" or cmd == "back":
                print("You step back into the balance hall.")
                current_room = "balance_hall_clear"

            else:
                print("Bryn looks at you expectantly, waiting for you to speak.")
        elif current_room == "mirror_hall":
            if cmd == "look":
                print("Three mirrors stand in a line, each can rotate left or right.")
                print("A light beam enters from the left wall. It must reach the right receiver.")
                print(f"Mirror angles (0 = forward, 1 = right, -1 = left): {mirror_angles}")
                print("Type 'turn mirror1 left', 'turn mirror2 right' etc. to adjust.")
                print("Type 'beam' to fire the light and test your setup.")

            elif cmd.startswith("turn mirror"):
                parts = cmd.split()
                if len(parts) < 3:
                    print("Invalid command.")
                    continue
                try:
                    mirror_idx = int(parts[1][-1]) - 1
                    direction = parts[2]
                    if mirror_idx < 0 or mirror_idx > 2:
                        print("No such mirror.")
                        continue
                    if direction == "left":
                        mirror_angles[mirror_idx] -= 1
                    elif direction == "right":
                        mirror_angles[mirror_idx] += 1
                    else:
                        print("Invalid direction.")
                        continue
                    print(f"Mirror {mirror_idx+1} rotated.")
                except:
                    print("Invalid command.")

            elif cmd == "beam":
                correct = [1, -1, 1]
                if mirror_angles == correct:
                    print("Light travels through all mirrors and hits the receiver.")
                    print("A hidden passage opens to the balance chamber.")
                    player_total_score += 10
                    current_room = "balance_hall"
                else:
                    mistake_streak += 1
                    damage = 1 if mistake_streak < 3 else 2
                    hp -= damage
                    jump_scare_face('flash')
                    print(f"Beam hits a wall and bounces back, burning you. HP -{damage}")
                    if hp <= 0:
                        print("You fall to the scorching beam.")
                        game_over = True
                        game_back = True
                        break

            else:
                print("Unknown command. Try 'look' to examine the room.")

        elif current_room == "balance_hall":
            if cmd == "look":
                print("A stone scale stands in the center. Left plate holds a 7-unit weight.")
                print("You must place items from your bag on the right plate to balance it exactly.")
                print("Type 'place [item name]' to put an item on the plate.")
                print("Type 'weigh' to check if the scale is balanced.")
                print("Type 'clear' to take all items back.")

            elif cmd == "clear":
                print("You take all items back from the plate.")
                if not hasattr(forgotten_archive, 'plate_items'):
                    forgotten_archive.plate_items = []
                forgotten_archive.plate_items.clear()
            elif cmd == 'bag':
                for i in range(len(have_list)):
                    print(have_list[i])
            elif cmd.startswith("place "):
                item_name = cmd[6:].strip()
                if item_name not in have_list:
                    print("You don't have that item.")
                    continue
                if not hasattr(forgotten_archive, 'plate_items'):
                    forgotten_archive.plate_items = []
                if item_name in forgotten_archive.plate_items:
                    print("That item is already on the plate.")
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
                    print("The scale balances perfectly. The main door to the core unlocks.")
                    print("You also notice a small, hidden side door half-buried in dust.")
                    print("Type 'workshop' to enter the side room, or 'forward' to continue to the core.")
                    current_room = "balance_hall_clear"
                else:
                    mistake_streak += 1
                    print(f"Right side weighs {total}. Not balanced.")
                    if mistake_streak >= 3:
                        hp -= 2
                        print("The scale tilts sharply and hits you. HP -2")
                        if hp <= 0:
                            print("You are crushed by the falling scale.")
                            game_over = True
                            game_back = True
                            break

            else:
                print("Unknown command. Try 'look' to examine the room.")
        elif current_room == "balance_hall_clear":
            if cmd == "forward":
                current_room = "core_room"
            elif cmd == "workshop":
                if gnome_hole_in == False:
                    print("You squeeze through the narrow side door into a tiny workshop.")
                    current_room = "gnome_workshop"
                else:
                    print('The gnome have already gone, just a empty tiny workshop.')
            elif cmd == "back":
                current_room = "balance_hall"
            else:
                print("Unknown command. Try 'forward' or 'workshop'.")
        elif current_room == "core_room":
            if cmd == "look":
                print("A heavy iron door blocks the way. It has a 3-digit combination lock.")
                print("Carved above the lock:")
                print("  'Count of the first runes, turns of the middle path, weight of the last truth.'")
                print("Type 'enter [3-digit code]' to try the combination.")
                print("You may also 'pray' at the small altar beside the door for a hint.")

            elif cmd == "pray":
                faith_cost = 5
                if faith >= faith_cost:
                    faith -= faith_cost
                    print("A soft voice whispers: 'Four runes pressed, three mirrors turned, seven stones weighed.'")
                    print("Hint: first digit = number of correct runes.")
                    player_total_score -= 20
                else:
                    print("You lack enough faith to receive guidance.")

            elif cmd.startswith("enter "):
                code = cmd.split()[1] if len(cmd.split()) > 1 else ""
                if code == final_code:
                    print("The lock clicks. The core chamber opens before you.")
                    print("Warm light flows out, filling the archive.")
                    print('Hp +20!!!')
                    hp += 20
                    one_hole_in = True
                    player_total_score += 50
                    gamestart()
                    return
                else:
                    mistake_streak += 1
                    damage = 2 if mistake_streak < 3 else 4
                    hp -= damage
                    jump_scare_face('flash')
                    print(f"Wrong code. Poison gas fills the room. HP -{damage}")
                    player_total_score -= 15
                    if hp <= 0:
                        print("You choke and fall unconscious.")
                        game_over = True
                        game_back = True
                        break

            else:
                print("Unknown command. Try 'look' to examine the room.")

    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return

def child_tomb():
    global hp, have_list, good, evil, faith, game_over, game_back, current_room
    global has_death_corpse, death_location, death_corpse_item,child_hole_in
    global player_total_score
    current_room = "child_tomb"

    print("\n=== CHILDREN'S CHAMBER ===")
    print("The air is cold and still. You hear faint humming.")
    print("Small toys scatter across the stone floor.")
    print("A tiny coffin sits in the corner, carved with stars.")
    print("A child's voice whispers: 'Did you come to play?'")

    toys_placed = []
    correct_order = ["crayon", "horse", "doll", "coffin"]
    question_stage = 0
    wrong_count = 0

    while True:
        if has_death_corpse and death_location == current_room:
            print('You see here a corpse, type corpse to search it.\n')
        consume_step_durability()
        cmd = input("child> ").strip().lower()

        if handle_terminal_cmd(cmd):
            continue

        if cmd == "leave" or cmd == "back":
            print("You step back quietly, closing the small door.")
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
            print("Four toys lie on the ground: crayon, horse, doll, coffin(just a toy).")
            print("Wall drawings show a boy drawing, riding, playing, then sleeping.")
            print("Type 'place [toy]' to put them on the stone altar in order.")
            print("Type 'reset' to start over.")

        elif cmd.startswith("place "):
            toy = cmd[6:].strip()
            if toy not in ["crayon", "horse", "doll", "coffin"]:
                print("That is not a toy here.")
                continue
            if toy in toys_placed:
                print("You already placed that one.")
                continue
            if toy == correct_order[len(toys_placed)]:
                toys_placed.append(toy)
                print(f"You place the {toy} on the altar. It glows faintly.")
                if len(toys_placed) == 4:
                    print("\nAll toys glow silver. A small boy appears before you.")
                    print("He looks about seven years old, pale and quiet.")
                    player_total_score += 5
                    question_stage = 1
            else:
                wrong_count += 1
                dmg = 1 if wrong_count < 3 else 3
                hp -= dmg
                print(f"The toy turns cold and burns your hand. HP -{dmg}")
                player_total_score -= 10
                toys_placed.clear()
                print("All toys fall off the altar.")
                if hp <= 0:
                    print("You collapse. The child whispers: 'Sleep then... stay forever.'")
                    game_over = True
                    game_back = True
                    break

        elif cmd == "reset":
            toys_placed.clear()
            print("You take all toys back.")

        elif question_stage == 1:
            if cmd == "yes":
                print("Boy: 'Then answer my questions. If you lie... I will know.'")
                player_total_score += 5
                question_stage = 2
            elif cmd == "no":
                print("Boy: 'Then why are you here? To steal from me too?'")
                print("The room goes dark. Something pushes you hard.")
                player_total_score -= 10
                hp -= 3
                print("HP -3")
                if hp <= 0:
                    print("You fall and never wake up.")
                    game_over = True
                    game_back = True
                    break
            else:
                print("Boy: 'Answer me. Are you here to play?'")

        elif question_stage == 2:
            if cmd == "stay" or cmd == "yes":
                print("\n===== ETERNAL PLAYMATE ENDING =====")
                print("The boy smiles brightly. The door closes forever.")
                print("You sit down and play with him. For a day, a year, an eternity.")
                print("No one ever finds you.")
                game_over = True
                game_back = True
                break
            elif cmd == "no" or cmd == "i cant":
                print("Boy: 'I knew it. Everyone leaves.'")
                print("He looks down, sad but not angry.")
                player_total_score += 5
                question_stage = 3
            else:
                print("Boy: 'Will you stay with me forever?'")

        elif question_stage == 3:
            if cmd == "wizard" or cmd == "the wizard" or cmd == "your father":
                print("The boy's eyes widen. 'You know him?'")
                print("'He put me here. He said he would bring me back.'")
                print("'He never came.'")
                print("\nThe boy fades into silver light.")
                print("'You are honest. Take this. Tell him I am not angry.'")
                have_list.append("child rune shard")
                faith += 15
                good += 20
                hp += 10
                player_total_score += 20
                print("You got CHILD RUNE SHARD. Faith +15, Good +20, HP +10")
                print("The small door opens. You may leave.")
                question_stage = 4
            else:
                print("Boy: 'Wrong. Guess again.'")
                hp -= 1
                print("HP -1")

        elif question_stage == 4 and cmd == "leave":
            print("You walk out of the small chamber quietly.")
            player_total_score += 5
            child_hole_in = True
            pendulum_mortuary()
            return

        elif cmd == "attack boy" or cmd == "kill boy":
            print("You lunge at the child. He screams.")
            print("The whole tomb shakes. Dark energy crushes you.")
            player_total_score -= 30
            hp -= 10
            evil += 30
            print("HP -10 | Evil +30")
            if hp <= 0:
                print("You are torn apart by the curse.")
                game_over = True
                game_back = True
                break
            print("The boy vanishes, crying. You are thrown out of the chamber.")
            child_hole_in = True
            pendulum_mortuary()
            return

        elif cmd == "corpse" or cmd == "search corpse":
            if has_death_corpse and death_location == current_room:
                print("\nA corpse curls in the corner, small and twisted.")
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print("Nothing useful left on the body.")
                has_death_corpse = False
            else:
                print("There is no corpse here.")

        else:
            print("Unknown command. Try 'look'.")

    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return

def handle_terminal_cmd(cmd):
    global game_back,game_over,hp
    
    cmd = cmd
    if cmd in ["ls", "dir"]:
        print("dust x9999")
        print("cobweb x42")
        print("broken_bones x7")
        print("your_sanity -1")
        print("ghost_footprint .hidden")
        return True
    elif cmd == "ls -la" or cmd == "dir /a":
        print("drwxr-xr-x  dust")
        print("drwxr-xr-x  darkness")
        print("-rw-r--r--  your_hope.txt (0 bytes)")
        print("-rw-r--r--  .developer_note")
        return True
    elif cmd.startswith("cd "):
        path = cmd[3:].strip()
        if path == "..":
            print("You cannot go back that easily.")
        elif path == "/":
            print("Root of the cave? You are already deep enough.")
        elif path == "~":
            print("Home? You left that behind long ago.")
        else:
            print(f"No such directory: {path}")
        return True
    elif cmd == "pwd":
        print("/death_adventure/unknown_depth/you_are_lost")
        return True
    elif cmd.startswith("mkdir "):
        name = cmd[6:].strip()
        print(f"Directory '{name}' created. Filled with dust instantly.")
        return True
    elif cmd == "rm -rf /" or cmd == "rm -rf /*":
        print("Deleting...")
        for _ in range(30):
            print("\n")
            time.sleep(0.01)
        print("Everything fades to black.\n")
        time.sleep(1.5)
        print("You deleted yourself.\n")
        time.sleep(2)
        hp -= 3
        if hp == 0:
            print('You die because you type something.')
            game_over = True
            game_back = True
        else:
            print("\n...You gasp and open your eyes. It felt real.")
            print("HP -3")
        return True
    elif cmd.startswith("rm "):
        print("You cannot delete reality.")
        return True
    elif cmd.startswith("sudo "):
        print("Permission denied. You are not the wizard.")
        return True
    elif cmd == "sudo su" or cmd == "su":
        print("Root access locked. Only the blood heir may enter.")
        return True
    elif cmd.startswith("cat "):
        file = cmd[4:].strip()
        if file == "diary":
            print("Pages are already in your memory.")
        elif file == "wall":
            print("You cannot read the wall this way.")
        else:
            print(f"No such file: {file}")
        return True
    elif cmd.startswith("echo "):
        text = cmd[5:].strip()
        print(f"A whisper echoes back: {text}")
        return True
    elif cmd in ["clear", "cls"]:
        print("\n" * 50)
        print("Screen cleared. Darkness remains.")
        return True
    elif cmd in ["exit", "quit"]:
        print("There is no exit. Only the cave.")
        return True
    elif cmd == "whoami":
        print("A poor adventurer about to die.")
        return True
    elif cmd.startswith("touch "):
        name = cmd[6:].strip()
        print(f"You touched {name}. It is cold and dusty.")
        return True
    elif cmd.startswith("chmod "):
        print("Permission bits do not work on ghosts.")
        return True
    elif cmd.startswith("ping "):
        target = cmd[5:].strip()
        print(f"Pinging {target}...")
        print("64 bytes from darkness: time=9999ms")
        print("No response. Only silence.")
        return True
    elif cmd in ["reboot", "shutdown -r now"]:
        print("System reboot failed. The curse prevents restart.")
        return True
    elif cmd in ["shutdown", "shutdown now", "halt"]:
        print("You cannot shut the cave down.")
        return True
    elif cmd == "ps" or cmd == "ps aux":
        print("PID  USER    COMMAND")
        print("1    ghost   haunting_you")
        print("2    curse   draining_hp")
        print("3    you     panicking")
        return True
    elif cmd.startswith("kill "):
        print("You cannot kill what is already dead.")
        return True
    elif cmd == "kill -9 1":
        print("Nice try. Ghost PID 1 is immortal.")
        return True
    elif cmd == "top":
        print("Load average: 9.99 9.99 9.99")
        print("Most process: curse, fear, your slow death")
        return True
    elif cmd.startswith("man "):
        topic = cmd[4:].strip()
        print(f"No manual for {topic}. Figure it out yourself.")
        return True
    elif cmd == "help":
        print("MANUAL: type anything and hope it works.")
        return True
    elif cmd in ["vim", "vi", "nano", "emacs"]:
        print("No editor here. The walls write their own story.")
        return True
    elif cmd == "python" or cmd == "python3":
        print("Python 3.?? (cursed edition)")
        print(">>> ")
        print("Error: no module named 'escape'")
        return True
    elif cmd.startswith("pip "):
        print("Could not fetch packages. No internet in the cave.")
        return True
    elif cmd in ["ifconfig", "ipconfig"]:
        print("eth0: 0.0.0.0")
        print("Status: disconnected from reality")
        return True
    elif cmd == "ipconfig /flushdns":
        print("DNS cache flushed. You still remember the curse.")
        return True
    elif cmd.startswith("curl ") or cmd.startswith("wget "):
        print("Network unreachable. Only ghosts have signal.")
        return True
    elif cmd == "date":
        print("Time does not exist down here.")
        return True
    elif cmd == "cal":
        print("Calendar blurred by dust. No day, no night.")
        return True
    elif cmd == "df -h":
        print("Filesystem  Size  Used  Free")
        print("/dev/cave    999T  999T   0%")
        print("No space left for your sanity.")
        return True
    elif cmd == "find .":
        print("./dust")
        print("./more_dust")
        print("./your_dead_future")
        return True
    elif cmd == "grep":
        print("Nothing found. Only silence.")
        return True
    elif cmd == "tar":
        print("You cannot archive your fate.")
        return True
    elif cmd in ["tree", "tree /f"]:
        print(".")
        print("└── darkness")
        print("    └── you")
        print("        └── doomed")
        return True
    elif cmd == "tasklist":
        print("Image Name           PID")
        print("curse.exe            1")
        print("ghost_service.exe    2")
        print("your_sanity.exe      3 (not responding)")
        return True
    elif cmd.startswith("taskkill"):
        print("ERROR: Access denied. Process is immortal.")
        return True
    elif cmd == "tracert":
        print("Tracing route to exit...")
        print("1  * * *  request timed out")
        print("2  * * *  request timed out")
        print("Destination never reached.")
        return True
    else:
        return False
    
def full_moon_maze():
    global hp, have_list, good, evil, faith, game_over, game_back, festival_mode
    global two_hole_in
    global current_room,has_death_corpse,death_corpse_item,death_location
    global player_total_score
    current_room = 'maze'
    if not festival_mode:
        print("The maze only appears under full moonlight.")
        return

    print("\n=== FULL MOON MAZE ===")
    print("Silver light seeps through stone cracks.")
    print("Moon phases shift on the walls. Paths change with every step.")
    print("The maze will vanish when the moon fades.")

    room = "shadow_hall"
    mistake = 0
    phase_progress = 0
    correct_phases = ["new", "waxing", "full", "waning", "crescent"]
    moon_code = "532"

    if has_death_corpse and death_location == current_room:
        print('You see here a corpse, type corpse to search it.\n')
    while True:
        consume_step_durability()
        cmd = input("moon> ").strip().lower()

        if cmd == "leave" or cmd == "back":
            print("You step out of the maze.")
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
            print('You see here a corpse, type corpse to search it.\n')
        elif room == "shadow_hall":
            if cmd == "look":
                print("Four shadow patterns on the ground: wolf, maiden, tree, crown.")
                print("Wall verse: 'First the beast that guards the night,")
                print("  Then the maid who lost her light,")
                print("  Last the root that holds the seal.'")
                print("Type 'step [name]' to walk on a shadow.")

            elif cmd.startswith("step "):
                target = cmd.split()[1] if len(cmd.split()) > 1 else ""
                order = ["wolf", "maiden", "tree"]
                if target == order[phase_progress]:
                    phase_progress += 1
                    print(f"Shadow of {target} glows softly.")
                    mistake = 0
                    if phase_progress == 3:
                        print("Stone door slides open. You enter the phase chamber.")
                        player_total_score += 5
                        room = "phase_chamber"
                        phase_progress = 0
                else:
                    mistake += 1
                    dmg = 1 if mistake < 3 else 3
                    hp -= dmg
                    print(f"Wrong shadow. Moonlight burns you. HP -{dmg}")
                    phase_progress = 0
                    if hp <= 0:
                        print("You collapse under silver fire.")
                        game_over = True
                        game_back = True
                        break
            else:
                print("Unknown command. Try 'look'.")

        elif room == "phase_chamber":
            if cmd == "look":
                print("Five stone plates on the wall, each carved a moon phase.")
                print("They are: new, waxing, full, waning, crescent.")
                print("Type 'press [phase]' to activate them in cycle order.")

            elif cmd.startswith("press "):
                phase = cmd.split()[1] if len(cmd.split()) > 1 else ""
                if phase == correct_phases[phase_progress]:
                    phase_progress += 1
                    print(f"{phase} plate lights up.")
                    mistake = 0
                    if phase_progress == 5:
                        print("All phases align. Final door reveals itself.")
                        player_total_score += 10
                        room = "moon_core"
                        phase_progress = 0
                else:
                    mistake += 1
                    dmg = 1 if mistake < 3 else 2
                    hp -= dmg
                    print(f"Wrong phase. Energy shocks you. HP -{dmg}")
                    phase_progress = 0
                    if hp <= 0:
                        print("Your body goes numb.")
                        game_over = True
                        game_back = True
                        break
            else:
                print("Unknown command. Try 'look'.")

        elif room == "moon_core":
            if cmd == "look":
                print("A moon-shaped altar stands in the center.")
                print("Three digit lock below the crystal.")
                print("Inscription: 'Count of phases, count of runes, count of lovers.'")
                print("Type 'enter [code]' to try. Type 'pray' for a hint.")

            elif cmd == "pray":
                if faith >= 10:
                    faith -= 10
                    print("Moonlight whispers: 'Five shapes, three stones, two souls.'")
                    player_total_score -= 5
                else:
                    print("Not enough faith.")

            elif cmd.startswith("enter "):
                code = cmd.split()[1] if len(cmd.split()) > 1 else ""
                if code == moon_code:
                    print("Lock clicks. Crystal blooms with silver light.")
                    print("The core chamber opens before you.")
                    print('You go back to the road.')
                    player_total_score += 20
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
                        print("You freeze under moon curse.")
                        game_over = True
                        game_back = True
                        break
            else:
                print("Unknown command. Try 'look'.")

    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return

def wax_chamber():
    global hp, have_list, good, evil, faith, game_over, game_back,three_hole_in
    global current_room,has_death_corpse,death_corpse_item,death_location
    global player_total_score

    jump_scare_face('flash')
    current_room = 'chamber'
    print("\n=== WAX CHAMBER ===")
    print("Cold wax smell fills your nose. Candles flicker weakly.")
    print("Seven human-shaped figures stand in a row, all wearing your face.")
    print("One of them is not wax. It is the first guardian.")
    print("Type 'examine [1-7]' to look closely.")
    print("Type 'choose [1-7]' when you know the answer.")

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
        print('You see here a corpse, type corpse to search it.\n')
    while True:
        consume_step_durability()
        cmd = input("wax> ").strip().lower()

        if cmd == "leave" or cmd == "back":
            print("You turn and run out before the wax figures move.")
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
                    print("No such figure.")
            except:
                print("Invalid number.")
        elif cmd == "examine corpse" or cmd == 'corpse' or cmd == 'search corpse' or cmd == 'find corpse':
            if has_death_corpse and death_location == current_room:
                print("\nA corpse slumps against the dusty floor. It wears your exact clothes.")
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print("Nothing useful left on the body.")
                has_death_corpse = False
            else:
                print("There is not any corpse..")
        elif cmd.startswith("choose "):
            try:
                num = int(cmd.split()[1])
                if num == correct:
                    print("The figure's eyes open. It is not wax.")
                    print("'You have my blood. You have come far.'")
                    print("The first guardian smiles and fades into dust.")
                    print("A stone door behind him opens slowly.")
                    print('You go back to the tomb.')
                    player_total_score += 15
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
                    jump_scare_face()
                    print(f"The wax figure lurches at you! HP -{dmg}")
                    player_total_score -= 20
                    print("All candles blow out for a second.")
                    if hp <= 0:
                        print("Wax hands drag you into the row.")
                        print("You become the eighth figure.")
                        print('You can not be birth forever!')
                        print('')
                        player_total_score = 0
                        print('Goodbye!')
                        end_score_rating()
                        print("=== Death Adventure v1.4 - Official Release ===")
                        print("Thank you for playing!")
                        exit()
            except:
                print("Invalid number.")
        else:
            print("Unknown command. Try 'examine 1' or 'choose 4'.")


def pendulum_mortuary():
    global hp, have_list, good, evil, faith, game_over, game_back,four_hole_in
    global current_room,has_death_corpse,death_corpse_item,death_location
    global player_total_score

    jump_scare_face('flash')
    current_room = 'mortuary'
    if has_death_corpse and death_location == current_room:
        print('You see here a corpse, type corpse to search it.\n')
    print("\n=== PENDULUM MORTUARY ===")
    print("Rotting wax and cold stone fill your nose.")
    print("Six stone coffins stand in a circle.")
    print("A rusted pendulum swings slowly above, counting dead time.")
    print("One coffin holds the first guardian. The rest hold hunger.")
    print('There are six coffines.')
    print('Try examine |coffine| or listen pendulum or open |coffine|')
    print('Still a way down, type down to go down.')
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
        consume_step_durability()
        cmd = input("mortuary> ").strip().lower()
        if cmd == "leave" or cmd == "back":
            print("You turn and walk out before the dead wake.")
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
            print("Tick... Tock... Tick... Tock...")
            print(f"You count {swing_count} swings so far.")
            if swing_count >= 3:
                print("The pendulum slows at the 4th coffin. And moving fast at 5th coffin, then slows at 6th coffine.")
        elif cmd == "open" or cmd == "child coffin" or cmd == 'down':
            if child_hole_in == False:
                print("The small coffin slides aside, revealing a narrow passage down.")
                child_tomb()
                return
            else:
                print('The door have already closed forever.')
        elif cmd.startswith("examine "):
            try:
                num = int(cmd.split()[1])
                if 1 <= num <= 6:
                    print(f"Coffin {num}: {coffin_details[num]}")
                    if num == correct and tried >= 2:
                        print("You feel faint warmth from inside. Not evil.")
                    else:
                        print('A cold freezing feeling.')
                else:
                    print("No such coffin.")
            except:
                print("Invalid number.")

        elif cmd == "pray":
            if faith >= 5:
                faith -= 5
                print("Warm light guides your eyes to the bronze ring mark.")
                player_total_score -= 5
            else:
                print("Not enough faith. The dead do not listen.")
        elif cmd == "examine corpse" or cmd == 'corpse' or cmd == 'search corpse' or cmd == 'find corpse':
            if has_death_corpse and death_location == current_room:
                print("\nA corpse slumps against the dusty floor. It wears your exact clothes.")
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print("Nothing useful left on the body.")
                has_death_corpse = False
            else:
                print("There is not any corpse..")
        elif cmd.startswith("open "):
            try:
                num = int(cmd.split()[1])
                if num == correct:
                    jump_scare_face('flash')
                    print("The lid opens silently. A body lies still, wearing your face.")
                    print("It holds a sealed letter in its hands.")
                    print("'I chose this fate. Do not blame the seal. Do not blame her.'")
                    print("'Free us both. That is the only way.'")
                    print("The body fades into dust. A heavy stone door rumbles open behind.")
                    print("Deep, heavy breathing comes from the darkness beyond.")
                    player_total_score += 5
                    hp += 10
                    faith += 10
                    good += 10
                    current_room = "dwarf_chamber"
                    continue
                        
                else:
                    tried += 1
                    dmg = 2 if tried < 3 else 8
                    hp -= dmg
                    jump_scare_face()
                    print(f"Dead hands reach out and scratch you! HP -{dmg}")
                    print("You hear faint gnawing sounds from inside.")
                    player_total_score += 5
                    if hp <= 0:
                        print("The dead drag you into the coffin.")
                        print("You become the seventh.")
                        print('You can not be rebirth.')
                        print('')
                        print('Goodbye!')
                        player_total_score = 0
                        end_score_rating()
                        print("=== Death Adventure v1.4 - Official Release ===")
                        print("Thank you for playing!")
                        exit()
            except:
                print("Invalid number.")
        elif current_room == "dwarf_chamber":
            if cmd == "look":
                print("A huge stone chamber. A massive dwarf in rusted armor stands in the center.")
                print("His eyes glow with corrupted red light. He grips a giant warhammer.")
                print("He growls: Trespasser. Leave. Or die.")
                print('Type talk / show toolkit / use holy amulet / attack dwarf / west')
            elif cmd == "talk to dwarf" or cmd == "speak gimble" or cmd == 'talk':
                if not hasattr(pendulum_mortuary, 'dwarf_talked'):
                    print("You call his name. He freezes, like he's trying to remember something.")
                    print("Gimble: ...Name. I know that name.")
                    print("He shakes his head, growling louder. No! Lies! All lies!")
                    print("He raises his hammer, ready to strike.")
                    pendulum_mortuary.dwarf_talked = True
                else:
                    print("He's too far gone to listen. You'll need something to jog his memory.")

            elif cmd == "show toolkit" or cmd == "give toolkit":
                if "gnome master toolkit" in have_list and hasattr(pendulum_mortuary, 'dwarf_talked') and pendulum_mortuary.dwarf_talked:
                    print("You hold up Bryn's toolkit. The dwarf stops moving.")
                    print("Gimble: Bryn...? Bryn's tools...")
                    print("The red glow in his eyes flickers. For a second, he looks like himself again.")
                    print("Gimble: Tell him ... I'm sorry. For everything.")
                    print("He steps aside, revealing the passage behind him.")
                    print("Gimble: Go. End this. Before I wake up again.")
                    player_total_score += 10
                    current_room = "dwarf_chamber_clear"
                else:
                    print("You have nothing that he would recognize.")

            elif cmd == "purify dwarf" or cmd == "use holy amulet":
                if "holy amulet" in have_list and good >= 30 and hasattr(pendulum_mortuary, 'dwarf_talked') and pendulum_mortuary.dwarf_talked:
                    print("You hold up the holy amulet. Pure light fills the chamber.")
                    print("The dwarf screams, but not in pain — in relief.")
                    print("Gimble: Finally. Finally free from this rot.")
                    print("He sets his hammer down gently. It glows with clean silver light.")
                    print("Gimble: Take this. It was meant for the heir.")
                    print("He fades into motes of light, smiling at last.")
                    print('You then go away.')
                    player_total_score += 10
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
                    print("Your heart is not pure enough. The amulet does not respond.")

            elif cmd == "attack dwarf" or cmd == "fight gimble":
                print("You charge at the dwarf. He roars and swings his hammer!")
                player_total_score -= 10
                dwarf_hp = 8
                while dwarf_hp > 0 and hp > 0:
                    print(f"\nDwarf HP: {dwarf_hp} | Your HP: {hp}")
                    action = input("strike / defend / run: ").strip().lower()
                    if action == "strike":
                        if "ghost sword" in have_list or "rune-forged hammer" in have_list:
                            dwarf_hp -= 2
                            print("Your weapon cuts through his corrupted armor!")
                        else:
                            dwarf_hp -= 1
                            print("You hit him, but it barely fazes him.")
                        if dwarf_hp > 0:
                            hp -= 2
                            print("His hammer slams into you! HP -2")
                    elif action == "defend":
                        hp -= 1
                        print("You block most of the blow. HP -1")
                    elif action == "run":
                        print("You retreat back to the mortuary.")
                        current_room = "mortuary"
                        break
                    else:
                        print("Invalid action!")
                if dwarf_hp <= 0:
                    print("The dwarf collapses with a heavy thud.")
                    print("You take his warhammer from his hands. It still hums with dark power.")
                    print('Then you leave.')
                    player_total_score += 15
                    have_list.append("corrupted warhammer")
                    evil += 30
                    four_hole_in = True
                    misty_swamp()
                    return
                elif hp <= 0:
                    print("His hammer crushes you. Everything goes dark.")
                    game_over = True
                    game_back = True
            else:
                print("The dwarf growls, watching your every move.")
        else:
            print("Unknown command. Try 'examine |coffine|' or 'listen pendulum' or 'open |coffine|'.")

    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return

def dwarven_forge_vault():
    global hp, have_list, orc_friend
    global player_total_score

    attempts_left = 2
    correct_recipe = {
        "iron": 2,
        "copper": 1,
        "silver": 1,
        "temp": "medium",
        "runes": ["moon", "star", "sun"]
    }

    print("\n==================== DWARVEN FORGE VAULT ====================")
    print("A long-lost dwarven forge. You must craft a blessed rune blade.")
    print("Three tattered notes lie nearby:")
    print("Note 1: Iron ore must be twice as much as copper ore. Total 4 parts.")
    print("Note 2: Temperature must not be the hottest nor the coldest.")
    print("Note 3: Sun rune goes last. Star rune does not go first.")

    while True:
        print(f"Materials left for {attempts_left} attempts.")
        consume_step_durability()
        cmd = input("forge> craft | back\n").strip().lower()
        if cmd == "back":
            break
        elif cmd == "craft":
            if attempts_left <= 0:
                print("All materials are exhausted. No more attempts this run.")
                break
            try:
                iron = int(input("Iron parts: ").strip()).strip().lower()
                copper = int(input("Copper parts: ").strip()).strip().lower()
                silver = int(input("Silver parts: ").strip()).strip().lower()
            except ValueError:
                attempts_left -= 1
                hp -= 2
                player_total_score -= 5
                print(f"Invalid input. The batch is ruined. Attempts left: {attempts_left}")
                continue

            temp = input("Temperature (low / medium / high): ").strip().lower()
            rune_input = input("Rune order separated by space: ").split().strip().lower()

            if (iron == correct_recipe["iron"] and
                copper == correct_recipe["copper"] and
                silver == correct_recipe["silver"] and
                temp == correct_recipe["temp"] and
                rune_input == correct_recipe["runes"]):
                print("\nFORGE SUCCESS. A blessed rune blade takes shape.")
                player_total_score += 20
                have_list.append("rune forged blade")
                break
            else:
                attempts_left -= 1
                hp -= 3
                print(f"Forging failed. The batch is ruined. Attempts left: {attempts_left}")
                player_total_score -= 10
        else:
            print("Unknown command.")

# tomb
def tomb():
    global game_over, hp, have_list, play_count, tomb_unlocked, game_back,cleared_ending
    global one_hole_in,two_hole_in,three_hole_in
    global tomb_pray_used
    global player_total_score
    
    print("\n=== FORGOTTEN TOMB (NG+ ONLY) ===")
    print("You step into a dark, ancient tomb.")
    print("The air is cold. Carvings on walls show your ancestors.")
    print("Only blood of the family can pass here...")
    print('You see here a new diary.')
    print('There is a deep shaft with some ledders, type down to go down!')
    print('You should first look around.')
    if play_count == 2:
        print('You can trial now.')
    tomb_unlocked = True

    while True:
        consume_step_durability()
        cmd = input("tomb> ").strip().lower()
        if handle_terminal_cmd(cmd):
            continue
        if cmd == "look" or cmd == 'look around':
            print("Stone coffins line both sides.")
            print("In the center: a glowing altar.")
            print('You see here a guardian.')
            print('You can challenge the guardian, if you lose, you will not die, but if you win, you will get something useful.')
            print('You seem to want to sing or dance.')
            print("On the wall: a huge carving of a woman (your ancestor).")
        elif cmd == 'read diary' or cmd == 'diary' or cmd == 'take diary':
            print('This is your fathers diary:')
            print('Son, if you find this diary, I have already died.')
            print('I was not go on a holiday, I just go to the cave and control the Evil.')
            print('I can not choose what to do, so you can do anything you want.')
            print('You should have a magic key to end the curse, I find it and put it in my coffin.')
            print('I wish you good luck, my son.')
        elif cmd == 'down' or cmd == 'go down':
            if three_hole_in == False:
                wax_chamber()
            else:
                print('You do not want to go in again.')
        elif cmd == "challenge guardian":
            if play_count == 2:
                print("Ancestor guardian appears!")
                guard_hp = 15
                while guard_hp > 0 and hp > 0:
                    print(f"Guardian HP: {guard_hp} | Your HP: {hp}")
                    fight = input("strike / defend: ").strip().lower()
                    if fight == "strike":
                        guard_hp -= 1
                        print("You strike the guardian!")
                        if guard_hp > 0:
                            hp -= 1
                            print("Guardian counters! hp -1")
                    elif fight == "defend":
                        print("You block the attack.")
                if guard_hp <= 0:
                    print("Guardian smiles: 'You are worthy.'")
                    have_list.append("guardian shield")
                    player_total_score += 10
                else:
                    print("Guardian spares you.")
                    hp = 15
            else:
                print("The guardian ignores you.")
        elif cmd == "trial":
            if play_count == 2:
                print("Light flows around you. Ancient figures appear.")
                print("They are your ancestors, guardians of this place.")
                print("Choose: choose inherit / choose refuse / choose listen")
                trial_choice = input().strip().lower()
                if trial_choice == "choose inherit":
                    print("You decide to carry on the duty of guardians.")
                    print("All spirits salute you. Your power rises greatly.")
                    hp += 10
                    player_total_score += 10
                    print("===== INHERITOR SIDE ENDING =====")
                elif trial_choice == "choose refuse":
                    print("You refuse the old fate and wish to end the cycle.")
                    print("Ancestors send their blessings to you.")
                    player_total_score += 10
                    print("===== FREEDOM SIDE ENDING =====")
                elif trial_choice == "choose listen":
                    print("You listen to stories of the past.")
                    print("You fully understand the pain of the ancient demon.")
                    print("Your mind becomes calm and clear.")
                    player_total_score += 10
                else:
                    print("Invalid choice.")
            else:
                print("The trial is not open for you yet.")
        elif cmd == "sing":
            print("You sing a silly song in the tomb.")
            print("A ghost yells: 'STOP SINGING PLEASE!'")
            hp += 1
        elif cmd == "eat candy":
            if "silly candy" in have_list:
                print("You eat the candy. Ghosts stare at you hungrily.")
            else:
                print("You have no candy to eat.")
        elif cmd == "pretend ghost":
            print("You float and howl like a ghost. Real ghosts laugh at you.")
        elif cmd == "tickling guardian":
            print("You tickle the guardian. He can't stop laughing and steps aside.")
        elif cmd == "offer snack":
            print("You offer food to ghosts. They shake heads, they can't eat anything.")
        elif cmd == "ask ghost why here":
            print("You ask the ghost why it lives here.")
            print("Ghost: 'Rent is cheap, and it’s quiet... mostly.'")
        elif cmd == "ghost wifi":
            print("You ask if the tomb has wifi.")
            print("Ghost: 'We use spirit signals, no internet needed!'")
        elif cmd == "ghost joke":
            print("You tell a ghost joke: 'What do you call a ghost that can’t lie?'")
            print("Ghost: 'A transparent liar!'")
        elif cmd == "ghost favorite dessert":
            print("You ask the ghost’s favorite dessert.")
            print("Ghost: 'I-scream, obviously.'")
        elif cmd == "ghost elevator":
            print("You ask if ghosts like elevators.")
            print("Ghost: 'Yep, they lift our spirits.'")
        elif cmd == "ghost social media":
            print("You ask why ghosts don’t use social media.")
            print("Ghost: 'Too many trolls, and we’re already ghosts.'")
        elif cmd == "ghost party":
            print("You ask if ghosts party here.")
            print("Ghost: 'This tomb’s our eternal rave.'")
        elif cmd == "ghost math":
            print("You ask if ghosts are good at math.")
            print("Ghost: 'Nah, too many transparent-cies.'")
        elif cmd == "ghost love":
            print("You ask if ghosts fall in love.")
            print("Ghost: 'Only with their ghoul-friends.'")
        elif cmd == "ghost homework":
            print("You ask the ghost to do your homework.")
            print("Ghost: 'I’m dead, not a tutor!'")
        elif cmd == "guardian joke":
            print("You tell a joke to the guardian.")
            print("Guardian: '...That was worse than my death.'")
        elif cmd == "do robot" or cmd == 'robot':
            print("You move stiffly like a robot. Ghosts mimic your silly moves.")
        elif cmd == "race ghost" or cmd == 'race':
            print("You race with ghosts. They float super fast and win easily.")
        elif cmd == "beg":
            print("You beg for snacks. The guardian rolls his eyes.")
        elif cmd == "greet":
            print("You say hello to ghosts. They wave back lazily.")
        elif cmd == "tease guardian":
            print("You tease the guardian. He crosses arms and refuses to talk.")
        elif cmd == "play hide and seek":
            print("You play hide and seek. Ghosts find you instantly.")
        elif cmd == "march":
            print("You march back and forth. Ghosts watch you curiously.")
        elif cmd == "blow whistle" or cmd == 'whistle':
            print("You blow a whistle. The whole tomb rings with sound.")
        elif cmd == "bow":
            print("You bow to the coffins. A faint rustle replies.")
        elif cmd == "yawn":
            print("You yawn loudly. Even ghosts feel sleepy.")
        elif cmd == 'kiss':
            print('You kiss the ghost! It shouts: WHAT ARE YOU DOING!!!')
        elif cmd == "whistle":
            print("You whistle loudly. Ghosts cover their ears.")
        elif cmd == "wave":
            print("You wave at the ancestor carving. It seems to wave back.")
        elif cmd == "dance":
            print("You dance in the tomb. The guardian sighs.")
            have_list.append("silly candy")
            print("You got SILLY CANDY!")
        elif cmd == "make noise":
            print("You make weird noises. Ghosts cover their ears.")
        elif cmd == "altar":
            print("You approach the glowing altar.")
            print("It holds an old locket and a final diary.")
            if "family locket" not in have_list:
                print("You take the locket.")
                player_total_score += 5
                have_list.append("family locket")
            if "final diary" not in have_list:
                print("You read the final diary:")
                print("'We are all bound here. The cycle ends only when we accept who we are.'")
                print("'You are not a treasure hunter. You are the heir.'")
                print("'Free us, and free yourself.'")
                player_total_score += 5
                have_list.append("final diary")
        elif cmd == "pray":
            if not tomb_pray_used:
                print("You kneel and pray for your ancestors.")
                print("A warm light surrounds you.")
                print("You feel their forgiveness.")
                hp += 5
                print("HP +5!")
                print("===== ANCESTOR'S BLESSING =====")
                player_total_score -= 10
                tomb_pray_used = True
            else:
                print("The ancestors have already given their blessing.")
                print("No more power comes from further prayer.")
        elif cmd == "open coffin":
            print("You open a stone coffin.")
            if 'broken amulet' not in have_list and 'a magic key' not in have_list:
                print("Inside: bones and a broken amulet. And a magic key.")
                print('But as you want to touch them, the wizard sprit(which is evil to you) suddenly appears!')
                wizard_phases = [
                    {
                        "hp_threshold": 40,
                        "dialogue": "Your great-great grandfather's spirit stands before you, staff raised.(That is beause he forgot everything)",
                        "attacks": [
                            {"name": "Arcane Bolt", "description": "Purple magic streaks toward you."},
                            {"name": "Frost Barrier", "description": "Ice shards explode outward."},
                            {"name": "Time Distortion", "description": "Your movements slow to a crawl.", "stun": True}
                        ],
                        "enrage": False,
                        "score_reward": 20
                    },
                    {
                        "hp_threshold": 20,
                        "dialogue": "\"You have grown strong... but you still do not understand the curse.\"",
                        "attacks": [
                            {"name": "Ancient Seal", "description": "Glowing runes bind your body.", "armor_break": True, "stun": True},
                            {"name": "Soul Burst", "description": "Raw spiritual power detonates around you."}
                        ],
                        "enrage": True,
                        "score_reward": 30
                    },
                    {
                        "hp_threshold": 8,
                        "dialogue": "\"Very well... I will show you my full power!\"",
                        "attacks": [
                            {"name": "Final Judgment", "description": "All light fades as pure magic descends.", "lifesteal": True, "curse": True},
                            {"name": "Bloodline Strike", "description": "Your very blood resonates with the attack."}
                        ],
                        "enrage": True,
                        "score_reward": 50
                    }
                ]
                boss_fight("Ancestral Wizard Spirit", 35, 5, wizard_phases, '?????', "final_wizard")
            if "broken amulet" not in have_list:
                have_list.append("broken amulet")
                print("You take the broken amulet.")
            if 'a magic key' not in have_list:
                have_list.append('a magic key')
                print('You take away the magic key.')
                player_total_score += 10
        elif cmd == "leave" or cmd == "back":
            print("You leave the tomb and return to the end of road.")
            gamestart()
        elif cmd == "bag":
            for item in have_list:
                print(item)
        elif cmd == "burp":
            print("You burp loudly. A ghost says: 'So rude!'")
        elif cmd == "sing baby shark":
            print("You sing Baby Shark. All ghosts run away.")
        elif cmd == "hide":
            print("You hide behind a stone. Ghosts pretend not to see you.")
        elif cmd == "blow kiss":
            print("You blow a kiss to the ghost. They float away, they are shy!")
        elif cmd == "nap":
            print("You take a short nap. Ghosts watch you sleep.")
        elif cmd == "truth":
            print("You speak the truth: 'I know who I am.'")
            print("The tomb shakes. The walls show all your past lives.")
            print("You understand everything.")
            print("===== TOMB TRUTH ENDING =====")
            game_over = True
            game_back = True
            break
        elif cmd == "tiktok":
            print("You try to film a TikTok in the tomb.")
            print("All ghosts hide quickly. They are shy!")
        elif cmd == "snore":
            print("You pretend to snore loudly.")
            print("A ghost says: 'BE QUIET!!!'")
        else:
            print("Unknown command.")

    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return

# misty swamp
def misty_swamp():
    global game_over, hp, have_list, time_period, good, evil, rune2, game_back, swamp_quest, swamp_visited, lily_count,cleared_ending,swamp_spirit_story,misty_end,has_death_corpse,death_corpse_item,death_location,four_hole_in,night
    global swamp_quest_done
    global player_total_score

    print("\n=== MISTY SWAMP ===")
    print("Thick fog covers the marsh. Every step is dangerous.")
    print('TYPE ‘quest’ for a quest, and if you are in a quest, type talk to talk to the ghost, ask past to ask past, ask for xxxxxxxx')
    if play_count == 1:
        print('You see a pass full of water, type dive to dive into,')
    if time_period == "night":
        print("Danger rises at night. Toxins grow stronger.")   

    if "a swamp herb" not in have_list:
        print("You notice a swamp herb growing near the entrance.")
        print("So you pick it.")
        print("A voice booms: You can only eat it in the swamp.")
        have_list.append("a swamp herb")

    swamp_visited = True
    swamp_quest = False
    lily_count = 0

    while True:
        print('You see a deep hole with some runed rope, type down to go down.')
        if has_death_corpse and death_location == current_room:
            print('You see here a corpse, type corpse to search it.\n')
        advance_time()
        consume_step_durability()
        scmd = input("swamp> ").strip().lower()
        if handle_terminal_cmd(scmd):
            continue
        if scmd == "west" or scmd == "back" or scmd == "leave":
            print("You walk out of the swamp and return to the forest.")
            return
        elif scmd == 'dive':
            if play_count == 1:
                print('You dive into a sewer.')
                sewer()
            else:
                print('The sewer had already closed forever.')
        elif scmd == 'down':
            if four_hole_in == False:
                pendulum_mortuary()
            else:
                print('You do not want to go in again.')
        elif scmd == "look":
            print("Fog blocks your sight. Dim glimmers flicker in the distance.")
        elif scmd == "hp":
            print(f"HP: {hp}")
        elif scmd == "bag":
            for item in have_list:
                print(item)
        elif scmd == "moral":
            print(f"Good: {good} | Evil: {evil}")
        elif scmd == "quest":
            if not swamp_quest_done:
                swamp_quest = True
                print("A lost spirit appears")
                print("Bring 3 lilies to help it rest")
                print('Type find lily to find lily.')
                print('Type turn in if you find three lily.')
            else:
                print("The spirit has already found peace.")
        elif scmd == "find lily" and swamp_quest:
            rnd = random.randint(1,6)
            if rnd == 1:
                print('A bad sprit hit you, then hide away.')
                print('Evil +10')
                evil += 10
            if rnd == 3:
                lily_count += 1
                print("You found a pure white lily. It emits soft light.")
            elif rnd == 4:
                lily_count += 1
                have_list.append("dewdrop")
                print("You found a lily and a crystal dewdrop!")
                print('A voice booms: You can only use the dewdrop in the swamp.')
                print('Type use dewdrop to use it.')
            elif rnd == 5:
                lily_count += 1
                good += 5
                print("A spirit guides you to a lily, blessing you.")
            else:
                print("You walk past small frogs, they hop playfully away.")
        elif scmd == "use dewdrop" and "dewdrop" in have_list:
            hp += 8
            good += 6
            have_list.remove("dewdrop")
            print("Crystal dewdrop melts into warm healing light.")
        elif scmd == "turn in" and swamp_quest and lily_count >= 3:
            have_list.append("swamp pendant")
            good += 15
            print("The spirit holds the lilies close, its form grows brighter.")
            print("Thank you for your kindness. Take this gift as my gratitude.")
            print('The ghost gives you a swamp pendant.')
            print('Now, you can choose an ending of swamp. Type swamp ending / peace leave / drain spirit to choose an ending.')
            lily_count = 0
            player_total_score += 10
            swamp_quest = False
        elif scmd == "progress" and swamp_quest:
            print(f"Lily collected: {lily_count} / 3. Keep going!")
        elif scmd == "tips":
            print("Find lilies, help the spirit, and the swamp will bless you.")

        elif scmd == "swamp ending" and "swamp pendant" in have_list and good >= 20:
            print("\n===== SWAMP GUARDIAN ENDING =====")
            print("The swamp is purified! All toxins fade away.")
            print('A voice booms: Thank you, mortal. I will give you a gift.')
            print('You receive 30 hp.')
            player_total_score += 35
            hp += 30
            print('HP +20')
            misty_end = True
            gamestart()
            return

        elif scmd == "peace leave" and "swamp pendant" in have_list:
            print("\n===== SWAMP PEACE ENDING =====")
            print("The swamp calms. You leave without curse or harm.")
            print('HP +5')
            hp += 5
            player_total_score += 10
            good += 5
            misty_end = True
            gamestart()
        elif scmd == "examine corpse" or scmd == 'corpse' or scmd == 'search corpse' or scmd == 'find corpse':
            if has_death_corpse and death_location == current_room:
                print("\nA corpse slumps against the dusty floor. It wears your exact clothes.")
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print("Nothing useful left on the body.")
                has_death_corpse = False
            else:
                print("There is not any corpse..")
        elif scmd == "drain spirit" and swamp_quest:
            print("\n===== SWAMP CURSE ENDING =====")
            print("You drain the spirit’s power. The swamp darkens.")
            evil += 25
            hp += 5
            print("A shadow follows you...")
            player_total_score += 5
            misty_end = True
            gamestart

        elif scmd == "search":
            find = random.randint(1, 3)
            if find == 1 or find == 2:
                print("You find a swamp herb.")
                have_list.append("a swamp herb")
            else:
                print("You find nothing but mud.")
        elif scmd == "help soul":
            if 'some water in the bottle' in have_list:
                have_list.remove('some water in the bottle')
                print("You aid a trapped swamp spirit.")
                good += 15
                have_list.append("healing potion")
            else:
                print('You do not have water to help soul.')
        elif scmd == "steal soul":
            print("You drain power from the spirit.")
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
            print("The floating spirit drifts closer, its voice soft and sad.")
            print("I was a traveler long ago. I lost my way in this swamp.")
            print("I knew the guardian of the cave, your ancestors. We were old friends.")
            print("I chose to stay here, guarding this misty land, so no one else gets trapped.")
            print("The lilies you collect are flowers I loved when I was alive.")
            if festival_mode:
                print("Under the full moon, old memories become warm.")
                print("The spirit shares a wisp of moonlight with you. HP +3")
                hp += 3
        elif scmd == "ask past" and swamp_quest:
            print("Past days... I watched countless people come and go.")
            print("Most chased treasure in the cave, few noticed the pain hidden there.")
            print("I wait here, hoping someone can end the endless cycle one day.")
            faith += 5
        elif scmd == "ask" and swamp_quest:
            if swamp_spirit_story == 0:
                print("Spirit: I was her handmaiden, when she was still human.")
                print("Spirit: The lady was kind. She never hurt anyone.\n")
                print('Still type ask for more.')
                swamp_spirit_story = 1
            elif swamp_spirit_story == 1:
                print("Spirit: When she was sealed away, I chose to stay here.")
                print("Spirit: I waited for someone to set her free\n")
                swamp_spirit_story = 2
            elif swamp_spirit_story == 2:
                print("Spirit: You have her eyes. You really are her descendant.")
                print("Spirit: Please, be gentle with her. She's suffered enough.\n")
                good += 10
                faith += 10
                swamp_spirit_story = 3
                player_total_score += 5
            else:
                print("The spirit floats silently among the lilies.")
        else:
            print("Unknown command.")

        toxin = 1
        if time_period == "night":
            toxin = 2
        hp -= toxin
        print(f"Swamp toxins burn you! HP -{toxin}")

        if hp <= 0:
            print("\n===== SWAMP DEATH ENDING =====")
            print("You are swallowed by the swamp...")
            jump_scare_face('flash')
            game_over = True
            game_back = True
            break

def developer_room():
    global hp, have_list, good, evil, rune1, rune2, rune3, trap_protect, festival_mode
    global meta_file_tier
    global player_total_score

    write_creepy_desktop_file(3)
    print("\n" + "="*60)
    print("               DEVELOPER ROOM")
    print("="*60)
    print("Welcome, dev tester! You can cheat here.")
    print("Commands: heal, max, godmode, leave")
    print("="*60)

    while True:
        cmd = input("dev> ").strip().lower()
        if cmd == "heal":
            hp += 10
            print("HP +10!")
            player_total_score -= 30
        elif cmd == "max":
            hp += 10
            good += 10
            evil = 0
            print("HALF MAX STATS!")
            player_total_score -= 50
        elif cmd == "godmode":
            trap_protect = True
            festival_mode = True
            hp += 10
            print("GOD MODE ACTIVATED!")
            player_total_score -= 45
        elif cmd == "leave" or cmd == "back":
            print('')
            print("You left the dev room.")
            print('')
            gamestart()
            return
        elif cmd == "bag":
            for item in have_list:
                print(item)
        else:
            print("Unknown command.")

# watchtower
def watchtower():
    global hp, have_list, good, evil, game_over, game_back,map_unlocked,cleared_ending
    global player_total_score

    print("\n=== ABANDONED WATCHTOWER ===")
    print("A crumbling stone tower stands here. Climb steps to reach the top.")
    print("Wind howls through broken windows.")
    print('Type up or down and look to play.')

    floor = 1
    while True:
        advance_time()
        consume_step_durability()
        cmd = input("tower> ").strip().lower()
        if cmd == "climb" or cmd == "up":
            if floor == 1:
                print("You climb to FLOOR 2. Dust and old ropes cover the walls.")
                floor = 2
            elif floor == 2:
                print("You climb to FLOOR 3. A small window overlooks the forest.")
                floor = 3
            elif floor == 3:
                print("You climb to FLOOR 4. A ghost sits quietly, watching the view.")
                print('Type ask story to ask past.')
                floor = 4
            elif floor == 4:
                print("You reach the TOP FLOOR! A huge panorama unfolds.")
                floor = 5
            elif floor == 5:
                print("You are already at the top!")

        elif cmd == "down":
            if floor > 1:
                floor -= 1
                print(f"You go down to FLOOR {floor}.")
            else:
                print("You are already at the bottom.")

        elif cmd == "look":
            if floor == 1:
                print("Old wooden door, broken stairs. Climb to go up.")
            elif floor == 2:
                print("Faint carvings on the wall: 'The view sets you free'.")
            elif floor == 3:
                print("You see the swamp, forest, and camp from here.")
            elif floor == 4:
                print("A ghost stares at the horizon. It doesn't want to hurt you.")
            elif floor == 5:
                print("\n=============================================")
                print("         ABANDONED WATCHTOWER - TOP")
                print("=============================================\n")
                print("Overlooking the entire land:")
                print("Forest (East) → Misty Swamp")
                print("Haunted Hut (West) → Altar & Dark Cave")
                print("Abandoned Camp (South) → Graveyard & Ancient Tomb")
                print("This watchtower stands in the north.")
                print("\nFull world map unlocked! You know every path now.")
                map_unlocked = True
                if "a bird feather" not in have_list:
                    have_list.append("a bird feather")
                    print("You found a bird feather. Type 'give feather' to hand it over to the ghost below.")

        elif cmd == "ask story" and floor == 4:
            if tower_ghost_story == 0:
                print("Ghost: I was the wizard's apprentice, long ago.")
                print("Ghost: I watched him seal the one he loved. I couldn't stop him.\n")
                print('Still type for more.')
                tower_ghost_story = 1
            elif tower_ghost_story == 1:
                print("Ghost: He told me to watch over the land, wait for his descendant.")
                print("Ghost: I waited. Hundreds of winters passed.\n")
                tower_ghost_story = 2
            elif tower_ghost_story == 2:
                print("Ghost: He was not a bad man. He was just too scared to lose her.")
                print("Ghost: Don't judge him too harshly.\n")
                player_total_score += 10
                faith += 5
                good += 5
                tower_ghost_story = 3
            else:
                print("The ghost goes back to staring at the horizon.")
        elif cmd == 'fight ghost' and floor == 4 or cmd == 'kill ghost' and floor == 4 or cmd == 'attack ghost' and floor == 4:
            print('The ghost does not want to fight with you and your hit do not hurt her.')
        elif cmd == "give feather":
            if "a bird feather" in have_list:
                print("The ghost smiles. It slowly fades away in peace.")
                have_list.remove("bird feather")
                player_total_score += 5
                good += 10
                hp += 3
                print("HP +3 | Good +10")
            else:
                print("You have no feather to give.")

        elif cmd == "leave" or cmd == "back" or cmd == "exit":
            print("You leave the watchtower and return to the road.")
            return

        elif cmd == "hp":
            print(f"HP: {hp}")
        elif cmd == "bag":
            for item in have_list:
                print(item)
        elif cmd == "moral":
            print(f"Good: {good} | Evil: {evil}")
        else:
            print("Unknown command.")

# ===================== PRINT VERSION - CELESTIAL REALM =====================
def print_heaven():
    global player_total_score
    print("="*60)
    print("               CELESTIAL REALM")
    print("="*60)
    print("A blinding light surrounds you. You have ascended to heaven.")
    print("Angels sing in the distance. The air is pure and peaceful.")
    print("You have broken the cycle of death and rebirth.")
    print('You now relised that your great-great grandfather the wizard is in fact a god.')
    print('He create this world, and all of the diarys, just to exam you. Now you pass it.')
    print('All is just a lie!')
    print("Now, you must decide the fate of all souls.")
    print("="*60)

    while True:
        print("\n[CELESTIAL REALM]")
        print("1. ANGEL SQUARE")
        print("2. HOLY LIBRARY")
        print("3. CREATION TEMPLE")
        print("4. RETURN TO MORTAL WORLD")
        print("5. FINAL JUDGEMENT")
        opt = input("> ").strip().lower()

        if opt == "1":
            print("\n===== ANGEL SQUARE =====")
            print("Countless angels gather here, praising the light.")
            print("An archangel approaches you.")
            print("'You have proven yourself worthy. What do you seek?'")
            print("Choose: ask for power / ask for peace / ask for forgiveness")
            choice = input().strip().lower()
            if choice == "ask for power":
                print("The archangel grants you divine power.")
                print("HP: 999 | Good: +50")
                print("You obtained DIVINE SWORD!")
            elif choice == "ask for peace":
                print("The archangel blesses all souls.")
                print("All ghosts in the mortal world find peace.")
                print("Good: +100")
            elif choice == "ask for forgiveness":
                print("The archangel forgives all sins.")
                print("Evil: 0 | Good: +75")

        elif opt == "2":
            print("\n===== HOLY LIBRARY =====")
            print("Books containing all knowledge of the universe line the walls.")
            print("You find a book titled 'The True History of the Curse'.")
            print("It reveals that the wizard and his wife were not the first.")
            print("The cycle has repeated for thousands of years.")
            print("But you are the first to break it.")
            print("Faith: +20")
            print("You obtained BOOK OF TRUTH!")
        elif opt == "3":
            print("\n===== CREATION TEMPLE =====")
            print("The source of all light and life.")
            print("You see the Creator sitting on a throne of stars.")
            print("'You have done well, my child. Now, what will you do?'")
            print("Choose: 1.become a god / 2.return to earth / 3.create a new world")
            choice = input().strip().lower()
            if choice == "become a god" or choice == '1':
                print("\n✨ GODHOOD ENDING ✨")
                print("You become a god, watching over all worlds.")
                print("You ensure that no one ever suffers like your family did.")
                show_message_wall()
                name = input("Your name: ").strip().lower()
                msg = input("Your message: ").strip().lower()
                save_message(name, msg)
                print('')
                print('You can final see what you can cheat:')
                print("=== Death Adventure Cheat ===")
                print("Usage: python3 main.py [OPTIONS]")
                print("Options:")
                print("  -g, -G, -godmode    Enable god mode (invincible)")
                print("  -c, -C, -cheat      Enable cheat mode (all items)")
                print("  -h, -help           Show help")
                print("=============================")
                player_total_score += 50
                end_score_rating()
                print("=== Death Adventure v1.4 - Official Release ===")
                print("Thank you for playing!")
                exit()
            elif choice == "return to earth" or choice == '2':
                print("\n🌍 MORTAL ENDING 🌍")
                print("You choose to return to earth and live a normal life.")
                print("You marry, have children, and die peacefully.")
                print("The curse is gone forever.")
                show_message_wall()
                name = input("Your name: ").strip().lower()
                msg = input("Your message: ").strip().lower()
                save_message(name, msg)
                print('')
                print('You can final see what you can cheat:')
                print("=== Death Adventure Cheat ===")
                print("Usage: python3 main.py [OPTIONS]")
                print("Options:")
                print("  -g, -G, -godmode    Enable god mode (invincible)")
                print("  -c, -C, -cheat      Enable cheat mode (all items)")
                print("  -h, -help           Show help")
                print("=============================")
                player_total_score += 50
                end_score_rating()
                print("=== Death Adventure v1.4 - Official Release ===")
                print("Thank you for playing!")
                exit()
            elif choice == "create a new world" or choice == '3':
                print("\n🌌 CREATOR ENDING 🌌")
                print("You create a new world where love and peace reign.")
                print("No more pain, no more suffering, no more cycles.")
                show_message_wall()
                name = input("Your name: ").strip().lower()
                msg = input("Your message: ").strip().lower()
                save_message(name, msg)
                print('')
                print('You can final see what you can cheat:')
                print("=== Death Adventure Cheat ===")
                print("Usage: python3 main.py [OPTIONS]")
                print("Options:")
                print("  -g, -G, -godmode    Enable god mode (invincible)")
                print("  -c, -C, -cheat      Enable cheat mode (all items)")
                print("  -h, -help           Show help")
                print("=============================")
                player_total_score += 50
                end_score_rating()
                print("=== Death Adventure v1.4 - Official Release ===")
                print("Thank you for playing!")
                exit()

        elif opt == "4":
            print("You return to the mortal world.")
            main()
            return

        elif opt == "5":
            print("\n===== FINAL JUDGEMENT =====")
            print("All souls gather before you.")
            print("You must decide their fate.")
            print("Choose: 1.judge all / 2.forgive all / 3.let them choose")
            choice = input().strip().lower()
            if choice == "judge all" or choice == '1':
                print("\n⚖️ JUDGEMENT ENDING ⚖️")
                print("You judge each soul based on their deeds.")
                print("Good souls go to heaven, evil souls go to hell.")
                print("Balance is restored to the universe.")
            elif choice == "forgive all" or choice == '2':
                print("\n❤️ FORGIVENESS ENDING ❤️")
                print("You forgive all souls, regardless of their deeds.")
                print("Everyone is given a second chance.")
                print("Love conquers all.")
            elif choice == "let them choose" or choice == '3':
                print("\n🆓 FREEDOM ENDING 🆓")
                print("You let each soul choose their own fate.")
                print("Some choose heaven, some choose hell, some choose to reincarnate.")
                print("True freedom is the greatest gift.")

            print("\n=== END OF THE JOURNEY ===")
            print("You have completed all four runs of Death Adventure.")
            show_message_wall()
            name = input("Your name: ").strip().lower()
            msg = input("Your message: ").strip().lower()
            save_message(name, msg)
            print('')
            print('You can final see what you can cheat:')
            print("=== Death Adventure Cheat ===")
            print("Usage: python3 main.py [OPTIONS]")
            print("Options:")
            print("  -g, -G, -godmode    Enable god mode (invincible)")
            print("  -c, -C, -cheat      Enable cheat mode (all items)")
            print("  -h, -help           Show help")
            print("=============================")
            player_total_score += 50
            end_score_rating()
            print("=== Death Adventure v1.4 - Official Release ===")
            print("Thank you for playing!")
            exit()
        elif opt == "6":
            jump_scare_face('flash')
            print('Wait, where is the 6? I only have five!')
            print('However, you find a titan in the secret room.')
            titan_guardian_easter()

def time_travel_origin():
    global good, evil, hp, game_over, game_back, cleared_ending
    global player_total_score

    print("\n" + "="*60)
    print("=========== TIME TRAVEL · 100 YEARS AGO ============")
    print("="*60)
    print("A strong light wraps you. You travel back to the past.")
    print("You see the young wizard & his wife before the curse...")
    print("You can change their fate.")
    print("="*60)

    past_phase = 1

    while True:
        print(f"\n--- PAST PHASE {past_phase} ---")
        cmd = input("past> ").strip().lower()

        if past_phase == 1:
            if cmd == "look":
                print("A quiet village. Young wizard is reading, his lover sits beside him.")
            elif cmd == "talk":
                print("You tell them about the future curse.")
                print("The young wizard looks scared: 'I will never hurt her...'")
                player_total_score += 30
                past_phase = 2
            elif cmd == "leave":
                print("You return to modern time.")
                gamestart()
                return
            else:
                print("Try 'look' or 'talk'")

        elif past_phase == 2:
            if cmd == "look":
                print("Evil men hurt the wizard’s wife. She is dying.")
            elif cmd == "help":
                print("You save her! The tragedy is avoided!")
                player_total_score += 30
                good += 99
                past_phase = 3
            elif cmd == "watch":
                print("You do nothing. She turns into a succubus.")
                player_total_score -= 100
                evil += 50
                past_phase = 3
            else:
                print("Try 'help' or 'watch'")

        elif past_phase == 3:
            if cmd == "look":
                print("The moment that decides everything.")
            elif cmd == "stop seal":
                print("\n✨ PERFECT ORIGIN ENDING ✨")
                print("You stop the seal. No curse. No pain.")
                print("The family cycle is BROKEN FOREVER.")
                cleared_ending = True
                player_total_score += 100
                main()
            elif cmd == "let seal":
                print("\n⚪ NORMAL ORIGIN ENDING ⚪")
                print("History remains. Curse continues.")
                player_total_score += 100
                main()
                return
            elif cmd == "unite":
                print("\n🌟 TRUE TIME ENDING 🌟")
                print("You unite two souls. Love defeats everything.")
                print("THIS IS THE ULTIMATE ENDING OF THE GAME.")
                player_total_score += 100
                cleared_ending = True
                main()
                return
            else:
                print("Choose: stop seal / let seal / unite")

        if game_over:
            print("\n=== TIME TRAVEL END ===")
            print("Type 'menu' to return")
            while True:
                c = input().strip().lower()
                if c == "menu":
                    main()
                    return

def jump_scare_face(mode="normal"):
    if mode == "flash":
        for i in range(30):
            print("\n")
        print("█████████████████████████")
        print("█░░░░░░░░░░░░░░░░░░░░░░░█")
        print("█░░  ◉          ◉    ░░█")
        print("█░░                  ░░█")
        print("█░░      ▄▄▄▄▄       ░░█")
        print("█░░     ███████      ░░█")
        print("█░░    █████████     ░░█")
        print("█░░                  ░░█")
        print("█░░░░░░░░░░░░░░░░░░░░░░░█")
        print("█████████████████████████")
        for i in range(50):
            print("\n")
            time.sleep(0.002)
        print("... Anything?")
    elif mode == "bloody":
        print("          .---.          ")
        print("         /     \\         ")
        print("        |  ✖   ✖  |        ")
        print("        |  \\   /  |        ")
        print("        |   \\ /   |        ")
        print("       /|        |\\       ")
        print("      / |  ____  | \\      ")
        print("     /  | |    | |  \\     ")
        print("    /   |_|    |_|   \\    ")
        print("   /          ▼         \\   ")
        print("  /_____________________\\  ")
        print("   ||  ||  ||  ||  ||     ")
        print("   vv  vv  vv  vv  vv     ")
    else:
        print("        .-'''-.        ")
        print("       /       \\       ")
        print("      |  O   O  |      ")
        print("      |    ▼    |      ")
        print("      \\  \\___/  /      ")
        print("       \\       /       ")
        print("        '-...-'        ")
        print("      ||       ||      ")
        print("       \\       /       ")
        print("        `-----'        ")

def hill():
    global current_room,hp,evil,good,game_back,game_over,cleared_ending,map_unlocked,hill_diary_read,grandmother
    global defeated_enemies
    global player_total_score

    high = 0
    current_room = 'hill'
    if 'hungry_ghoul' not in defeated_enemies:
        print('A ghoul find you.')
        combat("hungry ghoul", 11, 4, "ghoul claw", 5, enemy_id = "hungry_ghoul")
    print('You are now at the bottom of the hill, type climb to climb, look to look around.')
    while True:
        advance_time()
        consume_step_durability()
        cmd = input().strip().lower()
        if cmd == 'climb':
            if high == 0:
                high = 1
                print('You climb up the mountain, you see a statue of a wizard and still a lot of stairs up the mountain.')
            elif high == 1:
                high = 2
                print('There is still some very old stairs to the top.')
                print('You climb up the old stairs, you see an arrow shoot at you by it self!')
                x = random.randint(1,2)
                if x == 1:
                    print('It gets you, Hp -5!')
                    hp -= 5
                    if hp <= 0:
                        print('You was killed by the arrow.')
                        game_over = True
                        game_back = True
                        break
                else:
                    print('It misses!')
                if 'a book' not in have_list:
                    print('You see here a book, so you pick it up. Type read book to read it.')
                    have_list.append('a book')
                else:
                    print('There is nothing, just a lot of mud.')
            elif high == 2:
                high == 3
                print('You are at the top of the hill, the view is amazing here.')
                print('You unlock the map!')
                print('There is nothing special expect the brilliant view.')
                print('You can go down now.')
                map_unlocked = True
        elif cmd == 'read book' and 'a book' in have_list or cmd == 'read' and 'a book' in have_list:
            print('\nYou read the book, it says:')
            print('Book page 1:')
            print('Hahaha, man, if you read my book, you must have see my arrow trap!')
            print('Man, I am the human who killed wizard wife.\n')
            print('Book page 2:')
            print('I kill she because her husband -- the wizard is not a good man.')
            print('Let me tell you about him.\n')
            print('Book page 3:')
            print('He is the most powerful wizard in the world, but he did not do a lot of good things.')
            print('For example, he killed a man who just laughed at his clothes!\n')
            print('Book page 4:')
            print('He is so evil, and I am his employee.')
            print('I was angry with his rude, so I killed his wife.\n')
            print('The last page of the book:')
            print('His wife became a succubus, but she did not kill me, the one who killed me is in fact the wizard!')
            print('Then, he told people to build a statue and the stone in the church just to let people know that he is a good man!\n')
            print('The end of the book.')
            player_total_score += 10
            if grandmother == True:
                print('You are extremely confused, which of the note is right!')
                player_total_score += 10
        elif cmd == 'look' and high == 0:
            print('Just a way back to the campsite.')
        elif cmd == 'look' and high == 1:
            print('The statue may have been here for hundreds of years, it have a faint light surround it.')
        elif cmd == 'look' and high == 2:
            print('An invisible arrow trap and a lot of mud.')
        elif cmd == 'look' and high == 3:
            print('Nothing special, just some butterflies and some mosquite.')
        elif cmd == 'touch statue':
            print('The statue is cold.')
        elif cmd == 'leave' or cmd == 'back' or cmd == 'down' and high == 0:
            print('You climb down the hill and back to the road.')
            gamestart()
            return
        elif cmd == 'leave' or cmd == 'back' or cmd == 'down' and high == 1:
            high = 0
            print('You climb down the mountain, you are at the bottom of the mountain again.')
        elif cmd == 'leave' or cmd == 'back' or cmd == 'down' and high == 2:
            high = 1
            print('You climb down the old stairs, you find an arrow is ready to shoot again!')
        else:
            print('Unknown command.')
    if game_over == True:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == 'menu':
                main()
                return
            else:
                print('Please answer the question.')

def underwater_ruins():
    global hp, good, evil, have_list, game_over, game_back, current_room
    global underwater_visited, oxygen, diving_suit_obtained 
    global water_rune_1, water_rune_2, water_rune_3, pearl_obtained
    global underwater_ending_unlocked
    global has_death_corpse, death_location, death_corpse_item
    global sewer_in
    global player_total_score

    current_room = "sunken_temple"
    underwater_visited = True

    print("\n==================== SUNKEN TEMPLE RUINS ====================")
    print("Cold dark water surrounds you. Bubbles rise slowly from the stone floor.")
    print("Ancient sea god carvings cover every wall, glowing faintly blue.")
    print("Your oxygen is limited. Find air pockets or you will drown.")
    if light == True:
        print('Your light gones down by the water.')
        light = False
    print("Oxygen starts at 6. Every action consumes 1 oxygen.")

    oxygen = 6
    current_zone = "flooded_corridor"
    rune_order = 0
    correct_runes = ["tide", "abyss", "storm"]

    while True:
        oxygen -= 1
        if oxygen <= 0:
            print("You run out of air. Water fills your lungs.")
            hp -= 3
            if hp <= 0:
                print("You drown in the dark temple.")
                game_over = True
                game_back = True
                break
            print("You gasp and barely survive. HP -3")
            player_total_score -= 5
            oxygen = 2

        if has_death_corpse and death_location == current_room:
            print('You see a corpse on the seabed. Type corpse to search it.\n')

        cmd = input("underwater> ").strip().lower()
        if handle_terminal_cmd(cmd):
            continue

        if cmd == "back" or cmd == "surface":
            print("You swim back up to the cave tunnel.")
            break

        elif cmd == "bag":
            for item in have_list:
                print(item)
            continue

        elif cmd == "hp":
            print(f"HP: {hp}")
            continue

        elif cmd == "oxygen":
            print(f"Oxygen remaining: {oxygen}")
            continue

        elif cmd == "corpse" or cmd == "search corpse":
            if has_death_corpse and death_location == current_room:
                print("\nA drowned explorer lies on the stone.")
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print("Nothing useful left.")
                has_death_corpse = False
            else:
                print("There is no corpse here.")

        elif current_zone == "flooded_corridor":
            if cmd == "look":
                print("A long stone corridor half-buried in silt.")
                print("Three paths: forward to shrine, left to air pocket, right to treasury.")
                print("A faded rune glows on the left wall.")
            elif cmd == "forward":
                current_zone = "rune_shrine"
                print("You swim forward into the central rune shrine.")
            elif cmd == "left":
                current_zone = "air_pocket"
                print("You swim left into a small cave with breathable air.")
            elif cmd == "right":
                current_zone = "deep_treasury"
                print("You swim right into the sunken treasure room.")
            elif cmd == "examine rune":
                if not water_rune_1:
                    water_rune_1 = True
                    print("First water rune: TIDE")
                    print("It pulses with slow, steady energy.")
                else:
                    print("You already studied this rune.")
            else:
                print("Unknown command. Try 'look'.")

        elif current_zone == "air_pocket":
            if cmd == "look":
                print("A small cave with an air bubble at the top.")
                print("You can breathe here to restore oxygen.")
                print("A second rune is carved into the cave ceiling.")
            elif cmd == "breathe" or cmd == 'breath':
                oxygen = 10
                print("You take deep breaths. Oxygen restored to full.")
            elif cmd == "examine rune":
                if not water_rune_2:
                    water_rune_2 = True
                    print("Second water rune: ABYSS")
                    print("It hums with deep, silent power.")
                    player_total_score += 10
                else:
                    print("You already studied this rune.")
            elif cmd == "back":
                current_zone = "flooded_corridor"
                print("You swim back to the corridor.")
            else:
                print("Unknown command. Try 'breathe' or 'look'.")

        elif current_zone == "rune_shrine":
            if cmd == "look":
                print("A circular shrine with three stone altars underwater.")
                print("You must activate the runes in the correct order.")
                print("Type 'activate [rune]' to press an altar.")
                print("Wrong order will trigger a water jet attack.")
            elif cmd.startswith("activate "):
                rune_name = cmd.split()[1] if len(cmd.split()) > 1 else ""
                if rune_name not in ["tide", "abyss", "storm"]:
                    print("Unknown rune.")
                    continue
                if rune_name == correct_runes[rune_order]:
                    rune_order += 1
                    print(f"Rune {rune_name} glows bright blue.")
                    if rune_order == 3:
                        print("All runes align. A hidden passage opens upward.")
                        print("A glowing pearl rises from the depths.")
                        player_total_score += 10
                        if not pearl_obtained:
                            have_list.append("water-breathing pearl")
                            pearl_obtained = True
                            hp += 10
                            good += 10
                            print("You obtained the WATER-BREATHING PEARL.")
                            print("You will never drown in dark waters again.")
                            underwater_ending_unlocked = True
                else:
                    hp -= 3
                    print("Wrong rune! Pressurized water slams into you. HP -3")
                    player_total_score -= 15
                    rune_order = 0
                    if hp <= 0:
                        print("You are knocked unconscious and drown.")
                        game_over = True
                        game_back = True
                        break
            elif cmd == "back":
                current_zone = "flooded_corridor"
                print("You swim back to the corridor.")
            else:
                print("Unknown command. Try 'look'.")

        elif current_zone == "deep_treasury":
            if cmd == "look":
                print("A sunken treasure room filled with broken chests and coral.")
                print("A third rune is carved on the far wall.")
            elif cmd == "examine rune":
                if not water_rune_3:
                    water_rune_3 = True
                    print("Third water rune: STORM")
                    print("It crackles with wild, violent energy.")
                    player_total_score += 10
                else:
                    print("You already studied this rune.")
            elif cmd == "search":
                find = random.randint(1, 3)
                if find == 1:
                    print("You find gold coins in a broken chest.")
                    have_list.append("gold coins")
                elif find == 2:
                    print("You find an ancient sea amulet.")
                    have_list.append("sea amulet")
                else:
                    print("Only rust and coral.")
                    print('Hp -5')
                    player_total_score -= 10
                    hp -= 5
            elif cmd == "back":
                current_zone = "flooded_corridor"
                print("You swim back to the corridor.")
            else:
                print("Unknown command. Try 'look'.")

        else:
            print("Unknown command.")

    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return

def sewer():
    global hp,old_diary_readed,old_note_readed,game_back,game_over,has_death_corpse,death_corpse_item,death_location,current_room

    current_room = 'sewer'
    print('You crawl into a DARK SEWER TUNNEL.')
    print('You see here something is shinning in the deep.')
    print('TYPE deep or go deep to go deep, and you see a water path to east and a way up.')
    while True:
        if has_death_corpse and death_location == current_room:
            print('You see here a corpse, type corpse to search it.\n')
        consume_step_durability()
        sewer_cmd = input('sewer> ').strip().lower()
        if sewer_cmd == 'west' or sewer_cmd == 'back' or sewer_cmd == 'leave':
            current_room = 'first go'
            cave()
            return
        elif sewer_cmd == 'up':
            misty_swamp()
            return
        elif sewer_cmd == 'east' or sewer_cmd == 'e' or sewer_cmd == 'go east':
            if sewer_in == False:
                underwater_ruins()
                continue
            else:
                print('You have already gone in.')
        elif sewer_cmd == "examine corpse" or sewer_cmd == 'corpse' or sewer_cmd == 'search corpse' or sewer_cmd == 'find corpse':
            if has_death_corpse and death_location == current_room:
                print("\nA corpse slumps against the dusty floor. It wears your exact clothes.")
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print("Nothing useful left on the body.")
                has_death_corpse = False
            else:
                print("There is not any corpse..")
        elif sewer_cmd == 'forward':
            jump_scare_face('flash')
            print('Water rushes! You take damage.')
            hp -= 2
            print('hp -2')
            print('')
            print('You find a old note.')
            print('You read the note, it says:')
            print('')
            print('I have been waiting for 200 years.')
            print('I have to wait, until someone broke the curse.')
            print('My husband control me, but he is not evil. He just do not want me to destroy the world.')
            print('')
            old_note_readed = True
            if old_diary_readed == True or grave_diary_read == True:
                print('You realise that this note was written by you great-great grandmothe -- the Evil.')
            else:
                print('You: Who has written this note? It is so strange.')
            if hp <= 0:
                print('You drown. Game over!')
                game_over = True
                game_back = True
                break
        elif sewer_cmd == 'treasure':
            if not sewer_treasure_taken:
                print('You find gold coins.')
                have_list.append('gold coins')
                sewer_treasure_taken = True
            else:
                print('The treasure pile has already been looted.')
        elif sewer_cmd == "deep" or sewer_cmd == 'go deep':
            jump_scare_face('flash')
            print("You wade through dark water, reach a hidden stone door.")
            print("Ancient magic lingers here.")
            while True:
                consume_step_durability()
                deep_cmd = input("deep> ").strip().lower()
                if deep_cmd == "open door":
                    if "rune stone 1" in have_list:
                        print("Rune power unlocks the door. You enter the wizard's hidden room.")
                        print("Old table, worn staff and a letter on the desk.")
                        player_total_score += 5
                    else:
                        print("The door is sealed by rune magic.")
                elif deep_cmd == "read letter":
                    print("Letter from the wizard:")
                    print("I do not regret protecting the world, but I regret leaving her alone.")
                    print("If my descendant sees this, please be kind to her.")
                    old_note_readed = True
                elif deep_cmd == "take staff":
                    print("You pick up the wizard's old staff.")
                    have_list.append("wizard staff")
                    print("Staff: Weakens dark creatures in the cave.")
                elif deep_cmd == "leave":
                    print("You head back to the sewer tunnel.")
                    break
                else:
                    print("Unknown command.")
        elif sewer_cmd == 'bag':
            for i in have_list:
                print(i)
        else:
            print('Unknown command.')

#cave
def cave():
    global game_over, hp, have_list, light, p, amulet, map_unlocked, secret_unlocked, diary_read, legacy_unlocked, current_room, torch,rune1,rune2,rune3,rune,grandmother,gate_unlock,old_diary_readed, game_back,play_count,old_note_readed,festival_mode,cleared_ending,force_in_cave,all_collected,amulet,ng_amulet,has_elf_amulet
    global has_death_corpse, death_location, death_corpse_item
    global sewer_treasure_taken, explorer_thank_reward,sewer_in
    global meta_file_tier
    global player_total_score,orc_in,weapon_broken

    game_over = False
    while True:
        if current_room == 'entrance':
            while True:
                if has_death_corpse and death_location == current_room:
                    print('You see here a corpse, type corpse to search it.\n')
                consume_step_durability()
                op = input().strip().lower()
                if handle_terminal_cmd(op):
                    continue
                if op == 'unlock':
                    if 'a key' in have_list:
                        x = random.randint(1,5)
                        if x == 9:
                            pass
                        else:
                            if x == 8:
                                pass
                            else:
                                current_room = 'first go'
                                print('You succeed in unlock the grate. There is a path to the west.')
                                player_total_score += 10
                                print('You see here a small library, type library to go in.')
                                print('You feel that the way back is collapsed.')
                                break
                    else:
                        print('You do not have a key, you unleashed a ghost, the ghost kill you.')
                        print('If you have an amulet, you still have to be killed(laugh)')
                        print('Game over!')
                        game_over = True
                        game_back = True
                elif op == 'south':
                    print('There is no way to go to this direction.')
                elif op == 'east':
                    print('There is no way to go to this direction.')
                elif op == 'compass':
                    if 'old compass' in have_list:
                        print("Compass: You are deep in the CAVE. West goes deeper.")
                    else:
                        print("No compass available.")
                elif op == 'colin':
                    print('You go back to the house and then to the road.')
                    gamestart()
                    return
                elif op == "examine corpse" or op == 'corpse' or op == 'search corpse' or op == 'find corpse':
                    if has_death_corpse and death_location == current_room:
                        print("\nA corpse slumps against the dusty floor. It wears your exact clothes.")
                        if death_corpse_item:
                            print(f"You retrieve {death_corpse_item} from its pocket.")
                            have_list.append(death_corpse_item)
                        else:
                            print("Nothing useful left on the body.")
                        has_death_corpse = False
                    else:
                        print("There is not any corpse..")
                else:
                    print('Sorry, I do not understand that word.')
        if game_over == True:
            print("=== END ===")
            print("Type 'menu' to return main menu")
            while True:
                c = input().strip().lower()
                if c == 'menu':
                    main()
                    return
        if current_room == 'first go':
            while True:
                print('You see a sewer, type sewer to go dive into it.')
                if has_death_corpse and death_location == current_room:
                    print('You see here a corpse, type corpse to search it.\n')
                consume_step_durability()
                gocave = input().strip().lower()
                if gocave == 'east':
                    print("The way back is collapsed! You can't return unless you have a pick-axe.")
                elif gocave == 'dig':
                    if 'a pick-axe' in have_list:
                        print("YOU DUG A PATH BACK TO THE HOUSE!")
                        print("YOU ESCAPED THE CAVE!")
                        gamestart()
                        return
                    else:
                        print("YOU NEED A PICKAXE TO DIG!")
                elif gocave == "examine corpse" or gocave == 'corpse' or gocave == 'search corpse' or gocave == 'find corpse':
                    if has_death_corpse and death_location == current_room:
                        print("\nA corpse slumps against the dusty floor. It wears your exact clothes.")
                        if death_corpse_item:
                            print(f"You retrieve {death_corpse_item} from its pocket.")
                            have_list.append(death_corpse_item)
                        else:
                            print("Nothing useful left on the body.")
                        has_death_corpse = False
                    else:
                        print("There is not any corpse..")
                elif gocave == 'library':
                    print('Bookshelves full of diaries, all written by your ancestors.')
                    while True:
                        consume_step_durability()
                        lib = input('library> ').strip().lower()
                        if lib == 'read':
                            print('You read a memory:')
                            print('The wizard loved his wife more than anything.')
                            print('He sealed her to save the world, but hated himself for it.')
                            print('Every guardian since has hated their fate.')
                        elif lib == 'read all':
                            print('You absorb all memories.')
                            print('You see every guardian’s life, every pain, every choice.')
                            print('You understand everything now.')
                            faith += 10
                        elif lib == 'take book':
                            have_list.append('memory book')
                            print('You took a BOOK OF ANCESTOR MEMORIES.')
                        elif lib == 'back':
                            break
                        else:
                            print('Unknown command.')
                elif gocave == 'sewer' or gocave == 'go into sewer' or gocave == 'go into the sewer' or gocave == 'go to sewer':
                    sewer()
                elif gocave == 'west':
                    print('You walk deeper into the cave. There is still a path to west.')
                    print('You see old footprints on the ground. Someone came here before.')
                    if 'bat' not in defeated_enemies:
                        print('Suddenly, a bat appears, it wants to kill you!')
                        combat("cave bat swarm", 4, 2, None, 1,enemy_id='bat')
                        player_total_score += 10
                        current_room = 'go west'
                        break
                                
                elif gocave == 'bag':
                    for i in range(len(have_list)):
                        print(have_list[i])
                else:
                    print('Sorry, I do not understand that word.')
                if game_over == True:
                    print("=== END ===")
                    print("Type 'menu' to return main menu")
                    while True:
                        c = input().strip().lower()
                        if c == 'menu':
                            main()
                            return
                        else:
                            print('Please answer the question.')
        if current_room == 'go west':
            if has_death_corpse and death_location == current_room:
                    print('You see here a corpse, type corpse to search it.\n')
            consume_step_durability()
            west = input().strip().lower()
            if west == 'west':
                print('There is a stone path to west.')
                print('And there is also a sewer, type sewer to go in.')
                current_room = 'go west2'
            elif west == 'bag':
                for i in range(len(have_list)):
                    print(have_list[i])
            elif west == 'north':
                print('There is no way to go to this direction.')
            elif west == 'south':
                print('There is no way to go to this direction.')
            elif west == 'east':
                print('You go back to a room.')
                current_room = 'first go'
            else:
                print('Sorry, I do not understand that word.')
            if game_over == True:
                print("=== END ===")
                print("Type 'menu' to return main menu")
                while True:
                    c = input().strip().lower()
                    if c == 'menu':
                        main()
                        return
                    else:
                        print('Please answer the question.')
        if current_room == 'go west2':                       
            while True:
                if has_death_corpse and death_location == current_room:
                    print('You see here a corpse, type corpse to search it.\n')
                consume_step_durability()
                pathwest = input().strip().lower()
                if pathwest == 'west':
                    print('You see here a note. And a diary. There is still a way to west.')
                    print('There is still some old footprints to west.')
                    if has_death_corpse and death_location == current_room:
                        print('You see here a corpse, type corpse to search it.\n')
                    consume_step_durability()
                    west2 = input().strip().lower()
                    if west2 == 'west':
                        current_room = 'go west3'
                        break
                    elif pathwest == 'east':
                        print('You walk east and go back to a room.')
                        current_room = 'go west'
                        break
                    elif pathwest == "examine corpse" or pathwest == 'corpse' or pathwest == 'search corpse' or pathwest == 'find corpse':
                        if has_death_corpse and death_location == current_room:
                            print("\nA corpse slumps against the dusty floor. It wears your exact clothes.")
                            if death_corpse_item:
                                print(f"You retrieve {death_corpse_item} from its pocket.")
                                have_list.append(death_corpse_item)
                            else:
                                print("Nothing useful left on the body.")
                            has_death_corpse = False
                        else:
                            print("There is not any corpse..")
                    elif pathwest == 'bag':
                        for i in range(len(have_list)):
                            print(have_list[i])

                    else:
                        print('Sorry, I do not understand that word.')
                    if game_over == True:
                        print("=== END ===")
                        print("Type 'menu' to return main menu")
                        while True:
                            c = input().strip().lower()
                            if c == 'menu':
                                main()
                                return
                            else:
                                print('Please answer the question.')
        if current_room == 'go west3':                                          
            print('You can see a ghost, but the ghost does not see you!')
            print('You go west, you see here a human corpse, you are shocked! There is still path to west. You see here ' + p)
            print('Try touch corpse or ask about dev or west and you see a orc dungeon, type orc to go in.')
            while True:
                consume_step_durability()
                west3 = input().strip().lower()
                if west3 == 'west':
                    cave_horror_phases = [
                        {
                        "hp_threshold": 20,
                        "dialogue": "Something large drops from the cave ceiling. A pale, twisted creature blocks the path.",
                        "attacks": [
                            {"name": "Claw Maul", "description": "Long sharp claws tear at your flesh."},
                            {"name": "Bellowing Roar", "description": "Deafening scream echoes through the cave.", "stun": True}
                        ],
                        "enrage": False,
                        "score_reward": 45
                        },
                        {
                        "hp_threshold": 8,
                        "dialogue": "The creature's jaw unhinges at an impossible angle. It is about to devour you!",
                        "attacks": [
                            {"name": "Devour Bite", "description": "It lunges forward, trying to swallow you whole.", "lifesteal": True},
                            {"name": "Tail Sweep", "description": "Thick tail slams horizontally across the cave."}
                        ],
                        "enrage": True,
                        "score_reward": 70
                        }
                        ]
                    boss_fight("Cave Horror", 20, 5, cave_horror_phases, "monster fang", "cave_horror")
                    while True:
                        print("Two paths appear in front of you!")
                        print("One is BRIGHT, one is DARK")
                        choice = input("1.go bright / 2.go dark: ").strip().lower()
                        if choice == "go dark" or choice == '2':
                            print("You found DIAMONDS! You are rich!")
                            if 'a pick-axe' in have_list and 'diamond vault' in have_list:
                                print('You take all of the tresures away, you are the richest person in your country!')
                                if diary_read == True and legacy_unlocked == True:
                                    print('You fulfilled the lost explorer’s last wish.')
                                    print('His soul finally rests in peace.')
                                    player_total_score += 30
                                print('===== RICH ENDING! =====')
                                player_total_score += 75
                                game_over = True
                                game_back = True
                                cleared_ending = True
                                break
                            elif "a pick-axe" in have_list:
                                required_items = {"rope", "flint", "old compass", "an amulet", "diamond vault"}
                                if required_items.issubset(set(have_list)):
                                    all_collected = True
                                if all_collected:
                                    print("YOU HAVE COLLECTED EVERYTHING!")
                                    if diary_read == True and legacy_unlocked == True:
                                        print('You fulfilled the lost explorers last wish.')
                                        print('His soul finally rests in peace.')
                                        player_total_score += 30
                                    print("===== PERFECT ENDING =====")
                                    player_total_score += 100
                                    game_over = True
                                    game_back = True
                                    cleared_ending = True
                                    break
                                else:
                                    print("You use pick-axe to break the wall and ESCAPE!")
                                    print('You take the diamonds away!')
                                    if diary_read == True and legacy_unlocked == True:
                                        print('You fulfilled the lost explorers last wish.')
                                        print('His soul finally rests in peace.')
                                        player_total_score += 30
                                    print("===== YOU WIN ! =====")
                                    player_total_score += 50
                                    game_over = True
                                    game_back = True
                                    cleared_ending = True
                                    break
                            else:
                                print("You have treasure but can't escape... you starve.")
                                print('But you can still go to the next play count.')
                                print('Game over!')
                                player_total_score += 30
                                game_over = True
                                game_back = True
                                cleared_ending = True
                                break
                        elif choice == "go bright" or choice == '1':
                            print("It's a trap! SPIKES KILL YOU!")
                            print('You should try again and go to the dark road.')
                            print('Game over!')
                            game_over = True
                            game_back = True
                            break
                        elif choice == 'east':
                            print('You walk back to a room.')
                            break
                        elif choice == 'bag':
                            for i in range(len(have_list)):
                                print(have_list[i])
                        else:
                            print("Invalid command!")
                    if game_over == True:
                        print("=== END ===")
                        print("Type 'menu' to return main menu")
                        while True:
                            c = input().strip().lower()
                            if c == 'menu':
                                main()
                                return
                            else:
                                print('Please answer the question.')
                elif west3 == "orc":
                    if orc_in == False:
                        orc_tribe_dungeon()
                    else:
                        print('YOu have already been to it!')
                elif west3 == "hug ghost":
                    print("You hug the ghost! It panics: 'WHAT ARE YOU DOING?!'")
                    have_list.append("ghost hug")
                elif west3 == "ask about dev":
                    print("Ghost: The one who made this place?")
                    print("Ghost: He trapped us all here with bugs and typos.")
                    print("Ghost: Don't trust his 'perfect ending'.")
                elif west3 == "find secret wall":
                    if "a pick-axe" in have_list:
                        print("You break a cracked wall. A small room appears.")
                        print("Inside: an old dev test note.")
                        print('Try read read dev test note.')
                        have_list.append("dev test note")
                    else:
                        print("You need a pick-axe to break the wall.")
                elif west3 == "read dev test note":
                    if "dev test note" in have_list:
                        print("Note: 'If you are reading this, you are too deep.'")
                        print("Note: 'The real cheat code is in the house.'")
                        print("Note: 'colin -> woody -> garry. Don't tell anyone.'")
                    else:
                        print("You don't have the note.")
                elif west3 == "ghost job":
                    print("You ask what the ghost’s job is.")
                    print("Ghost: 'I just scare people who sing badly. Like you.'")
                elif west3 == "ghost bored":
                    print("You say: You look really bored.")
                    print("Ghost: 'I’ve been bored for 300 years. Help me.'")
                elif west3 == "ghost friend":
                    print("You ask: Can we be friends?")
                    print("Ghost: 'Sure! Just don’t sing again, deal?'")
                elif west3 == "ghost joke":
                    print("You tell a ghost joke: 'Why don't ghosts lie?'")
                    print("Ghost: 'Because you can see right through us!'")
                elif west3 == "ghost favorite food":
                    print("You ask: What's your favorite snack?")
                    print("Ghost: 'Ice scream! It's always to die for.'")
                elif west3 == "ghost school":
                    print("You ask if ghosts go to school.")
                    print("Ghost: 'Yeah, to learn how to BOO!'")
                elif west3 == "ghost rain":
                    print("You ask why ghosts hate rain.")
                    print("Ghost: 'It dampens our spirits!'")
                elif west3 == "ghost phone":
                    print("You ask if ghosts have phones.")
                    print("Ghost: 'Sure, we use ghostwriters for all our texts.'")
                elif west3 == "ghost band":
                    print("You ask if ghosts play music.")
                    print("Ghost: 'We love the boo-m bass!'")
                elif west3 == "ghost pet":
                    print("You ask if ghosts have pets.")
                    print("Ghost: 'Only scare-rows and boo-berries.'")
                elif west3 == "ghost workout":
                    print("You ask how ghosts exercise.")
                    print("Ghost: 'Spectral-tors, duh!'")
                elif west3 == "ghost holiday":
                    print("You ask where ghosts go on vacation.")
                    print("Ghost: 'Lake Eerie, always.'")
                elif festival_mode:
                    print("Ghost smiles: Happy full moon! Here's a gift!")
                    hp += 2
                elif west3 == "ghost fashion":
                    print("You ask why ghosts wear sheets.")
                    print("Ghost: 'It’s the latest haunting fashion.'")
                elif west3 == "ghost password":
                    print("You ask the cave’s secret password.")
                    print("Ghost: 'NO SINGING. That’s the only password.'")
                elif west3 == "tell scary story":
                    print("You tell a scary story. Ghost laughs: 'That can't scare me.'")
                elif west3 == "wave flashlight":
                    print("You wave light around. Ghost chases the light playfully.")
                elif west3 == "ask age":
                    print("You ask how old it is. Ghost: 'I lost count hundreds of years ago.'")
                elif west3 == "ask food":
                    print("You ask what it likes to eat. Ghost: 'Ghosts don't need food, just fun!'")
                elif west3 == "scare ghost":
                    print("You jump out to scare it. Ghost: 'Nice try, I'm already dead.'")
                elif west3 == "ask sleep":
                    print("You ask if it ever sleeps. Ghost: 'Sleep is for living people!'")
                elif west3 == "borrow clothes":
                    print("You joke to borrow its clothes. Ghost: 'I have no real clothes at all!'")
                elif west3 == "ask travel":
                    print("You ask if it wants to go outside. Ghost: 'Sunshine burns me! No way!'")
                elif west3 == "sing off key":
                    print("You sing terribly. The ghost covers its ears and spins around.")
                elif west3 == "play dead":
                    print("You lie down and play dead. The ghost pokes you again and again.")
                elif west3 == "lift hand":
                    print("You lift your hand up. The ghost floats higher as well.")
                elif west3 == "walk slow":
                    print("You walk slowly. The ghost drifts beside you quietly.")
                elif west3 == "lean close":
                    print("You lean close to the ghost. It moves back shyly.")
                elif west3 == "race on foot" or west3 == 'race':
                    print("You run to compete. The ghost just floats past you in a second.")
                elif west3 == "blow kiss to ghost":
                    print("You blow a kiss. The ghost pretends to catch it and blushes.")
                elif west3 == "play tag":
                    print("You play tag. The ghost can go through walls, you never catch it.")
                elif west3 == "complain cold" or west3 == 'complain':
                    print("You complain about the cold. Ghost laughs: 'I am colder forever.'")
                elif west3 == "pat ghost":
                    print("You pat the ghost's head. It floats higher shyly.")
                elif west3 == "wave finger":
                    print("You shake your finger. The ghost acts naughty.")
                elif west3 == "call" or west3 == 'call ghost':
                    print("You call the ghost. It drifts closer slowly.")
                elif west3 == "point around":
                    print("You point around. The ghost looks everywhere confused.")
                elif west3 == "hum song":
                    print("You hum a tune. The ghost sways along with the rhythm.")
                elif west3 == 'sing':
                    print('You sing a silly song, Ghost: SHUT UP PLEASE!')
                elif west3 == "selfie":
                    print("You take a selfie with the ghost.")
                    print("The ghost feels cool and waves hand.")
                elif west3 == "feed":
                    print("You try to feed the ghost.")
                    print("Ghost: 'I don't eat snacks!!!'")
                elif west3 == "tease ghost":
                    print("You tease the ghost. It pouts like a kid.")
                elif west3 == "fight ghost":
                    if festival_mode:
                        print("Ghost smiles: Happy full moon! Here's a gift!")
                        hp += 2
                    else:
                        if play_count == 1:
                            print("The ghost attacks!")
                            ghost_hp = 3
                            while ghost_hp > 0 and hp > 0:
                                print(f"Ghost HP: {ghost_hp} | Your HP: {hp}")
                                fight = input("attack / run: ").strip().lower()
                                if fight == "attack":
                                    ghost_hp -= 1
                                    print("You hit the ghost!")
                                    if ghost_hp > 0:
                                        hp -= 2
                                        print("Ghost hits you! hp -2")
                                elif fight == "run":
                                    print("You run away.")
                                    break
                            if ghost_hp <= 0:
                                print("The ghost fades. It leaves a ghost sword.")
                                have_list.append("ghost sword")
                            elif hp <= 0:
                                print("You die in battle. Game over!")
                                game_over = True
                                game_back = True
                        else:
                            print("The ghost bows. It won’t fight you.")    
                elif west3 == 'take pick-axe':
                    print('You shatter while you touch it.')
                    print('Luckily, you got it.')
                    print('Try find secret wall.')
                    print('Hp -3')
                    hp -= 3
                    if hp <= 0:
                        print("Your HP is gone!")
                        print('Game over!')
                        game_over = True
                        game_back = True
                        break
                    print('left hp: ' + str(hp))
                    have_list.append(p)
                    p = 'nothing'
                    if play_count == 2:
                        print("A CAVE GHOST APPEARS!")
                        print("The ghost looks straight at you. But do not harm you.")
                        print("'You came back... to end the cycle?'")
                    elif play_count == 1:
                        print('A ghost appears!')
                        if festival_mode:
                            print("Ghost smiles: Happy full moon! Here's a gift!")
                            hp += 2
                        else:
                            if amulet == True:
                                print('Amulet protects you!')
                            else:
                                combat("ghost fighter", 8, 3, "ghost sword", 8)
                                game_over = True
                                game_back = True
                                break
                elif west3 == 'east':
                    print('You go back to a room.')
                    current_room = 'go west2'
                    break
                elif west3 == 'touch corpse':
                    if 'an amulet' not in have_list:
                        print('You found an old amulet!')
                        amulet = True
                        have_list.append('an amulet')
                        player_total_score += 25
                elif west3 == 'room':
                    print("YOU ENTERED A DEADLY TRAP CHAMBER!")
                    trap = random.randint(1,4)
                    if trap != 1:
                        print("YOU AVOIDED ALL TRAPS!")
                        print("YOUR PICKAXE BECOMES UNBREAKABLE!")
                        player_total_score += 30
                    else:
                        print("TRAPS ACTIVATED! YOU DIED!")
                        game_over = True
                        game_back = True
                        break
                elif west3 == 'thank you':
                    if diary_read and not explorer_thank_reward:
                        print('A warm wind brings you diamonds.')
                        have_list.append('diamonds')
                        explorer_thank_reward = True
                    elif diary_read:
                        print('No more blessings come from the explorer spirit.')
                    else:
                        print('No one hears you.')
                elif west3 == 'colin woody':
                    print('DIAMOND VAULT! You found the ultimate treasure!')
                    print('You take diamond vault away.')
                    player_total_score += 5
                    have_list.append('diamond vault')
                elif west3 == 'bag':
                    for i in range(len(have_list)):
                        print(have_list[i])
                elif west3 == 'kill me':
                    print('You give up exploring. Game over!')
                    game_over = True
                    game_back = True
                    break
                elif west3 == 'search corpse':
                    print('You found a BELONGING of the dead explorer.')
                    print('It is a OLD IRON COMPASS.')
                    have_list.append('old compass')
                    legacy_unlocked = True
                elif west3 == 'bury corpse':
                    if diary_read == True:
                        print('You gently cover the corpse with stones.')
                        print('A warm feeling protects you.')
                        print('THE EXPLORER SOUL THANKS YOU.')
                        amulet = True
                    else:
                        print('You cannot bury what you do not respect.')
                else:
                    print('Sorry, I do not understand that word.')
                
                if game_over == True:
                    print("=== END ===")
                    print("Type 'menu' to return main menu")
                    while True:
                        c = input().strip().lower()
                        if c == 'menu':
                            main()
                            return
                        else:
                            print('Please answer the question.')
            if game_over == True:
                print("=== END ===")
                print("Type 'menu' to return main menu")
                while True:
                    c = input().strip().lower()
                    if c == 'menu':
                        main()
                        return

def combat(enemy_name, base_enemy_hp, base_enemy_dmg, loot_item = None, loot_evil = 0, enemy_id = None):
    global hp, good, evil, have_list, game_over, game_back
    global base_attack_bonus, base_defense_bonus, escape_bonus
    global player_weapon_damage, player_armor_reduction
    global difficulty_scalar, defeated_enemies,weapon_broken,weapon_durability,weather_duration,player_total_score

    enemy_hp = int(base_enemy_hp * difficulty_scalar)
    enemy_max_dmg = int(base_enemy_dmg * difficulty_scalar)
    enemy_min_dmg = max(1, enemy_max_dmg - 2)

    print(f"\n=== {enemy_name.upper()} ===")
    print(f"A {enemy_name} blocks your path.")
    print("Commands: 1.attack | 2.defend | 3.flee | 4.use potion | 5.bag | 6.hp")

    while True:
        if enemy_hp <= 0:
            print(f"\nThe {enemy_name} falls defeated.")
            if loot_item:
                print(f"You find: {loot_item}")
                have_list.append(loot_item)
            if loot_evil != 0:
                print(f"Evil {('+' if loot_evil > 0 else '')}{loot_evil}")
                evil += loot_evil
            if enemy_id is not None:
                defeated_enemies.add(enemy_id)
            player_total_score += 25
            adjust_sanity(-3)
            return True

        if hp <= 0:
            print(f"\nThe {enemy_name} strikes you down.")
            game_over = True
            game_back = True
            break

        cmd = input("combat> ").strip().lower()

        if cmd == "attack" or cmd == '1':
            player_dmg = random.randint(1, player_weapon_damage) + base_attack_bonus
            enemy_hp -= player_dmg
            print(f"You strike! Deal {player_dmg} damage.")
            if not weapon_broken and player_weapon_damage > 1:
                weapon_durability -= 1
                if weapon_durability <= 0:
                    weapon_broken = True
                    player_weapon_damage = 1
                    for w in ["iron sword", "cursed greatsword", "captain longsword",'ghost sword']:
                        if w in have_list:
                            have_list.remove(w)
                    print("Your weapon shatters! You fight with bare fists from now on.")
                    player_total_score -= 15
            if enemy_hp > 0:
                enemy_dmg = random.randint(enemy_min_dmg, enemy_max_dmg)
                final_dmg = max(0, enemy_dmg - base_defense_bonus - player_armor_reduction)
                hp -= final_dmg
                print(f"{enemy_name.title()} attacks! You take {final_dmg} damage.")

        elif cmd == "defend" or cmd == '2':
            enemy_dmg = random.randint(enemy_min_dmg, enemy_max_dmg)
            final_dmg = max(0, enemy_dmg // 2 - base_defense_bonus - player_armor_reduction)
            hp -= final_dmg
            print(f"You raise your guard. You take {final_dmg} damage.")
            print('You then hit again and deal 1 damage.')
            enemy_hp -= 1

        elif cmd == "flee" or cmd == '3':
            escape_chance = 3 + escape_bonus
            if enemy_hp <= 5:
                if random.randint(1, 10) <= escape_chance:
                    print("You successfully escape.")
                    player_total_score -= 30
                    return None
                else:
                    enemy_dmg = random.randint(enemy_min_dmg, enemy_max_dmg)
                    final_dmg = max(0, enemy_dmg - base_defense_bonus)
                    hp -= final_dmg
                    print(f"Escape failed! You take {final_dmg} damage while running.")
                    player_total_score -= 10
            else:
                print('The enemy is strong enough so you can not flee.')
                print('You then take 1 damage from the enemy.')
                hp -= 1
        elif cmd == "use potion" or cmd == '4':
            if "healing potion" in have_list:
                have_list.remove("healing potion")
                heal = random.randint(5, 10)
                hp += heal
                print(f"You drink a healing potion. Restore {heal} HP.")
            else:
                print("You have no healing potion.")

        elif cmd == "bag" or cmd == '5':
            for item in have_list:
                print(item)

        elif cmd == "hp" or cmd == '6':
            print(f"Your HP: {hp}")
            print(f"Enemy HP: {enemy_hp}")

        else:
            print("Unknown command.")

    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return

def blood_warrior_encounter():
    global bw
    if bw == False:
        combat("blood cursed warrior", 15, 4, "cursed greatsword", 10)
        bw = True
def blood_rift_dungeon():
    global hp, evil, have_list, game_over, game_back
    global blood_dungeon_cleared, blood_rune_hatred, blood_rune_agony, blood_rune_despair
    global blood_lord_seal_obtained
    global player_total_score

    if 'hound' not in defeated_enemies:
        combat("blood hound", 10, 4, "blood fang", 6, enemy_id = "hound")
    print("\n=== BLOOD RIFT DUNGEON ===")
    print("You climb down the crimson crack in the ground.")
    print("Warm blood-like liquid drips from the walls.")
    print("Three side chambers and a central altar stand before you.")
    print("Commands: left | middle | right | altar | back | bag | hp")

    correct_order = ["hatred", "agony", "despair"]
    input_order = []
    blood_dungeon_cleared = False

    while True:
        consume_step_durability()
        cmd = input("rift> ").strip().lower()

        if cmd == "back":
            print("You climb back up to the surface.")
            break

        elif cmd == "left":
            if not blood_rune_hatred:
                print("A rune glows on the wall: HATRED")
                blood_rune_hatred = True
            else:
                print("You already took the hatred rune.")

        elif cmd == "middle":
            if not blood_rune_agony:
                print("A rune glows on the wall: AGONY")
                blood_rune_agony = True
            else:
                print("You already took the agony rune.")

        elif cmd == "right":
            if not blood_rune_despair:
                print("A rune glows on the wall: DESPAIR")
                blood_rune_despair = True
            else:
                print("You already took the despair rune.")

        elif cmd == "altar":
            if not (blood_rune_hatred and blood_rune_agony and blood_rune_despair):
                print("The altar is silent. You need all three runes first.")
                continue
            print("The altar has three slots. Place runes in order.")
            print("Type 'place hatred', 'place despair', 'place agony'")
            while len(input_order) < 3:
                consume_step_durability()
                place_cmd = input("altar> ").strip().lower()
                if place_cmd.startswith("place "):
                    rune_name = place_cmd.split()[1]
                    if rune_name not in ["hatred", "agony", "despair"]:
                        print("Unknown rune.")
                        continue
                    input_order.append(rune_name)
                elif place_cmd == "reset":
                    input_order = []
                    print("You reset the altar.")
                else:
                    print("Unknown command.")

            if input_order == correct_order:
                print("\nAll runes glow deep red. The altar shakes violently!")
                print("A black seal rises from the blood pool.")
                if not blood_lord_seal_obtained:
                    have_list.append("blood lord seal")
                    blood_lord_seal_obtained = True
                    evil += 15
                    hp += 10
                    print("You obtained the BLOOD LORD SEAL.")
                    print("Max HP +10, Evil +15")
                    player_total_score += 20
                blood_dungeon_cleared = True
                break
            else:
                hp -= 3
                print("\nWrong order! Blood energy explodes in your face!")
                print("HP -3. The altar resets.")
                player_total_score -= 10
                input_order = []
                if hp <= 0:
                    print("You burn to ash in the blood fire.")
                    game_over = True
                    game_back = True
                    break

        elif cmd == "bag":
            for item in have_list:
                print(item)

        elif cmd == "hp":
            print(f"HP: {hp}")

        else:
            print("Unknown command.")

    if game_over:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == "menu":
                main()
                return

def advance_time():
    global step_count, time_period, festival_steps, festival_mode
    global weather_duration, weather_damage, amulet, game_over, game_back,good,evil,hp,current_weather,blood_dungeon_cleared,blood_lord_seal_obtained,blood_moon,blood_rune_agony,blood_warrior_alive,blood_warrior_hp,sanity

    consume_step_durability()
    step_count += 1
    if step_count % 4 == 0:
        festival_steps += 1
        if time_period == "dusk" and festival_steps >= 3 and random.randint(1,3) == 1 and not blood_moon:
            festival_mode = True
            festival_steps = 0
            print("\n=====================================")
            print("FULL MOON FESTIVAL BEGINS!")
            print(" All ghosts are friendly tonight!")
            print("=====================================\n")
            hp += 5
            good += 5
        if time_period == 'dusk' and random.randint(1, 4) == 1 and festival_steps >= 1 and not festival_mode:
            blood_moon = True
            blood_warrior_alive = True
            festival_steps = 0
            mac_horror_whisper("The blood moon rises.", "chant")
            print("\n=====================================")
            print("A BLOODY MOON RISES")
            print("The sky turns crimson. Evil surges in the air.")
            print("=====================================\n")
            hp -= 1
            evil += 5
            print('Suddenly, you are hit by something.')
            blood_warrior_encounter()
        if time_period == "day":
            time_period = "dusk"
            print("\n=== DUSK | The world fades to dark ===")
        elif time_period == "dusk":
            time_period = "night"
            print("\n=== NIGHT FALLS | Without light, you will DIE!!! ===")
        elif time_period == "night" and festival_mode:
            time_period = "day"
            print("\n=== SUNRISE | Safe again ===")
            festival_mode = False
            festival_steps = 0
            print("\n=====================================")
            print("  FULL MOON FESTIVAL ENDS  ")
            print("Ghosts return to their normal state.")
            print("=====================================\n")
        elif blood_moon and time_period == 'night':
            blood_moon = False
            blood_warrior_alive = False
            time_period = "day"
            print("\n=== SUNRISE | Safe again ===")
            print("\n=====================================")
            print("  BLOODY MOON FADES  ")
            print("The moon returns to normal. Evil calms down.")
            print("=====================================\n")
        elif time_period == 'night':
            time_period = "day"
            print("\n=== SUNRISE | Safe again ===")
    if (festival_mode or blood_moon) and not defeated_werewolf:
        if random.randint(1, 3) == 1:
            werewolf_encounter()
    if time_period == "night" and not torch and not light:
        hp -= 1
        print("Darkness burns you! Hp -1")
        if "cursed dagger" in have_list:
            print('The cursed dagger hits you in the dark. Hp -1')
            hp -= 1
        if hp <= 0:
            print("You were consumed by the dark...")
            game_over = True
            game_back = True
            print("=== END ===")
            print("Type 'menu' to return main menu")
            while True:
                c = input().strip().lower()
                if c == 'menu':
                    main()
                    return
    elif time_period == 'night' and torch or time_period == 'night' and light:
        print('Your light protects you from the darkness.')
    # Weather
    weather_duration -= 1
    if weather_duration <= 0:
        update_weather()
        print("\nThe weather changes.")
        print_weather()
    if weather_damage > 0:
        if amulet == False:
            hp -= weather_damage
            print(f"You take {weather_damage} damage from the weather.")
            if hp <= 0:
                print("You died from the harsh weather.")
                game_over = True
                game_back = True
                if game_over == True:
                    print("=== END ===")
                    print("Type 'menu' to return main menu")
                    while True:
                        c = input().strip().lower()
                        if c == 'menu':
                            main()
                            return
        else:
            print('Your amulet protects you from the harsh weather.')
    if current_weather == 'light_rain' and random.randint(1,2) == 1:
        print('You are in the rain, so romantic, luckily, you feel better. Hp +1')
        hp += 1
    if game_over == True:
        print("=== END ===")
        print("Type 'menu' to return main menu")
        while True:
            c = input().strip().lower()
            if c == 'menu':
                main()
                return

#game
def gamestart():
    global have_list, game_over, light, hp, map_unlocked, secret_unlocked, amulet, take, chain1, chain2, current_room, torch,l,k,n,s,f,w,sc,rune1,rune2,rune3,rune,grandmother,diary_read,old_diary_readed,grave_diary_read, game_back,play_count,trap_protect,cleared_ending,force_in_cave,hill_diary_read
    global step_count
    global time_period
    global festival_mode, festival_steps
    global good, evil
    global weather_duration,weather_damage
    global merchant_story_stage,swamp_spirit_story,hut_ghost_story,tower_ghost_story
    global has_death_corpse, death_location, death_corpse_item
    global one_hole_in,two_hole_in,three_hole_in,grave_take
    global grave_looted, church_purified, church_desecrated
    global x2,blood_moon,defeated_enemies,torch_durability
    global meta_file_tier
    global player_total_score,guardian_phases
    
    game_over = False
    altar = False
    if play_count == 2:
        print("=== NEW GAME+ ===")
        print("The curse and this game remembers you.\n")
    cleared_ending = False
    print('You are at the end of the road, there is a black house nearby.')
    print('You see a road lead to south. A pass to north, a forest in east and a hut in west.')
    print('Type ‘help’ for help, ‘in’ to go in the house, ‘journal’ for tasks, ‘moral’ for see if you are evil or good and ‘weather’ for weather.')
    print('Also, ‘statue’ to see statues.')
    print('And save to save, load to load if you have saved.\n')
    if has_death_corpse and death_location == current_room:
        print('You see here a corpse, type corpse to search it.\n')
    if map_unlocked == True:
            print('Type map to see full map.')
    while True:
        current_room = 'road'
        if play_count >= 2 and death_count >= 1 and random.randint(1, 10) == 1:
            auto_cmd = random.choice(["go deeper", "do not leave", "stay here", "kill yourself"])
            print(auto_cmd)
            time.sleep(0.8)
            print("You didn't type that.")
            time.sleep(1)
            print("Your body moves anyway.")
            hp -= 2
            if auto_cmd == 'go deeper':
                if current_room != 'cave':
                    print('You go into the cave!!!')
                current_room = "cave"
                print("You find yourself deeper in the cave than you remember.")
                print('You go back to the road.')
                print('You can control you again.')
                current_room = 'road'
                evil += 10
            elif auto_cmd == 'do not leave':
                print('You stay here forever.')
                time.sleep(1)
                print('Well, you then wake up. Hp -1')
                print('You can control you again.')
                hp -= 1
            elif auto_cmd == 'stay here':
                print('You stay here for a while, you can control you again.')
            elif auto_cmd == 'kill yourself':
                for i in range(30):
                    print('-------------------------------------------------------------------------------------------------------\n')
                    time.sleep(0.03)
                    print('You kill yourself!!!')
                    game_back = True
                    game_over = True
                    break
        if death_count >= 3 and random.randint(1, 10) == 1:
            player_name = get_last_player_name() or os.getlogin()
            print("\nYou hear your name whispered right in your ear.")
            print(f"'{player_name}... turn around...'")
            print("There is nobody behind you.")
            hp -= 1
        advance_time()
        # NIGHT DAMAGE (STRONGER)
        if festival_mode:
            print('Full moon! A hole appears on the ground, type down to go down.')
        consume_step_durability()
        desktop_path = os.path.expanduser("~/Desktop")
        try:
            real_files = os.listdir(desktop_path)
            real_item = random.choice(real_files) if real_files else "unknown_file.txt"
        except:
            real_item = "a file from your desktop"
        go = input().strip().lower()
        if handle_terminal_cmd(go):
            continue
        if go == 'in':
            current_room = 'house'
            if play_count == 2:
                mac_horror_whisper("You return again.", "demon")
                jump_scare_face('flash')
                print('')
                print('You see something is written on the wall.')
                print("The text has changed.")
                print("'You return again. The cave needs its own blood.'")
                print("'All explorers were you. The demon is your ancestor.'")
                print('All the diamonds are not the real treasure, you are!')
                print('')
            elif play_count == 1:
                mac_horror_whisper("What are you going to do here?", "demon")
                jump_scare_face('flash')
                print('')
                print('You see something is written on the wall.')
                print('It says that a long time ago, the cave is full of water, but after sometimes, it do not have water anymore.')
                print('Some ghost had hidden some treasure inside the cave, then a lot of people go in.')
                print('Unfortunately, no one comes out alive, but they have left some diary and note to tell where the treasure is.')
                print('A few years ago, a man who is poor went into the cave, and they just hear some screaming.')
                print('And then, the man never come out alive.')
                print('His campsite is near this house, in the south. There may still have some useful things.')
                print('But, for safety, this country have let soldiers to protect the cave, and do not let anyone come in again.')
                print('Because it is HAUNTED!!!')
                print('')
            while True:
                print('You are in the house, there is ' + l + k + n + s + sc +f + w + 'and a note your father left')
                print('You notice that the wall is strange. Type wall to search the wall.')
                print('You see here a shaft, it is not too deep, type ’down‘ to go down.')
                if has_death_corpse and death_location == current_room:
                    print('You see here a corpse, type corpse to search it.\n')
                consume_step_durability()
                take = input().strip().lower()
                if handle_terminal_cmd(take):
                    continue
                elif take == 'take lamp':
                    if 'a lamp' not in have_list:
                        print('Ok')
                        have_list.append('a lamp')
                        torch_durability = TORCH_MAX
                        l = ''
                    else:
                        print('You have already taken it.')
                elif take == 'down' or take == 'go down' or take == 'climb down':
                    if one_hole_in == False:
                        forgotten_archive()
                    else:
                        print('You do not want to go in again.')
                elif take == 'take key':
                    if 'a key' not in have_list:
                        print('Ok')
                        have_list.append('a key')
                        k = ''
                    else:
                        print('You have already take it!')
                elif take == 'pc' or take == 'take pc':
                    print("You find an old dusty computer under the table.")
                    print("It's running Windows 11... and a copy of this exact game.")
                    print("The screen shows on the computer: 'You died.'")
                    print("You feel weirdly self-aware.")
                elif take == "who made this" or take == 'Who made this' or take == 'who made this?' or take == 'Who made this?':
                    print("A voice whispers from nowhere: 'A very tired developer.'")
                    print("'He wrote all of this in a hurry. Sorry for the bugs.'")
                elif take == "is this a game" or take == 'Is this a game' or take == 'is this a game?' or take == 'Is this a game?':
                    print("The screen glitches for a second.")
                    print("You feel like someone is watching you type commands.")
                    print("...Then everything goes back to normal.")
                elif take == "spin":
                    print("You spin around and feel dizzy.")
                elif take == "jump":
                    print("You jump around the house. Boring!")
                elif take == "flip table":
                    print("You flip the table. It's very childish.")
                elif take == 'take food':
                    if 'some food' not in have_list:
                        print('Ok')
                        have_list.append('some food')
                        f = ''
                    else:
                        print('You have already take this!')
                elif take == 'take water':
                    if 'a bottle' not in have_list:
                        print('Ok')
                        have_list.append('a bottle')
                        have_list.append('some water in the bottle')
                        w = ''
                    else:
                        print('You have already take this!')
                elif take == 'take scroll':
                    if 'a scroll' not in have_list:
                        print('Ok')
                        have_list.append('a scroll')
                        sc = ''
                    else:
                        print('You have already take this!')
                elif take == 'wall':
                    if rune1 == False:
                        print('You found a RUNE on the wall!')
                        print('Rune text: The cave holds an ancient demon.')
                        rune1 = True
                        have_list.append('rune stone 1')
                    else:
                        print('You find a hole which is big enough for a rune, but you may have already take the rune away.')
                elif take == "examine corpse" or take == 'corpse' or take == 'search corpse' or take == 'find corpse':
                    if has_death_corpse and death_location == current_room:
                        print("\nA corpse slumps against the dusty floor. It wears your exact clothes.")
                        if death_corpse_item:
                            print(f"You retrieve {death_corpse_item} from its pocket.")
                            have_list.append(death_corpse_item)
                        else:
                            print("Nothing useful left on the body.")
                        has_death_corpse = False
                    else:
                        print("There is not any corpse..")
                elif take == 'light lamp':
                    if 'a lamp' in have_list:
                        print('The light is lit. The room bright up!')
                        light = True
                    else:
                        print('You do not have a lamp!')
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
                        print('=== COMMANDS ===')
                        print('take, out, altar, eat, drink, bag, map, compass')
                        print('light lamp, colin, woody, make torch')
                        print('unlock, west, east, dig, sewer, forward, treasure')
                        print('room, touch corpse, search corpse, thank you, look wall')
                        print('search ground, place runes, hp, status,church, purify, desecrate, read stone')
                        print('In the cave, it is very dark. You should bring light your lamp unless you want to be eaten by a Grue.')
                        print('===============')
                    else:
                        print('No scroll found.')
                elif take == 'make torch':
                    if 'flint' in have_list and 'a lamp' in have_list:
                        print("You crafted a torch.")
                        have_list.remove('flint')
                        have_list.remove('a lamp')
                        have_list.append('a torch')
                        torch = True
                        light = True
                    else:
                        print("You need flint and a lamp.")
                elif take == 'take note':
                    print('When you take the note, some magic energy hurts you, you can not take away it. You read it, it says magic word: colin, but you should read it on an altar.')
                elif take == 'out':
                    print('You are at the end of road again.')
                    break
                elif take == 'altar' or take == 'up' or take == 'go to altar':
                    print('You climb up the high altar, you can not descent down again!')
                    altar = True
                    break
                elif take == "eat":
                    if "some food" in have_list:
                        have_list.remove("some food")
                        hp += 3
                        adjust_sanity(30)
                        print("You eat food. HP +3")
                    else:
                        print("You have no food.")

                elif take == "drink":
                    if "some water in the bottle" in have_list:
                        have_list.remove("some water in the bottle")
                        hp += 2
                        print("You drink water. HP +2")
                        adjust_sanity(20)
                    else:
                        print("You have no water.")
                elif take == 'bag':
                    for i in range(len(have_list)):
                        print(have_list[i])
                elif take == "stare":
                    print("You stare at the wall for a long time. Nothing happens.")
                elif take == "clap":
                    print("You clap your hands. Echoes fill the room.")
                elif take == 'colin':
                    print('You say colin, you feel strange.')
                    chain1 = True
                elif take == 'woody' and chain1:
                    chain2 = True
                    print('You say woody, you get some money!')
                    have_list.append('some gold coins')                
                elif take == 'garry' and chain2:
                    if play_count == 1:
                        print('Wow, you know the magic words!')
                        print('You are so cool!')
                        print('I will give you light in exchange.')
                        print('The room bright up.')
                        light = True
                    else:
                        print('I do not want to give you light even if you know the magic words. Because you have to done all by yourself.')
                elif take == 'map':
                    print('MAP: House -> Altar -> Cave -> West -> Diamonds')
                    map_unlocked = True
                elif take == 'compass':
                    if 'old compass' in have_list:
                        if current_room == "house":
                            print("Compass: You are in the HOUSE. Go 'out' to road, 'south' to camp. Go on the altar, light your lamp and cast 'colin' to go into the death cave.")
                        elif current_room == "road":
                            print("Compass: You are on the ROAD. 'in' for house, 'south' for camp.")
                        else:
                            print("Compass spins wildly.")
                    else:
                        print("You do not have a compass.")
                elif take == 'read father note' or take == 'take father note' or take == 'father note':
                    print('You found a hidden note from your father, beneath the floor.')
                    print('')
                    print('Son,')
                    print('If you are reading this, I am already dead.')
                    print('I never went on holiday. I came to the cave to finish our family’s duty.')
                    print('Our bloodline carries the wizard’s power and the demon’s soul.')
                    print('I tried to break the curse. I failed.')
                    print('The cave does not want treasure. It wants the heir.')
                    print('You are the only one who can finally end it.')
                    print('I am sorry I left you.')
                    print('Father.')
                    print('')
                else:
                    print('Sorry, I do not understand that word.')
            if altar == True:
                if play_count == 2:
                    print('You hear a demon talk to you!')
                    print("This time, you understand every word clearly.")
                    print("'Descendant... you have returned.'")
                    print("'Seal me, free me, or join me.'")
                elif play_count == 1:
                    print('You hear a demon talk to you! But you do not know what she says.')
                print('You see here ' + rune)
                while True:
                    can_enter_altar()
                    if rune1 and rune2 and rune3 and x2 == True:
                        print('You can place the runes now, type place runes to place them.')
                    consume_step_durability()
                    tele = input().strip().lower()
                    if tele == 'light lamp':
                        if 'a lamp' in have_list:
                            print('The light is lit. The room bright up!')
                            light =True
                        else:
                            print('You do not have a lamp!')
                    elif tele == 'take rune':
                        if play_count == 2:
                            if rune != 'nothing':
                                print('Ok')
                                print('Rune says: But, if you control the demon, you must be here for all of your life.')
                                rune = 'nothing' 
                                rune3 = True
                                player_total_score += 10
                            else:
                                print('You have already taken the rune.')
                        else:
                            print('You can not get this rune, because some mysterious power force pretents you from taking.')
                            print('Only enable in ng2, and try to go in the death cave!\n')
                    elif tele == 'colin':
                        mac_horror_whisper("Welcome to your tomb.", "demon")
                        print('You suddenly fall asleep, when you wake up, you are at a cave.')
                        current_room = 'entrance'
                        if play_count == 1:
                            if light == False and not torch:
                                print('A Grue appears, it would not die forever, you can just make it turns to flee.')
                                combat("Grue", 20, 5, None, 7)
                                force_in_cave = True
                            elif torch == True:
                                print("Your torch keeps Grue away.")
                                print('Welcome to death cave!')
                                print('You are in a cave, there is a grate. The grate is locked. You must open the grate to go further.')
                                current_room = "cave"
                                cave()
                                if game_over == True:
                                    print("=== END ===")
                                    print("Type 'menu' to return main menu")
                                    while True:
                                        c = input().strip().lower()
                                        if c == 'menu':
                                            main()
                                            return
                            elif light == True or force_in_cave:
                                print('Welcome to death cave!')
                                print('You are in a cave, there is a grate. The grate is locked. You must open the grate to go further.')
                                current_room = "cave"
                                cave()
                                if game_over == True:
                                    print("=== END ===")
                                    print("Type 'menu' to return main menu")
                                    while True:
                                        c = input().strip().lower()
                                        if c == 'menu':
                                            main()
                                            return  
                        else:
                            print('You can not go in again, try to collect three runes to pass ng2.')
                    elif tele == 'down':
                        if 'rope' in have_list:
                            print('You go down safetly with your rope.')
                            altar = False
                            break
                        else:
                            if hp > 20:
                                print('You jump down the high altar and break some of your bones!')
                                print('Hp -20')
                                hp -= 20
                            else:
                                print('You jump down the high altar and break all of your bones!')
                                print('Game over!')
                                game_over = True
                                game_back = True
                                break
                    elif tele == 'place runes':
                        can_enter_altar()
                        if x2 == True:
                            if rune1 and rune2 and rune3:
                                mac_demon_whisper("The guardian wakes.")
                                guardian_phases = [
                                    {
                                        "hp_threshold": 50,
                                        "dialogue": "Stone armor rises from the altar. The ancient seal guardian awakens to test the heir.",
                                        "attacks": [
                                            {"name": "Stone Fist", "description": "Heavy rocky fist slams down with crushing force."},
                                            {"name": "Rune Shockwave", "description": "Glowing runes send a wave of sealing energy outward."},
                                            {"name": "Crushing Slam", "description": "It lifts its fist and strikes the ground with full force."}
                                        ],
                                        "enrage": False,
                                        "score_reward": 10
                                    },
                                    {
                                        "hp_threshold": 35,
                                        "dialogue": "Cracks spread across its stone body. Dark power seeps out, strengthening its strikes!",
                                        "attacks": [
                                            {"name": "Shadow Crush", "description": "Darkness wraps around its fist and slams into you."},
                                            {"name": "Soul Drain", "description": "Ancient runes drain your life force.", "lifesteal": True},
                                            {"name": "Seal Burst", "description": "Concentrated sealing power explodes at your feet.", "curse": True}
                                        ],
                                        "enrage": False,
                                        "score_reward": 30
                                    },
                                    {
                                        "hp_threshold": 15,
                                        "dialogue": "\"You are not worthy... of breaking the seal.\" The guardian enters berserk final form!",
                                        "attacks": [
                                            {"name": "Annihilation Strike", "description": "Full power blow, aimed to shatter you in one hit."},
                                            {"name": "Eternal Seal", "description": "All runes ignite at once, corrupting your spirit.", "curse": True, "lifesteal": True},
                                            {"name": "Final Judgment", "description": "The guardian channels all remaining power for a killing blow."}
                                        ],
                                        "enrage": True,
                                        "score_reward": 60
                                    }
                                ]
                                boss_fight("Ancient Seal Guardian", 50, 7, guardian_phases, "guardian core", "seal_guardian")
                                print('Wow, amazing, you defeat the last boss of this game!')
                                good = good - evil
                                write_creepy_desktop_file(5)
                                print('The ancient seal trembles!')
                                if play_count == 1:
                                    print('Choose: seal (good > 10) / release / absorb / sacrifice / symbiosis (good > 5) / leave ')
                                elif play_count == 2:
                                    print('Choose: seal (good > 10) / release / absorb / sacrifice / symbiosis / unleash (good > 20) / leave / break curse (good > 25) / truth')
                                while True:
                                    c = input().strip().lower()
                                    if c == 'seal':
                                        if good >= 10:
                                            print('You sealed the cave Evil FOREVER.')
                                            print('And then, you stay here until you dead.')
                                            if grave_diary_read == True:
                                                print('You realised that all explorers were guardians, not treasure hunters.')
                                                print('They gave up wealth to protect the world.')
                                                print('====== TRUE GUARDIAN ENDING ======')
                                                player_total_score += 50
                                                game_over = True
                                                game_back = True
                                                cleared_ending = True
                                                break
                                            else:
                                                print('You seal the Evil again.')
                                                print('===== HERO ENDING =====')
                                                player_total_score += 50
                                            game_over = True
                                            game_back = True
                                            cleared_ending = True
                                            break
                                        else:
                                            print('You are not good enough.')
                                    elif c == 'unleash':
                                        if play_count == 2:
                                            if good >= 20:
                                                print('You unleash your great-great grandmother, the wizard -- your great-great grandfather appears.')
                                                print('They are all free!')
                                                print('====== FREE ENDING ======')
                                                player_total_score += 50
                                                game_over = True
                                                game_back = True
                                                cleared_ending = True
                                                break
                                            else:
                                                print('You are not good enough.')
                                        elif play_count == 1:
                                            print('You do not know how to unleash, because the curse.')
                                    elif c == 'leave':
                                        if play_count == 2:
                                            print('You leave the cave safetly, and you never come back again.')
                                            print('====== ESCAPE ENDING ======')
                                            player_total_score += 50
                                            game_over = True
                                            cleared_ending = True
                                            break
                                        elif play_count == 1:
                                            print('You want to leave, but the Evil kills you.')
                                            print('====== DIED ENDING ======')
                                            player_total_score += 50
                                            game_over = True
                                            game_back = True
                                            cleared_ending = True
                                            break
                                    elif c == 'release':
                                        print('Evil awakened! It destroys everything!')
                                        print('====== BAD ENDING ======')
                                        player_total_score += 50
                                        game_over = True
                                        game_back = True
                                        cleared_ending = True
                                        break
                                    elif c == 'talk':
                                        if grave_diary_read == True and old_diary_readed == True and good >= 20:
                                            print('You say: Hello, great-great grandmother!')
                                            print('The Evil is shocked, then she smiles and hug you!')
                                            print('===== THE BEST ENDING! =====')
                                            player_total_score += 60
                                            game_over = True
                                            game_back = True
                                            cleared_ending = True
                                            break
                                        else:
                                            print('The Evil do not want to talk to you.')
                                    elif c == 'absorb':
                                        print('You absorb the Evil power!')
                                        print('You become the immortal ruler of the cave!')
                                        print('===== DEMON LORD ENDING =====')
                                        player_total_score += 50
                                        amulet = True
                                        hp = 99
                                        game_over = True
                                        game_back = True
                                        cleared_ending = True
                                        break
                                    elif c == 'sacrifice':
                                        print('You sacrifice your life force to calm the Evil.')
                                        print('You turn to stone, guarding the cave forever.')
                                        print('===== SACRIFICE ENDING =====')
                                        player_total_score += 50
                                        game_over = True
                                        game_back = True
                                        cleared_ending = True
                                        break
                                    elif c == 'symbiosis':
                                        if good >= 5:
                                            print('You make a pact with the Evil.')
                                            print('You gain power but can never leave the cave.')
                                            print('===== SYMBIOSIS ENDING =====')
                                            player_total_score += 50
                                            game_over = True
                                            game_back = True
                                            cleared_ending = True
                                            break
                                        else:
                                            print('You are not good enough.')
                                    elif c == 'truth':
                                        if play_count == 2:
                                            if 'a magic key' in have_list:
                                                print("You place all runes and speak the ancient words.")
                                                print("The curse is broken. The cave is finally free.")
                                                print("You have escaped the cycle of death.")
                                                print("===== TRUTH ENDING =====")
                                                player_total_score += 100
                                                game_over = True
                                                game_back = True
                                                cleared_ending = True
                                                break
                                            else:
                                                print('You do not have a magic key, so you can not end the curse.')
                                                print('====== NORMAL ENDING ======')
                                                game_over = True
                                                game_back = True
                                                cleared_ending = True
                                                player_total_score += 50
                                                break
                                        elif play_count == 1:
                                            print('You do not know the truth.')
                                        game_over = True
                                        game_back = True
                                        cleared_ending = True
                                        break
                                    elif c == 'break curse':
                                        if 'a magic key' in have_list and play_count == 2:
                                            if good >= 25:
                                                print('You use the magic key to break the curse.')
                                                print('Your great-great grandfather and his wife, and your great grandfather and his wife, and your grandfather and his wife, and you father and you mum, all appears.')
                                                print('You celebrate together.')
                                                print('====== THAT IS THE REAL ENDING ======')
                                                player_total_score += 100
                                                game_over = True
                                                game_back = True
                                                cleared_ending = True
                                                break
                                            else:
                                                print('You are not good enough')
                                        else:
                                            print('You do not have a magic key.(Or you can not do it now.)')
                                    else:
                                        print('Invalid choice!')
                                if force_over == True:
                                    break
                            if game_over:
                                print("=== END ===")
                                print("Type 'menu' to return main menu")
                                while True:
                                    c = input().strip().lower()
                                    if c == 'menu':
                                        main()
                                        return
                            else:
                                print('Not enough runes!')
                            if force_over == True:
                                break
                        else:
                            if play_count == 2:
                                print('\nYou should done the soldier and lieutenant task and then read the grave diary and the old diary in the forest.')
                                print('Also, you should have at least 6 items in your bag. Also, of course, three runes.\n')
                            else:
                                print('Only avalible in ng2, try to go to the death cave!')
                    elif tele == 'woody':
                        if light == True:
                            print('A secret power surrounds you!')
                            secret_unlocked = True
                        else:
                            print('Nothing happens.')
                    elif tele == 'bag':
                        for i in range(len(have_list)):
                            print(have_list[i])
                    else:
                        print('Sorry, I do not understand that word.')
                    if force_over == True:
                        break
                if force_over == True:
                    break
            if force_over == True:
                break
        elif go == "help":
            print("\n=== HELP ===")
            print("north / south / east / west - Move between areas")
            print("in - Enter the house")
            print("bag - Check your inventory")
            print("hp - Check current HP")
            print("save / load - Save or load progress")
            print("tomb - Enter tomb (New Game+ only)")
            print("read diary / take diary - Check story notes")
            print("sing / dance / joke - Fun interactive commands")
            print("leave / back - Return to previous area")
            print('dev - To cheat')
            print("============\n")
        elif go == 'down' or go == 'go down':
            if festival_mode:
                if three_hole_in == False:
                    full_moon_maze()
                else:
                    print('You do not want to go in again.')
            else:
                print('I do not see any hole.')
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
                print('Do not cheat! You are alredy have many things! For example, three runes in your memory.')
        elif go == "bag" and death_count >= 2 and random.randint(1, 2) == 1:
            for item in have_list:
                print(item)
            print(real_item)
            time.sleep(1.5)
            jump_scare_face('flash')
            print("\n...Wait, that wasn't in your bag.")
        elif go == "examine corpse" or go == 'corpse' or go == 'search corpse' or go == 'find corpse':
            if has_death_corpse and death_location == current_room:
                print("\nA corpse slumps against the dusty floor. It wears your exact clothes.")
                if death_corpse_item:
                    print(f"You retrieve {death_corpse_item} from its pocket.")
                    have_list.append(death_corpse_item)
                else:
                    print("Nothing useful left on the body.")
                has_death_corpse = False
            else:
                print("There is not any corpse..")
        elif go == 'hp':
            print('HP:', hp)
        elif go == 'bag':
            for i in range(len(have_list)):
                print(have_list[i])
        elif go == 'map':
            print("""WORLD MAP (Only ground)
        ====================
        [Watchtower]   [Road * (You are here)]
                |
        [Merchant]      [House] --> [altar] --> [???]
                |
        [Forest]  <-->  [Haunted Hut]
                |
        [Abandoned Camp]
                |
        [Grave]   [???]
                |
        [Misty Swamp]
                |
        ====================""")
        elif go == "moral":
            print(f"Good: {good} | Evil: {evil}")
            if good > evil:
                print("You are kind. NPCs treat you friendly.")
            elif evil > good:
                print("You are ruthless. NPCs stay alert.")
            else:
                print('You are not good or evil.')
        elif go == "weather":
            print_weather()
        elif go == "eat":
            if "some food" in have_list:
                have_list.remove("some food")
                hp += 3
                print("You eat food. HP +3")
            else:
                print("No food.")

        elif go == "drink":
            if "some water in the bottle" in have_list:
                have_list.remove("some water in the bottle")
                hp += 2
                print("You drink water. HP +2")
                player_total_score += 10
            else:
                print("No water.")
        elif go == 'north':
            tower_check = input("Go to merchant or watchtower or military_fort? (1.merchant / 2.tower / 3.fort): ").strip().lower()
            if tower_check == "fort" or tower_check == '3':
                military_fort()
                continue
            elif tower_check == "tower" or tower_check == '2':
                watchtower()
                continue
            elif tower_check == 'merchant' or tower_check == '1':
                good = good - evil
                evil = 0
                if good >= 5:
                    print('You found a TRAVELING MERCHANT!')
                    print('Type trade food/water to trade.')
                    print('Type ask ask past or talk more to ask.')
                    if args.godmode:
                        print('Merchant: Welcome, god, what are you going to do here?')
                    while True:
                        advance_time()
                        consume_step_durability()
                        m = input('merchant> ').strip().lower()
                        if m == 'trade food':
                            if 'some food' in have_list:
                                have_list.remove('some food')
                                have_list.append('super amulet')
                                amulet = True
                                print('Trade success! Got SUPER AMULET!')
                        elif m == 'trade water':
                            if 'a bottle' in have_list:
                                have_list.remove('a bottle')
                                torch = True
                                light = True
                                print('Trade success! Got ETERNAL TORCH!')
                        elif m == "stare":
                            print("You stare at the merchant. He feels awkward.")
                        elif m == 'attack merchant' or m == 'kill merchant' or m == 'attack him' or m == 'kill him' or m == 'fight him' or m == 'fight merchant':
                            print('Merchant: Really? Attack a definess poor merchant? You are so evil!')
                            adjust_sanity(-5)
                            evil += 5
                        elif m == "wave hand":
                            print("You wave. The merchant waves back lazily.")
                        elif m == "nod":
                            print("You nod again and again. The merchant nods along too.")
                        elif m == "copy move":
                            print("You copy every move the merchant makes. He gets confused and freezes.")
                        elif m == "pretend to cry":
                            print("You pretend to cry. The merchant panics and does not know what to do.")
                        elif m == "dance together":
                            print("You dance together. Both of you look extremely clumsy.")
                        elif m == "doze":
                            print("You pretend to doze. The merchant stays quiet.")
                        elif m == "walk around":
                            print("You walk circles around him. He just stands still.")
                        elif m == "complain":
                            print("You complain about the cave. Merchant agrees with you.")
                        elif m == "merchant lazy":
                            print("You say: You look so lazy.")
                            print("Merchant: 'Business is slow when everyone gets haunted.'")
                        elif m == "merchant ghost":
                            print("You ask: Are you scared of ghosts?")
                            print("Merchant: 'Nah, they owe me money.'")
                        elif m == "merchant tired":
                            print("You say: You look tired.")
                            print("Merchant: 'I work next to a death cave. Of course I’m tired!'")
                        elif m == "arm wrestle":
                            print("You challenge arm wrestling. You lose in one second.")
                        elif m == 'leave' or m == 'back' or m == 'south':
                            print('You return to road.')
                            break
                        elif m == "ask past":
                            print("Merchant: I was once just like you, chasing gold in this cave.")
                            print("I learned all the secrets, but chose to walk away from the cycle.")
                            print("I trade goods here, watching every new heir step onto this road.")
                        elif m == "talk more" or m == 'talk':
                            if merchant_story_stage == 0:
                                print("Merchant: I used to be an adventurer too, same as you.")
                                print("Merchant: I came here with my best friend, chasing the diamond legend.\n")
                                print('You can still type ask more if you want to know more.\n')
                                good += 5
                                adjust_sanity(5)
                                merchant_story_stage = 1
                            elif merchant_story_stage == 1:
                                print("Merchant: He was the last guardian of this cave. Your grandfather's generation.")
                                print("Merchant: He chose to stay inside, and I chose to wait outside.\n")
                                merchant_story_stage = 2
                                adjust_sanity(5)
                                good += 5
                            elif merchant_story_stage == 2:
                                print("Merchant: I've seen hundreds of people walk in. Most never come out.")
                                print("Merchant: You're the first one with his eyes. The bloodline shows.\n")
                                good += 5
                                merchant_story_stage = 3
                                adjust_sanity(5)
                            elif merchant_story_stage == 3:
                                print("Merchant: End the cycle. Don't repeat his mistake.")
                                print("Merchant: Take this. He left it for the heir.\n")
                                if "rune1" not in have_list:
                                    have_list.append("stone rune1")
                                    rune1 = True
                                    print("You got a rune!")
                                adjust_sanity(5)
                                player_total_score += 20
                                if evil >= 0:
                                    evil = 0
                                else:
                                    good += 10
                                merchant_story_stage = 4
                            else:
                                print("Merchant nods quietly, watching the cave entrance.\n")
                        elif m == "ask fate":
                            print("Merchant: Your blood ties you to this place. No one escapes easily.")
                            print("But choices are always yours. That is the only freedom we have.")
                        elif m == "trade secret":
                            if play_count == 2 and grave_diary_read:
                                if "gold coins" in have_list:
                                    have_list.remove("gold coins")
                                    have_list.append("ancient scroll")
                                    print("You traded gold for ANCIENT SCROLL.")
                                    print("Scroll words: The key breaks chain, heart heals hate.")
                                else:
                                    print("You have no gold coins to trade.")
                            else:
                                print("He shakes his head, unwilling to talk more.")
                        elif m == "trade coin" or m == 'trade coins' or m == 'trade gold coins':
                            if "gold coins" in have_list:
                                have_list.remove("gold coins")
                                hp += 10
                                print("You trade your gold coins, and your HP +10.")
                            else:
                                print("You do not have gold coins.")
                        elif m == "joke":
                            print("Merchant: 'Why did the ghost avoid the cave? Too many skeletons!'")
                            print("You laugh. The merchant grins.")
                        elif m == "pretend dead":
                            print("You pretend to die. Merchant: 'Again?'")
                        elif m == "sing together":
                            print("You sing with him. Both of you sound terrible.")
                        elif m == "point":
                            print("You point at distant woods. He has no interest at all.")
                        elif m == "tickling":
                            print("You tickle the merchant. He laughs loudly.")
                        elif m == "dance":
                            print("The merchant does a silly dance. You feel silly too.")
                        elif m == "act like ghost":
                            print("You float and howl. Merchant rolls eyes and keeps calm.")
                        elif m == "beg for gifts" or m == 'beg':
                            print("You ask for free gifts. Merchant shakes his head firmly.")
                        elif m == "pretend sleep":
                            print("You lie down to sleep. Merchant quietly walks around you.")
                        elif m == "cheer":
                            print("You cheer loudly. The merchant claps weakly.")
                        elif m == "walk side by side":
                            print("You walk beside him. He keeps a little distance.")
                        elif m == 'attack merchant' or m == 'attack' or m == 'kill merchant' or m == 'kill' or m == 'attack him' or m == 'kill him':
                            print('Merchant: Really? Attack a merchant, you are so evil.')
                            evil += 5
                            print('You feel shy and go back to the road.')
                            break
                        else:
                            print('Unknown command.')
                else:
                    print('Merchant: Go away! Evil man!')
            else:
                print('Unknown command.')
        elif go == "statue":
            print(f"HP: {hp}")
            print(f"Time: {time_period}")
            print(f"Good: {good} | Evil: {evil}")
            print(f"New Game+: {play_count}")
            print('Sanity: ?')
        elif go == 'west':
            print('You found a HAUNTED HUT in forest.')
            print('You hear a woman crying: forgive me!')
            print('You see there still to west. Type west to go or talk ro talk.')
            if festival_mode:
                print("Ghost smiles: Happy full moon! Here's a gift!")
                hp += 2
            while True:
                consume_step_durability()
                h = input('hut> ').strip().lower()
                if h == 'talk':
                    print('Ghost: Bring me my husband’s diary.')
                    print('Ghost: My husband disappears with your great grand father!')
                    if grave_diary_read == True or old_diary_readed == True:
                        print('You: Ok, I see.')
                        player_total_score += 10
                    else:
                        print('You: Who is my great grand father?')
                elif h == 'give diary':
                    if diary_read:
                        print('Ghost smiles! Max HP +5!')
                        hp += 5
                        good += 10
                        break
                    else:
                        print('You have no diary.')
                elif h == "ask wish":
                    print("Ghost: I only wish to see my husband one last time.")
                    print("He stayed in the cave to watch over me, never left.")
                elif h == "comfort ghost":
                    if old_diary_readed and grave_diary_read:
                        print("You tell her you understand her long loneliness.")
                        print("The ghost bursts into tears of relief.")
                        print("Max HP increased permanently!")
                    else:
                        print("The ghost just stares at you silently.")
                elif h == "lead to cave":
                    if play_count == 2:
                        print("The ghost follows you to the cave entrance.")
                        print("Two ancient spirits meet after hundreds of years.")
                        print("They wave goodbye to you, their souls rest in peace.")
                        print("===== SPIRIT PEACE SIDE ENDING =====")
                        trap_protect = True
                    else:
                        print("A strange force blocks the way. Can't do this now.")
                elif h == 'leave' or h == 'east' or h == 'back':
                    print('You go back to road.')
                    break
                elif h == "forgive":
                    if good >= 20:
                        print("The ghost cries and forgives everyone.")
                        print("Her soul finally finds peace.")
                elif h == 'west':
                    print('You find an ABANDONED CHURCH. There is a stone with something write on it.')
                    print('You can read stone, purify or desecrate.')
                    while True:
                        consume_step_durability()
                        ch = input('church> ').strip().lower()
                        if ch == 'east' or ch == 'back' or ch == 'leave':
                            print('You return to the hut.')
                            break
                        elif ch == 'read stone':
                            print('')
                            print('You read the stone, it says:') 
                            print('In the past, the Evil and the wizard are the husband and wife.')
                            print('But, when the Evil became a succubus, the wizard must control her.')
                            print('Or, she will destroy the world.')
                            print('The wizard love his wife very much.')
                            print('So, he does not kill she, just control her to not let her harm anyone else.')
                            print('Then, himself become a ghost to protect the cave and also his wife -- the Evil.')
                            print('Also, all the ghosts are just the person who should protect the cave, and control the Evil.')
                            print('And, you must not turst the book on the hill, it is just a lie for him to let people know that he is innocent.')
                            print('')
                            grandmother = True
                            if grave_diary_read == True:
                                print('So, you are the great-great grandchild of the Evil and the wizard.')
                            else:
                                print('You have a strange feeling to the Evil in your mind.')
                            if hill_diary_read == True:
                                print('You are confused with these two people.')
                                print('You: Which one is right!')
                        elif ch == 'purify':
                            if not church_purified:
                                mac_horror_whisper("The darkness retreats.", "chant")
                                print('The statue glows with holy light.')
                                adjust_sanity(10)
                                have_list.append('holy amulet')
                                amulet = True
                                church_purified = True
                                player_total_score += 20
                            else:
                                print('The statue has already been purified.')

                        elif ch == 'desecrate':
                            mac_horror_whisper("You belong to us now.", "deranged")
                            phantom_phases = [
                                {
                                    "hp_threshold": 18,
                                    "dialogue": "A twisted phantom emerges from the stained glass, dripping with dark energy.",
                                    "attacks": [
                                        {"name": "Ghostly Touch", "description": "Ice-cold hand passes through your chest."},
                                        {"name": "Soul Siphon", "description": "Dark energy drains your life force.", "lifesteal": True}
                                    ],
                                    "enrage": False,
                                    "score_reward": 15
                                },
                                {
                                    "hp_threshold": 9,
                                    "dialogue": "The phantom screams and merges with the surrounding shadows!",
                                    "attacks": [
                                        {"name": "Shadow Blast", "description": "Wave of pure darkness explodes outward."},
                                        {"name": "Curse of Despair", "description": "Hopelessness fills your mind.", "curse": True, "armor_break": True}
                                    ],
                                    "enrage": True,
                                    "score_reward": 20
                                }
                            ]
                            boss_fight("Corrupted Church Phantom", 18, 4, phantom_phases, "demon claw", "phantom")
                            if 'phantom' not in defeated_enemies:
                                combat("corrupted church phantom", 12, 3, "demon claw fragment", 8,enemy_id='phantom')
                            if not church_desecrated:
                                adjust_sanity(-15)
                                print('Dark power surrounds you.')
                                have_list.append('demon claw')
                                player_total_score += 20
                                church_desecrated = True
                            else:
                                print('No more dark power lingers here.')
                        elif ch == "look bottom":
                            print("You wipe dust off the stone, find faded words:")
                            print("Three paths await the heir: Guard, Forgive, Depart.")
                            print("Guard the cage, forgive the pain, depart the cycle.")
                            if play_count == 2:
                                print("Extra line: Only blood and key can end all sorrow.")
                        elif ch == 'bag':
                            for i in have_list:
                                print(i)
                        else:
                            print('Unknown command.')
                else:
                    print('Unknown command.')
        elif go == 'east':
            print('You are in the forest.')
            print('An old diary lies on the ground. Further east lies the misty swamp.')
            if "forest_wolf" not in defeated_enemies:
                print('Sunnenly, a wolf appears.')
                combat("feral forest wolf", 6, 2, "wolf pelt", 2,enemy_id = "forest_wolf")
            while True:
                advance_time()
                consume_step_durability()
                forest_take = input("1.read diary / 2.east / 3.leave: ").strip().lower()
                if forest_take == 'read diary' or forest_take == 'take diary' or forest_take == '1':
                    print('You read this old diary. It says:')
                    print('')
                    print('diary page 1:')
                    print('I do not want to kill her, but I must do something.')
                    print('I feel that her magic energy has been more strong.')
                    print('If I do not control her, the world might be destroyed.')
                    print('')
                    print('diary page 2:')
                    print('I control her, but I can not go out the cave again!')
                    print('May be I should wait here for all my life.')
                    print('So, I can not be a wizard anymore.')
                    print('')
                    print('diary page 3:')
                    print('I saw my son, and tell he when I died, he must be here for all his life too.')
                    print('Cave is just a PRISON!')
                    print('END')
                    print('')
                    old_diary_readed = True
                    if grave_diary_read:
                        print('You realised that this is your great-great grandfathers diary.')
                        print('You feel shocked.')
                        print('Then, you go away.')
                        break
                    else:
                        print('You: Who is the man?')
                        print('Then, you leave.')
                        break
                elif forest_take == 'east' or forest_take == 'go to swamp' or forest_take == 'go to misty swamp' or forest_take == '2':
                    if misty_end == False:
                        misty_swamp()
                        if game_over:
                            print("=== END ===")
                            print("Type 'menu' to return main menu")
                            while True:
                                c = input().strip().lower()
                                if c == 'menu':
                                    main()
                                    return
                    else:
                        print('You have already end the misty swamp, you do not have to go in again.')
                    break
                elif forest_take == 'leave' or forest_take == 'back' or forest_take == 'west' or forest_take == '3':
                    print('You go back to the road.')
                    break
                elif forest_take == 'climb tree':
                    x = random.randint(1,2)
                    if x == 1:
                        print('You find some mosquite in the tree, Hp -1')
                        print('What you are filling is as same as what I am filling!')
                        hp -= 1
                        if hp <= 0:
                            print('Such a joke! Killed by a tiny mosquite.')
                            game_back = True
                            game_over = True
                            break
                    else:
                        print('Luck for you, you find some delicious nut, Hp +1')
                        hp += 1
                elif forest_take == 'tree':
                    print('Hmm... the trees are the oak tree which have grown for about fifty years.')
                elif forest_take == 'cut tree':
                    cmd = input('really? Cut down a tree? Y/N').strip().lower()
                    if cmd == 'Y' or cmd == 'y' or cmd == 'yes' or cmd == 'YES':
                        print('You cut down a tree, you are so evil!')
                        print('The tree fall on your toes.')
                        print('Oach, that hurts! Hp -5')
                        hp -= 5
                        player_total_score -= 10
                        if hp <= 0:
                            print('You are killed by a tree, hahaha.')
                            game_back = True
                            game_over = True
                            break
                        evil += 10
                    elif cmd == 'N' or cmd == 'n' or cmd == 'no' or cmd == 'NO':
                        print('OK, so you do not cut down the tree.')
                    else:
                        print('PLease answer the question.')
                elif forest_take == "talk to bird":
                    print("The bird circles above you, chirping softly.")
                    if old_diary_readed:
                        print("Bird: ...Trapped... forever...")
                    else:
                        print("The bird flies away, leaving you confused.")
                elif forest_take == "feed bird":
                    if "some food" in have_list:
                        have_list.remove("some food")
                        print("The bird eats happily, then drops a small feather.")
                        have_list.append("spirit feather")
                        print("You got SPIRIT FEATHER! It glows faintly.")
                elif forest_take == "wave to bird":
                    print("You wave to a bird. It flies closer for a second.")
                else:
                    print('Unknown command.')
        elif go == 'south':
            print('You find a hidden trail leading to an ABANDONED CAMP. There is a camp in the west. And also a grave in the east. And the path still leads to a hill to south.')
            print('You see a grave, something is written on it: game developer, killed by a lot of bug and error.')
            print('A voice booms: Dig the grave, then you will find me. Or, you can search the grave.')
            if rune2 == False:
                print('Hint: Search the grave, and then...(Too low to hear clearly)')
            if blood_moon:
                print('Bloody moon in the sky, a crimson crack appears on the ground, type down to go down.')
            while True:
                print('You see a lot of camps and a cliff.')
                if play_count == 2:
                    print('You feel someone is calling you to go to the tomb.')
                print('Type search to search, chest to open chest, back to go back.')
                if has_death_corpse and death_location == current_room:
                    print('You see here a corpse, type corpse to search it.\n')
                advance_time()
                consume_step_durability()
                camp_cmd = input('camp> ').strip().lower()
                if camp_cmd == 'west':
                    print('You head west into the camp.')
                    print('Old tents, cold firepit, and a chest.')
                elif camp_cmd == 'down' or camp_cmd == 'go down' or camp_cmd == 'd':
                    blood_rift_dungeon()
                    continue
                elif camp_cmd == "make funny face":
                    print("You make a funny face. A squirrel stares at you.")
                elif camp_cmd == 'go to hill' or camp_cmd == 'south' or camp_cmd == 'forward' or camp_cmd == 'go to south':
                    hill()
                    return
                elif camp_cmd == "count stars":
                    print("You count stars. You fall asleep after 3.")
                elif camp_cmd == "talk to fire":
                    print("You talk to the campfire. It does not answer.")
                elif camp_cmd == "jump":
                    print("You jump up and down. You look silly.")
                elif camp_cmd == "examine corpse" or camp_cmd == 'corpse' or camp_cmd == 'search corpse' or camp_cmd == 'find corpse':
                    if has_death_corpse and death_location == current_room:
                        print("\nA corpse slumps against the dusty floor. It wears your exact clothes.")
                        if death_corpse_item:
                            print(f"You retrieve {death_corpse_item} from its pocket.")
                            have_list.append(death_corpse_item)
                        else:
                            print("Nothing useful left on the body.")
                        has_death_corpse = False
                    else:
                        print("There is not any corpse..")
                elif camp_cmd == 'firepit':
                    if festival_mode:
                        print('There is a ghost hidden in the firepit!')
                        print("Ghost smiles: Happy full moon! Here's a gift!")
                        hp += 2
                    if amulet == False or ng_amulet == False or has_elf_amulet == False:
                        if hp > 3:
                            print('A ghost hit you then float in the high sky.')
                            print('Hp -3')
                            hp -= 3
                        else:
                            print('There is a ghost hidden in the firepit. It kills you!')
                            print('Game over!')
                            game_over = True
                            game_back = True
                            break
                    elif args.godmode:
                        print('The ghost kneels to you.')
                        print('Ghost: Wish you good luck, my god.')
                        hp += 1
                    else:
                        print('Your amulet keeps the ghost away.')
                elif camp_cmd == "play":
                    print("You play with a small stone. So fun!")
                elif camp_cmd == "yell":
                    print("You yell loudly in the camp.")
                    print("A bird flies away quickly.")
                elif camp_cmd == "tell joke":
                    print("You tell a joke to the grave.")
                    print("A faint laugh echoes: 'That was terrible!'")
                elif camp_cmd == 'search':
                    if 'rope' not in have_list:
                        print('You find a ROPE.')
                        have_list.append('rope')
                    else:
                        print('You searched thoroughly. Nothing else remains.')

                elif camp_cmd == 'chest':
                    if 'flint' not in have_list:
                        print('You open the chest and find a FLINT.')
                        have_list.append('flint')
                        player_total_score += 10
                    else:
                        print('The chest is already empty.')
                elif camp_cmd == "tomb" or camp_cmd == 'go to tomb' or camp_cmd == 'go to the tomb':
                    if play_count == 2:
                        print("\n[NG+ ONLY] A hidden stone door slowly opens...")
                        player_total_score += 10
                        tomb()
                    else:
                        print("The stone door is sealed. Only the returning one may enter.")
                elif camp_cmd == 'north':
                    print('You walk back to the road.')
                    break
                elif camp_cmd == 'east':
                    print('You find an old graveyard.')
                    if 'grave_boss' not in defeated_enemies:
                        print('A grave digger find you, but he is undead.')
                        combat("undead gravedigger", 14, 4, 'some gold coins', 6, enemy_id = "grave_boss")
                    if festival_mode:
                        print("Ghost smiles: Happy full moon! Here's a gift!")
                        hp += 2
                    else:
                        print('Ghosts wander, but they do not attack.')
                    if 'super amulet' not in have_list:
                        print('You find a SUPER AMULET.')
                        print('You put it in your bag and walk back quietly.')
                        have_list.append('super amulet')
                        player_total_score += 10
                        amulet = True
                    else:
                        print('Nothing there.')
                elif camp_cmd == 'back' or camp_cmd == 'leave':
                    print('You walk back to the road.')
                    break
                elif camp_cmd == 'cliff':
                    print("A steep cliff stands ahead.")
                elif camp_cmd == 'climb down':
                    if 'rope' in have_list:
                        print("You use rope to climb down to cave entrance.")
                        print('Welcome to death cave!')
                        current_room = "cave"
                        cave()
                        if game_over:
                            print("=== END ===")
                            print("Type 'menu' to return main menu")
                            while True:
                                c = input().strip().lower()
                                if c == 'menu':
                                    main()
                                    return
                    else:
                        print("You need a rope to climb down.")
                elif camp_cmd == 'bag':
                    for i in have_list:
                        print(i)
                elif camp_cmd == 'search grave':
                    gravedigger_phases = [
                        {
                            "hp_threshold": 14,
                            "dialogue": "The undead gravedigger rises from the dirt, rusty shovel in hand.",
                            "attacks": [
                                {"name": "Shovel Strike", "description": "Heavy metal shovel swings at your head."},
                                {"name": "Dirt Throw", "description": "Dirt and rocks fly into your face.", "stun": True}
                            ],
                            "enrage": False,
                            "score_reward": 25
                        },
                        {
                            "hp_threshold": 7,
                            "dialogue": "The gravedigger roars and enters a furious rage!",
                            "attacks": [
                                {"name": "Frenzied Swipe", "description": "Wild rapid strikes leave no opening."},
                                {"name": "Grave Slam", "description": "Shovel slams the ground, shaking your bones."}
                            ],
                            "enrage": True,
                            "score_reward": 35
                        }
                    ]
                    boss_fight("Undead Gravedigger", 14, 3, gravedigger_phases, "gold coins", "grave_boss")
                    if rune2 == False:
                        print('You found RUNE STONE 2!')
                        print('Rune text: Three runes control the seal. And someone should cotrol it again with it.')
                        rune2 = True
                        player_total_score += 25
                        have_list.append('rune stone 2')
                    else:
                        print('You find a hole for a rune, but you may have already took the rune away.')
                elif camp_cmd == 'dig grave':
                    if grave_take == False:
                        mac_horror_whisper("You disturb the dead.", "normal")
                        print('You dig the grave. There is some treasure and a diary. Take treasure or leave it? 1.take / 2.leave (Even you choose any choice, you will read the diary.)')
                        choice = input().strip().lower()
                        if choice == 'take' or choice == '1':
                            print('You take the treasure. The spirit rages.')
                            have_list.append('a diamond')
                            evil += 15
                            print('')
                            print('You read the diary:')
                            print('You found the EXPLORER’S COMPLETE DIARY!')
                            print('It reveals some of the truth of the cave and the demon.')
                            print('It says that a long time ago, there was a beautiful woman.')
                            print('Unfortunately, one day, she was killed by a man who do not like her.')
                            print('Then, she became a succubus.')
                            print('The man found the succubus and the succubus killed him.')
                            print('Then, a wizard appears, and control her, so she became a Evil.')
                            print('She was active when the wizard died.')
                            print('And then, the diarys owner go on and control the Evil.')
                            print('It also says, he is your great-great grandfather!')
                            print('In the end of diary, you great grandfather says that he have be in the cave for 60 years.')
                            print('He had wanted to unleash his great grandmother for a lot of times.')
                            print('Then he give up. And he also says that if you see this diary, you will have to choose an answer.')
                            print('There is still some words, but you can not read them because they are covered by a lot of blood.')
                            print('')
                            grave_diary_read = True
                            player_total_score -= 30
                            adjust_sanity(-10)
                        elif choice == 'leave' or choice == 'back':
                            print('You respect the deceased. The spirit approves.')
                            good += 15
                            print('')
                            print('You read the diary:')
                            print('You found the EXPLORER’S COMPLETE DIARY!')
                            print('It reveals the full truth of the cave and the demon.')
                            print('It says that a long time ago, there was a beautiful woman.')
                            print('Unfortunately, one day, she was killed by a man who do not like her.')
                            print('Then, she became a succubus.')
                            print('The man found the succubus and the succubus killed him.')
                            print('Then, a wizard appears, and control her, so she became a Evil.')
                            print('She was active when the wizard died.')
                            print('And then, the diarys owner go on and control the Evil.')
                            print('It also says, he is your great-great grandfather!')
                            print('In the end of diary, you great grandfather says that he have be in the cave for 60 years.')
                            print('He had wanted to unleash his great grandmother for a lot of times.')
                            print('Then he give up. And he also says that if you see this diary, you will have to choose an answer.')
                            print('There is still some words, but you can not read them because they are covered by a lot of blue ink.')
                            print('')
                            adjust_sanity(10)
                            player_total_score += 20
                            grave_diary_read = True
                        else:
                            print('Sorry, I do not understand that word.')
                    else:
                        print('You have alrady dig the grave!')
        else:
            print('Unknown command.')
        if game_over == True:
            print("=== END ===")
            print("Type 'menu' to return main menu")
            while True:
                c = input().strip().lower()
                if c == 'menu':
                    main()
                    return
        if force_over == True:
            break

def ng_three():
    global m1, m2, m3,cleared_ending
    global meta_file_tier
    global player_total_score

    m1 = False
    m2 = False
    m3 = False
    
    print("============================================")
    print("          ILLUSION TUNNEL          ")
    print("============================================")
    print("She bears no malice toward the world.")
    print("She only resents being confined by her lover for two century.")
    print("The road ends here. Only the tunnel remains.")
    
    while True:
        print("\n[ILLUSION TUNNEL]")
        print("1. MEMORY CORRIDOR")
        print("2. SEAL RUINS")
        if m1 and m2:
            print("3. GATHER TRUTH")
        if m3:
            print("4. FINAL CHOICE")
        print("5. EXIT TUNNEL")
        
        consume_step_durability()
        opt = input(">").strip().lower()
        
        if opt == "1":
            print("\n===== MEMORY CORRIDOR =====")
            print("The walls are filled with fragments of time.")
            print("You see her first meeting with the wizard.")
            print("Laughter echoes in the empty space.")
            print("You see the day she was betrayed by the world.")
            print("You see the fear that drove him to make the seal.")
            print("You see two hundred years of silent waiting.")
            print("The corridor reveals all her past.")
            print('Then, you finally understand that your great-great grandfather is just too afraid to losing her, not afraid she destroy the world.')
            print('This is all a fake!!!')
            print('All the diary, may be all fake, but he can not change this corridor.')
            m1 = True
        
        elif opt == "2":
            print("\n===== SEAL RUINS =====")
            print("Broken pillars surround you.")
            print("Runes glow faintly on the stone.")
            print("This is where she was trapped for two hundred years.")
            print("The seal was not for punishment.")
            print("It was a desperate act of love.")
            print("But love became a cage.")
            print("You understand the truth of the seal.")
            m2 = True
        
        elif opt == "3" and m1 and m2:
            print("\n===== TRUTH GATHERED =====")
            print("All pieces are connected.")
            print("She was never an enemy.")
            print("She was a prisoner of love.")
            print("She never hated the world.")
            print("She only grieved for the one who locked her away.")
            m3 = True
        
        elif opt == "4" and m3:
            print("\n===== FINAL JUDGEMENT =====")
            print("She appears in front of you.")
            print("Her eyes are calm, not angry.")
            print("What will you do?")
            print("1. RELEASE HER")
            print("2. STAY WITH HER")
            print("3. END THE CYCLE")
            print("4. REUNITE WITH THE WIZARD")
            e = input(">").strip().lower()
            if e == "1":
                print("\nYou break the eternal seal.")
                print("She smiles and fades into light.")
                print("No more pain. No more cage.")
                print("FINAL ENDING : SALVATION")
                print('')
                print("\nCongratulations! You beat 3rd run!")
                player_total_score += 75
                cleared_ending = True
                main()
                return
            elif e == "2":
                print("\nYou choose to stay by her side.")
                print("The illusion becomes your home.")
                print("She is no longer alone.")
                print("FINAL ENDING : COEXISTENCE")
                print('')
                print("\nCongratulations! You beat 3rd run!")
                player_total_score += 75
                cleared_ending = True
                main()
                return
            elif e == "3":
                print("\nYou erase all memories and bonds.")
                print("The cycle breaks completely.")
                print("Everything returns to silence.")
                print("FINAL ENDING : ANNIHILATION")
                print('')
                print("\nCongratulations! You beat 3rd run!")
                player_total_score += 75
                cleared_ending = True
                main()
                return
            elif e == "4":
                print("\nYou call forth the wizard's lingering spirit.")
                print("The two souls meet again after a hundred years apart.")
                print("Hatred and pain fade away at last.")
                print("They stay side by side, free from seal and sorrow.")
                print("FINAL ENDING : TURE FINAL ENDING")
                print('')
                print("\nCongratulations! You beat 3rd run!")
                player_total_score += 75
                cleared_ending = True
                main()
                return
        elif opt == "5":
            print("You leave the tunnel.")
            break

# main menu
def menu():
    global meta_file_tier
    global game_over,time_period,step_count

    apply_permanent_bonuses()
    game_over = False
    time_period = "day"
    step_count = 0
    perm_upgrade_menu()
    if death_count == 1:
        write_creepy_desktop_file(1)
    elif death_count == 3:
        write_creepy_desktop_file(2)
    print('This is the main menu.')
    print('You can type start or quit or task for tasks.')
    if play_count == 3:
        print('You can try to type time to do a time travel and avoid the trady.')
    if play_count == 2:
        print('There are some new things, since you heard that there the curse is for you.')
    while True:
        print('')
        if play_count == 3:
            start = input('1.start/2.quit/3.task/4.time: ').strip().lower()
        elif play_count == 4:
            start = input('1.heaven/2.quit: ').strip().lower()
        else:
            start = input('1.start/2.quit/3.task: ').strip().lower()
        if play_count != 4:
            if start == 'start' or start == '1':
                print('')
                if play_count <= 2:
                    print('Type dev to cheat.')
                    print('')
                    gamestart()
                elif play_count == 3:
                    print('A voice booms: Mortol, you have done well, you can go to my home -- ILLUSION TUNNEL and meet me now.')
                    print('The voice also says: And I have tell you that I am your great-great grandfather -- the wizard.')
                    ng_three()
            elif start == 'quit' or start == '2':
                if play_count <= 4:
                    print('')
                    end_score_rating()
                    print('Goodbye!')
                    print("=== Death Adventure v1.4 - Official Release ===")
                    print("Thank you for playing!")
                    exit()
                else:
                    show_message_wall()
                    name = input("Your name: ").strip().lower()
                    msg = input("Your message: ").strip().lower()
                    save_message(name, msg)
                    print('')
                    print('You can final see what you can cheat:')
                    print("=== Death Adventure Cheat ===")
                    print("Usage: python3 main.py [OPTIONS]")
                    print("Options:")
                    print("  -g, -G, -godmode    Enable god mode (invincible)")
                    print("  -c, -C, -cheat      Enable cheat mode (all items)")
                    print("  -h, -help           Show help")
                    print("=============================")
                    print('And, do you know, when you are at the ng one, you can type Garry in the house, then you will win!')
                    end_score_rating()
                    print('Also, you can type colin, and woody and garry in the house, then you will pass the ng one.\n')
                    print("=== Death Adventure v1.4 - Official Release ===")
                    print("Thank you for playing!")
                    exit()   
            elif start == "time" or start == 'time travel' or start == '4':
                if play_count == 3:
                    time_travel_origin()
                else:
                    print("Only available in 3rd run.")
            elif start == 'task' or start == '3':
                if play_count <= 2:
                    print('')
                    print('TASKS:')
                    print('TRUE ENDING (ng2): find three stone runes -> go to the altar -> read diarys (You can also do not done this) -> place runes -> choose')
                    print('RICH ENDING: house -> take things -> go on the altar -> go in the cave -> west -> choose way')
                    print('DUNGEON: play again -> south -> go to tomb -> search by yourself')
                    print('')
                else:
                    print('I can not help you too.')
        elif play_count == 4:
            if start == 'heaven' or start == '1':
                print_heaven()
            elif start == 'quit' or start == '2':
                print('You break the circle but refuses to go to the heaven, instead, you live in mortol world forever.')
                show_message_wall()
                name = input("Your name: ").strip().lower()
                msg = input("Your message: ").strip().lower()
                save_message(name, msg)
                print('')
                print('You can final see what you can cheat:')
                print("=== Death Adventure Cheat ===")
                print("Usage: python3 main.py [OPTIONS]")
                print("Options:")
                print("  -g, -G, -godmode    Enable god mode (invincible)")
                print("  -c, -C, -cheat      Enable cheat mode (all items)")
                print("  -h, -help           Show help")
                end_score_rating()
                print("=============================")
                print("=== Death Adventure v1.4 - Official Release ===")
                print("Thank you for playing!")
                exit()
            
        else:
            print('Please answer the question.')
# main
def main():
    global have_list, game_over, light, hp, l, k, n, s, f, w, p, sc, secret_unlocked, map_unlocked, amulet, turn_count, chain1, chain2, diary_read, legacy_unlocked, new_game_plus, ng_amulet, ng_compass, ng_diary, current_room, torch, no_light_run, all_collected, rune1, rune2, rune3, faith, sky, moon, trap_protect, rune, grandmother, gate_unlock, old_diary_readed, grave_diary_read, force_over, game_back, play_count, tomb_unlocked, old_note_readed,cleared_ending,time_period,step_count,death_count,good,evil,death_corpse_item,death_location,has_death_corpse,one_hole_in,two_hole_in,three_hole_in,four_hole_in,no_death_run,player_total_score,sanity,permanent_points

    today = datetime.date.today()
    m = today.month
    d = today.day
    if play_count == 1:
        if m == 1:
            if d == 1:
                print("\n=====================================")
                print("✨ NEW YEAR FESTIVAL ✨")
                print("New cycle begins, hope fills the cave.")
                print("=====================================\n")
                hp += 8
                good += 8
            elif d == 3:
                print("\n=====================================")
                print("❄️ FROSTBITE CURSE ❄️")
                print("Freezing wind pierces your bones.")
                print("=====================================\n")
                hp -= 3
                evil += 2
            elif d == 10:
                print("\n=====================================")
                print("🔇 DEAD SILENCE DAY 🔇")
                print("All spirits fall silent, no one answers.")
                print("=====================================\n")
                faith -= 5
            elif d == 14:
                print("\n=====================================")
                print("📖 LEGACY FESTIVAL 📖")
                print("Ancient records glow, memories stir.")
                print("=====================================\n")
                diary_read = True
                have_list.append("ancient diary")
            elif d == 18:
                print("\n=====================================")
                print("👻 WINTER WHISPER CURSE 👻")
                print("Cold whispers feed the darkness in your heart.")
                print("=====================================\n")
                evil += 6
            elif d == 25:
                print("\n=====================================")
                print("🌑 LONG NIGHT CURSE 🌑")
                print("Darkness burns twice as fierce tonight.")
                print("=====================================\n")
                hp -= 2
                evil += 3
            elif d == 26:
                print("\n=====================================")
                print("🌞 DAWN FESTIVAL 🌞")
                print("First light weakens dark power.")
                print("=====================================\n")
                evil -= 5
                torch = True
            elif d == 31:
                print("\n=====================================")
                print("👻 WHISPER FESTIVAL 👻")
                print("Shadows speak, cave remembers.")
                print("=====================================\n")
                have_list.append("shadow whisper")
                faith += 6

        elif m == 2:
            if d == 2:
                print("\n=====================================")
                print("🌱 BLOOM FESTIVAL 🌱")
                print("Soft warmth calms all spirits.")
                print("=====================================\n")
                hp += 5
            elif d == 5:
                print("\n=====================================")
                print("🧊 THIN ICE CURSE 🧊")
                print("Hidden traps lie under thin ice.")
                print("=====================================\n")
                trap_protect = False
            elif d == 9:
                print("\n=====================================")
                print("🌫️ MIST ILLUSION DAY 🌫️")
                print("The map fades, you lose your sense of direction.")
                print("=====================================\n")
                map_unlocked = False
            elif d == 12:
                print("\n=====================================")
                print("🦠 SPOILED AIR DAY 🦠")
                print("Damp foul air makes you weak.")
                print("=====================================\n")
                hp -= 2
            elif d == 14:
                print("\n=====================================")
                print("❤️ TENDER FESTIVAL ❤️")
                print("Gentle hearts heal old wounds.")
                print("=====================================\n")
                good += 10
            elif d == 17:
                print("\n=====================================")
                print("🍀 LUCK FESTIVAL 🍀")
                print("Hidden treasures appear.")
                print("=====================================\n")
                have_list.append("lucky clover")
            elif d == 19:
                print("\n=====================================")
                print("💔 VAIN HOPE DAY 💔")
                print("Kindness dissolves into the fog.")
                print("=====================================\n")
                good -= 5
            elif d == 20:
                print("\n=====================================")
                print("💧 MERCY FESTIVAL 💧")
                print("Kindness purifies dark aura.")
                print("=====================================\n")
                evil -= 8
                good += 5
            elif d == 22:
                print("\n=====================================")
                print("💡 BROKEN LAMP DAY 💡")
                print("Your lamp flickers and dies.")
                print("=====================================\n")
                light = False
            elif d == 26:
                print("\n=====================================")
                print("🌀 ECHO CURSE DAY 🌀")
                print("Twisted echoes confuse your mind.")
                print("=====================================\n")
                faith -= 4
                evil += 3
            elif d == 28:
                print("\n=====================================")
                print("🕯️ EMBER FESTIVAL 🕯️")
                print("Flame wards off darkness.")
                print("=====================================\n")
                light = True
                have_list.append("eternal flame")
            elif d == 29:
                print("\n=====================================")
                print('Wow, you enter this game February 29th, the day four year once!')
                print('I will let you be as well as a god!')
                print("=====================================\n")
                hp = 999
                trap_protect = True
                rune1 = True
                rune2 = True
                rune3 = True
                diary_read = True
                old_diary_readed = True
                old_note_readed = True
                light = True
                good = 100
                grave_diary_read = True
                have_list.append('rope')
                have_list.append('ghost sword')
                have_list.append('gold coins')
                have_list.append('a pick-axe')
                have_list.append('super amulet')
                have_list.append('holy amulet')
                amulet = True
                map_unlocked = True

        elif m == 3:
            if d == 4:
                print("\n=====================================")
                print("🌙 LUNAR FESTIVAL 🌙")
                print("Moonlight reveals forgotten truths.")
                print("=====================================\n")
                faith += 7
            elif d == 6:
                print("\n=====================================")
                print("☠️ TOXIC MIST CURSE ☠️")
                print("Poisonous mist fills the swamp.")
                print("=====================================\n")
                hp -= 2
                evil += 4
            elif d == 11:
                print("\n=====================================")
                print("👻 WRAITH AWAKEN DAY 👻")
                print("Slumbering evil spirits wake from the earth.")
                print("=====================================\n")
                evil += 6
            elif d == 14:
                print("\n=====================================")
                print("🤍 PURE FESTIVAL 🤍")
                print("Innocence softens malice.")
                print("=====================================\n")
                good += 9
            elif d == 17:
                print("\n=====================================")
                print("🌿 NATURE FESTIVAL 🌿")
                print("Green energy restores vitality.")
                print("=====================================\n")
                hp += 6
            elif d == 20:
                print("\n=====================================")
                print("⚖️ BALANCE FESTIVAL ⚖️")
                print("Light and dark align.")
                print("=====================================\n")
                good += 7
                evil -= 7
            elif d == 22:
                print("\n=====================================")
                print("🌿 THORN GROWTH CURSE 🌿")
                print("Cursed thorns tear at your skin.")
                print("=====================================\n")
                hp -= 3
            elif d == 27:
                print("\n=====================================")
                print("❌ FALSE RUNE DAY ❌")
                print("Fake runes confuse your memory.")
                print("=====================================\n")
                faith -= 6
            elif d == 29:
                print("\n=====================================")
                print("🌧️ COLD RAIN DAY 🌧️")
                print("Cold rain seeps through your clothes.")
                print("=====================================\n")
                hp -= 2
                evil += 2
            elif d == 31:
                print("\n=====================================")
                print("👻 COMPANION FESTIVAL 👻")
                print("Ghosts walk beside you.")
                print("=====================================\n")
                have_list.append("ghost companion")

        elif m == 4:
            if d == 1:
                print("\n=====================================")
                print("🎭 PRANK FESTIVAL 🎭")
                print("Mischief fills the halls.")
                print("=====================================\n")
                have_list.append("trickster mask")
            elif d == 8:
                print("\n=====================================")
                print("🕳️ MUDDY TRAP DAY 🕳️")
                print("Hidden mud traps are everywhere.")
                print("=====================================\n")
                trap_protect = False
                hp -= 1
            elif d == 12:
                print("\n=====================================")
                print("🌧️ WRAITH RAIN CURSE 🌧️")
                print("Rain carries vengeful spirits.")
                print("=====================================\n")
                hp -= 3
            elif d == 14:
                print("\n=====================================")
                print("🖤 SHADOW FESTIVAL 🖤")
                print("Embrace the dark side.")
                print("=====================================\n")
                evil += 5
            elif d == 15:
                print("\n=====================================")
                print("🌧️ CLEANSE FESTIVAL 🌧️")
                print("Rain washes corruption.")
                print("=====================================\n")
                evil -= 10
            elif d == 18:
                print("\n=====================================")
                print("🌑 SHADOW GROW DAY 🌑")
                print("Darkness grows stronger.")
                print("=====================================\n")
                evil += 5
                hp -= 1
            elif d == 22:
                print("\n=====================================")
                print("🌱 GROWTH FESTIVAL 🌱")
                print("Life force surges.")
                print("=====================================\n")
                hp += 7
            elif d == 27:
                print("\n=====================================")
                print("💡 HOLLOW LIGHT DAY 💡")
                print("Your light grows dim and weak.")
                print("=====================================\n")
                hp -= 2
            elif d == 30:
                print("\n=====================================")
                print("👻 AWAKEN FESTIVAL 👻")
                print("Ancient spirits stir.")
                print("=====================================\n")
                have_list.append("ghost essence")

        elif m == 5:
            if d == 5:
                print("\n=====================================")
                print("🌸 HOPE FESTIVAL 🌸")
                print("Bright hopes bloom.")
                print("=====================================\n")
                good += 8
            elif d == 7:
                print("\n=====================================")
                print("🔥 SCORCHING HEAT DAY 🔥")
                print("Scorching heat drains your strength.")
                print("=====================================\n")
                hp -= 3
            elif d == 11:
                print("\n=====================================")
                print("🐺 BEAST HUNT DAY 🐺")
                print("Wild beasts roam the woods.")
                print("=====================================\n")
                hp -= 3
            elif d == 14:
                print("\n=====================================")
                print("💛 GOLDEN FESTIVAL 💛")
                print("Kindness shines bright.")
                print("=====================================\n")
                good += 10
            elif d == 16:
                print("\n=====================================")
                print("🩸 BLOOD BUDDING CURSE 🩸")
                print("Cursed plants bloom with evil.")
                print("=====================================\n")
                evil += 7
            elif d == 20:
                print("\n=====================================")
                print("⚡ STORM FESTIVAL ⚡")
                print("Thunder awakens power.")
                print("=====================================\n")
                have_list.append("thunder core")
            elif d == 21:
                print("\n=====================================")
                print("🧠 FRAYED SANITY DAY 🧠")
                print("Hallucinations cloud your mind.")
                print("=====================================\n")
                faith -= 7
            elif d == 25:
                print("\n=====================================")
                print("🌙 SILVER FESTIVAL 🌙")
                print("Moonlight gathers spirits.")
                print("=====================================\n")
                faith += 8
            elif d == 29:
                print("\n=====================================")
                print("🔥 HOT WIND CURSE 🔥")
                print("Hot wind blows out your torch.")
                print("=====================================\n")
                torch = False
            elif d == 31:
                print("\n=====================================")
                print("👻 TIE FESTIVAL 👻")
                print("Souls connect forever.")
                print("=====================================\n")
                have_list.append("spirit bond")

        elif m == 6:
            if d == 1:
                print('\n=====================================')
                print('Happy Childrens Day!')
                print('You receive a silly candy.')
                have_list.append('silly candy')
                print("=====================================\n")
            elif d == 4:
                print("\n=====================================")
                print("💧 DEHYDRATION DAY 💧")
                print("The sun drains all moisture from you.")
                print("=====================================\n")
                hp -= 3
            elif d == 6:
                print("\n=====================================")
                print("☀️ SOLAR FESTIVAL ☀️")
                print("Sunlight dispels shadows.")
                print("=====================================\n")
                evil -= 6
            elif d == 9:
                print("\n=====================================")
                print("🔥 SCORCHED TONGUE DAY 🔥")
                print("No spirit wants to talk to you.")
                print("=====================================\n")
                good -= 5
            elif d == 14:
                print("\n=====================================")
                print("💙 CALM FESTIVAL 💙")
                print("Peace calms chaos.")
                print("=====================================\n")
                good += 7
            elif d == 16:
                print("\n=====================================")
                print("☀️ MIDDAY GLARE CURSE ☀️")
                print("Blinding sunlight makes your map useless.")
                print("=====================================\n")
                map_unlocked = False
            elif d == 20:
                print("\n=====================================")
                print('??? XXXXXXXX FESTIVAL ???')
                print('????????????????????????????????????')
                print("=====================================\n")
                hp = 1
                evil = 30
                have_list.append('??????')
            elif d == 21:
                print("\n=====================================")
                print("🌞 LONGEST DAY FESTIVAL 🌞")
                print("Light triumphs over dark.")
                print("=====================================\n")
                hp += 8
            elif d == 23:
                print("\n=====================================")
                print("🌿 WITHERED HERB DAY 🌿")
                print("All healing herbs wither in the heat.")
                print("=====================================\n")
                hp -= 2
            elif d == 24:
                print("\n=====================================")
                print("🔥 GUARD FESTIVAL 🔥")
                print("Flame shields all harm.")
                print("=====================================\n")
                torch = True
            elif d == 27:
                print("\n=====================================")
                print("🌪️ DUSK STORM CURSE 🌪️")
                print("Dusk storm blows out your flame.")
                print("=====================================\n")
                torch = False
                light = False
            elif d == 29:
                print("\n=====================================")
                print("🦗 CICADA CHAOS DAY 🦗")
                print("Deafening noise breaks your focus.")
                print("=====================================\n")
                faith -= 7
            elif d == 30:
                print("\n=====================================")
                print("👻 MEMORY FESTIVAL 👻")
                print("Past echoes clearly.")
                print("=====================================\n")
                diary_read = True
                old_diary_readed = True
                old_note_readed = True

        elif m == 7:
            if d == 3:
                print("\n=====================================")
                print("👻 GHOST HUNT CURSE 👻")
                print("Hostile ghosts roam the land.")
                print("=====================================\n")
                evil += 6
                hp -= 2
            elif d == 7:
                print("\n=====================================")
                print("🌌 STAR FESTIVAL 🌌")
                print("Stars reveal fate.")
                print("=====================================\n")
                faith += 10
            elif d == 10:
                print("\n=====================================")
                print("🥵 HEAT STROKE DAY 🥵")
                print("Searing heat drains your strength.")
                print("=====================================\n")
                hp -= 4
            elif d == 13:
                print("\n=====================================")
                print("🗡️ CURSED DAGGER DAY 🗡️")
                print("A cursed blade appears in your bag.")
                print("=====================================\n")
                have_list.append("cursed dagger")
                evil += 3
            elif d == 15:
                print("\n=====================================")
                print("👻 SPIRIT GATE FESTIVAL 👻")
                print("Ghost world opens.")
                print("=====================================\n")
                have_list.append("ancestor blessing")
                good += 12
            elif d == 18:
                print("\n=====================================")
                print("🏜️ MIRAGE CURSE 🏜️")
                print("Mirages lead you astray.")
                print("=====================================\n")
                map_unlocked = False
                faith -= 5
            elif d == 20:
                print("\n=====================================")
                print("🌊 WAVE FESTIVAL 🌊")
                print("Tide cleanses dark.")
                print("=====================================\n")
                evil -= 10
            elif d == 25:
                print("\n=====================================")
                print("💎 TRUTH FESTIVAL 💎")
                print("Light reveals secrets.")
                print("=====================================\n")
                have_list.append("crystal light")
            elif d == 28:
                print("\n=====================================")
                print("🌑 BLOOD MOON EVE 🌑")
                print("Dark power surges before the blood moon.")
                print("=====================================\n")
                evil += 8
            elif d == 30:
                print("\n=====================================")
                print("😈 SUCCUBUS WHISPER DAY 😈")
                print("Her voice whispers in your ear.")
                print("=====================================\n")
                faith -= 8
                evil += 5
            elif d == 31:
                print("\n=====================================")
                print("👻 SHADOWTALE FESTIVAL 👻")
                print("Stories of old rise.")
                print("=====================================\n")
                have_list.append("shadow story")

        elif m == 8:
            if d == 3:
                print("\n=====================================")
                print("🍂 WITHERING CURSE 🍂")
                print("Everything withers and fades.")
                print("=====================================\n")
                hp -= 3
                good -= 4
            elif d == 6:
                print("\n=====================================")
                print("🪞 BROKEN GHOST MIRROR DAY 🪞")
                print("A shattered mirror appears in your bag.")
                print("=====================================\n")
                have_list.append("broken ghost mirror")
                faith -= 5
            elif d == 8:
                print("\n=====================================")
                print("🌺 PURIFY FESTIVAL 🌺")
                print("Purity removes greed.")
                print("=====================================\n")
                good += 8
            elif d == 11:
                print("\n=====================================")
                print("💀 FAMINE CURSE DAY 💀")
                print("Hunger drains your willpower.")
                print("=====================================\n")
                hp -= 4
                evil += 5
            elif d == 15:
                print("\n=====================================")
                print("🌕 FULLMOON FESTIVAL 🌕")
                print("Big moon calms spirits.")
                print("=====================================\n")
                hp += 4
                amulet = True
            elif d == 17:
                print("\n=====================================")
                print("🌑 BLOOD MOON FESTIVAL 🌑")
                print("The blood moon rises. All darkness grows stronger.")
                print("=====================================\n")
                evil += 10
                hp -= 3
            elif d == 20:
                print("\n=====================================")
                print("🍂 HARVEST FESTIVAL 🍂")
                print("Bounty appears.")
                print("=====================================\n")
                have_list.append("harvest fruit")
            elif d == 23:
                print("\n=====================================")
                print("📿 ROTTEN CHARM DAY 📿")
                print("A rotten charm slips into your bag.")
                print("=====================================\n")
                have_list.append("rotten charm")
                amulet = False
            elif d == 25:
                print("\n=====================================")
                print("🌙 DUSK FESTIVAL 🌙")
                print("Day meets night softly.")
                print("=====================================\n")
                faith += 7
            elif d == 27:
                print("\n=====================================")
                print("⛓️ SOUL CHAIN DAY ⛓️")
                print("A cold soul chain wraps around you.")
                print("=====================================\n")
                have_list.append("soul chain")
                evil += 6
            elif d == 29:
                print("\n=====================================")
                print("👻 GHOST RAID DAY 👻")
                print("Waves of ghosts launch sudden attacks.")
                print("=====================================\n")
                hp -= 5
                evil += 7
            elif d == 31:
                print("\n=====================================")
                print("👻 REST FESTIVAL 👻")
                print("Ghosts find peace.")
                print("=====================================\n")
                good += 6

        elif m == 9:
            if d == 3:
                print("\n=====================================")
                print("💨 WAILING WIND CURSE 💨")
                print("Howling winds shatter your will.")
                print("=====================================\n")
                faith -= 7
            elif d == 7:
                print("\n=====================================")
                print("🌫️ MEMORY FOG DAY 🌫️")
                print("Fog blurs your memories.")
                print("=====================================\n")
                faith -= 5
                evil += 3
            elif d == 9:
                print("\n=====================================")
                print("📜 WISDOM FESTIVAL 📜")
                print("Ancient knowledge awakens.")
                print("=====================================\n")
                have_list.append("ancient scroll")
            elif d == 12:
                print("\n=====================================")
                print("🍂 FALLEN LEAF CURSE 🍂")
                print("Cursed leaves cut your skin.")
                print("=====================================\n")
                hp -= 3
            elif d == 14:
                print("\n=====================================")
                print("💜 COURAGE FESTIVAL 💜")
                print("Brave hearts stand tall.")
                print("=====================================\n")
                good += 8
            elif d == 19:
                print("\n=====================================")
                print("⚔️ OLD GRUDGE AWAKEN DAY ⚔️")
                print("Ancient grudges rise from the grave.")
                print("=====================================\n")
                evil += 8
            elif d == 22:
                print("\n=====================================")
                print("🍁 AUTUMN BALANCE FESTIVAL 🍁")
                print("Seasons balance.")
                print("=====================================\n")
                good += 7
                evil -= 7
            elif d == 27:
                print("\n=====================================")
                print("🛡️ PROTECT FESTIVAL 🛡️")
                print("Guardians watch.")
                print("=====================================\n")
                amulet = True
            elif d == 28:
                print("\n=====================================")
                print("🌆 TWILIGHT CHAOS DAY 🌆")
                print("Day and night fall into chaos.")
                print("=====================================\n")
                time_period = "night"
            elif d == 30:
                print("\n=====================================")
                print("🌙 ECHO FESTIVAL 🌙")
                print("Memories return.")
                print("=====================================\n")
                faith += 8

        elif m == 10:
            if d == 1:
                print("\n=====================================")
                print("🍁 RED LEAF FESTIVAL 🍁")
                print("Cave blazes warm.")
                print("=====================================\n")
                hp += 5
            elif d == 6:
                print("\n=====================================")
                print("🧟 DEAD WALK DAY 🧟")
                print("The dead walk the earth tonight.")
                print("=====================================\n")
                trap_protect = False
                evil += 5
            elif d == 11:
                print("\n=====================================")
                print("🌑 DARKNESS EROSION CURSE 🌑")
                print("Darkness eats through your light.")
                print("=====================================\n")
                hp -= 4
                light = False
            elif d == 15:
                print("\n=====================================")
                print("👻 GATHER FESTIVAL 👻")
                print("Ghosts assemble.")
                print("=====================================\n")
                have_list.append("shadow dance")
            elif d == 18:
                print("\n=====================================")
                print("☠️ CURSE STRENGTHEN DAY ☠️")
                print("The ancient curse grows stronger.")
                print("=====================================\n")
                evil += 7
                hp -= 2
            elif d == 20:
                print("\n=====================================")
                print("💀 BONE FESTIVAL 💀")
                print("Old memories awaken.")
                print("=====================================\n")
                diary_read = True
                old_note_readed = True
                old_diary_readed = True
            elif d == 25:
                print("\n=====================================")
                print("🕯️ LAMP FESTIVAL 🕯️")
                print("Light guides lost souls.")
                print("=====================================\n")
                light = True
            elif d == 27:
                print("\n=====================================")
                print("👻 GHOST RAID DAY 👻")
                print("Ghosts launch a sudden attack.")
                print("=====================================\n")
                hp -= 4
            elif d == 29:
                print("\n=====================================")
                print("⛪ FALSE SALVATION DAY ⛪")
                print("Fake hope twists your kindness.")
                print("=====================================\n")
                good -= 8
            elif d == 31:
                print("\n=====================================")
                print("🎃 ALLHALLOWS FESTIVAL 🎃")
                print("Ghosts play, treats fall.")
                print("=====================================\n")
                hp += 3
                good += 5
                evil -= 3

        elif m == 11:
            if d == 1:
                print("\n=====================================")
                print("👧 INNOCENCE FESTIVAL 👧")
                print("Pure hearts return.")
                print("=====================================\n")
                good += 10
            elif d == 2:
                print("\n=====================================")
                print("👻 LEGEND FESTIVAL 👻")
                print("Ancient tales live.")
                print("=====================================\n")
                faith += 10
            elif d == 5:
                print("\n=====================================")
                print("🌫️ THICK FOG LOST DAY 🌫️")
                print("Thick fog makes you lose your way.")
                print("=====================================\n")
                map_unlocked = False
            elif d == 9:
                print("\n=====================================")
                print("🥶 BITTER COLD DAY 🥶")
                print("Bitter cold freezes your bones.")
                print("=====================================\n")
                hp -= 4
            elif d == 11:
                print("\n=====================================")
                print("⚔️ VALOR FESTIVAL ⚔️")
                print("Fears fade away.")
                print("=====================================\n")
                hp += 7
            elif d == 15:
                print("\n=====================================")
                print("🤫 SILENCE CURSE DAY 🤫")
                print("No spirit will speak to you today.")
                print("=====================================\n")
                faith -= 6
            elif d == 20:
                print("\n=====================================")
                print("🌫️ VEIL FESTIVAL 🌫️")
                print("Masks hide truths.")
                print("=====================================\n")
                have_list.append("misty veil")
            elif d == 22:
                print("\n=====================================")
                print("⚙️ FROZEN GEAR DAY ⚙️")
                print("All your tools freeze and fail.")
                print("=====================================\n")
                trap_protect = False
            elif d == 26:
                print("\n=====================================")
                print("👻 HOMELESS GHOST DAY 👻")
                print("Wandering ghosts cling to you.")
                print("=====================================\n")
                evil += 7
            elif d == 28:
                print("\n=====================================")
                print("⭐ FAINT STAR DAY ⭐")
                print("Stars fade, you lose your guidance.")
                print("=====================================\n")
                faith -= 8
            elif d == 30:
                print("\n=====================================")
                print("🕊️ PEACE FESTIVAL 🕊️")
                print("Ghosts rest forever.")
                print("=====================================\n")
                good += 8

        elif m == 12:
            if d == 3:
                print("\n=====================================")
                print("🌑 POLAR NIGHT CURSE 🌑")
                print("Endless night falls over the valley.")
                print("=====================================\n")
                time_period = "night"
                evil += 4
            elif d == 5:
                print("\n=====================================")
                print("❄️ FROST FESTIVAL ❄️")
                print("Calm quiet wraps cave.")
                print("=====================================\n")
                hp += 4
            elif d == 8:
                print("\n=====================================")
                print("🥶 FROSTBITE WEATHER DAY 🥶")
                print("Freezing weather weakens you.")
                print("=====================================\n")
                hp -= 3
            elif d == 14:
                print("\n=====================================")
                print("😔 DESPAIR EVE 😔")
                print("The weight of the cycle crushes hope.")
                print("=====================================\n")
                good -= 7
                evil += 5
            elif d == 15:
                print("\n=====================================")
                print("🌟 HOPESTAR FESTIVAL 🌟")
                print("Hope never fades.")
                print("=====================================\n")
                faith += 10
            elif d == 19:
                print("\n=====================================")
                print("🧊 FROZEN AMULET DAY 🧊")
                print("Ice freezes your amulet powerless.")
                print("=====================================\n")
                amulet = False
            elif d == 22:
                print("\n=====================================")
                print("❄️ SHORTEST DAY FESTIVAL ❄️")
                print("Light returns.")
                print("=====================================\n")
                hp += 6
            elif d == 25:
                print("\n=====================================")
                print("🎄 WARMTH FESTIVAL 🎄")
                print("Ghosts feel cozy.")
                print("=====================================\n")
                hp += 5
                have_list.append("christmas candy")
            elif d == 27:
                print("\n=====================================")
                print("👻 WINTER WRAITH DAY 👻")
                print("Frost wraiths strike from the cold.")
                print("=====================================\n")
                hp -= 4
            elif d == 29:
                print("\n=====================================")
                print("🔁 CYCLE CLOSE DAY 🔁")
                print("The loop tightens around you.")
                print("=====================================\n")
                hp -= 3
                evil += 4
            elif d == 31:
                print("\n=====================================")
                print("✨ FAREWELL FESTIVAL ✨")
                print("Old ends, new begins.")
                print("=====================================\n")
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
    if play_count == 1 and cleared_ending == True:
        play_count = 2
    if play_count == 4:
        print('A voice booms: Mortol, you final break the cycle, you pass my exam, so I will let you go to the heaven and meet me.\n')
        print('Game developer: PLayer, you have already done the main game, you can quit now or go to the last part.')
    if game_back == False:
        if not args.godmode:
            print('=== Death Adventure v1.4 - Official Release ===')
            print('Welcome to death adventure! You are a poor adventure, dream of rich and treasure. I will be your eyes and hands. You can say west or east north and south to control.')
            print('Your family always have somebody disappears. Your father said that he will go on a holiday, but he never came back.\n')
            character_creation()
            good += 5
        else:
            print('=== Death Adventure v1.4 - Official Release ===')
            print('Welcome to death adventure! You are a god who go to the mortol world. I will be your eyes and hands. You can say west or east north and south to control.')
            print('You go to mortol world beacause you see a family which have a curse. But unfortunately, you become a part of the curse too!')
            print('Then, you become a mortol who has the power as a god.')
            print('You should still have to choose a character.')
            print('Your will still die, however.\n')
            character_creation()
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
            good = 100
            grave_diary_read = True
            have_list.append('rope')
            have_list.append('ghost sword')
            have_list.append('gold coins')
            have_list.append('a pick-axe')
            have_list.append('super amulet')
            have_list.append('holy amulet')
            amulet = True
            map_unlocked = True
            print("God mode activated\n")
            menu()
        if args.cheat:
            have_list.extend(["a lamp", "a key", "a pick-axe", "super amulet", "ghost sword", "gold coins"])
            hp = 999
            map_unlocked = True
            secret_unlocked = True
            rune1 = rune2 = rune3 = True
            trap_protect = True
            torch = True
            print("Cheat mode enabled\n")
            menu()
        menu()
    elif game_back == True:
        if cleared_ending == True:
            permanent_points += 1
            if play_count == 2:
                if args.godmode:
                    pass
                else:
                    have_list = []
                light = False
                hp += 25
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
                sanity = 100
                print('')
                print('Welcome back to the death adventure!')
                print('The cave remembers you!')
                print('')
                print('A voice booms:')
                print('Descendent, you done a well job.')
                print('Our curfse will be broken by you.')
                print('Please hurry! Before out ghosts disappears.')
                print('Go to the campsite, then go to the tomb to find me.')
                print('')
                print('So, you will go to the menu.')
                print('')
                game_over = False
                cleared_ending = False
                menu()
            elif play_count == 3:
                print('Welcome to the last least not last part of death adventure.')
                print('You will never go to the cave again, instead, your great-great grandfather tell you to go somewhere.')
                print('So, you will go to the menu.')
                game_over = False
                cleared_ending = False
                menu()
            menu()
        else:
            print('So, you died, and you will go back to the menu to choose if you want to challenge again.')
            print('And you have to come to the first turn of the cycle.')
            print('Because of the curse, you rebirth again.')
            mac_demon_whisper("You died.")
            player_total_score = 0
            no_death_run = False
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
            sanity = 100
            if args.godmode:
                pass
            else:
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
            sanity = 100

            # Morality System
            good = 0
            evil = 0
            death_count += 1
            if death_count == 3:
                print("\n[Whisper] You've died five times already.")
                print("[Whisper] Maybe try the dev room next time?\n")
            if death_count == 5:
                print("\n[Ghost Laugh] Five death! You're our favorite visitor!\n")
                print('Hp +5 in case of you die again.')
                hp += 5
            if death_count >= 8 and death_count < 10:
                 print("\n[Ghosts Sing] You are part of us now!")
                 print('Hp +10 and you can trap protect in case you finally become part of ghost.')
                 hp += 10
                 trap_protect = True
            if death_count >= 10:
                print('You finally become a ghost, and can not be birth forever.')
                print('')
                end_score_rating()
                print('Goodbye!')
                print("=== Death Adventure v1.4 - Official Release ===")
                print("Thank you for playing!")
                exit()
            print('You can choose a character again.')
            character_creation()
            menu()
    if force_over == True:
        return
if __name__ == '__main__':
    main()  