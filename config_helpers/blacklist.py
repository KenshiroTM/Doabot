import re
import string

from config_helpers.general import load_file, save_file

blacklist_name = "blacklist.json"

# Maps special characters to standard ASCII letters (leet speak, unicode, accents)
_CHAR_SUBSTITUTIONS = {
    '4': 'a', '@': 'a', '∆': 'a', 'α': 'a', 'â': 'a', 'ä': 'a', 'à': 'a', 'á': 'a',
    'ã': 'a', 'å': 'a', 'ª': 'a',
    '8': 'b', 'ß': 'b', 'β': 'b',
    '<': 'c', '©': 'c', '¢': 'c', 'ç': 'c',
    'δ': 'd', 'ď': 'd', 'đ': 'd',
    '3': 'e', '€': 'e', '£': 'e', 'ê': 'e', 'ë': 'e', 'è': 'e', 'é': 'e', 'є': 'e',
    'ƒ': 'f',
    '9': 'g', '6': 'g',
    'н': 'h',
    '1': 'i', '!': 'i', '|': 'i', '¡': 'i', 'î': 'i', 'ï': 'i', 'ì': 'i', 'í': 'i', 'ı': 'i',
    'ʝ': 'j',
    'κ': 'k',
    'λ': 'l', 'ł': 'l', 'ĺ': 'l', 'ľ': 'l',
    'μ': 'm',
    'η': 'n', 'ñ': 'n', 'ń': 'n', 'ň': 'n',
    '0': 'o', 'ø': 'o', 'ö': 'o', 'ô': 'o', 'ó': 'o', 'ò': 'o', 'õ': 'o', '°': 'o', 'ο': 'o',
    'ρ': 'p', 'π': 'p', 'þ': 'p',
    'я': 'r', 'ř': 'r', 'ŕ': 'r',
    '5': 's', '$': 's', '§': 's', 'š': 's', 'ś': 's', 'ş': 's',
    '7': 't', '+': 't', '†': 't', 'τ': 't', 'ť': 't', 'ţ': 't',
    'υ': 'u', 'û': 'u', 'ü': 'u', 'ù': 'u', 'ú': 'u', 'ű': 'u',
    'ν': 'v',
    'ω': 'w', 'ŵ': 'w',
    'χ': 'x',
    'γ': 'y', '¥': 'y', 'ÿ': 'y', 'ý': 'y',
    '2': 'z', 'ž': 'z', 'ź': 'z',
}

# Punctuation characters to strip from token edges
_EDGE_PUNCTUATION = string.punctuation + "«»‹›"


def _normalize_text(text: str) -> str:
    """Normalizes text: lowercase, char substitution, removes spaces, collapses repeats."""
    text = text.lower()  # Convert to lowercase

    # Replace special chars with standard ASCII (leet speak, unicode)
    normalized = [_CHAR_SUBSTITUTIONS.get(ch, ch) for ch in text]
    text = ''.join(normalized)

    # Remove spaces (catches spaced slurs aka S L U R)
    text = text.replace(' ', '')

    # Exceptions: keep g doubled on long repeats (most popular slurs use these)
    text = re.sub(r'g{3,}', 'gg', text)

    # Everything else: 3+ repeats → 1 char (e.g. "iiiii" → "i", "rrrrr" → "r")
    text = re.sub(r'(.)\1+', r'\1', text)

    return text


def _normalize_token(token: str) -> str:
    """Normalizes a single token: strips edge punctuation + full normalization."""
    token = token.strip(_EDGE_PUNCTUATION)  # Cut off !?., etc. from start/end
    return _normalize_text(token)


def _tokenize(text: str) -> list[str]:
    """Splits text into alphanumeric tokens using regex.
    This ensures 'code123slur456' is treated as one token,
    while 'hello slur world' splits into ['hello', 'slur', 'world']."""
    return re.findall(r'\w+', text)


def check_blacklist(message: str, data: dict) -> dict | None:
    """
    Checks message against blacklist words.
    Sensitive: substring match anywhere in text (catches "xxslurxx" "s l u r" "5lur" and all combined).
    Insensitive: exact token match (whole word only, does not fire false alarm on links, codes etc).
    """

    # --- SENSITIVE: substring match in entire message ---
    sensitive_words = data.get("sensitive", [])
    normalized_message = _normalize_text(message)  # Normalize full message

    for word in sensitive_words:
        normalized_word = _normalize_text(word)  # Normalize blacklist word
        if normalized_word in normalized_message:  # Word appears anywhere?
            return {
                "matched_word": word,
                "category": "sensitive",
                "original_fragment": message,
            }

    # --- INSENSITIVE: exact token match ---
    insensitive_words = data.get("insensitive", [])
    tokens = _tokenize(message)  # Use regex tokenizer instead of split()

    for word in insensitive_words:
        normalized_word = _normalize_text(word)
        for raw_token in tokens:
            normalized_token = _normalize_token(raw_token)  # Token without edge punctuation
            if normalized_word == normalized_token:  # Exact match
                return {
                    "matched_word": word,
                    "category": "insensitive",
                    "original_fragment": raw_token,
                }

    return None  # Nothing found

def add_blacklisted_word(word: str, case: str="s") -> bool:
    data = load_file(blacklist_name)
    category = "sensitive" if case == "s" else "insensitive"
    word_lower = word.lower()

    if word_lower in data.get(category, []):
        return False
    data.setdefault(category, []).append(word_lower)
    save_file(blacklist_name, data)
    return True


def remove_blacklisted_word(word: str, case: str="s") -> bool:
    data = load_file(blacklist_name)
    category = "sensitive" if case == "s" else "insensitive"
    word_lower = word.lower()

    for i, existing in enumerate(data.get(category, [])):
        if existing == word_lower:
            data[category].pop(i)
            save_file(blacklist_name, data)
            return True
    return False

def get_blacklisted_words(case: str="both") -> list[str] | dict:
    data = load_file(blacklist_name)

    if case == "sensitive":
        return data.get("sensitive", [])
    elif case == "insensitive":
        return data.get("insensitive", [])
    elif case == "both":
        return {
            "sensitive": data.get("sensitive", []),
            "insensitive": data.get("insensitive", [])
        }
    else:
        raise ValueError("Invalid case. Use 'sensitive', 'insensitive', 'both'.")