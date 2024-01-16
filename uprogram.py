from bcc import BPF
from ctypes import *
import time
import csv

def print_event(cpu, data, size):
  data = b["output"].event(data)
  print(f"{data.pid} {data.uid} {data.message} {data.counter}")
  with open(result_file, 'a') as csvfile:
    csv_append = csv.writer(csvfile)
    csv_append.writerow([data.counter, data.timestamp])
    csvfile.close()

current_epoch_ts = time.time_ns()
boot_relative_ts = time.monotonic_ns()
boot_epoch_ts = current_epoch_ts - boot_relative_ts

test_number_file = open('./test_number.txt','r')
test_number = test_number_file.read()
result_file = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/ebpf_" + test_number + ".csv"

program = "kprogram.c"

b = BPF(src_file = program)

b.attach_kprobe(event = "vfs_read", fn_name = "protected_file")
#b.attach_kprobe(event = "vfs_write", fn_name= "protected_file")

#user/kernel space map association
i_map = b["inode_map"]
ts_map = b["epoch_ts_map"]
permitted_processes = b["permitted_processes_map"]

#populating maps
i_map[c_int(0)] = c_uint32(5114453) #TODO: flexibilizar o arquivo protegido
ts_map[c_int(0)] = c_uint64(boot_epoch_ts)
permitted_processes_file = open("./teste/permitted.txt", "r")
n = 0
line = permitted_processes_file.readline()
while line:
  print("Copying " + str(int(line)) + " to eBPF map [permitted_processes_map]")
  permitted_processes[c_uint64(int(line))] = c_uint64(int(line))
  line = permitted_processes_file.readline()
  n = n + 1


print("%-6s %-6s %-10s %-6s" % ("PID", "UID", "MESSAGE", "COUNTER"))
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