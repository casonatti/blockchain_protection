import csv

test_number_file = open('./test_number.txt','r')
test_number = test_number_file.read()

input = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/ebpf_" + test_number + ".csv"
output = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/ebpf_" + test_number + "_corrected.csv"

i = 1

with open(input) as csv_file:
    data_source = csv.reader(csv_file, delimiter=',')
    with open(output, 'w', newline='') as results_file:
        data_sink = csv.writer(results_file)
        data_sink.writerow(['Iteration','TS_eBPF'])
        for line in data_source:
          if line[0] != 'Iteration':
            if int(line[0]) % 2 == 1:
              data_sink.writerow([i, line[1]])
              i=i+1