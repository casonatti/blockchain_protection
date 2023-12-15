import psutil
import time

#etime = time.time()
#xtime = time.monotonic()


etime = time.time()
etime_ns = time.time_ns()
xtime_ns = time.monotonic_ns()
xtime = time.monotonic()
btime_epoch = etime_ns - xtime_ns - 89999999


btime = psutil.boot_time()

print(f"ETIME: {etime:.23}")
print(f"ETIME (ns): {etime_ns}")
print(f"BTIME: {btime}")
print(f"XTIME: {xtime}")
print(f"XTIME (ns): {xtime_ns}")
print(f"BTIME_E: {btime_epoch}")