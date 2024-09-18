import os
from typing import Dict, List, Literal, Union
from enum import Enum

import aiofiles
import typer
import asyncio
import aiohttp
from tqdm.asyncio import tqdm
from rich.console import Console
from rich.tree import Tree

console = Console()


app = typer.Typer(name="files", help="to manage the filestore objects")

class Process(Enum):    
    list = 1
    download = 2
    upload = 3

async def async_download(url: str, filename: str, timeout=60):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}/{filename}", timeout=60) as response:
            if response.status == 200:
                total_size = int(response.headers.get('content-length', 0))
                chunk_size = 8192
                progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
                async with aiofiles.open(''.join(['./', filename]), 'wb') as file:
                    while True:
                        try:
                            chunk = await asyncio.wait_for(response.content.read(chunk_size), timeout=timeout)
                        except asyncio.TimeoutError:
                            print(f"Timeout error while processing object. Retrying...")
                            continue
                        if not chunk:
                            break
                        await file.write(chunk)
                        progress_bar.update(len(chunk))
                progress_bar.close()
                print(f'File {filename} processed succesfully!')
            else:
                print(f'Error processing {filename}: {response.status}')

async def async_upload(url: str, file_path: str, timeout: int = 60):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data={'in_file': open(file_path, 'rb')}, timeout=timeout) as resp:
                if resp.status == 200:
                    total = resp.headers.get('content-length', 0)
                    total = int(total) if total else 0
                    with tqdm(total=total, unit='iB', unit_scale=True, unit_divisor=1024, desc=f"Uploading {file_path}") as progress:
                        while True:
                            try:
                                chunk = await asyncio.wait_for(resp.content.read(8192), timeout=timeout)
                            except asyncio.TimeoutError:
                                print(f"Timeout error while processing {file_path}. Retrying...")
                                continue
                            if not chunk:
                                break
                            progress.update(len(chunk))
                    print(f'File {file_path} uploaded successfully!')
                else:
                    text = await resp.text()
                    print(f'Error uploading {file_path}: {resp.status} - {resp.reason}\nResponse: {text}')
        except aiohttp.ClientError as e:
            print(f'Error uploading {file_path}: {e}')

async def async_list(url: str, timeout: int = 60) -> List[Dict[str, Dict[str, str]]]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=timeout) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    raise Exception(f'Error listing files: {resp.status} - {resp.reason}')
        except aiohttp.ClientError as e:
            raise Exception(f'Error listing files: {e}')
        
async def async_remove(url: str, timeout: int = 60) -> List[Dict[str, Dict[str, str]]]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=timeout) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    raise Exception(f'Error listing files: {resp.status} - {resp.reason}')
        except aiohttp.ClientError as e:
            raise Exception(f'Error listing files: {e}')
        
@app.command()
def download(obj_name: str) -> str:
    """
    download object from filestore
    """
    FSTORE_URL = os.getenv('FSTORE_URL')
    url_path = '/'.join([FSTORE_URL, 'files', 'download'])
    return asyncio.run(async_download(url_path, obj_name))

@app.command()
def upload(path_to_obj: str) -> str:
    """
    upload object to filestore
    """
    FSTORE_URL = os.getenv('FSTORE_URL')
    url_path = '/'.join([FSTORE_URL, 'files', 'upload'])
    return asyncio.run(async_upload(url_path, path_to_obj))

@app.command()
def list() -> str:
    """
    List files in the filestore
    """
    FSTORE_URL = os.getenv('FSTORE_URL')
    url_path = '/'.join([FSTORE_URL, 'files'])
    data: List = asyncio.run(async_list(url_path))
    if data:
        root = Tree("Files in the Filestore")
        for obj in data:
            print(obj)
            print()
        return data
    else:
        print("No objects")

