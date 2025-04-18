import subprocess

def run_detective():
    process = subprocess.Popen(
        ['./detective'],          
        stdout=subprocess.PIPE,   
        stderr=subprocess.PIPE,   
        text=True                 
    )

    
    try:
        for line in process.stdout:
            print(line, end='')  
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        process.kill()

if __name__ == "__main__":
    print("(Example: /home/-USER_NAME-/)")
    print("Enter directory path to watch: ")
    run_detective()


