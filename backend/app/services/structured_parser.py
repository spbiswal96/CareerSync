import re

from app.models.resume import ParsedResume
from app.services.contact_extractor import extract_email, extract_phone
from app.services.section_detector import detect_sections


def parse_resume(raw_text: str) -> ParsedResume:
    sections = detect_sections(raw_text)

    skills = _parse_skills(sections.get("skills", ""))
    experience = _split_entries(sections.get("experience", ""))
    education = _split_entries(sections.get("education", ""))
    certifications = _split_lines(sections.get("certifications", ""))
    projects = _split_lines(sections.get("projects", ""))

    return ParsedResume(
        email=extract_email(raw_text),
        phone=extract_phone(raw_text),
        summary=sections.get("summary") or sections.get("objective") or None,
        skills=skills,
        experience=[{"raw_text": e} for e in experience],
        education=[{"raw_text": e} for e in education],
        certifications=certifications,
        projects=projects,
        raw_text=raw_text,
    )


def _parse_skills(skills_text: str) -> list[str]:
    if not skills_text:
        return []

    parts = re.split(r"[,\n•|/]", skills_text)
    return [p.strip() for p in parts if p.strip()]


def _split_lines(text: str) -> list[str]:
    if not text:
        return []
    return [line.strip("•- \t") for line in text.split("\n") if line.strip()]


def _split_entries(text: str) -> list[str]:
    """Split a section into entries on blank lines (paragraph breaks)."""
    if not text:
        return []
    blocks = re.split(r"\n\s*\n", text)
    return [b.strip() for b in blocks if b.strip()]