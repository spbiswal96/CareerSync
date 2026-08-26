from fastapi import APIRouter
from pydantic import BaseModel

from app.services.keyword_engine import extract_keywords

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


class KeywordExtractRequest(BaseModel):
    job_description: str


@router.post("/extract-keywords-test")
async def extract_keywords_test(request: KeywordExtractRequest):
    """TEMPORARY diagnostic route."""
    return extract_keywords(request.job_description)