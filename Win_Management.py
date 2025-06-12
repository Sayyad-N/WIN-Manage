#Code Written By SayyadN
#Date : 12-6-2025
#Code Start

#Import Reqired Libs
import ctypes , subprocess , winreg , random , string , os , wmi , sys , ctypes.wintypes , math 

#Admin Check
def admin():
    try:
       return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if  not admin():
    print("Please ReRun App as Admin")

#All Functions For user management
def list_users():
    result = subprocess.check_output("net user", shell=True, text=True)
    users =[]
    for line in result.splitlines():
        if "----" in line or "The command completed" in line or line.strip() == "":
            continue
        users.extend(line.strip().split())
    print(f"All Users: {users}")
    return users

#For Add User
def add_user():
    user_name = input("Enter Your User_name :").strip()
    passwd = input("Enter You passwd : ")
    subprocess.call(f"net user {user_name} {passwd} /add" , shell=True )
    print(f"Added USer: {user_name} , Password is {passwd}")

#For Delete as user
def del_user(): 
    user_name = input("Enter Your User name :").strip()
    if user_name not in list_users :
        print("User Not Found Please Check Again")
        return False
    else: 
        subprocess.call(f'net user {user_name} /delete', shell=True)
        print(f"user {user_name} deleted")
        return True

#Change user passwd
def passwd_change():
    user_name = input("Enter User_name :").strip()
    if user_name not in list_users :
        print("Please Check USer Name ")
    else:
        passwd = input("Enter Your Passwd (Enter if none) :")
        subprocess.call(f'net user "{username}" "{new_password}"', shell=True)
        print("Password Changed or Set")

#For Disable User 
def Disable_user():
    user_name = input("Enter User Name :")
    if user_name not in list_users :
        print("Please Check USer Name ")
    else:
        subprocess.call(f'net user "{username}" /active:no', shell=True)
        print("User Disabled")

#enable user 
def enable_user():
    user_name = input("Enter User Name :")
    if user_name not in list_users :
        print("Please Check USer Name ")
    else:
        subprocess.call(f'net user "{username}" /active:yes', shell=True)
        print("User Enabled")

#Remove Admin
def remove_admin():
    user_name = input("Enter User Name :")
    if user_name not in list_users :
        print("Please Check USer Name ")
    else:
        subprocess.call(f'net localgroup administrators "{username}" /delete', shell=True)
        print("Admin Removed ")

def list_groups():
    result = subprocess.check_output("net localgroup", shell=True, text=True)
    groups = []
    for line in result.splitlines():
        line = line.strip()
        if line and not line.startswith("---") and not line.lower().startswith("the command completed"):
            groups.extend(line.split())
    print(f"\nAll Groups:\n{groups}")
    return groups

def list_group_members():
    group_name = input("Enter Group Name: ").strip()
    groups = list_groups()
    if group_name not in groups:
        print("Check Group Name")
        return None
    else:
        result = subprocess.check_output(f'net localgroup "{group_name}"', shell=True, text=True)
        print(f"\nAll Users in Group '{group_name}':\n{result}")
        return result

def create_group():
    group_name = input("Enter Group Name: ").strip()
    groups = list_groups()
    if group_name in groups:
        print(f"Group '{group_name}' already exists.")
        return
    subprocess.call(f'net localgroup "{group_name}" /add', shell=True)
    print(f"Group '{group_name}' added.")

def del_group():
    group_name = input("Enter Group Name: ").strip()
    groups = list_groups()
    if group_name not in groups:
        print("Check Group Name")
        return
    subprocess.call(f'net localgroup "{group_name}" /delete', shell=True)
    print(f"Group '{group_name}' deleted.")

