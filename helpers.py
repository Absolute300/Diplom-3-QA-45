import re


def parse_int(text):
    return int(re.sub(r"\D", "", text))


def normalize_order_number(order_number):
    normalized = re.sub(r"\D", "", str(order_number))
    return normalized.lstrip("0") or "0"


def extract_order_number(text):
    numbers = re.findall(r"\d{4,}", text)
    if not numbers:
        raise ValueError(f"Order number was not found in text: {text!r}")
    return normalize_order_number(numbers[0])