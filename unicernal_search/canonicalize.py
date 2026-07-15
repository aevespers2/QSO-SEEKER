from __future__ import annotations

import re
import unicodedata

ZERO_WIDTH = {"\u200b", "\u200c", "\u200d", "\u2060", "\ufeff"}
BIDI = {"\u061c", "\u200e", "\u200f", "\u202a", "\u202b", "\u202c", "\u202d", "\u202e", "\u2066", "\u2067", "\u2068", "\u2069"}
WHITESPACE = re.compile(r"[\t\r\n\f\v\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+")


def _is_emoji_or_symbol(ch: str) -> bool:
    category = unicodedata.category(ch)
    return category in {"So", "Sk"} or 0x1F000 <= ord(ch) <= 0x1FAFF


def _script(ch: str) -> str | None:
    if not ch.isalpha():
        return None
    name = unicodedata.name(ch, "")
    for script in ("LATIN", "CYRILLIC", "GREEK", "HEBREW", "ARABIC", "HIRAGANA", "KATAKANA", "HANGUL", "CJK"):
        if script in name:
            return script
    return "OTHER"


def canonicalize(text: str, *, metadata: bool = False) -> tuple[str, list[str], list[str]]:
    transformations: list[str] = []
    flags: list[str] = []

    value = unicodedata.normalize("NFKC", text)
    if value != text:
        transformations.append("unicode_nfkc")

    cleaned = "".join(ch for ch in value if ch not in ZERO_WIDTH and ch not in BIDI)
    if cleaned != value:
        transformations.append("removed_invisible_controls")
        flags.append("concealed_unicode")
    value = cleaned

    scripts = {_script(ch) for ch in value}
    scripts.discard(None)
    scripts.discard("OTHER")
    if len(scripts) > 1:
        flags.append("mixed_script_text")

    if metadata:
        cleaned = "".join(ch for ch in value if not _is_emoji_or_symbol(ch))
        if cleaned != value:
            transformations.append("removed_emoji_and_symbols")
            flags.append("emoji_or_symbol_present")
        value = cleaned

    cleaned = WHITESPACE.sub(" ", value).strip()
    if cleaned != value:
        transformations.append("canonicalized_whitespace")
    value = cleaned

    return value, sorted(set(transformations)), sorted(set(flags))
