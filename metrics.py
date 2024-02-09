import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np

test_type_file = open('./tests/test_type.txt','r')
test_type = test_type_file.read()

#test_type = 'access_time'
#test_type = 'access_fault'
#test_type = 'overhead'

if test_type == 'access_time':
  source_automated_tests_ebpf = "./tests/" + test_type + "/at_ebpf_" + test_type + ".csv"
  source_automated_tests_inotify = "./tests/" + test_type + "/at_inotify_" + test_type + ".csv"
  source_ebpf = "./tests/" + test_type + "/ebpf_" + test_type + "_corrected.csv"
  source_inofify = "./tests/" + test_type + "/inotify_" + test_type + ".csv"

  df1 = pd.read_csv(source_automated_tests_ebpf)
  df2 = pd.read_csv(source_automated_tests_inotify)
  df3 = pd.read_csv(source_ebpf)
  df4 = pd.read_csv(source_inofify)

  merge_1 = pd.merge(df1, df2, on='Iteration')
  merge_2 = pd.merge(merge_1, df3, on='Iteration')
  df = pd.merge(merge_2, df4, on='Iteration')

  vector_size = [None]*1000

  df['Diff_Inotify'] = vector_size
  df['Diff_eBPF'] = vector_size

  df['Diff_Inotify'] = df['TS_Inotify'] - df['TS_AT_Inotify']
  df['Diff_eBPF'] = df['TS_eBPF'] - df['TS_AT_eBPF']

  
  print(df.head())

  print(df['Diff_eBPF'].mean())
  print(df['Diff_Inotify'].mean())

  
  plt.figure(figsize=(5,4))

  plt.plot(df['Iteration'], df['Diff_Inotify'], color='black', label='inotify', linestyle='solid', linewidth=.7)
  plt.plot(df['Iteration'], df['Diff_eBPF'], color='red', label='Scylla', linestyle='--', linewidth=.7)
  plt.yticks(list(range(0,260000,50000)) + [10000,60000])
  plt.legend()

  #plt.yscale('log')
  #plt.title("Time spent per Iteration")
  plt.grid(linestyle='-', color='lightgray')
  plt.gca().set_axisbelow(True)
  plt.xlabel("Iteration")
  plt.ylabel("Time [ns]")
  plt.tight_layout()
  #plt.show()
  plt.savefig("./tests/" + test_type + "/ebpf_x_inotify.pdf")

if test_type == 'overhead':
  source_automated_tests = "./tests/" + test_type + "/at_without_" + test_type + ".csv"
  source_ebpf = "./tests/" + test_type + "/at_ebpf_" + test_type + ".csv"
  source_inotify = "./tests/" + test_type + "/at_inotify_" + test_type + ".csv"
  source_p_ebpf = "./tests/" + test_type + "/at_p_ebpf_" + test_type + ".csv"
  source_p_inotify = "./tests/" + test_type + "/at_p_inotify_" + test_type + ".csv"
  

  df1 = pd.read_csv(source_automated_tests)
  df2 = pd.read_csv(source_ebpf)
  df3 = pd.read_csv(source_inotify)
  df4 = pd.read_csv(source_p_ebpf)
  df5 = pd.read_csv(source_p_inotify)

  merge_1 = pd.merge(df1, df2, on='Iteration')
  merge_2 = pd.merge(merge_1, df3, on='Iteration')
  merge_3 = pd.merge(merge_2, df4, on='Iteration')
  df = pd.merge(merge_3, df5, on='Iteration')

  print(f"without: {df1['Elapsed_Without'].mean()}")
  print(f"ebpf np: {df2['Elapsed_eBPF_NP'].mean()}")
  print(f"inotify np: {df3['Elapsed_Inotify_NP'].mean()}")
  print(f"ebpf p: {df4['Elapsed_eBPF_P'].mean()}")
  print(f"inotify p: {df5['Elapsed_Inotify_P'].mean()}")
  print()

  print(df.head())

  mean_at = df1['Elapsed_Without'].mean()
  mean_e_np = df2['Elapsed_eBPF_NP'].mean()
  mean_i_np = df3['Elapsed_Inotify_NP'].mean()
  mean_e_p = df4['Elapsed_eBPF_P'].mean()
  mean_i_p = df5['Elapsed_Inotify_P'].mean()

  df_std = df.std()

  errors = [df_std['Elapsed_eBPF_NP'], df_std['Elapsed_Inotify_NP'], df_std['Elapsed_eBPF_P'], df_std['Elapsed_Inotify_P']]
  print(errors)

  plt.figure(figsize=(5,4))
  #plt.grid(axis='y', linestyle='solid', linewidth=1.25)
  plt.grid(axis='y', linestyle='-', color='lightgray')
  plt.gca().set_axisbelow(True)
  mean_line = plt.axhline(mean_at, linestyle='dashed', linewidth=1, color='dimgray', label='Normal Access Mean')
  overhead = plt.bar(['eBPF\nUnprotected','inotify\nUnprotected','eBPF\nProtected', 'inotify\nProtected'], [mean_e_np, mean_i_np, mean_e_p, mean_i_p], color='lightgray', width=0.8, edgecolor='black', yerr=errors, capsize=7, label='Overhead')
  #plt.bar(['eBPF\nUnprotected','inotify\nUnprotected','eBPF\nProtected', 'inotify\nProtected'], [(.96*mean_e_np), (0.75*mean_i_np),(0.65*mean_e_p), (0.74*mean_i_p)], color='darkgray', width=0.78,  capsize=7)
  

  plt.ylim(0, 50000)

  plt.xlabel("Type of Access")
  plt.ylabel("Time [ns]")
  plt.legend(handles=[mean_line])

  #plt.text(-0.01, mean_at + 320, f'Mean: {round(mean_at):.2f}', color='red', fontsize=12, ha='center', rotation=35)
  plt.text(-.87, mean_at-120, f'{round(mean_at)}', color='dimgray', fontsize=10, ha='center')
  plt.text(-.61, mean_at-124, "-", color='black', fontsize=10, ha='center')
  plt.text(-.62, mean_at-124, "-", color='black', fontsize=10, ha='center')
  plt.text(0, mean_e_np/2, f'{round(((mean_e_np-mean_at)/mean_e_np)*100)}%', weight="bold", color='black', fontsize=10, ha='center')
  plt.text(1, mean_i_np/2, f'{round(((mean_i_np-mean_at)/mean_i_np)*100)}%', weight="bold", color='black', fontsize=10, ha='center')
  plt.text(2, mean_e_p/2, f'{round(((mean_e_p-mean_at)/mean_e_p)*100)}%', weight="bold", color='black', fontsize=10, ha='center')
  plt.text(3, mean_i_p/2, f'{round(((mean_i_p-mean_at)/mean_i_p)*100)}%', weight="bold", color='black', fontsize=10, ha='center')

  #plt.show()
  plt.tight_layout()
  plt.savefig("./tests/" + test_type + "/overhead.pdf")

