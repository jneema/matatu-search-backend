def get_localized(en_value: str | None, sw_value: str | None, lang: str = "en") -> str | None:
    """Return the localized value, falling back to English if SW is missing."""
    if lang == "sw" and sw_value:
        return sw_value
    return en_value