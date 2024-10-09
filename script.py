#!/usr/bin/env python3
import argparse
import os


def get_cpu_name():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if "model name" in line:
                return line.split(":")[1].strip()


def get_cpu_cores():
    cores = 0
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line.startswith("processor"):
                cores += 1
    return cores


def get_total_ram_gb():
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if "MemTotal" in line:
                mem_kb = int(line.split()[1])
                mem_gb = mem_kb / (1024 * 1024)
                return round(mem_gb, 2)
            

def get_available_memory_gb():
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if "MemAvailable" in line:
                mem_kb = int(line.split()[1])
                mem_gb = mem_kb / (1024 * 1024)
                return round(mem_gb, 2)


def get_storage_devices():
    devices = []
    for device in os.listdir('/sys/block'):
        if not device.startswith(("loop", "ram")):
            devices.append(device)
    return devices


def get_device_size_gb(device):
    size_path = f'/sys/block/{device}/size'
    with open(size_path, 'r') as f:
        sectors = int(f.read().strip())
        size_gb = (sectors * 512) / (1024 ** 3)  # Convert to GB
        return round(size_gb, 2)


def get_root_device():
    with open('/proc/mounts', 'r') as f:
        for line in f:
            parts = line.split()
            if parts[1] == '/':
                return parts[0]


def get_mounted_filesystems():
    with open('/proc/mounts', 'r') as f:
        return len(f.readlines())
    

def get_running_processes():
    process_count = 0
    for entry in os.listdir('/proc'):
        if entry.isdigit():
            process_count += 1
    return process_count


def get_kernel_cmdline():
    with open('/proc/cmdline', 'r') as f:
        return f.read().strip()


def get_kernel_version():
    with open('/proc/version', 'r') as f:
        return f.read().split()[2]


def get_system_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.read().split()[0])
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        return f"{hours}h {minutes}m {seconds}s"


def main():
    parser = argparse.ArgumentParser(description="System Information Tool")
    parser.add_argument('--cpu', action='store_true', help="Show CPU information")
    parser.add_argument('--memory', action='store_true', help="Show memory information")
    parser.add_argument('--storage', action='store_true', help="Show storage devices and their sizes")
    parser.add_argument('--root', action='store_true', help="Show the root filesystem device")
    parser.add_argument('--filesystems', action='store_true', help="Show the total number of mounted filesystems")
    parser.add_argument('--processes', action='store_true', help="Show the number of running processes")
    parser.add_argument('--cmdline', action='store_true', help="Show the kernel command line")
    parser.add_argument('--version', action='store_true', help="Show the kernel version")
    parser.add_argument('--uptime', action='store_true', help="Show system uptime")

    args = parser.parse_args()

    if args.cpu:
        print("CPU Name:", get_cpu_name())
        print("CPU Cores:", get_cpu_cores())
    
    if args.memory:
        print("Total RAM (GB):", get_total_ram_gb())
        print("Available Memory (GB):", get_available_memory_gb())
    
    if args.storage:
        devices = get_storage_devices()
        print("Storage Devices:")
        for device in devices:
            print(f"  {device}: {get_device_size_gb(device)} GB")
    
    if args.root:
        print("Root Filesystem Device:", get_root_device())
    
    if args.filesystems:
        print("Total Mounted Filesystems:", get_mounted_filesystems())
    
    if args.processes:
        print("Running Processes:", get_running_processes())
    
    if args.cmdline:
        print("Kernel Command Line:", get_kernel_cmdline())
    
    if args.version:
        print("Kernel Version:", get_kernel_version())
    
    if args.uptime:
        print("System Uptime:", get_system_uptime())

if __name__ == "__main__":
    main()