if test_type == 'access_fault':
  source_automated_tests_ebpf_s1 = "./tests/" + test_type + "/at_ebpf_sample_1_" + test_type + ".csv"
  source_automated_tests_ebpf_s2 = "./tests/" + test_type + "/at_ebpf_sample_2_" + test_type + ".csv"
  source_automated_tests_ebpf_s3 = "./tests/" + test_type + "/at_ebpf_sample_3_" + test_type + ".csv"
  source_automated_tests_inot_s1 = "./tests/" + test_type + "/at_inot_sample_1_" + test_type + ".csv"
  source_automated_tests_inot_s2 = "./tests/" + test_type + "/at_inot_sample_2_" + test_type + ".csv"
  source_automated_tests_inot_s3 = "./tests/" + test_type + "/at_inot_sample_3_" + test_type + ".csv"
  source_ebpf_s1 = "./tests/" + test_type + "/ebpf_sample_1_" + test_type + "_corrected.csv"
  source_ebpf_s2 = "./tests/" + test_type + "/ebpf_sample_2_" + test_type + "_corrected.csv"
  source_ebpf_s3 = "./tests/" + test_type + "/ebpf_sample_3_" + test_type + "_corrected.csv"
  source_inot_s1 = "./tests/" + test_type + "/inotify_sample_1_" + test_type + ".csv"
  source_inot_s2 = "./tests/" + test_type + "/inotify_sample_2_" + test_type + ".csv"
  source_inot_s3 = "./tests/" + test_type + "/inotify_sample_3_" + test_type + ".csv"


  df_at_e_s1 = pd.read_csv(source_automated_tests_ebpf_s1)
  df_at_e_s2 = pd.read_csv(source_automated_tests_ebpf_s2)
  df_at_e_s3 = pd.read_csv(source_automated_tests_ebpf_s3)
  df_at_i_s1 = pd.read_csv(source_automated_tests_inot_s1)
  df_at_i_s2 = pd.read_csv(source_automated_tests_inot_s2)
  df_at_i_s3 = pd.read_csv(source_automated_tests_inot_s3)

  df_ebpf_s1 = pd.read_csv(source_ebpf_s1)
  df_ebpf_s2 = pd.read_csv(source_ebpf_s2)
  df_ebpf_s3 = pd.read_csv(source_ebpf_s3)

  df_inot_s1 = pd.read_csv(source_inot_s1)
  df_inot_s2 = pd.read_csv(source_inot_s2)
  df_inot_s3 = pd.read_csv(source_inot_s3)

  mean_ebpf = (df_ebpf_s1.size/2 + df_ebpf_s2.size/2 + df_ebpf_s3.size/2)/3
  mean_inotify = (df_inot_s1.size/2 + df_inot_s2.size/2 + df_inot_s3.size/2)/3

  mean_std_ebpf = math.sqrt((((df_ebpf_s1.size/2)-mean_ebpf)**2 + ((df_ebpf_s2.size/2)-mean_ebpf)**2 + ((df_ebpf_s3.size/2)-mean_ebpf)**2)/3)
  mean_std_inotify = math.sqrt((((df_inot_s1.size/2)-mean_inotify)**2 + ((df_inot_s2.size/2)-mean_inotify)**2 + ((df_inot_s3.size/2)-mean_inotify)**2)/3)
  errors = [mean_std_ebpf, mean_std_inotify]

  print("Média eBPF: " + mean_ebpf)
  print("Média Inotify: " + mean_inotify)
  print("Desvio Padrão eBPF: " + mean_std_ebpf)
  print("Desvio Padrão Inotify: " + mean_std_inotify)

  plt.figure(figsize=(8,5))
  #plt.grid(axis='y', linestyle='solid', linewidth=1.25)
  plt.grid(axis='y', linestyle='-', color='lightgray')
  plt.gca().set_axisbelow(True)
  total_access = plt.axhline(100000, linestyle='dashed', linewidth=1, color='red', label='Normal Access Count')
  plt.bar(['eBPF', 'Inotify'], [mean_ebpf, mean_inotify], color='lightgray', edgecolor='black', yerr=errors, capsize=7)

  plt.ylim(0, 110000)

  plt.xlabel("Type of Access")
  plt.ylabel("Access Count Mean")
  plt.legend(handles=[total_access])

  plt.text(-0.19, 100000 + 280, f'Total Access: 100000', color='red', fontsize=12, ha='center')

  #plt.show()
  plt.savefig("./tests/" + test_type + "/access_count.pdf")

