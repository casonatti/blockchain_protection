import csv
import time
import timeit

test_number_file = open('./test_number.txt','r')
test_number = test_number_file.read()

file_path="/home/jeison/ic/repositorios/solucao_ic/teste/wallet.txt"
result_file = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_" + test_number + ".csv"

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

            # Introducing a delay of approximately 15 microsecond using timeit
            #timeit.timeit(lambda: None, number=15000)  # Adjust number to control delay precision

read_file_multiple_times(file_path, 10000)