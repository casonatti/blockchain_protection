from bcc import BPF
from ctypes import *
import time
import csv
import subprocess

def print_event(cpu, data, size):
  data = b["output"].event(data)
  print(f"{data.pid} {data.gpid} {data.uid} {data.hooked_inode} {data.message} {data.counter} {data.teste}")
  with open(result_file, 'a') as csvfile:
    csv_append = csv.writer(csvfile)
    csv_append.writerow([data.counter, data.timestamp])
    csvfile.close()

current_epoch_ts = time.time_ns()
boot_relative_ts = time.monotonic_ns()
boot_epoch_ts = current_epoch_ts - boot_relative_ts

test_type_file = open('./tests/test_type.txt','r')
test_type = test_type_file.read()
result_file = "./tests/" + test_type + "/ebpf_" + test_type + ".csv"

#get clef GPID
try:
  clef_gpid_search = subprocess.run(["ps", "-e", "-o", "pid,comm"], stdout=subprocess.PIPE, text=True, check=True) # Run the ps command to get information about processes with the specified command name
  lines = clef_gpid_search.stdout.strip().split('\n')
  clef_gpid = [int(line.split()[0]) for line in lines[1:] if line.split()[-1] == 'clef'] # Split the output into lines and extract the PIDs for the specified program name
  with open('./tests/permitted_pids.txt', 'w') as file:
    file.write(str(clef_gpid[0]))
except subprocess.CalledProcessError:
  print(f"Error retrieving PIDs for 'clef'.")
  exit()

program = "kprogram.c"

b = BPF(src_file = program)

b.attach_kprobe(event = "vfs_read", fn_name = "protected_file")
#b.attach_kprobe(event = "vfs_write", fn_name= "protected_file")

#user/kernel space map association
i_map = b["inode_map"]
ts_map = b["epoch_ts_map"]
permitted_processes_map = b["permitted_processes_map"]

#populating maps
ts_map[c_int(0)] = c_uint64(boot_epoch_ts)

permitted_pids_file = open("./tests/permitted_pids.txt", "r")
line = permitted_pids_file.readline()
while line:
  print("Copying " + line[:-1] + " to eBPF map [permitted_processes_map]")
  permitted_processes_map[c_uint64(int(line))] = c_uint64(int(line))
  line = permitted_pids_file.readline()

inode_list_file = open("./tests/protected_inodes.txt", "r")
line = inode_list_file.readline()
while line:
  print("Copying " + line[:-1] + " to eBPF map [inode_map]")
  i_map[c_uint32(int(line))] = c_uint32(int(line))
  line = inode_list_file.readline()


print("%-6s %-6s %-6s %-8s %-10s %-6s" % ("PID", "GPID", "UID", "INODE", "MESSAGE", "COUNTER(UID)"))
#print("Program Initialized")

b["output"].open_perf_buffer(print_event)

with open(result_file, 'w') as csvfile:
    csv_append = csv.writer(csvfile)
    csv_append.writerow(['Iteration','TS_eBPF'])
    csvfile.close()

while True:
  try:
    b.perf_buffer_poll()
  except KeyboardInterrupt:
    exit(0)