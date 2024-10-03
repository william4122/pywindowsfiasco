import os
import subprocess
from datetime import datetime
import ctypes
import sys
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init()

# Check if running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Relaunch script with admin privileges
if not is_admin():
    print(Fore.RED + "Script is not running with administrator privileges. Relaunching with admin rights..." + Style.RESET_ALL)
    # Re-run the script with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Directory containing the ISOs, replace with your directory!
iso_directory = r"C:\Users\Will\Desktop\Operating system ISOs"

# Get a list of ISO files in the directory
iso_files = [f for f in os.listdir(iso_directory) if f.endswith(".iso")]

# Display the list of ISOs
print(Fore.GREEN + Style.BRIGHT + "Available ISOs:" + Style.RESET_ALL)
for i, iso in enumerate(iso_files, 1):
    print(f"{Fore.YELLOW}{i}. {iso}{Style.RESET_ALL}")

# Ask user to select ISOs
user_input = input(Fore.CYAN + "Enter the numbers of the ISOs you'd like to provision (e.g., 1,2,3): " + Style.RESET_ALL)
selected_indices = [int(x.strip()) for x in user_input.split(",")]

# Get the current date and time with seconds
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Loop over the selected ISOs and provision VMs
for index in selected_indices:
    iso_file = iso_files[index - 1]  # Get the selected ISO file
    iso_filename = os.path.basename(iso_file).split('.')[0]  # Extract filename without extension
    vm_name = f"{current_datetime}_{iso_filename}"  # VM name with date and ISO filename
    iso_path = os.path.join(iso_directory, iso_file)  # Full path to the ISO

    # PowerShell command as a list to avoid issues with quotes and escaping
    ps_command = [
        "powershell", "-Command",
        f"New-VM -Name '{vm_name}' -MemoryStartupBytes 4GB -Generation 1 -NewVHDPath 'C:\\Hyper-V\\{vm_name}.vhdx' -NewVHDSizeBytes 50GB;",
        f"Set-VMDvdDrive -VMName '{vm_name}' -Path '{iso_path}';",
        f"Start-VM -Name '{vm_name}'"
    ]

    # Execute the PowerShell command using subprocess.run
    process = subprocess.run(ps_command, capture_output=True, text=True)

    # Output the result with colors
    if process.returncode == 0:
        print(Fore.GREEN + f"Successfully provisioned VM: {vm_name}" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Error provisioning VM: {vm_name}\n{process.stderr}\n{process.stdout}" + Style.RESET_ALL)
