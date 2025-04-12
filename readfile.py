import subprocess

# Biên dịch file C++ (readfile.cpp) với g++
compile_process = subprocess.run(['g++', 'readfile.cpp', '-o', 'readfile'], capture_output=True, text=True)

# Kiểm tra nếu biên dịch thành công
if compile_process.returncode == 0:
    print("Ex: /home/-USER_NAME-/Desktop/example.txt")
    print("Please enter path of the file: ")
    
    # Run the progam has compiler
    run_process = subprocess.run(['./readfile'], capture_output=True, text=True)
    
    if run_process.returncode == 0:
        print(run_process.stdout)
    else:
        print(run_process.stderr)
else:
    print("Compiler error", compile_process.stderr)

