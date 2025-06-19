import psutil
import time

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'exe', 'cmdline']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

if __name__ == "__main__":
    while True:
        for proc in get_running_processes():
            print(f"[+] {proc['name']} ({proc['pid']}) CPU: {proc['cpu_percent']}% MEM: {proc['memory_percent']}%")
        time.sleep(5)
