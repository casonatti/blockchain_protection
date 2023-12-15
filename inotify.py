import os
import pyinotify
import time
import csv

test_number_file = open('./test_number.txt','r')
test_number = test_number_file.read()
result_file = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/inotify_" + test_number + ".csv"

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
                access_time = time.time_ns()
                access_counter.increment_count()
                with open(result_file, 'a') as csv_obj:
                    csv_append = csv.writer(csv_obj)
                    csv_append.writerow([access_counter.access_count, access_time])
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
    with open(result_file, 'w') as csvfile:
        csv_append = csv.writer(csvfile)
        csv_append.writerow(['Iteration','TS_Inotify'])
        csvfile.close()
    monitor_file_access(file_to_monitor,access_counter)

