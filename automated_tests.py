import csv
import time
import timeit

test_type_file = open('./tests/test_type.txt','r')
test_type = test_type_file.read()

file_path="./tests/wallet.txt"
result_file = "./tests/" + test_type + "/at_" + test_type + ".csv"

def read_file_multiple_times(file_path, times):
    print("Automated Tests Initialized...")
    with open(result_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Iteration','Elapsed_eBPF_NP'])

        for i in range(times):
            start = time.time_ns()
            with open(file_path, 'r') as file:
                content = file.read()

            end = time.time_ns()
            elapsed = end - start
            #formated_timestamp = f"{timestamp:.19}"
            csv_writer.writerow([i+1, elapsed])

            # Introducing a delay of approximately 270 nanoseconds using timeit
            timeit.timeit(lambda: None, number=270)  # Adjust number to control delay precision

def read_file_multiple_times_access_time(file_path, times):
    print("Automated Tests Initialized...")
    with open(result_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Iteration', 'TS_AT_eBPF'])

        for i in range(times):
            timestamp = time.time_ns()
            with open(file_path, 'r') as file:
                content = file.read()

            csv_writer.writerow([i+1, timestamp])

            # Introducing a delay of approximately 5 microsecond using timeit
            timeit.timeit(lambda: None, number=5000)  # Adjust number to control delay precision

if(test_type == 'access_time'):
    read_file_multiple_times_access_time(file_path, 1000)
else:
    read_file_multiple_times(file_path, 10000)