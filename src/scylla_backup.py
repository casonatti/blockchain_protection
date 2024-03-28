from bcc import BPF
from ctypes import *
import time
import csv
import subprocess

# Get info from eBPF program and generate logs
def print_event(cpu, data, size):
  data = b["output"].event(data)
  print(f"{data.thread_pid} {data.thread_gpid} {data.uid} {data.hooked_inode} {data.message} {data.counter}")
  # with open(result_file, 'a') as csvfile:
  #   csv_append = csv.writer(csvfile)
  #   csv_append.writerow([data.counter, data.timestamp])
  #   csvfile.close()

# Get timestamp epoch at the boot time (bcc only offers timestamp counting since boot)
current_epoch_ts = time.time_ns()
boot_relative_ts = time.monotonic_ns()
boot_epoch_ts = current_epoch_ts - boot_relative_ts

# Evaluation purpose
# test_type_file = open('../evaluation/config/test_type.txt','r')
# test_type = test_type_file.read()
# result_file = "../evaluation/results/" + test_type + "/ebpf_" + test_type + ".csv"

# Get clef GPID
try:
  clef_gpid_search = subprocess.run(["ps", "-e", "-o", "pid,comm"], stdout=subprocess.PIPE, text=True, check=True) # Run the ps command to get information about processes with the specified command name
  lines = clef_gpid_search.stdout.strip().split('\n')
  clef_gpid = [int(line.split()[0]) for line in lines[1:] if line.split()[-1] == 'clef'] # Split the output into lines and extract the PIDs for the specified program name
  with open('../evaluation/config/permitted_pids.txt', 'w') as file:
    file.write(str(clef_gpid[0]))
except subprocess.CalledProcessError:
  print(f"Error retrieving PIDs for 'clef'.")
  exit()

# Load eBPF program into de kernel and attach eBPF function to vfs_read syscall
program = "readMonitor.c"
b = BPF(src_file = program)
b.attach_kprobe(event = "vfs_read", fn_name = "protected_file")
#b.attach_kprobe(event = "vfs_write", fn_name= "protected_file")

# user/kernel -space map association
i_map = b["protected_inodes_map"]
ts_map = b["epoch_ts_map"]
permitted_processes_map = b["permitted_processes_map"]

# Populating maps
ts_map[c_int(0)] = c_uint64(boot_epoch_ts)

permitted_pids_file = open("../evaluation/config/permitted_pids.txt", "r")
line = permitted_pids_file.readline()
while line:
  print("Copying " + line[:-1] + " to eBPF map [permitted_processes_map]")
  permitted_processes_map[c_uint64(int(line))] = c_uint64(int(line))
  line = permitted_pids_file.readline()

inode_list_file = open("../evaluation/config/protected_inodes.txt", "r")
line = inode_list_file.readline()
while line:
  print("Copying " + line[:-1] + " to eBPF map [inode_map]")
  i_map[c_uint32(int(line))] = c_uint32(int(line))
  line = inode_list_file.readline()

# Print data header in the terminal
print("%-6s %-6s %-6s %-8s %-10s %-6s" % ("PID", "GPID", "UID", "INODE", "MESSAGE", "COUNTER(UID)"))

# Link user and kernel spaces for gathering info
b["output"].open_perf_buffer(print_event)

# Evaluation purpose
# with open(result_file, 'w') as csvfile:
#   csv_append = csv.writer(csvfile)
#   csv_append.writerow(['Iteration','TS_eBPF'])
#   csvfile.close()

# Keep on checking for new data
while True:
  try:
    b.perf_buffer_poll()
  except KeyboardInterrupt:
    exit(0)