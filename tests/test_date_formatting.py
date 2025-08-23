#!/usr/bin/env python3
"""
Test script to verify date formatting functionality.
"""

from datetime import datetime

def test_date_formatting():
    """Test the date formatting method."""
    
    # Sample dates from the API
    test_dates = [
        "2025-08-23T12:00:00",
        "2025-08-31T12:00:00",
        "2025-01-15T09:30:00",
        "N/A",
        "",
        None
    ]
    
    print("Testing date formatting...")
    print("=" * 40)
    
    for date_string in test_dates:
        formatted = format_date(date_string)
        print(f"'{date_string}' -> '{formatted}'")
    
    return True

def format_date(date_string: str) -> str:
    """
    Format date string from ISO format to French format.
    
    Args:
        date_string: Date string in ISO format (e.g., "2025-08-23T12:00:00")
        
    Returns:
        Formatted date string (e.g., "23/08/2025")
    """
    if not date_string or date_string == 'N/A':
        return 'N/A'
    
    try:
        # Parse ISO date string
        if 'T' in date_string:
            # Remove time part if present
            date_part = date_string.split('T')[0]
        else:
            date_part = date_string
        
        # Parse the date
        parsed_date = datetime.strptime(date_part, '%Y-%m-%d')
        
        # Format to French date format
        return parsed_date.strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        # If parsing fails, return original string
        return date_string

if __name__ == "__main__":
    test_date_formatting()
