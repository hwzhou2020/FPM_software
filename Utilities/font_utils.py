from functools import lru_cache

from PySide6.QtGui import QFont, QFontDatabase

_FONT_PREFERENCES = [
    "SF Pro Display",
    "Helvetica Neue",
    "Segoe UI",
    "Helvetica",
    "Arial",
    "Ubuntu",
    "Sans Serif",
]

_MONO_FONT_PREFERENCES = [
    "SF Mono",
    "Menlo",
    "Consolas",
    "Fira Code",
    "Source Code Pro",
    "Ubuntu Mono",
    "DejaVu Sans Mono",
    "Liberation Mono",
    "Courier New",
    "Monaco",
    "monospace",
]

_GENERIC_FONT_TOKENS = {
    "sans serif": "sans-serif",
    "sans-serif": "sans-serif",
    "monospace": "monospace",
}


@lru_cache(maxsize=1)
def _available_families():
    """Cache the set of font families reported by Qt to avoid repeated lookups."""
    db = QFontDatabase()
    return set(db.families())


def _family_exists(family: str) -> bool:
    # Generic family names such as "Sans Serif"/"monospace" are always considered available.
    if family.lower() in _GENERIC_FONT_TOKENS:
        return True
    return family in _available_families()


def _format_css_font_token(family: str) -> str:
    token = _GENERIC_FONT_TOKENS.get(family.lower())
    if token:
        return token
    return f"\"{family}\""


def _build_css_stack(preferences, fallback_generic: str) -> str:
    available = []
    seen = set()
    for family in preferences:
        if not _family_exists(family):
            continue
        token = _format_css_font_token(family)
        if token not in seen:
            available.append(token)
            seen.add(token)

    if not available:
        default_family = QFont().defaultFamily()
        available = [f"\"{default_family}\"", fallback_generic]
    return ", ".join(available)


@lru_cache(maxsize=1)
def get_primary_font_family() -> str:
    """Return the first preferred font family that exists on the current platform."""
    for family in _FONT_PREFERENCES:
        if _family_exists(family) and family.lower() not in _GENERIC_FONT_TOKENS:
            return family
    return QFont().defaultFamily()


@lru_cache(maxsize=1)
def get_font_stack_css() -> str:
    """Build a sans-serif font stack string with only available fonts."""
    return _build_css_stack(_FONT_PREFERENCES, "sans-serif")


@lru_cache(maxsize=1)
def get_monospace_font_family() -> str:
    """Return the best available monospace font family."""
    for family in _MONO_FONT_PREFERENCES:
        if _family_exists(family) and family.lower() not in _GENERIC_FONT_TOKENS:
            return family
    fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
    if fixed_font and fixed_font.family():
        return fixed_font.family()
    return QFont().defaultFamily()


@lru_cache(maxsize=1)
def get_monospace_font_stack_css() -> str:
    """Build a monospace font stack string with only available fonts."""
    return _build_css_stack(_MONO_FONT_PREFERENCES, "monospace")


def build_ui_font(point_size: int, weight: int = QFont.Normal) -> QFont:
    """Create a QFont using the best available UI family."""
    font = QFont(get_primary_font_family(), point_size)
    font.setWeight(weight)
    return font


def build_monospace_font(point_size: int, weight: int = QFont.Normal) -> QFont:
    """Create a QFont using the best available monospace family."""
    font = QFont(get_monospace_font_family(), point_size)
    font.setWeight(weight)
    return font
