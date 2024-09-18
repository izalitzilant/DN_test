import asyncio
import datetime
import os
from datetime import datetime, timezone

import aiofiles
from hurry.filesize import size
from fastapi import APIRouter, Depends, Response, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse

from ..dependencies import get_filestore_dir


router = APIRouter(prefix="/files",
                   tags=["files"],)

def parse_fstore_object(filename: str, file_path: str) -> str:
    """
    Parse the object from the file representation to rest-like dto object with readable format.
    """
    fstore_obj = {}
    stats = os.stat(file_path)
    fstore_obj[filename] = filename = {"obj size": size(stats.st_size),
                             "access time": datetime.fromtimestamp(stats.st_atime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                             "inode number": stats.st_ino,
                             "creation time": datetime.fromtimestamp(stats.st_birthtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                             "user ID": stats.st_uid}
    return fstore_obj
    
@router.get("/")
async def get_fstore_objects_info(response: Response, fstore_dir: str = Depends(get_filestore_dir)) -> list:
    """
    Read filestore directory and return the list of objects info as dict.
    """
    fstr_dir_list = []
    for x in os.listdir(fstore_dir):
        file_path = '/'.join([fstore_dir, x])
        fstr_dir_list.append(parse_fstore_object(x, file_path))
    if len(fstore_dir) == 0:
        response.status_code = status.HTTP_204_NO_CONTENT

    return fstr_dir_list

@router.get("/{filename}", responses={204: {"description": "The request was successfull but object wasn't found"}})
async def get_fstore_object_info(filename:str, response: Response, fstore_dir: str = Depends(get_filestore_dir)) -> dict:
    """
    Read filestore directory and return the list of object info.
    """
    fstr_dir = {}
    file_path = '/'.join([fstore_dir, filename])
    if os.path.exists(file_path):
        fstr_dir[filename] = (parse_fstore_object(filename, file_path))
        return fstr_dir
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"result": "No such file exists"}

@router.get("/download/{filename}", response_class=FileResponse)
async def download_object_from_fstore(filename: str, response: FileResponse, fstore_dir: str = Depends(get_filestore_dir)) -> FileResponse:
    """
    Download file from the filestore by filename.
    
    - **filename**: filename
    """
    file_path = '/'.join([fstore_dir, filename])
    if os.path.exists(file_path):
        # def iterfile():s
        #     with open(file_path, "rb") as f:
        #         yield from f
        # return StreamingResponse(iterfile())
        return FileResponse(path=file_path, media_type="application/octet-stream", filename=filename)
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
    return response

@router.post("/upload", status_code=200)
async def upload_object_to_fstore(in_file: UploadFile, fstore_dir: str = Depends(get_filestore_dir)) -> dict:
    """
    Upload the file into the filestore.

    - **in_file**: file to accept
    """   
    out_file_path = '/'.join([fstore_dir, in_file.filename])

    async with aiofiles.open(out_file_path, 'wb') as out_file:
        content = await in_file.read()
        await out_file.write(content)
    
    return {"result": "OK"}

@router.post("/uploadfiles", status_code=200)
async def upload_object_to_fstore(files: list[UploadFile], fstore_dir: str = Depends(get_filestore_dir)) -> dict: 
    """
    Upload the file into the filestore.

    - **in_file**: file to accept
    """
    async def write_to_file(file: UploadFile):
        out_file_path = '/'.join([fstore_dir, file.filename])
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
    
    await asyncio.gather(*[write_to_file(file) for file in files])
    
    return {"result": "OK"}

@router.delete("/{filename}", status_code=200)
async def upload_object_to_fstore(filename: str, fstore_dir: str = Depends(get_filestore_dir)) -> dict: 
    """
    Upload the file into the filestore.

    - **in_file**: file to accept
    """
    out_file_path = '/'.join([fstore_dir, filename])
    os.remove(out_file_path)
    
    return {"result": "OK"}

