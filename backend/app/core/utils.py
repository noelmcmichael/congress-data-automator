"""
Utility functions for data processing.
"""
from typing import Dict, Optional

# State name to abbreviation mapping
STATE_MAPPING: Dict[str, str] = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
    'District of Columbia': 'DC',
    'Puerto Rico': 'PR',
    'Virgin Islands': 'VI',
    'Guam': 'GU',
    'American Samoa': 'AS',
    'Northern Mariana Islands': 'MP',
}


def get_state_abbreviation(state_name: str) -> Optional[str]:
    """
    Convert state name to abbreviation.
    
    Args:
        state_name: Full state name
        
    Returns:
        Two-letter state abbreviation or None if not found
    """
    if not state_name:
        return None
    
    # If already an abbreviation, return as is
    if len(state_name) == 2 and state_name.isupper():
        return state_name
    
    # Look up full name
    return STATE_MAPPING.get(state_name.strip())


def get_chamber_name(chamber: str) -> str:
    """
    Convert chamber designation to standard format.
    
    Args:
        chamber: Chamber designation from API
        
    Returns:
        Standardized chamber name
    """
    if not chamber:
        return "Unknown"
    
    chamber_lower = chamber.lower()
    if "house" in chamber_lower:
        return "House"
    elif "senate" in chamber_lower:
        return "Senate"
    else:
        return chamber.title()