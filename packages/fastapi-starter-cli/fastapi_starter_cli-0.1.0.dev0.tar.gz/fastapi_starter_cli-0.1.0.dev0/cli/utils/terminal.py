import os
import signal
import sys
import time
import shutil

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def signal_handler(sig, frame):
    print('\nSaliendo...')
    sys.exit(0)

def monitor_terminal_size(banner_callback):
    signal.signal(signal.SIGINT, signal_handler)
    last_size = shutil.get_terminal_size()
    
    try:
        while True:
            current_size = shutil.get_terminal_size()
            if current_size != last_size:
                banner_callback()
                last_size = current_size
            time.sleep(0.1)
    except KeyboardInterrupt:
        sys.exit(0)