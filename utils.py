import subprocess
import nbformat

def download_from_ftp(url, file_path):
    '''Function to download files from an ftp server using the axel command in a subprocess'''
    command = ['axel', '-n', '10', '--output', file_path, url]
    subprocess.run(command, check=True)

def extract_notebook_code(notebook_path: str, output_path: str, cells_to_extract: list):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    code_to_write = ""
    for cell_index in cells_to_extract:
        cell = nb.cells[cell_index]
        if cell.cell_type == 'code':
            code_to_write += cell.source + '\n\n'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(code_to_write)

    print(f"Extracted code has been written to {output_path}")