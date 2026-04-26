from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter(prefix="/upload", tags=["Upload"])
UPLOAD_DIR = "uploads"

@router.post("", summary="Upload files")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"url": f"/{file_path}"}