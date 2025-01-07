import secrets
from decimal import Decimal

def generate_random_512bit():
    """Generate a random 512-bit number."""
    return Decimal(secrets.SystemRandom().getrandbits(512))