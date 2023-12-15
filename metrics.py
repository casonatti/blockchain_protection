import pandas as pd
import matplotlib.pyplot as plt

test_number_file = open('./test_number.txt','r')
test_number = test_number_file.read()


if test_number == 'test_0':
  source_automated_tests = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_" + test_number + ".csv"
  source_ebpf = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/ebpf_" + test_number + "_corrected.csv"
  source_inofify = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/inotify_" + test_number + ".csv"

  df1 = pd.read_csv(source_automated_tests)
  df2 = pd.read_csv(source_ebpf)
  df3 = pd.read_csv(source_inofify)

  merged_df = pd.merge(df1, df2, on='Iteration')
  df = pd.merge(merged_df, df3, on='Iteration')

  vector_size = [None]*1000

  df['Diff_Inotify'] = vector_size
  df['Diff_eBPF'] = vector_size

  df['Diff_Inotify'] = df['TS_Inotify'] - df['TS_Tests']
  df['Diff_eBPF'] = df['TS_eBPF'] - df['TS_Tests']

  print(df.head())

  df.plot.line(y=['Diff_eBPF', 'Diff_Inotify'], figsize=(10,6))

  plt.title("eBPF x Inotify")
  plt.xlabel("Iteration")
  plt.ylabel("Time(ns)")

  #plt.show()
  plt.savefig("/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/mean_time.pdf")

if test_number == 'test_1':
  source_automated_tests_ebpf = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_ebpf_" + test_number + ".csv"
  source_automated_tests_inotify = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_inotify_" + test_number + ".csv"
  source_ebpf = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/ebpf_" + test_number + "_corrected.csv"
  source_inofify = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/inotify_" + test_number + ".csv"

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

  df['Diff_Inotify'] = df['TS_Inotify'] - df['TS_Tests_Inotify']
  df['Diff_eBPF'] = df['TS_eBPF'] - df['TS_Tests_eBPF']

  print(df.head())

  plt.figure(figsize=(8,6))
  plt.plot(df['Iteration'], df['Diff_Inotify'], color='darkgray', label='Inotify', linestyle='solid', linewidth=0.7)
  plt.plot(df['Iteration'], df['Diff_eBPF'], color='red', label='eBPF', linestyle='dashdot', linewidth=0.7)
  plt.legend()


  #plt.title("Time spent per Iteration")
  plt.xlabel("Iteration")
  plt.ylabel("Time(ns)")

  #plt.show()
  plt.savefig("/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/ebpf_x_inotify.pdf")

if test_number == 'test_2':
  source_automated_tests = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_without_" + test_number + ".csv"
  source_ebpf = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_ebpf_" + test_number + ".csv"
  source_inotify = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_inotify_" + test_number + ".csv"
  source_p_ebpf = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_p_ebpf_" + test_number + ".csv"
  source_p_inotify = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_p_inotify_" + test_number + ".csv"
  

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

  plt.figure(figsize=(8,5))
  plt.grid(axis='y', linestyle='solid', linewidth=1.25)
  plt.gca().set_axisbelow(True)
  mean_line = plt.axhline(mean_at, linestyle='dashed', linewidth=1, color='red', label='Normal Access Time')
  plt.bar(['eBPF_Unprotected','Inotify_Unprotected','eBPF_Protected', 'Inotify_Protected'], [mean_e_np, mean_i_np, mean_e_p, mean_i_p], color='lightgray', edgecolor='black', yerr=errors, capsize=7)

  plt.ylim(0, 10000)

  plt.xlabel("Type of Access")
  plt.ylabel("Time [ns]")
  plt.legend(handles=[mean_line])

  plt.text(-0.19, mean_at + 280, f'Mean: {mean_at:.2f}', color='red', fontsize=12, ha='center', rotation=45)

  #plt.show()
  plt.savefig("/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/overhead.pdf")

if test_number == 'test_3':
  print(test_number)

  source_automated_tests_ebpf_s1 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_ebpf_sample_1_" + test_number + ".csv"
  source_automated_tests_ebpf_s2 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_ebpf_sample_2_" + test_number + ".csv"
  source_automated_tests_ebpf_s3 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_ebpf_sample_3_" + test_number + ".csv"
  source_automated_tests_inot_s1 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_inot_sample_1_" + test_number + ".csv"
  source_automated_tests_inot_s2 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_inot_sample_2_" + test_number + ".csv"
  source_automated_tests_inot_s3 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/at_inot_sample_3_" + test_number + ".csv"
  source_ebpf_s1 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/ebpf_sample_1_" + test_number + "_corrected.csv"
  source_ebpf_s2 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/ebpf_sample_2_" + test_number + "_corrected.csv"
  source_ebpf_s3 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/ebpf_sample_3_" + test_number + "_corrected.csv"
  source_inot_s1 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/inotify_sample_1_" + test_number + ".csv"
  source_inot_s2 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/inotify_sample_2_" + test_number + ".csv"
  source_inot_s3 = "/home/jeison/ic/repositorios/solucao_ic/teste/" + test_number + "/inotify_sample_3_" + test_number + ".csv"


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

  print(df_at_e_s1.size/2)
  print(df_at_e_s2.size/2)
  print(df_at_e_s3.size/2)
  print(df_at_i_s1.size/2)
  print(df_at_i_s2.size/2)
  print(df_at_i_s3.size/2)

  print(df_ebpf_s1.size/2)
  print(df_ebpf_s2.size/2)
  print(df_ebpf_s3.size/2)

  print(df_inot_s1.size/2)
  print(df_inot_s2.size/2)
  print(df_inot_s3.size/2)

  a = df_ebpf_s1.size/2 + df_ebpf_s2.size/2 + df_ebpf_s3.size/2
  print(a/3)

  #df.plot.line(y='Diff_Inotify', figsize=(10,6))
  #df.plot.line(y='Diff_eBPF', figsize=(10,6))

  #plt.title("Time spent per Iteration")
  #plt.xlabel("Iteration")
  #plt.ylabel("Time(ns)")

  #plt.show()