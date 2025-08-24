"""Helper functions for parsing Google Sheets URLs and extracting spreadsheet IDs."""

import re
from typing import Optional


def extract_spreadsheet_id(url_or_id: str) -> str:
    """
    Extract spreadsheet ID from a Google Sheets URL or return the ID if already clean.
    
    Supports various URL formats:
    - https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
    - https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=0
    - https://docs.google.com/spreadsheets/d/SPREADSHEET_ID
    - SPREADSHEET_ID (already clean)
    
    Args:
        url_or_id: Google Sheets URL or spreadsheet ID
        
    Returns:
        Clean spreadsheet ID
        
    Raises:
        ValueError: If the URL format is invalid or ID cannot be extracted
    """
    url_or_id = url_or_id.strip()
    
    # If it's already a clean spreadsheet ID (no slashes or protocol), return as-is
    if not ("/" in url_or_id or ":" in url_or_id):
        if _is_valid_spreadsheet_id(url_or_id):
            return url_or_id
        else:
            raise ValueError(f"Invalid spreadsheet ID format: {url_or_id}")
    
    # Extract ID from Google Sheets URL
    patterns = [
        r"https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)",
        r"docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            spreadsheet_id = match.group(1)
            if _is_valid_spreadsheet_id(spreadsheet_id):
                return spreadsheet_id
            else:
                raise ValueError(f"Extracted ID appears invalid: {spreadsheet_id}")
    
    raise ValueError(f"Could not extract spreadsheet ID from: {url_or_id}")


def _is_valid_spreadsheet_id(spreadsheet_id: str) -> bool:
    """
    Validate that a string looks like a valid Google Sheets spreadsheet ID.
    
    Google Sheets IDs are typically 44 characters long and contain letters, 
    numbers, hyphens, and underscores.
    """
    if not spreadsheet_id:
        return False
        
    # Check length (typical range for Google Sheets IDs)
    if len(spreadsheet_id) < 20 or len(spreadsheet_id) > 60:
        return False
        
    # Check characters (letters, numbers, hyphens, underscores)
    if not re.match(r"^[a-zA-Z0-9-_]+$", spreadsheet_id):
        return False
        
    return True


def validate_google_sheets_url(url: str) -> bool:
    """
    Validate that a URL is a valid Google Sheets URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid Google Sheets URL, False otherwise
    """
    try:
        extract_spreadsheet_id(url)
        return True
    except ValueError:
        return False