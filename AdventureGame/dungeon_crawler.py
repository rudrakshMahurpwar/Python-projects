import json
import random
from typing import Callable, Dict, List

WEAPONS = ("sword", "staff")
CHOICES = {
    "directions": ("Upstairs", "Dungeon"),
    "actions": ("Fight", "Talk", "Run"),
    "dragon": ("Attack Dragon", "Sneak Past Dragon"),
}

Riddle = Dict[str, str]
Action = Callable[[], bool]


# -------------------------
# UTILITY FUNCTIONS
# -------------------------


def normalize(text: str) -> str:
    return text.strip().lower()


def luck() -> bool:
    return random.choice((True, False))


# -------------------------
# RIDDLE SYSTEM
# -------------------------


def load_riddles(difficulty: str) -> List[Riddle]:
    """Load riddles from a JSON file based on difficulty."""
    try:
        with open("riddles.json", "r") as file:
            data = json.load(file)

        for group in data:
            if normalize(group["difficulty"]) == normalize(difficulty):
                for riddle in group["riddles"]:
                    riddle["answer"] = normalize(riddle["answer"])
                return group["riddles"]

    except FileNotFoundError:
        print("Riddles file not found. Using default.")

    # Default riddle if file missing
    return [
        {
            "riddle": "I speak without a mouth and hear without ears. What am I?",
            "answer": "echo",
        }
    ]


def ask_riddle(riddles: List[Riddle]) -> bool:
    riddle = random.choice(riddles)
    print(riddle["riddle"])
    return normalize(input("> ")) == riddle["answer"]


# -------------------------
# INPUT SYSTEM
# -------------------------


def prompt_choice(options: tuple[str, ...]) -> str:
    """Prompt the user to select from a list of options."""
    normalized = [opt.lower() for opt in options]
    letter_map = {chr(97 + i): opt for i, opt in enumerate(normalized)}

    while True:
        print("\nChoose one:")
        for key, value in letter_map.items():
            print(f"({key}) {value.title()}")

        user_input = normalize(input("> "))

        if user_input in letter_map:
            return letter_map[user_input]
        if user_input in normalized:
            return user_input

        print("Invalid choice. Try again.")


# -------------------------
# COMBAT SYSTEM
# -------------------------


def weapon_actions(weapon: str, sword: Action, staff: Action) -> bool:
    """Perform the action corresponding to the weapon."""
    actions = {"sword": sword, "staff": staff}
    action = actions.get(weapon)
    if not action:
        print("Invalid weapon.")
        return False
    return action()


def weapon_check(weapon: str, sword: Action, staff: Action, fail_message: str) -> bool:
    """Check weapon action, fallback to defeat message."""
    return weapon_actions(weapon, sword, staff) or defeat(fail_message)


# -------------------------
# SCENES
# -------------------------


def upstairs_scene(weapon: str, riddles: List[Riddle]) -> bool:
    print("You meet a Dark Knight blocking the hallway.")
    choice = prompt_choice(CHOICES["actions"])

    if choice == "fight":
        return weapon_check(
            weapon,
            sword=lambda: victory("You defeat the Knight."),
            staff=lambda: False,
            fail_message="Magic fails against armor.",
        )

    if choice == "talk":
        print("Answer the riddle to pass.")
        return ask_riddle(riddles) or defeat("He attacks you.")

    return defeat("You trip and fall.")


def dungeon_scene(weapon: str, riddles: List[Riddle]) -> bool:
    print("It's dark and cold.")
    choice = prompt_choice(CHOICES["dragon"])
    attack = choice == "attack dragon"

    success = weapon_actions(
        weapon,
        sword=luck,
        staff=lambda: ask_riddle(riddles) if attack else ask_riddle(riddles) or luck(),
    )

    if not success:
        return defeat("You failed to escape.")

    return dungeon_escape(weapon, riddles)


def dungeon_escape(weapon: str, riddles: List[Riddle]) -> bool:
    return weapon_actions(
        weapon,
        sword=lambda: victory("You break the lock and find treasure."),
        staff=lambda: ask_riddle(riddles),
    )


# -------------------------
# RESULT HELPERS
# -------------------------


def victory(message: str) -> bool:
    print(message)
    return True


def defeat(message: str) -> bool:
    print(message)
    return False


# -------------------------
# GAME LOOP
# -------------------------


def main() -> bool:
    difficulty = prompt_choice(("Easy", "Medium", "Hard"))
    riddles = load_riddles(difficulty)

    print("\nYou stand before a dark fortress.")
    weapon = prompt_choice(WEAPONS)
    direction = prompt_choice(CHOICES["directions"])

    scenes = {"upstairs": upstairs_scene, "dungeon": dungeon_scene}
    return scenes[direction](weapon, riddles)


if __name__ == "__main__":
    name = input("Enter your name: ")
    print(f"Hello {name}.")

    while True:
        play = normalize(input("Do you want to play? (y/n) "))
        if play in ("y", "yes"):
            print("\nSelect difficulty:")
            result = main()
            print("\nYou won!" if result else "\nYou lost!")
        else:
            print("Goodbye.")
            break
