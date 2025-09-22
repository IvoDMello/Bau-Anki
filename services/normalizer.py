import re
def to_unique_key(text: str) -> str:
    if not text:
        return ""
    t = text.strip().lower()
    t = re.sub(r"[\p{Punct}]+", "", t) if hasattr(re, "P") else re.sub(r"[\W_]+", "", t, flags=re.UNICODE)
    return t