def addto_group():
    user_name = input("Enter User Name: ").strip()
    group_name = input("Enter Group Name: ").strip()

    groups = list_groups()
    users = list_users()

    if group_name not in groups:
        print("Check Group Name")
        return
    if user_name not in users:
        print("Check User Name")
        return

    subprocess.call(f'net localgroup "{group_name}" "{user_name}" /add', shell=True)
    print(f"Added user '{user_name}' to group '{group_name}'.")

def removefrom_group():
    user_name = input("Enter User Name: ").strip()
    group_name = input("Enter Group Name: ").strip()

    groups = list_groups()
    users = list_users()

    if group_name not in groups:
        print("Check Group Name")
        return
    if user_name not in users:
        print("Check User Name")
        return

    subprocess.call(f'net localgroup "{group_name}" "{user_name}" /delete', shell=True)
    print(f"Removed user '{user_name}' from group '{group_name}'.")

def user_management():
    while True:
        print("\n======= User Management  =======")
        print("1.list users")
        print("2. Add User ")
        print("3. Remove User")
        print("4. Password Change")
        print("5. Disable USer")
        print("6. Enable User")
        print("7. Remove Admin ")
        print("8. List Groups")
        print("9. List Group Members")
        print("10. Create Group")
        print("11. Remove Group")
        print("12. Add User To Group")
        print("13. Remove User From Group")
        print("0. Exit")

        choice = input("Choose: ").strip()

        match choice:
            case "1": list_users()
            case "2": add_user()
            case "3": del_user()
            case "4": passwd_change()
            case "5": disable_user()
            case "6": enable_user()
            case "7": remove_admin()
            case "8": list_groups()
            case "9": list_group_members()
            case "10": create_group()
            case "11": del_group()
            case "12": addto_group()
            case "13": Removefrom_group()
            case "0":
                print("👋 Exit")
                break
            case _: print("❌ Invaild Input")

#All Functions in User Management Ended 

#All Funtions in Computer Management Enterprise (Note : Some Setting Will be removed and You Relly need Admin TO back it)

# Check admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def relaunch_as_admin():
    if not is_admin():
        print("Relaunching with administrator privileges...")
        # Use ShellExecuteW with "runas" verb to relaunch as admin
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit()  # Exit the current non-admin process

# Run command silently
def run_cmd(command):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call(command, shell=True, startupinfo=startupinfo)

# Set a registry value
def set_reg(hive, path, name, value, reg_type=winreg.REG_DWORD):
    try:
        key = winreg.CreateKey(hive, path)
        winreg.SetValueEx(key, name, 0, reg_type, value)
        winreg.CloseKey(key)
        print(f"[+] Set: {path}\\{name} = {value}")
    except:
        print(f"[!] Failed to set: {path}\\{name}")

# Delete a registry value
def del_reg(hive, path, name):
    try:
        key = winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
        print(f"[+] Removed: {path}\\{name}")
    except:
        pass

# Generate a random PC name
def generate_name():
        return "WIN-" + ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Change PC name
def change_computer_name(new_name):
    old_name = os.environ["COMPUTERNAME"]
    run_cmd(f'wmic computersystem where name="{old_name}" call rename name="{new_name}"')
    print(f"[+] Changed computer name to: {new_name}")
    print("[!] Restarting to apply changes...")
    run_cmd("shutdown /r /t 5 /f")

