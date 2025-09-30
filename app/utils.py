import phonenumbers
from phonenumbers import NumberParseException

def validate_phone(raw: str, region: str = "KG"):
    try:
        p = phonenumbers.parse(raw, region)
        if not phonenumbers.is_possible_number(p) or not phonenumbers.is_valid_number(p):
            return None
        return phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        return None
