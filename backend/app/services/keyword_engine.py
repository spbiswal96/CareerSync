import re

import spacy

from app.data.skills_taxonomy import SKILLS_TAXONOMY
from app.core.logging import get_logger

logger = get_logger(__name__)

_nlp = spacy.load("en_core_web_sm")

TRAILING_NOISE_WORDS = {"experience", "skills", "knowledge", "background", "understanding", "environment"}
MAX_NGRAM_LENGTH = 3


def extract_keywords(job_description: str) -> dict[str, list[str]]:
    """Extract and categorize keywords from a job description.

    Returns a dict mapping category name -> list of matched keyword strings.
    Unrecognized candidate phrases are dropped (not returned as "Other") to
    keep results high-precision; recall improves as the taxonomy grows.
    """
    doc = _nlp(job_description)
    candidates = _extract_candidate_phrases(doc)

    categorized: dict[str, list[str]] = {}
    seen: set[str] = set()

    for phrase in candidates:
        for sub_phrase in _generate_ngrams(phrase):
            normalized = sub_phrase.lower().strip()
            if normalized in SKILLS_TAXONOMY and normalized not in seen:
                category = SKILLS_TAXONOMY[normalized]
                categorized.setdefault(category, []).append(sub_phrase)
                seen.add(normalized)

    logger.info("Extracted %d categorized keywords from job description", sum(len(v) for v in categorized.values()))
    return categorized


def _extract_candidate_phrases(doc) -> list[str]:
    """Break noun chunks into smaller candidate phrases and split on conjunctions."""
    candidates: list[str] = []

    for chunk in doc.noun_chunks:
        text = chunk.text.strip()
        sub_phrases = re.split(r"\s+and\s+|,\s*", text)
        for sub in sub_phrases:
            cleaned = _strip_trailing_noise(sub.strip())
            if cleaned:
                candidates.append(cleaned)

    for ent in doc.ents:
        candidates.append(ent.text.strip())

    return candidates


def _strip_trailing_noise(phrase: str) -> str:
    words = phrase.split()
    while words and words[-1].lower() in TRAILING_NOISE_WORDS:
        words.pop()
    return " ".join(words)


def _generate_ngrams(phrase: str) -> list[str]:
    """Generate the phrase itself plus all contiguous word n-grams up to
    MAX_NGRAM_LENGTH, so a multi-word chunk like 'a DevOps Engineer with AWS'
    can still match 'DevOps Engineer' or 'AWS' individually."""
    words = phrase.split()
    ngrams = [phrase]

    for size in range(1, min(MAX_NGRAM_LENGTH, len(words)) + 1):
        for i in range(len(words) - size + 1):
            ngrams.append(" ".join(words[i : i + size]))

    return ngrams