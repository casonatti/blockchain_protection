#include <linux/dcache.h>
#include <linux/sched.h>
#include <linux/fs.h>
#include <uapi/linux/ptrace.h>

BPF_HASH(counter_table);
BPF_HASH(permitted_processes_map, u64);
BPF_HASH(inode_map, u32);
//BPF_ARRAY(inode_map, u32, 1);
BPF_ARRAY(epoch_ts_map, u64, 1);
BPF_PERF_OUTPUT(output);

struct data_t {
  u64 uid;
  u32 thread_pid;
  u64 gpid;
  u32 hooked_inode;
  u32 protected_inode;
  u64 timestamp;
  u64 counter;
  char message[21];
};

int protected_file(struct pt_regs *ctx, struct file *file) {
  u64 boot_ebpf_ts = bpf_ktime_get_ns();
  struct data_t data = {};
  int index = 0;
  u64 counter = 0;
  u64 *boot_epoch_ts = epoch_ts_map.lookup(&index);

  if(!boot_epoch_ts)
    return -1;

  data.hooked_inode = file->f_inode->i_ino;             //pega o inode do arquivo que esta sendo aberto 

  u64 tgid = bpf_get_current_pid_tgid();           //u64 takes 64 bits where the first 32 bits are the group PID and the least 32 are the thread PID
  data.thread_pid = tgid;
  data.gpid = tgid >> 32;                          //pega o GPID do processo que efetuou a chamada de sistema 
  data.uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;    //pega o ID do usuario que efetuou a chamada de sistema

  u64 *inode_ptr = inode_map.lookup(&data.hooked_inode);   //pega o endereço do inode do arquivo protegido no map de inodes (inserido no userspace)
  if(inode_ptr != NULL) {
    data.protected_inode = *inode_ptr;                  //se existe um endereço, armazena o inode na estrutura de dados
    
    data.timestamp = *boot_epoch_ts + boot_ebpf_ts;   //time since epoch (got in user space when the program started) + computer uptime => timestamp in ns  

    u64 *permitted_process_ptr = permitted_processes_map.lookup(&data.gpid);

    if(permitted_process_ptr == NULL && data.uid != 0) {
      char message[20] = "GPID Not Authorized";

      bpf_probe_read_kernel(&data.message, sizeof(data.message), message);
      output.perf_submit(ctx, &data, sizeof(data));
      bpf_send_signal(9);
    } else {
      u64 *counter_ptr = counter_table.lookup(&data.uid);

      if(counter_ptr != 0) {
        counter = *counter_ptr;
      }

      counter++;
      counter_table.update(&data.uid, &counter);
      data.counter = counter;

      char message[11] = "Authorized";
      bpf_probe_read_kernel(&data.message, sizeof(data.message), message); //helper function usada para ler dados do kernel e armazena no espaco do ebpf
      

      output.perf_submit(ctx, &data, sizeof(data));     //popula o buffer que pode ser lido no userspace
    }
  }

  return 0;
}