# Apply all hardening settings
def apply_hardening():
    print("[*] Applying cybersecurity hardening settings...")

    # Disable telemetry & activity
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry", 0)
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\System", "PublishUserActivities", 0)
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\System", "UploadUserActivities", 0)

    # Disable Cortana
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\Windows Search", "AllowCortana", 0)

    # Disable remote desktop/assistance
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Terminal Server", "fDenyTSConnections", 1)
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Remote Assistance", "fAllowToGetHelp", 0)

    # Disable Control Panel & settings pages
    set_reg(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoControlPanel", 1)
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", "SettingsPageVisibility", "hide:privacy;privacy-feedback;privacy-speech;privacy-location", winreg.REG_SZ)

    # Disable Task Manager, CMD, Registry, Run
    set_reg(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableTaskMgr", 1)
    set_reg(winreg.HKEY_CURRENT_USER, r"Software\Policies\Microsoft\Windows\System", "DisableCMD", 1)
    set_reg(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableRegistryTools", 1)
    set_reg(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoRun", 1)

    # Disable USB storage
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\USBSTOR", "Start", 4)

    # Enforce password policy (lock screen, complexity)
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "InactivityTimeoutSecs", 300)
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Lsa", "LimitBlankPasswordUse", 1)

    # Disable hotspot and Bluetooth
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Network", "NC_ShowSharedAccessUI", 0)
    set_reg(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\BTHPORT", "Start", 4)

    # Disable advertising ID
    set_reg(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo", "Enabled", 0)

    # Change PC name
    new_name = generate_name()
    change_computer_name(new_name)

# Revert all changes
def rollback_settings():
    print("[*] Rolling back all changes...")

    # Revert all registry settings
    registry_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\System", "PublishUserActivities"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\System", "UploadUserActivities"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\Windows Search", "AllowCortana"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Terminal Server", "fDenyTSConnections"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Remote Assistance", "fAllowToGetHelp"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoControlPanel"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", "SettingsPageVisibility"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableTaskMgr"),
        (winreg.HKEY_CURRENT_USER, r"Software\Policies\Microsoft\Windows\System", "DisableCMD"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableRegistryTools"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoRun"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\USBSTOR", "Start"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "InactivityTimeoutSecs"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Lsa", "LimitBlankPasswordUse"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Network", "NC_ShowSharedAccessUI"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\BTHPORT", "Start"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo", "Enabled")
    ]

    for hive, path, name in registry_keys:
        del_reg(hive, path, name)

    print("[+] All settings reverted. You may need to restart.")

def Menu_Cyber():
        print("""
1. Apply Cybersecurity Hardening
2. Rollback Changes
            """)

        choice = input("Select option [1 or 2]: ").strip()

        if choice == "1":
             apply_hardening()
        elif choice == "2":
            rollback_settings()
        else:
            print("❌ Invalid choice.")

#All Cyber Functions Ending Bro 

#All Functions About System Info ,,
#  Source From : https://github.com/nathan242/system_detect/blob/master/system_detect.py

def System_info():
# Function to get valid WMI data
    def get_objects(obj_list, values, not_empty):
        ret = []
        for o in obj_list:
            valid = all(str(getattr(o, e)).strip() not in ["", "None"] for e in not_empty)
            if valid:
                ret.append([str(getattr(o, v)).strip() for v in values])
        return ret

# Function to read BIOS ACPI table
    def get_acpi_table(tableID):
        try:
            FirmwareTableProviderSignature = ctypes.wintypes.DWORD(1094930505)  # 'ACPI'
            FirmwareTableID = ctypes.wintypes.DWORD(tableID)
            size = ctypes.windll.kernel32.GetSystemFirmwareTable(FirmwareTableProviderSignature, FirmwareTableID, None, 0)
            buffer = ctypes.create_string_buffer(size)
            ctypes.windll.kernel32.GetSystemFirmwareTable(FirmwareTableProviderSignature, FirmwareTableID, buffer, size)
            return buffer.raw
        except:
            return b""


    # WMI objects
    print("[*] Collecting system info. Please wait...\n")
    wmi_obj = wmi.WMI()
    wmi_obj2 = wmi.WMI(moniker="//./root/wmi")

    # Hardware info
    sys_manufacturer = wmi_obj.Win32_ComputerSystem()[0].Manufacturer
    sys_product = wmi_obj.Win32_ComputerSystem()[0].Model
    cpu_list = wmi_obj.Win32_Processor()
    ram_mb = str(int(wmi_obj.Win32_OperatingSystem()[0].TotalVisibleMemorySize) // 1024) + " MB"
    disk_list = wmi_obj.Win32_DiskDrive()
    gpu_list = wmi_obj.Win32_VideoController()

    # Display info
    try:
        display_list = wmi_obj2.query("SELECT MaxHorizontalImageSize,MaxVerticalImageSize FROM WmiMonitorBasicDisplayParams")
    except:
        display_list = []

    # Software info
    os_name = wmi_obj.Win32_OperatingSystem()[0].Name.split("|")[0]
    bios_lic = get_acpi_table(1296323405)
    if bios_lic:
        bios_lic = bios_lic[56:].decode("utf-8", errors="ignore")
    else:
        bios_lic = "Not Found"

    # Display gathered info
    print("=== HARDWARE INFORMATION ===")
    print(f"SYSTEM MANUFACTURER: {sys_manufacturer}")
    print(f"SYSTEM PRODUCT: {sys_product}")

    for cpu in get_objects(cpu_list, ["Name"], ["Name"]):
        print(f"CPU: {cpu[0]}")

    print(f"RAM: {ram_mb}")

    for disk in get_objects(disk_list, ["Model", "Size"], ["Model", "Size"]):
        size_gb = int(disk[1]) // (1024**3)
        print(f"DISK: {disk[0]} | SIZE: {size_gb} GB")

    for gpu in get_objects(gpu_list, ["Name", "AdapterRAM"], ["Name", "AdapterRAM"]):
        vram_mb = int(gpu[1]) // (1024**2)
        print(f"GPU: {gpu[0]} | VIDEO RAM: {vram_mb} MB")

    for display in get_objects(display_list, ["MaxHorizontalImageSize", "MaxVerticalImageSize"], ["MaxHorizontalImageSize", "MaxVerticalImageSize"]):
        try:
            x_inch = float(display[0]) / 2.54
            y_inch = float(display[1]) / 2.54
            diag = round(math.sqrt(x_inch**2 + y_inch**2), 1)
            print(f"DISPLAY SIZE: {diag} inches")
        except:
            continue

    print("\n=== SOFTWARE INFORMATION ===")
    print(f"OS: {os_name}")
    print(f"BIOS LICENSE KEY: {bios_lic}")


#Main Menu For All 
def main_menu():
    print("""
 __          ___         __  __                                                   _   
 \ \        / (_)       |  \/  |                                                 | |  
  \ \  /\  / / _ _ __   | \  / | __ _ _ __   __ _  __ _  ___ _ __ ___   ___ _ __ | |_ 
   \ \/  \/ / | | '_ \  | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '_ ` _ \ / _ \ '_ \| __|
    \  /\  /  | | | | | | |  | | (_| | | | | (_| | (_| |  __/ | | | | |  __/ | | | |_ 
     \/  \/   |_|_| |_| |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_| |_| |_|\___|_| |_|\__|
                                                   __/ |                              
  ____           _____                            |___/  _                            
 |  _ \         / ____|                           | | \ | |                           
 | |_) |_   _  | (___   __ _ _   _ _   _  __ _  __| |  \| |                           
 |  _ <| | | |  \___ \ / _` | | | | | | |/ _` |/ _` | . ` |                           
 | |_) | |_| |  ____) | (_| | |_| | |_| | (_| | (_| | |\  |                           
 |____/ \__, | |_____/ \__,_|\__, |\__, |\__,_|\__,_|_| \_|                           
         __/ |                __/ | __/ |                                             
        |___/                |___/ |___/                                              

    """)
    admin()
    relaunch_as_admin()
    print("1. Manage USers")
    print("2. Apply BEst Cyber Policy for Computers (MDM) (Note: Beta)")
    print("3. Get System Info")
    choose = int(input("Enter Your Number : "))

    if choose == 1:
        user_management()
    elif choose == 2:
        Menu_Cyber()
    elif choose == 3:
        System_info()
    else:
        print("Invaild Input")

main_menu()
