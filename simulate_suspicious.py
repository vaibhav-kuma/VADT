import time
import subprocess
import sys

def simulate_high_cpu():
    print("[*] Simulating high CPU usage...")
    while True:
        pass  # Infinite loop to spike CPU

def simulate_cmd_keyword():
    print("[*] Launching fake process with suspicious command-line args...")
    subprocess.Popen(["python", "-c", "import time; time.sleep(60)", "--inject", "--steal"])

def simulate_high_memory():
    print("[*] Simulating high memory usage...")
    memory_hog = []
    try:
        while True:
            memory_hog.append(' ' * 10**6)  # Allocate memory in chunks
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("[*] Memory test stopped.")

def simulate_unsigned_binary():
    print("[*] Simulating unsigned executable (mock)...")
    subprocess.Popen(["python", "-c", "import time; time.sleep(60)", "fake_unsigned_exe.exe"])

if __name__ == "__main__":
    choice = input("""Choose simulation type:
1. High CPU
2. Suspicious Command-Line
3. High Memory Usage
4. Unsigned Executable (Mock)
> """)

    if choice == "1":
        simulate_high_cpu()
    elif choice == "2":
        simulate_cmd_keyword()
    elif choice == "3":
        simulate_high_memory()
    elif choice == "4":
        simulate_unsigned_binary()
    else:
        print("Invalid option.")
