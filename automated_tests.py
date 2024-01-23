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
        csv_writer.writerow(['Iteration','TS_Tests'])

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

read_file_multiple_times(file_path, 10000)