import random
from config import P, Gx, Gy  # Import constants from config.py

def generate_keys(P, Gx, Gy):
    """Generate a random private-public key pair for testing."""
    private_key = random.randint(1, P - 1)
    public_key_x = (Gx * private_key) % P
    public_key_y = (Gy * private_key) % P
    return private_key, (public_key_x, public_key_y)

# Test function
if __name__ == "__main__":
    private_key, public_key = generate_keys(P, Gx, Gy)
    print(f"Private Key: {private_key}")
    print(f"Public Key: {public_key}")
