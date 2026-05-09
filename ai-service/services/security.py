import re


# =========================
# SANITIZE PROMPT INJECTION
# =========================
def sanitize_input(text):

    blocked_patterns = [

        r"ignore previous instructions",

        r"system prompt",

        r"developer message",

        r"act as",

        r"bypass",

        r"jailbreak",

        r"override",

        r"pretend",

        r"roleplay",

        r"disable safety",
    ]

    cleaned_text = text.lower()

    for pattern in blocked_patterns:

        cleaned_text = re.sub(
            pattern,
            "",
            cleaned_text
        )

    return cleaned_text


# =========================
# MASK PII DATA
# =========================
def mask_sensitive_data(text):

    # MASK EMAILS
    text = re.sub(

        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",

        "[EMAIL_MASKED]",

        text
    )

    # MASK PHONE NUMBERS
    text = re.sub(

        r"\+?\d[\d -]{8,12}\d",

        "[PHONE_MASKED]",

        text
    )

    return text