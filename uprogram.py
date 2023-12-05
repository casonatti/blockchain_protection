from bcc import BPF
from ctypes import *

program = "kprogram.c"

b = BPF(src_file = program)

b.attach_kprobe(event = "vfs_read", fn_name = "protected_file")
b.attach_kprobe(event = "vfs_write", fn_name= "protected_file")

def print_event(cpu, data, size):
  data = b["output"].event(data)
  print(f"{data.pid} {data.uid} {data.message} {data.counter}")

i_map = b["inode_map"]

i_map[c_int(0)] = c_uint32(5112459) #TODO: flexibilizar o arquivo protegido

print("%-6s %-6s %-10s %-6s" % ("PID", "UID", "MESSAGE", "COUNTER"))

b["output"].open_perf_buffer(print_event)

while True:
  try:
    b.perf_buffer_poll()
  except KeyboardInterrupt:
    exit(0)