if test_type == 'resource_usage':
  source_at_s1 = "./tests/" + test_type + "/at_sample_" + test_type + ".csv"
  source_scylla_s1 = "./tests/" + test_type + "/scylla_sample_" + test_type + ".csv"
  source_inot_s1 = "./tests/" + test_type + "/inotify_sample_" + test_type + ".csv"

  df1 = pd.read_csv(source_at_s1)
  df2 = pd.read_csv(source_scylla_s1)
  df3 = pd.read_csv(source_inot_s1)

  merge_1 = pd.merge(df1, df2, on='Time')
  df = pd.merge(merge_1, df3, on='Time')

  print(df)

  plt.figure(figsize=(8,5))

  df_markers = df
  df_markers = df_markers.groupby(np.arange(len(df_markers))//15).mean()

  #uncomment for peak test graphs
  df_markers['AT_CPU_USAGE'] = df_markers['AT_CPU_USAGE'].map({df_markers['AT_CPU_USAGE'].max():df['AT_CPU_USAGE'].max()}).fillna(df_markers['AT_CPU_USAGE'])
  df_markers['INOTIFY_CPU_USAGE'] = df_markers['INOTIFY_CPU_USAGE'].map({df_markers['INOTIFY_CPU_USAGE'].max():df['INOTIFY_CPU_USAGE'].max()}).fillna(df_markers['INOTIFY_CPU_USAGE'])
  df_markers['SCYLLA_CPU_USAGE'] = df_markers['SCYLLA_CPU_USAGE'].map({df_markers['SCYLLA_CPU_USAGE'].max():df['SCYLLA_CPU_USAGE'].max()}).fillna(df_markers['SCYLLA_CPU_USAGE'])

  print(df_markers)

  plt.plot(df_markers['Time'], df_markers['AT_CPU_USAGE'], '*', fillstyle='none', markersize=4, color='black', label='at', linestyle='solid', linewidth=.5)
  plt.plot(df_markers['Time'], df_markers['INOTIFY_CPU_USAGE'], 's', fillstyle='none', markersize=4, color='gray', label='inotify', linestyle='solid', linewidth=.5)
  plt.plot(df_markers['Time'], df_markers['SCYLLA_CPU_USAGE'], 'x', fillstyle='none', markersize=4, color='red', label='scylla', linestyle='dotted', linewidth=.5)
  # plt.yticks(list(range(0,50,5)))
  plt.legend()
  plt.xlabel("Time[s]")
  plt.ylabel("CPU Usage[%]")
  plt.grid(axis='y', linestyle='--')
  plt.savefig("./tests/" + test_type + "/cpu_usage.pdf")

  plt.figure(figsize=(8,5))
  plt.plot(df_markers['Time'], df_markers['AT_MEMORY_USAGE'], marker='*', fillstyle='none', markersize=4, color='black', label='at', linestyle='solid', linewidth=.5)
  plt.plot(df_markers['Time'], df_markers['INOTIFY_MEMORY_USAGE'], marker='s', fillstyle='none', markersize=4, color='gray', label='inotify', linestyle='solid', linewidth=.5)
  plt.plot(df_markers['Time'], df_markers['SCYLLA_MEMORY_USAGE'], marker='x', fillstyle='none', markersize=4, color='red', label='scylla', linestyle='dotted', linewidth=.5)
  plt.legend()
  plt.xlabel("Time[s]")
  plt.ylabel("Memory Usage[%]")

  plt.savefig("./tests/" + test_type + "/memory_usage.pdf")