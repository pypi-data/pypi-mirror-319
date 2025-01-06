import decimal
from napier.config import P

def custom_summation(P, n):
    """Perform custom summation iteratively to prevent overflow."""
    decimal.getcontext().prec = 100  # Set high precision
    result = decimal.Decimal(0)  # Initialize result as a Decimal
    P = decimal.Decimal(P)  # Ensure P is treated as a Decimal

    for j in range(1, n + 1):
        term = (P ** j) / (j ** 2 + 1)  # Compute the term
        if abs(term) < decimal.Decimal('1e-50'):  # Stop if term becomes negligible
            break
        result += term  # Accumulate the result

    return result

# Test function
if __name__ == "__main__":
    n = 100  # Adjust n based on the desired precision and range
    result = custom_summation(P, n)
    print(f"Custom Summation Result: {result}")
