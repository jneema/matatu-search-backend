import cloudinary          # type: ignore
import cloudinary.uploader  # type: ignore
from fastapi import UploadFile


def _configure() -> None:
    from app.core.config import settings
    cloudinary.config(  # type: ignore
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


async def upload_image(file: UploadFile, folder: str = "matatus") -> str:
    _configure()
    contents = await file.read()
    result = cloudinary.uploader.upload(  # type: ignore
        contents,
        folder=folder,
        resource_type="image",
    )
    return result["secure_url"]
