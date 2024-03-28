from bcc import BPF
from ctypes import *
from Log import *
import time
import threading

class Scylla():
  def __init__(self, log):
    self.log = log

    # Get timestamp epoch at the boot time (bcc only offers timestamp counting since boot)
    current_epoch_ts = time.time_ns()
    boot_relative_ts = time.monotonic_ns()
    boot_epoch_ts = current_epoch_ts - boot_relative_ts

    # Load eBPF program into de kernel and attach eBPF function to vfs_read syscall
    program = "readMonitor.c"
    self.b = BPF(src_file = program)
    self.b.attach_kprobe(event = "vfs_read", fn_name = "protected_file")
    #b.attach_kprobe(event = "vfs_write", fn_name= "protected_file")

    # user/kernel -space map association
    i_map = self.b["protected_inodes_map"]
    ts_map = self.b["epoch_ts_map"]
    permitted_processes_map = self.b["permitted_processes_map"]

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
      temp = line.split()
      print("Copying " + line[:-1] + " to eBPF map [inode_map]")
      i_map[c_uint32(int(temp[0]))] = c_uint32(int(temp[0]))
      line = inode_list_file.readline()

    # Link user and kernel spaces for gathering info
    self.b["output"].open_perf_buffer(self.log_event)

  # Get info from eBPF program and generate logs
  def log_event(self, cpu, data, size):
    data = self.b["output"].event(data)
    # print(f"{data.thread_pid} {data.thread_gpid} {data.uid} {data.hooked_inode} {data.message} {data.counter}")
    self.log.append(f"{data.thread_pid} {data.thread_gpid} {data.uid} {data.hooked_inode} {data.message} {data.counter}")
    # with open(result_file, 'a') as csvfile:
    #   csv_append = csv.writer(csvfile)
    #   csv_append.writerow([data.counter, data.timestamp])
    #   csvfile.close()

  def run(self):
    # Print data header in the terminal
    # print("%-6s %-6s %-6s %-8s %-10s %-6s" % ("PID", "GPID", "UID", "INODE", "MESSAGE", "COUNTER(UID)"))

    # Keep on checking for new data
    while True:
      try:
        self.b.perf_buffer_poll()
      except KeyboardInterrupt:
        exit(0)