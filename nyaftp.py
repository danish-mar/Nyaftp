import ftplib
import getpass
import os
import time
from tqdm import tqdm
from colorama import Fore, Style
import os

def greet(to_exec):
    if to_exec == False:
        print(f"{Fore.MAGENTA}Welcome to NyaaFTP~{Style.RESET_ALL}")
    else:
        text = pyfiglet.figlet_format("nyaFTP~", font='slant')
        print(f"{Fore.MAGENTA}{text}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}=====+ NyaFTP client V0.2 +====={Style.RESET_ALL}")
try:
    import pyfiglet
    estyle = True
except ImportError:
    estyle = False

greet(estyle)

is_connected = False

help = f"""
{Fore.MAGENTA}Nyaaa~ Here's how to use me!

get <server_filename> -- fetches a file fwom the servewr
cd <server_path> -- changed the dir to path nya~
ls <server_path> -- lists the files in path owo
push <local_filename> -- push a file to the server fwom local file system uwu
tdownload <local_filename> -- same as get but with speed experimental
pwd -- prints the workin directorw
rm <server_filename> -- remove a file/folder from the server 
mkdir <server_foldername> -- create a directory on the server
lkdir <local_foldername> -- create a new dir on local filesystem
lls <local_fodlername> -- list local files or folder
lrm <local_filename> -- removes a local file or folder
lcd <local_filename> -- changes local dir
lpwd -- prints the local working directory
clear -- clears the terminal


{Style.RESET_ALL}
"""
def uwufy(text):
    uwufied = text.replace("r", "w").replace("l", "w") + " (´・ω・`)"
    return uwufied

