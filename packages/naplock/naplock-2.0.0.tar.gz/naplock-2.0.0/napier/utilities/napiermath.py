import numpy as np
from config import P  # Import constants from config.py

def custom_summation(P, n):
    """Perform custom summation as per the NQSF formula."""
    j = np.arange(1, n + 1)
    return np.sum(P ** j / (j ** 2 + 1))

# Test function
if __name__ == "__main__":
    n = 10
    result = custom_summation(P, n)
    print(f"Custom Summation Result: {result}")
