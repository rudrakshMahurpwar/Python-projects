import random


def strip_and_lower_string(string: str) -> str:
    return string.strip().lower()


def choice(options: tuple) -> str:
    print("Choose one:")
    for index, item in enumerate(options):
        print(f"({chr(97+index)}) {item}.")

    while True:
        user_input = strip_and_lower_string(input("> "))
        for index, option in enumerate(options):
            letter = chr(97 + index)
            if (
                user_input.startswith(letter)
                or user_input.startswith(f"({letter})")
                or user_input == option
            ):
                return strip_and_lower_string(option)
        print("Invalid Choice. Try again.")


def ask_riddle() -> bool:
    print(
        "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?"
    )
    answer = strip_and_lower_string(input("> "))
    return answer == "echo"


name: str = input("Enter Your Name: ")

print(f"Hello {name} welcome to the game.")

should_we_play: str = strip_and_lower_string(
    input("Do you want to play the game: (y/n) ")
)
print("Please select the difficulty for the game.")

if should_we_play == "y" or should_we_play == "yes":
    print("You wake up in front of a dark fortress.")
    print("There is a Sword and a Magic Staff on the ground.")
    weapon: str = choice(("Sword", "Staff"))
    print("Inside, you see two paths:")
    direction: str = choice(("Upstairs", "Dungeon"))

    match direction:
        case "upstairs":
            print("You meet a Dark Knight blocking the hallway.")
            print("A monster at a distance")
            dark_knight = choice(("Fight", "Talk", "Run"))

            match dark_knight:
                case "fight":
                    if weapon == "sword":
                        print(
                            "You defeat the Knight.\nHurray!! You found the treasure room."
                        )
                    elif weapon == "staff":
                        print("The Knight blocks Magic.")
                        print("You Lose.")
                case "talk":
                    print("Answer the riddle to pass the knight")
                    knight_riddle = ask_riddle()
                    (
                        print("He lets you pass\nYou won!!")
                        if knight_riddle
                        else print("He attacked you.\nYou lost")
                    )
                case "run":
                    print("You trip and fall from stairs.\nYou lose")
        case "dungeon":
            print("It's dark and cold.\nYou see:\n* A Locked Door\n* A sleeping Dragon")
            sneak: bool = random.choice([True, False])
            escaped: bool = False
            dungeon = choice(("Attack Dragon", "Sneak Past Dragon"))
            if dungeon == "attack dragon":
                match weapon:
                    case "sword":
                        print(
                            "You dashed toward the Dragon with your sword trying to stab him."
                        )
                        if sneak:
                            print("You successfully defeated the Dragon and escaped.")
                            escaped = True
                        else:
                            print(
                                "Unfortunately, Dragon is too powerful and it burns you."
                            )
                            print("You lose")

                    case "staff":
                        print(
                            "Answer the riddle to cast the correct spell with you staff"
                        )
                        dungeon_riddle = ask_riddle()

                        if dungeon_riddle:
                            print("Magic puts Dragon to sleep forever. You win!")
                            escaped = True
                        else:
                            print("Your spell failed. Dragon Burnt you.\n You lost")

            elif dungeon == "sneak past dragon":
                if weapon == "sword":
                    if sneak:
                        print("You escaped the Dragon. you won!")
                        escaped = True
                    else:
                        print(
                            "The Dragon is awake. He spits the flame on you. You lose"
                        )

                elif weapon == "staff":
                    print(
                        "Answer the riddle to cast the Muffliato Charm using your Magical staff"
                    )
                    dragon_riddle = ask_riddle()
                    if dragon_riddle:
                        print("Your spell worked. You escaped the Dragon, you won!")
                    else:
                        print(
                            "You failed to cast the correct spell. You can still sneak past the Dragon."
                        )
                        print("Shhh... Trying to sneak...")

                        if sneak:
                            print("You escaped the Dragon. you won!")
                            escaped = True
                        else:
                            print(
                                "The Dragon is awake. He spits the flame on you. You lose"
                            )

            if escaped:
                match weapon:
                    case "sword":
                        print("You break lock. You found the treasure.")
                    case "staff":
                        print(
                            "Answer the riddle to cast the Alohomora Charm using your Magical staff"
                        )
                        door_riddle = ask_riddle()
                        (
                            print(
                                "Your spell worked. You break lock and found the treasure."
                            )
                            if door_riddle
                            else print("Your spell failed.\nYou lose")
                        )

else:
    print("We are NOT playing....bye...!")
