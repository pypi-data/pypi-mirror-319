__all__ = [
    "inches_to_mm",
]

import fractions

mm_per_inch = 25.40

def inches_to_mm(inches: int | float | fractions.Fraction) -> float:
    """Convert inches to millimeters.
    """
    return float(inches) * mm_per_inch


def mm_to_inches(mm: int | float) -> float:
    """Convert millimeters to inches.
    """
    return float(mm) / mm_per_inch
