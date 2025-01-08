# neuromeka_lib/install.py

import socket
import subprocess
import shutil
import os
import sys
import urllib.request
import zipfile

def main():
    hostname = socket.gethostname()

    print("Download library files...")
    if hostname == 'STEP3':
        download_url = 'http://s3.ap-northeast-2.amazonaws.com/download.neuromeka.com/Library/lib_step3.zip'
        target_dir = '/opt/3rdparty_lib/lib/'
    elif hostname == 'Step-TP':
        download_url = 'http://s3.ap-northeast-2.amazonaws.com/download.neuromeka.com/Library/lib_step2.zip'
        target_dir = '/opt/3rdparty_libs/lib/'
    else:
        sys.exit(1)

    download_dir = os.path.join('.', 'downloaded_libs')

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    zip_filename = os.path.join(download_dir, 'libs.zip')
    urllib.request.urlretrieve(download_url, zip_filename)
    print(f"Done downloading {hostname} library files...")

    print('Start Unzip')
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(download_dir)
    print('Unzip complete')

    print(f"download_dir: {download_dir}")

    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    
    print('Changing permissions')
    subprocess.run(f'echo root | sudo -S chmod -R 777 {download_dir}', shell=True, check=True)
    print('Permissions changed')

    print('Copying files')
    subprocess.run(f"echo root | sudo -S cp -r {os.path.join(download_dir, '.')} {target_dir}", shell=True, check=True)
    print("Copy complete.")

    print('Running ldconfig')
    subprocess.check_call(['ldconfig'])
    print('ldconfig complete')

if __name__ == '__main__':
    main()
