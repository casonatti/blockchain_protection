#include <linux/dcache.h>
#include <linux/sched.h>
#include <linux/fs.h>
#include <uapi/linux/ptrace.h>

BPF_HASH(counter_table);
BPF_ARRAY(inode_map, u32, 1);
BPF_PERF_OUTPUT(output);

struct data_t {
  u64 uid;
  u32 pid;
  u32 hooked_inode;
  u32 protected_inode;
  u64 timestamp;
  u64 counter;
  char message[18];
};

int protected_file(struct pt_regs *ctx, struct file *file) {
  struct data_t data = {};
  int index = 0;
  u64 counter = 0;

  data.hooked_inode = file->f_inode->i_ino;             //pega o inode do arquivo que esta sendo aberto 

  data.pid = bpf_get_current_pid_tgid();                //pega o PID do processo que efetuou a chamada de sistema
  data.uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;    //pega o ID do usuario que efetuou a chamada de sistema

  unsigned int *inode_ptr = inode_map.lookup(&index);   //pega o endereço do inode do arquivo protegido no map de inodes (inserido no userspace)
  if(inode_ptr != NULL) {
    data.protected_inode = *inode_ptr;                  //se existe um endereço, armazena o inode na estrutura de dados
    if(data.protected_inode == data.hooked_inode) {     //compara o inode do arquivo protegido com o inode do arquivo que esta sendo aberto
      data.timestamp = bpf_ktime_get_ns();              //registra o timestamp do evento
      u64 *counter_ptr = counter_table.lookup(&data.uid);
      if(counter_ptr != 0) {
        counter = *counter_ptr;
        counter++;
        counter_table.update(&data.uid, &counter);
        data.counter = counter;
      }
      if(data.uid == 1000) {                            //caso seja um usuario nao autorizado, cria a mensagem de negacao e mata o processo
        char message[18] = "Permission Denied";
        bpf_probe_read_kernel(&data.message, sizeof(data.message), message); //helper function usada para ler dados do kernel e armazena no espaco do ebpf
        bpf_send_signal(9);                             //helper function para enviar sinais do sistema
      } else {                                          //caso seja um usuario autorizado, cria a mensagem de autorizacao e permite a conclusao da chamada
        char message[11] = "Authorized";
        bpf_probe_read_kernel(&data.message, sizeof(data.message), message); //helper function usada para ler dados do kernel e armazena no espaco do ebpf
      }

      output.perf_submit(ctx, &data, sizeof(data));     //popula o buffer que pode ser lido no userspace
    }
  }

  return 0;
}