#include <linux/dcache.h>
#include <linux/sched.h>
#include <linux/fs.h>
#include <uapi/linux/ptrace.h>

// Define BPF hash maps and arrays
BPF_HASH(counter_table);                // Map to store user counters
BPF_HASH(permitted_processes_map, u64); // Map to store permitted processes
BPF_HASH(protected_inodes_map, u32);    // Map to store protected inodes
BPF_ARRAY(epoch_ts_map, u64, 1);        // Array to store epoch timestamp
BPF_PERF_OUTPUT(output);                // Perf output to send data to user space

struct data_t {
  u64 uid;              // User ID
  u32 thread_pid;       // Thread PID
  u64 thread_gpid;      // Thread Group PID
  u32 hooked_inode;     // Inode of the file being accessed
  u32 protected_inode;  // Protected inode
  u64 timestamp;        // Timestamp
  u64 counter;          // Counter
  char hooked_filename[30]; // Filename of the file being accessed
  int auth;             // Authorized
};

int protected_file(struct pt_regs *ctx, struct file *file) {
  // Get boot epoch timestamp
  u64 boot_ebpf_ts = bpf_ktime_get_ns();

  // Initialize variables
  struct data_t data = {};
  struct dentry *dentry;
  int index = 0;
  u64 counter = 0;
  u64 *boot_epoch_ts = epoch_ts_map.lookup(&index);

  // If there is no timestamp in the map, return
  if(!boot_epoch_ts)
    return -1;

  // Get the filename of the file being accessed
  dentry = file->f_path.dentry;
  if (dentry != NULL && dentry->d_name.name != NULL) {
    bpf_probe_read_kernel(&data.hooked_filename, sizeof(data.hooked_filename), dentry->d_name.name);
  }

  // Get inode of the file being accessed
  data.hooked_inode = file->f_inode->i_ino;

  // Get PID, Group PID and User ID info
  u64 tgid = bpf_get_current_pid_tgid();
  data.thread_pid = tgid;
  data.thread_gpid = tgid >> 32;
  data.uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;

  // Lookup protected inode
  u64 *inode_ptr = protected_inodes_map.lookup(&data.hooked_inode);

  // If protected inode is found, the hooked inode is a protected file
  if(inode_ptr != NULL) {
    data.protected_inode = *inode_ptr;
    
    // Update timestamp
    data.timestamp = *boot_epoch_ts + boot_ebpf_ts;

    // Check if the process is a permitted one
    u64 *permitted_process_ptr = permitted_processes_map.lookup(&data.thread_gpid);

    // If the process is not a permitted one, send data to user-space and kill the process
    if(permitted_process_ptr == NULL) {
      data.auth = 0;

      // Send data to user-space
      output.perf_submit(ctx, &data, sizeof(data));

      // Kill the process
      bpf_send_signal(9);
    } else {
      data.auth = 1;

      // Get user counter
      u64 *counter_ptr = counter_table.lookup(&data.uid);

      if(counter_ptr != 0) {
        counter = *counter_ptr;
      }

      counter++;

      // Update Map
      counter_table.update(&data.uid, &counter);
      data.counter = counter;
      
      // Send data to user-space
      output.perf_submit(ctx, &data, sizeof(data));
    }
  }

  return 0;
}