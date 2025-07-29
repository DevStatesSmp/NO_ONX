import time
from src.config.CONFIG import FEATURE
from .getError import *

try:
    def loading_effect(text="Loading modules", delay=0.175, duration=3):
        """
        Displays a loading effect in the terminal.
        Args:
            text (str): The text to display while loading.
            delay (float): Delay between each loading symbol.
            duration (int): Duration for the loading effect in seconds.
        """
        if FEATURE.get("DISABLE_LOADING", False):
            return     
        spinner = ['◜', '◝', '◞', '◟', '◡', '◠', '◜', '◝', '◞']

        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                for symbol in spinner:
                    print(f"\r\033[93m{text} {symbol}\033[0m", end='', flush=True)
                    time.sleep(delay)
                    if time.time() - start_time >= duration:
                        break

            print('\r' + ' ' * (len(text) + 3) + '\r', end='', flush=True)

        except KeyboardInterrupt:
            handle_error("Error when loading", "Loading interrupted, exiting...")
            exit(1)

except Exception as e:
    handle_error(ErrorContent.LOADING, {str(e)})