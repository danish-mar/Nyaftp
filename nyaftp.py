import ftplib
import getpass
import os
import time
from tqdm import tqdm
import colorama
from colorama import Fore, Style
import os
is_connected = False

help = f"""
{Fore.MAGENTA}Nyaaa~ Here's how to use me!

get <filename> -- fetches a file fwom the servewr
cd <path> -- changed the dir to path nya~
ls <path> -- lists the files in path owo
push <local_filename> -- push a file to the server fwom local file system uwu
tdownload <local_filename> -- same as get but with speed experimental
pwd -- prints the workin directorw 
help -- prints this message nyaa~

{Style.RESET_ALL}
"""
chelp = f"""{Fore.CYAN}Nyaaa~ Here's how to use me!:
{Style.BRIGHT}connect {Style.RESET_ALL}{Fore.CYAN}<host> -- connect to the servewr
{Style.BRIGHT}anonConnect {Style.RESET_ALL}{Fore.CYAN}<host> -- connect to the server anonymously
{Style.BRIGHT}disconnect {Style.RESET_ALL}{Fore.CYAN}<host> -- disconnect active connections
{Style.BRIGHT}exit {Style.RESET_ALL}{Fore.CYAN} -- exits nyaaa~
{Style.RESET_ALL}
"""
host_history = []

def history():
    print(f"{Fore.MAGENTA}---Peviously connected hosts---{Style.RESET_ALL}")
    for i in host_history:
        print(i)

def hist_connect(index):
        try:
            is_connected = True
            host = host_history[index]
            username = input("username:")
            password = getpass.getpass("Password:")
            ftp = ftplib.FTP(host,username,password)
            print(f"Connected to {host}")
            is_connected = True
            print(ftp.getwelcome())
            main()
        except ftplib.error_perm:
            print(f"{Fore.RED}Authentication failed please check password{Style.RESET_ALL}")
        except ftplib.error_proto:
            print(f"{Fore.RED}Protocol error{Style.RESET_ALL}")
        except ftplib.error_temp:
            print(f"{Fore.RED}Temporary error{Style.RESET_ALL}")
        except ConnectionRefusedError:
            print(f"{Fore.RED} Connection Refused by the server {Style.RESET_ALL}")
        except IndexError:
            print(f"{Fore.RED}World starts from 0 not 1{Style.BRIGHT}")
def bye():
    print(f"{Fore.RED}Byee~{Style.RESET_ALL}")
    exit(0)

def byte2mb(bytes):
    xbyte = int(bytes)
    return xbyte / 1000000

def upload_file(filename, path):
    if path == '':
        path = '.'
    try:
        ftp.storbinary(f"STOR {filename}", open(filename, "rb"))
        filesize = os.path.getsize(filename)
        print(f"File {filename} uploaded {byte2mb(filesize)}")
    except FileNotFoundError:
        print(f"File {filename} does not exist")
    except PermissionError:
        print(f"Permission denied")
    except KeyboardInterrupt:
        print("Interrupted")



