# file: src/app/security/rate_limit.py

def check_rate_limit(ip: str) -> bool:
    """
    Hook para integrar redis o fastapi-limiter.
    """
    return True
