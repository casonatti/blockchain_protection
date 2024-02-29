import csv
import psutil
import time

def monitor_cpu(interval):
    with open("./results/resource_usage/_sample_resource_usage.csv", 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Time','CPU_USAGE', 'MEMORY_USAGE'])

        i = 0.0
        while i != 150.5:
            # Get CPU percentage
            cpu_percent = psutil.cpu_percent(interval=interval)
            memory = psutil.virtual_memory()
            print(f"Time: {i} \t CPU Usage: {cpu_percent}% \t Memory Usage: {memory[2]}") #memory[2] is the percent usage
            csv_writer.writerow([i, cpu_percent, memory[2]])
            i = i + interval

if __name__ == "__main__":
    monitor_cpu(0.5)
