import re

SECTION_HEADERS = {
    "summary": ["summary", "professional summary"],
    "objective": ["objective", "career objective"],
    "experience": ["experience", "work experience", "professional experience", "employment history"],
    "education": ["education", "academic background"],
    "skills": ["skills", "technical skills", "core competencies"],
    "projects": ["projects", "personal projects"],
    "certifications": ["certifications", "licenses & certifications", "certificates"],
    "achievements": ["achievements", "accomplishments"],
    "publications": ["publications"],
    "languages": ["languages"],
}


def detect_sections(text: str) -> dict[str, str]:
    """Split resume text into sections based on common header keywords.

    Returns a dict mapping section name -> raw text content of that section.
    Lines that appear before the first recognized header are ignored here
    (they typically contain contact info, handled separately).
    """
    lines = text.split("\n")
    header_pattern = _build_header_pattern()

    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    for line in lines:
        stripped = line.strip()
        matched_section = _match_header(stripped, header_pattern)

        if matched_section:
            current_section = matched_section
            sections.setdefault(current_section, [])
            continue

        if current_section:
            sections[current_section].append(line)

    return {name: "\n".join(content).strip() for name, content in sections.items()}


def _build_header_pattern() -> dict[str, str]:
    return {
        section: "|".join(re.escape(kw) for kw in keywords)
        for section, keywords in SECTION_HEADERS.items()
    }


def _match_header(line: str, header_pattern: dict[str, str]) -> str | None:
    if not line or len(line) > 50:
        return None

    normalized = line.lower().strip(":").strip()

    for section, pattern in header_pattern.items():
        if re.fullmatch(pattern, normalized):
            return section

    return None