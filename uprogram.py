from bcc import BPF
from ctypes import *
import time
import csv

def print_event(cpu, data, size):
  data = b["output"].event(data)
  print(f"{data.pid} {data.ppid} {data.uid} {data.hooked_inode} {data.message} {data.counter}")
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

program = "kprogram.c"

b = BPF(src_file = program)

b.attach_kprobe(event = "vfs_read", fn_name = "protected_file")
#b.attach_kprobe(event = "vfs_write", fn_name= "protected_file")

#user/kernel space map association
i_map = b["inode_map"]
ts_map = b["epoch_ts_map"]
permitted_processes = b["permitted_processes_map"]

#populating maps
ts_map[c_int(0)] = c_uint64(boot_epoch_ts)

inode_list_file = open("./tests/protected_inodes.txt", "r")
line = inode_list_file.readline()
while line:
  print("Copying " + str(int(line)) + " to eBPF map [inode_map]")
  i_map[c_uint32(int(line))] = c_uint32(int(line))
  line = inode_list_file.readline()

permitted_processes_file = open("./tests/permitted_pids.txt", "r")
line = permitted_processes_file.readline()
while line:
  print("Copying " + str(int(line)) + " to eBPF map [permitted_processes_map]")
  permitted_processes[c_uint64(int(line))] = c_uint64(int(line))
  line = permitted_processes_file.readline()


print("%-6s %-6s %-6s %-8s %-10s %-6s" % ("PID", "PPID", "UID", "INODE", "MESSAGE", "COUNTER"))
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