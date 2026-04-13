# Android/Termux version

import time
import sys
import subprocess
import os
import tty
import termios
import contextlib

# place your word here
WORDS = "word here"

running = False

@contextlib.contextmanager
def raw_mode(file):
    """Enable raw mode for keyboard input (no Enter key needed)"""
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

def set_clipboard():
    """Set clipboard content using termux-clipboard-set"""
    try:
        subprocess.run(['termux-clipboard-set', WORDS], 
                      capture_output=True, text=True, check=False)
        return True
    except Exception as e:
        print(f"Clipboard error: {e}")
        return False

def paste_text():
    """Paste using input keyevent (KEYCODE_PASTE = 279)"""
    try:
        subprocess.run(['input', 'keyevent', '279'], capture_output=True, check=False)
        return True
    except:
        return False

def send_enter():
    """Send enter key (KEYCODE_ENTER = 66)"""
    try:
        subprocess.run(['input', 'keyevent', '66'], capture_output=True, check=False)
        return True
    except:
        return False

def spam_fk():
    global running
    print("\n📋 Copying  text to clipboard...")
    if set_clipboard():
        print("✅ Text ready")
    else:
        print("❌ Failed to set clipboard")
        return
    
    print("Starting in 3 seconds... Tap into Discord")
    time.sleep(3)
    
    count = 0
    while running:
        paste_text()
        time.sleep(0.1)
        send_enter()
        count += 1
        print(f"💥 Sent massive FK block #{count}")
        time.sleep(2)
    
    print("\n🛑 Spamming stopped")

def check_requirements():
    """Check if required Termux packages are installed"""
    print("Checking requirements...")
    
    # Check for termux-clipboard-set
    result = subprocess.run(['which', 'termux-clipboard-set'], capture_output=True, check=False)
    if result.returncode != 0:
        print("❌ termux-clipboard-set not found!")
        print("Install with: pkg install termux-api")
        return False
    
    # Check for input command
    result = subprocess.run(['which', 'input'], capture_output=True, check=False)
    if result.returncode != 0:
        print("❌ 'input' command not found!")
        print("This requires root or Termux running with proper permissions")
        return False
    
    print("✅ Requirements met!")
    return True

def get_key():
    """Read a single keypress without Enter key"""
    with raw_mode(sys.stdin):
        ch = sys.stdin.read(1)
        if ord(ch) == 3:  # Ctrl+C
            raise KeyboardInterrupt
        return ch

def main():
    global running
    
    print("=" * 50)
    print("💀DISCORD WORD SPAMMER (Android/Termux)💀")
    print("=" * 50)
    
    # Check requirements first
    if not check_requirements():
        print("\n⚠️  Missing requirements. Please install:")
        print("  pkg install termux-api")
        print("\nNote: 'input' command requires root or Termux with proper permissions.")
        print("If 'input' is not available, use the alternative method below.\n")
        
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            sys.exit(1)
    
    print("\nCONTROL KEYS:")
    print("  Press 's' - START SPAMMING")
    print("  Press 't' - STOP SPAMMING")
    print("  Press 'q' - EXIT")
    print("=" * 50)
    print("\nReady and waiting for commands...\n")
    
    try:
        while True:
            key = get_key()
            
            if key == 's':
                if not running:
                    running = True
                    print("\n🚀 STARTED!")
                    spam_fk()
                else:
                    print("\n⚠️  Already running! Press 't' to stop first.")
            
            elif key == 't':
                if running:
                    running = False
                    print("\n🛑 STOPPED")
                else:
                    print("\n⚠️  Not running. Press 's' to start.")
            
            elif key == 'q':
                if running:
                    running = False
                    time.sleep(0.5)
                print("\n👋 EXITING")
                sys.exit(0)
            
            elif key == 'h':
                print("\nCommands: s=start, t=stop, q=quit")
            
            # Ignore other keys
                
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()