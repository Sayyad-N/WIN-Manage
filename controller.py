#Code Written By SayyadN
#Code For Education
#Date : 16-8-2025

#Import Required Libs
import socket

ip_server = input("Please Enter Ip Of DEvice -> ")
PORT = 5050

def cmd_send(cmd):
    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.connect((ip_server ,PORT ))
        s.sendall(cmd.encode())
        respone = s.recv(1024).decode()

if __name__ == "__main__":
    print("🔒 MDM Controller")
    print("[1] قفل تطبيق")
    print("[2] تعطيل USB")
    print("[3] إغلاق الجهاز")
    print("[4] عرض البرامج ")

    choice = input("اختر: ")
    if choice == "1":
        app = input("اسم التطبيق (مثال chrome.exe): ")
        cmd_send(f"block {app}")
    elif choice == "2":
        cmd_send("usb_off")
    elif choice == "3":
        cmd_send("shutdown")
    elif choice =="4":
        cmd_send("list_apps")