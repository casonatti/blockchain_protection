# Scylla: Securing Blockchain Wallet Files using eBPF

<img src="misc/logo.png" width="128"/>


## Introduction

In this repository, we introduce **Scylla**, an innovative solution meticulously designed to enhance the security of BC (Blockchain) wallet-related files by preventing unauthorized access through the utilization of eBPF (extended Berkeley Packet Filter). The proposed solution employs fine-grained access control mechanisms, providing robust protection for critical files, including account files. This is achieved by actively monitoring system calls of processes directed towards these sensitive files.

## Key Features

- **Fine-grained Access Control:** **Scylla** implements fine-grained access control measures to safeguard critical files, ensuring that only authorized processes can interact with them.

- **Automatic Execution:** The solution is designed to execute automatically during system boot time, ensuring seamless and continuous protection.

- **Protection Based on Inodes:** **Scylla** protects itself and user-defined files based on their *inodes*, providing an additional layer of security.

## How it Works

During execution, **Scylla** actively monitors the system calls of processes aiming to access sensitive files. This proactive approach allows it to intercept and prevent unauthorized attempts to read or modify the content of a file. Notably, evaluations of **Scylla** demonstrate its capability to achieve these security objectives without introducing significant overhead to legitimate processes.

## Performance Comparison

In comparative evaluations, **solution** has proven to outperform *inotify*, a Linux kernel subsystem designed for monitoring changes in the filesystem. Unlike *inotify*, **Scylla** goes beyond mere monitoring, actively preventing unauthorized file access and providing a more robust security solution for BC wallet-related files.

## Getting Started

To use **Scylla**, follow these steps:

1. Clone the repository: `git clone https://github.com/casonatti/blockchain_protection`
2. Follow the installation instructions in the provided documentation.
3. Execute **Scylla** during the boot time to enable automatic protection.

## Contributing

We welcome contributions from the community. If you find issues or have suggestions for improvements, please create an issue or submit a pull request.

## License

This project is licensed under the [Apache License 2.0](LICENSE) - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

We would like to express our gratitude to the open-source community and contributors for their valuable feedback and contributions to enhance the effectiveness of **Scylla**.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Language](https://img.shields.io/badge/Language-Python-green.svg)](https://www.python.org/)
