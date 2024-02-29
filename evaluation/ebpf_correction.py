import csv

test_type_file = open('./config/test_type.txt','r')
test_type = test_type_file.read()

input = "./results/" + test_type + "/ebpf_" + test_type + ".csv"
output = "./results/" + test_type + "/ebpf_" + test_type + "_corrected.csv"

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