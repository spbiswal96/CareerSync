from fastapi import APIRouter, HTTPException, UploadFile

from app.core.logging import get_logger
from app.schemas.resume import ResumeUploadResponse
from app.utils.file_utils import is_allowed_extension, save_upload

logger = get_logger(__name__)
router = APIRouter(prefix="/api/resume", tags=["resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    if not is_allowed_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Allowed: .pdf, .docx, .txt",
        )

    try:
        resume_id, saved_path, size_bytes = await save_upload(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    logger.info("Resume uploaded: resume_id=%s size_bytes=%d", resume_id, size_bytes)

    return ResumeUploadResponse(
        resume_id=resume_id,
        filename=file.filename,
        size_bytes=size_bytes,
    )