chelp = f"""{Fore.CYAN}Nyaaa~ Here's how to use me!:
{Style.BRIGHT}connect {Style.RESET_ALL}{Fore.CYAN}<host> -- connect to the servewr
{Style.BRIGHT}anonConnect {Style.RESET_ALL}{Fore.CYAN}<host> -- connect to the server anonymously
{Style.BRIGHT}disconnect {Style.RESET_ALL}{Fore.CYAN}<host> -- disconnect active connections
{Style.BRIGHT}exit {Style.RESET_ALL}{Fore.CYAN} -- exits nyaaa~
{Style.BRIGHT}ls {Style.RESET_ALL}{Fore.CYAN}<path> -- list files and folders in current dir
{Style.BRIGHT}rm {Style.RESET_ALL}{Fore.CYAN}<name> -- removes file/folder from current dir
{Style.BRIGHT}cd {Style.RESET_ALL}{Fore.CYAN}<name> -- changes the current directory to another directory
{Style.BRIGHT}pwd {Style.RESET_ALL}{Fore.CYAN} -- prints working directory
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

def copy_file(filename, destination):
    try:
        ftp.rename(filename,destination)
    except ftplib.error_perm:
        print(f"{Fore.RED}Permission denied{Style.RESET_ALL}")
    except ftplib.error_proto:
        print(f"{Fore.RED}Protocol error{Style.RESET}")
    except:
        print(f"{Fore.RED}An unexpected error occoured{Style.RESET_ALL}")

def ftp_rm(name):
    try:
        ftp.delete(name)
    except ftplib.error_perm:
        print(f"{Fore.RED}Permission denied{Style.RESET_ALL}")
    except ftplib.error_proto:
        print(f"{Fore.RED}Protocol error{Style.RESET}")
    except:
        print(f"{Fore.RED}An unexpected error occoured{Style.RESET_ALL}")

def ftp_mkdir(name):
    try:
        ftp.mkd(name)
    except ftplib.error_perm:
        print(f"{Fore.RED}Permission denied{Style.RESET_ALL}")
    except ftplib.error_proto:
        print(f"{Fore.RED}Protocol error{Style.RESET}")
    except:
        print(f"{Fore.RED}An unexpected error occoured{Style.RESET_ALL}")


def list_files(path="."):
    """
    Lists the files and directories in the given path. If no path is supplied, it lists the files and directories in the current directory.
    Applies color to directories and files in the output.
    """
    if not os.path.exists(path):
        print(f"Path {path} does not exist.")
        return
    
    if os.path.isdir(path):
        names = os.listdir(path)
        for i in range(len(names)):
            name = names[i]
            if os.path.isdir(os.path.join(path, name)):
                print(f"{Fore.BLUE}{name}{Style.RESET_ALL}", end="  ")
            else:
                print(f"{Fore.GREEN}{name}{Style.RESET_ALL}", end="  ")
            if i == len(names) - 1:
                print()
    else:
        print(f"{Fore.GREEN}{path}{Style.RESET_ALL}")
# def list_files(path="."):
#     if not os.path.exists(path):
#         print(f"Path {path} does not exist.")
#         return
    
#     if os.path.isdir(path):
#         for name in os.listdir(path):
#             if os.path.isdir(os.path.join(path, name)):
#                 print(f"{Fore.BLUE}{name}{Style.RESET_ALL}")
#             else:
#                 print(f"{Fore.GREEN}{name}{Style.RESET_ALL}")
#     else:
#         print(f"{Fore.GREEN}{path}{Style.RESET_ALL}")


def upload_file(filename, path):
    if path == '':
        path = "."
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

def local_create_dir(path):
    try:
        os.mkdir(path)
    except os.error:
        print(f"{Fore.RED}OS error!{Style.RESET}")

def local_delete_dir(path):
    try:
        if os.path.isdir(path):
            os.rmdir(path)
            print(uwufy(f"Directory {path} deleted"))
        elif os.path.isfile(path):
            os.remove(path)
            print(uwufy(f"File {path} deleted"))
    except os.error:
        print(f"{Fore.RED}OS error!{Style.RESET_ALL}")

def current_path():
    if is_connected:
        return ftp.pwd()
    else:
        return os.getcwd()

def cd(path):
    try:
        ftp.cwd(path)
    except ftplib.error_perm:
        print("Permission denied")
    except ftplib.error_proto:
        print("Protocol error")
    except ftplib.error_temp:
        print("Temporary error")


def local_change_dir(path):
    try:
        os.chdir(path)
    except os.error:
        print(f"{Fore.RED}OS error!{Style.RESET}")

def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')

# For Unix-based systems (Linux, macOS, etc.)
    else:
        _ = os.system('clear')

def main():
    while True:
        global is_connected
        try:
            cmd = input(f"{Fore.LIGHTMAGENTA_EX}srv[{current_path()}]@[{Style.BRIGHT}{host}]]:{Style.RESET_ALL}")
            if cmd == "help":
                print(help)
            elif cmd.startswith("ls"):
                ls_files(cmd[3:])
            elif cmd.startswith("lls"):
                xpath = cmd[4:]
                if not xpath:
                    xpath = "."
                if not os.path.exists(xpath):
                    print(f"Path {xpath} does not exist.")
                else:
                    list_files(xpath)
            elif cmd.startswith("lpwd"):
                print(f'{os.getcwd()}')
            elif cmd.startswith("lcd"):
                    xpath = cmd[4:]
                    if not xpath:
                        xpath = "."
                    if not os.path.exists(xpath):
                        print(uwufy(f"Path {xpath} does not exist."))
                    else:
                        local_change_dir(xpath)
            elif cmd.startswith("lkdir"):
                local_create_dir(cmd[5:])
            elif cmd.startswith("rm"):
                ftp_rm(cmd[3:])
            elif cmd.startswith("mkdir"):
                ftp_mkdir(cmd[5:])
            elif cmd.startswith("cd"):
                cd(cmd[3:])
            elif cmd.startswith("get"):
                get_file(cmd[4:])
            elif cmd.startswith("push"):
                upload_file(cmd[5:], cmd[3:])
            elif cmd == 'pwd':
                print(current_path())
            elif cmd.startswith("lrm"):
                local_delete_dir(cmd[4:])
            elif cmd == 'clear':
                clear_screen()
            elif cmd == "disconnect":
                is_connected = False
                break
        except KeyboardInterrupt:
            print("Interrupted")
            print("disconnecting...")
            ftp.close()
            is_connected = False
            print("Disconnected\n")
            break


while True:
    xin = input(f"{Fore.MAGENTA}NyaFTP[{current_path()}]>{Style.RESET_ALL}")
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
    elif xin.startswith('ls'):
        xpath = xin[3:]
        if not xpath:
            xpath = "."
        if not os.path.exists(xpath):
            print(f"Path {xpath} does not exist.")
        else:
            list_files(xpath)
    elif xin.startswith('cd'):
        xpath = xin[3:]
        if not xpath:
            xpath = "."
        if not os.path.exists(xpath):
            print(uwufy(f"Path {xpath} does not exist."))
        else:
            local_change_dir(xpath)
    elif xin.startswith('mkdir'):
        xpath = xin[6:]
        if not xpath:
            print(uwufy(f"{Fore.RED}mkdir <filename> --creates a new empty directory{Style.RESET_ALL}"))
        if os.path.exists(xpath):
            print(uwufy(f"{Fore.RED}Path {xpath} already exists{Style.RESET_ALL}"))
        else:
            local_create_dir(xpath)
    elif xin.startswith('rm'):
        xpath = xin[3:]
        if not xpath:
            print(uwufy(f"{Fore.RED}rm <filename> --deletes a directory{Style.RESET_ALL}"))
        else:
            local_delete_dir(xpath)
    elif xin == "banner":
        greet(estyle)
    if xin == "exit":
        bye()
    elif xin == "clear":
        clear_screen()
    elif xin == "":
        print(f"{Fore.RED}Command {xin} not found{Style.RESET_ALL}")
    
    
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

