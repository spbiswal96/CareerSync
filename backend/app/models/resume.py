from pydantic import BaseModel


class ExperienceEntry(BaseModel):
    raw_text: str


class EducationEntry(BaseModel):
    raw_text: str


class ParsedResume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    summary: str | None = None
    skills: list[str] = []
    experience: list[ExperienceEntry] = []
    education: list[EducationEntry] = []
    certifications: list[str] = []
    projects: list[str] = []
    raw_text: str