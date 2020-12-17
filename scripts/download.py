"""
A short script for downloading the alltheplaces data to 
the data directory.
"""
import requests
import tarfile
import os


def download_extract_tar(path: str, url: str):
    os.makedirs(path, exist_ok=True)

    print(f'downloading data from {url}')
    res = requests.get(url)
    res.raise_for_status()
    tar_path = path + '.tar.gz'
    print(f'writing data to {tar_path}')
    with open(tar_path, 'wb') as f:
        f.write(res.content)

    print(f'extracting to {path}')
    with tarfile.open(tar_path) as tar_file:
        tar_file.extractall(path)

    print(f'removing {tar_path}')
    os.remove(tar_path)


if __name__ == '__main__':
    data_directory = "data/alltheplaces"
    data_url = 'https://data.alltheplaces.xyz/runs/2020-12-09-14-42-39/output.tar.gz'
    
    download_extract_tar(data_directory, data_url)

    output_directory = f'{data_directory}/output'
    print(f'moving files from {output_directory} to {data_directory}')
    for file_name in os.listdir(output_directory):
        os.rename(f'{output_directory}/{file_name}', f'{data_directory}/{file_name}')
    os.rmdir(output_directory)


