# file: src/app/security/mfa.py

import random

def generate_mfa_code() -> str:
    return f"{random.randint(0, 999999):06d}"
