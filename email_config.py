#!/usr/bin/env python3
"""
Email Configuration for Risk Stratification System
Configure your email settings here for sending AI recommendations
"""

import os

# Email Configuration
# Update these settings with your email provider details

# Gmail Configuration (Recommended)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False

# Your Gmail credentials
# Note: Use App Password for Gmail (not your regular password)
MAIL_USERNAME = 'your-email@gmail.com'  # Replace with your Gmail
MAIL_PASSWORD = 'your-app-password'     # Replace with your Gmail App Password
MAIL_DEFAULT_SENDER = 'your-email@gmail.com'  # Replace with your Gmail

# Alternative: Outlook/Hotmail Configuration
# MAIL_SERVER = 'smtp-mail.outlook.com'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USE_SSL = False
# MAIL_USERNAME = 'your-email@outlook.com'
# MAIL_PASSWORD = 'your-password'
# MAIL_DEFAULT_SENDER = 'your-email@outlook.com'

# Alternative: Yahoo Configuration
# MAIL_SERVER = 'smtp.mail.yahoo.com'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USE_SSL = False
# MAIL_USERNAME = 'your-email@yahoo.com'
# MAIL_PASSWORD = 'your-app-password'
# MAIL_DEFAULT_SENDER = 'your-email@yahoo.com'

# Email Content Settings
EMAIL_SUBJECT_PREFIX = "Health Risk Assessment - "
EMAIL_FOOTER = """
---
This is an automated message from your healthcare provider.
For medical emergencies, call 911 or your local emergency number.
Please do not reply to this email.
"""

# Risk Thresholds for Email Sending
HIGH_RISK_LABELS = ['Very High Risk', 'High Risk']

# Email Frequency Settings
MAX_EMAILS_PER_DAY = 100  # Limit to prevent spam
EMAIL_COOLDOWN_HOURS = 24  # Hours between emails to same patient

# Instructions for Gmail App Password:
"""
To use Gmail for sending emails:

1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account settings > Security > App passwords
3. Generate an app password for "Mail"
4. Use that password in MAIL_PASSWORD above
5. Keep your regular Gmail password secure

For other email providers, check their SMTP settings and security requirements.
"""
