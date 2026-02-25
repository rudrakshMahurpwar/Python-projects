import os

while True:
    dialogue = input("Enter your sentence ('q' to quit): ")

    if dialogue.lower() == "q":
        break

    # Escape single quotes for PowerShell
    safe_dialogue = dialogue.replace("'", "''")

    os.system(
        f'powershell -Command "Add-Type -AssemblyName System.Speech; '
        f"$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.Rate=1; "
        f"$s.Speak('{safe_dialogue}')\""
    )
