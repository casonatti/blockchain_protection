import csv
import time
import timeit

file_path="/home/jeison/ic/repositorios/solucao_ic/teste/wallet.txt"
result_file = "./resultados/file_access.csv"

def read_file_multiple_times(file_path, times):
    print("Automated Tests Initialized...")
    with open(result_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Iteration', 'TimeElapsed(seconds)'])

        for i in range(times):
            timestamp = time.time()
            with open(file_path, 'r') as file:
                content = file.read()

            formated_timestamp = f"{timestamp:.19}"
            csv_writer.writerow([i+1, formated_timestamp])

            # Introducing a delay of approximately 5 microsecond using timeit
            timeit.timeit(lambda: None, number=100000)  # Adjust number to control delay precision

read_file_multiple_times(file_path, 1000)