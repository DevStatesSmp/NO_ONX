import time

def loading_effect(text="Loading modules", delay=0.3):
    spinner = ['/', '|', '\\', '-'] 
    for _ in range(10):
        for symbol in spinner:
            print(f"\r\033[93m{text} {symbol}\033[0m", end='', flush=True)
            time.sleep(delay)
    print()