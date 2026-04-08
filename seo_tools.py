"""SEO analysis utilities.

The module provides deterministic and testable helpers for auditing HTML
content and calculating keyword metrics.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Dict, Iterable, List

_WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?", re.IGNORECASE)


@dataclass
class SeoAuditResult:
    """Structured result of an SEO audit."""

    score: int
    checks: Dict[str, bool]
    recommendations: List[str]
    keyword_density: Dict[str, float]


class _SeoHtmlParser(HTMLParser):
    """Extract key SEO elements from HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.in_h1 = False
        self.title = ""
        self.meta_description = ""
        self.h1_text: List[str] = []
        self.body_text: List[str] = []
        self.image_total = 0
        self.image_with_alt = 0

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        attrs_map = {key.lower(): (value or "") for key, value in attrs}

        if tag.lower() == "title":
            self.in_title = True
        elif tag.lower() == "h1":
            self.in_h1 = True
        elif tag.lower() == "meta" and attrs_map.get("name", "").lower() == "description":
            self.meta_description = attrs_map.get("content", "").strip()
        elif tag.lower() == "img":
            self.image_total += 1
            if attrs_map.get("alt", "").strip():
                self.image_with_alt += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False
        elif tag.lower() == "h1":
            self.in_h1 = False

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text:
            return

        self.body_text.append(text)
        if self.in_title:
            self.title += f" {text}" if self.title else text
        if self.in_h1:
            self.h1_text.append(text)


def tokenize(text: str) -> List[str]:
    """Split text into normalized words."""

    return [token.lower() for token in _WORD_RE.findall(text)]


def keyword_density(text: str, keywords: Iterable[str]) -> Dict[str, float]:
    """Calculate keyword density percentages with exact word matching.

    Returns percentages in the range [0, 100], rounded to 2 decimals.
    """

    words = tokenize(text)
    total_words = len(words)
    if total_words == 0:
        return {keyword.lower().strip(): 0.0 for keyword in keywords}

    counts = Counter(words)
    densities: Dict[str, float] = {}
    for keyword in keywords:
        normalized = keyword.lower().strip()
        if not normalized:
            continue

        phrase_tokens = tokenize(normalized)
        if not phrase_tokens:
            continue

        if len(phrase_tokens) == 1:
            occurrences = counts[phrase_tokens[0]]
        else:
            occurrences = 0
            for i in range(total_words - len(phrase_tokens) + 1):
                if words[i : i + len(phrase_tokens)] == phrase_tokens:
                    occurrences += 1

        densities[normalized] = round((occurrences / total_words) * 100, 2)

    return densities


def audit_html(html: str, target_keywords: Iterable[str]) -> SeoAuditResult:
    """Run a practical on-page SEO audit for an HTML document."""

    parser = _SeoHtmlParser()
    parser.feed(html)

    title_len = len(parser.title.strip())
    description_len = len(parser.meta_description)
    text_blob = " ".join(parser.body_text)
    densities = keyword_density(text_blob, target_keywords)

    checks = {
        "title_present": bool(parser.title.strip()),
        "title_length_ok": 50 <= title_len <= 60,
        "meta_description_present": bool(parser.meta_description),
        "meta_description_length_ok": 120 <= description_len <= 160,
        "has_h1": bool(parser.h1_text),
        "image_alt_coverage_ok": parser.image_total == 0
        or parser.image_with_alt == parser.image_total,
        "keywords_used": any(value > 0 for value in densities.values()),
    }

    recommendations: List[str] = []
    if not checks["title_present"]:
        recommendations.append("Add a <title> tag with a concise primary keyword.")
    elif not checks["title_length_ok"]:
        recommendations.append("Keep title length between 50 and 60 characters.")

    if not checks["meta_description_present"]:
        recommendations.append("Add a meta description to improve SERP click-through rate.")
    elif not checks["meta_description_length_ok"]:
        recommendations.append("Keep meta description between 120 and 160 characters.")

    if not checks["has_h1"]:
        recommendations.append("Add a single descriptive <h1> heading.")

    if not checks["image_alt_coverage_ok"]:
        recommendations.append("Ensure every <img> has meaningful alt text.")

    if not checks["keywords_used"]:
        recommendations.append("Use your target keywords naturally in body content.")

    score = round((sum(checks.values()) / len(checks)) * 100)
    return SeoAuditResult(
        score=score,
        checks=checks,
        recommendations=recommendations,
        keyword_density=densities,
    )
