import os
import sys
import time
import scp
import paramiko
import argparse


def upload_save(ssh, scp, pwd, local_path, server_path):
    print("Uploading Server Save File...")

    print("Stopping factorio.service...")
    cmd = "echo " + pwd + " | sudo -S systemctl stop factorio.service"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(3)

    print("Uploading save zip file via SCP...")
    scp.put(local_path, server_path)

    print("Restarting factorio.service...")
    cmd = "echo " + pwd + " | sudo -S systemctl restart factorio.service"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(3)

    cmd = "echo " + pwd + " | sudo -S systemctl status factorio.service --no-pager"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("".join(stdout.readlines()))

    stdin, stdout, stderr = ssh.exec_command("ls -al /opt/factorio/saves/")
    print("".join(stdout.readlines()) + "\nUploading Complete!")


def download_save(ssh, scp, pwd, local_path, server_path):
    print("Downloading Server Save File...")

    print("Stopping factorio.service...")
    cmd = "echo " + pwd + " | sudo -S systemctl stop factorio.service"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(3)

    print("Downloading save zip file via SCP...")
    scp.get(server_path, local_path)
    time.sleep(3)

    print("Restarting factorio.service...")
    cmd = "echo " + pwd + " | sudo -S systemctl restart factorio.service"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(3)

    cmd = "echo " + pwd + " | sudo -S systemctl status factorio.service --no-pager"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("".join(stdout.readlines()) + "\nDownload Complete!")


def sync_mods(ssh, scp, pwd, local_mod_path, server_mod_path):
    print("Stopping factorio.service...")
    cmd = "echo " + pwd + " | sudo -S systemctl stop factorio.service"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(3)

    print("Uploading mod files via SCP...")
    for item in os.listdir(local_mod_path):
        scp.put(local_mod_path + os.sep + item, server_mod_path + '/' + item)
        time.sleep(3)

    print("Restarting factorio.service...")
    cmd = "echo " + pwd + " | sudo -S systemctl restart factorio.service"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(3)

    cmd = "echo " + pwd + " | sudo -S systemctl status factorio.service --no-pager"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("".join(stdout.readlines()) + "\nRestart Complete!")



def restart(ssh, pwd):
    print("Stopping factorio.service...")
    cmd = "echo " + pwd + " | sudo -S systemctl stop factorio.service"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(3)

    print("Restarting factorio.service...")
    cmd = "echo " + pwd + " | sudo -S systemctl restart factorio.service"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(3)

    cmd = "echo " + pwd + " | sudo -S systemctl status factorio.service --no-pager"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("".join(stdout.readlines()) + "\nRestart Complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-u", "--upload", action="store_true", help="Upload Server Save File")
    parser.add_argument("-d", "--download", action="store_true", help="Download Server Save File")
    parser.add_argument("-m", "--mods", action="store_true", help="Upload Mod Files")
    parser.add_argument("-s", "--start", action="store_true", help="Start Server Factorio.service")
    inputs = parser.parse_args()

    local_save_path = r"F:\Game\Factorio\saves\wonderland.zip"
    server_save_path = r"/opt/factorio/saves/wonderland.zip"

    local_mod_path = r"F:\Game\Factorio\mods\\"
    server_mod_path = r"/opt/factorio/mods/"

    host_ip = "192.168.1.120"
    user = "wolf"
    password = "1234"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host_ip, username=user, password=password, port=22)
    scp = scp.SCPClient(ssh.get_transport())

    if inputs.upload:
        upload_save(ssh, scp, password, local_save_path, server_save_path)
    elif inputs.download:
        download_save(ssh, scp, password, local_save_path, server_save_path)
    elif inputs.mods:
        sync_mods(ssh, scp, password, local_mod_path, server_mod_path)
    elif inputs.start:
        restart(ssh, password)
    elif not inputs.upload and not inputs.download and not inputs.start:
        msg = "Select Function Index:\n[1] Upload Save\n[2] Download Save\n[3] Sync Mods\n[4] Start Server\n"
        input_value = input(msg)
        if input_value == "1":
            upload_save(ssh, scp, password, local_save_path, server_save_path)
        elif input_value == "2":
            download_save(ssh, scp, password, local_save_path, server_save_path)
        elif input_value == "3":
            sync_mods(ssh, scp, password, local_mod_path, server_mod_path)
        elif input_value == "4":
            restart(ssh, password)
        else:
            sys.exit("ERROR: Invalid Input")

    scp.close()
    ssh.close()
    time.sleep(10)
