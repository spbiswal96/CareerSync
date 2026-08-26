import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import get_settings

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
TEMP_DIR = Path("temp")


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def is_allowed_extension(filename: str) -> bool:
    return get_extension(filename) in ALLOWED_EXTENSIONS


def ensure_temp_dir() -> Path:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    return TEMP_DIR


async def save_upload(file: UploadFile) -> tuple[str, Path, int]:
    """Save an uploaded file to the temp directory.

    Returns (resume_id, saved_path, size_bytes).
    """
    settings = get_settings()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024

    ensure_temp_dir()
    resume_id = str(uuid.uuid4())
    extension = get_extension(file.filename or "")
    saved_path = TEMP_DIR / f"{resume_id}{extension}"

    size_bytes = 0
    with open(saved_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            size_bytes += len(chunk)
            if size_bytes > max_bytes:
                f.close()
                saved_path.unlink(missing_ok=True)
                raise ValueError(f"File exceeds maximum size of {settings.max_upload_size_mb}MB")
            f.write(chunk)

    if size_bytes == 0:
        saved_path.unlink(missing_ok=True)
        raise ValueError("Uploaded file is empty")

    return resume_id, saved_path, size_bytes