def get_file(filename, verbose=True):
    try:
        with open(filename, 'wb') as fd:
            total = ftp.size(filename)

            with tqdm(total=total,unit='B', unit_scale=True, unit_divisor=1024, disable=not verbose) as pbar:
                def cb(data):
                    pbar.update(len(data))
                    fd.write(data)

                ftp.retrbinary('RETR {}'.format(filename), cb)
                
            filesize = byte2mb(total)
            print(f"File {filename} downloaded {byte2mb(filesize)}")
    except FileNotFoundError:
        print(f"File {filename} does not exist")
    except PermissionError:
        print(f"Permission denied")
    except ConnectionAbortedError:
        print(f"{Fore.RED}Connection Error!{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print("Interrupted")



def ls_files(path):
    try:
        ftp.cwd(path)
        files = ftp.nlst()
        for file in files:
            print(file)
    except ftplib.error_perm:
        print("Permission denied")
    except ftplib.error_proto:
        print("Protocol error")
    except ftplib.error_temp:
        print("Temporary error")



def cd(path):
    try:
        ftp.cwd(path)
    except ftplib.error_perm:
        print("Permission denied")
    except ftplib.error_proto:
        print("Protocol error")
    except ftplib.error_temp:
        print("Temporary error")

def get_current_dir():
    return ftp.pwd()


def main():
    while True:
        try:
            cmd = input(f"srv[{get_current_dir()}]:")
            if cmd == "help":
                print(help)
            elif cmd.startswith("ls"):
                ls_files(cmd[3:])
            elif cmd.startswith("cd"):
                cd(cmd[3:])
            elif cmd.startswith("get"):
                get_file(cmd[4:])
            elif cmd.startswith("push"):
                upload_file(cmd[5:], cmd[3:])
            elif cmd == 'pwd':
                print(get_current_dir())
            elif cmd == "disconnect":
                break
        except KeyboardInterrupt:
            print("Interrupted")
            print("disconnecting...")
            ftp.close()
            print("Disconnected\n")
            exit(0)


while True:
    xin = input(f"{Fore.MAGENTA}NyaFTP>{Style.RESET_ALL}")
    if xin.startswith("connect"):
        try:
            is_connected = True
            host = xin[8:]
            host_history.append(host)
            username = input("username:")
            password = getpass.getpass("Password:")
            ftp = ftplib.FTP(host,username,password)
            print(f"Connected to {host}")
            is_connected = True
            print(ftp.getwelcome())
            main()
        except KeyboardInterrupt:
            print(f"{Fore.RED}Interrupted{Style.RESET_ALL}")
        except ftplib.error_perm:
            print(f"{Fore.RED}Authentication failed please check password{Style.RESET_ALL}")
        except ftplib.error_proto:
            print(f"{Fore.RED}Protocol error{Style.RESET_ALL}")
        except ftplib.error_temp:
            print(f"{Fore.RED}Temporary error{Style.RESET_ALL}")
        except ConnectionRefusedError:
            print(f"{Fore.RED} Connection Refused by the serve {Style.RESET_ALL}")
    elif xin.startswith("anonConnect"):
        try:
            host = xin[12:]
            host_history.append(host)

            print(f"{Fore.CYAN}Trying Anonym connections to {Style.BRIGHT}{host}{Style.RESET_ALL}")
            username = 'anonymous'
            password = 'xyx@xuz.com'
            ftp = ftplib.FTP(host,username,password)
            print(f"Connected to {host}")
            is_connected = True
            print(ftp.getwelcome())
            main()
        except ftplib.error_perm:
            print(f"{Fore.RED}Authentication failed please check password{Style.RESET_ALL}")
        except ftplib.error_proto:
            print(f"{Fore.RED}Protocol error{Style.RESET_ALL}")
        except ftplib.error_temp:
            print(f"{Fore.RED}Temporary error{Style.RESET_ALL}")
        except NameError:
            print(f"{Fore.RED}Usage : anonConnect <host>{Style.RESET_ALL}")
        except AttributeError:
            print(f"{Fore.RED}Usage : anonConnect <host>{Style.RESET_ALL}")
        except ConnectionRefusedError:
            print(f"{Fore.RED}{Style.DIM}{Style.RESET_ALL}{Fore.RED}Error Connection Refused by the serwver {Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"{Fore.RED}Aborted{Style.RESET_ALL}")
    elif xin.startswith("disconnect"):
        if is_connected == False:
            print(f"{Fore.RED}Error Not connected{Style.RESET_ALL}")
        else:
            is_connected = False
            ftp.close()
            print("Disconnected")
    elif xin == "help":
        print(chelp)
    elif xin == 'history':
        history()
    elif xin.startswith('hconnect'):
        host = int(xin[9:])
        hist_connect(host)
    if xin == "exit":
        bye()
    
#taking server details 
# def connect():
#     server = input("Server:")
# #taking user details
#     username = input("Username:")

#     if username == 'anon':
#         username = "Anonymous"
#         password = "xyx@xuz.com"
#         try:
#             ftp = ftplib.FTP(server)
#             ftp.login('anonymous', password)
#             print(f"Connected to {server}")
#             print(ftp.getwelcome())
#             main()
#         except ftplib.error_perm:
#             print("Authentication failed please check password")
#         except ftplib.error_proto:
#             print("Protocol error")
#         except ftplib.error_temp:
#             print("Temporary error")

# password = getpass.getpass(prompt="Password:")

# print(f"Connecting to {server}")

# try:
#     ftp = ftplib.FTP(server)
#     ftp.login(server, password, username)
#     print(f"Connected to {server}")
#     print(ftp.getwelcome())
#     main()
# except ftplib.error_perm:
#     print("Authentication failed please check password")
# except ftplib.error_proto:
#     print("Protocol error")
# except ftplib.error_temp:
#     print("Temporary error")

