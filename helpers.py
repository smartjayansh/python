import requests
import urllib.parse

from flask import redirect, render_template, request, session, url_for
from functools import wraps

#$env:FLASK_ENV = "development"
def lookup(symbol):
    """Look up quote for symbol."""
    # Contact API
    try:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=intitle:{urllib.parse.quote_plus(symbol)}&key=AIzaSyAaVB1rnJ5Yi5o4MBb4gMAzv6pHi6scTfA")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        
        return quote
    except (KeyError, TypeError, ValueError):
        return None


def lookupsub(symbol):
    """Look up quote for symbol."""
    # Contact API
    try:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=subject:{urllib.parse.quote_plus(symbol)}&key=AIzaSyAaVB1rnJ5Yi5o4MBb4gMAzv6pHi6scTfA")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        
        return quote
    except (KeyError, TypeError, ValueError):
        return None

def lookupisbn(symbol):
    """Look up quote for symbol."""
    # Contact API
    try:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{urllib.parse.quote_plus(symbol)}&key=AIzaSyAaVB1rnJ5Yi5o4MBb4gMAzv6pHi6scTfA")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        
        return quote
    except (KeyError, TypeError, ValueError):
        return None