import subprocess

def download_from_ftp(url, file_path):
    command = ['axel', '-n', '10', '--output', file_path, url]
    subprocess.run(command, check=True)