#linux version
import subprocess
import time
import sys
from pynput import keyboard


#place your word here

WORDS = "word here"
running = False

def spam_fk():
    global running
    print("📋 Copying  text to clipboard...")
    subprocess.run(["wl-copy"], input=WORDS, text=True)
    print("✅ Text ready")
    print("Starting in 3 seconds... Click into Vesktop!")
    time.sleep(3)
    
    count = 0
    while running:
        subprocess.run(["xdotool", "key", "ctrl+v"])
        time.sleep(0.1)
        subprocess.run(["xdotool", "key", "Return"])
        count += 1
        print(f"💥 Sent massive FK block #{count}")

        #adjust this if the bot check got you
        time.sleep(2)

def on_press(key):
    global running
    try:
        if key == keyboard.Key.f9:
            if not running:
                running = True
                print("\n🚀 STARTED!")
                spam_fk()
        elif key == keyboard.Key.f10:
            running = False
            print("\n🛑 STOPPED")
        elif key == keyboard.Key.f11:
            print("\n👋 EXITING")
            sys.exit(0)
    except:
        pass

print("=" * 50)
print("💀DISCORD WORD SPAMMER💀")
print("=" * 50)
print("F9 - START")
print("F10 - STOP")
print("F11 - EXIT")
print("=" * 50)

listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
