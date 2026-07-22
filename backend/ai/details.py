import re

def extract_details(text):

    # Email
    email = "Not Found"
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        email = email_match.group()

    # Phone
    phone = "Not Found"
    phone_match = re.search(r'(\+91[\-\s]?)?[6-9]\d{9}', text)
    if phone_match:
        phone = phone_match.group()

    # Name (First non-empty line)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    name = lines[0] if lines else "Not Found"

    return {
        "name": name,
        "email": email,
        "phone": phone
    }