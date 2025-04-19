import subprocess
import os
import sys
import logging
from time import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_detective(file_to_scan):
    try:
        # Run the file_scan subprocess on the given file
        logging.info(f"Scanning file: {file_to_scan}")

        process = subprocess.Popen(
            ['./file_scan', file_to_scan],  # Scan the specific file
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Set a timeout limit for process execution (e.g., 60 seconds)
        timeout_seconds = 60
        start_time = time()

        while True:
            # If the process finishes, break the loop
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break

            # Handle process timeout
            if time() - start_time > timeout_seconds:
                logging.warning("Process timeout reached. Terminating...")
                process.kill()
                break

            if output:
                print(output.strip())  # Print each line of output

        # Capture any errors from the stderr
        stderr_output = process.stderr.read()
        if stderr_output:
            logging.error(f"Error: {stderr_output.strip()}")

    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess execution failed with error: {e}")
    except ValueError as ve:
        logging.error(ve)
    except KeyboardInterrupt:
        logging.info("\nProgram interrupted. Exiting...")
        process.kill()  # Ensure the process is killed when interrupted
    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")
    finally:
        process.stdout.close()
        process.stderr.close()

def scan_all_files_in_directory(directory_path):
    """ Scan all files in a directory (including subdirectories). """
    if not os.path.isdir(directory_path):
        logging.error(f"The directory '{directory_path}' is invalid.")
        return

    logging.info(f"Scanning all files in directory: {directory_path} (Enter to continued)")
    
    # Walk through the directory and find all files
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            logging.info(f"Queueing file: {file_path} for scanning.")
            run_detective(file_path)

def get_directory_input():
    directory_path = input("Enter directory path to scan: ").strip()
    if not directory_path:
        logging.error("No directory path provided.")
        sys.exit(1)
    return directory_path

def get_file_input():
    file_path = input("Enter the file path to scan: ").strip()
    if not os.path.isfile(file_path):
        logging.error(f"The file '{file_path}' does not exist.")
        return None
    return file_path

def main():
    while True:
        print("\nSelect an option:")
        print("A: Scan All Files in Directory")
        print("B: Scan One Specific File")
        print("E: Exit")

        option = input("Enter your choice (A/B/E): ").strip().upper()

        if option == "E":
            print("Exiting program...")
            break
        elif option == "A":
            directory_path = get_directory_input()
            scan_all_files_in_directory(directory_path)  # Scan all files in the directory
        elif option == "B":
            file_to_scan = get_file_input()  # Get the specific file to scan
            if file_to_scan:
                run_detective(file_to_scan)  # Scan a specific file
        else:
            logging.error("Invalid option. Please select A, B, or E.")

if __name__ == "__main__":
    main()





