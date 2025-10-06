"""
google_search.py - Simple Google search integration for DsD GRC AI
"""
from googlesearch import search

def google_search(query, num_results=5):
    """Returns top Google search result URLs for a query."""
    return list(search(query, num_results=num_results, lang="en"))
