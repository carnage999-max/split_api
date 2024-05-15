import time
import os
from fastapi import FastAPI, File, APIRouter, UploadFile, HTTPException, Response, Request
from fastapi.responses import FileResponse, HTMLResponse
import shutil
from typing import List
from pathlib import Path

from scripts import csv_to_chunk, json_to_chunk


split_router = APIRouter()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
csv_zip_folder_name = ""
json_zip_folder_name = ""
json_folder_path_ = ""
j_files = list()
json_zip_file_name = ""
csv_folder_path_ = ""
c_files = list()
csv_zip_file_name = ""


@split_router.post('/csv')
def split_csv(file: UploadFile, num_lines: int, response:Response):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Upload only csv files")
    try:
        with open(f"{BASE_DIR}/uploaded_files/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    csv_to_chunk.filename = file.filename
    csv_to_chunk.number_of_lines = num_lines
    csv_to_chunk.file_size = file.size
    csv_to_chunk.main()
    global csv_zip_folder_name
    csv_zip_folder_name = "".join(csv_to_chunk.newpath.split("/")[-1])
    csv_to_chunk.remove_uploaded_file()
    global csv_folder_path_, c_files, csv_zip_file_name
    csv_folder_path_ = os.path.join(BASE_DIR, "files", "csv", csv_zip_folder_name)
    c_files = [i for i in os.listdir(csv_folder_path_) if os.path.isfile(os.path.join(csv_folder_path_, i))]
    csv_zip_file_name = "".join(c_files)
    download_zip_path = os.path.join(csv_folder_path_,csv_zip_file_name)
    if Path(download_zip_path).is_file():
        return FileResponse(download_zip_path, filename=csv_zip_file_name, media_type="application/zip")
    else:
        response.status_code = 404
        return {
            "error": "File not found"
        }    
@split_router.post("/json")
def split_json(file:UploadFile, num_lines:int):
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Upload only a JSON file")
    try:
        with open(f"{BASE_DIR}/uploaded_files/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    json_to_chunk.filename = file.filename
    json_to_chunk.num_lines = num_lines
    json_to_chunk.file_size = file.size
    json_to_chunk.main()
    global json_folder_path_, j_files, json_zip_file_name
    global json_zip_folder_name
    json_zip_folder_name = "".join(json_to_chunk.newpath.split("/")[-1])
    json_to_chunk.remove_uploaded_file()
    json_folder_path_ = os.path.join(BASE_DIR, "files", "json", json_zip_folder_name)
    j_files = [i for i in os.listdir(json_folder_path_) if os.path.isfile(os.path.join(json_folder_path_, i))]
    json_zip_file_name = "".join(j_files)
    download_zip_path = os.path.join(json_folder_path_, json_zip_file_name)
    if Path(download_zip_path).is_file():
        return FileResponse(download_zip_path, filename=json_zip_file_name, media_type="application/zip")
    else:
        return {
            "error": "File not found"
        }