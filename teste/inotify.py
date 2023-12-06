import os
import pyinotify
import time
import csv

result_file = "./resultados/resultado_inotify.csv"

class AccessCounter:
    def __init__(self):
        self.access_count = 0

    def increment_count(self):
        self.access_count += 1

def monitor_file_access(file_path, access_counter):
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_OPEN

    class EventHandler(pyinotify.ProcessEvent):
        def process_default(self, event):
            if event.pathname == file_path:
                access_time = time.time()
                access_counter.increment_count()
                with open(result_file, 'a') as csv_obj:
                    csv_append = csv.writer(csv_obj)
                    csv_append.writerow([access_counter.access_count, f"{access_time:.19}"])
                    csv_obj.close()
                #print(f"{access_time:.13f} {access_counter.access_count}")
                #print(f"File {file_path} accessed at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(access_time))}")

    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)

    wdd = wm.add_watch(os.path.dirname(file_path), mask)

    try:
        print(f"Monitoring access to file: {file_path}")
        notifier.loop()
    except KeyboardInterrupt:
        print("Monitoring stopped.")


if __name__ == "__main__":
    file_to_monitor = "/home/jeison/ic/repositorios/solucao_ic/teste/wallet.txt"
    access_counter = AccessCounter()
    with open(result_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Iteration', 'TimeElapsed(seconds)'])
        csvfile.close()
    monitor_file_access(file_to_monitor,access_counter)

