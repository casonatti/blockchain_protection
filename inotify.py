import os
import pyinotify
import time
import csv

test_type_file = open('./tests/test_type.txt','r')
test_type = test_type_file.read()
result_file = "./tests/" + test_type + "/inotify_" + test_type + ".csv"

class AccessCounter:
    def __init__(self):
        self.access_count = 0

    def increment_count(self):
        self.access_count += 1

def monitor_file_access(file_path, access_counter):
    paths_to_monitor = []

    with open("./tests/inode_paths.txt", "r") as file:
        paths_to_monitor = [line.strip() for line in file.readlines()]

    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_OPEN

    class EventHandler(pyinotify.ProcessEvent):
        def process_default(self, event):
            if event.mask & pyinotify.IN_OPEN:
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

    for path in paths_to_monitor:
        wdd = wm.add_watch(path, mask, rec=False)
    #wdd = wm.add_watch(os.path.dirname(file_path), mask)

    try:
        print(f"iNotify is monitoring!")
        notifier.loop()
    except KeyboardInterrupt:
        print("Monitoring stopped.")


if __name__ == "__main__":
    file_to_monitor = "/home/lab212/ic/repositories/blockchain_protection/tests/teste.txt"
    access_counter = AccessCounter()
    with open(result_file, 'w') as csvfile:
        csv_append = csv.writer(csvfile)
        csv_append.writerow(['Iteration','TS_Inotify'])
        csvfile.close()
    monitor_file_access(file_to_monitor,access_counter)

