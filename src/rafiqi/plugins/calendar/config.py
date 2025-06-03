"""Google Calendar configuration"""
import os
from pathlib import Path

# Google Calendar API Configuration
GOOGLE_CALENDAR_CONFIG = {
    'client_config': {
        'web': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'project_id': os.getenv('GOOGLE_PROJECT_ID'),
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'redirect_uris': ['http://localhost:8080/'],
        }
    },
    'scopes': ['https://www.googleapis.com/auth/calendar'],
    'token_file': Path.home() / '.rafiqi' / 'calendar_token.json'
}

# Ensure the config directory exists
GOOGLE_CALENDAR_CONFIG['token_file'].parent.mkdir(parents=True, exist_ok=True) 