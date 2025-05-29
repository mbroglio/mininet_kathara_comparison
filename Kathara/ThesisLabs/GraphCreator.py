import matplotlib.pyplot as plt
import re
import datetime
import os
import sys

# Regular expression pattern to match log timestamp
timestamp_pattern = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - CPU and Memory Usage for Kathara-Related Processes"
)

# Regular expression pattern to match process data
process_pattern = re.compile(r"^\S+\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)\s+(.+)$")


def parse_log(log_file_path):
    """Parse a single kathara log file and return the usage data."""
    relative_times = []
    cpu_usage = []
    mem_usage = []

    try:
        with open(log_file_path, "r") as file:
            lines = file.readlines()

        current_timestamp = None
        start_timestamp = None
        total_cpu = 0.0
        total_mem = 0.0

        for line in lines:
            timestamp_match = timestamp_pattern.match(line)
            if timestamp_match:
                if current_timestamp:
                    # Store data from previous timestamp
                    # Calculate relative time in seconds from start
                    time_diff = (current_timestamp - start_timestamp).total_seconds()
                    relative_times.append(time_diff)
                    cpu_usage.append(total_cpu)
                    mem_usage.append(total_mem)
                else:
                    # First timestamp encountered
                    start_timestamp = datetime.datetime.strptime(
                        timestamp_match.group(1), "%Y-%m-%d %H:%M:%S"
                    )

                # Parse current timestamp
                current_timestamp = datetime.datetime.strptime(
                    timestamp_match.group(1), "%Y-%m-%d %H:%M:%S"
                )
                total_cpu = 0.0
                total_mem = 0.0
                continue

            process_match = process_pattern.match(line.strip())
            if process_match:
                total_cpu += float(process_match.group(2))  # %CPU
                total_mem += float(process_match.group(3))  # %MEM

        # Store the last recorded data
        if current_timestamp and start_timestamp:
            time_diff = (current_timestamp - start_timestamp).total_seconds()
            relative_times.append(time_diff)
            cpu_usage.append(total_cpu)
            mem_usage.append(total_mem)

        return relative_times, cpu_usage, mem_usage
    except Exception as e:
        print(f"Error parsing log file {log_file_path}: {e}")
        return [], [], []


def plot_and_save_graphs(relative_times, cpu_usage, mem_usage, folder_name, output_dir):
    """Plot and save CPU and memory usage graphs for a given folder."""
    if not relative_times:
        print(f"No data to plot for {folder_name}")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Plot CPU usage over time
    plt.figure(figsize=(10, 5))
    plt.plot(
        relative_times,
        cpu_usage,
        label="CPU Usage (%)",
        color="red",
        linestyle="-",
    )
    #plt.title(f"{folder_name} - Total CPU Usage Over Time")
    plt.xlabel("Time (seconds from start)")
    plt.ylabel("CPU Usage (%)")
    plt.grid(True)
    plt.legend()
    cpu_svg_path = os.path.join(output_dir, f"{folder_name}_kathara_cpu_usage.svg")
    plt.savefig(cpu_svg_path, format="svg")
    plt.close()  # Close the figure to free memory

    # Plot Memory usage over time
    plt.figure(figsize=(10, 5))
    plt.plot(
        relative_times,
        mem_usage,
        label="Memory Usage (%)",
        color="blue",
        linestyle="-",
    )
    #plt.title(f"{folder_name} - Total Memory Usage Over Time")
    plt.xlabel("Time (seconds from start)")
    plt.ylabel("Memory Usage (%)")
    plt.grid(True)
    plt.legend()
    mem_svg_path = os.path.join(output_dir, f"{folder_name}_kathara_memory_usage.svg")
    plt.savefig(mem_svg_path, format="svg")
    plt.close()  # Close the figure to free memory

    print(f"Saved graphs for {folder_name}")


def process_directories(root_dir, output_dir="kathara"):
    """Recursively process all directories starting from root_dir."""
    log_filename = "kathara_usage.log"
    processed_folders = 0

    for current_dir, subdirs, files in os.walk(root_dir):
        if log_filename in files:
            # Get folder name for output file naming
            folder_name = os.path.basename(current_dir)
            if not folder_name:  # In case we're in the root directory
                folder_name = "root"

            print(f"Processing {folder_name}...")
            log_file_path = os.path.join(current_dir, log_filename)
            
            # Parse the log file
            relative_times, cpu_usage, mem_usage = parse_log(log_file_path)
            
            # Plot and save the graphs
            plot_and_save_graphs(relative_times, cpu_usage, mem_usage, folder_name, output_dir)
            processed_folders += 1

    if processed_folders == 0:
        print(f"No '{log_filename}' files found in any subdirectories of '{root_dir}'")
    else:
        print(f"Processed {processed_folders} folders. All output saved to '{output_dir}' directory.")


if __name__ == "__main__":
    # Use command line argument for root directory if provided, otherwise use current directory
    root_directory = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # Create output directory for all SVG files
    output_directory = "kathara"
    
    print(f"Searching for kathara_usage.log files in '{root_directory}' and all subdirectories...")
    process_directories(root_directory, output_directory)